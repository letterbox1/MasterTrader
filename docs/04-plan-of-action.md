# MasterTrader — Plan of Action (v2)

Personal-use build, one developer plus AI pair-programming. Time estimates assume evenings and weekends; halve them if full-time.

**Order of work:**
1. Make the **platform workable** first: data, storage, monitoring, strategy framework, risk, journal.
2. Then **strategies get added and experimented with by you**. The plan never assumes a trading style or timeframe.
3. Each phase ends with a **demo you can actually use**.
4. **MCP is last** (Phase 8), and only if you want it.

Module numbers (M0–M20) refer to [03-build-spec.md](03-build-spec.md).

## ⚠️ Do this week regardless of phase
- [ ] **Telegram:**
  - register `api_id`/`api_hash` at my.telegram.org with a **dedicated number** (try the landline via voice-call code, otherwise a prepaid SIM);
  - set a 2-step password;
  - create a bot via @BotFather.
- [ ] **Discord:**
  - create a private "MasterTrader Feeds" server with `#mt-inbox` (+ category channels);
  - register a bot app with the Message Content intent;
  - start following the announcement channels you already know about.
- [ ] **Reddit (optional):** apply for free personal API access before 2026-10-31 (see [06 §0](06-aggregators-and-market-providers.md#0-️-time-sensitive-actions)). X stays deferred.
- [ ] **Free demo/practice accounts:**
  - OANDA practice, IG demo, Alpaca paper, IBKR paper;
  - Binance and Bybit testnets.
- [ ] **Free API keys:** FRED, EIA, Myfxbook, CoinGecko Demo, CryptoRank Sandbox, Etherscan, Helius, GoPlus, Tenderly.

## Phase 0 — Foundations & security baseline (weeks 1–2)
- [ ] **Monorepo and code quality:**
  - `uv` workspace, packages per [build spec §3](03-build-spec.md#3-repository-layout);
  - ruff, mypy, pytest, pre-commit with **gitleaks**;
  - `third_party/LICENSES.md`.
- [ ] **Host:**
  - LUKS full-disk encryption, firewall deny-inbound;
  - Tailscale-only access;
  - chrony for time sync.
- [ ] **`docker-compose.yml`** (images pinned by digest):
  - Postgres 16 + TimescaleDB (TSL image) + pgvector;
  - NATS JetStream;
  - Prefect;
  - Grafana + Loki + Prometheus + Vector;
  - Ollama;
  - MLflow.
- [ ] **Core code:**
  - `mt_core` types;
  - `mt_store` schemas (`market`, `text`, `features`, `strategy`, `risk`, `audit`, `journal`, `curation`, `ops`) + Alembic migrations;
  - `pit(as_of)` API + CI test.
- [ ] **Audit and logging:**
  - append-only audit roles + daily hash chain;
  - structured logging (structlog) with `trace_id`.
- [ ] **Secrets and backups:**
  - `sops`/`age` secrets;
  - pgBackRest + restic off-site backups;
  - automated restore test.
- [ ] **`mt_api` command layer skeleton.** The UI and Telegram will call it; MCP will later wrap it.
- [ ] **Model gateway:**
  - LiteLLM proxy (≥ 1.83, pinned by digest) with Claude + your custom endpoint + a local model;
  - per-role budgets;
  - **TEI** container (bge-small-en-v1.5 + bge-reranker-v2-m3).

**Demo:** `docker compose up` gives a healthy stack, with Grafana showing DB/NATS/host health and logs in Loki.

## Phase 1 — Market data, recording & live monitoring (weeks 3–6)
- [ ] **Crypto real-time** via Nautilus/ccxt WebSockets: trades, L1, L2 diff. Recorded to the **Parquet catalog**, plus a bar builder writing 1s/1m bars to Timescale with continuous aggregates to 1D.
- [ ] **Crypto history:** data.binance.vision backfill (trades/aggTrades/1s klines).
- [ ] **FX & metals:**
  - OANDA practice stream + IG demo stream;
  - Dukascopy tick history;
  - ECB/Frankfurter reference rates;
  - **RBA F11 FX** (for tax).
- [ ] **Stocks/ETFs:** Alpaca IEX + yfinance daily; FinanceDatabase symbol master; `exchange_calendars`.
- [ ] **Macro:**
  - FRED/ALFRED, Treasury, `sdmx1` (ECB/IMF/OECD/BIS/Eurostat), BoE/BoC/RBA/SNB;
  - EIA, USDA, CFTC COT;
  - **ABS CPI**.
- [ ] **Fundamentals:** EDGAR via edgartools.
- [ ] **Quota tracker** per connector (free-tier throttling).
- [ ] **M16 data-quality monitor:** stale, gaps, bad ticks, cross-source divergence, clock skew, book integrity → `audit.dq_events` + Grafana alerts → Telegram.
- [ ] **M16 cost monitor:**
  - fee tiers, funding, swap/financing, spreads by hour-of-week;
  - venue balance/position reconciliation.
- [ ] Run the open provider checks in [06 §3](06-aggregators-and-market-providers.md#open-checks-do-these-in-phase-1).

**Demo:** Grafana shows live prices at every timeframe from ticks to 1D across all asset classes, plus live spread/funding/swap panels and data-quality alerts arriving on Telegram.

## Phase 2 — Strategy framework, risk manager & research lab (weeks 7–11)
- [ ] **M0 strategy framework:**
  - templates for scalping, intraday, EMA/MA, mean-reversion, breakout, swing, grid/DCA, pairs, event, ML;
  - manifest schema; registry; multi-timeframe helpers.
- [ ] **M11 risk manager:**
  - policy model at global, venue, strategy, instrument and portfolio levels;
  - sizing models;
  - pre-trade checks (incl. DQ status and event blackout);
  - kill switch;
  - dead-man's switch;
  - change control (tighten instantly / loosen with Telegram + TOTP);
  - hard-ceiling file;
  - audit.
- [ ] **M12 engine wrapper:** Nautilus sandbox/paper on testnets/practice accounts. Custom **Alpaca, OANDA and IG** adapters.
- [ ] **M7 lab:**
  - fast screener + Nautilus truth backtests using **measured costs from M16**;
  - validation suite (walk-forward, purged CV, MC permutation, bootstrap Sharpe, deflated Sharpe);
  - vendored freqtrade look-ahead/recursive analysers;
  - Optuna;
  - MLflow tracking.
- [ ] **M6 core features:** TA-Lib, Alpha158, microstructure; IC evaluator.
- [ ] **Sandboxed LLM strategy generator.**
- [ ] **M21 Decision One tier A:**
  - train → calibrate → compile (ONNX/Treelite) → in-process runtime;
  - latency benchmark (target < 50 µs);
  - MLflow model registry.
- [ ] **M15 web UI v1:** strategy builder/registry, backtest viewer, risk-policy editor, positions, manual trade ticket. **Telegram bot v1:** alerts, `/kill`, `/status`, `/pause`.

**Demo:** you create any strategy type on any timeframe (template, code or "describe it"), backtest it with realistic costs, validate it, and run it on paper behind the risk manager.

## Phase 3 — Journal & tax (weeks 12–15)
- [ ] **M18 journal ingestion:** Nautilus fills, ccxt ledgers (funding, fees, transfers), broker statements (IBKR Flex, OANDA, IG), and on-chain events.
- [ ] **FX service:** RBA for AUD; reputable exchange rate for crypto; source recorded per event.
- [ ] **Lot engine:** specific-ID → FIFO; FX-cash lots (Div 775); Decimal.
- [ ] **Rules plugins:**
  - **AU_2026** plugin plus golden tests from ATO examples;
  - PAYG-instalment estimator;
  - wash-sale flags;
  - myTax worksheet.
- [ ] **AU_2027_REFORM** scaffolding plus the **30 June 2027 snapshot job**.
- [ ] **Residency timeline**, with AE/EG/CY/GENERIC plugin stubs.
- [ ] **Trading-journal UI:** per trade, with strategy, signal, chart snapshot, notes and tags.
- [ ] **Exports:**
  - Beancount (+ Fava) export;
  - accountant pack;
  - daily reconciliation journal ↔ venues.
- [ ] Log the tax-agent questions as tasks ([09](09-journal-and-tax.md#questions-for-your-tax-agent-tracked-as-tasks)).

**Demo:** every paper trade, fee and funding payment appears automatically in the journal; an FY-to-date AU tax summary and PAYG estimate are generated.

## Phase 4 — News, social, events & calendars (weeks 16–19)
- [ ] **News:** RSS + trafilatura/crawl4ai; **RSS-Bridge** sidecar (whitelist, auth, internal network); GDELT.
- [ ] **Social:**
  - Telegram (Telethon + Bot API + RSS-Bridge fallback);
  - Discord bot on followed announcement channels;
  - Bluesky Jetstream; Mastodon;
  - StockTwits/YouTube conditional.
- [ ] **Text processing:** local-LLM relevance gate → entity linking → FinBERT → embeddings (TEI) → `document`.
- [ ] **M9 document RAG** (`rag` schema):
  - hybrid pgvector + tsvector with RRF;
  - rerank;
  - point-in-time filter;
  - filing/news chunking;
  - retrieval benchmarks.
- [ ] **Events:** USGS, GDACS, NOAA/NHC, FIRMS, ReliefWeb, UCDP, OpenSanctions, Kalshi/Polymarket + exposure map.
- [ ] **Calendars:** FRED release dates, ForexFactory weekly JSON, central-bank schedules, earnings/IPOs. Blackout windows feed M11.
- [ ] **Features:** retail positioning (Myfxbook, IG, OANDA books), nowcasts, Fed-path probabilities, VIX regime.

**Demo:** a morning Telegram brief covering news, sentiment movers, global events mapped to assets, today's calendar with risk blackouts, and data/cost health.

## Phase 5 — Airdrops, launches & curation queue (weeks 20–23)
- [ ] **M19 task queue:** Telegram Done/Skip/Snooze/Details/Never; daily and weekly digests.
- [ ] **M19 community curation:** Discord servers + announcement channels to follow, Telegram channels, Galxe spaces.
- [ ] **M4 discovery:** DefiLlama tokenless protocols, CryptoRank, CoinGecko, DexScreener, Galxe (read-only), Snapshot/forums, Discord inbox.
- [ ] **M4 risk scoring:**
  - GoPlus, RugCheck, Honeypot.is;
  - blocklists;
  - re-implemented solana-rugchecker + CRPWarner heuristics;
  - evaluation on the SoK dataset.
- [ ] **Viability scoring:** includes AU geo/KYC exclusion.
- [ ] **Hot-wallet claim executor:**
  - signed mandates;
  - Tenderly/`simulateTransaction` pre-checks;
  - caps;
  - approval revokes/sweeps.
- [ ] **Airdrop/staking income** goes to the journal with tax classification.

**Demo:** a weekly digest of vetted airdrops/launches with step-by-step tasks; eligible claims executed automatically on the hot wallet with simulation proof; scams rejected with reasons.

## Phase 6 — AI decision layer, memory & anomalies (weeks 24–28)
- [ ] **M8 decision graph:** LangGraph debate graph (TradingAgents-derived) with FinRobot valuation tools and a macro/events analyst; structured `Signal` with provenance.
- [ ] **M9 memory:**
  - **Hindsight** self-hosted (slim, our Postgres schema, TEI embeddings/rerank, LLM via gateway);
  - memory banks;
  - decision settlement + reflection;
  - point-in-time recall.
- [ ] **M21 tier B advisor:**
  - Qwen3.5-4B on vLLM (GPU) or llama.cpp (CPU);
  - JSON-schema flags to NATS KV;
  - timeout fallback.
- [ ] **M21 distillation loop:** teacher log (M8) + outcomes → tier A retrain / tier B LoRA → calibration → gated promotion; teacher in shadow.
- [ ] **Optional:** LightRAG graph over filings (offline).
- [ ] **M10:** anomaly detectors + explain agent.
- [ ] **LLM-signal strategy template** (M0) consuming M8 signals.
- [ ] **Evaluation and cost:** evaluate on post-training-cutoff data; LLM cost cap and spend panel; every call audited.
- [ ] **Optional:** Hummingbot MM sidecar; MiroFish/OASIS crowd-sim experiment.

**Demo:** ask for an analysis of any instrument and get a sourced signal; anomalies are explained on Telegram; LLM-signal strategies run on paper.

## Phase 7 — Prove it, then go small-live (months 7–10+)
- [ ] Your strategies run in paper/approve mode for the configured period (default ≥ 3 months).
- [ ] **Weekly review:**
  - paper vs backtest tracking error;
  - realised vs modelled costs;
  - DQ incidents;
  - journal reconciliation.
- [ ] Promote strategies that pass the [gates](03-build-spec.md#8-promotion-gates-per-strategy-configurable) to small live allocations, using separate live sub-accounts with withdrawals disabled.
- [ ] MT5 bridge / cTrader / Saxo adapters if needed.

## Phase 8 — MCP control plane (last; only if you want it)
- [ ] **`mt_mcp` adapter over `mt_api`:** read & analyse, talk to agents, trade & adjust positions, strategies, risk, curation. See [build spec M20](03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted).
- [ ] **Safeguards:**
  - MCP orders default to approve mode;
  - loosening risk needs Telegram + TOTP;
  - withdrawals/keys/mandates are never exposed;
  - full audit.

**Demo:** from Claude, "how are my strategies doing, tighten BTC max position to X, and close half my EURUSD", with the order confirmed on Telegram.

## Standing rules
- **Platform first, strategies second.** The system never hard-codes a trading style or timeframe.
- **Paper first, always.** Live keys have no withdrawal rights and tiny caps at first.
- **Tests:** nothing merges without passing them. The point-in-time, risk-manager and tax golden tests are mandatory.
- **Vendored code:** review every third-party bump (diff for telemetry, referral IDs, network calls).
- **Monthly upkeep:**
  - check data-source API/ToS changes;
  - rotate keys every 90 days;
  - run a restore test.
