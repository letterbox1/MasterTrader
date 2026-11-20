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

**Rust is the default for everything we write**, including the code we borrow ideas or components from (17 §H). Python is allowed only for the short list in §2.2.

| Crate / service | Module | Notes |
|---|---|---|
| `mt-core` | shared types | Instrument, BarSpec, Tick, Event, Signal, OrderIntent, RiskPolicy, JournalEvent, manifest schema, config, clock. Exposed to Python through the same PyO3 module as `pit`, so both languages share one definition |
| (strategies) | M0 | **Strategies are Rust by default**: built-in templates in `crates/mt-engine/src/strategy/`, your own in `strategies/<name>/` (a Rust crate + manifest). Python strategies are allowed only for ML-driven research on the Python node (§2.2) and are ported to Rust (ONNX inference via `ort`) before live. Registry, lifecycle and bots are in `mt-api` |
| `mt-api` | M15 command layer | axum + tokio; OpenAPI via utoipa (`openapi-typescript` generates the web client). REST + WebSocket; Supabase Auth JWTs (§4.6); C0–C3 and preview tokens |
| `mt-risk` | M11 | **One implementation**, linked into `mt-api`, the engine (PyO3 binding for any Python node) and `mt-deadman`; risk golden tests run against the crate |
| `mt-deadman` | M11 layer 2 | Small static binary, own trade-only keys, cancel/flatten only |
| `mt-engine` | M12 | NautilusTrader **Rust live node** where the venue's Rust adapter is production-ready (U, per venue), else the Python node with the same `mt-risk` binding. Custom adapters in Rust where Nautilus has none: Alpaca, OANDA, IG, cTrader, and the AU spot venues Independent Reserve and BTC Markets (U: check Nautilus's adapter list first). ccxt is never used to place orders |
| `mt-recorder` | M1 streaming | Venue WebSocket → Parquet catalog + bars (§4.3); Nautilus Rust data clients where available (U) |
| `mt-connectors` | M1 batch, M5 calendars | **Replaces OpenBB, fredapi, sdmx1, edgartools and yfinance:** typed Rust clients for FRED/ALFRED, EIA, USDA NASS, US Treasury, BLS, ECB/SDMX, CFTC COT, World Bank, IMF, SEC EDGAR (submissions + XBRL `companyfacts` JSON), Dukascopy (`bi5`), data.binance.vision, daily futures from free sources whose terms allow automated personal use (Yahoo chart data only if its terms allow (U)), CoinGecko, DefiLlama, Myfxbook, Finnhub, CryptoPanic, Twelve Data, calendars. Every client writes through `pit` with provenance |
| `mt-scheduler` | batch orchestration | **Replaces Prefect:** Postgres-backed job queue and cron (`apalis`-style), retries, backfills, run history in Postgres, job status on D16/D07. Runs Rust jobs in-process and Python training jobs (§2.2) as containers/subprocesses |
| `mt-features` | M6 | Feature library and evaluator (incremental in the engine, batch via `mt-scheduler`) |
| `mt-nlp` | M2 pipeline (`nlp`) | Relevance gate, entity linking (GLiNER ONNX (U)), FinBERT sentiment (ONNX via `ort`), embeddings and rerank via TEI over HTTP → `text.document` |
| `mt-agents` | M8 | **Rust agent runtime** on `rig-core` (MIT) with an explicit state-machine graph and Postgres checkpoints, replacing LangGraph. Hosts the **TradingAgents-style debate** (rewritten from its Apache-2.0 design, NOTICE kept), the **valuation desk** (FinRobot-style DCF/WACC/comps as deterministic Rust, LLM only for narrative), the **research workflows** (Anthropic financial-services skills; the skill files are prompts, language-neutral) and the optional **persona lenses**. All model calls go through the LiteLLM gateway |
| `mt-memory` | M9 | RAG (hybrid pgvector + tsvector, TEI rerank) and the Hindsight client (HTTP); decision settlement |
| `mt-models` | M21 runtime | Tier A inference (ONNX via `ort`), tier B client (SemIf readout via the vLLM server; own head via ONNX), model registry, question registry, labels |
| `mt-anomaly` | M10 | Detectors (statistical, streaming) + the explain agent on `mt-agents` |
| `mt-lab-core` | M7 (production side) | Walk-forward and validation harness, **bias analysers** (look-ahead and recursive-formula checks, clean-room from freqtrade's ideas, no GPL code), **setup-odds simulator** (R2.59), cost models, gate reports; drives Nautilus Rust backtests. The Python lab (§2.2) calls it through PyO3 |
| `mt-crowdsim` | M14 | **Scenario & crowd simulator** (§2.4), clean-room Rust on the OASIS/MiroFish idea; no MiroFish or OASIS code |
| `mt-airdrop`, `mt-airdrop-exec` | M4 | Discovery, enrichment, risk/viability scoring, EV gate; mandated claims, simulation, revokes, sweeps |
| `mt-curation` | M19 | Task queue, digests, community verification |
| `mt-social` | M23 | Drafts → your approval → web intent; credibility and shill-burst posture |
| `mt-onchain`, `mt-treasury`, `mt-signer` | 13, M22 | Chain reads, cost gate (`mt_onchain::costgate`), indexer, hold-and-earn; intents-only signer (alloy, Solana SDK) |
| `mt-journal` | M18 | Lot engine, tax rules (`rust_decimal`), reports, exports; tax golden tests in the crate |
| `mt-feeds` | M2 sources | RSS/Atom (incl. rss-bridge output), the Discord feeds bot, Bluesky, Mastodon, Farcaster and GDELT clients → `raw.text.*` on the `scrape` network; article text extraction is handed to `mt_extract` (§2.2) |
| `mt-events`, `mt-intel-writer` | M3, M2/M3 writer | Event pollers (USGS, GDACS, NOAA, FIRMS, ReliefWeb, UCDP, ACLED, Kalshi, Polymarket, congressional disclosures R4.17); INSERT-only writer for scrape outputs |
| `mt-monitor`, `mt-store`, `mt-obs` | M16, `pit`, M17 | DQ/costs/recon/egress; `pit` + WORM helpers (PyO3 bindings); WORM writer, hash chain, seal |
| `mt-telegram-bot`, `mt-mcp` | M15, M20 | teloxide bot; `rmcp` MCP adapter over `mt-api` |
| `mt-mm-adapter` | M13 | Rust client of the **Hummingbot API** (REST + WebSocket); Hummingbot itself runs unmodified in its own container |

### 2.2 Python (uv workspace, `packages/`): only where absolutely required

| Package | Why Python is required | Boundary |
|---|---|---|
| `mt_research` (lab exploration + training + offline batch reports) | The ML and research ecosystem has no Rust equivalent: PyTorch, LightGBM, scikit-learn, Optuna, Qlib, vectorbt, LoRA/FinBERT fine-tuning, notebooks, MLflow client. Also the nightly offline batch jobs that use Python-only libraries: Pandera/Evidently DQ reports, `exchange_calendars` table generation and the optional akshare daily Asia futures backfill (all written to Postgres through the `mt_store` binding for the Rust services) | Trains and explores only. Promoted models are exported to **ONNX** and run in Rust; reads data only through the `pit` binding; runs as `mt-scheduler` jobs |
| `mt_extract` (`ingest-text` extraction) | trafilatura's article extraction quality has no Rust match (U); crawl4ai (container) for JS pages | On the `scrape` network; publishes `raw.text.*` only |
| `mt_telegram_reader` | **Telethon** for MTProto: the Rust option (grammers) was archived in Feb 2026 and is unaudited | Scrape side; regex postures only (`posture.telegram.*`), never text to models |
| `mt_ledger_import` | ccxt's ledger/statement endpoints across many exchanges (historical accounts) | Hands normalised events to `mt-journal` |
| `mt_mt5_bridge` (optional, Windows VPS) | The `MetaTrader5` package is Windows/Python-only | Executes only orders that already passed `mt-risk` in `mt-engine`'s MT5 adapter; no decisions of its own |

**Also Python, but not ours to run:** LiteLLM loads its callbacks as Python, so the `audit.llm_call` writer is a small plugin file mounted into the unmodified LiteLLM container (P0-T042). It only writes audit rows through the `mt_store.obs` binding.

**Rules:** Python never places orders, signs, or runs on the live decision path. It publishes to NATS or calls `mt-api`; reads only through `pit`; writes audit rows through the `mt-obs` binding (`mt_store.obs`), so the hash chain has one implementation.

### 2.3 Third-party services (any language, run unmodified as pinned containers)

Their language doesn't matter to us: we run them as they are and talk to them over HTTP, NATS or SQL. Full list with language, licence and what we'd do for an open-source release: [19](19-third-party-register.md).

NATS JetStream, Supabase stack, Caddy, LiteLLM, MLflow, TEI, llama-server / vLLM, Hindsight, LightRAG (optional), rss-bridge, crawl4ai, Hummingbot (+ Hummingbot API), Anvil, Grafana/Loki/Prometheus/Alertmanager/Vector, ntfy.

### 2.4 Scenario & crowd simulator (M14): a go-live tool

- **What it does:** turns a headline or event into a simulated crowd reaction: a population of LLM persona agents (retail, funds, market makers, media, bots), seeded and recorded. The output is a **scenario**: a sentiment path plus price, volatility, spread and liquidity shocks.
- **Where it's used:**
  - **During the 8-week paper period:** a **scenario twin**, a second paper engine running the same bots on replayed live data with injected scenarios, shows how each bot behaves under shocks the real market hasn't produced yet. It's a weekly report per bot, part of the weekly review pack.
  - **In the stress tests:** alongside the four historical shocks before live (P7-T069).
- **Storage:** `risk.sim_*` (simulator runs and scenarios) and `risk.twin_*` (twin runs and reports), every row `synthetic = true`.
- **Boundaries:**
  - It never trades the real paper or live accounts.
  - Its data is flagged `synthetic = true` and never enters features, model training or RAG.
  - It runs isolated with no route to the signer.
  - LLM calls use the local model by default, inside the budget.
- **Build early:** its tasks depend only on the paper engine (P2), the local model and gateway (P0) and the event feeds, not on the rest of Phase 6, so with dependency gating it's built alongside Phase 2 and can join the 8-week paper period from its first weeks. Paper weeks that run before it's ready simply have no twin report.
- **Why clean-room Rust:** MiroFish is AGPL-3.0, needs Zep Cloud and ships insecure defaults (01 §3.9). We take the idea, not the code.

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
| 1s bars + continuous aggregates 1m, 5m, 15m, 1h, 4h, 1D, 1W | `mt-recorder` writes 1s bars and every standard size directly as it builds bars from ticks. Backfills and corrections re-run a rollup job that rebuilds the affected higher sizes from 1m (idempotent, upsert by key) |
| `time_bucket` for other sizes | `date_bin()` at read time, inside `pit(as_of)` |
| Native compression | Raw ticks and L2 already live in the Parquet catalog. Bars older than `db.bars_hot_months` (16 §2.15) are exported to Parquet and dropped from Postgres partitions; `pit(as_of)` reads both transparently. Defaults: 1s bars stay in Postgres for `db.bars_1s_hot_days` (90 days) and then live only in Parquet; 1m and larger stay in Postgres for good on the workstation, 24 months of 1m bars in the cloud |

### 4.4 Point-in-time and WORM

- `pit(as_of)` stays the only research read path; the CI guard (no direct table reads in research code) covers Rust and Python.
- WORM is unchanged ([15 §2](15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)): an offline `worm_owner` role owns the WORM tables, app roles are INSERT/SELECT only, blocking triggers, per-row hash chain, daily externally anchored seal.
- WORM DDL (migrations tagged `-- mt:worm`) is applied by a separate step that connects as `worm_owner` with the offline credential, not by the routine `supabase migration up` (U: whether the CLI can run a migration subset as another role; otherwise `mt worm migrate` runs them with `psql`).
- **Cloud caveat:** on Supabase cloud the platform operator holds the real superuser. That can't stop a privileged operator from altering rows, so the external seal is what proves tampering; it's unchanged and runs in every mode.

### 4.5 Access rules

- **The browser never talks to the database.** Every read and command goes through `mt-api`, so the "one command layer" principle holds. Row-level security is enabled on every table with no policies for the `anon` and `authenticated` roles (deny all).
- The Supabase Data API (PostgREST) and Realtime are **off** for MasterTrader schemas by default (`supabase.data_api: off`, `supabase.realtime: off`). Live streams come from NATS through `mt-api`'s WebSocket.
- Supabase Storage holds private buckets for reports, tax exports and attachments.

### 4.6 Auth

- **Supabase Auth** replaces the hand-built login: your one account, password plus **TOTP MFA** (enrolment required; sign-ups disabled). Passkeys if Supabase supports them as MFA by then (U).
- `mt-api` verifies the Supabase JWT (asymmetric signing keys, JWKS) and requires the MFA level `aal2` for every command.
- **Telegram (bot and Mini App):** Telegram can't carry a Supabase session. `mt-api` verifies the Telegram `initData` signature for your one linked Telegram user, and asks for a TOTP code (checked against the same Supabase MFA factor (U); if Supabase can't verify a code server-side outside a browser session, `mt-api` verifies it against a separate Telegram TOTP factor you enrol once) before C3 actions, then issues a short-lived command session at `aal2` strength (default 15 min). Same C0–C3 rules as the web.
- **No recovery codes:** Supabase Auth has none. Enrol a second TOTP factor on another device as your backup; if both are lost, the break-glass `mtctl auth reset-mfa` on the workstation (local shell, offline `worm_owner`-style credential) resets them and is audited.
- C0–C3 confirmations, preview tokens, the session limits in [16 §2.14](16-configuration-and-safety-model.md#214-platform--operations) and the break-glass `mtctl` CLI are unchanged.

### 4.7 Backups

| Mode | Backups |
|---|---|
| Workstation | pgBackRest (or WAL-G) in a sidecar container sharing the Postgres data volume, fed by `archive_command`: the Supabase Postgres image doesn't ship pgBackRest (U: confirm the sidecar setup). WAL archive, nightly incremental, weekly full, + restic off-site, as before |
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
| NATS JetStream, `mt-scheduler`, `mt-monitor`, ingest | Stateful and always on |
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
4. **Strategies are Rust by default** (§2.1). An ML-driven strategy may start in Python for research and paper; before live its model is exported to ONNX and the strategy runs in Rust.

## 10. Sources

Checked 2026-11-19; re-verify before relying on them (agents' RESEARCH tasks do).
- Vercel Rust runtime (public beta) and function limits: vercel.com/docs/functions/runtimes/rust, vercel.com/docs/functions/limitations.
- Supabase TimescaleDB deprecation on Postgres 17 and pg_partman migration guide: supabase.com/docs/guides/database/extensions/timescaledb, supabase.com/docs/guides/database/migrating-to-pg-partman.
- Supabase free plan (500 MB, pause after 7 days idle) and Pro pricing: supabase.com/pricing (third-party summaries agree).
- Supabase read replicas: supabase.com/docs/guides/platform/read-replicas.
- NautilusTrader Rust-native strategies and live node: nautilustrader.io/docs/latest/concepts/overview, release notes 1.228–2.0.0rc.
