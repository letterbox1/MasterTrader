# MasterTrader — Build Spec (personal-use edition, v2)

**Context:** a proprietary, private, single-user platform. The aim is **minimal hoops**: use whatever works best (including GPL/AGPL code), self-host (your workstation first, [18](18-platform-and-deployment.md)), **free data and free tiers only**, and keep only the disciplines that protect money, records and future options.

**Design stance:** MasterTrader is a **platform, not a strategy**.
- It doesn't presume any trading style or timeframe.
- Any strategy type can be built, backtested, simulated, paper-traded and run live on any timeframe, from **tick / order-book level up to daily-and-above**.
- Strategies, risk limits and preferences are **user inputs** (UI, Telegram, and later MCP), not things baked into the code.
- Every number in this spec that shapes trading (limits, thresholds, timers, gates) is a **default you can change**, not a hard rule. The reference values live in [16](16-configuration-and-safety-model.md); where this spec and 16 differ, 16 wins.

Companion docs:
- [07 security notes](07-security-notes.md)
- [08 airdrops & curation](08-airdrops-and-token-launches.md)
- [09 journal & tax](09-journal-and-tax.md)
- [06 data sources](06-aggregators-and-market-providers.md)
- [04 plan of action](04-plan-of-action.md)
- [15 bots, HITL & WORM records](15-bots-hitl-and-worm-audit.md)
- [16 configuration, defaults & failure safety](16-configuration-and-safety-model.md)
- [17 decisions register](17-decisions-register.md) (the decision for every planning gap)
- [18 platform & deployment](18-platform-and-deployment.md) (canonical for languages, the database, deployment modes and the workstation-first path; where this spec and 18 differ on those, 18 wins)

---

## 1. Ground rules

| Rule | Meaning |
|---|---|
| **Languages** | **Rust for everything we write**, including what we rebuild from borrowed designs (TradingAgents, FinRobot, Vibe-Trading, freqtrade-style analysers; [17 §H](17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20)). **Python only where absolutely required**, in five packages: `mt_research` (ML training and research), `mt_extract` (trafilatura), `mt_telegram_reader` (Telethon), `mt_ledger_import` (ccxt ledger history) and the MT5 bridge ([18 §2.2](18-platform-and-deployment.md#22-python-uv-workspace-packages-only-where-absolutely-required)). Strategies are Rust by default. TypeScript for the web app. **Python never places orders, signs or sits on the live decision path**: it publishes to NATS or calls `mt-api`, so every order still passes `mt-risk`, and research reads only through `pit(as_of)` ([18 §2](18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary)). |
| **Personal use** | Nothing is distributed or served to others, so GPL/AGPL code could be used directly. We don't need to: borrowed designs are rebuilt in Rust, clean-room for GPL/AGPL sources (e.g. the freqtrade-style analysers in M7). Any copyleft code that is ever vendored goes under `third_party/copyleft/<name>/` with a line in the copyleft register ([19 §4](19-third-party-register.md#4-copyleft-register--and-the-release-plan)). Yahoo, Myfxbook, ForexFactory and similar personal-use terms are fine. Keep the repo **private**. |
| **Configuration** | **Nothing that shapes trading is hard-coded.** Limits, sizing, drawdown triggers, capital steps, wallet caps, gas budgets, validation gates, approval timers and failure behaviour are configuration with documented defaults ([16](16-configuration-and-safety-model.md)). Layers inherit **tighten-only**: L0 hard ceilings (edited in the agent/bot strategy settings; the ceilings section applies to every bot) → L1 system → L2 venue/account → L3 sleeve → L4 bot; the effective value is the strictest. Tightening is immediate; loosening is C3, at every layer including L0. A strategy manifest *proposes* values, never imposes them. Every change is a versioned WORM row ([16 §1](16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance)). |
| **Free only** | Only free sources and free tiers. A single user should stay under the free limits. **Excluded (paid):** X API, CoinGlass, CME FedWatch API, TokenSniffer, Glassnode, Trading Economics, Databento credits, paid exchange data. **Every connector has a quota tracker that throttles before the limit.** |
| **Deferred** | Reddit (optional if API access is granted) and X: revisit only if free and permitted. **MCP control plane:** built last (Phase 8), only once the platform is in daily use. |
| **Never** | Self-bots, fake engagement, sybil farming, scraping that breaks a platform's terms, autonomous wallet signatures outside a mandate (see [07](07-security-notes.md)). |
| **Jurisdiction** | Australian tax resident now; possible move to the UAE, Egypt or Cyprus later. The journal and tax engine are jurisdiction-pluggable ([09](09-journal-and-tax.md)). |
| **Policy & compliance** | AU retail boundary, the **venue access registry** (orders blocked to venues/products not lawfully available to you), **2× crypto-derivatives leverage cap** (default L0 ceiling, [16 §2.1](16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)), explicit self-trade prevention where the venue supports it, Travel Rule, per-platform data terms: see [12](12-policy-and-compliance.md). Rule changes are watched, never auto-applied (M3a). |
| **Data provenance** | Every stored row carries **seven separate columns**: `source`, `licence`, `train_ok`, `model_input_ok`, `display_ok`, `retention_days`, `commercial_ok`. Training and inference paths (including MCP responses, M20) refuse disallowed rows. **Telegram text never reaches any model, RAG index or training set** (Telegram API terms); Telegram feeds deterministic postures only ([12 §4–5](12-policy-and-compliance.md#4-per-platform-data--automation-rules)). |
| **Failure safety** | A down engine, host or network must leave no unprotected exposure: three-layer dead-man (M11), resting venue-side stops on every live position, restart flat with bots paused, one fixed egress IP for exchange keys ([16 §3](16-configuration-and-safety-model.md#3-failure-safety)). |

---

## 2. Target environment

| Item | Choice |
|---|---|
| Host | **Workstation first.** Phases 0–6 build, test and paper-trade on your workstation (Mode 1); no dedicated host, full-disk encryption, Tailscale or hardware key is needed before Phase 7. The optional shift to a runtime host (workstation, home server or Sydney VM), Vercel and Supabase cloud is a set of Phase 7 OPS tasks: P7-T071 (choose), P7-T072 (YubiKey), P7-T073 (harden, migrate, deploy, re-verify) ([18 §9](18-platform-and-deployment.md#9-workstation-first-build-path)). As a guide for an always-on runtime host: 8–16 cores, 32–64 GB RAM, **2–4 TB NVMe** (tick/L2 storage), plus a HDD for cold Parquet; full-disk encryption from the shift. |
| Deployment modes | `deploy.mode`: `workstation` (default) \| `hybrid` \| `regional` ([18 §5](18-platform-and-deployment.md#5-deployment-modes), [16 §2.15](16-configuration-and-safety-model.md#215-platform-deployment-and-regions)). The always-on services (engine, dead-man, recorder, NATS, workers, signer) never run on Vercel ([18 §6](18-platform-and-deployment.md#6-what-cant-run-on-vercel-and-why)). |
| Language / packaging | **Rust** (Cargo workspace, `crates/`) first; **Python 3.12** (`uv` workspace, `packages/`) only for the five packages in 18 §2.2; **TypeScript** (`pnpm`) for `apps/web`. One `just` (or `make`) entry point runs the lot. |
| Runtime | Docker Compose, one compose file per mode in `infra/`, with images pinned by digest |
| Engine | **NautilusTrader** (pinned), event-driven: the same code runs backtest, sandbox/paper and live. The **Rust live node** runs where the venue's Rust adapter is production-ready (U, per venue), otherwise the Python node; both link `mt-risk` |
| Bus | **NATS JetStream** (market data fan-out, events, alerts) |
| Databases | **Supabase Postgres** (Postgres 17 with pgvector, pg_trgm, pgcrypto, pg_cron, pgTAP, and pg_partman if available (U)) is the system of record. **No TimescaleDB** (deprecated on Supabase Postgres 17): bars use monthly native partitions ([18 §4.3](18-platform-and-deployment.md#43-bars-without-timescaledb)). Where it runs (`db.target`): Supabase CLI for development and tests, self-hosted Supabase on the workstation (default), optionally Supabase cloud in Sydney (paid; a USER decision at shift time) ([18 §4.1](18-platform-and-deployment.md#41-where-it-runs)). **Nautilus ParquetDataCatalog + DuckDB** hold raw ticks/L2. **QuestDB** is optional, only if live SQL over raw ticks is ever needed. |
| Auth | **Supabase Auth**: your one account, password + TOTP MFA, sign-ups off. `mt-api` verifies the JWT and requires `aal2` for every command ([18 §4.6](18-platform-and-deployment.md#46-auth)) |
| Web hosting | The same SPA served locally by Caddy (`web.host: local`, default) or deployed to Vercel (`web.host: vercel`); the browser never talks to the database ([18 §4.5](18-platform-and-deployment.md#45-access-rules)) |
| Observability | **Grafana + Loki** (logs, shipped by Vector) + **Prometheus** (metrics) + **OpenTelemetry** traces. **One alert fan-out:** Grafana alerts → webhook → the `alert.*` consumer → Telegram / ntfy / email |
| Models | **Decision One** (M21): tier A = in-process compiled GBDT/ONNX (~10–50 µs) in the order path; tier B = **decision models** (SemIf readout → own Qwen3 + LoRA + classification head, ~2–12 ms on GPU) for text/context judgements, async. Research/chat/debate go through the **LiteLLM gateway** → Claude API / your custom endpoint / local fallback. Local fallback model served by `llm-local` (llama-server on CPU or vLLM on GPU) for the `local-advisor` route. Embeddings and rerank via **two TEI containers**: `tei-embed` (bge-small-en-v1.5) and `tei-rerank` (bge-reranker-v2-m3). See [10](10-memory-rag-and-models.md). |
| GPU (optional) | `models.gpu_profile: auto` uses a GPU if one is detected, otherwise CPU profiles (the default); GPU-only checks run only when a GPU is present ([16 §2.15](16-configuration-and-safety-model.md#215-platform-deployment-and-regions)). One consumer GPU (16–24 GB VRAM) makes tier B fast: ~2–12 ms per decision (0.6B head), p95 SLO < 50 ms. Without one, tier B runs CPU ONNX at ~100–400 ms per decision and is used only for slower flags ([10 §4.3](10-memory-rag-and-models.md#43-design)) |
| Orchestration | `mt-scheduler` (Rust; replaces Prefect): Postgres-backed jobs and cron, retries, backfills, run history, status on D16/D07; Python training jobs run as its jobs. Long-running services under Compose |
| Access | Everything bound to localhost or the internal network. Remote access via **Tailscale** only, and only where needed: phone access, hybrid mode with `api.exposure: tailnet` (default), and the go-live egress exit node ([18 §8](18-platform-and-deployment.md#8-tailscale-and-the-hardware-key-per-mode)) |
| Secrets | `sops` + `age` encrypted file → tmpfs at start. The encrypted file lives **outside this repo** (e.g. `~/.config/mastertrader/`), backed up by restic ([07 §2](07-security-notes.md#2-secrets)). The age identities sit in the OS keychain (or a passphrase-protected age file) until Phase 7, then on a YubiKey before live money (`secrets.age_identity_store`, P7-T072) |

---

## 3. Repository layout

This is the **canonical** layout; [02 §11](02-v1-architecture.md#11-repository-layout) points here and [18 §3](18-platform-and-deployment.md#3-repository-layout) summarises it. Crate and package names follow [18 §2](18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary). The full container list is in [02 §3.2](02-v1-architecture.md#32-containers).

```
MasterTrader/
├── Cargo.toml / Cargo.lock       # Rust workspace
├── crates/                       # Rust crates (18 §2.1)
│   ├── mt-core/          # shared types (Instrument, BarSpec, Tick, Event, Signal, OrderIntent, RiskPolicy, JournalEvent), config, clock, message schemas; exposed to Python through the same PyO3 module as pit
│   ├── mt-api/           # command layer (M15): axum + tokio REST/WS, utoipa OpenAPI, Supabase JWT check (aal2), C0–C3 confirmations; used by the web app, Telegram and (later) MCP
│   ├── mt-risk/          # risk manager (M11): policies, pre-trade checks, portfolio risk, kill switch; one crate linked into mt-api, the engine (PyO3 binding for the Python node) and mt-deadman
│   ├── mt-deadman/       # dead-man layer 2 sidecar: small static binary, own trade-only keys, cancel/flatten only (M11)
│   ├── mt-engine/        # NautilusTrader live node + custom Rust adapters (Alpaca, OANDA, IG, cTrader, AU spot venues); built-in Rust strategy templates in src/strategy/ (M0, M12); MT5 via the Python bridge (packages/mt_mt5_bridge)
│   ├── mt-recorder/      # streaming market data (M1): venue WS → Parquet catalog + standard bar sizes into monthly partitions, rollup job
│   ├── mt-monitor/       # live data-quality + cost/TCA + reconciliation + egress check (M16)
│   ├── mt-store/         # pit(as_of) read path with Python bindings (PyO3 module `mt_store`, which also carries the mt-core types), WORM helpers, Parquet catalog helpers, partition job; sqlx compile-checked queries
│   ├── mt-obs/           # WORM writer, hash chain, daily seal, integrity response, tracing/metrics, LLM-call audit (M17)
│   ├── mt-signer/        # intents-only signer for hot/burner/identity keys (alloy for EVM, Solana SDK); accepts intents only from the policy service; writes `audit.signer_ledger` (13 §2)
│   ├── mt-journal/       # journal ingestion, lot engine, FX service, jurisdiction plugins, reports, exports; rust_decimal; tax golden tests (M18)
│   ├── mt-events/        # global-event pollers: USGS, GDACS, NOAA, FIRMS, ReliefWeb, UCDP, ACLED, Kalshi, Polymarket, congressional disclosures (M3)
│   ├── mt-telegram-bot/  # Telegram bot (teloxide, Bot API): alerts, digests, approvals, task buttons, /kill (M15)
│   ├── mt-mcp/           # (Phase 8, last) MCP server on the official Rust SDK (rmcp): thin adapter over mt-api (M20)
│   ├── mt-onchain/       # on-chain helpers: the cost gate (`costgate`), simulation calls to Anvil, live fee inputs
│   ├── mt-treasury/      # wallet-indexer + unified view, custody tiers, signer client, hold-and-earn, yield allocator, DAO/depeg/exploit monitors (M22)
│   ├── mt-airdrop/       # airdrop/launch discovery, enrichment, risk & viability scoring, EV gate (M4)
│   ├── mt-airdrop-exec/  # airdrop policy service: mandated claims, simulation, revokes, sweeps (M4 execution)
│   ├── mt-connectors/    # batch data clients (M1, M5): FRED/ALFRED, EIA, USDA NASS, Treasury, BLS, ECB/SDMX, CFTC COT, World Bank, IMF, SEC EDGAR (submissions + XBRL companyfacts), Dukascopy, data.binance.vision, CoinGecko, DefiLlama, Myfxbook, Finnhub, CryptoPanic, Twelve Data, calendars; replaces OpenBB, fredapi, sdmx1, edgartools, yfinance; quota tracker per client
│   ├── mt-scheduler/     # batch orchestration (replaces Prefect): Postgres-backed job queue and cron, retries, backfills, run history, job status on D16/D07; runs Python training jobs as containers/subprocesses
│   ├── mt-features/      # feature library + evaluator (M6): incremental in the engine, batch via mt-scheduler
│   ├── mt-nlp/           # nlp service (M2): relevance gate client, entity linking (GLiNER ONNX (U)), FinBERT (ONNX via ort), TEI embeddings/rerank over HTTP → text.document
│   ├── mt-agents/        # agent runtime (M8) on rig-core: explicit state-machine graph, Postgres checkpoints; debate, valuation desk, research workflows (skills/ prompts, NOTICE kept), persona lenses, strategy-generator loop
│   ├── mt-memory/        # document RAG (hybrid pgvector/tsvector, TEI rerank), Hindsight HTTP client, PIT filter, decision settlement (M9)
│   ├── mt-models/        # model runtime (M21): tier A inference (ONNX via ort), tier B client (SemIf readout via vLLM; own head via ONNX), model and question registries, labels
│   ├── mt-anomaly/       # anomaly detectors + explain agent on mt-agents (M10)
│   ├── mt-lab-core/      # lab production side (M7): walk-forward/validation harness, clean-room bias analysers, setup-odds simulator, cost models, gate reports; drives Nautilus backtests; PyO3 binding for mt_research
│   ├── mt-crowdsim/      # scenario & crowd simulator + scenario twin driver (M14), clean-room on the OASIS/MiroFish idea
│   ├── mt-curation/      # user task queue + community curation (Discord/Telegram/Galxe) + digests (M19)
│   ├── mt-social/        # social participation: drafts → your approval → web-intent post; credibility + shill-burst posture (M23)
│   ├── mt-intel-writer/  # core-side INSERT-only writer for scrape outputs (Telegram postures, raw events, regulatory snapshots)
│   └── mt-mm-adapter/    # Rust client of the Hummingbot API (REST + WebSocket) behind mt-api/M11 (M13)
├── pyproject.toml / uv.lock      # uv workspace (Python only where absolutely required)
├── packages/                     # the five Python packages (18 §2.2); none places orders, signs or sits on the live decision path
│   ├── mt_research/      # lab exploration + training (M7, M6, M21): PyTorch, LightGBM, scikit-learn, Optuna, Qlib, vectorbt (research only), LoRA/FinBERT fine-tuning, notebooks, MLflow client; exports promoted models to ONNX; reads only through pit; runs as mt-scheduler jobs; Python strategies for ML research on paper only
│   ├── mt_extract/       # ingest-text article extraction with trafilatura (crawl4ai container for JS pages); publishes raw.text.* only (M2)
│   ├── mt_telegram_reader/ # Telethon MTProto reader; regex postures only (posture.telegram.*), never text to models (M2)
│   ├── mt_ledger_import/ # ccxt ledger/statement history; hands normalised events to mt-journal (M18)
│   └── mt_mt5_bridge/    # optional MT5 bridge (Windows VPS; the MetaTrader5 package is Windows/Python-only); reaches venues only through mt-api/mt-risk (M12)
├── apps/web/             # React + TypeScript SPA (M15 web UI, [02 §10](02-v1-architecture.md#10-frontend-architecture)), served by Caddy or Vercel; vercel.json for the optional Vercel deploy
├── supabase/             # config.toml, migrations/*.sql (all 13 schemas in §4), seed.sql, tests/ (pgTAP: schema, WORM and pit invariants)
├── infra/                # compose files per mode (images pinned by digest), caddy, grafana dashboards, prometheus/alert rules, sops config (no secrets), host provisioning (P7 shift), seeds
├── services/             # configs for third-party containers run unmodified: hummingbot + Hummingbot API (M13), rss-bridge, crawl4ai; optional rotki / ghostfolio / beancount-fava
├── strategies/           # user strategies, each a Rust crate + manifest (any type); Python only for ML research on paper, ported to Rust (ONNX) before live
├── third_party/          # vendored code (pinned commit + licence) + LICENSES.md; copyleft only under third_party/copyleft/<name>/, listed in 19 §4
├── notebooks/  tests/  docs/  docs/runbooks/  ui-examples/  brand/  DESIGN.md
```

**Builds and checks:**
- Rust: `cargo test -p <crate>` and `cargo clippy`. Python (the five packages only): `uv run pytest`. Web: `pnpm test` and `pnpm playwright`.
- Licences: `just licence-audit` (cargo-deny + pip-licenses + a scan of `third_party/`) reports every ⚑ item in the copyleft register ([19 §4](19-third-party-register.md#4-copyleft-register--and-the-release-plan)).
- **Migrations:** plain SQL in `supabase/migrations/` (no Alembic). Applied locally with `supabase db reset` / `supabase migration up`, and to a cloud project with `supabase db push`. SQL invariants: `supabase test db` (pgTAP).
- The golden tests (risk, `pit`, WORM, tax) live in the Rust crates; `pit` is also tested through its Python binding.

**Design choice that keeps MCP cheap later:** every user action (change a risk limit, pause a strategy, adjust a position, approve an order, mark a task) is a typed command in **`mt-api`**.
- The web UI and the Telegram bot call `mt-api` from day one.
- The MCP server (M20) is then just a thin adapter that exposes the same commands to Claude.
- It needs no new business logic, so building it last costs little.

---

## 4. Data model (overview)

**Supabase Postgres** schemas (one canonical list; **all 13 are created in Phase 0** by SQL migrations in `supabase/migrations/`, later phases add tables additively with new migration files). The same migrations deploy to the local stack and, optionally, Supabase cloud ([18 §4](18-platform-and-deployment.md#4-database-supabase-postgres)):
- **`market`**: instruments, bars (monthly native range partitions, created ahead by pg_partman where available, otherwise by the `mt-store` partition job on pg_cron (U); [18 §4.3](18-platform-and-deployment.md#43-bars-without-timescaledb)), cost and spread series, funding/swap rates.
- **`text`**: documents, events, calendars, Telegram postures (`text.telegram_posture`).
- **`features`**
- **`strategy`**: registry, runs, results, bots.
- **`risk`**: policies, limits, changes.
- **`audit`**: canonical (singular) tables `audit.order`, `audit.fill`, `audit.command`, `audit.llm_call`, `audit.dq_event`, `audit.dq_ack`, `audit.cost_event`, `audit.recon`, `audit.decision_run`, `audit.seal`, `audit.integrity_incident`, `audit.mcp_call`, `audit.auth_event`, `audit.verify_run`, `audit.signer_ledger`, `audit.signal`, `audit.tierb_decision`, `audit.anomaly`.
- **`journal`**: events, lots, matches, FX rates, residency, reports.
- **`curation`**: tasks (`curation.task`, from P3), community, airdrops.
- **`ops`**: venue registry, `ops.wallets` (the one registry for accounts and on-chain addresses, created in P3, extended by the P5 wallet-indexer), drill log.
- **`rag`**: document chunks and embeddings (M9).
- **`models`**: model registry, questions, labels (M21).
- **`treasury`**: hold-and-earn positions, transfers, policy (M22).
- **`hindsight`**: Hindsight agent memory (M9).

Raw ticks, quotes and L2 live in the **Parquet catalog**.

**Bars without TimescaleDB** ([18 §4.3](18-platform-and-deployment.md#43-bars-without-timescaledb)):
- `mt-recorder` writes 1s bars and every standard size (1m, 5m, 15m, 1h, 4h, 1D, 1W) as it builds them from ticks.
- Backfills and corrections re-run an idempotent rollup job (upsert by key) that rebuilds the higher sizes from 1m.
- Any other size is `date_bin()` at read time inside `pit(as_of)`.
- Bars older than `db.bars_hot_months` ([16 §2.15](16-configuration-and-safety-model.md#215-platform-deployment-and-regions)) are exported to Parquet and their partitions dropped; `pit(as_of)` reads both transparently.

**Access rules** ([18 §4.5](18-platform-and-deployment.md#45-access-rules)): row-level security on every table with no policies for `anon` and `authenticated` (deny all); the Supabase Data API and Realtime off for MasterTrader schemas; the browser reads only through `mt-api`. Supabase Storage holds private buckets for reports, tax exports and attachments.

**Point-in-time rule:**
- Every fact carries an `event_time` and an `ingest_time`.
- Research and backtests read only through `pit(as_of=…)` in the `mt-store` crate; Python code calls the same implementation through its binding, `mt_store.pit(as_of=…)`.
- A CI test fails if a module, Rust or Python, bypasses it.

**Audit tables are WORM** (write-once, read-many; full design in [15 §2](15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)):
- Owned by an offline `worm_owner` role; app roles INSERT/SELECT only; UPDATE/DELETE/TRUNCATE revoked and blocked by triggers.
- Per-row hash chain (`prev_hash`, `row_hash`) plus a daily Merkle seal anchored outside the DB (object-locked storage, optional OpenTimestamps, Telegram witness).
- pgTAP tests (`supabase test db`) hold the WORM invariants.
- On Supabase cloud the platform operator holds the real superuser, so the external seal is what proves tampering; it runs in every mode ([18 §4.4](18-platform-and-deployment.md#44-point-in-time-and-worm)).

**Append-only rules:**
- Insert-only DB roles.
- A per-row hash chain, sealed daily outside the DB.
- Corrections are new rows that reference the original.
- WORM insert p99 < 5 ms; the order path never waits on seals.

(Full column lists live in each module's spec and in `supabase/migrations/`. Earlier tables (`document`, `geo_event`, `calendar_event`, `signal`, `decision_log`, `exposure_map`) are kept.)

---

## 5. Modules

Module headings keep their original package names so existing links still work. The **Package** line under each heading is current: Rust crates in `crates/`, Python packages in `packages/` ([18 §2](18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary)).

### M0 Strategy framework — `mt_strategy` (strategy-agnostic, any timeframe)

**Package:** **Rust by default**: built-in templates in `crates/mt-engine/src/strategy/`, your own strategies in `strategies/<name>/` (a Rust crate + manifest). The registry, lifecycle and bots live in `crates/mt-api`; the manifest and parameter schemas in `crates/mt-core`. Python strategies (Nautilus's Python strategy API, in `packages/mt_research`) are allowed only for ML-driven research on paper and are ported to Rust (ONNX inference via `ort`) before live [18 §2.1](18-platform-and-deployment.md#21-rust-cargo-workspace-crates).

- **Built on Nautilus `Strategy`/`Actor`.** One strategy class runs unchanged in backtest, sandbox/paper and live.
- **Strategy types supported as first-class templates:**
  - scalping (tick / order-book driven);
  - intraday;
  - trend/EMA/MA crossovers;
  - mean reversion;
  - breakout;
  - swing and position;
  - grid/DCA;
  - market making (via Nautilus or the Hummingbot sidecar; optional, P6);
  - pairs/stat-arb;
  - event/news-driven;
  - ML-signal;
  - LLM-signal (M8; from P6);
  - deterministic rule-based (MasterTradingBot strategies, [14 §8](14-strategy-evidence-and-validation.md#8-mastertradingbot-integration));
  - funding carry, cross-sectional momentum, token-unlock positioning, memecoin momentum with rug filtering (paper first).
- **Templates are starting points, not limits.** Any custom logic is allowed.
- **Evidence & priority:** each template shows its evidence and priority (P1/P2/P3) from [14 §3](14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates).
- **Never-build list:** latency-race patterns (sniping, atomic/latency arbitrage, copy-trading, prediction-market bots) are rated **X**, and **sandwiching is Never**. They have no template, and the manifest validator rejects them.
- **Any timeframe:** subscribe to raw **ticks / quotes / trades / order-book deltas**, or any **bar spec**:
  - time bars: 1s, 5s, 1m, 3m, 7m, 1h, 4h, 1D, 1W…;
  - tick bars, volume bars, value bars.
  - Several timeframes can be combined in one strategy (e.g. 1D trend filter + 5m entries + tick execution).
  - Bars are aggregated from the finest data available for that venue. The framework reports the native minimum per instrument (see §6).
- **Strategy manifest** (`strategies/<name>/manifest.yaml`):
  - instruments/universe and data subscriptions (with timeframes);
  - parameters with types, ranges and defaults (drives the UI forms and optimisation);
  - required features;
  - risk-policy reference;
  - proposed bot mode (`paper` / `hitl` / `autonomous`; the mode itself is set per bot, [15 §1.2](15-bots-hitl-and-worm-audit.md#12-modes)) and proposed risk values (proposals only: you accept or tighten them, [16 §1](16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance));
  - **counterparty** (one sentence: who loses to this strategy and why; required);
  - **sleeve** (capital bucket with its own limits and kill switch);
  - **kill criteria**, written before deployment;
  - **benchmark** (asset-class passive alternative).
- **Lifecycle:** a strategy version is **promoted** draft → backtested → validated through the gates in §8. A **bot** running a validated version is **switched** between modes: `paper` → `hitl` (C2) → `autonomous` (C3); stepping back is C1 ([16 §2.3](16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)). A strategy's own mode (`strategy.set_mode`) caps its bots: the stricter of strategy and bot mode applies. `approve`/`auto` are retired aliases for `hitl`/`autonomous`. Every transition is logged.
- **Ways to create a strategy:**
  1. write Rust (Python only for ML research on paper, ported to Rust before live);
  2. configure a template in the UI;
  3. describe it to the LLM strategy generator (M7, sandboxed; it emits Rust);
  4. import/port from other frameworks (freqtrade/Vibe-Trading patterns).
- **Experimentation:**
  - parameter sweeps;
  - A/B comparisons on identical data;
  - shadow mode (a live strategy runs in parallel paper mode for comparison).

### M1 Market & macro data — `mt_data.market`

**Package:** `crates/mt-recorder` (Rust) for streaming and bar building; `crates/mt-connectors` (Rust) for batch history, macro and fundamentals, run as `crates/mt-scheduler` jobs. The connectors replace OpenBB, fredapi, sdmx1, edgartools and yfinance; every client writes with provenance [18 §2.1](18-platform-and-deployment.md#21-rust-cargo-workspace-crates).

**Free only, with a quota tracker per connector.**

**Crypto:**
- **Real-time:** public WebSockets for trades, L1 and L2 diff depth (Binance, Bybit, OKX, Coinbase, Kraken) via the Nautilus adapters (Rust data clients where available (U)); ccxt is used only for ledger history (`mt_ledger_import`).
- **History:** **data.binance.vision** (trades, aggTrades, klines down to 1s).
- **Enrichment:** CoinGecko Demo, DefiLlama.

**FX & metals:**
- **OANDA v20** practice stream (max 4 quotes/s per instrument).
- **IG** Lightstreamer (demo).
- **Dukascopy** historical ticks (cross-source reference).
- TrueFX / HistData for cross-checks.
- ECB reference rates + self-hosted **Frankfurter**.
- Twelve Data free tier as backup bars.
- Spot XAU/XAG from brokers (**no LBMA**: it needs a licence).

**Stocks/ETFs:**
- **Alpaca Basic** (real-time IEX, 30 WebSocket symbols).
- Daily history via `mt-connectors` (Yahoo chart data (U): 18 §2.1 lists no Yahoo client; Twelve Data and Alpaca history otherwise).
- FinanceDatabase as the symbol master.

**Futures/commodities:**
- No free real-time feed, so daily data only (Yahoo `GC=F`, `CL=F` via `mt-connectors` (U); akshare for Asia runs as an optional `mt_research` offline batch job, 18 §2.2).
- EIA, USDA (WASDE report files keyless; QuickStats API with a free key from T0.10), CFTC COT, Baker Hughes.
- **Futures-like exposure is traded via crypto perps or FX/CFDs** (OANDA/IG).

**Rates & macro:**
- US Treasury, **FRED/ALFRED** (vintages).
- **SDMX** for ECB/IMF/OECD/BIS/Eurostat via the `mt-connectors` SDMX client (replaces `sdmx1`).
- BoE IADB, BoC Valet, RBA, SNB, BoJ.
- DBnomics as the catch-all.
- **ABS CPI**: All groups CPI, weighted average of eight capital cities (series A2325846C (U), verify), needed for the 2027 tax indexation.
- **RBA F11 daily FX** (needed for tax).

**Fundamentals:** SEC EDGAR via `mt-connectors` (submissions + XBRL `companyfacts` JSON; replaces edgartools): filings, 13F, Form 4, S-1/424B.

**Recording pipeline:**
- Venue WS → `mt-recorder` (Nautilus Rust data clients where available (U)) → NATS.
- From NATS:
  - strategies (in-process);
  - the **Parquet recorder** (rolled every 1–5 minutes, compacted daily);
  - the **bar builder** (in `mt-recorder`) writing 1s bars and every standard size (1m, 5m, 15m, 1h, 4h, 1D, 1W) straight into the monthly partitions of `market.bar_*`; backfills and corrections re-run the rollup job. Any other size is a `date_bin` query at read time inside `pit(as_of)` (§4, [18 §4.3](18-platform-and-deployment.md#43-bars-without-timescaledb)).

**L2 recording:** raw L2 diffs at native speed only for symbols a bot needs order-book data for (default ≤ 3 symbols, configurable); 1 s book snapshots for the rest.

**Storage budget:** about 0.3–1 TB/year for about 10 liquid crypto symbols at trades + L1 + L2 on that basis (U; re-measured in the Phase 1 soak).

### M2 News & social — `mt_data.text`

**Package:** ingest-text: feed clients in Rust (RSS, Discord bot, Bluesky, Mastodon, Farcaster, GDELT; API news via `crates/mt-connectors`; streaming feeds in `crates/mt-feeds`), article extraction in `packages/mt_extract` (Python, trafilatura; crawl4ai container for JS pages), Telegram reading in `packages/mt_telegram_reader` (Python, Telethon; postures only). The nlp service is `crates/mt-nlp` (Rust: entity linking with GLiNER via ONNX (U), FinBERT via `ort`, embeddings and rerank via TEI over HTTP) [18 §2](18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary).

See [06 §2](06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack).

**News:**
- RSS feeds + **trafilatura** / **crawl4ai**.
- **RSS-Bridge** as an internal sidecar (whitelisted bridges, auth on).
- **GDELT**.
- EDGAR feeds.
- Central-bank RSS.

**Social (free):**
- **Telegram:** Telethon client (dedicated number, e.g. a landline/prepaid) + Bot API + RSS-Bridge fallback.
  - **Postures only:** Telegram → regex extractor → postures → code/policy. Regex-extracted contract addresses/tickers and counts (mention velocity, channel count, new-channel share, time since first call) are stored in `text.telegram_posture` and published on `posture.telegram.*`; the only consumers are M4 and M11 **rules**.
  - **No model ever sees Telegram text**: not FinBERT, tier B, RAG, agents or training ([12 §4](12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
  - Joins go through a `FLOOD_WAIT`-aware queue; cap of 500 channels.
- **Discord:** your own server + **followed announcement channels** + your own bot.
- **Bluesky Jetstream**, Mastodon, **Farcaster** (self-hosted Hubble, free).
- Conditional: StockTwits, YouTube RSS/API.
- Extra news APIs (free, personal use):
  - **Finnhub** (60/min), for equities/FX headlines (read its ML clause first);
  - CryptoPanic's free tier for crypto news (read its terms first).
- **Reddit:** optional if API access is granted; **X deferred.**

**Processing** (non-Telegram sources only; provenance flags checked first; this is the model chain Telegram never enters):
1. Dedupe.
2. Relevance gate (tier-B stage 1, M21): p95 ≤ 300 ms on GPU, ≤ 3 s on CPU, queued, never on the order path.
3. Entity/ticker linking.
4. FinBERT sentiment.
5. Local embeddings.
6. Store in `document` (approximate timestamps are flagged).

### M3 Global events — `mt_data.events`

**Package:** `crates/mt-events` (Rust pollers) [18 §2](18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary).

**Sources:**
- USGS, GDACS, NOAA/NHC, NASA FIRMS, ReliefWeb, UCDP, GDELT, OpenSanctions.
- ACLED (research account). FIRMS/ACLED keys and the OpenSanctions licence are a USER task.
- Central-bank statements and minutes.
- **Kalshi / Polymarket** public reads as event probabilities. **Read-only:** Polymarket is ISP-blocked for Australians, so only where lawfully reachable, never via VPN; no trading.

**Exposure map:** links each event's location to assets (country → FX/index/bond ETF; region → commodity).

**Event score:** severity × exposure × novelty.

### M4 Airdrops, token launches & ICOs — `mt_airdrop`

**Package:** `crates/mt-airdrop` (Rust: discovery, enrichment, scoring) + `crates/mt-airdrop-exec` (Rust policy service: mandated claims, simulation, revokes, sweeps). Signing only via `crates/mt-signer` [18 §2](18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary).

Full design: [08](08-airdrops-and-token-launches.md).

**Pipeline:** discover → vet → score → decide (auto-claim / user task / watch / reject) → track → journal.

**Risk feeds:**
- **GoPlus** (EVM), **RugCheck** (Solana), **Honeypot.is**.
- DexScreener, Helius and **Blockscout** / own RPC (Etherscan for manual lookups only: its terms bar use as a decision input).
- **Own wallet-cluster detection** (common funder within 3–5 hops, same-slot/bundled buys, shared CEX-withdrawal origin), the highest-value check.
- Entity **blacklist** with funding-graph auto-flagging.
- A cited **project dossier** for campaigns and longer holds.
- Phishing blocklists.
- Re-implemented solana-rugchecker heuristics and CRPWarner concepts; optional sandboxed Gigahorse deep scan.
- Scores calibrated on the SoK rug-pull dataset.

**Autonomous only for:**
- read-only work;
- **eligible claims** from the chain's **airdrop identity wallet** under a signed mandate, with simulation (Anvil / `simulateTransaction`) and the on-chain cost gate;
- **genuine-use on-chain tasks** (swap, stake, provide liquidity, vote) sized to real usage, under a mandate and the cost gate, after a successful **burner** run. No pattern mimicry, dust loops, volume farming or wash trading for points;
- defensive revokes/sweeps.

All signing goes through the signer, which accepts intents only from the policy service. Default EV hurdle: 5% p.a. on capital locked ([16 §2.7](16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)). Until live execution passes the Phase 7 gates, airdrop disposal (sale) is a USER task.

**Everything else**, including all social engagement and ICO/IDO participation, becomes a **user task** with step-by-step instructions.

### M5 Calendars — `mt_data.calendar`

**Package:** `crates/mt-connectors` (Rust calendar clients, run as `mt-scheduler` jobs). `exchange_calendars` is Python, so its session/holiday data is loaded as data files or a Rust calendar crate is used (U) [18 §2.1](18-platform-and-deployment.md#21-rust-cargo-workspace-crates).

- **Sources:**
  - FRED/ALFRED release dates;
  - **ForexFactory weekly JSON** (consensus forecasts, cached);
  - central-bank meeting schedules;
  - COT/EIA/WASDE/Baker Hughes days;
  - EDGAR earnings and IPO filings;
  - exchange holiday/session calendars (`exchange_calendars` data, see Package).
- **Strategy and risk uses:** strategies and the risk manager can query "event within N minutes", e.g. to pause scalpers around NFP.
- **Default blackout:** for high-importance events, bots marked `event_sensitive` (scalping/intraday templates by default) block new entries from 15 min before to 15 min after; exits and protective orders continue. Configurable per bot and event type ([16 §2.8](16-configuration-and-safety-model.md#28-calendar-blackouts)).

### M6 Features — `mt_features`

**Package:** `crates/mt-features` (Rust: feature library and evaluator; incremental in the engine, batch via `mt-scheduler`). Feature exploration and forecast-model training run in `packages/mt_research` (Python); promoted features are rebuilt in Rust and promoted models run via ONNX (`ort`) [18 §2.1](18-platform-and-deployment.md#21-rust-cargo-workspace-crates).

- **Sentiment & regime per market type:** separate pipelines for crypto, FX, gold/silver/metals, energy and equities/indices, plus a shared **macro layer** (USD, rates, calendar, risk-on/off). Each outputs a sentiment score, fear/greed gauge, news-impact flags and a **regime label**. Crypto inputs add Fear & Greed, funding, open interest, liquidations and long/short ratios.
- **Market and factor features:**
  - TA-Lib;
  - Qlib Alpha158 and the Vibe-Trading factor zoo: definitions rebuilt in Rust for production; Qlib itself stays in `mt_research` for exploration;
  - microstructure features from ticks/L2 (order-flow imbalance, spread, depth, trade intensity).
- **Sentiment, positioning and macro features:**
  - sentiment and event scores;
  - COT;
  - retail positioning (Myfxbook, IG, OANDA books);
  - nowcasts (GDPNow, NY Fed, Cleveland Fed);
  - Fed SEP;
  - Fed-path probabilities computed from ZQ futures;
  - BIS effective exchange rates;
  - VIX regime;
  - prediction-market probabilities.
- **Price regime (`regime_v1`, from P2):** bull / bear / chop per asset, daily, from the 200-day average and 90-day return ([16 §2.4.1](16-configuration-and-safety-model.md#241-regime-labels-for-per-regime-results)). Used by the per-regime gate (§8). Sentiment-based regimes (P4) are later candidates.
- **Telegram is never a feature:** Telegram postures go only to M4/M11 rules. M6, tier A/B, agents and RAG never consume them.
- **Forecast models:** Chronos / TimesFM / Kronos for volatility and volume (run in `mt_research`; ONNX in Rust where they export cleanly (U)).
- **Versioning and evaluation:** features are versioned, and an evaluator measures IC, rank-IC and decay.

### M7 Research lab — `mt_lab`

**Package:** split in two [18 §2.1](18-platform-and-deployment.md#21-rust-cargo-workspace-crates):
- `crates/mt-lab-core` (Rust, production side): walk-forward and validation harness, **bias analysers**, **setup-odds simulator** (R2.59), cost models and gate reports; drives Nautilus Rust backtests. Python reaches it through a PyO3 binding.
- `packages/mt_research` (Python): exploration, screening, training and optimisation; runs as `mt-scheduler` jobs and reads only through `pit`.

Strategies are Rust by default (M0).

- **Two backtest paths:**
  - **Screening:** fast vectorised path in `mt_research` (vectorbt, research only: Apache-2.0 + Commons Clause ⚑, [19 §2](19-third-party-register.md#2-python-libraries-we-keep-only-where-absolutely-required-18-22); Vibe-Trading-style engines).
  - **Truth:** **Nautilus** backtests driven by `mt-lab-core` with L1/L2 replay, measured fee/slippage/latency models (fed from M16) and funding/swap costs.
- **Validation:**
  - walk-forward;
  - purged K-fold;
  - Monte Carlo permutation;
  - bootstrap Sharpe CI;
  - deflated Sharpe (DSR, a probability; default gate ≥ 0.95);
  - **look-ahead and recursive-formula analysers**: clean-room Rust in `mt-lab-core`, from freqtrade's ideas only (freqtrade is GPL-3.0; no GPL code). They replace the vendored copy from P2-B051, which is removed when they land ([17 §H](17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20), [19 §4](19-third-party-register.md#4-copyleft-register--and-the-release-plan)).
  - Leakage findings are fixed, or each is waived by you (`lab.leakage.waive`, C2, audited).
- **Optimisation** (in `mt_research`):
  - Optuna, with a complexity penalty;
  - experiment tracking (**MLflow**, self-hosted) of every run: code version, parameters, data range, costs, results.
- **Setup-odds simulator** (R2.59): replays bootstrapped continuations from the instrument's own recent bars plus past occurrences of the same setup, all through `pit(as_of)` (day-trader-skill idea, rebuilt in Rust). Informational only: never overrides M11.
- **Sandboxed LLM strategy generation:** a Vibe-Trading-style research → strategy loop (in `mt-agents`) that emits **Rust** strategies against our templates; they are compiled and tested in the sandbox. No network, no secrets.

### M8 AI decision layer — `mt_agents`

**Package:** `crates/mt-agents` (Rust agent runtime on `rig-core` (MIT), replacing LangGraph): an explicit state-machine graph with Postgres checkpoints. All model calls go through the LiteLLM gateway [18 §2.1](18-platform-and-deployment.md#21-rust-cargo-workspace-crates).

- **Debate graph:** a TradingAgents-style run, rebuilt in Rust from its Apache-2.0 design (prompts adapted, NOTICE kept):
  1. Analysts: technical, sentiment, news, fundamentals, macro/events.
  2. Bull/bear debate.
  3. Research manager.
  4. Trader.
  5. Risk debate.
  6. Portfolio manager.
- **Tools:**
  - the **valuation desk**: FinRobot-style DCF/WACC/DDM/comps operators as deterministic Rust (the LLM writes only the narrative; SEC XBRL from `mt-connectors`; the FinRobot name isn't used);
  - `pit` data tools;
  - memory recall (`mt-memory`).
- **Research workflows:** the Anthropic financial-services skill files (earnings preview/analysis, catalyst calendar, thesis tracker, morning note, DCF/comps) used as prompts in `crates/mt-agents/skills/`, NOTICE kept.
- **Persona lenses** (optional, off by default): investor-persona viewpoints in the debate.
- **Output:** a structured `Signal` with fields: id, ts, as_of, instrument, horizon, direction, edge, calibrated confidence, rationale summary, sources[], model/prompt versions, run id.
- **How strategies use it:** an *LLM-signal* strategy (M0) or any strategy can consume these signals as a feature.
- **Versioning:** prompts and models are versioned and every call is audited (`audit.llm_call`, written from P0, M17).

### M9 Memory & RAG — `mt_memory`

**Package:** `crates/mt-memory` (Rust: document RAG, the Hindsight HTTP client, the point-in-time filter, decision settlement). Hindsight itself runs unmodified as its own container [18 §2.1](18-platform-and-deployment.md#21-rust-cargo-workspace-crates).

Full design: [10](10-memory-rag-and-models.md).

**Hindsight** (MIT), self-hosted:
- **slim** image, running in our Supabase Postgres in its own `hindsight` schema;
- **local embedder and reranker via TEI** (`tei-embed`: bge-small-en-v1.5, 384-d; `tei-rerank`: bge-reranker-v2-m3);
- its LLM goes through the LiteLLM gateway.

**Memory banks:** `decisions`, `strategies`, `market-regimes`, `user`, `ops`.

**Point-in-time recall in backtests** ([10 §1](10-memory-rag-and-models.md#1-hindsight-self-hosted-agent-memory)):
- every memory carries `observed_at` / `ingested_at`;
- consolidated and reflection memories carry the **latest** source time and are excluded when it's > `as_of`;
- if Hindsight can't enforce this, backtests run with memory **disabled** or from a frozen per-`as_of` snapshot;
- a PIT recall test is mandatory.

**Document RAG** (`rag` schema):
- pgvector HNSW (halfvec) + native tsvector + pg_trgm;
- **Reciprocal Rank Fusion**, then cross-encoder rerank, then recency decay;
- **`ingested_at`/`published_at` ≤ as_of filter**.
- Chunking: filings by section with context headers; news with dedup.
- Caches: embedding, retrieval and prompt caches.
- Shares the TEI embedder with Hindsight.

**Optional later:** LightRAG graph over filings (offline, research path only).

**Decision settlement and reflection** go into Hindsight, and teacher logs go into `decisions` (feeding M21 distillation).

### M10 Anomaly monitor — `mt_anomaly`

**Package:** `crates/mt-anomaly` (Rust: streaming detectors; the explain agent runs on `mt-agents`) [18 §2.1](18-platform-and-deployment.md#21-rust-cargo-workspace-crates).

- **Detectors** on market, sentiment and event streams:
  - robust z-scores;
  - IsolationForest (trained in `mt_research`, run via ONNX (U));
  - change points;
  - correlation breaks.
- **Explain agent:** writes a brief and sends it to Telegram. It also runs on request (`anomaly.explain`, C1, from the UI or MCP).

### M11 Risk manager — `mt_risk` (built in; user inputs via UI/Telegram, later MCP)

**Package:** `crates/mt-risk` (Rust, **one implementation**): linked into `mt-api` (policy, previews), the engine (pre-trade checks; a PyO3 binding where the strategy or node is Python) and `crates/mt-deadman` (dead-man layer 2). Risk golden tests run against the crate [18 §2](18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary).

**Authoritative and default-deny.** It runs as a pre-trade check in front of the Nautilus `RiskEngine`, which also enforces hard limits natively. **Every order passes through it,** whatever its source: strategy, LLM agent, UI, Telegram or MCP.

**Risk policy** is a versioned YAML/DB document, edited through `mt-api`. It covers several levels:

| Level | Examples of configurable limits |
|---|---|
| Global | Max gross/net exposure, max daily loss, max drawdown (trailing/peak), max leverage, max open orders, trading hours/blackouts, base currency |
| Per venue / account | Max notional, leverage, allowed instruments, order-rate limits |
| Per strategy | Capital allocation, max position, max loss per day/trade, max consecutive losses, cool-down after a loss, allowed timeframes/instruments |
| Per instrument / asset class | Max position, max spread to trade, min liquidity, news/event blackout windows (via M5) |
| Portfolio | Correlation/cluster exposure (e.g. USD, crypto beta), VaR/ES estimate, concentration |
| Sizing models (selectable per strategy) | Fixed size, fixed fractional, volatility target (ATR), **stop-distance sizing**, Kelly (`f = (p·b − q)/b`, quarter-Kelly ceiling, never `2p − 1`), risk-parity |
| Sleeves | Capital split into sleeves with separate limits/kill switches; exposure **netted per asset across sleeves** |
| Defaults | Every value is a configurable default in [16 §2](16-configuration-and-safety-model.md#2-default-values-all-configurable): risk per trade, venue concentration (default ≤ 25% of equity per venue), two-stage sleeve and system drawdowns (measured on trading equity, excluding the vault and hold-and-earn, adjusted for your deposits and withdrawals: the drawdown basis in [16 §2.1](16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)), **decision deadlines**, price collar, API-error pause, cost blow-out, 2× crypto-derivatives cap |

**Fallback ladder** (live state shown in D06):
1. Healthy + high confidence → normal size.
2. Low confidence → half size or observe only.
3. Late decision / stale feed → hold.
4. Model service down → rules only: exits, no new entries.
5. Hard limit → halt the sleeve.
6. Kill switch → halt everything (see **Kill switch** below).

**Venue registry check:** orders to venues/products not `allowed` for your residency are rejected ([12 §2](12-policy-and-compliance.md#2-venue-access-registry)).

**Pre-trade checks:**
- policy limits;
- price collar (default 2% from the last trade for crypto majors, 0.5% FX majors, 1% ETFs);
- liquidity/spread check from M16;
- duplicate-order check (idempotent client order IDs, M12);
- event blackout (M5);
- **data age, checked inline on every order**: older than the bot's threshold (default 2 s fast / 60 s slow bots, session-aware) → rejected, and the ladder holds ([16 §2.2](16-configuration-and-safety-model.md#22-data-freshness-what-stale-means)); plus the DQ status (**no trading on a stale/bad feed**);
- **WORM integrity status** (`audit.integrity` in NATS KV): after a verify mismatch the default is `block_new_entries` (exits continue) until you acknowledge (M17, [16 §2.11](16-configuration-and-safety-model.md#211-worm-integrity));
- egress check: exchange traffic must leave via the allow-listed fixed IP ([16 §3.2](16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys)).

**Kill switch:**
- **Triggers:**
  - manual (UI, Telegram `/kill` via NATS `kill.set`, later MCP);
  - automatic: system drawdown stage 2 and unexplained reconciliation mismatches. Smaller breaches act more narrowly, per [16 §2.1](16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown): daily loss halts the sleeve, sleeve drawdowns halve sizes then halt the sleeve, API errors pause the venue, a cost blow-out pauses the bot.
- **Actions:** stop new trading, cancel orders, apply each bot's `on_system_failure` policy, freeze new treasury/earn moves, and (from P5, default on) sweep hot trading balances to the vault address. In P2 there's no sweep yet: P2 provides a logged no-op sweep hook.

**Dead-man's switch: three layers** ([16 §3.1](16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)):
1. **In-engine watchdog** on feed, risk, DB and NATS heartbeats (1 s): a component missing 5 s → cancel open orders for affected bots; 10 s → apply each bot's `on_system_failure`.
2. **External `deadman` sidecar** with its own trade-only keys and venue connections, watching the engine's heartbeat: engine missing 5 s → cancel all open orders; 10 s → flatten per `on_system_failure`.
3. **Venue-side** cancel-on-disconnect / countdown timers where supported, plus **resting stop-loss orders at the venue** placed at entry for every live position.

`on_system_failure` is set per bot (default `flatten`; alternatives `cancel_orders_only`, `hold`). After an unplanned stop the engine restarts with every bot **paused**, reconciles, trades from flat, and waits for you to resume (C1). All timings are defaults.

**Change control** (see [07 §6](07-security-notes.md#6-application-controls)):
- **Tightening** applies immediately.
- **Loosening** (raising a limit, enabling `autonomous`) is **C3**: Telegram approve + TOTP + cool-down (default 15 min, [16 §2.3](16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)). Restarting a halted sleeve (`risk.sleeve.restart`) is also C3.
- **L0 hard ceilings** are edited in the agent/bot strategy settings (the ceilings section applies to every bot): tightening is immediate, loosening is C3 like every other loosening ([16 §1](16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance)).
- Until the Telegram C3 path exists (P2), C3 commands complete through a break-glass CLI on the runtime host (`mtctl approve <id>` + TOTP; a local shell at the workstation, or SSH over Tailscale when remote, [18 §8](18-platform-and-deployment.md#8-tailscale-and-the-hardware-key-per-mode)), audited.
- Every change is audited and versioned (rollback).

**Modes per mandate / bot:** `paper` / `hitl` (formerly `approve`: Telegram/UI approval card per order) / `autonomous` (formerly `auto`). paper → HITL is C2; HITL → autonomous is C3.

**Trading bots:** a bot deploys one strategy version onto a market scope (single instrument, list or dynamic selection) with its own venue account, sleeve, mode and approval policy. You set each bot to **autonomous** or **HITL**; HITL bots send approval cards to Telegram; protective exits never wait for approval; autonomous needs C3 and auto-downgrades to HITL on decay/DQ/ladder events. Full design: [15 §1](15-bots-hitl-and-worm-audit.md#1-trading-bots).

### M12 Execution — `mt_engine`

**Package:** `crates/mt-engine` (Rust). NautilusTrader **Rust live node** where the venue's Rust adapter is production-ready (U, per venue), otherwise the Python node with the same `mt-risk` binding. Custom adapters (Alpaca, OANDA, IG, cTrader) are written in Rust against Nautilus's adapter traits [18 §2](18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary).

- **Nautilus adapters:** IBKR, Binance, Bybit, OKX, Coinbase, Kraken, Hyperliquid, Betfair. These are subject to the **venue access registry**: for an AU resident, offshore perps (Bybit/Bitget…) are data-only, Hyperliquid waits on professional advice, and Polymarket trading is blocked.
- **Custom adapters:**
  - **Alpaca** (paper/live);
  - **OANDA v20**;
  - **IG**;
  - optionally **cTrader** Open API/FIX and Saxo (SIM);
  - MT5 (Windows bridge, `packages/mt_mt5_bridge`, reaching venues only through `mt-api`/`mt-risk`) for **FP Markets / MasterTradingBot**, with cTrader Open API as the Linux route ([14 §8](14-strategy-evidence-and-validation.md#8-mastertradingbot-integration));
  - **AU spot venues** via custom Rust adapters (was ccxt; Python never places orders, 18 §2.2; effort per venue (U)): Independent Reserve, BTC Markets, Kraken AU, CoinSpot;
  - **DEX execution**: Jupiter + Jito (Solana), 1inch free + Flashbots Protect (EVM), via the signer service and the **on-chain cost gate** ([13 §7](13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16)).
- **Key safety:** keys are trade-only, **withdrawals disabled**, IP allow-listed to one fixed AU egress IP (an exit node with a static IP; broadband and 4G both tunnel to it, [16 §3.2](16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys)); separate sub-accounts per mode (`paper` / `hitl` / `autonomous`). Practice/paper accounts use their normal credentials; live accounts use read-only keys where offered, otherwise trade-only.
- **IBKR** runs through an `ib-gateway` container (IBC-managed) when used.
- **Self-trade prevention:** the STP mode is sent **explicitly on every order** where the venue supports it (12 §3). Netting brokers (OANDA, IG, Alpaca, IBKR) have no STP field: the venue registry marks `stp: n/a (netting)`, and one strategy runs per account/sub-account where netting would merge bots.
- **Client order ID** = `{bot}-{engine_epoch}-{seq}`; a signal hash is stored separately for idempotency, so a restarted engine can't resubmit the same signal. Open orders are reconciled from the venue before trading resumes.
- **Venue-side protection:** cancel-after timers (refreshed every 15 s, 60 s timeout by default) and a resting venue stop for every live position (dead-man layer 3, M11).

### M13 Market-making sidecar

**Package:** third-party `hummingbot` + Hummingbot API containers, run unmodified, driven by `crates/mt-mm-adapter` (Rust client of the Hummingbot API, REST + WebSocket) behind `mt-api`/M11 [18 §2.1](18-platform-and-deployment.md#21-rust-cargo-workspace-crates).

- **Hummingbot** with telemetry off and broker IDs stripped.
- It's treated as a venue behind M11.

### M14 Crowd simulation (optional)

_Heading kept for links. M14 is now the **go-live scenario & crowd simulator**, not an optional experiment ([17 §H](17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20); supersedes P6-B009's "otherwise skip")._

**Package:** `crates/mt-crowdsim` (Rust, clean-room on the OASIS/MiroFish idea; no MiroFish or OASIS code: MiroFish is AGPL-3.0, needs Zep Cloud and ships insecure defaults) [18 §2.4](18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool).

- **What it does:** turns a headline or event into a simulated crowd reaction. A seeded, recorded population of LLM persona agents (retail, funds, market makers, media, bots) produces a **scenario**: a sentiment path plus price, volatility, spread and liquidity shocks.
- **Scenario twin (8-week paper period):** a second paper engine runs the same bots on replayed live data with injected scenarios. It shows how each bot behaves under shocks the real market hasn't produced yet; a weekly report per bot joins the weekly review pack.
- **Stress tests:** before live, the scenarios run alongside the four historical shocks (P7-T069).
- **Boundaries:**
  - it never trades the real paper or live accounts;
  - its data is flagged `synthetic = true` and never enters features, model training or RAG;
  - it runs isolated with no route to the signer;
  - LLM calls use the local model by default, inside the LLM budget.
- **Defaults** ([16 §2.14b](16-configuration-and-safety-model.md#214b-scenario--crowd-simulator-m14)): scenario twin on during the paper period and before live; 3 scenarios a week; 200 persona agents × 10 rounds; `local-advisor` route; shock caps price ±15%, volatility ×3, spread ×5, liquidity ÷5.

### M15 UI & alerts — `mt_ui` (calls `mt_api`)

**Package:** `apps/web` (React + TypeScript, `pnpm`) and `crates/mt-telegram-bot` (Rust, teloxide); both call `crates/mt-api` (Rust, axum). The old `mt_ui` package is retired [18 §2](18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary).

**Design source of truth:** [DESIGN.md](../DESIGN.md) v2.
- Fully responsive from 1920px+ down to 240px, portrait and landscape, on the shared breakpoint set.
- Reference screens are in [ui-examples/](../ui-examples/README.md).
- Tailwind is built locally (no CDN).
- A Playwright viewport-matrix test runs in CI.


- **Web UI** (React SPA in `apps/web`, served locally by Caddy or deployed to Vercel per `web.host`, calling `mt-api`; login through the Supabase Auth client only, and the browser never talks to the database, [18 §4.5–4.6](18-platform-and-deployment.md#45-access-rules)):
  - strategy builder/registry;
  - backtest/experiment viewer;
  - risk-policy editor;
  - positions/P&L;
  - **manual trade ticket and position adjust** (through M11);
  - approvals queue;
  - task queue;
  - journal/tax views.
- **Grafana:** markets, costs, DQ, P&L, LLM spend, system health. Its alerts use the one fan-out in §2 (webhook → `alert.*` → Telegram / ntfy / email).
- **Telegram bot** (`mt-telegram-bot`, Rust, teloxide; reading channels is Telethon in M2, Python):
  - alerts and digests;
  - approve/deny buttons;
  - task Done/Skip/Snooze;
  - `/kill` (published on NATS `kill.set` with credentials limited to that subject; the engine writes the WORM record with source `telegram`), `/status`, `/pnl`, `/pause <strategy>`.

### M16 Live cost & data-quality monitor — `mt_monitor` (always on, autonomous)

**Package:** `crates/mt-monitor` (Rust) [18 §2](18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary).

**Data quality**, a streaming service on NATS with rolling state per instrument:

| Check | Method |
|---|---|
| Stale feed | **Data age** = now − our receive time per stream (not the exchange timestamp). Thresholds per bot (default 2 s fast / 60 s slow), session-aware (closed sessions are `closed`, not stale). The monitor flips `dq.status` to `stale` ≤ 250 ms (p99) after the threshold; M11 also checks age inline on every order ([16 §2.2](16-configuration-and-safety-model.md#22-data-freshness-what-stale-means)) |
| Gaps | Exchange sequence IDs / trade-ID continuity / expected bar counts |
| Bad ticks | Robust z-score (median/MAD; default flag at z ≥ 8, configurable); price outside the spread band; crossed/locked book |
| Cross-source divergence | Mid-price difference in bps between two free sources (Binance vs Bybit/OKX/Coinbase; OANDA vs Dukascopy/IG); default alert at 25 bps crypto / 5 bps FX majors, configurable |
| Clock skew | `recv_ts − exchange_ts` p99; chrony offset |
| Book integrity | Venue checksums; periodic REST snapshot reconciliation |
| Batch | Nightly validation of Parquet (Rust checks in `mt-monitor`, replacing Pandera) and drift reports (Evidently, Python-only, run as an `mt_research` job on `mt-scheduler` (U)) |

**Costs, always measured from free APIs:**
- **Fees:**
  - commissions per fill and current fee tiers (each venue's fee/commission endpoint through the `mt-engine` adapters, e.g. Binance commission endpoint, IBKR `commissionAndFeesReport`, Alpaca);
  - borrow rates.
- **Funding and swaps:**
  - funding rates (predicted + realised);
  - swap/financing (OANDA `InstrumentFinancing` + realised financing transactions; IG realised funding).
- **Spreads:** `spread_bps` by instrument × hour-of-week.
- **TCA (implementation shortfall)** for every order:
  - decision price, arrival price, fill VWAP, fees and funding;
  - broken down into delay / spread-impact / fees;
  - a rolling **realised-vs-modelled** cost ratio per strategy × venue × instrument.

**Outputs:**
- Incidents go to `audit.dq_event` / `audit.cost_event`; an acknowledgement is a new WORM row (`audit.dq_ack`), never an update.
- Metrics go to Prometheus; alerts use the one fan-out in §2.
- **M11 is told** to pause affected bots: stale feed, spread > 3× normal (default, configurable), cost blow-out (realised ÷ modelled cost > 1.5× over the last 20 fills, default, [16 §2.1](16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)).
- Measured costs are **fed back** into the M7 backtest fee/slippage models.

**Reconciliation:**
- Positions and open orders are compared with each venue's own records every 60 s, balances every 5 min, and in full at end of day (Sydney).
- Tolerance: position quantities match exactly; balances within 0.01% or dust.
- A mismatch matched to a known journal event within 24 h is explained; otherwise it's **unexplained**, which halts everything (a kill criterion).
- Results go to `audit.recon` (WORM) and `recon.*`. All values are defaults ([16 §2.9](16-configuration-and-safety-model.md#29-reconciliation)).

### M17 Observability & audit — `mt_obs`

**Package:** `crates/mt-obs` (Rust: WORM writer, hash chain, daily seal, integrity response, tracing/metrics) [18 §2](18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary).

**System of record (Postgres `audit`)** holds:
- orders, fills, cancels, fees, funding (`audit.order`, `audit.fill`);
- decisions and signals (`audit.decision_run`);
- **every LLM call** (`audit.llm_call`: model, prompt/response hash + text, tokens, cost, latency), written **from P0** via the LiteLLM callback;
- risk-policy changes;
- DQ/cost incidents and reconciliation (`audit.dq_event`, `audit.dq_ack`, `audit.cost_event`, `audit.recon`);
- **every `mt-api` command** (`audit.command`; source: `web` / `telegram` / `mcp` / `system`);
- **every MCP call**, reads included (`audit.mcp_call`, linked to `audit.command` for commands);
- seals and integrity incidents (`audit.seal`, `audit.integrity_incident`);
- mandate changes.

These tables are WORM (append-only, hash-chained, sealed daily outside the DB) and kept ≥ 7 years.

**Integrity check** ([16 §2.11](16-configuration-and-safety-model.md#211-worm-integrity)):
- `audit.verify` runs hourly (incremental) plus a daily full verify against the external seal.
- A mismatch sets the `audit.integrity` status in NATS KV, which M11 reads pre-trade. Default action `block_new_entries` (exits continue); options `alert_only` / `halt_all`.
- You clear it with `audit.integrity.ack` (C3) after investigating. Every incident and ack is a WORM row (`audit.integrity_incident`).
- If Postgres is unreachable, writes buffer in NATS JetStream (bounded, default 1 GB or 24 h); nothing executes without a record ([16 §3.3](16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check)).

**Logs:**
- **Loki**, fed by Vector, with structured JSON logs (`tracing` in Rust, structlog in Python) and low-cardinality labels.
- Retention 30–90 days.
- Every audit row carries a `trace_id` so you can jump from a fill to its logs in Grafana.

**Metrics and traces:** Prometheus + OpenTelemetry (optionally Tempo); optionally **Arize Phoenix** for an LLM-trace UI.

**Not chosen:**
- Graylog (SSPL, heavy).
- OpenObserve (AGPL, duplicates Grafana).
- Soda Core (now ELv2).
- ArcticDB (BSL).
- TDengine (AGPL, IoT-focused). This is our reading of "TenentDB".

**Backups** (per mode, [18 §4.7](18-platform-and-deployment.md#47-backups)): on the workstation, pgBackRest against the Supabase Postgres container + restic to an encrypted off-site target: continuous WAL archive, nightly incremental, weekly full. On Supabase cloud, its managed daily backups plus our nightly logical dump to restic. In every mode, a monthly automated restore test and a monthly immutable WORM export.

### M18 Trading journal & tax — `mt_journal`

**Package:** `crates/mt-journal` (Rust, `rust_decimal`; lot engine, tax rules, reports; tax golden tests against the crate). Exchange ledger/statement history via ccxt stays in `packages/mt_ledger_import` (Python), which hands normalised events to `mt-journal` [18 §2.2](18-platform-and-deployment.md#22-python-uv-workspace-packages-only-where-absolutely-required).

Full design: [09](09-journal-and-tax.md).

- **Journal:** an automatic, append-only journal of every economic event, with home-currency values and FX source (RBA for AUD). Crypto values follow the valuation hierarchy in [16 §4.1](16-configuration-and-safety-model.md#41-valuing-crypto-for-the-journal) (fill price → VWAP of our recorded trades → on-chain pool price; aggregators cross-check only).
- **Lot engine:** rp2-style; specific-ID first, FIFO fallback; FX-cash lots.
- **Jurisdiction plugins:**
  - **AU_2026** (50% discount, CFDs on revenue account, Div 775, crypto income, wash-sale flags (re-acquisition within 30 days either side of a loss disposal, flag only, default, [16 §4.4](16-configuration-and-safety-model.md#44-tax-flags)), myTax mapping, **PAYG-instalment estimator** computing both ATO instalment-amount and instalment-rate methods; GST/BAS mode dormant);
  - **AU_2027_REFORM** (30 June 2027 snapshot, CPI indexation, 30% minimum tax, (U));
  - **AE**, **EG** (crypto hard-flag), **CY** (8% crypto), **GENERIC**.
- **Residency timeline:** CGT event I1 modelling.
- **Trading journal view:**
  - per trade: strategy, rationale/signal, chart snapshot, tags, notes;
  - review prompts.
- **Exports:**
  - Beancount (or hledger) ledger + Fava UI;
  - accountant CSV/PDF pack;
  - CARF reconciliation.
- **Optional sidecars:** Rotki (on-chain decoding), TaxHacker (expense receipts, local LLM), Ghostfolio (portfolio view).

### M19 User task queue & community curation — `mt_curation`

**Package:** `crates/mt-curation` (Rust) [18 §2.1](18-platform-and-deployment.md#21-rust-cargo-workspace-crates).

- **One queue for everything that needs a human.** Covers:
  - airdrop social tasks;
  - ICO reviews;
  - manual claims;
  - **Discord servers/channels to join and follow**;
  - Telegram channels to join;
  - X accounts to follow (manual);
  - Galxe spaces;
  - approval revokes;
  - tax-agent questions;
  - HITL order approvals.
- **Task types** (the canonical list; 08, D13 and the roadmap use these names): `JOIN_DISCORD`, `FOLLOW_ANNOUNCEMENTS`, `JOIN_TELEGRAM`, `FOLLOW_X`, `QUEST`, `ONCHAIN_ACTION_MANUAL`, `CLAIM_MANUAL`, `ICO_REVIEW`, `REVOKE_APPROVAL`, `TAX_QUESTION` (formerly `TAX_RECORD`), `GENUINE_USE`, `PRO_ADVICE`, `VENUE_CHECK`, `APPROVE_ORDER`, `REG_CHANGE` (regulatory & venue watch review, [16 §4.3](16-configuration-and-safety-model.md#43-live-inputs-instead-of-constants)).
- **Storage:** one table, `curation.task`, created minimally in P3 (tax-agent questions); P5 extends it with additive migrations.
- **Discord curation:**
  - invites discovered from **official sources only** (CoinGecko links, project sites/docs, official X bio) and verified against blocklists;
  - each entry states **which announcement channel to Follow** and which inbox channel to target;
  - a "leave when" condition;
  - the bot confirms delivery after you tap Done, and re-prompts if a followed channel delivers nothing in 7 days; at most 3 new servers are suggested per week (defaults, [16 §2.13](16-configuration-and-safety-model.md#213-curation)).
- **Cadence (configurable):**
  - instant alerts for urgent items;
  - **daily** digest;
  - **weekly** curation and review digest.
- **Telegram buttons:** Done / Skip / Snooze / Details / Never. Feedback tunes ranking, and tasks expire automatically.

### M21 Decision One & model serving — `mt_models`

**Package:** `crates/mt-models` (Rust runtime: tier A inference via ONNX/`ort` inside the engine, tier B client (SemIf readout via the vLLM server; own head via ONNX), model registry, question registry, labels). Training, calibration and distillation run in `packages/mt_research` (Python) as `mt-scheduler` jobs and export ONNX [18 §2](18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary).

Full design: [10 §4–5](10-memory-rag-and-models.md#4-decision-one-decision-models--microsecond-engine).

**Tier A: microsecond engine, in the order path.**
- **Model and runtime:** a GBDT/linear/small-MLP model, exported to **ONNX** and loaded **in-process** in the strategy through `ort` (Treelite / lleaves only for Python research runs; a parity test checks the scores match before promotion).
- **Latency:** ~10–50 µs per prediction.
- **Inputs:** incremental features plus cached tier-B flags.
- **Output:** a calibrated probability/edge, which M11 sizes.
- **Applicability:** works for every strategy type, including scalpers.

**Tier B: decision models (asynchronous, event-driven; "System One" class, no text generation).**
- **What they do:** typed questions (choice/score/yes-no) from a versioned registry return **option probabilities in one forward pass**.
- **Stage 1 (Phase 4):** **SemIf**-style option-logit readout on Qwen3.5-4B (zero-shot; relevance gate, first flags).
- **Stage 2 (Phase 6):** our own **Qwen3-0.6B/1.7B + LoRA + classification head** (Clef pattern):
  - distilled from M8 debate decisions and corrected against realised outcomes;
  - CE + Brier loss, temperature/isotonic calibration, abstention thresholds;
  - served by the vLLM `/classify` pooling runner or ONNX;
  - **~2–12 ms per decision on a consumer GPU** (0.6B, est.), p95 SLO < 50 ms; CPU 100–400 ms.
- **Bake-off:** against Laya (fine-tuned), self-hosted Clef-flash, SemIf and JSON generation, plus Kev-4B/9B only if a public, licence-compatible release exists (U), on our data + FinMMEval Buy/Hold/Sell.
- **Excluded:** Jev and Microsoft-Decision-1 (closed, paid).
- **Outputs:** cached on NATS KV as tier-A features. Auto-decide only at ≥ 0.75 precision; direct veto only at ≥ 0.90 precision; calibration ECE ≤ 0.05; flip rate ≤ 0.1%; ≥ 14 days in shadow before promotion (defaults, [16 §2.10](16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets)).
- **Determinism controls:** FP32 head, fixed batch, **prefix caching off** on the decision path, pinned revisions, logged prompt hash; CPU ONNX FP32 for backtests. A shared-prefix mode is allowed only for offline/backfill scoring, marked non-deterministic and never used for decisions or backtests.

**Labels and distillation:** until the P6 teacher exists, tier A trains on forward-return / triple-barrier labels from market data (`models.tiera.train`, C1). From P6, M8's debate decisions (the teacher) plus realised outcomes train tier A and the tier B decision-model heads; teacher labels are an extra source and don't change existing model versions.
- Students are calibrated (isotonic/Platt; Brier/ECE).
- They are promoted only through §8 gates, with the teacher in shadow.

**Model gateway (LiteLLM proxy, ≥ 1.83, pinned by digest):**
- **Routes:** research, chat, debate, strategy generation, explain agents and Hindsight route via `research-primary` (Claude), then `research-custom` (your endpoint), then `local-advisor` (served by `llm-local`).
- **Budgets and fallback:** per-role daily budgets plus a monthly cap (§7); local fallback when a budget is exhausted.
- **Never on the hot path.**

**Supporting pieces:**
- **TEI** containers `tei-embed` (embeddings) and `tei-rerank` (rerank).
- **Model registry in MLflow:** version, training data range, calibration, benchmark latency.
- **Latency SLOs** per tier, monitored in M17.

### M22 Wallets, treasury & hold-and-earn — `mt_treasury`

**Package:** `crates/mt-treasury` (Rust: wallet-indexer, unified view, hold-and-earn) + `crates/mt-onchain` (cost gate) + `crates/mt-signer` [18 §2](18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary).

Full design: [13](13-wallets-treasury-and-onchain.md).

- **Wallets:**
  - **Custody tiers:** vault (cold, manual), Hyperliquid master (hardware EIP-712, if approved), warm, hot, airdrop identity (one per chain), burner.
  - **Vault and warm are watch-only:** the system never holds their keys; it may prepare unsigned transactions (QR/WalletConnect) for you to sign in your own wallet.
  - The **signer service** accepts intents only, and only from the policy service (airdrop-exec, treasury and DEX execution all go through it), with allow-lists, caps, simulation, sized-and-revoked approvals and **durable-nonce hard blocks**. Floats, signer caps and gas budgets are defaults you confirm before signing is enabled ([16 §2.7](16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)).
  - The **cost gate** is one library, the `costgate` module of `crates/mt-onchain` (formerly `mt_onchain.costgate`): the signer uses it from P5, the treasury from P6.
- **Unified wallet view:**
  - one address registry, `ops.wallets` (created in P3, extended by the P5 wallet-indexer), with read-only aggregation (Helius DAS, Blockscout/RPC, Hyperliquid `/info`, venue read-only APIs from Rust);
  - monthly rotki reconciliation.
- **Hold-and-earn:**
  - LSTs, allow-listed lending (core Aave/Spark/Kamino), Pendle PTs, capped HLP;
  - a node/validator net-earnings model;
  - a yield allocator (`apyBase`; default ≤ 20% of treasury per protocol; HLP ≤ 10% of stablecoins and ≤ 5% of total portfolio, whichever is smaller).
- **Monitors:**
  - DAO proposals (Snapshot/Tally);
  - **stablecoin depeg**: > 50 bps (default) → reduce exposure once the P6 treasury exists; before that, alert + task;
  - exploit/oracle/TVL-drop, venue health, bridge policy.
- **Treasury:** floats per sleeve, daily profit sweeps to the vault, stablecoin concentration caps, a 20–40% reserve.

### M23 Social participation — `mt_social`

**Package:** `crates/mt-social` (Rust) [18 §2.1](18-platform-and-deployment.md#21-rust-cargo-workspace-crates).

Full design: [13 §8](13-wallets-treasury-and-onchain.md#8-social-participation-m23-mt_social).

- **Drafts:**
  - written by a local model in your voice, grounded in real activity;
  - you approve/edit/skip, and a holdings disclosure line is added.
- **Posting:** an X **web-intent** link that you click to post (no API cost). The proof URL is captured and the quest task marked done.
- **Signals:**
  - account **credibility scores** from past calls vs outcomes;
  - a **shill-burst posture** (mentions vs on-chain unique-buyer growth) as a dump-risk signal.
- **Not built:** extra accounts, auto-posting, engagement pods, pay-to-post.

### M20 MCP control plane — `mt_mcp` (built LAST, Phase 8, only if wanted)

**Package:** `crates/mt-mcp` (Rust, official MCP SDK `rmcp`) [18 §2](18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary).

**Purpose:** talk to the trading system and its agents through Claude (Desktop/Code) or another MCP client. You can ask, analyse, adjust and trade conversationally.

**How it's built:**
- A thin adapter over `mt-api`, using the official Rust MCP SDK (`rmcp`).
- **Transport:** Streamable HTTP (JSON-RPC 2.0, SSE streaming, resumable) on Tailscale/TLS, or stdio (newline-delimited JSON) locally; an optional legacy HTTP+SSE endpoint for older clients. The `mcp` container sits on the internal network behind Caddy, on Tailscale only. Server notifications (fills, approvals, alerts) use resource subscriptions.
- **Tokens:** opaque 256-bit, shown once, stored hashed (HMAC-SHA-256 with a server pepper), scoped, revocable instantly, with last-used time and client identity recorded. Expiry is your choice per token: 1 day · 7 days · 30 days · 1 year · custom · indefinite (indefinite = red warning + C3 + monthly reminder). Creating a token is C1 for `read` / `analyse` / `curation` scopes and C3 for `trade` / `strategy` / `risk_tighten` scopes or indefinite expiry ([16 §2.12](16-configuration-and-safety-model.md#212-mcp-phase-8)). OAuth 2.1 (PKCE, resource indicators) for clients that support MCP authorization.
- **Because the UI and Telegram already use `mt-api`, this is mostly wiring.**

**Scope (all via `mt-api`; every order still passes through M11):**

| Area | Tools |
|---|---|
| Read & analyse | Positions, P&L, exposure, orders, fills; strategy status and performance; backtest/experiment results; cost/TCA and DQ status; market data and features; news/event summaries; journal/tax summaries; task queue |
| Talk to agents | Ask the M8 decision graph for analysis/a signal on an instrument; query memory (M9); request an anomaly explanation (M10, `anomaly.explain`) |
| Trade & adjust | Place/modify/cancel orders; **adjust or close positions**; move stops/targets; scale in/out; flatten an instrument or strategy. Each one creates an approval card for you |
| Strategies | Create/edit parameters, run backtests and sweeps, promote/demote (gates still apply), pause/resume |
| Risk | View the policy; tighten instantly (scope `risk_tighten`); kill switch. Loosening is never a scope: it's C3 |
| Curation | Add watchlist items/airdrop URLs, mark tasks |

**Safeguards** ([16 §2.12](16-configuration-and-safety-model.md#212-mcp-phase-8)):
- MCP orders go through the same risk manager.
- **Confirmation levels for `source = mcp`:** C0 reads run; C1 runs per the token's scopes; C2 (every order) **always** creates your approval card on Telegram/web (TTL default 5 min, expiry = reject); C3 goes through Telegram + TOTP as usual. There's no "skip approval" option for MCP orders.
- **MCP can never approve** anything, its own orders included. Approvals come only from you on Telegram or the web.
- **Never exposed:** withdrawals, `wallet.sweep`, `treasury.*` moves, `airdrop.claim.execute`, mandates, key/token management, `approval.*`, `mcp.*`, restore/delete (incl. `system.restore.test`, `memory.delete`), `system.service.restart`, `risk.deadman.ack`, `/system/keys`, `/system/logs`, audit writes.
- **Response guard:** MCP responses pass the provenance filter like any model input: no Telegram text, no `model_input_ok = false` rows, PII (TFN, addresses, statements) redacted, secrets scrubbed, untrusted text wrapped and marked.
- **Limits** (defaults): 60 reads/min and 10 writes/min per token; 256 KB per tool result.
- Every call, reads included, is logged to `audit.mcp_call` (WORM); commands are also in `audit.command` with source `mcp`.

---

## 6. Smallest free timeframe by asset class

| Asset class | Finest free real-time | Finest free history | Practical note |
|---|---|---|---|
| Crypto spot/perps | Tick trades, L1, L2 diff depth (100 ms) via exchange WebSockets | 1s klines, trades, aggTrades (data.binance.vision); L2 history only if self-recorded | Supports scalping |
| FX / metals (CFD) | ~4 quotes/s per instrument (OANDA); IG streaming | Dukascopy ticks | No L2 in FX; Dukascopy is the reference |
| US stocks/ETFs | IEX trades/quotes, 30 symbols (Alpaca free) | Alpaca IEX history; Yahoo daily via `mt-connectors` (U) | IEX ≠ NBBO: fine for swing, weak for scalping cost measurement |
| Futures / commodities | None free (IBKR needs paid data) | Daily | Use perps/CFDs for intraday exposure |
| Bonds | — | Daily yields (Treasury/FRED) | Trade bond ETFs / Treasury futures via IBKR |

The UI shows each instrument's finest available resolution, so you know which strategy types are realistic for it.

---

## 7. LLM cost control

- **Model tiers:**
  - Decision One tier A (no LLM) in the order path;
  - tier B decision models (single forward pass, no generation) for text/context judgements;
  - local models for analysts and gating;
  - Claude (or your custom endpoint) for managers and research.
  - All non-hot-path calls go through the **LiteLLM gateway** with per-role daily budgets and local fallback, and every call is audited (`audit.llm_call`, from P0).
- **When agents run:**
  - per the strategy's configured cadence;
  - **event-triggered** (anomaly, calendar, big news);
  - never per tick.
- **Caching:** tool outputs are cached per (instrument, as_of).
- **Spending limit:** a monthly cap (default US$40, checked month-to-date) plus per-role daily budgets (defaults: debate $1.00, strategy-gen $0.50, explain $0.30, memory $0.30, chat $0.40, shadow $0.30 for tier-B shadow checks). Whichever is exhausted first routes that call to the local model ([16 §2.10](16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets)). Spend panel in Grafana.

---

## 8. Promotion gates (per strategy, configurable)

Every threshold below is a default in the per-strategy gate profile ([16 §2.4](16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile)). Tightening is free; loosening any gate is C3.

1. **Out-of-sample performance:** beats its benchmark on walk-forward out-of-sample data, after measured costs (M16).
2. **Robustness statistics:** Monte Carlo permutation p < 0.05; **deflated Sharpe ratio (DSR) ≥ 0.95**. DSR is a probability (0–1) that the true Sharpe is above zero after counting every variant tried.
3. **Bias checks:** the look-ahead and recursive analysers come back clean, or each finding is waived by you (C2, audited).
4. **LLM strategies:** evaluated on data after the model's training cutoff.
5. **Paper / HITL trading** before autonomous or a capital step:
   - default ≥ 8 weeks **and** ≥ 50 trades (P1 sleeves ≥ 8 weeks; memecoin ≥ 300 trades; low-frequency bots that can't reach the count use ≥ 26 weeks);
   - P&L and costs track the backtest within tolerance.
6. **Live:** start with the bot's starting allocation (default A$2,000, set per bot when it goes live). After **4 consecutive clean weeks**, step up **+25% of the current allocation**, each step approved by you (C3); a kill-criterion warning steps back one step, a halt returns to the starting allocation after your review. "Clean week" and the step rules: [16 §2.5](16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot); written kill criteria: [14 §7](14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7).
7. **Harness extensions** ([14 §6](14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8)):
   - profitable in **each year and each regime** (bull/bear/chop, `regime_v1`, [16 §2.4.1](16-configuration-and-safety-model.md#241-regime-labels-for-per-regime-results));
   - survives **2× and 3× measured costs**;
   - DSR ≥ 0.95 (item 2) with an **automatic trial counter**;
   - walk-forward judged on the **worst fold** and the share of positive folds;
   - an **LLM-assisted leakage review** quoting exact lines;
   - **survivorship-free** universes (delisted/rugged kept);
   - beats the **asset-class passive benchmark** after costs.
8. **Decay monitoring** (built in P2 for paper, extended to live in P7), one action per signal ([16 §2.6](16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each)):
   - rolling 60-trade Sharpe or hit rate below the backtest 5th percentile → alert + downgrade the bot autonomous → HITL;
   - CUSUM break on P&L residuals, or 5 consecutive losing trades on the bot → alert + downgrade to HITL;
   - daily health check fails (30-day Sharpe < ½ validated, or DD > 1.5× backtest max) → halt the bot pending your review;
   - a kill criterion ([14 §7](14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7)) → halt the sleeve and step capital down.
9. **Safety drills:** kill switch, dead-man and restart drills passed on the bot's venue (evaluated from `ops.drill_log`).

---

## 9. Future-proof hygiene

1. Third-party code lives under `third_party/` with a licence manifest.
2. GPL/AGPL code is isolated: only under `third_party/copyleft/<name>/`, listed in the copyleft register ([19 §4](19-third-party-register.md#4-copyleft-register--and-the-release-plan)); `just licence-audit` reports it. Every outside component, its language and its release action: [19](19-third-party-register.md).
3. Every data source is tagged `license: personal|commercial_ok|unknown` and `cost: free|paid`. Every **row** carries provenance + use flags (12 §5), so a SaaS pivot is a retrain on `commercial_ok` rows.
4. The repo stays **private**.
