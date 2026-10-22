# MasterTrader — Build Spec (personal-use edition, v2)

**Context:** a proprietary, private, single-user platform. The aim is **minimal hoops**: use whatever works best (including GPL/AGPL code), self-host on one machine, **free data and free tiers only**, and keep only the disciplines that protect money, records and future options.

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

---

## 1. Ground rules

| Rule | Meaning |
|---|---|
| **Personal use** | GPL/AGPL code can be used directly, because nothing is distributed or served to others (e.g. freqtrade's analysers are vendored in M7). Yahoo, Myfxbook, ForexFactory and similar personal-use terms are fine. Keep the repo **private**. |
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
| Host | One Linux box: 8–16 cores, 32–64 GB RAM, **2–4 TB NVMe** (tick/L2 storage), plus a HDD for cold Parquet. Optional GPU for local LLMs. Full-disk encryption. |
| Language / packaging | Python 3.12, `uv` workspace monorepo |
| Runtime | Docker Compose, with images pinned by digest |
| Engine | **NautilusTrader** (pinned), event-driven: the same code runs backtest, sandbox/paper and live |
| Bus | **NATS JetStream** (market data fan-out, events, alerts) |
| Databases | **Postgres 16 + TimescaleDB (TSL Community image) + pgvector** is the system of record. **Nautilus ParquetDataCatalog + DuckDB** hold raw ticks/L2. **QuestDB** is optional, only if live SQL over raw ticks is ever needed. |
| Observability | **Grafana + Loki** (logs, shipped by Vector) + **Prometheus** (metrics) + **OpenTelemetry** traces. **One alert fan-out:** Grafana alerts → webhook → the `alert.*` consumer → Telegram / ntfy / email |
| Models | **Decision One** (M21): tier A = in-process compiled GBDT/ONNX (~10–50 µs) in the order path; tier B = **decision models** (SemIf readout → own Qwen3 + LoRA + classification head, ~2–12 ms on GPU) for text/context judgements, async. Research/chat/debate go through the **LiteLLM gateway** → Claude API / your custom endpoint / local fallback. Local fallback model served by `llm-local` (llama-server on CPU or vLLM on GPU) for the `local-advisor` route. Embeddings and rerank via **two TEI containers**: `tei-embed` (bge-small-en-v1.5) and `tei-rerank` (bge-reranker-v2-m3). See [10](10-memory-rag-and-models.md). |
| GPU (recommended) | One consumer GPU (16–24 GB VRAM) makes tier B fast: ~2–12 ms per decision (0.6B head), p95 SLO < 50 ms. Without one, tier B runs CPU ONNX at ~100–400 ms per decision and is used only for slower flags ([10 §4.3](10-memory-rag-and-models.md#43-design)) |
| Orchestration | Prefect (batch and scheduled flows); long-running services under Compose |
| Access | Everything bound to localhost or the internal network; remote access via **Tailscale** only |
| Secrets | `sops` + `age` encrypted file → tmpfs at start. The encrypted file lives **outside this repo** (e.g. `~/.config/mastertrader/`), backed up by restic ([07 §2](07-security-notes.md#2-secrets)) |

---

## 3. Repository layout

This is the **canonical** layout; [02 §11](02-v1-architecture.md#11-repository-layout) points here. The full container list is in [02 §3.2](02-v1-architecture.md#32-containers).

```
MasterTrader/
├── pyproject.toml / uv.lock      # uv workspace
├── packages/                     # Python packages
│   ├── mt_core/        # shared types (Instrument, BarSpec, Tick, Event, Signal, OrderIntent, RiskPolicy, JournalEvent), config, clock, logging
│   ├── mt_store/       # schema definitions (all 13 schemas in §4), point-in-time query API, WORM helpers, Parquet catalog helpers
│   ├── mt_data/        # connectors + recorders: market (M1), text/social (M2), events (M3), calendars (M5); quota tracker
│   ├── mt_features/    # feature library + evaluator (M6)
│   ├── mt_strategy/    # strategy framework: base classes, templates, registry, parameter schemas, multi-timeframe helpers (M0)
│   ├── mt_lab/         # backtest/sim orchestration, validation, optimisation, sandboxed LLM strategy generation (M7)
│   ├── mt_agents/      # LangGraph decision graph + tools (M8)
│   ├── mt_memory/      # Hindsight agent memory + document RAG (hybrid pgvector/tsvector, rerank) + decision settlement (M9)
│   ├── mt_models/      # Decision One tier A runtime + tier B advisor client, model registry, distillation, gateway config (M21)
│   ├── mt_anomaly/     # anomaly detectors + explain agent (M10)
│   ├── mt_risk/        # risk manager: policies, pre-trade checks, portfolio risk, kill switch, dead-man's switch incl. the `deadman` sidecar (M11)
│   ├── mt_engine/      # Nautilus wrapper + custom adapters (Alpaca, OANDA, IG, cTrader, MT5) (M12)
│   ├── mt_monitor/     # live data-quality + cost/TCA monitor (M16)
│   ├── mt_obs/         # logging/metrics/tracing setup, audit writers, LLM-call audit (M17)
│   ├── mt_journal/     # journal ingestion, lot engine, FX service, jurisdiction plugins, reports, exports (M18)
│   ├── mt_airdrop/     # airdrop/launch discovery, risk & viability scoring, mandates, claim executor (M4)
│   ├── mt_curation/    # user task queue + community curation (Discord/Telegram/Galxe) + digests (M19)
│   ├── mt_onchain/     # on-chain helpers: the cost gate library (`mt_onchain.costgate`), simulation, live fee inputs
│   ├── mt_signer/      # intents-only signer for hot/burner/identity keys; accepts intents only from the policy service; writes `audit.signer_ledger` (13 §2)
│   ├── mt_treasury/    # wallets registry + unified view, custody tiers, signer client, hold-and-earn, yield allocator, DAO/depeg/exploit monitors (M22)
│   ├── mt_social/      # social participation: drafts → your approval → web-intent post; credibility + shill-burst posture (M23)
│   ├── mt_api/         # internal command API used by UI, Telegram and (later) MCP; all actions go through it
│   ├── mt_ui/          # Telegram bot (M15); the web app is `apps/web`
│   └── mt_mcp/         # (Phase 8, last) MCP server: thin adapter over mt_api (M20)
├── apps/web/           # React + TypeScript SPA (M15 web UI, [02 §10](02-v1-architecture.md#10-frontend-architecture)), served by Caddy
├── infra/              # docker-compose.yml (images pinned by digest), caddy, grafana dashboards, prometheus/alert rules, sops config (no secrets), host provisioning, seeds
├── migrations/         # Alembic migrations for every schema
├── services/           # hummingbot (M13), crowdsim (M14), rss-bridge config, optional rotki / ghostfolio / beancount-fava
├── strategies/         # user strategies (any type), each with a manifest
├── third_party/        # vendored code (pinned commit + licence) + LICENSES.md
├── notebooks/  tests/  docs/  docs/runbooks/  ui-examples/  brand/  DESIGN.md
```

**Design choice that keeps MCP cheap later:** every user action (change a risk limit, pause a strategy, adjust a position, approve an order, mark a task) is a typed command in **`mt_api`**.
- The web UI and the Telegram bot call `mt_api` from day one.
- The MCP server (M20) is then just a thin adapter that exposes the same commands to Claude.
- It needs no new business logic, so building it last costs little.

---

## 4. Data model (overview)

Postgres schemas (one canonical list; **all 13 are created in Phase 0**, later phases add tables additively):
- **`market`**: instruments, bars (hypertables), cost and spread series, funding/swap rates.
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

**Point-in-time rule:**
- Every fact carries an `event_time` and an `ingest_time`.
- Research and backtests read only through `mt_store.pit(as_of=…)`.
- A CI test fails if a module bypasses it.

**Audit tables are WORM** (write-once, read-many; full design in [15 §2](15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)):
- Owned by an offline `worm_owner` role; app roles INSERT/SELECT only; UPDATE/DELETE/TRUNCATE revoked and blocked by triggers.
- Per-row hash chain (`prev_hash`, `row_hash`) plus a daily Merkle seal anchored outside the DB (object-locked storage, optional OpenTimestamps, Telegram witness).

**Append-only rules:**
- Insert-only DB roles.
- A per-row hash chain, sealed daily outside the DB.
- Corrections are new rows that reference the original.
- WORM insert p99 < 5 ms; the order path never waits on seals.

(Full column lists live in each module's spec and in migrations. Earlier tables (`document`, `geo_event`, `calendar_event`, `signal`, `decision_log`, `exposure_map`) are kept.)

---

## 5. Modules

### M0 Strategy framework — `mt_strategy` (strategy-agnostic, any timeframe)

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
  1. write Python;
  2. configure a template in the UI;
  3. describe it to the LLM strategy generator (M7, sandboxed);
  4. import/port from other frameworks (freqtrade/Vibe-Trading patterns).
- **Experimentation:**
  - parameter sweeps;
  - A/B comparisons on identical data;
  - shadow mode (a live strategy runs in parallel paper mode for comparison).

### M1 Market & macro data — `mt_data.market`

**Free only, with a quota tracker per connector.**

**Crypto:**
- **Real-time:** public WebSockets for trades, L1 and L2 diff depth (Binance, Bybit, OKX, Coinbase, Kraken) via the Nautilus adapters and ccxt.
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
- yfinance / OpenBB for daily history.
- FinanceDatabase as the symbol master.

**Futures/commodities:**
- No free real-time feed, so daily data only (yfinance `GC=F`, `CL=F`; akshare for Asia).
- EIA, USDA (WASDE/QuickStats), CFTC COT, Baker Hughes.
- **Futures-like exposure is traded via crypto perps or FX/CFDs** (OANDA/IG).

**Rates & macro:**
- US Treasury, **FRED/ALFRED** (vintages).
- **`sdmx1`** for ECB/IMF/OECD/BIS/Eurostat.
- BoE IADB, BoC Valet, RBA, SNB, BoJ.
- DBnomics as the catch-all.
- **ABS CPI**: All groups CPI, weighted average of eight capital cities (series A2325846C (U), verify), needed for the 2027 tax indexation.
- **RBA F11 daily FX** (needed for tax).

**Fundamentals:** SEC EDGAR via edgartools (filings, 13F, Form 4, S-1/424B).

**Recording pipeline:**
- Venue WS → Nautilus data client → NATS.
- From NATS:
  - strategies (in-process);
  - the **Parquet recorder** (rolled every 1–5 minutes, compacted daily);
  - the **bar builder** writing 1s bars into Timescale, with continuous aggregates at 1m, 5m, 15m, 1h, 4h, 1D and 1W. Any other size is a `time_bucket` query at read time.

**L2 recording:** raw L2 diffs at native speed only for symbols a bot needs order-book data for (default ≤ 3 symbols, configurable); 1 s book snapshots for the rest.

**Storage budget:** about 0.3–1 TB/year for about 10 liquid crypto symbols at trades + L1 + L2 on that basis (U; re-measured in the Phase 1 soak).

### M2 News & social — `mt_data.text`

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

**Sources:**
- USGS, GDACS, NOAA/NHC, NASA FIRMS, ReliefWeb, UCDP, GDELT, OpenSanctions.
- ACLED (research account). FIRMS/ACLED keys and the OpenSanctions licence are a USER task.
- Central-bank statements and minutes.
- **Kalshi / Polymarket** public reads as event probabilities. **Read-only:** Polymarket is ISP-blocked for Australians, so only where lawfully reachable, never via VPN; no trading.

**Exposure map:** links each event's location to assets (country → FX/index/bond ETF; region → commodity).

**Event score:** severity × exposure × novelty.

### M4 Airdrops, token launches & ICOs — `mt_airdrop`

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

- **Sources:**
  - FRED/ALFRED release dates;
  - **ForexFactory weekly JSON** (consensus forecasts, cached);
  - central-bank meeting schedules;
  - COT/EIA/WASDE/Baker Hughes days;
  - EDGAR earnings and IPO filings;
  - exchange holiday/session calendars (`exchange_calendars`).
- **Strategy and risk uses:** strategies and the risk manager can query "event within N minutes", e.g. to pause scalpers around NFP.
- **Default blackout:** for high-importance events, bots marked `event_sensitive` (scalping/intraday templates by default) block new entries from 15 min before to 15 min after; exits and protective orders continue. Configurable per bot and event type ([16 §2.8](16-configuration-and-safety-model.md#28-calendar-blackouts)).

### M6 Features — `mt_features`

- **Sentiment & regime per market type:** separate pipelines for crypto, FX, gold/silver/metals, energy and equities/indices, plus a shared **macro layer** (USD, rates, calendar, risk-on/off). Each outputs a sentiment score, fear/greed gauge, news-impact flags and a **regime label**. Crypto inputs add Fear & Greed, funding, open interest, liquidations and long/short ratios.
- **Market and factor features:**
  - TA-Lib;
  - Qlib Alpha158;
  - Vibe-Trading factor zoo;
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
- **Forecast models:** Chronos / TimesFM / Kronos for volatility and volume.
- **Versioning and evaluation:** features are versioned, and an evaluator measures IC, rank-IC and decay.

### M7 Research lab — `mt_lab`

- **Two backtest paths:**
  - **Screening:** fast vectorised path (vectorbt / Vibe-Trading engines).
  - **Truth:** **Nautilus** backtests with L1/L2 replay, measured fee/slippage/latency models (fed from M16) and funding/swap costs.
- **Validation:**
  - walk-forward;
  - purged K-fold;
  - Monte Carlo permutation;
  - bootstrap Sharpe CI;
  - deflated Sharpe (DSR, a probability; default gate ≥ 0.95);
  - **freqtrade look-ahead/recursive analysers**: GPL-3.0, vendored under `third_party/` with their licence and isolated in `mt_lab` (personal use, §1). A clean-room rewrite is needed only for a SaaS ([05](05-saas-legal-and-licensing.md)).
  - Leakage findings are fixed, or each is waived by you (`lab.leakage.waive`, C2, audited).
- **Optimisation:**
  - Optuna, with a complexity penalty;
  - experiment tracking (**MLflow**, self-hosted) of every run: code version, parameters, data range, costs, results.
- **Sandboxed LLM strategy generation:** no network, no secrets.

### M8 AI decision layer — `mt_agents`

- **Debate graph:** a TradingAgents-style LangGraph run:
  1. Analysts: technical, sentiment, news, fundamentals, macro/events.
  2. Bull/bear debate.
  3. Research manager.
  4. Trader.
  5. Risk debate.
  6. Portfolio manager.
- **Tools:** FinRobot V2 valuation operators, `pit` data tools, memory recall.
- **Output:** a structured `Signal` with fields: id, ts, as_of, instrument, horizon, direction, edge, calibrated confidence, rationale summary, sources[], model/prompt versions, run id.
- **How strategies use it:** an *LLM-signal* strategy (M0) or any strategy can consume these signals as a feature.
- **Versioning:** prompts and models are versioned and every call is audited (`audit.llm_call`, written from P0, M17).

### M9 Memory & RAG — `mt_memory`

Full design: [10](10-memory-rag-and-models.md).

**Hindsight** (MIT), self-hosted:
- **slim** image, running in our Postgres in its own `hindsight` schema;
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

- **Detectors** on market, sentiment and event streams:
  - robust z-scores;
  - IsolationForest;
  - change points;
  - correlation breaks.
- **Explain agent:** writes a brief and sends it to Telegram. It also runs on request (`anomaly.explain`, C1, from the UI or MCP).

### M11 Risk manager — `mt_risk` (built in; user inputs via UI/Telegram, later MCP)

**Authoritative and default-deny.** It runs as a pre-trade check in front of the Nautilus `RiskEngine`, which also enforces hard limits natively. **Every order passes through it,** whatever its source: strategy, LLM agent, UI, Telegram or MCP.

**Risk policy** is a versioned YAML/DB document, edited through `mt_api`. It covers several levels:

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
- Until the Telegram C3 path exists (P2), C3 commands complete through a host-only break-glass CLI (`mtctl approve <id>` + TOTP over SSH/Tailscale), audited.
- Every change is audited and versioned (rollback).

**Modes per mandate / bot:** `paper` / `hitl` (formerly `approve`: Telegram/UI approval card per order) / `autonomous` (formerly `auto`). paper → HITL is C2; HITL → autonomous is C3.

**Trading bots:** a bot deploys one strategy version onto a market scope (single instrument, list or dynamic selection) with its own venue account, sleeve, mode and approval policy. You set each bot to **autonomous** or **HITL**; HITL bots send approval cards to Telegram; protective exits never wait for approval; autonomous needs C3 and auto-downgrades to HITL on decay/DQ/ladder events. Full design: [15 §1](15-bots-hitl-and-worm-audit.md#1-trading-bots).

### M12 Execution — `mt_engine`

- **Nautilus adapters:** IBKR, Binance, Bybit, OKX, Coinbase, Kraken, Hyperliquid, Betfair. These are subject to the **venue access registry**: for an AU resident, offshore perps (Bybit/Bitget…) are data-only, Hyperliquid waits on professional advice, and Polymarket trading is blocked.
- **Custom adapters:**
  - **Alpaca** (paper/live);
  - **OANDA v20**;
  - **IG**;
  - optionally **cTrader** Open API/FIX and Saxo (SIM);
  - MT5 (Windows bridge) for **FP Markets / MasterTradingBot**, with cTrader Open API as the Linux route ([14 §8](14-strategy-evidence-and-validation.md#8-mastertradingbot-integration));
  - **AU spot venues via ccxt**: Independent Reserve, BTC Markets, Kraken AU, CoinSpot;
  - **DEX execution**: Jupiter + Jito (Solana), 1inch free + Flashbots Protect (EVM), via the signer service and the **on-chain cost gate** ([13 §7](13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16)).
- **Key safety:** keys are trade-only, **withdrawals disabled**, IP allow-listed to one fixed AU egress IP (an exit node with a static IP; broadband and 4G both tunnel to it, [16 §3.2](16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys)); separate sub-accounts per mode (`paper` / `hitl` / `autonomous`). Practice/paper accounts use their normal credentials; live accounts use read-only keys where offered, otherwise trade-only.
- **IBKR** runs through an `ib-gateway` container (IBC-managed) when used.
- **Self-trade prevention:** the STP mode is sent **explicitly on every order** where the venue supports it (12 §3). Netting brokers (OANDA, IG, Alpaca, IBKR) have no STP field: the venue registry marks `stp: n/a (netting)`, and one strategy runs per account/sub-account where netting would merge bots.
- **Client order ID** = `{bot}-{engine_epoch}-{seq}`; a signal hash is stored separately for idempotency, so a restarted engine can't resubmit the same signal. Open orders are reconciled from the venue before trading resumes.
- **Venue-side protection:** cancel-after timers (refreshed every 15 s, 60 s timeout by default) and a resting venue stop for every live position (dead-man layer 3, M11).

### M13 Market-making sidecar

- **Hummingbot** with telemetry off and broker IDs stripped.
- It's treated as a venue behind M11.

### M14 Crowd simulation (optional)

- MiroFish/OASIS scenario narratives, used as a candidate feature only.
- Only with a **local memory backend** and a hardened config (auth on, no default secrets, no open CORS); **no Zep Cloud**. If that isn't possible, M14 is skipped.

### M15 UI & alerts — `mt_ui` (calls `mt_api`)

**Design source of truth:** [DESIGN.md](../DESIGN.md) v2.
- Fully responsive from 1920px+ down to 240px, portrait and landscape, on the shared breakpoint set.
- Reference screens are in [ui-examples/](../ui-examples/README.md).
- Tailwind is built locally (no CDN).
- A Playwright viewport-matrix test runs in CI.


- **Web UI** (React SPA in `apps/web`, served by Caddy, calling `mt_api`):
  - strategy builder/registry;
  - backtest/experiment viewer;
  - risk-policy editor;
  - positions/P&L;
  - **manual trade ticket and position adjust** (through M11);
  - approvals queue;
  - task queue;
  - journal/tax views.
- **Grafana:** markets, costs, DQ, P&L, LLM spend, system health. Its alerts use the one fan-out in §2 (webhook → `alert.*` → Telegram / ntfy / email).
- **Telegram bot:**
  - alerts and digests;
  - approve/deny buttons;
  - task Done/Skip/Snooze;
  - `/kill` (published on NATS `kill.set` with credentials limited to that subject; the engine writes the WORM record with source `telegram`), `/status`, `/pnl`, `/pause <strategy>`.

### M16 Live cost & data-quality monitor — `mt_monitor` (always on, autonomous)

**Data quality**, a streaming service on NATS with rolling state per instrument:

| Check | Method |
|---|---|
| Stale feed | **Data age** = now − our receive time per stream (not the exchange timestamp). Thresholds per bot (default 2 s fast / 60 s slow), session-aware (closed sessions are `closed`, not stale). The monitor flips `dq.status` to `stale` ≤ 250 ms (p99) after the threshold; M11 also checks age inline on every order ([16 §2.2](16-configuration-and-safety-model.md#22-data-freshness-what-stale-means)) |
| Gaps | Exchange sequence IDs / trade-ID continuity / expected bar counts |
| Bad ticks | Robust z-score (median/MAD; default flag at z ≥ 8, configurable); price outside the spread band; crossed/locked book |
| Cross-source divergence | Mid-price difference in bps between two free sources (Binance vs Bybit/OKX/Coinbase; OANDA vs Dukascopy/IG); default alert at 25 bps crypto / 5 bps FX majors, configurable |
| Clock skew | `recv_ts − exchange_ts` p99; chrony offset |
| Book integrity | Venue checksums; periodic REST snapshot reconciliation |
| Batch | Nightly Pandera validation of Parquet; Evidently drift reports |

**Costs, always measured from free APIs:**
- **Fees:**
  - commissions per fill and current fee tiers (ccxt `fetchTradingFees`, Binance commission endpoint, IBKR `commissionAndFeesReport`, Alpaca);
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

**System of record (Postgres `audit`)** holds:
- orders, fills, cancels, fees, funding (`audit.order`, `audit.fill`);
- decisions and signals (`audit.decision_run`);
- **every LLM call** (`audit.llm_call`: model, prompt/response hash + text, tokens, cost, latency), written **from P0** via the LiteLLM callback;
- risk-policy changes;
- DQ/cost incidents and reconciliation (`audit.dq_event`, `audit.dq_ack`, `audit.cost_event`, `audit.recon`);
- **every `mt_api` command** (`audit.command`; source: `web` / `telegram` / `mcp` / `system`);
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
- **Loki**, fed by Vector, with structured JSON logs (structlog) and low-cardinality labels.
- Retention 30–90 days.
- Every audit row carries a `trace_id` so you can jump from a fill to its logs in Grafana.

**Metrics and traces:** Prometheus + OpenTelemetry (optionally Tempo); optionally **Arize Phoenix** for an LLM-trace UI.

**Not chosen:**
- Graylog (SSPL, heavy).
- OpenObserve (AGPL, duplicates Grafana).
- Soda Core (now ELv2).
- ArcticDB (BSL).
- TDengine (AGPL, IoT-focused). This is our reading of "TenentDB".

**Backups:** pgBackRest + restic to an encrypted off-site target: continuous WAL archive, nightly incremental, weekly full, a monthly automated restore test and a monthly immutable WORM export.

### M18 Trading journal & tax — `mt_journal`

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

Full design: [10 §4–5](10-memory-rag-and-models.md#4-decision-one-decision-models--microsecond-engine).

**Tier A: microsecond engine, in the order path.**
- **Model and runtime:** a GBDT/linear/small-MLP model, compiled to **ONNX Runtime / Treelite / lleaves**, loaded **in-process** in the strategy.
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

Full design: [13](13-wallets-treasury-and-onchain.md).

- **Wallets:**
  - **Custody tiers:** vault (cold, manual), Hyperliquid master (hardware EIP-712, if approved), warm, hot, airdrop identity (one per chain), burner.
  - **Vault and warm are watch-only:** the system never holds their keys; it may prepare unsigned transactions (QR/WalletConnect) for you to sign in your own wallet.
  - The **signer service** accepts intents only, and only from the policy service (airdrop-exec, treasury and DEX execution all go through it), with allow-lists, caps, simulation, sized-and-revoked approvals and **durable-nonce hard blocks**. Floats, signer caps and gas budgets are defaults you confirm before signing is enabled ([16 §2.7](16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)).
  - The **cost gate** is one library, `mt_onchain.costgate`: the signer uses it from P5, the treasury from P6.
- **Unified wallet view:**
  - one address registry, `ops.wallets` (created in P3, extended by the P5 wallet-indexer), with read-only aggregation (Helius DAS, Blockscout/RPC, Hyperliquid `/info`, ccxt read-only);
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

**Purpose:** talk to the trading system and its agents through Claude (Desktop/Code) or another MCP client. You can ask, analyse, adjust and trade conversationally.

**How it's built:**
- A thin adapter over `mt_api`, using the official `mcp` Python SDK or FastMCP.
- **Transport:** Streamable HTTP (JSON-RPC 2.0, SSE streaming, resumable) on Tailscale/TLS, or stdio (newline-delimited JSON) locally; an optional legacy HTTP+SSE endpoint for older clients. The `mcp` container sits on the internal network behind Caddy, on Tailscale only. Server notifications (fills, approvals, alerts) use resource subscriptions.
- **Tokens:** opaque 256-bit, shown once, stored hashed (HMAC-SHA-256 with a server pepper), scoped, revocable instantly, with last-used time and client identity recorded. Expiry is your choice per token: 1 day · 7 days · 30 days · 1 year · custom · indefinite (indefinite = red warning + C3 + monthly reminder). Creating a token is C2 for `read` / `analyse` / `curation` scopes and C3 for `trade` / `strategy` / `risk_tighten` scopes or indefinite expiry ([16 §2.12](16-configuration-and-safety-model.md#212-mcp-phase-8)). OAuth 2.1 (PKCE, resource indicators) for clients that support MCP authorization.
- **Because the UI and Telegram already use `mt_api`, this is mostly wiring.**

**Scope (all via `mt_api`; every order still passes through M11):**

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
| US stocks/ETFs | IEX trades/quotes, 30 symbols (Alpaca free) | Alpaca IEX history; daily via yfinance | IEX ≠ NBBO: fine for swing, weak for scalping cost measurement |
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
2. GPL/AGPL code is isolated.
3. Every data source is tagged `license: personal|commercial_ok|unknown` and `cost: free|paid`. Every **row** carries provenance + use flags (12 §5), so a SaaS pivot is a retrain on `commercial_ok` rows.
4. The repo stays **private**.
