# MasterTrader — Architecture (v3, end-to-end)

This is the blueprint that backend and frontend work build against.
- Module behaviour: [03-build-spec.md](03-build-spec.md) (M0–M23).
- Order of work: [04-plan-of-action.md](04-plan-of-action.md).
- UI scope: [ui/README.md](ui/README.md).
- Visual system: [../DESIGN.md](../DESIGN.md).

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
6. **Record everything.** Append-only, hash-chained audit and journal; logs only for operations.
7. **One command layer (`mt_api`).** The web UI, Telegram and (Phase 8) MCP are thin clients of the same typed, audited commands.
8. **Free only, personal use, private, no telemetry.** Generated code is sandboxed; GPL/AGPL code is isolated; secrets never reach LLMs.

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
- **Outbound traffic** to venues and wallets goes only through the execution service (M12) and the signer, each behind M11 / mandates.

## 3. Deployment topology

Docker Compose on one host. Images are pinned by digest. Everything is reachable only on localhost or Tailscale.

### 3.1 Networks

| Network | Members | Internet egress | Purpose |
|---|---|---|---|
| `edge` | caddy, mt-api | — | TLS termination on the Tailscale interface; serves the web app |
| `core` | mt-api, all app services, nats, postgres, mlflow, tei, litellm, vllm, hindsight | Venues and LLM APIs via allow-list | Business logic |
| `scrape` | ingest-text, rss-bridge, crawl4ai | Yes (wide) | Untrusted fetching; **no route to postgres or signer** (publishes to NATS via a narrow NATS account) |
| `signer` | signer | Chain RPC only | Hot-wallet signing; reachable only from airdrop-exec |
| `obs` | grafana, loki, prometheus, vector, alertmanager | Telegram API (alerts) | Observability |

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
| `litellm` | LiteLLM ≥ 1.83 | Model gateway (research/chat/debate) | 0 |
| `tei` | text-embeddings-inference (CPU or GPU) | Embeddings + rerank | 0 |
| `ingest-market` | `mt_data.market` | Venue WS clients (via Nautilus data clients), Parquet recorder, bar builder | 1 |
| `ingest-batch` | `mt_data` (Prefect flows) | Macro, fundamentals, calendars, backfills | 1 |
| `monitor` | `mt_monitor` | Data-quality + cost/TCA + reconciliation (M16) | 1 |
| `engine` | `mt_engine` (NautilusTrader TradingNode) + `mt_strategy` + `mt_risk` + Decision One tier A | Live/paper trading node; strategies; risk; execution | 2 |
| `backtest-worker` | `mt_lab` | Backtests, validation, optimisation, distillation, sandbox orchestration | 2 |
| `sandbox` | gVisor/`--network none` runner | LLM-generated strategy code | 2 |
| `journal` | `mt_journal` | Journal ingestion, lot engine, tax rules, reports | 3 |
| `ingest-text` | `mt_data.text` | RSS, Telegram (Telethon + Bot), Discord bot, Bluesky, Mastodon, GDELT | 4 |
| `rss-bridge` | rss-bridge | Feeds for sites without RSS | 4 |
| `nlp` | `mt_features.text` | Relevance gate, entity linking, FinBERT, embeddings → `text.document` | 4 |
| `ingest-events` | `mt_data.events` | USGS/GDACS/NOAA/FIRMS/ReliefWeb/UCDP/Kalshi/Polymarket | 4 |
| `airdrop` | `mt_airdrop` | Discovery, enrichment, risk/viability scoring | 5 |
| `airdrop-exec` + `signer` | `mt_airdrop.exec` | Mandated claims, simulation, revokes | 5 |
| `curation` | `mt_curation` | Task queue, digests | 5 |
| `wallet-indexer` | `mt_treasury.indexer` | Unified wallet view: balances, transfers (internal tagging), approvals, nonce-authority and depeg monitors | 5 |
| `treasury` | `mt_treasury` | M22 hold-and-earn + treasury allocation, on-chain cost gate | 6 |
| `signer` (extended) | `mt_signer` | Intents-only signer for hot/burner/identity keys (13 §2); also serves DEX execution | 5 |
| `anvil` | foundry anvil | Local mainnet-fork simulation before signatures | 5 |
| `social` | `mt_social` | M23 social drafts (approval → web intent from your account) | 6 (optional) |
| `ntfy` | ntfy | Second, independent alert channel (push) | 1 |
| `telegram-bot` | `mt_ui.telegram` | Alerts, digests, approvals, task buttons, `/kill` | 2 (alerts from 1) |
| `agents` | `mt_agents` | LangGraph debate runs (M8) | 6 |
| `hindsight` | Hindsight (slim) | Agent memory (schema `hindsight`) | 6 |
| `decision-svc` | `mt_models` + vLLM (`/classify`) or ONNX | Decision One tier B (SemIf readout → own Qwen-LoRA head) | 4 (SemIf) / 6 |
| `anomaly` | `mt_anomaly` | Detectors + explain agent | 6 |
| `hummingbot` | hummingbot (telemetry off) | Market-making sidecar | 6 (optional) |
| `mcp` | `mt_mcp` | MCP adapter over `mt_api` | 8 (optional) |

**Hardware:** 8–16 cores, 32–64 GB RAM, 2–4 TB NVMe + HDD for cold Parquet. A 16–24 GB GPU is recommended for tier B, vLLM, Hindsight and LightRAG.

## 4. Logical components

| Module | Package | Runs in | Owns (Postgres schema/tables) | Publishes | Consumes |
|---|---|---|---|---|---|
| M0 Strategy framework | `mt_strategy` | engine, backtest-worker | `strategy.registry`, `strategy.versions`, `strategy.runs` | `sig.*`, `strat.status.*` | `md.*`, `feat.*`, `dec.tierb.*` |
| M1 Market data | `mt_data.market` | ingest-market, ingest-batch | `market.instrument`, `market.bar_*`, `market.macro_series`, `market.filing` | `md.*`, `dq.raw.*` | venue WS/REST |
| M2 News & social | `mt_data.text` | ingest-text, nlp | `text.document`, `text.source` | `text.doc.*` | feeds |
| M3 Events | `mt_data.events` | ingest-events | `text.geo_event`, `text.exposure_map` | `evt.*` | feeds |
| M4 Airdrops | `mt_airdrop` | airdrop, airdrop-exec | `curation.airdrop_*`, `curation.mandate`, `curation.exec_log` | `airdrop.*`, `task.new` | risk APIs, chain RPC |
| M5 Calendars | `mt_data.calendar` | ingest-batch | `text.calendar_event` | `cal.*` | FRED, ForexFactory, CB |
| M6 Features | `mt_features` | engine (incremental), batch | `features.value`, `features.def` | `feat.*` | `md.*`, `text.*`, `evt.*` |
| M7 Lab | `mt_lab` | backtest-worker, sandbox | `strategy.backtest`, `strategy.experiment` (+ MLflow) | `lab.job.*` | catalog, features |
| M8 Agents | `mt_agents` | agents | `audit.decision_run`, `audit.signal` | `sig.agent.*` | RAG, memory, gateway |
| M9 Memory & RAG | `mt_memory` | agents, nlp, hindsight | `rag.doc_chunk`, `hindsight.*` | — | TEI |
| M10 Anomaly | `mt_anomaly` | anomaly | `audit.anomaly` | `alert.anomaly.*` | `md.*`, `text.*`, `evt.*` |
| M11 Risk | `mt_risk` | engine (in-process) + mt-api (policy) | `risk.policy`, `risk.limit_state`, `risk.change`, `risk.event` | `risk.*`, KV `risk_state`, `kill` | `ord.intent.*`, `dq.status.*`, `cost.*` |
| M12 Execution | `mt_engine` | engine | `audit.order`, `audit.fill`, `audit.position_snapshot` | `ord.*`, `fill.*`, `pos.*` | venues |
| M13 MM sidecar | hummingbot + adapter | hummingbot | `audit.mm_*` | `mm.*` | Hummingbot API |
| M14 Crowd-sim | services/crowdsim | optional | `research.crowdsim_run` | — | — |
| M15 UI | `mt_ui` (web + telegram) | caddy, telegram-bot | `ops.user_pref`, `ops.notification` | — | WS topics |
| M16 Monitor | `mt_monitor` | monitor | `audit.dq_event`, `audit.cost_event`, `market.spread_*`, `audit.recon` | `dq.status.*`, `cost.*`, `recon.*` | `md.*`, fills, venues |
| M17 Observability & audit | `mt_obs` | all | `audit.*` hash chain, `audit.llm_call`, `audit.command` | metrics, logs | — |
| M18 Journal & tax | `mt_journal` | journal | `journal.*` | `journal.*` | fills, ledgers, chain, airdrops |
| M19 Curation | `mt_curation` | curation, telegram-bot | `curation.task`, `curation.community` | `task.*` | `airdrop.*`, `risk.approval.*` |
| M20 MCP | `mt_mcp` | mcp | — (via `audit.command`) | — | `mt_api` |
| M22 Treasury & hold-and-earn | `mt_treasury` | treasury, wallet-indexer | `treasury.wallet`, `treasury.transfer`, `treasury.position`, `treasury.policy` | `wallet.*`, `treasury.*` | chain RPC, venues, `risk.*` |
| M23 Social participation | `mt_social` | social | `curation.social_draft` | `social.draft.*` | `text.doc.*`, `task.*` |
| M21 Models | `mt_models` | engine (tier A), decision-svc, litellm, tei | `models.registry`, `models.question`, `audit.tierb_decision` | `dec.tierb.*`, KV `tierb_scores` | `text.doc.*`, M8 teacher log |

## 5. Data architecture

### 5.1 Stores

| Store | Holds | Retention | Backup |
|---|---|---|---|
| **Postgres** (`market`, `text`, `features`, `strategy`, `risk`, `audit`, `journal`, `curation`, `models`, `rag`, `hindsight`, `ops`) | System of record: bars (hypertables + continuous aggregates 1s→1D), business data, audit, journal, documents + embeddings | Audit/journal ≥ 7 years; bars forever (compressed); documents forever | pgBackRest (full weekly, WAL continuous) + restic off-site; monthly automated restore test |
| **Parquet catalog** (Nautilus `ParquetDataCatalog`) | Raw trades, quotes, L2 deltas/snapshots, backfills | Forever (hot NVMe 90 days → cold HDD) | restic (cold) |
| **NATS JetStream** | Streams (§6) + KV (`risk_state`, `kill`, `feed_status`, `tierb_scores`, `heartbeat`) | Streams 24h–7d; KV latest | Not backed up (rebuildable) |
| **MLflow** | Experiments, model artifacts (ONNX, LoRA), metrics | Forever | restic |
| **Loki / Prometheus** | Logs 30–90d / metrics 90d | Rolling | Not backed up |
| **Secrets** | sops+age file → tmpfs | — | Encrypted copy off-site |

### 5.2 Key conventions

- **Time:**
  - `timestamptz` UTC everywhere, nanosecond precision kept in Parquet;
  - `event_time`, `ingest_time` on every fact;
  - the UI renders in the user's timezone (default Australia/Sydney).
- **IDs:** UUIDv7 (time-ordered). Instruments use the Nautilus `InstrumentId` (`BTCUSDT.BINANCE`).
- **Money:** `numeric` / `Decimal`, never floats, for prices, sizes, fees and tax. Each instrument's precision comes from instrument metadata.
- **Point-in-time:** `mt_store.pit(as_of)` is the only read path for research/backtests (CI-enforced).
- **Append-only:** `audit.*` and `journal.*` are insert-only roles with a daily hash chain; corrections reference the row they supersede.

### 5.3 Core entities (abbreviated; full DDL in migrations)

`instrument`, `bar`, `feature_value`, `document`, `geo_event`, `calendar_event`, `strategy`, `strategy_version`, `strategy_run`, `backtest`, `experiment`, `signal`, `decision_run`, `tierb_decision`, `order`, `fill`, `position_snapshot`, `risk_policy`, `risk_limit_state`, `risk_change`, `risk_event`, `mandate`, `dq_event`, `cost_event`, `recon_result`, `journal_event`, `lot`, `lot_match`, `fx_rate`, `residency_period`, `tax_report`, `airdrop_opportunity`, `token_risk_report`, `user_task`, `community_item`, `notification`, `command`, `llm_call`, `model_registry`, `question`.

## 6. Messaging (NATS)

**Subject taxonomy** (all payloads are versioned msgspec/JSON schemas in `mt_core.schemas`):

| Subject | Payload | Producers → consumers |
|---|---|---|
| `md.{venue}.{symbol}.trade` / `.quote` / `.book` / `.bar.{spec}` | Market data | ingest-market → engine, monitor, features, UI (throttled) |
| `dq.status.{venue}.{symbol}` | `ok \| degraded \| stale \| bad` + reasons | monitor → engine (risk), UI |
| `cost.{venue}.{symbol}` | spread/fee/funding/swap snapshot | monitor → risk, lab, UI |
| `feat.{name}.{symbol}` | Feature values | features → engine |
| `text.doc.new` | Document id + tickers + scores | nlp → decision-svc, agents, UI |
| `evt.{kind}` / `cal.{kind}` | Global events / calendar items | ingest → risk (blackouts), agents, UI |
| `dec.tierb.{question}.{subject}` | Option probabilities | decision-svc → engine (KV), UI |
| `sig.{source}.{strategy}` | Signal | strategies/agents → engine |
| `ord.intent.{strategy}` → `ord.risk.{decision}` → `ord.{state}` | Order lifecycle | engine/mt-api → risk → venue |
| `fill.{venue}` / `pos.{account}` | Fills / positions | engine → journal, monitor, UI |
| `risk.event` / `risk.approval.request` / `risk.approval.result` | Risk events and approvals | risk ↔ mt-api, telegram |
| `kill.set` / KV `kill` | Kill switch | mt-api/telegram/monitor → engine, hummingbot, airdrop-exec |
| `sys.heartbeat.{service}` | Liveness | all → dead-man watchdog |
| `alert.{severity}.{kind}` | Alerts | all → telegram, UI |
| `task.new` / `task.updated` | User tasks | airdrop, curation, risk → telegram, UI |
| `journal.event.new` | Journal | journal → UI |
| `wallet.{chain}.{address}.balance` / `.transfer` / `.approval` / `.nonce_authority` | Wallet events | wallet-indexer → risk, journal, UI |
| `treasury.intent` / `treasury.result` / `treasury.depeg` | Treasury moves and depeg alerts | treasury ↔ risk, signer; → UI |
| `social.draft.new` / `social.draft.decision` | Social drafts | social → telegram, UI |
| `venue.registry.changed` | Venue registry updates | mt-api → risk, engine |

**Rules:**
- **Dead-man's switch:** the engine's watchdog consumes `sys.heartbeat.*`. A missing critical heartbeat (engine, monitor, risk, postgres, nats) for N seconds triggers cancel-all and, if configured, flatten.
- **UI streams** are fanned out by mt-api over WebSocket topics with server-side throttling (≤ 4 Hz per symbol in charts, ≤ 1 Hz in tables).

## 7. API contract (`mt_api`)

**Transport and auth:**
- FastAPI under `/api/v1`, with OpenAPI generated and versioned.
- Auth: single user, local login (Argon2) + **TOTP**, over Tailscale only. Session cookie (`SameSite=Strict`, `HttpOnly`) for the web; scoped tokens for Telegram and MCP.

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
| `/positions`, `/orders`, `/fills` | Positions, orders, fills |
| `/markets/instruments`, `/markets/{id}/bars?spec=&from=&to=` | Instruments, bars |
| `/markets/{id}/book`, `/markets/matrix` | Order book, cross-asset matrix |
| `/strategies`, `/strategies/{id}`, `/strategies/{id}/runs`, `/strategies/templates` | Strategies |
| `/lab/backtests`, `/lab/backtests/{id}`, `/lab/experiments`, `/lab/jobs` | Research lab |
| `/agents/runs`, `/agents/runs/{id}`, `/signals` | Agent runs, signals |
| `/models/registry`, `/models/questions`, `/models/tierb/decisions`, `/models/benchmarks`, `/models/gateway/spend` | Models |
| `/memory/search`, `/memory/banks`, `/rag/search` | Memory and document search |
| `/risk/policy`, `/risk/state`, `/risk/events`, `/risk/changes`, `/risk/stress` | Risk |
| `/data/feeds`, `/data/quotas`, `/data/dq-events`, `/data/costs`, `/data/recon` | Data quality, costs, reconciliation |
| `/intel/documents` (+ `/{id}`), `/intel/events`, `/intel/calendar`, `/intel/sentiment` | Intel |
| `/mm/bots` (+ `/{id}`, `/{id}/pnl`) | Market-making bots |
| `/airdrops`, `/airdrops/{id}`, `/airdrops/mandates`, `/airdrops/wallet` | Airdrops |
| `/tasks` (+ `/{id}`), `/community`, `/social/drafts` | Tasks, curation and social drafts |
| `/wallets` (+ `/{id}`, `/transfers`), `/treasury`, `/treasury/earn` | Unified wallet view, treasury, hold-and-earn |
| `/venues/registry` | Venue access registry (12 §2) |
| `/journal/trades` (+ `/{id}`), `/journal/events`, `/journal/lots` | Journal |
| `/tax/summary?fy=`, `/tax/reports`, `/tax/residency` | Tax |
| `/system/health`, `/system/services`, `/system/logs` (Loki proxy), `/system/backups`, `/system/keys` (masked metadata only), `/system/settings` | System |
| `/mcp/tools` | MCP tool registry (Phase 8) |
| `/audit/log` | Audit log |
| `/notifications` | Notifications |

### 7.2 Commands (REST, write)

`POST /api/v1/commands/{command}`:
- Body: `{ "args": {...}, "idempotency_key": "...", "reason": "..." }`.
- Every command is written to `audit.command` with source = `web | telegram | mcp | system`.

**Confirmation levels** (enforced server-side, never only in the UI):

| Level | When | Flow |
|---|---|---|
| **C0** | Reads, harmless toggles (UI prefs, marking a task) | None |
| **C1** | Reversible actions (pause strategy, cancel order, run backtest) | In-app confirm sheet |
| **C2** | Trading actions (place/modify order, flatten, start a live strategy in approve mode) | Confirm sheet showing the risk-check preview; hold-to-confirm on touch |
| **C3** | **Loosening risk**: raise limits, enable `auto` mode, new mandate, disable kill switch | C2 + **Telegram approve + TOTP**, then a cool-down (default 15 min) before it takes effect |
| **Kill** | Kill switch ON | Single confirm (never blocked); turning it OFF is C3 |

**Command catalogue (v1):**

| Group | Commands |
|---|---|
| Orders | `order.place`, `order.modify`, `order.cancel`, `order.cancel_all`, `position.close`, `position.reduce`, `position.set_brackets` |
| Approvals | `approval.approve`, `approval.reject` |
| Strategies | `strategy.create`, `strategy.update_params`, `strategy.clone`, `strategy.archive`, `strategy.start`, `strategy.pause`, `strategy.resume`, `strategy.stop`, `strategy.promote`, `strategy.demote`, `strategy.set_mode` (paper / approve / auto) |
| Lab | `lab.backtest.run`, `lab.sweep.run`, `lab.validate.run`, `lab.generate_strategy`, `lab.job.cancel` |
| Agents & models | `agents.run_analysis`, `models.tierb.ask`, `models.promote`, `models.rollback`, `models.bakeoff.run`, `models.question.update`, `memory.delete` |
| Market making | `mm.bot.create`, `mm.bot.start`, `mm.bot.stop`, `mm.bot.update`, `mm.bot.cancel_all` |
| Risk | `risk.policy.update` (diff; tighten = C1, loosen = C3), `risk.kill.on`, `risk.kill.off`, `risk.deadman.ack`, `risk.stress.run` |
| Data | `data.feed.pause`, `data.feed.resume`, `data.backfill.run`, `data.recon.run` |
| Intel | `intel.source.add`, `intel.source.mute`, `intel.watchlist.update` |
| Airdrops | `airdrop.add_url`, `airdrop.rescore`, `airdrop.reject`, `airdrop.mandate.create` (C3), `airdrop.mandate.revoke`, `airdrop.claim.execute` (C2 unless covered by a mandate), `wallet.revoke_approval`, `wallet.sweep` |
| Tasks | `task.done`, `task.skip`, `task.snooze`, `task.never`, `social.draft.approve` (C1, opens a web intent), `social.draft.reject` |
| Wallets & treasury | `wallet.register` (C1), `wallet.tag` (C1), `treasury.allocate` (C2; loosening policy C3), `treasury.earn.enter` / `treasury.earn.exit` (C2) |
| Venues & ladder | `venue.registry.update` (tighten C1, allow C3), `risk.ladder.set` (down C1, up C3) |
| Journal & tax | `journal.note.add`, `journal.tag`, `tax.report.generate`, `tax.export`, `tax.residency.add`, `tax.regime.set`, `tax.lot.select` |
| System | `system.backup.run`, `system.restore.test`, `system.key.rotate_reminder`, `system.settings.update`, `system.service.restart`, `audit.verify` |
| MCP (Phase 8) | `mcp.tool.set`, `mcp.policy.set`, `mcp.token.revoke` |

### 7.3 Real-time (WebSocket `/api/v1/ws`)

- **Protocol:** subscribe/unsubscribe to topics: `{op: "sub", topic: "md.bar", params: {...}}`.
- **Topics:**
  - `portfolio`, `positions`, `orders`, `fills`;
  - `md.quote`, `md.trade`, `md.book`, `md.bar`;
  - `dq.status`, `cost`;
  - `risk.state`, `risk.event`, `kill`, `heartbeat`;
  - `signals`, `tierb`, `agents.run`;
  - `text.doc`, `evt`, `cal`;
  - `airdrop`, `tasks`, `journal`, `notifications`, `lab.job`, `system`;
  - `mm`, `recon`.
- **Message envelope:** `{topic, seq, ts, data}`. The client detects gaps via `seq` and re-syncs with the matching REST query.

### 7.4 Telegram & MCP

- **Telegram** maps buttons and slash commands to the same commands. It holds the **C3 confirmation** channel (approve + TOTP prompt).
- **MCP** (Phase 8) exposes the queries plus a subset of commands. MCP-originated orders default to approval-required. Withdrawals, keys and mandates are never exposed.

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
