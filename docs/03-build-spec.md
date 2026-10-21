# MasterTrader — Build Spec (personal-use edition, v2)

**Context:** a proprietary, private, single-user platform. The aim is **minimal hoops**: use whatever works best (including GPL/AGPL code), self-host on one machine, **free data and free tiers only**, and keep only the disciplines that protect money, records and future options.

**Design stance:** MasterTrader is a **platform, not a strategy**.
- It doesn't presume any trading style or timeframe.
- Any strategy type can be built, backtested, simulated, paper-traded and run live on any timeframe, from **tick / order-book level up to daily-and-above**.
- Strategies, risk limits and preferences are **user inputs** (UI, Telegram, and later MCP), not things baked into the code.

Companion docs:
- [07 security notes](07-security-notes.md)
- [08 airdrops & curation](08-airdrops-and-token-launches.md)
- [09 journal & tax](09-journal-and-tax.md)
- [06 data sources](06-aggregators-and-market-providers.md)
- [04 plan of action](04-plan-of-action.md)

---

## 1. Ground rules

| Rule | Meaning |
|---|---|
| **Personal use** | GPL/AGPL code can be used directly, because nothing is distributed or served to others. Yahoo, Myfxbook, ForexFactory and similar personal-use terms are fine. Keep the repo **private**. |
| **Free only** | Only free sources and free tiers. A single user should stay under the free limits. **Excluded (paid):** X API, CoinGlass, CME FedWatch API, TokenSniffer, Glassnode, Trading Economics, Databento credits, paid exchange data. **Every connector has a quota tracker that throttles before the limit.** |
| **Deferred** | Reddit (optional if API access is granted) and X: revisit only if free and permitted. **MCP control plane:** built last (Phase 8), only once the platform is in daily use. |
| **Never** | Self-bots, fake engagement, sybil farming, scraping that breaks a platform's terms, autonomous wallet signatures outside a mandate (see [07](07-security-notes.md)). |
| **Jurisdiction** | Australian tax resident now; possible move to the UAE, Egypt or Cyprus later. The journal and tax engine are jurisdiction-pluggable ([09](09-journal-and-tax.md)). |

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
| Observability | **Grafana + Loki** (logs, shipped by Vector) + **Prometheus** (metrics) + **OpenTelemetry** traces; Grafana Alerting → Telegram |
| Models | **Decision One** (M21): tier A = in-process compiled GBDT/ONNX (~10–50 µs) in the order path; tier B = **decision models** (SemIf readout → own Qwen3 + LoRA + classification head, ~2–12 ms on GPU) for text/context judgements, async. Research/chat/debate go through the **LiteLLM gateway** → Claude API / your custom endpoint / local fallback. Embeddings and rerank via **TEI** (bge-small-en-v1.5 + bge-reranker-v2-m3). See [10](10-memory-rag-and-models.md). |
| GPU (recommended) | One consumer GPU (16–24 GB VRAM) makes tier B fast (~150–300 ms/decision); without one, tier B is seconds-scale and used only for slower flags |
| Orchestration | Prefect (batch and scheduled flows); long-running services under Compose |
| Access | Everything bound to localhost or the internal network; remote access via **Tailscale** only |
| Secrets | `sops` + `age` encrypted file → tmpfs at start ([07 §2](07-security-notes.md#2-secrets)) |

---

## 3. Repository layout

```
MasterTrader/
├── pyproject.toml / uv.lock
├── docker-compose.yml            # postgres+timescale+pgvector, nats, prefect, grafana, loki, prometheus, vector, ollama, rss-bridge, app services
├── packages/
│   ├── mt_core/        # shared types (Instrument, BarSpec, Tick, Event, Signal, OrderIntent, RiskPolicy, JournalEvent), config, clock, logging
│   ├── mt_store/       # schemas (market, audit, journal, ops, curation), migrations, point-in-time query API, Parquet catalog helpers
│   ├── mt_data/        # connectors + recorders: market (M1), text/social (M2), events (M3), calendars (M5); quota tracker
│   ├── mt_features/    # feature library + evaluator (M6)
│   ├── mt_strategy/    # strategy framework: base classes, templates, registry, parameter schemas, multi-timeframe helpers (M0)
│   ├── mt_lab/         # backtest/sim orchestration, validation, optimisation, sandboxed LLM strategy generation (M7)
│   ├── mt_agents/      # LangGraph decision graph + tools (M8)
│   ├── mt_memory/      # Hindsight agent memory + document RAG (hybrid pgvector/tsvector, rerank) + decision settlement (M9)
│   ├── mt_models/      # Decision One tier A runtime + tier B advisor client, model registry, distillation, gateway config (M21)
│   ├── mt_anomaly/     # anomaly detectors + explain agent (M10)
│   ├── mt_risk/        # risk manager: policies, pre-trade checks, portfolio risk, kill switch, dead-man's switch (M11)
│   ├── mt_engine/      # Nautilus wrapper + custom adapters (Alpaca, OANDA, IG, cTrader, MT5) (M12)
│   ├── mt_monitor/     # live data-quality + cost/TCA monitor (M16)
│   ├── mt_obs/         # logging/metrics/tracing setup, audit writers, LLM-call audit (M17)
│   ├── mt_journal/     # journal ingestion, lot engine, FX service, jurisdiction plugins, reports, exports (M18)
│   ├── mt_airdrop/     # airdrop/launch discovery, risk & viability scoring, mandates, claim executor (M4)
│   ├── mt_curation/    # user task queue + community curation (Discord/Telegram/Galxe) + digests (M19)
│   ├── mt_api/         # internal command API used by UI, Telegram and (later) MCP; all actions go through it
│   ├── mt_ui/          # FastAPI web UI + Telegram bot (M15)
│   └── mt_mcp/         # (Phase 8, last) MCP server: thin adapter over mt_api (M20)
├── services/           # hummingbot (M13), crowdsim (M14), rss-bridge config, optional rotki / ghostfolio / beancount-fava
├── strategies/         # user strategies (any type), each with a manifest
├── third_party/        # vendored code (pinned commit + licence) + LICENSES.md
├── notebooks/  tests/  docs/  docs/runbooks/
```

**Design choice that keeps MCP cheap later:** every user action (change a risk limit, pause a strategy, adjust a position, approve an order, mark a task) is a typed command in **`mt_api`**.
- The web UI and the Telegram bot call `mt_api` from day one.
- The MCP server (M20) is then just a thin adapter that exposes the same commands to Claude.
- It needs no new business logic, so building it last costs little.

---

## 4. Data model (overview)

Postgres schemas:
- **`market`**: instruments, bars (hypertables), cost and spread series, funding/swap rates.
- **`text`**: documents, events, calendars.
- **`features`**
- **`strategy`**: registry, runs, results.
- **`risk`**: policies, limits, changes.
- **`audit`**: orders, fills, decisions, LLM calls, DQ/cost events, risk changes, commands.
- **`journal`**: events, lots, matches, FX rates, residency, reports.
- **`curation`**: tasks, community, airdrops.
- **`ops`**

Raw ticks, quotes and L2 live in the **Parquet catalog**.

**Point-in-time rule:**
- Every fact carries an `event_time` and an `ingest_time`.
- Research and backtests read only through `mt_store.pit(as_of=…)`.
- A CI test fails if a module bypasses it.

**Audit tables are append-only:**
- Insert-only DB roles.
- A daily hash chain.
- Corrections are new rows that reference the original.

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
  - market making (via Nautilus or the Hummingbot sidecar);
  - pairs/stat-arb;
  - event/news-driven;
  - ML-signal;
  - LLM-signal (M8).
- **Templates are starting points, not limits.** Any custom logic is allowed.
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
  - mode (backtest/paper/approve/auto).
- **Lifecycle:** draft → backtested → validated → paper → approve-mode → auto, with gates in §8. Every transition is logged.
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
- **ABS CPI** (needed for the 2027 tax indexation).
- **RBA F11 daily FX** (needed for tax).

**Fundamentals:** SEC EDGAR via edgartools (filings, 13F, Form 4, S-1/424B).

**Recording pipeline:**
- Venue WS → Nautilus data client → NATS.
- From NATS:
  - strategies (in-process);
  - the **Parquet recorder** (rolled every 1–5 minutes, compacted daily);
  - the **bar builder** writing 1s/1m bars into Timescale, with continuous aggregates for 5m–1D and arbitrary `time_bucket` sizes.

**Storage budget:** about 0.3–1 TB/year for about 10 liquid crypto symbols at trades + L1 + L2@1s.

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
- **Discord:** your own server + **followed announcement channels** + your own bot.
- **Bluesky Jetstream**, Mastodon.
- Conditional: StockTwits, YouTube RSS/API.
- **Reddit:** optional if API access is granted; **X deferred.**

**Processing:**
1. Dedupe.
2. Local-LLM relevance gate.
3. Entity/ticker linking.
4. FinBERT sentiment.
5. Local embeddings.
6. Store in `document` (approximate timestamps are flagged).

### M3 Global events — `mt_data.events`

**Sources:**
- USGS, GDACS, NOAA/NHC, NASA FIRMS, ReliefWeb, UCDP, GDELT, OpenSanctions.
- ACLED (research account).
- Central-bank statements and minutes.
- **Kalshi / Polymarket** public reads as event probabilities.

**Exposure map:** links each event's location to assets (country → FX/index/bond ETF; region → commodity).

**Event score:** severity × exposure × novelty.

### M4 Airdrops, token launches & ICOs — `mt_airdrop`

Full design: [08](08-airdrops-and-token-launches.md).

**Pipeline:** discover → vet → score → decide (auto-claim / user task / watch / reject) → track → journal.

**Risk feeds:**
- **GoPlus** (EVM), **RugCheck** (Solana), **Honeypot.is**.
- DexScreener, Helius and Etherscan free tiers.
- Phishing blocklists.
- Re-implemented solana-rugchecker heuristics and CRPWarner concepts; optional sandboxed Gigahorse deep scan.
- Scores calibrated on the SoK rug-pull dataset.

**Autonomous only for:**
- read-only work;
- **eligible claims** from a dedicated hot wallet under a signed mandate, with simulation;
- defensive revokes/sweeps.

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

### M6 Features — `mt_features`

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
  - deflated Sharpe;
  - **freqtrade look-ahead/recursive analysers** (vendored).
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
- **Output:** a structured `Signal` with provenance.
- **How strategies use it:** an *LLM-signal* strategy (M0) or any strategy can consume these signals as a feature.
- **Versioning:** prompts and models are versioned and every call is audited (M17).

### M9 Memory & RAG — `mt_memory`

Full design: [10](10-memory-rag-and-models.md).

**Hindsight** (MIT), self-hosted:
- **slim** image, running in our Postgres in its own `hindsight` schema;
- **local embedder and reranker via TEI**: bge-small-en-v1.5 (384-d) + bge-reranker-v2-m3;
- its LLM goes through the LiteLLM gateway.

**Memory banks:** `decisions`, `strategies`, `market-regimes`, `user`, `ops`. Point-in-time recall in backtests.

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
- **Explain agent:** writes a brief and sends it to Telegram.

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
| Sizing models (selectable per strategy) | Fixed size, fixed fractional, volatility target (ATR), Kelly-capped, risk-parity |

**Pre-trade checks:**
- policy limits;
- price collar (within X% of the last trade);
- liquidity/spread check from M16;
- duplicate-order check (idempotent client order IDs);
- event blackout;
- data-quality status (**no trading on a stale/bad feed**).

**Kill switch:**
- **Triggers:**
  - manual (UI, Telegram `/kill`, later MCP);
  - automatic on a breach: daily loss, drawdown, error rate, DQ failure, cost blow-out.
- **Actions:** cancel all, optionally flatten, block new orders.

**Dead-man's switch:** heartbeats from the engine, feeds, risk and DB. If one is missing for N seconds, cancel open orders and optionally flatten.

**Change control** (see [07 §6](07-security-notes.md#6-application-controls)):
- **Tightening** applies immediately.
- **Loosening** (raising a limit, enabling auto) needs Telegram confirmation + TOTP plus a cool-down.
- **Hard ceilings** live in a file no API can write.
- Every change is audited and versioned (rollback).

**Modes per mandate:** `paper` / `approve` (Telegram/UI button per order) / `auto`.

### M12 Execution — `mt_engine`

- **Nautilus adapters:** IBKR, Binance, Bybit, OKX, Coinbase, Kraken, Hyperliquid, Polymarket, Betfair.
- **Custom adapters:**
  - **Alpaca** (paper/live);
  - **OANDA v20**;
  - **IG**;
  - optionally **cTrader** Open API/FIX and Saxo (SIM);
  - MT5 (Windows bridge) if needed.
- **Key safety:** keys are trade-only, **withdrawals disabled**, IP allow-listed; separate sub-accounts for paper/approve/auto.

### M13 Market-making sidecar

- **Hummingbot** with telemetry off and broker IDs stripped.
- It's treated as a venue behind M11.

### M14 Crowd simulation (optional)

- MiroFish/OASIS scenario narratives, used as a candidate feature only.

### M15 UI & alerts — `mt_ui` (calls `mt_api`)

- **Web UI:**
  - strategy builder/registry;
  - backtest/experiment viewer;
  - risk-policy editor;
  - positions/P&L;
  - **manual trade ticket and position adjust** (through M11);
  - approvals queue;
  - task queue;
  - journal/tax views.
- **Grafana:** markets, costs, DQ, P&L, LLM spend, system health.
- **Telegram bot:**
  - alerts and digests;
  - approve/deny buttons;
  - task Done/Skip/Snooze;
  - `/kill`, `/status`, `/pnl`, `/pause <strategy>`.

### M16 Live cost & data-quality monitor — `mt_monitor` (always on, autonomous)

**Data quality**, a streaming service on NATS with rolling state per instrument:

| Check | Method |
|---|---|
| Stale feed | Session-aware timeout per instrument and venue |
| Gaps | Exchange sequence IDs / trade-ID continuity / expected bar counts |
| Bad ticks | Robust z-score (median/MAD); price outside the spread band; crossed/locked book |
| Cross-source divergence | Mid-price difference in bps between two free sources (Binance vs Bybit/OKX/Coinbase; OANDA vs Dukascopy/IG) |
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
- Incidents go to `audit.dq_events` / `audit.cost_events`.
- Metrics go to Prometheus, with Grafana alerts → Telegram.
- **M11 is told** to pause affected strategies (stale feed, spread > N× normal, cost ratio > 1.5×).
- Measured costs are **fed back** into the M7 backtest fee/slippage models.

**Reconciliation:**
- Positions and balances are compared with each venue's own records every N minutes and at end of day.
- Any mismatch is an incident.

### M17 Observability & audit — `mt_obs`

**System of record (Postgres `audit`)** holds:
- orders, fills, cancels, fees, funding;
- decisions and signals;
- **every LLM call** (model, prompt/response hash + text, tokens, cost, latency);
- risk-policy changes;
- DQ/cost incidents;
- **every `mt_api` command** (source: ui / telegram / mcp / system);
- mandate changes.

These tables are append-only and hash-chained, and kept ≥ 7 years.

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

**Backups:** pgBackRest + restic to an encrypted off-site target, with automated monthly restore tests.

### M18 Trading journal & tax — `mt_journal`

Full design: [09](09-journal-and-tax.md).

- **Journal:** an automatic, append-only journal of every economic event, with home-currency values and FX source (RBA for AUD).
- **Lot engine:** rp2-style; specific-ID first, FIFO fallback; FX-cash lots.
- **Jurisdiction plugins:**
  - **AU_2026** (50% discount, CFDs on revenue account, Div 775, crypto income, wash-sale flags, myTax mapping, **PAYG-instalment estimator**; GST/BAS mode dormant);
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
  - approve-mode orders.
- **Discord curation:**
  - invites discovered from **official sources only** (CoinGecko links, project sites/docs, official X bio) and verified against blocklists;
  - each entry states **which announcement channel to Follow** and which inbox channel to target;
  - a "leave when" condition;
  - the bot confirms delivery after you tap Done.
- **Cadence (configurable):**
  - instant alerts for urgent items;
  - **daily** digest;
  - **weekly** curation and review digest.
- **Telegram buttons:** Done / Skip / Snooze / Details / Never. Feedback tunes ranking, and tasks expire automatically.

### M21 Decision One & model serving — `mt_models`

Full design: [10 §4–5](10-memory-rag-and-models.md#4-decision-one-fast-accurate-concurrent-decisions).

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
  - **~2–12 ms per decision on a consumer GPU** (est.).
- **Bake-off:** against Laya (fine-tuned), self-hosted Clef-flash, SemIf and JSON generation, on our data + FinMMEval Buy/Hold/Sell.
- **Excluded:** Jev and Microsoft-Decision-1 (closed, paid).
- **Outputs:** cached on NATS KV as tier-A features; direct veto only above a calibrated high-precision threshold.
- **Determinism controls:** FP32 head, fixed batch, no prefix cache on the decision path, pinned revisions, logged prompt hash; CPU ONNX FP32 for backtests.

**Distillation:** M8's debate decisions (the teacher) plus realised outcomes train tier A and the tier B decision-model heads.
- Students are calibrated (isotonic/Platt; Brier/ECE).
- They are promoted only through §8 gates, with the teacher in shadow.

**Model gateway (LiteLLM proxy, ≥ 1.83, pinned by digest):**
- **Routes:** research, chat, debate, strategy generation, explain agents and Hindsight route via `research-primary` (Claude), then `research-custom` (your endpoint), then `local-advisor`.
- **Budgets and fallback:** per-role budgets; local fallback when a budget is exhausted.
- **Never on the hot path.**

**Supporting pieces:**
- **TEI** container (embeddings + rerank).
- **Model registry in MLflow:** version, training data range, calibration, benchmark latency.
- **Latency SLOs** per tier, monitored in M17.

### M20 MCP control plane — `mt_mcp` (built LAST, Phase 8, only if wanted)

**Purpose:** talk to the trading system and its agents through Claude (Desktop/Code) or another MCP client. You can ask, analyse, adjust and trade conversationally.

**How it's built:**
- A thin adapter over `mt_api`, using the official `mcp` Python SDK or FastMCP.
- Transport is **stdio**, or Streamable HTTP on localhost/Tailscale with token auth.
- **Because the UI and Telegram already use `mt_api`, this is mostly wiring.**

**Scope (all via `mt_api`; every order still passes through M11):**

| Area | Tools |
|---|---|
| Read & analyse | Positions, P&L, exposure, orders, fills; strategy status and performance; backtest/experiment results; cost/TCA and DQ status; market data and features; news/event summaries; journal/tax summaries; task queue |
| Talk to agents | Ask the M8 decision graph for analysis/a signal on an instrument; query memory (M9); request an anomaly explanation (M10) |
| Trade & adjust | Place/modify/cancel orders; **adjust or close positions**; move stops/targets; scale in/out; flatten an instrument or strategy |
| Strategies | Create/edit parameters, run backtests and sweeps, promote/demote (gates still apply), pause/resume |
| Risk | View the policy; tighten instantly; loosen with out-of-band confirmation; kill switch |
| Curation | Add watchlist items/airdrop URLs, mark tasks |

**Safeguards:**
- MCP orders go through the same risk manager.
- By default MCP-originated orders run in **approve mode** (Telegram button), configurable per venue and size.
- Loosening risk limits needs Telegram + TOTP confirmation.
- Hard ceilings can't be written.
- **Never exposed:** withdrawals, API-key management, wallet mandate signing.
- Every call is audited (`audit.commands`, source = mcp).

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
  - All non-hot-path calls go through the **LiteLLM gateway** with per-role daily budgets and local fallback.
- **When agents run:**
  - per the strategy's configured cadence;
  - **event-triggered** (anomaly, calendar, big news);
  - never per tick.
- **Caching:** tool outputs are cached per (instrument, as_of).
- **Spending limit:** a monthly cap, with a spend panel in Grafana.

---

## 8. Promotion gates (per strategy, configurable)

1. **Out-of-sample performance:** beats its benchmark on walk-forward out-of-sample data, after measured costs (M16).
2. **Robustness statistics:** Monte Carlo permutation p < 0.05; deflated Sharpe > 0.
3. **Bias checks:** the look-ahead and recursive analysers come back clean.
4. **LLM strategies:** evaluated on data after the model's training cutoff.
5. **Paper / approve trading:**
   - paper or approve mode for a configurable period (default 3 months);
   - P&L and costs track the backtest within tolerance.
6. **Live:** start small; scale on schedule.

---

## 9. Future-proof hygiene

1. Third-party code lives under `third_party/` with a licence manifest.
2. GPL/AGPL code is isolated.
3. Every data source is tagged `license: personal|commercial_ok|unknown` and `cost: free|paid`.
4. The repo stays **private**.
