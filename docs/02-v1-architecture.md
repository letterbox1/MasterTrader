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
          IBKR, Binance, Bybit, OKX,  (M1–M5, quota-       (Claude, your custom   airdrop identity-wallet claims)
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
| `core` | mt-api, all app services (incl. `intel-writer` and the alert consumer `telegram-bot`), nats, postgres, mlflow, tei-embed, tei-rerank, litellm, llm-local, hindsight, deadman, ib-gateway | Venues and LLM APIs via allow-list; venue traffic via the egress exit node from P7 | Business logic. `mcp` is **not** on `core`: it reaches only `mt_api` |
| `scrape` | ingest-text, rss-bridge, crawl4ai | Yes (wide) | Untrusted fetching; **no route to postgres or signer** (publishes to NATS via a narrow NATS account) |
| `signer` | signer | Chain RPC only | Hot-wallet signing; accepts intents only from the policy service (airdrop-exec in P5; treasury and DEX execution go through it, [13 §2](13-wallets-treasury-and-onchain.md)) |
| `ctl` | mt-api, docker-proxy | — | Restricted Docker-socket proxy: `system.service.restart` may restart only allow-listed containers; no other Docker API |
| `obs` | grafana, loki, prometheus, vector, alertmanager; `telegram-bot` (alert consumer, from P1) | P0 only: Telegram API for the interim direct Alertmanager route. None once the P1 fan-out exists | Observability. From P1, alerts leave only through the single `alert.*` fan-out (§6) |

**Alerts (P0 → P1):**
- **P0** has no fan-out yet, so Alertmanager sends straight to Telegram (the `obs` Telegram egress above). This route is temporary.
- **From P1** (P1-T045), Alertmanager and Grafana send only to the alert consumer's webhook, and the direct route and the `obs` Telegram egress are removed.
- The alert consumer (`telegram-bot`) joins `core` (NATS `alert.*`), `obs` (the Grafana/Alertmanager webhook) and `edge` (publishing to ntfy through Caddy).
- Its own egress allow-list adds only the Telegram Bot API and your configured SMTP host. No other container or network gains egress.

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
| `ingest-text` | `mt_data.text` | RSS, Telegram (Telethon + Bot), Discord bot, Bluesky, Mastodon, GDELT, on `scrape` with no DB route: publishes `raw.*` and `posture.telegram.*` only. **Telegram: postures only** (regex extractor → `posture.telegram.*`; never to nlp, RAG or models, F3b) | 4 |
| `crawl4ai` | crawl4ai | Fallback extractor for JS-rendered pages (trafilatura first); on `scrape`, publishes `raw.text.*` only | 4 |
| `intel-writer` | `mt_data` (writer worker) | Core-side writer for scrape outputs: `posture.telegram.*` → `text.telegram_mention` / `text.telegram_posture`, `raw.evt.*` → `text.geo_event`, `raw.reg.*` → regulatory-watch snapshots. No model clients; INSERT-only on its tables | 4 |
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
| M2 News & social | `mt_data.text` | ingest-text, nlp | `text.document`, `text.source`, `text.telegram_mention`, `text.telegram_posture` (both `model_input_ok = false`, `train_ok = false`; written by `intel-writer`) | `raw.*`, `text.doc.*` (never Telegram), `posture.telegram.*` | feeds |
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
| **NATS JetStream** | Streams (§6) + KV (`risk_state`, `kill`, `feed_status`, `tierb_scores`, `heartbeat`, `audit.integrity` (bucket `audit`, key `integrity`), `worm_buffer`) | Streams 24h–7d; KV latest. When Postgres is unreachable, WORM writes buffer here: default bound 1 GB or 24 h; above 80% new entries stop, exits continue ([16 §3.3](16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check)) | Not backed up (rebuildable) |
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
- **WORM:** `audit.*`, `journal.*`, `risk.change`, `strategy.bot_version`, mandates and the signer ledger (`audit.signer_ledger`) are write-once (offline owner role, INSERT/SELECT-only app roles, blocking triggers, per-row hash chain, daily externally anchored seal); corrections reference the row they supersede. See [15 §2](15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many).

### 5.3 Core entities (abbreviated; full DDL in migrations)

| Schema | Core tables |
|---|---|
| `market` | `market.instrument`, `market.bar_*`, `market.macro_series`, `market.filing` |
| `text` | `text.document`, `text.source`, `text.telegram_mention`, `text.telegram_posture`, `text.geo_event`, `text.calendar_event` |
| `features` | `features.value`, `features.def` |
| `strategy` | `strategy.registry`, `strategy.versions`, `strategy.runs`, `strategy.bot`, `strategy.bot_version`, `strategy.backtest`, `strategy.experiment` |
| `risk` | `risk.policy`, `risk.limit_state`, `risk.change`, `risk.event`, `risk.approval` |
| `audit` | `audit.order`, `audit.fill`, `audit.position_snapshot`, `audit.signal` (fields in [03 M8](03-build-spec.md)), `audit.decision_run`, `audit.tierb_decision`, `audit.dq_event`, `audit.dq_ack`, `audit.cost_event`, `audit.recon`, `audit.command`, `audit.llm_call`, `audit.mcp_call`, `audit.seal`, `audit.integrity_incident` |
| `journal` | journal events, lots, lot matches, FX rates, residency periods, tax reports (`journal.*`) |
| `curation` | `curation.task` (user tasks), `curation.community`, `curation.airdrop_*` (opportunities, token risk reports), `curation.mandate`, `curation.exec_log`, `curation.social_draft` |
| `ops` | `ops.wallets`, `ops.venue_registry`, `ops.user_pref`, `ops.notification` |
| `models` / `rag` / `treasury` / `hindsight` | `models.registry`, `models.question`, `models.label`; `rag.doc_chunk`; `treasury.transfer`, `treasury.position`, `treasury.policy`; `hindsight.*` |

Table names follow the §4 naming rules (singular, schema-qualified).

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
| `raw.text.{source}` / `raw.evt.{kind}` / `raw.reg.{source}` | Raw fetched items from the `scrape` side (narrow NATS account, publish-only) | ingest-text, crawl4ai → nlp (`raw.text.*`, never Telegram); ingest-events → `intel-writer` (`raw.evt.*`); regulatory watch → `intel-writer` (`raw.reg.*`) |
| `text.doc.new` | Document id + tickers + scores (never Telegram) | nlp → decision-svc, agents, UI |
| `posture.telegram.{subject}` | Structured Telegram postures and mentions (no text) | ingest-text → `intel-writer` (stores `text.telegram_mention` / `text.telegram_posture`), M4 airdrop rules, M11 rules, UI (D08). Never M6 features, tier A/B, agents, RAG or MCP |
| `evt.{kind}` / `cal.{kind}` | Global events / calendar items | ingest → risk (blackouts), agents, UI |
| `dec.tierb.{question}.{subject}` | Option probabilities | decision-svc → engine (KV), UI |
| `sig.{source}.{strategy}` | Signal | strategies/agents → engine |
| `engine.cmd.{command}` | Engine control (strategy and bot start/pause/resume/stop, mode, shadow runs) | mt-api → engine |
| `strat.status.{strategy}` / `bot.{id}.status` | Strategy and bot status | engine → mt-api, UI |
| `ord.intent.{strategy}` → `ord.risk.{decision}` → `ord.{state}` | Order lifecycle | engine/mt-api → risk → venue |
| `fill.{venue}` / `pos.{account}` | Fills / positions | engine → journal, monitor, UI |
| `risk.event` / `risk.approval.request` / `risk.approval.result` | Risk events and approvals (carry `bot_id`) | risk ↔ mt-api, telegram |
| `kill.set` / KV `kill` | Kill switch | mt-api/telegram/monitor → engine, deadman, hummingbot, airdrop-exec, treasury |
| KV `audit.integrity` | WORM integrity status from `audit.verify` (`ok` or the configured mismatch action). KV bucket names can't contain dots, so it's stored as bucket `audit`, key `integrity` | mt_obs → M11 (read pre-trade), UI |
| `worm.buffer.{table}` / KV `worm_buffer` | WORM writes buffered while Postgres is unreachable; KV holds the fill level (≥ 80% → new entries stop, [16 §3.3](16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check)) | writers → drainer on recovery; KV → M11 (read pre-trade), UI |
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
| `/markets/instruments` (+ `/{id}`: metadata, min resolution, licence flags), `/markets/{id}/bars?spec=&from=&to=` | Instruments, bars |
| `/markets/{id}/book`, `/markets/matrix` | Order book, cross-asset matrix |
| `/strategies`, `/strategies/{id}`, `/strategies/{id}/runs`, `/strategies/templates`, `/strategies/{id}/gate-report` | Strategies; gate report against the strategy's gate profile ([16 §2.4](16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile)) |
| `/lab/backtests`, `/lab/backtests/{id}`, `/lab/experiments`, `/lab/experiments/{id}`, `/lab/jobs` | Research lab |
| `/agents/runs`, `/agents/runs/{id}`, `/signals` | Agent runs, signals |
| `/models/registry`, `/models/questions`, `/models/tierb/decisions`, `/models/benchmarks`, `/models/gateway/spend`, `/models/labels`, `/models/labels/queue` | Models; labels and the labelling queue |
| `/memory/search`, `/memory/banks`, `/rag/search` | Memory and document search |
| `/risk/policy`, `/risk/state`, `/risk/events`, `/risk/changes`, `/risk/stress` | Risk. `/risk/policy` returns the effective value of each setting and the layer (L0–L4) that set it ([16 §1](16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance)); `/risk/changes?source=` filters by source |
| `/risk/capital-steps`, `/risk/kill-criteria` | Capital-step plan and state per sleeve/bot, kill-criteria state (Phase 7, [16 §2.5–2.6](16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot)) |
| `/data/feeds`, `/data/quotas`, `/data/dq-events`, `/data/costs`, `/data/recon` | Data quality, costs, reconciliation |
| `/intel/documents` (+ `/{id}`), `/intel/events`, `/intel/calendar`, `/intel/sentiment`, `/intel/postures` | Intel; `/intel/postures` = Telegram postures, numbers only, never text (F3b) |
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

**Filters the dashboards use** (query parameters on the routes above, not separate routes):
- Portfolio and execution: `/positions?instrument=&strategy=`, `/orders?instrument=&strategy=&source=`, `/signals?strategy=&limit=`, `/bots?active=1`, `/approvals?status=&source=`.
- Markets: `/markets/instruments?watchlist=`, `/markets/matrix?group=correlation|macro|positioning`, `/models/tierb/decisions?subject=`.
- Strategies and lab: `/strategies/{id}?gates=1&versions=1`, `/strategies/{id}/runs?metrics=1`, `/agents/runs?settled=1&metrics=1`, `/lab/jobs?kind=backfill`.
- Risk: `/risk/state?breakdown=1|ladder=1`, `/risk/changes?status=pending&source=`.
- Data: `/data/feeds?kind=text|storage=1`, `/data/costs?tca=1|snapshot=|compare=1|instrument=`, `/data/recon?scope=journal`.
- Intel: `/intel/documents?ticker=|sources=1`, `/intel/events?instrument=`, `/intel/calendar?instrument=`, `/rag/search?similar=`.
- Other: `/airdrops/{id}?risk=1|eligibility=1|history=1`, `/tasks?urgent=1|type=|opportunity=|status=`, `/journal/trades?analytics=1`, `/tax/summary?fy=&section=cgt|income|payg`, `/notifications?kind=|severity=`, `/wallets?kind=|group=`, `/system/health?slo=1`, `/system/services?kind=venue|hummingbot|mcp`, `/system/settings?section=`, `/system/logs?strategy=`, `/audit/log?source=`.

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

**Command catalogue (v1)** with each command's confirmation level. Where a command can tighten or loosen, the direction of the change decides the level (tighten C1, loosen C3, [16 §1](16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance)); the server computes it in the preview call.

| Group | Commands |
|---|---|
| Orders | `order.place` (C2), `order.modify` (C2), `order.cancel` (C1), `order.cancel_all` (C2; scope all / venue / strategy / instrument), `position.close` (C2; `{halt: true, reason}` = flatten-and-halt the bot), `position.reduce` (C2), `position.set_brackets` (C2) |
| Approvals | `approval.approve` (C2; large orders add hold-to-confirm / TOTP, [16 §2.3](16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)), `approval.approve_partial` (C2), `approval.reject` (C1) ([15 §1.5](15-bots-hitl-and-worm-audit.md#15-api-data-and-ui)); `web` and `telegram` sources only, never callable from MCP (§7.4) |
| Strategies | `strategy.create` (C1), `strategy.update_params` (C1 paper; C2 live; C3 if it increases risk), `strategy.clone` (C1), `strategy.archive` (C1), `strategy.start` (C1), `strategy.pause` / `strategy.resume` / `strategy.stop` (C1), `strategy.promote` (C1; autonomous stage C3), `strategy.demote` (C1), `strategy.run_shadow` (C1), `strategy.set_mode` (the highest mode its bots may use: allow `hitl` C2, allow `autonomous` C3, restrict C1). A strategy is **promoted through gates**; each bot's mode is set per bot, and the stricter of the two applies |
| Bots ([15 §1](15-bots-hitl-and-worm-audit.md#1-trading-bots)) | `bot.create` (C1), `bot.update_scope` / `bot.update_params` (incl. `on_system_failure`; tighten C1, loosen C3, incl. widening an autonomous bot's scope), `bot.set_mode` (`paper` C1, `paper` → `hitl` C2, `autonomous` → `hitl` C1, → `autonomous` **C3**), `bot.start` / `bot.pause` / `bot.resume` / `bot.stop` (C1), `bot.approval_policy.set` (tighten C1, loosen C3) |
| Lab | `lab.backtest.run` (C1), `lab.sweep.run` (C1), `lab.validate.run` (C1; incl. distillation runs), `lab.generate_strategy` (C1; uses LLM budget), `lab.job.cancel` (C1), `lab.leakage.waive` (C2, reason required, audited), `lab.gate_report.generate` (C1) |
| Agents & models | `agents.run_analysis` (C1; uses LLM budget), `models.tierb.ask` (C0), `models.tiera.train` (C1: train → calibrate → compile), `models.label.add` (C0), `models.promote` (C2; to production for a model used by autonomous bots C3), `models.rollback` (C1), `models.bakeoff.run` (C1), `models.question.update` (C1, new version; loosening a threshold below its default bar C3), `memory.delete` (C1), `anomaly.explain` (C1; result arrives as a notification) |
| Market making | `mm.bot.create` (C1, paper), `mm.bot.start` (C1 paper, **C3 live**: a live market-making bot quotes on its own, like `autonomous` mode), `mm.bot.stop` (C1), `mm.bot.update` (C1 paper, C2 live, C3 if it increases risk), `mm.bot.cancel_all` (C1) |
| Risk | `risk.policy.update` (diff on any layer L0–L4, including the hard-ceilings section of the bot strategy settings and confirming the wallet floats, signer caps and gas budgets that enable signing ([16 §2.7](16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)); tighten C1 and immediate, loosen C3; cancelling a pending change C1), `risk.kill.on` (Kill), `risk.kill.off` (C3), `risk.deadman.ack` (C1), `risk.stress.run` (C1), `risk.sleeve.restart` (C3; after a sleeve drawdown or health halt), `risk.capital.fund` (C3), `risk.capital_step.approve` (C3), `risk.review.close` (C3) |
| Data | `data.feed.pause` / `data.feed.resume` (C1), `data.backfill.run` (C1), `data.recon.run` (C1), `data.incident.ack` (C0; appends an `audit.dq_ack` row, never updates the incident) |
| Intel | `intel.source.add` (C1; paid/ToS-banned sources rejected), `intel.source.mute` (C0), `intel.watchlist.update` (C0) |
| Airdrops | `airdrop.add_url` (C0), `airdrop.rescore` (C0), `airdrop.reject` (C1), `airdrop.mandate.create` (C3), `airdrop.mandate.revoke` (C1), `airdrop.claim.execute` (C2 unless covered by a mandate), `wallet.revoke_approval` (C2), `wallet.sweep` (C2; to the allow-listed vault address) |
| Tasks | `task.done` / `task.skip` / `task.snooze` (C0), `task.never` (C1), `task.answer` (C1; e.g. a tax-agent answer), `social.draft.approve` (C1, opens a web intent), `social.draft.reject` (C1) |
| Wallets & treasury | `wallet.register` (C1), `wallet.tag` (C1), `treasury.allocate` (C2; loosening policy C3), `treasury.earn.enter` / `treasury.earn.exit` (C2) |
| Venues & ladder | `venue.registry.update` (tighten C1, allow a venue/product C3), `risk.ladder.set` (down C1, up C3) |
| Journal & tax | `journal.note.add` (C0; optional attachment, stored content-addressed under `data/attachments/` and referenced by hash), `journal.tag` (C0), `journal.manual_event.add` (C2, reason required), `journal.review.signoff` (C1), `tax.report.generate` (C1), `tax.export` (C0), `tax.residency.add` (C1; emits `tax.residency.changed`; any loosening it causes in the venue registry is C3), `tax.regime.set` (C1), `tax.lot.select` (C1), `tax.fy.lock` / `tax.fy.unlock` (C3; unlock needs a reason) |
| System | `system.backup.run` (C1), `system.restore.test` (C1), `system.key.rotate_reminder` (C0), `system.settings.update` (C0 for preferences, layout and digests; C1 to tighten or for schedules; C3 to loosen, e.g. raise an LLM budget or a DQ threshold), `system.service.restart` (C2; allow-listed containers only, via `docker-proxy`), `audit.verify` (C1), `audit.integrity.ack` (C3; clears a WORM verify mismatch after investigation, [16 §2.11](16-configuration-and-safety-model.md#211-worm-integrity)), `ops.drill.record` (C1) |
| MCP (Phase 8) | `mcp.token.create` (C1; C3 for indefinite expiry or the `trade`, `strategy`, `risk_tighten` scopes), `mcp.token.revoke` (C1, immediate), `mcp.tool.set` (disable C1; enable a read/analyse/curation tool C1, a trade/strategy/risk tool C3), `mcp.policy.set` (tighten C1, loosen C3). All web/Telegram only |

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
  - **Never exposed:** withdrawals, `wallet.sweep`, `treasury.*` moves, `airdrop.claim.execute`, mandates, key and token management, `approval.*`, `mcp.*`, restore/delete (incl. `system.restore.test`, `memory.delete`), `system.service.restart`, `risk.deadman.ack`, `/system/keys`, `/system/logs`, audit writes ([03 M20](03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted)). Loosening risk is never a scope.
  - **Tokens:** opaque 256-bit, shown once, stored hashed (HMAC-SHA-256 with a server pepper), scoped (`read`, `analyse`, `trade`, `strategy`, `risk_tighten`, `curation`), revocable instantly, last use and client identity recorded. Expiry is chosen per token (1 day · 7 days · 30 days · 1 year · custom · indefinite; indefinite shows a warning, needs C3 and a monthly reminder). OAuth 2.1 (PKCE, resource indicators) for clients that support MCP authorization.
  - **Transport:** Streamable HTTP (JSON-RPC 2.0, SSE streaming, resumable) at `/mcp` on Caddy, Tailscale/TLS only; stdio locally; an optional legacy HTTP+SSE endpoint for older clients. Server notifications (fills, approvals, alerts) via resource subscriptions.
  - **Responses** pass the same provenance filter as any model input: no Telegram text, no `model_input_ok = false` rows, tax PII redacted, untrusted text wrapped and marked.
  - **Audit:** every MCP call, reads included, is a WORM row in `audit.mcp_call`; commands are also in `audit.command`. Default limits: 60 reads/min and 10 writes/min per token, 256 KB per result.

## 8. End-to-end flows

**F1: Market data → bars → quality**
1. Venue WebSocket → Nautilus data client (ingest-market).
2. Publish `md.*`.
3. Parquet recorder (1–5 min files, daily compaction).
4. Bar builder writes 1s bars into Timescale; continuous aggregates build 1m, 5m, 15m, 1h, 4h, 1D and 1W; other sizes are `time_bucket` queries at read time.
5. The monitor checks staleness, gaps, outliers, cross-source divergence and clock skew → `dq.status.*`.
   - **Data age** = now − the time *we received* the last update for that stream; thresholds per bot (default 2 s fast, 60 s slow), session-aware (closed sessions are `closed`, not stale) ([16 §2.2](16-configuration-and-safety-model.md#22-data-freshness-what-stale-means)).
   - The monitor flips `dq.status` to `stale` within ≤ 250 ms (p99) of the threshold being crossed.
6. The risk manager blocks orders on `stale`/`bad`, and also **checks data age inline on every order**, so no order acts on stale data whatever the monitor's timing.
7. The UI shows feed health.

**F2: Signal → decision → risk → order → fill → journal → TCA**
1. A strategy (M0) receives `md`/`feat`/`tierb` inputs.
2. Decision One tier A (µs) produces a calibrated edge.
3. Deterministic sizing → `OrderIntent`.
4. **M11 pre-trade checks:** effective limits (strictest layer), collar, liquidity/spread, DQ status and inline data age, blackout, decision deadline, WORM integrity status (KV `audit.integrity`), egress status (`egress.status`, checked from Phase 1, P1-T071; the fixed exit-node IP arrives in P7), duplicate check. The client order ID is `{bot}-{engine_epoch}-{seq}`; a signal hash is stored separately for idempotency.
5. Mode routing (per bot):
   - `autonomous`: submit;
   - `hitl`: `risk.approval.request` → Telegram/web approval card → approve within the TTL (default 60 s intraday · 15 min swing · 4 h position, [16 §2.3](16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)) or expire = reject;
   - `paper`: simulated fill.
   - Protective exits never wait for approval in any mode.
6. Venue fill → `fill.*`.
7. **Journal (M18)** records the fill + fees; the lot engine updates.
8. **Monitor (M16)** computes implementation shortfall vs the decision/arrival price and updates the realised-vs-modelled cost ratio.
9. **Grafana and the UI** update; the audit row is chained.

**F3: Text → decision models → features** (every source except Telegram)
1. A feed (RSS / Discord / Bluesky / Mastodon / GDELT) arrives. A provenance gate drops any row with `model_input_ok = false`; Telegram never enters this flow (F3b).
2. ingest-text normalises it and dedupes.
3. The nlp service runs:
   - the relevance gate (tier B / SemIf; queued, never on the order path);
   - entity/ticker linking;
   - FinBERT sentiment;
   - TEI embeddings.
4. The result goes to `text.document` + `rag.doc_chunk`.
5. `text.doc.new` triggers decision-svc questions (direction, event type, veto…).
6. `dec.tierb.*` updates KV `tierb_scores`, which tier A reads as features.
7. High-severity veto → `risk.event` (above the calibrated threshold only).

**F3b: Telegram → postures (code and policy only)**
1. Telegram messages arrive (Telethon / Bot API) in ingest-text.
2. A deterministic regex extractor pulls contract addresses, tickers and counts and turns them into postures (mention velocity, channel count, new-channel share, time since first call).
3. ingest-text publishes postures and mentions on `posture.telegram.{subject}`; it has no DB route. The core-side `intel-writer` stores them in `text.telegram_mention` (structured fields only) and `text.telegram_posture` (both `model_input_ok = false`, `train_ok = false`).
4. Only code/policy rules consume them (M4 airdrop rules, M11 rules); D08 displays them as postures. Never nlp, RAG, M6 features, tier A/B, agents or MCP ([12 §4–5](12-policy-and-compliance.md#4-per-platform-data--automation-rules)).

**F4: Research debate → signal → teacher log → distillation**
1. A scheduled or event-triggered `agents.run_analysis` (M8, via the LiteLLM gateway) runs with RAG + memory recall.
2. It produces a structured `Signal` with provenance.
3. The signal is stored in `audit.decision_run`, and Hindsight retains the episode.
4. After the horizon, **settlement** computes the outcome and the agent writes a reflection.
5. A nightly Prefect flow distils teacher + outcomes into tier A / tier B candidates.
6. Candidates are calibrated and benchmarked, then promoted only through the gates (models registry).

**F5: Risk policy change**
1. The UI/Telegram/MCP sends `risk.policy.update` with a diff for one layer (L0 hard ceilings … L4 bot, [16 §1](16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance)). MCP can only tighten.
2. The server validates the diff (inconsistent settings are rejected with the reason) and classifies each field:
   - **tighten** → applied immediately, audited, notified;
   - **loosen** → C3: Telegram approve + TOTP → cool-down → applied.
3. A value looser than a parent layer is rejected; the effective value is always the strictest across layers.
4. **L0 hard ceilings** are edited in the ceilings section of the agent/bot strategy settings, which applies to every bot. Same rule: tightening is immediate, loosening is C3.
5. Every change is a new WORM version row (`risk.change`); rollback re-applies an earlier version as a new row.

**F6: Kill switch & dead-man**
1. **Triggers:**
   - `risk.kill.on` from any client;
   - automatic: system drawdown stage 2 or an unexplained reconciliation mismatch. Smaller breaches act narrowly ([03 M11](03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp), [16 §2.1](16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)): daily loss halts the sleeve, sleeve drawdowns halve sizes then halt the sleeve, API errors pause the venue, a cost blow-out pauses the bot;
   - a missing heartbeat (the dead-man layers in §6 act on their own as well).
2. KV `kill = ON`, then:
   - new trading stops and the engine cancels all orders;
   - each bot's `on_system_failure` policy is applied (default `flatten`);
   - Hummingbot stops;
   - new treasury/earn moves and airdrop-exec claims freeze;
   - from P5 (default on), hot trading balances sweep to the vault address; protective sweeps and revokes are exempt from the freeze. P2 has no sweep yet;
   - the UI shows a global red banner.
3. **Turning it off** is C3, and requires the trigger condition to be cleared.
4. **Restart after an unplanned stop:** the engine starts with every bot paused, reconciles each venue, flattens or cancels any residue, and resumes only when you tap resume (C1) or a bot has `auto_resume_after_crash: true` ([16 §3.1](16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)).

**F7: Strategy lifecycle**
1. `draft` (create/template/generate in the sandbox).
2. `backtested`.
3. `validated` (gate profile, [16 §2.4](16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile): walk-forward, MC permutation, DSR ≥ 0.95, look-ahead check, cost stress…).
4. **Bots** run the validated version in a mode, set per bot: `paper` → `hitl` (C2) → `autonomous` (C3, only after the paper/HITL period: default ≥ 8 weeks and ≥ 50 trades).
5. Each promotion checks the gates and is audited. Decay signals downgrade an autonomous bot to `hitl` automatically ([16 §2.6](16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each)).

**F8: Airdrop**
1. Discover → normalise/dedupe → enrich → risk-score (GoPlus / RugCheck / Honeypot.is / heuristics / blocklists) → viability score.
2. Decide:
   - **reject**, with reasons;
   - **user task** (steps, verified links);
   - **auto-claim**, only if an active mandate covers it. Auto-claims use the chain's **airdrop identity wallet** (never the hot trading wallet) and go through the policy service → cost gate → simulation → signer → the journal (income classification).

**F9: Tax**
1. Fills, ledgers, funding, airdrops and staking events become journal events.
2. Valuation follows [16 §4.1](16-configuration-and-safety-model.md#41-valuing-crypto-for-the-journal) (fill price → VWAP of our recorded trades → on-chain pool price; aggregators cross-check only). FX conversion uses the RBA rate (AUD; missing days use the last business day, non-F11 currencies go via USD).
3. The lot engine applies specific-ID with FIFO fallback.
4. The jurisdiction plugin by residency period runs: AU_2026, then AU_2027_REFORM.
5. Outputs:
   - **quarterly:** PAYG instalment estimate;
   - **at EOFY:** myTax worksheet + CGT schedule + accountant pack + Beancount export.
6. **Snapshot jobs:** 30 Jun 2027, and on any residency change (CGT event I1), priced per asset class ([16 §4.2](16-configuration-and-safety-model.md#42-market-value-snapshot-30-june-2027-and-any-residency-change)).
7. **Residency change:** `tax.residency.add` emits `tax.residency.changed`; the venue registry recomputes, and any loosening that results is C3. The registry carries the `residency_version` it last applied; until it catches up, M11 fails closed (rejects new entries on residency-dependent products; exits still pass).

**F10: Curation loop**
1. Sources (airdrops, Discord/Telegram discovery, risk approvals, tax questions) create user tasks in `curation.task`.
2. Delivery: instant alerts or daily/weekly digests (Telegram + UI).
3. You tap Done / Skip / Snooze / Never.
4. Feedback updates the ranking.
5. For Discord follow tasks, the bot verifies that posts arrive.

**F11: Backup & incident**
- **Backups:** continuous WAL archive → nightly incremental → weekly full → monthly restore test → monthly immutable WORM export → alert on any failure.
- **Incident runbooks** in `docs/runbooks/`: keys leaked, server down with open positions, bad data, wallet drained.

## 9. Cross-cutting

### 9.1 Security

See [07-security-notes.md](07-security-notes.md):
- **Network segmentation** (§3.1).
- **Exchange/broker keys:** trade-only scope, withdrawals disabled, allow-listed only to the fixed egress IP (§3.1), separate sub-accounts for paper and live bots.
- **Secrets and roles:** secrets via sops; least-privilege DB roles.
- **Untrusted input:** LLMs never see secrets; scraped text is marked untrusted.
- **Server-side confirmation levels** (§7.2); loosening anything, including L0 hard ceilings, is C3.
- **WORM records** with external seals ([15 §2](15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).

### 9.2 Observability & SLOs

| SLO | Target | Measured by |
|---|---|---|
| Decision One tier A latency | p99 < 50 µs per prediction | In-process histogram |
| Pre-trade risk check | p99 < 1 ms | Engine metrics |
| Strategy signal → order submitted (`autonomous`) | p99 < 5 ms (excl. venue) | Trace spans |
| Tier B decision | p95 < 50 ms (GPU, 0.6B head; ~2–12 ms typical, CPU 100–400 ms) | decision-svc metrics |
| Stage-1 relevance gate (nlp) | p95 ≤ 300 ms GPU, ≤ 3 s CPU; queued, never on the order path | nlp metrics |
| Data age over the per-bot threshold (default 2 s fast, 60 s slow, configurable) → `dq.status` stale | ≤ 250 ms p99 after the threshold is crossed (M11 also checks age inline on every order; [16 §2.2](16-configuration-and-safety-model.md#22-data-freshness-what-stale-means)). Replaces "detection → paused < 2 s" | Monitor |
| WORM insert (`audit.*`, `journal.*`) | p99 < 5 ms; the order path never waits on seals | DB metrics |
| Command bus (`mt_api`, excl. handler) | p99 < 50 ms | mt-api metrics |
| UI live update lag (server → screen) | p95 < 500 ms | Client telemetry (local only) |
| Kill switch → all cancels sent | < 1 s | Engine metrics |
| Dead-man reaction | Cancel at 5 s, `on_system_failure` at 10 s of missing heartbeat (defaults, [16 §3.1](16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)) | Engine + deadman metrics |
| Backup restore test | Monthly pass | Prefect flow |

Targets are defaults. Operating values (stale thresholds, reconciliation intervals, collars, error pauses, dead-man timers) live in [16 §2–3](16-configuration-and-safety-model.md#2-default-values-all-configurable) and are changed in settings.

### 9.3 Degraded modes

| Failure | System behaviour | UI behaviour |
|---|---|---|
| A feed is stale/bad | Strategies using it pause; no new orders on that instrument (closed sessions are `closed`, not stale) | Amber/red feed chip; banner on affected screens |
| Venue disconnect | Reconnect with backoff; affected orders flagged unknown → reconcile | Venue chip red; positions marked "unconfirmed" |
| Postgres down | The engine doesn't keep opening positions: the in-engine watchdog treats the missing DB heartbeat like any critical component ([16 §3.1](16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)): 5 s → cancel open orders, 10 s → each bot's `on_system_failure`. Records of those exits buffer in NATS JetStream (default bound 1 GB or 24 h; above 80% new entries stop, exits continue); nothing executes without a record | Red system banner, read-only UI |
| WORM verify mismatch | Default `block_new_entries`: no new entries, exits and protective orders continue, no loosening until `audit.integrity.ack` (C3); options `alert_only` / `halt_all` ([16 §2.11](16-configuration-and-safety-model.md#211-worm-integrity)) | Critical banner; alert on every channel |
| Engine down | `deadman` sidecar cancels at 5 s and flattens per `on_system_failure` at 10 s; restart is flat with bots paused | Red system banner; Telegram alert |
| Host or internet down / egress tunnel down | Nothing on our side can reach venues; venue cancel-after timers cancel open orders and resting venue stops protect positions (fail flat) | Telegram/ntfy alert (if reachable) |
| Egress IP or country mismatch | New orders blocked; alert | Red egress chip |
| LLM gateway/budget exhausted | Falls back to local models; agents degrade | "Local models" badge |
| GPU unavailable | Tier B on CPU (slower) or disabled; tier A unaffected | Tier B status degraded |
| mt-api down | Engine unaffected; Telegram `/kill` still works via the bot → NATS (credentials limited to `kill.set`; the engine writes the kill to WORM with source `telegram`) | Web unreachable; Telegram alert |

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

The canonical repository layout is [03 §3](03-build-spec.md#3-repository-layout); this doc doesn't repeat it.

## 12. End-to-end build plan

Each phase ends with a usable demo; details are in [04-plan-of-action.md](04-plan-of-action.md).

| Phase | Backend deliverables | Frontend deliverables (see [ui/](ui/README.md)) | Exit criteria |
|---|---|---|---|
| 0 Foundations | Host hardening, compose, Postgres/NATS/Prefect/obs/MLflow/LiteLLM (+ `audit.llm_call`)/`tei-embed`/`tei-rerank`/`llm-local`, all schemas + `pit`, WORM layer + integrity response, `mt_api` skeleton (auth + TOTP, commands with preview tokens, WS), break-glass C3 CLI, backups | Web shell (top bar, nav, status bar, kill-switch placeholder), design preset, component library v0, **System** dashboard (health), Playwright matrix in CI | Stack healthy; login + TOTP; responsive shell passes matrix |
| 1 Data & monitoring | ingest-market, Parquet recorder, bar builder, batch macro/fundamentals, quota tracker, **monitor** (DQ, costs, recon) | **Data & Quality**, **Markets** (charts, matrix, instrument detail), notifications | Live bars tick→1D for all asset classes; DQ alerts on Telegram |
| 2 Strategies, risk, lab | Strategy framework + templates, bots, **risk manager** (layered config), three-layer dead-man (`deadman` sidecar), engine paper/testnet, custom adapters (Alpaca/OANDA/IG), lab (backtest/validate/optimise/MLflow), tier A runtime, sandbox generator, Telegram bot v1 | **Cockpit**, **Strategies**, **Research Lab**, **Execution**, **Risk** | Any strategy type created → backtested with measured costs → paper behind risk; kill switch drill passes |
| 3 Journal & tax | Journal ingestion, FX service, lot engine, AU_2026 (+ 2027 scaffold), residency, exports | **Journal**, **Tax & Reports** | Every paper fill auto-journalled; FY-to-date AU summary + PAYG estimate |
| 4 Intel | ingest-text/events, RSS-Bridge, nlp pipeline, RAG, calendars, SemIf tier B | **Intel** (news/social/events/calendar), tier B outputs on Markets/Cockpit | Morning brief; calendar blackouts enforce in risk |
| 5 Airdrops & curation | airdrop pipeline, risk feeds, mandates + signer + Anvil simulation, task queue + digests, custody tiers, wallet-indexer (unified wallet view) | **Airdrops & Launches**, **Tasks & Curation**, **Wallets & Treasury** (view) | Weekly vetted digest; simulated auto-claim on testnet |
| 6 AI & models | Agents (debate), Hindsight, decision-svc (own head), distillation, anomaly, optional Hummingbot, M22 hold-and-earn, optional M23 social drafts | **Agents & Decisions**, **Models & Memory**, **Market Making** | Sourced signals; bake-off report; anomaly explanations |
| 7 Prove → small live | Live sub-accounts, fixed-IP egress exit node, reconciliation hardening, capital steps and kill criteria, gate reports, weekly reviews | Approvals polish, mobile polish; capital-step, kill-criteria and gate-report views (D03/D06/D14/D16) | Gates passed per bot's strategy ([16 §2.4](16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile): paper/HITL default ≥ 8 weeks and ≥ 50 trades); micro-live stable. The 12-month review is a recurring calendar task, not a phase item |
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

**Promotion gates (per-strategy gate profile; defaults, configurable in [16 §2.4](16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile); loosening a gate is C3):**
1. **Performance:** walk-forward out-of-sample results beat the asset-class passive benchmark after **measured** costs; default ≥ 60% of folds positive and worst fold ≥ −(sleeve halt drawdown).
2. **Robustness statistics:** Monte Carlo permutation p < 0.05; **deflated Sharpe ratio (DSR) ≥ 0.95** (DSR is a probability, so 0.95 = 95% confidence the true Sharpe is above zero); still profitable at 2× measured costs; positive in each year and regime.
3. **Bias checks:** look-ahead and recursive analysers clean, leakage review clean (or each finding waived by you, C2).
4. **LLM components:** tested only on data after the model's training cutoff.
5. **Paper/HITL period** before autonomous or a capital step: default ≥ 8 weeks **and** ≥ 50 trades (P1 sleeves ≥ 8 weeks; memecoin ≥ 300 trades; low-frequency bots ≥ 26 weeks), with P&L and costs tracking the backtest.
6. **Safety drills:** kill switch, dead-man's switch (all three layers), restart and DQ pause exercised on the bot's venue.
