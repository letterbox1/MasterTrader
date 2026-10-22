# MasterTrader — Architecture (v3, end-to-end)

This is the blueprint that backend and frontend work build against.
- Module behaviour: [03-build-spec.md](03-build-spec.md) (M0–M23).
- Order of work: [04-plan-of-action.md](04-plan-of-action.md).
- UI scope: [ui/README.md](ui/README.md).
- Visual system: [../DESIGN.md](../DESIGN.md).
- Configurable defaults and failure safety: [16-configuration-and-safety-model.md](16-configuration-and-safety-model.md). Numbers quoted here are defaults; 16 is the reference.
- Decisions on planning gaps: [17-decisions-register.md](17-decisions-register.md).

**Contents:**
1. Principles
2. System context
3. Deployment topology
4. Logical components
5. Data architecture
6. Messaging (NATS)
7. API contract (`mt_api`)
8. End-to-end flows
9. Cross-cutting: security, observability, SLOs, degraded modes
10. Frontend architecture
11. Repository layout
12. End-to-end build plan
13. Asset coverage & promotion gates

---

## 1. Principles

1. **A platform, not a strategy.** Any strategy type on any timeframe (tick/L2 → 1D+). Styles, timeframes, capital and risk limits are user inputs.
2. **Models reason, code computes, the risk manager decides.** No order from any source (strategy, Decision One, LLM agent, UI, Telegram, MCP) reaches a venue without passing the deterministic risk manager (M11).
3. **Point-in-time everything.**
   - Every record carries `event_time` + `ingest_time`.
   - Research reads only via `pit(as_of)`.
   - Raw text is archived so backtests can be replayed.
4. **One engine for backtest, paper and live:** NautilusTrader.
5. **Measure, then feed back.** Live data quality and trading costs (M16) gate trading and calibrate backtests.
6. **Record everything.** Audit and journal are WORM (write-once, hash-chained, externally sealed; [15 §2](15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)); logs only for operations.
7. **One command layer (`mt_api`).** The web UI, Telegram and (Phase 8) MCP are thin clients of the same typed, audited commands.
8. **Free only, personal use, private, no telemetry.** Generated code is sandboxed; GPL/AGPL code is isolated; secrets never reach LLMs.
9. **Nothing that shapes trading is hard-coded.** Limits, sizing, timers, gates and failure behaviour are layered settings with defaults (L0 hard ceilings → L4 bot; the strictest wins), set in the UI or Telegram and versioned as WORM rows ([16 §1](16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance)).

## 2. System context

```
               ┌──────────────── You ────────────────┐
               │ Web app (any device, via Tailscale) │ Telegram bot │ Claude via MCP (Phase 8)
               └───────────────┬─────────────────────┴──────┬───────┴──────────┬───────────
                               ▼                            ▼                  ▼
                      ┌─────────────────────── MasterTrader host (one Linux box) ───────────────────────┐
                      │  edge (Caddy) → mt_api (REST/WS) → services → NATS / Postgres / Parquet / models │
                      └───────┬───────────────┬──────────────────┬───────────────────┬──────────────────┘
                              ▼               ▼                  ▼                   ▼
          Brokers/exchanges (trade)   Free data sources   LLM APIs via gateway   Chains (RPC: Helius/Blockscout,
          IBKR, Binance, Bybit, OKX,  (M1–M5, quota-       (Claude, your custom   hot-wallet claims only)
          Coinbase, Kraken, Hyperliquid, tracked)          endpoint)
          Alpaca, OANDA, IG
```

- **Trust boundary:** everything inbound from data sources, social feeds, LLM outputs and chain data is **untrusted input**.
- **Outbound traffic** to venues and wallets goes only through the execution service (M12) and the signer, each behind M11 / mandates. The one exception is the `deadman` sidecar, which can only cancel and flatten ([16 §3.1](16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)).
- **Exchange egress:** from Phase 7, all exchange traffic leaves through one fixed-IP WireGuard/Tailscale exit node in Sydney, the only IP allow-listed on the keys; broadband and 4G both tunnel to it ([16 §3.2](16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys)).
- **Telegram text** is never model input: it becomes structured postures only (F3b, [12 §4–5](12-policy-and-compliance.md#4-per-platform-data--automation-rules)).

## 3. Deployment topology

Docker Compose on one host. Images are pinned by digest. Everything is reachable only on localhost or Tailscale.

### 3.1 Networks

| Network | Members | Internet egress | Purpose |
|---|---|---|---|
| `edge` | caddy, mt-api, ntfy, mcp (P8) | ntfy: upstream relay only (iOS push, message ID only) | TLS termination on the Tailscale interface; serves the web app, ntfy and the MCP endpoint (`/mcp`). Nothing is published except via Tailscale |
| `core` | mt-api, all app services, nats, postgres, mlflow, tei-embed, tei-rerank, litellm, llm-local, hindsight, deadman, ib-gateway | Venues and LLM APIs via allow-list; venue traffic via the egress exit node from P7 | Business logic. `mcp` is **not** on `core`: it reaches only `mt_api` |
| `scrape` | ingest-text, rss-bridge, crawl4ai | Yes (wide) | Untrusted fetching; **no route to postgres or signer** (publishes to NATS via a narrow NATS account) |
| `signer` | signer | Chain RPC only | Hot-wallet signing; accepts intents only from the policy service (airdrop-exec in P5; treasury and DEX execution go through it, [13 §2](13-wallets-treasury-and-onchain.md)) |
| `ctl` | mt-api, docker-proxy | — | Restricted Docker-socket proxy: `system.service.restart` may restart only allow-listed containers; no other Docker API |
| `obs` | grafana, loki, prometheus, vector, alertmanager | Telegram API (alerts) | Observability. Alerts leave only through the single `alert.*` fan-out (§6) |

**Egress exit node (external, P7):** a small WireGuard/Tailscale exit node on a Sydney cloud VM with a static IP, outside the host. All venue traffic (engine, deadman, monitor recon, ib-gateway) is routed through it, so a broadband → 4G failover doesn't change the IP the exchanges see. If the tunnel is down, nothing on our side can reach the venues and protection falls to venue timers and resting stops ([16 §3.2](16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys)).

### 3.2 Containers

| Service | Package / image | Role | Phase |
|---|---|---|---|
| `caddy` | caddy | Reverse proxy, TLS, static web app | 0 |
| `mt-api` | `mt_api` (FastAPI + uvicorn) | REST + WebSocket gateway, auth, command bus, confirmation flow | 0 |
| `postgres` | postgres 16 + timescaledb (TSL) + pgvector + pg_trgm | System of record | 0 |
| `nats` | nats (JetStream) | Event bus, KV state | 0 |
| `prefect-server` + `prefect-worker` | prefect | Scheduled batch flows (backfills, macro, EOD jobs, retraining) | 0 |
| `grafana`, `loki`, `prometheus`, `vector`, `alertmanager` | — | Observability | 0 |
| `mlflow` | mlflow | Experiments + model registry | 0 |
| `litellm` | LiteLLM ≥ 1.83 | Model gateway (research/chat/debate); its callback writes every call to `audit.llm_call` from P0 | 0 |
| `tei-embed` | text-embeddings-inference (CPU or GPU) | Embeddings (one model per TEI instance) | 0 |
| `tei-rerank` | text-embeddings-inference (CPU or GPU) | Reranker | 0 |
| `llm-local` | llama-server (CPU) or vLLM (GPU) | Serves the `local-advisor` route; gateway fallback when budgets are exhausted ([10 §5](10-memory-rag-and-models.md)) | 0 |
| `docker-proxy` | restricted Docker-socket proxy | Lets `system.service.restart` restart allow-listed containers only; mt-api never mounts the Docker socket | 0 |
| `ingest-market` | `mt_data.market` | Venue WS clients (via Nautilus data clients), Parquet recorder, bar builder | 1 |
| `ib-gateway` | IB Gateway, IBC-managed (digest-pinned) | IBKR API session with scheduled re-login; only when IBKR is used (read-only API for P1 recon) | 1 (when IBKR is used) |
| `ingest-batch` | `mt_data` (Prefect flows) | Macro, fundamentals, calendars, backfills | 1 |
| `monitor` | `mt_monitor` | Data-quality + cost/TCA + reconciliation (M16) | 1 |
| `engine` | `mt_engine` (NautilusTrader TradingNode) + `mt_strategy` + `mt_risk` + Decision One tier A | Live/paper trading node; strategies; risk; execution; in-engine watchdog (dead-man layer 1) | 2 |
| `deadman` | `mt_risk.deadman` (small sidecar) | Dead-man layer 2: watches the **engine's** heartbeat with its own trade-only keys and venue connections; can only cancel and flatten per `on_system_failure` ([16 §3.1](16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)) | 2 |
| `backtest-worker` | `mt_lab` | Backtests, validation, optimisation, distillation, sandbox orchestration | 2 |
| `sandbox` | gVisor/`--network none` runner | LLM-generated strategy code | 2 |
| `journal` | `mt_journal` | Journal ingestion, lot engine, tax rules, reports | 3 |
| `ingest-text` | `mt_data.text` | RSS, Telegram (Telethon + Bot), Discord bot, Bluesky, Mastodon, GDELT. **Telegram: postures only** (regex extractor → `text.telegram_posture`; never to nlp, RAG or models, F3b) | 4 |
| `rss-bridge` | rss-bridge | Feeds for sites without RSS | 4 |
| `nlp` | `mt_features.text` | Relevance gate, entity linking, FinBERT, embeddings → `text.document` | 4 |
| `ingest-events` | `mt_data.events` | USGS/GDACS/NOAA/FIRMS/ReliefWeb/UCDP/Kalshi/Polymarket | 4 |
| `airdrop` | `mt_airdrop` | Discovery, enrichment, risk/viability scoring | 5 |
| `airdrop-exec` + `signer` | `mt_airdrop.exec` | The **policy service** in P5: mandated claims, simulation, revokes, sweeps to the vault | 5 |
| (library) | `mt_onchain.costgate` | On-chain cost gate, used by the signer path from P5 and by `treasury` in P6 ([13 §7](13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16)) | 5 |
| `curation` | `mt_curation` | Task queue, digests | 5 |
| `wallet-indexer` | `mt_treasury.indexer` | Unified wallet view: balances, transfers (internal tagging), approvals, nonce-authority and depeg monitors; extends `ops.wallets` | 5 |
| `treasury` | `mt_treasury` | M22 hold-and-earn + treasury allocation; uses `mt_onchain.costgate`; signs only via the policy service | 6 |
| `signer` (extended) | `mt_signer` | Intents-only signer for hot/burner/identity keys (13 §2); accepts intents only from the policy service (airdrop-exec, treasury and DEX execution all go through it) | 5 |
| `anvil` | foundry anvil | Local mainnet-fork simulation before signatures | 5 |
| `social` | `mt_social` | M23 social drafts (approval → web intent from your account) | 6 (optional) |
| `ntfy` | ntfy (self-hosted) | Second, independent alert channel (push), reachable via Tailscale only; iOS push uses ntfy's upstream relay, which carries only a message ID | 1 |
| `telegram-bot` | `mt_ui.telegram` | Alerts, digests, approvals, task buttons, `/kill` (its NATS credentials may publish only `kill.set`) | 2 (alerts from 1) |
| `agents` | `mt_agents` | LangGraph debate runs (M8) | 6 |
| `hindsight` | Hindsight (slim) | Agent memory (schema `hindsight`) | 6 |
| `decision-svc` | `mt_models` + vLLM (`/classify`) or ONNX | Decision One tier B (SemIf readout → own Qwen-LoRA head). Decision path: prefix caching **off**, fixed batch ([10 §4.3](10-memory-rag-and-models.md)) | 4 (SemIf) / 6 |
| `anomaly` | `mt_anomaly` | Detectors + explain agent | 6 |
| `hummingbot` | hummingbot (telemetry off) | Market-making sidecar | 6 (optional) |
| `mcp` | `mt_mcp` | MCP adapter over `mt_api` (thin; no DB or NATS access); on `edge` behind Caddy, Tailscale only (§7.4) | 8 (optional) |
| (external) egress exit node | WireGuard/Tailscale on a Sydney cloud VM, static IP | Fixed egress IP for all exchange traffic (§3.1) | 7 |

**Hardware:** 8–16 cores, 32–64 GB RAM, 2–4 TB NVMe + HDD for cold Parquet. A 16–24 GB GPU is recommended for tier B, vLLM, Hindsight and LightRAG.

## 4. Logical components

| Module | Package | Runs in | Owns (Postgres schema/tables) | Publishes | Consumes |
|---|---|---|---|---|---|
| M0 Strategy framework | `mt_strategy` | engine, backtest-worker | `strategy.registry`, `strategy.versions`, `strategy.runs`, `strategy.bot`, `strategy.bot_version` (WORM) | `sig.*`, `strat.status.*`, `bot.{id}.status` | `md.*`, `feat.*`, `dec.tierb.*`, `engine.cmd.*` |
| M1 Market data | `mt_data.market` | ingest-market, ingest-batch | `market.instrument`, `market.bar_*`, `market.macro_series`, `market.filing` | `md.*`, `dq.raw.*` | venue WS/REST |
| M2 News & social | `mt_data.text` | ingest-text, nlp | `text.document`, `text.source`, `text.telegram_posture` (`model_input_ok = false`, `train_ok = false`) | `text.doc.*` (never Telegram), `posture.telegram.*` | feeds |
| M3 Events | `mt_data.events` | ingest-events | `text.geo_event`, `text.exposure_map` | `evt.*` | feeds |
| M4 Airdrops | `mt_airdrop` | airdrop, airdrop-exec | `curation.airdrop_*`, `curation.mandate`, `curation.exec_log` | `airdrop.*`, `task.new` | risk APIs, chain RPC, `posture.telegram.*` (rules only) |
| M5 Calendars | `mt_data.calendar` | ingest-batch | `text.calendar_event` | `cal.*` | FRED, ForexFactory, CB |
| M6 Features | `mt_features` | engine (incremental), batch | `features.value`, `features.def` | `feat.*` | `md.*`, `text.*`, `evt.*` |
| M7 Lab | `mt_lab` | backtest-worker, sandbox | `strategy.backtest`, `strategy.experiment` (+ MLflow) | `lab.job.*` | catalog, features |
| M8 Agents | `mt_agents` | agents | `audit.decision_run`, `audit.signal` (`Signal` fields in [03 M8](03-build-spec.md)) | `sig.agent.*` | RAG, memory, gateway |
| M9 Memory & RAG | `mt_memory` | agents, nlp, hindsight | `rag.doc_chunk`, `hindsight.*` | — | TEI |
| M10 Anomaly | `mt_anomaly` | anomaly | `audit.anomaly` | `alert.anomaly.*` | `md.*`, `text.*`, `evt.*`, `anomaly.explain` requests |
| M11 Risk | `mt_risk` | engine (in-process) + mt-api (policy) + deadman | `risk.policy`, `risk.limit_state`, `risk.change`, `risk.event`, `risk.approval` | `risk.*`, KV `risk_state`, `kill` | `ord.intent.*`, `dq.status.*`, `cost.*`, KV `audit.integrity`, `egress.status`, `posture.telegram.*` (rules only), `venue.registry.changed`, `sys.heartbeat.*` |
| M12 Execution | `mt_engine` | engine | `audit.order`, `audit.fill`, `audit.position_snapshot` | `ord.*`, `fill.*`, `pos.*` | venues |
| M13 MM sidecar | hummingbot + adapter | hummingbot | `audit.mm_*` | `mm.*` | Hummingbot API |
| M14 Crowd-sim | services/crowdsim | optional | `strategy.crowdsim_run` | — | — |
| M15 UI | `mt_ui` (web + telegram) | caddy, telegram-bot | `ops.user_pref`, `ops.notification` | — | WS topics |
| M16 Monitor | `mt_monitor` | monitor | `audit.dq_event`, `audit.dq_ack`, `audit.cost_event`, `market.spread_*`, `audit.recon` | `dq.status.*`, `cost.*`, `recon.*`, `egress.status` | `md.*`, `dq.raw.*`, fills, venues |
| M17 Observability & audit | `mt_obs` | all | `audit.*` hash chain, `audit.command`, `audit.llm_call` (from P0, LiteLLM callback), `audit.seal`, `audit.integrity_incident` | metrics, logs, KV `audit.integrity` | — |
| M18 Journal & tax | `mt_journal` | journal | `journal.*`, `ops.wallets` (account and address registry, created P3) | `journal.*`, `tax.residency.changed` | fills, ledgers, chain, airdrops |
| M19 Curation | `mt_curation` | curation, telegram-bot | `curation.task` (minimal table from P3 for tax questions; P5 extends it additively), `curation.community` | `task.*` | `airdrop.*`, `risk.approval.*` |
| M20 MCP | `mt_mcp` | mcp | — (via `mt_api`: `audit.mcp_call` for every MCP call, `audit.command` for commands) | — | `mt_api` |
| M22 Treasury & hold-and-earn | `mt_treasury` | treasury, wallet-indexer | `treasury.transfer`, `treasury.position`, `treasury.policy`; extends `ops.wallets` (P5) | `wallet.*`, `treasury.*` | chain RPC, venues, `risk.*` |
| M23 Social participation | `mt_social` | social | `curation.social_draft` | `social.draft.*` | `text.doc.*`, `task.*` |
| M21 Models | `mt_models` | engine (tier A), decision-svc, litellm, llm-local, tei-embed, tei-rerank | `models.registry`, `models.question`, `models.label`, `audit.tierb_decision` | `dec.tierb.*`, KV `tierb_scores` | `text.doc.*`, M8 teacher log |

**Naming rules:**
- **Audit tables are singular and schema-qualified.** The canonical names are `audit.order`, `audit.fill`, `audit.command`, `audit.llm_call`, `audit.dq_event`, `audit.dq_ack`, `audit.cost_event`, `audit.recon`, `audit.decision_run`, `audit.seal`, `audit.integrity_incident`, `audit.mcp_call` ([17 §B](17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)). Other docs use these names.
- **One wallet registry:** `ops.wallets` holds accounts and on-chain addresses. P3 creates it; the P5 wallet-indexer and M22 extend it additively. There is no `treasury.wallet`.
- **Telegram postures** (`text.telegram_posture`, `posture.telegram.*`) are consumed only by code/policy rules (M4, M11). Never by M6 features, tier A/B, agents or RAG.

## 5. Data architecture

### 5.1 Stores

| Store | Holds | Retention | Backup |
|---|---|---|---|
| **Postgres** (`market`, `text`, `features`, `strategy`, `risk`, `audit`, `journal`, `curation`, `ops`, `rag`, `models`, `treasury`, `hindsight`; **all 13 schemas created in P0**, tables added by later phases) | System of record: bars (hypertables + continuous aggregates at 1m, 5m, 15m, 1h, 4h, 1D, 1W; any other size via `time_bucket` at read time), business data, audit, journal, documents + embeddings | Audit/journal ≥ 7 years; bars forever (compressed); documents forever | pgBackRest: continuous WAL archive, nightly incremental, weekly full; restic off-site; monthly automated restore test; monthly immutable WORM export ([15 §2.2](15-bots-hitl-and-worm-audit.md#22-layers)) |
| **Parquet catalog** (Nautilus `ParquetDataCatalog`) | Raw trades, quotes, L2 deltas/snapshots, backfills. L2 deltas are recorded at native speed only for symbols a bot needs order-book data for (default ≤ 3); others get 1 s snapshots | Forever (hot NVMe 90 days → cold HDD) | restic (cold) |
| **NATS JetStream** | Streams (§6) + KV (`risk_state`, `kill`, `feed_status`, `tierb_scores`, `heartbeat`, `audit.integrity`) | Streams 24h–7d; KV latest. When Postgres is unreachable, WORM writes buffer here: default bound 1 GB or 24 h; above 80% new entries stop, exits continue ([16 §3.3](16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check)) | Not backed up (rebuildable) |
| **MLflow** | Experiments, model artifacts (ONNX, LoRA), metrics | Forever | restic |
| **Loki / Prometheus** | Logs 30–90d / metrics 90d | Rolling | Not backed up |
| **Secrets** | sops+age file **outside the repo** (e.g. `~/.config/mastertrader/`) → tmpfs | — | Encrypted copy off-site (restic) |

### 5.2 Key conventions

- **Time:**
  - `timestamptz` UTC everywhere, nanosecond precision kept in Parquet;
  - `event_time`, `ingest_time` on every fact;
  - the UI renders in the user's timezone (default Australia/Sydney).
- **IDs:** UUIDv7 (time-ordered). Instruments use the Nautilus `InstrumentId` (`BTCUSDT.BINANCE`).
- **Money:** `numeric` / `Decimal`, never floats, for prices, sizes, fees and tax. Each instrument's precision comes from instrument metadata.
- **Point-in-time:** `mt_store.pit(as_of)` is the only read path for research/backtests (CI-enforced).
- **WORM:** `audit.*`, `journal.*`, `risk.change`, `strategy.bot_version`, mandates and the signer ledger are write-once (offline owner role, INSERT/SELECT-only app roles, blocking triggers, per-row hash chain, daily externally anchored seal); corrections reference the row they supersede. See [15 §2](15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many).

### 5.3 Core entities (abbreviated; full DDL in migrations)

`instrument`, `bar`, `feature_value`, `document`, `telegram_posture`, `geo_event`, `calendar_event`, `strategy`, `strategy_version`, `strategy_run`, `bot`, `bot_version`, `backtest`, `experiment`, `signal` (fields in [03 M8](03-build-spec.md)), `decision_run`, `tierb_decision`, `order`, `fill`, `position_snapshot`, `risk_policy`, `risk_limit_state`, `risk_change`, `risk_event`, `risk_approval`, `mandate`, `dq_event`, `dq_ack`, `cost_event`, `recon`, `journal_event`, `lot`, `lot_match`, `fx_rate`, `residency_period`, `tax_report`, `airdrop_opportunity`, `token_risk_report`, `user_task`, `community_item`, `wallets`, `notification`, `command`, `llm_call`, `mcp_call`, `seal`, `integrity_incident`, `model_registry`, `question`, `label`.

Table names follow the §4 naming rules (singular, schema-qualified, e.g. `audit.recon`, `audit.mcp_call`).

## 6. Messaging (NATS)

**Subject taxonomy** (all payloads are versioned msgspec/JSON schemas in `mt_core.schemas`):

| Subject | Payload | Producers → consumers |
|---|---|---|
| `md.{venue}.{symbol}.trade` / `.quote` / `.book` / `.bar.{spec}` | Market data | ingest-market → engine, monitor, features, UI (throttled) |
| `dq.raw.{venue}.{symbol}` | Raw feed health: receive times, gaps, sequence breaks, clock skew | ingest-market → monitor |
| `dq.status.{venue}.{symbol}` | `ok \| degraded \| stale \| closed \| bad` + reasons | monitor → engine (risk), UI |
| `recon.{venue}` | Reconciliation result (positions, orders, balances; matched / explained / unexplained) | monitor → risk, journal, UI |
| `egress.status` | Egress IP and country check ([16 §3.2](16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys)) | monitor → risk, UI |
| `cost.{venue}.{symbol}` | spread/fee/funding/swap snapshot | monitor → risk, lab, UI |
| `feat.{name}.{symbol}` | Feature values | features → engine |
| `text.doc.new` | Document id + tickers + scores (never Telegram) | nlp → decision-svc, agents, UI |
| `posture.telegram.{subject}` | Structured Telegram posture (no text) | ingest-text → M4 airdrop rules, M11 rules, UI (D08). Never M6 features, tier A/B, agents or RAG |
| `evt.{kind}` / `cal.{kind}` | Global events / calendar items | ingest → risk (blackouts), agents, UI |
| `dec.tierb.{question}.{subject}` | Option probabilities | decision-svc → engine (KV), UI |
| `sig.{source}.{strategy}` | Signal | strategies/agents → engine |
| `engine.cmd.{command}` | Engine control (strategy and bot start/pause/resume/stop, mode, shadow runs) | mt-api → engine |
| `strat.status.{strategy}` / `bot.{id}.status` | Strategy and bot status | engine → mt-api, UI |
| `ord.intent.{strategy}` → `ord.risk.{decision}` → `ord.{state}` | Order lifecycle | engine/mt-api → risk → venue |
| `fill.{venue}` / `pos.{account}` | Fills / positions | engine → journal, monitor, UI |
| `risk.event` / `risk.approval.request` / `risk.approval.result` | Risk events and approvals (carry `bot_id`) | risk ↔ mt-api, telegram |
| `kill.set` / KV `kill` | Kill switch | mt-api/telegram/monitor → engine, deadman, hummingbot, airdrop-exec, treasury |
| KV `audit.integrity` | WORM integrity status from `audit.verify` (`ok` or the configured mismatch action) | mt_obs → M11 (read pre-trade), UI |
| `sys.heartbeat.{service}` | Liveness (every 1 s) | all → in-engine watchdog (dead-man layer 1); the engine's heartbeat also → `deadman` sidecar (layer 2) |
| `alert.{severity}.{kind}` | Alerts | all services, plus Grafana/Alertmanager via webhook → the single alert consumer → Telegram, ntfy, email, UI notifications |
| `task.new` / `task.updated` | User tasks | airdrop, curation, risk → telegram, UI |
| `journal.event.new` | Journal | journal → UI |
| `tax.residency.changed` | Residency period added or changed | journal → mt-api (venue registry recompute), UI |
| `wallet.{chain}.{address}.balance` / `.transfer` / `.approval` / `.nonce_authority` | Wallet events | wallet-indexer → risk, journal, UI |
| `treasury.intent` / `treasury.result` / `treasury.depeg` | Treasury moves and depeg alerts | treasury ↔ risk, signer; → UI |
| `social.draft.new` / `social.draft.decision` | Social drafts | social → telegram, UI |
| `venue.registry.changed` | Venue registry updates | mt-api → risk, engine |

**Rules:**
- **Dead-man's switch (three layers, [16 §3.1](16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)):**
  1. The in-engine watchdog consumes `sys.heartbeat.*`. A critical component (feeds, risk, postgres, nats) missing for 5 s (default) → cancel open orders for affected bots; 10 s (default) → apply each bot's `on_system_failure` (default `flatten`).
  2. The `deadman` sidecar watches the **engine's** heartbeat with its own keys and venue connections: missing 5 s → cancel all open orders; 10 s → flatten per `on_system_failure`.
  3. Venue-side cancel-after timers and resting stops cover a dead host or network.
- **Telegram `/kill` when mt-api is down:** the bot publishes `kill.set` with NATS credentials that may publish nothing else. The engine writes the kill event to WORM with source `telegram`.
- **One alert path:** nothing sends alerts directly to a channel; everything goes through `alert.*`, so dedupe happens in one place.
- **UI streams** are fanned out by mt-api over WebSocket topics with server-side throttling (≤ 4 Hz per symbol in charts, ≤ 1 Hz in tables).

## 7. API contract (`mt_api`)

**Transport and auth:**
- FastAPI under `/api/v1`, with OpenAPI generated and versioned.
- Auth: single user, local login (Argon2) + **TOTP**, over Tailscale only. Session cookie (`SameSite=Strict`, `HttpOnly`) for the web; scoped tokens for Telegram and MCP (MCP token rules in §7.4).

**Conventions:**
- JSON bodies with snake_case keys.
- Decimals are sent as strings.
- Times are ISO-8601 UTC.
- Pagination is cursor-based.
- Errors use RFC 9457 problem+json.

### 7.1 Queries (REST, read)

| Endpoint | Purpose |
|---|---|
| `/portfolio/summary` | Value, P&L, margin, exposure, drawdown |
| `POST /risk/preview` | Dry-run pre-trade checks for an intent (no side effects) |
| `/positions`, `/orders`, `/fills` | Positions, orders, fills (`/orders?source=web\|telegram\|mcp\|system`) |
| `/bots`, `/bots/{id}`, `/bots/{id}/approvals`, `/approvals?status=pending` | Bots and HITL approvals ([15 §1.5](15-bots-hitl-and-worm-audit.md#15-api-data-and-ui)) |
| `/markets/instruments`, `/markets/{id}/bars?spec=&from=&to=` | Instruments, bars |
| `/markets/{id}/book`, `/markets/matrix` | Order book, cross-asset matrix |
| `/strategies`, `/strategies/{id}`, `/strategies/{id}/runs`, `/strategies/templates`, `/strategies/{id}/gate-report` | Strategies; gate report against the strategy's gate profile ([16 §2.4](16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile)) |
| `/lab/backtests`, `/lab/backtests/{id}`, `/lab/experiments`, `/lab/jobs` | Research lab |
| `/agents/runs`, `/agents/runs/{id}`, `/signals` | Agent runs, signals |
| `/models/registry`, `/models/questions`, `/models/tierb/decisions`, `/models/benchmarks`, `/models/gateway/spend`, `/models/labels`, `/models/labels/queue` | Models; labels and the labelling queue |
| `/memory/search`, `/memory/banks`, `/rag/search` | Memory and document search |
| `/risk/policy`, `/risk/state`, `/risk/events`, `/risk/changes`, `/risk/stress` | Risk. `/risk/policy` returns the effective value of each setting and the layer (L0–L4) that set it ([16 §1](16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance)); `/risk/changes?source=` filters by source |
| `/risk/capital-steps`, `/risk/kill-criteria` | Capital-step plan and state per sleeve/bot, kill-criteria state (Phase 7, [16 §2.5–2.6](16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot)) |
| `/data/feeds`, `/data/quotas`, `/data/dq-events`, `/data/costs`, `/data/recon` | Data quality, costs, reconciliation |
| `/intel/documents` (+ `/{id}`), `/intel/events`, `/intel/calendar`, `/intel/sentiment` | Intel |
| `/mm/bots` (+ `/{id}`, `/{id}/pnl`) | Market-making bots |
| `/airdrops`, `/airdrops/{id}`, `/airdrops/mandates`, `/airdrops/wallet` | Airdrops |
| `/tasks` (+ `/{id}`), `/community`, `/social/drafts` | Tasks, curation and social drafts |
| `/wallets` (+ `/{id}`, `/transfers`), `/treasury`, `/treasury/earn` | Unified wallet view, treasury, hold-and-earn |
| `/venues/registry` | Venue access registry (12 §2) |
| `/journal/trades` (+ `/{id}`), `/journal/events`, `/journal/lots`, `/journal/reviews` | Journal; weekly reviews (Phase 7) |
| `/tax/summary?fy=`, `/tax/reports`, `/tax/residency` | Tax |
| `/system/health`, `/system/services` (`?kind=`), `/system/logs` (Loki proxy), `/system/backups`, `/system/keys` (masked metadata only), `/system/settings`, `/system/preflight` | System; go-live preflight (Phase 7) |
| `/mcp/tools`, `/mcp/tokens`, `/mcp/sessions` | MCP tool registry, tokens (metadata only, never the secret), sessions (Phase 8) |
| `/audit/log` (`?source=`), `/audit/integrity` | Audit log; WORM integrity status and incidents |
| `/notifications` | Notifications |

### 7.2 Commands (REST, write)

`POST /api/v1/commands/{command}`:
- Body: `{ "args": {...}, "idempotency_key": "...", "reason": "...", "confirm_token": "..." }`.
- `POST /api/v1/commands/{command}/preview` validates the args, runs the risk preview where relevant, and returns the confirmation level plus a `confirm_token` bound to the exact args. Executing a C1+ command without a valid token returns `428 Precondition Required`.
- Every command is written to `audit.command` with source = `web | telegram | mcp | system`.

**Confirmation levels** (enforced server-side, never only in the UI):

| Level | When | Flow | Server check |
|---|---|---|---|
| **C0** | Reads, harmless toggles (UI prefs, marking a task) | None | — |
| **C1** | Reversible or tightening actions (pause a bot, cancel order, run backtest, tighten a limit) | In-app confirm sheet | Explicit `confirm_token` from the preview call |
| **C2** | Trading actions (place/modify order, flatten, switch a bot `paper` → `hitl`) | Confirm sheet showing the risk-check preview; hold-to-confirm on touch | Token carries a hash of the risk preview bound to the exact command, and the session re-authenticated within 12 h |
| **C3** | **Loosening risk**: loosen any setting on any layer (incl. the L0 hard ceilings, [16 §1](16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance)), switch a bot to `autonomous`, new mandate, kill switch OFF | C2 + **Telegram approve + TOTP**, then a cool-down (default 15 min, configurable) before it takes effect | C2 checks + a Telegram approval and TOTP for this command id |
| **Kill** | Kill switch ON | Single confirm (never blocked); turning it OFF is C3 | — |

**Before Telegram C3 exists (P0–P1):** C3 commands complete through a host-only break-glass CLI, `mtctl approve <id>` + TOTP, over SSH on Tailscale; audited like any C3. It is retired once Telegram C3 works (P2).

Every C3 approval and every settings change is a WORM row (`audit.command`, `risk.change`).

**Command catalogue (v1):**

| Group | Commands |
|---|---|
| Orders | `order.place`, `order.modify`, `order.cancel`, `order.cancel_all`, `position.close` (`{halt: true, reason}` = flatten-and-halt the bot), `position.reduce`, `position.set_brackets` |
| Approvals | `approval.approve`, `approval.approve_partial`, `approval.reject` ([15 §1.5](15-bots-hitl-and-worm-audit.md#15-api-data-and-ui)); never callable from MCP (§7.4) |
| Strategies | `strategy.create`, `strategy.update_params`, `strategy.clone`, `strategy.archive`, `strategy.start`, `strategy.pause`, `strategy.resume`, `strategy.stop`, `strategy.promote`, `strategy.demote`, `strategy.run_shadow` (C1). A strategy is **promoted through gates**; modes are set per bot |
| Bots ([15 §1](15-bots-hitl-and-worm-audit.md#1-trading-bots)) | `bot.create`, `bot.update_scope`, `bot.update_params` (incl. `on_system_failure`), `bot.set_mode` (`paper` C1, `paper` → `hitl` C2, `autonomous` → `hitl` C1, → `autonomous` **C3**), `bot.start`, `bot.pause`, `bot.resume`, `bot.stop`, `bot.approval_policy.set` |
| Lab | `lab.backtest.run`, `lab.sweep.run`, `lab.validate.run`, `lab.generate_strategy`, `lab.job.cancel`, `lab.leakage.waive` (C2, reason required, audited), `lab.gate_report.generate` |
| Agents & models | `agents.run_analysis`, `models.tierb.ask`, `models.tiera.train` (C1: train → calibrate → compile), `models.label.add` (C0), `models.promote`, `models.rollback`, `models.bakeoff.run`, `models.question.update`, `memory.delete`, `anomaly.explain` (C1; result arrives as a notification) |
| Market making | `mm.bot.create`, `mm.bot.start`, `mm.bot.stop`, `mm.bot.update`, `mm.bot.cancel_all` |
| Risk | `risk.policy.update` (diff on any layer L0–L4, including the hard-ceilings section of the bot strategy settings; tighten = C1 and immediate, loosen = C3), `risk.kill.on`, `risk.kill.off`, `risk.deadman.ack`, `risk.stress.run`, `risk.sleeve.restart` (C3; after a sleeve drawdown or health halt), `risk.capital.fund` (C3), `risk.capital_step.approve` (C3), `risk.review.close` (C3) |
| Data | `data.feed.pause`, `data.feed.resume`, `data.backfill.run`, `data.recon.run`, `data.incident.ack` (C0; appends an `audit.dq_ack` row, never updates the incident) |
| Intel | `intel.source.add`, `intel.source.mute`, `intel.watchlist.update` |
| Airdrops | `airdrop.add_url`, `airdrop.rescore`, `airdrop.reject`, `airdrop.mandate.create` (C3), `airdrop.mandate.revoke`, `airdrop.claim.execute` (C2 unless covered by a mandate), `wallet.revoke_approval`, `wallet.sweep` |
| Tasks | `task.done`, `task.skip`, `task.snooze`, `task.never`, `task.answer` (C1; e.g. a tax-agent answer), `social.draft.approve` (C1, opens a web intent), `social.draft.reject` |
| Wallets & treasury | `wallet.register` (C1), `wallet.tag` (C1), `treasury.allocate` (C2; loosening policy C3), `treasury.earn.enter` / `treasury.earn.exit` (C2) |
| Venues & ladder | `venue.registry.update` (tighten C1, allow C3), `risk.ladder.set` (down C1, up C3) |
| Journal & tax | `journal.note.add` (optional attachment, stored content-addressed under `data/attachments/` and referenced by hash), `journal.tag`, `journal.manual_event.add` (C2), `journal.review.signoff`, `tax.report.generate`, `tax.export`, `tax.residency.add` (emits `tax.residency.changed`; any loosening it causes in the venue registry is C3), `tax.regime.set`, `tax.lot.select`, `tax.fy.lock` / `tax.fy.unlock` (C3) |
| System | `system.backup.run`, `system.restore.test`, `system.key.rotate_reminder`, `system.settings.update`, `system.service.restart` (allow-listed containers only, via `docker-proxy`), `audit.verify`, `audit.integrity.ack` (C3; clears a WORM verify mismatch after investigation, [16 §2.11](16-configuration-and-safety-model.md#211-worm-integrity)), `ops.drill.record` |
| MCP (Phase 8) | `mcp.token.create` (C1; C3 for indefinite expiry or the `trade`, `strategy`, `risk_tighten` scopes), `mcp.token.revoke`, `mcp.tool.set`, `mcp.policy.set` |

### 7.3 Real-time (WebSocket `/api/v1/ws`)

- **Protocol:** subscribe/unsubscribe to topics: `{op: "sub", topic: "md.bar", params: {...}}`.
- **Topics:**
  - `portfolio`, `positions`, `orders`, `fills`;
  - `md.quote`, `md.trade`, `md.book`, `md.bar`;
  - `dq.status`, `cost`;
  - `risk.state`, `risk.event`, `kill`, `heartbeat`;
  - `bots`, `approvals`;
  - `signals`, `tierb`, `agents.run`;
  - `text.doc`, `evt`, `cal`;
  - `airdrop`, `tasks`, `journal`, `notifications`, `alert`, `lab.job`, `system`;
  - `wallet` (P5), `treasury` (P6);
  - `mm`, `recon`.
- **Message envelope:** `{topic, seq, ts, data}`. The client detects gaps via `seq` and re-syncs with the matching REST query.

### 7.4 Telegram & MCP

- **Telegram** maps buttons and slash commands to the same commands. It holds the **C3 confirmation** channel (approve + TOTP prompt) from P2; before that, the break-glass CLI (§7.2). When mt-api is down, `/kill` still works via NATS (§6).
- **MCP** (Phase 8) exposes the queries plus a subset of commands ([16 §2.12](16-configuration-and-safety-model.md#212-mcp-phase-8)):
  - **Levels for `source = mcp`:** C0 reads run directly; C1 runs if the token has the scope; C2 orders **always** create an approval card on Telegram/web (TTL default 5 min, expiry = reject), with no "skip approval" option; C3 goes through Telegram + TOTP as usual.
  - **MCP can never approve** anything, its own orders included. Approvals come only from you on Telegram or the web.
  - **Never exposed:** withdrawals, `wallet.sweep`, `treasury.*` moves, `airdrop.claim.execute`, mandates, key and token management, `approval.*`, `mcp.*`, restore/delete, audit writes. Loosening risk is never a scope.
  - **Tokens:** opaque 256-bit, shown once, stored hashed (HMAC-SHA-256 with a server pepper), scoped (`read`, `analyse`, `trade`, `strategy`, `risk_tighten`, `curation`), revocable instantly, last use and client identity recorded. Expiry is chosen per token (1 day · 7 days · 30 days · 1 year · custom · indefinite; indefinite shows a warning, needs C3 and a monthly reminder). OAuth 2.1 (PKCE, resource indicators) for clients that support MCP authorization.
  - **Transport:** Streamable HTTP (JSON-RPC 2.0, SSE streaming, resumable) at `/mcp` on Caddy, Tailscale/TLS only; stdio locally; an optional legacy HTTP+SSE endpoint for older clients. Server notifications (fills, approvals, alerts) via resource subscriptions.
  - **Responses** pass the same provenance filter as any model input: no Telegram text, no `model_input_ok = false` rows, tax PII redacted, untrusted text wrapped and marked.
  - **Audit:** every MCP call, reads included, is a WORM row in `audit.mcp_call`; commands are also in `audit.command`. Default limits: 60 reads/min and 10 writes/min per token, 256 KB per result.

## 8. End-to-end flows

**F1: Market data → bars → quality**
1. Venue WebSocket → Nautilus data client (ingest-market).
2. Publish `md.*`.
3. Parquet recorder (1–5 min files, daily compaction).
4. Bar builder writes 1s/1m bars into Timescale; continuous aggregates build to 1D.
5. The monitor checks staleness, gaps, outliers, cross-source divergence and clock skew → `dq.status.*`.
6. The risk manager blocks orders on `stale`/`bad`.
7. The UI shows feed health.

**F2: Signal → decision → risk → order → fill → journal → TCA**
1. A strategy (M0) receives `md`/`feat`/`tierb` inputs.
2. Decision One tier A (µs) produces a calibrated edge.
3. Deterministic sizing → `OrderIntent`.
4. **M11 pre-trade checks:** policy limits, collar, liquidity/spread, DQ status, blackout, duplicate check.
5. Mode routing:
   - `auto`: submit;
   - `approve`: `risk.approval.request` → UI/Telegram → approve within TTL or expire;
   - `paper`: simulated fill.
6. Venue fill → `fill.*`.
7. **Journal (M18)** records the fill + fees; the lot engine updates.
8. **Monitor (M16)** computes implementation shortfall vs the decision/arrival price and updates the realised-vs-modelled cost ratio.
9. **Grafana and the UI** update; the audit row is chained.

**F3: Text → decision models → features**
1. A feed (RSS / Telegram / Discord / Bluesky / GDELT) arrives.
2. ingest-text normalises it and dedupes.
3. The nlp service runs:
   - the relevance gate (tier B / SemIf);
   - entity/ticker linking;
   - FinBERT sentiment;
   - TEI embeddings.
4. The result goes to `text.document` + `rag.doc_chunk`.
5. `text.doc.new` triggers decision-svc questions (direction, event type, veto…).
6. `dec.tierb.*` updates KV `tierb_scores`, which tier A reads as features.
7. High-severity veto → `risk.event` (above the calibrated threshold only).

**F4: Research debate → signal → teacher log → distillation**
1. A scheduled or event-triggered `agents.run_analysis` (M8, via the LiteLLM gateway) runs with RAG + memory recall.
2. It produces a structured `Signal` with provenance.
3. The signal is stored in `audit.decision_run`, and Hindsight retains the episode.
4. After the horizon, **settlement** computes the outcome and the agent writes a reflection.
5. A nightly Prefect flow distils teacher + outcomes into tier A / tier B candidates.
6. Candidates are calibrated and benchmarked, then promoted only through the gates (models registry).

**F5: Risk policy change**
1. The UI/Telegram/MCP sends `risk.policy.update` with a diff.
2. The server classifies each field:
   - **tighten** → applied immediately, audited, notified;
   - **loosen** → C3: Telegram approve + TOTP → cool-down → applied.
3. Changes above the **hard ceilings file** are always rejected.

**F6: Kill switch & dead-man**
1. **Triggers:**
   - `risk.kill.on` from any client;
   - an automatic breach (daily loss, drawdown, DQ, error rate, cost blow-out);
   - a missing heartbeat.
2. KV `kill = ON`, then:
   - the engine cancels all orders and optionally flattens;
   - Hummingbot stops;
   - airdrop-exec freezes;
   - the UI shows a global red banner.
3. **Turning it off** is C3, and requires the trigger condition to be cleared.

**F7: Strategy lifecycle**
1. `draft` (create/template/generate in the sandbox).
2. `backtested`.
3. `validated` (walk-forward, MC permutation, deflated Sharpe, look-ahead check).
4. `paper`.
5. `approve` mode.
6. `auto`. Each promotion checks the gates and is audited, and `auto` is C3.

**F8: Airdrop**
1. Discover → normalise/dedupe → enrich → risk-score (GoPlus / RugCheck / Honeypot.is / heuristics / blocklists) → viability score.
2. Decide:
   - **reject**, with reasons;
   - **user task** (steps, verified links);
   - **auto-claim**, only if an active mandate covers it. Auto-claims go through simulation → signer → the journal (income classification).

**F9: Tax**
1. Fills, ledgers, funding, airdrops and staking events become journal events.
2. FX conversion uses the RBA rate (AUD).
3. The lot engine applies specific-ID with FIFO fallback.
4. The jurisdiction plugin by residency period runs: AU_2026, then AU_2027_REFORM.
5. Outputs:
   - **quarterly:** PAYG instalment estimate;
   - **at EOFY:** myTax worksheet + CGT schedule + accountant pack + Beancount export.
6. **Snapshot jobs:** 30 Jun 2027, and on any residency change (CGT event I1).

**F10: Curation loop**
1. Sources (airdrops, Discord/Telegram discovery, risk approvals, tax questions) create `user_task`s.
2. Delivery: instant alerts or daily/weekly digests (Telegram + UI).
3. You tap Done / Skip / Snooze / Never.
4. Feedback updates the ranking.
5. For Discord follow tasks, the bot verifies that posts arrive.

**F11: Backup & incident**
- **Backups:** nightly backup → weekly full → monthly restore test → alert on any failure.
- **Incident runbooks** in `docs/runbooks/`: keys leaked, server down with open positions, bad data, wallet drained.

## 9. Cross-cutting

### 9.1 Security

See [07-security-notes.md](07-security-notes.md):
- **Network segmentation** (§3.1).
- **Exchange/broker keys:** trade-only scope, withdrawals disabled, IP allow-listed, per-mode sub-accounts.
- **Secrets and roles:** secrets via sops; least-privilege DB roles.
- **Untrusted input:** LLMs never see secrets; scraped text is marked untrusted.
- **Server-side confirmation levels** (§7.2).

### 9.2 Observability & SLOs

| SLO | Target | Measured by |
|---|---|---|
| Decision One tier A latency | p99 < 50 µs per prediction | In-process histogram |
| Pre-trade risk check | p99 < 1 ms | Engine metrics |
| Strategy signal → order submitted (`auto`) | p99 < 5 ms (excl. venue) | Trace spans |
| Tier B decision | p95 < 50 ms (GPU, 0.6B head) | decision-svc metrics |
| Feed staleness detection → strategy paused | < 2 s | Monitor |
| UI live update lag (server → screen) | p95 < 500 ms | Client telemetry (local only) |
| Kill switch → all cancels sent | < 1 s | Engine metrics |
| Backup restore test | Monthly pass | Prefect flow |

### 9.3 Degraded modes

| Failure | System behaviour | UI behaviour |
|---|---|---|
| A feed is stale/bad | Strategies using it pause; no new orders on that instrument | Amber/red feed chip; banner on affected screens |
| Venue disconnect | Reconnect with backoff; affected orders flagged unknown → reconcile | Venue chip red; positions marked "unconfirmed" |
| Postgres down | Engine continues in memory with risk limits; journal buffered in NATS (bounded); dead-man after the threshold | Red system banner, read-only UI |
| LLM gateway/budget exhausted | Falls back to local models; agents degrade | "Local models" badge |
| GPU unavailable | Tier B on CPU (slower) or disabled; tier A unaffected | Tier B status degraded |
| mt-api down | Engine unaffected; Telegram `/kill` still works via the bot → NATS | Web unreachable; Telegram alert |

## 10. Frontend architecture

| Concern | Choice | Why |
|---|---|---|
| App | **React 18 + TypeScript + Vite**, single-page app served by Caddy; **PWA** (installable on phone/tablet) | Simple, fast, one codebase for all form factors |
| Routing / data | **TanStack Router** + **TanStack Query** (REST) + a typed WebSocket client feeding the Query cache | Typed routes, cache, re-sync on gaps |
| State | Zustand for UI state (layout, density, theme, workspace) | Small, no boilerplate |
| Styling | Tailwind (local build) with the **DESIGN.md v2 preset** (tokens + breakpoints + container queries) | Matches the design system |
| Components | Headless primitives (**Radix UI**) styled to DESIGN.md; own component library `apps/web/src/components` | Accessible dialogs, sheets, menus |
| Charts | **TradingView lightweight-charts** (Apache-2.0) for price; **ECharts** (Apache-2.0) for analytics (heatmaps, distributions, equity curves) | Performant, free |
| Tables | **TanStack Table** + **TanStack Virtual** | Large blotters/logs |
| Forms | react-hook-form + zod (schemas generated from OpenAPI) | Validation matches the backend |
| API types | `openapi-typescript` generated from `mt_api` | One contract |
| Testing | Vitest + Testing Library; **Playwright viewport matrix** (DESIGN.md §6.8); axe accessibility checks | Responsive + a11y gates |
| Telegram | Bot (python-telegram-bot) in `mt_ui.telegram`; optional Telegram Mini App reusing web routes | Mobile approvals and alerts |

Layout model: app shell (DESIGN.md §6.4) + **workspaces**.
- A dashboard is a grid of tiles; tiles are container-query components.
- Users can rearrange and save layouts per breakpoint tier (persisted in `ops.user_pref`).

## 11. Repository layout

```
MasterTrader/
├── packages/            # Python: mt_core, mt_store, mt_data, mt_features, mt_strategy, mt_lab, mt_agents, mt_memory,
│                        #         mt_anomaly, mt_risk, mt_engine, mt_monitor, mt_obs, mt_journal, mt_airdrop,
│                        #         mt_curation, mt_models, mt_api, mt_ui (telegram), mt_mcp
├── apps/web/            # React app (src/routes, src/components, src/tiles, src/lib/api, src/lib/ws, tailwind preset)
├── services/            # hummingbot, rss-bridge, crowdsim, compose overrides
├── strategies/          # user strategies + manifests
├── infra/               # docker-compose.yml, caddy, grafana dashboards, prometheus rules, alertmanager, sops config
├── migrations/          # Alembic
├── third_party/         # vendored code + LICENSES.md
├── tests/  notebooks/  docs/ (+ docs/ui, docs/runbooks)  ui-examples/  brand/  DESIGN.md
```

## 12. End-to-end build plan

Each phase ends with a usable demo; details are in [04-plan-of-action.md](04-plan-of-action.md).

| Phase | Backend deliverables | Frontend deliverables (see [ui/](ui/README.md)) | Exit criteria |
|---|---|---|---|
| 0 Foundations | Host hardening, compose, Postgres/NATS/Prefect/obs/MLflow/LiteLLM/TEI, schemas + `pit`, audit chain, `mt_api` skeleton (auth + TOTP, commands, WS), backups | Web shell (top bar, nav, status bar, kill-switch placeholder), design preset, component library v0, **System** dashboard (health), Playwright matrix in CI | Stack healthy; login + TOTP; responsive shell passes matrix |
| 1 Data & monitoring | ingest-market, Parquet recorder, bar builder, batch macro/fundamentals, quota tracker, **monitor** (DQ, costs, recon) | **Data & Quality**, **Markets** (charts, matrix, instrument detail), notifications | Live bars tick→1D for all asset classes; DQ alerts on Telegram |
| 2 Strategies, risk, lab | Strategy framework + templates, **risk manager**, engine paper/testnet, custom adapters (Alpaca/OANDA/IG), lab (backtest/validate/optimise/MLflow), tier A runtime, sandbox generator, Telegram bot v1 | **Cockpit**, **Strategies**, **Research Lab**, **Execution**, **Risk** | Any strategy type created → backtested with measured costs → paper behind risk; kill switch drill passes |
| 3 Journal & tax | Journal ingestion, FX service, lot engine, AU_2026 (+ 2027 scaffold), residency, exports | **Journal**, **Tax & Reports** | Every paper fill auto-journalled; FY-to-date AU summary + PAYG estimate |
| 4 Intel | ingest-text/events, RSS-Bridge, nlp pipeline, RAG, calendars, SemIf tier B | **Intel** (news/social/events/calendar), tier B outputs on Markets/Cockpit | Morning brief; calendar blackouts enforce in risk |
| 5 Airdrops & curation | airdrop pipeline, risk feeds, mandates + signer + Anvil simulation, task queue + digests, custody tiers, wallet-indexer (unified wallet view) | **Airdrops & Launches**, **Tasks & Curation**, **Wallets & Treasury** (view) | Weekly vetted digest; simulated auto-claim on testnet |
| 6 AI & models | Agents (debate), Hindsight, decision-svc (own head), distillation, anomaly, optional Hummingbot, M22 hold-and-earn, optional M23 social drafts | **Agents & Decisions**, **Models & Memory**, **Market Making** | Sourced signals; bake-off report; anomaly explanations |
| 7 Prove → small live | Live sub-accounts, reconciliation hardening | Approvals polish, mobile polish | Gates passed per strategy; ≥ 3 months paper/approve |
| 8 MCP | `mt_mcp` over `mt_api` | **MCP Console** (audit of MCP sessions) | Claude can analyse/adjust with approvals |

## 13. Asset coverage & promotion gates

| Asset class | Free data | Execution |
|---|---|---|
| Crypto spot / perps | Exchange WebSockets (ticks, L2), data.binance.vision, CoinGecko, DefiLlama | Nautilus (Binance, Bybit, OKX, Coinbase, Kraken, Hyperliquid), Hummingbot |
| Forex & metals | OANDA/IG streams, Dukascopy ticks, ECB/Frankfurter, FRED | OANDA v20, IG, IBKR; optional cTrader/Saxo/MT5 |
| Commodities | EIA, USDA, COT, Baker Hughes; daily futures | CFDs (OANDA/IG), crypto perps; IBKR futures (data is paid) |
| Stocks / ETFs | Alpaca IEX (real-time, 30 symbols), yfinance, EDGAR | Alpaca, IBKR |
| Bonds / rates | Treasury, FRED/ALFRED, sdmx1 | Bond ETFs, Treasury futures (IBKR) |
| IPOs | EDGAR S-1/424B, exchange calendars | Alpaca / IBKR after listing |
| ICOs / airdrops | M4 tracker + risk feeds | Auto-claim (eligible, safe) or user task |
| Prediction markets | Kalshi / Polymarket public reads | Signal source; Polymarket adapter optional |

**Promotion gates (per strategy, configurable):**
1. **Performance:** walk-forward out-of-sample results beat the benchmark after **measured** costs.
2. **Robustness statistics:** Monte Carlo permutation p < 0.05; deflated Sharpe > 0.
3. **Bias checks:** look-ahead and recursive analysers clean.
4. **LLM components:** tested only on data after the model's training cutoff.
5. **Paper/approve period:** default ≥ 3 months, with P&L and costs tracking the backtest.
6. **Safety drills:** kill switch, dead-man's switch and DQ pause exercised.
