# MasterTrader — Platform & Deployment (v4 stack)

This doc is canonical for **which language each service is written in, where each part runs, the database, and how the system moves from your workstation to the cloud**. It supersedes the stack choices in [02 §3](02-v1-architecture.md#3-deployment-topology), [02 §5.1](02-v1-architecture.md#51-stores), [02 §10](02-v1-architecture.md#10-frontend-architecture) and [03 §2–3](03-build-spec.md#3-repository-layout) wherever they differ. Behaviour (modules M0–M23, risk, WORM, `pit`, HITL) is unchanged.
- Decision record: [17 §G](17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19).
- Configurable defaults: [16 §2.15](16-configuration-and-safety-model.md#215-platform-deployment-and-regions).
- Facts marked **(U)** are unverified; an agent RESEARCH task checks each one before the build that relies on it.

**Contents:**
1. Summary
2. Language split: Rust first, Python where necessary
3. Repository layout
4. Database: Supabase Postgres
5. Deployment modes
6. What can't run on Vercel, and why
7. Latency and regions
8. Tailscale and the hardware key, per mode
9. Workstation-first build path
10. Sources

---

## 1. Summary

- **Backend:** Rust for every service we write, unless a Python-only library makes Python necessary (§2). The trading engine stays **NautilusTrader**, whose core is Rust; strategies can be Rust or Python on the same engine.
- **Frontend:** the React + TypeScript web app (`apps/web`), built once. The same bundle is served locally (Caddy) or deployed to **Vercel**.
- **Database:** **Supabase Postgres**, run locally (Supabase CLI for development and tests, the self-hosted Supabase stack on the always-on workstation) or on **Supabase cloud** if you choose. One set of SQL migrations deploys to both.
- **Where things run:** the whole system runs on your **workstation** first: built, tested and paper-traded there. Shifting to the cloud later is a set of OPS tasks, not a rewrite. The always-on trading services (engine, dead-man, recorder, event bus) never run as Vercel Functions (§6).
- **Regions:** one region by default (Sydney). Optional per-venue regional engines come later, only when measured slippage shows they pay for themselves (§7).

## 2. Language split: Rust first, Python where necessary

### 2.1 Rust (Cargo workspace, `crates/`)

| Crate / service | Module | Replaces | Notes |
|---|---|---|---|
| `mt-core` | shared types | `mt_core` | Instrument, BarSpec, Tick, Event, Signal, OrderIntent, RiskPolicy, JournalEvent, config, clock. Exposed to Python through the same PyO3 module as `pit`, so both languages share one definition |
| `mt-api` | M15 command layer | FastAPI `mt_api` | axum + tokio; OpenAPI generated with utoipa, so `openapi-typescript` still generates the web client. REST + WebSocket; verifies Supabase Auth JWTs (§4.6); C0–C3 confirmation and preview tokens unchanged |
| `mt-risk` | M11 | `mt_risk` | **One implementation**: linked into `mt-api` (policy, previews), the engine (pre-trade checks, via a PyO3 binding where the strategy or node is Python) and `deadman`. Risk golden tests run against the crate |
| `mt-deadman` | M11 layer 2 | `mt_risk.deadman` | Small static binary, own trade-only keys, cancel/flatten only |
| `mt-engine` | M12 | `mt_engine` | NautilusTrader **Rust live node** where the venue's Rust adapter exists and is production-ready (U, per venue); otherwise the Python node with the same `mt-risk` binding. Custom adapters (Alpaca, OANDA, IG, cTrader) are written in Rust against Nautilus's adapter traits |
| `mt-recorder` | M1 (streaming part) | `mt_data.market` recorder + bar builder | Venue WebSocket → Parquet catalog + standard bar sizes (§4.3). Uses Nautilus Rust data clients where available (U) |
| `mt-monitor` | M16 | `mt_monitor` | Data quality, costs/TCA, reconciliation, egress check |
| `mt-store` | `pit(as_of)`, WORM helpers | `mt_store` | `pit` is a Rust library with **Python bindings** (PyO3), so Rust and Python research share one point-in-time read path. sqlx with compile-time-checked queries |
| `mt-obs` | M17 | `mt_obs` | WORM writer, hash chain, daily seal, integrity response, tracing/metrics |
| `mt-signer` | 13 §2 | `mt_signer` | Intents-only signer (alloy for EVM, Solana SDK for Solana); keys never leave it |
| `mt-journal` | M18 lot engine + tax | `mt_journal` (compute part) | `rust_decimal`; tax golden tests against the crate. Statement parsing that needs a Python-only parser stays in Python behind it |
| `mt-events` | M3 | `mt_data.events` | Simple REST/feed pollers (USGS, GDACS, NOAA, FIRMS, ReliefWeb, UCDP, Kalshi, Polymarket) |
| `mt-telegram-bot` | M15 alerts, approvals, `/kill` | python-telegram-bot | teloxide (Bot API). Reading channels is different: see Telethon below |
| `mt-mcp` | M20 (Phase 8) | `mt_mcp` | Official Rust MCP SDK (`rmcp`); still a thin adapter over `mt-api` |
| `mt-onchain`, `mt-treasury` (indexer, cost gate), `mt-airdrop-exec` | M4 exec, M22 | Python packages | Chain reads, simulation calls to Anvil, mandates, revokes, sweeps |

### 2.2 Python (uv workspace, `packages/`): only where necessary

| Package | Why Python is necessary |
|---|---|
| `mt_strategy` (Python strategies), `mt_lab` | Nautilus's Python strategy API and backtest tooling, plus the research stack (pandas/polars, vectorbt, Optuna, MLflow client). Deterministic strategies can be written in Rust instead (§9 step 4) |
| `mt_features` (research side), `mt_models` (training), `mt_anomaly` | PyTorch, LightGBM, scikit-learn, Qlib, FinBERT. **Inference** can move to Rust (ONNX via `ort`) when a model is promoted to the engine path (tier A) |
| `mt_agents`, `mt_memory` | LangGraph, TradingAgents, FinRobot, Hindsight client, RAG tooling |
| `mt_data` batch flows (Prefect) | Python-only SDKs: OpenBB, edgartools, yfinance, fredapi, sdmx1, Dukascopy/ccxt helpers |
| `mt_data.text` (`ingest-text`, `nlp`) | Telethon (MTProto, Python-only), trafilatura, crawl4ai, spaCy/FinBERT |
| `mt_airdrop` (discovery and scoring), `mt_curation`, `mt_social` | Python data and LLM tooling; anything that signs goes through the Rust signer |

**Rule:** Python services never place orders or sign. They publish to NATS or call `mt-api`, so every order still passes `mt-risk`, and research still reads only through `pit(as_of)` (the Python binding of the Rust implementation).

### 2.3 Third-party services (any language, run as pinned containers)

NATS JetStream, Supabase stack, Caddy, LiteLLM, MLflow, TEI, llama-server / vLLM, Hindsight, rss-bridge, crawl4ai, Hummingbot, Anvil, Grafana/Loki/Prometheus/Alertmanager/Vector, ntfy. Images are pinned by digest as before.

## 3. Repository layout

```
MasterTrader/
├── Cargo.toml / Cargo.lock       # Rust workspace
├── crates/                       # Rust crates (§2.1)
├── pyproject.toml / uv.lock      # uv workspace (Python only where necessary)
├── packages/                     # Python packages (§2.2)
├── apps/web/                     # React + TypeScript SPA; vercel.json for the optional Vercel deploy
├── supabase/                     # config.toml, migrations/*.sql (all 13 schemas), seed.sql, tests (pgTAP)
├── infra/                        # compose files per mode (§5), caddy, observability, sops config (no secrets), host provisioning
├── services/ strategies/ third_party/ notebooks/ tests/ docs/ brand/ DESIGN.md
```

- **Migrations:** plain SQL in `supabase/migrations/`, replacing Alembic. Applied locally with `supabase db reset` / `supabase migration up`, and to the cloud project with `supabase db push`. pgTAP tests (`supabase test db`) hold the schema, WORM and `pit` invariants.
- **Builds:** `cargo` for Rust, `uv` for Python, `pnpm` for the web app. One `just` (or `make`) entry point runs the lot.

## 4. Database: Supabase Postgres

### 4.1 Where it runs

| Mode | How | Cost |
|---|---|---|
| **Development and tests** | Supabase CLI: `supabase start` runs the full local stack in Docker (Postgres, Auth, Storage, Studio). CI and agents use the same | Free |
| **Workstation (always-on)** | Self-hosted Supabase (the official Docker Compose setup) on the workstation, same images and migrations | Free |
| **Supabase cloud** (optional, at shift time) | A Supabase project in the region nearest the engine (default Sydney, `ap-southeast-2`); `supabase link` + `supabase db push` | **Paid.** The free plan is capped at 500 MB and pauses after 7 days idle, so it can't hold a trading system; Pro is about US$25/month plus compute (§10). A USER decision at shift time |
| **Supabase cloud + read replicas** (optional) | Read replicas in other regions for dashboards and reports far from the primary | Paid; needs larger compute (U) |

### 4.2 Extensions

pgvector, pg_trgm, pgcrypto, pg_cron, pgTAP, and pg_partman if available (U). **TimescaleDB is not used**: Supabase has deprecated it on Postgres 17, and new projects run 17.

### 4.3 Bars without TimescaleDB

| Was (TimescaleDB) | Now |
|---|---|
| Hypertables | Native range partitioning by month on `market.bar_*`; partitions created ahead by pg_partman where available, otherwise by an `mt-store` partition job scheduled with pg_cron (U: check pg_partman on the target Postgres 17) |
| Continuous aggregates 1m, 5m, 15m, 1h, 4h, 1D, 1W | `mt-recorder` writes every standard size directly as it builds bars from ticks. Backfills and corrections re-run a rollup job that rebuilds the affected higher sizes from 1m (idempotent, upsert by key) |
| `time_bucket` for other sizes | `date_bin()` at read time, inside `pit(as_of)` |
| Native compression | Raw ticks and L2 already live in the Parquet catalog. Bars older than `db.bars_hot_months` (16 §2.15) are exported to Parquet and dropped from Postgres partitions; `pit(as_of)` reads both transparently. Default: keep all bars in Postgres on the workstation; 24 months of 1m bars in the cloud |

### 4.4 Point-in-time and WORM

- `pit(as_of)` stays the only research read path; the CI guard (no direct table reads in research code) covers Rust and Python.
- WORM is unchanged ([15 §2](15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)): an offline `worm_owner` role owns the WORM tables, app roles are INSERT/SELECT only, blocking triggers, per-row hash chain, daily externally anchored seal.
- **Cloud caveat:** on Supabase cloud the platform operator holds the real superuser. That can't stop a privileged operator from altering rows, so the external seal is what proves tampering; it's unchanged and runs in every mode.

### 4.5 Access rules

- **The browser never talks to the database.** Every read and command goes through `mt-api`, so the "one command layer" principle holds. Row-level security is enabled on every table with no policies for the `anon` and `authenticated` roles (deny all).
- The Supabase Data API (PostgREST) and Realtime are **off** for MasterTrader schemas by default (`supabase.data_api: off`, `supabase.realtime: off`). Live streams come from NATS through `mt-api`'s WebSocket.
- Supabase Storage holds private buckets for reports, tax exports and attachments.

### 4.6 Auth

- **Supabase Auth** replaces the hand-built login: your one account, password plus **TOTP MFA** (enrolment required; sign-ups disabled). Passkeys if Supabase supports them as MFA by then (U).
- `mt-api` verifies the Supabase JWT (asymmetric signing keys, JWKS) and requires the MFA level `aal2` for every command.
- C0–C3 confirmations, preview tokens, the session limits in [16 §2.14](16-configuration-and-safety-model.md#214-platform--operations) and the break-glass `mtctl` CLI are unchanged.

### 4.7 Backups

| Mode | Backups |
|---|---|
| Workstation | pgBackRest against the Supabase Postgres container (WAL archive, nightly incremental, weekly full) + restic off-site, as before |
| Supabase cloud | Supabase's managed daily backups; point-in-time recovery is a paid add-on (USER decision). Our own nightly logical dump to restic still runs, so recovery never depends on one provider |
| Every mode | Monthly restore test and the monthly immutable WORM export, unchanged |

## 5. Deployment modes

| | **Mode 1: Workstation** (default) | **Mode 2: Hybrid cloud** (optional shift) | **Mode 3: Regional engines** (optional, later) |
|---|---|---|---|
| Web app | Served locally by Caddy | **Vercel** (static build of `apps/web`) | Vercel |
| `mt-api` | Workstation | Runtime host | Primary runtime host |
| Engine, dead-man, recorder, monitor, NATS, workers, signer, local models | Workstation | **Runtime host**: your workstation, a home server, or a cloud VM in Sydney | One runtime host per venue region (§7) |
| Database | Self-hosted Supabase on the workstation | Supabase cloud (Sydney) | Supabase cloud primary + read replicas |
| Exchange egress IP | Your broadband IP (paper/testnet); fixed egress exit node from P7 | The runtime host's static IP, or the exit node | Each region's own static IP |
| Cost | Free (power and broadband) | Vercel Hobby is free for personal use (U); Supabase Pro paid; a VM is optional | Paid per region |

**Browser → API in Mode 2.** The Vercel-hosted page is static; your browser calls `mt-api` on the runtime host:
- **Default `api.exposure: tailnet`:** `mt-api` stays private on Tailscale, so your phone or laptop needs Tailscale on to use the app. Nothing on the runtime host is open to the internet.
- **Option `public`:** `mt-api` behind a public HTTPS endpoint (Caddy with a real certificate, or a tunnel) with Supabase Auth + TOTP on every request, a strict CORS allow-list for the Vercel domain, and rate limits. Changing to `public` is C3.

**Vercel Functions** (Rust, Python or containers) are optional and only for stateless, short work: e.g. a read-only status endpoint or scheduled report rendering. **Never** in the order path, never holding exchange keys.

## 6. What can't run on Vercel, and why

| Service | Why not Vercel |
|---|---|
| Engine, `deadman`, `mt-recorder` | Must run continuously and hold venue WebSockets. Vercel Functions scale to zero and have a maximum duration (300 s default, 800 s max on paid plans, (U) for container functions); WebSockets are limited by the same duration |
| Anything that calls an exchange | Exchange keys are IP-locked; Vercel functions and containers don't get a static egress IP on standard plans (U) |
| NATS JetStream, Prefect workers, `mt-monitor`, ingest | Stateful and always on |
| Local models (TEI, llama-server, vLLM), backtest workers | Need a GPU or long CPU runs and local disk |
| Signer | Keys must stay on a host you control |

## 7. Latency and regions

**What helps latency and what doesn't:**
- Order latency is the distance between the **engine** and the **exchange's matching engine**. Database read replicas don't change it.
- From Sydney, Asian venues are roughly 100 ms+ away (U, measure). That matters for sub-second strategies; for minute-to-day horizons it's noise next to spread and fees.
- MasterTrader already measures this: M16 TCA records the slippage and time-to-ack per venue.

**Default:** one region (Sydney) for the engine and the database (`deploy.engine_regions: [syd]`).

**Regional engines (Mode 3) are allowed only when all of these hold** (checked by `mt-monitor` and the deploy tooling):
1. **Measured benefit:** M16 shows latency-attributable slippage on a bot above `deploy.region_min_benefit_bps` over at least `deploy.region_eval_trades` live or paper trades.
2. **Jurisdiction:** the region is one where the venue serves an Australian-resident account; never a region used to reach a venue or product you couldn't otherwise use. This keeps the no-location-masking rule ([12 §3](12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention)). The venue registry carries the allowed regions.
3. **Keys:** each region has its own static egress IP, added to that venue's key allow-list; each region has its own `deadman` and venue timers.
4. **One risk authority:** portfolio limits stay global. Each region gets a pre-allocated slice of the risk budget, so its local `mt-risk` checks need no cross-region round trip. The primary reconciles every `risk.region_sync_s` seconds and can shrink a slice to zero. Changing allocations or adding a region is C3.

**Database regions:** the primary sits with the primary engine. Read replicas (cloud only) serve dashboards and reports elsewhere; writes always go to the primary.

## 8. Tailscale and the hardware key, per mode

**Tailscale** is a private network between your own devices. MasterTrader uses it for four things:
1. Your phone and laptop reach the app and API without any port open to the internet.
2. SSH to the runtime host for maintenance and the break-glass `mtctl approve`.
3. ntfy push and (Phase 8) the MCP endpoint stay private.
4. The fixed-IP **egress exit node** at go-live: broadband and 4G both tunnel to one Sydney static IP, the only IP on your IP-locked exchange keys.

| Mode | Tailscale |
|---|---|
| Workstation, working at the machine | **Not needed.** Everything is on localhost |
| Workstation, using your phone | Needed for phone access (free personal plan) |
| Hybrid cloud | Needed with `api.exposure: tailnet` (default); optional with `public` |
| Go-live (P7) | Needed for the egress exit node, unless the runtime host is itself a VM with a static IP |

**Hardware key (YubiKey)** holds the **age** private keys that decrypt the secrets file (exchange keys, LLM keys, bot tokens). Two identities:
- **host:** decrypts the runtime secrets at start-up;
- **offline:** used only for the `worm_owner` database credential and to recover the secrets file.

If the disk or a backup is stolen, the secrets stay encrypted, because the key that opens them isn't on that disk.

| Stage | Where the age keys live |
|---|---|
| Build, tests, paper and testnet | OS keychain (or a passphrase-protected age file) is enough: no real money is at stake |
| Before live money (P7) | YubiKey for both identities: the default from P7 (`secrets.age_identity_store: yubikey`, [16 §2.15](16-configuration-and-safety-model.md#215-platform-deployment-and-regions)), done in P7-T072 ([07 §2](07-security-notes.md#2-secrets)) |

## 9. Workstation-first build path

1. **Phases 0–6 build and test on your workstation** with the Supabase CLI stack, Docker Compose and keyless fixtures (build first, keys last). GPU is optional: CPU profiles for TEI and the local model are the default; a GPU profile switches on automatically if one is detected.
2. **Paper and testnet** run on the workstation (Mode 1).
3. **The shift (Phase 7, before live money)** is a set of OPS tasks:
   1. choose the runtime host;
   2. optionally deploy `apps/web` to Vercel;
   3. optionally `supabase link` + `db push` to a cloud project and migrate data;
   4. set up the egress IP;
   5. rerun the full verification suite on the target.

   Live money only starts after that suite passes on the target.
4. **Rust vs Python per strategy:** deterministic strategies may be written in Rust from the start. ML-driven ones start in Python and are ported only when profiling shows a need.

## 10. Sources

Checked 2026-11-19; re-verify before relying on them (agents' RESEARCH tasks do).
- Vercel Rust runtime (public beta) and function limits: vercel.com/docs/functions/runtimes/rust, vercel.com/docs/functions/limitations.
- Supabase TimescaleDB deprecation on Postgres 17 and pg_partman migration guide: supabase.com/docs/guides/database/extensions/timescaledb, supabase.com/docs/guides/database/migrating-to-pg-partman.
- Supabase free plan (500 MB, pause after 7 days idle) and Pro pricing: supabase.com/pricing (third-party summaries agree).
- Supabase read replicas: supabase.com/docs/guides/platform/read-replicas.
- NautilusTrader Rust-native strategies and live node: nautilustrader.io/docs/latest/concepts/overview, release notes 1.228–2.0.0rc.
