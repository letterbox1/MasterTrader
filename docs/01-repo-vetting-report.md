# MasterTrader — Open-Source Trading Repo Vetting Report

_Date: 2026-10-21. Method: every repo was shallow-cloned and its code read (nothing was executed or installed), followed by web research (GitHub pages, PyPI, papers, blogs, press). Star counts come from github.com pages on 2026-10-21 (the GitHub REST API was blocked from the research environment). Reddit and Hacker News were mostly unreachable, so "community reputation" leans on blogs, papers, issues and press. Anything marked **(U)** could not be independently verified._

---

## 1. TL;DR verdicts

| # | Repo | License | Stars | Last commit | What it is | Verdict |
|---|---|---|---|---|---|---|
| 1 | [HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading) | MIT | ~36.1k | 2026-10-20 | LLM research agent → strategy code → multi-market backtester → 19 broker connectors | **Borrow components** (research/strategy layer) |
| 2 | [AI4Finance-Foundation/FinRobot](https://github.com/AI4Finance-Foundation/FinRobot) | Apache-2.0 + NOTICE + trademark policy | ~8.3k | 2026-09-28 | Multi-agent equity research & valuation (DCF/DDM/LBO/comps) | **Borrow components** (valuation desk) |
| 3 | [hummingbot/hummingbot](https://github.com/hummingbot/hummingbot) | Apache-2.0 | ~20.6k | 2026-09-22 | Crypto market-making / arbitrage bot framework, 47 connectors, DEX via Gateway | **Adopt as a module** (market making, long-tail crypto venues) |
| 4 | [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) | Apache-2.0 | ~112k | 2026-10-16 | LangGraph multi-agent "trading firm": analysts → bull/bear debate → trader → risk debate → PM | **Borrow pattern + components** (AI decision layer) |
| 5 | [freqtrade/freqtrade](https://github.com/freqtrade/freqtrade) | **GPL-3.0** | ~55.7k | 2026-10-20 | Crypto directional bot: candles, hyperopt, FreqAI ML, FreqUI | **Reference only** (or run unmodified as a separate service) |
| 6 | [nautechsystems/nautilus_trader](https://github.com/nautechsystems/nautilus_trader) | LGPL-3.0 (+CLA) | ~30.4k | 2026-10-21 | Rust/Python event-driven, multi-asset, production engine with order-book-level backtesting | **Adopt as CORE engine** |
| 7 | [NoFxAiOS/nofx](https://github.com/NoFxAiOS/nofx) | **AGPL-3.0** | ~13.1k | 2026-10-20 | Go "AI trading OS": LLM → JSON → crypto perp orders | **Avoid the code; borrow ideas** (hidden fees + default-on telemetry) |
| 8 | [VibeTradingLabs/vibetrading](https://github.com/VibeTradingLabs/vibetrading) | "MIT" in pyproject only — **no LICENSE file** | ~102 | 2026-03-23 | Small crypto prompt→strategy→DEX-perp library | **Avoid** (redundant, unsafe, unlicensed in practice) |
| + | [666ghj/MiroFish](https://github.com/666ghj/MiroFish) | **AGPL-3.0** | ~80.9k | 2026-10-02 | Swarm social-simulation "prediction engine" on CAMEL-AI OASIS + Zep Cloud | **Reference only / sandboxed experiment** |
| + | [simplifaisoul/osiris](https://github.com/simplifaisoul/osiris) | MIT | ~11.2k | 2026-10-20 | OSINT world-map dashboard (GDELT, USGS, GDACS, FIRMS…) | **Reference only; lift small pieces** (memecoin promo, unreviewable binaries) |

### Redundancy calls

- **VibeTradingLabs/vibetrading is fully redundant** next to HKUDS/Vibe-Trading. The two are **unrelated projects that happen to share a name**: separate histories and authors, no shared code. It isn't a fork or a squat; VibeTradingLabs actually published the name on PyPI first, in May 2025. HKUDS does everything it does, with far better safety and backtest realism. Its only unique asset is a set of DEX-perp adapters (Paradex, Lighter, Aster, Extended), and ccxt / Nautilus / official SDKs cover those better.
- **freqtrade is redundant *as an engine*** next to NautilusTrader. Nautilus does crypto directional trading with more realistic fills, and handles every other asset class too. freqtrade's unique value is its research tooling: look-ahead/recursive-bias analysers, hyperopt, FreqAI and FreqUI. Re-implement those ideas; GPL blocks importing the code.
- **nofx is redundant** next to Nautilus + Hummingbot (execution) and TradingAgents (LLM reasoning). It also carries serious trust problems. Keep only its "Frontier mode" idea.
- **Hummingbot is NOT redundant.** It's the only repo with mature market-making, cross-exchange arbitrage and AMM liquidity-provision strategies, plus long-tail CEX/DEX venues that Nautilus lacks. Its *backtester* is redundant.
- **TradingAgents and FinRobot are complementary, not redundant.** TradingAgents is the investment committee (debate → decision); FinRobot is the valuation desk (deterministic DCF/WACC/comps and SEC XBRL).
- **MiroFish and osiris are each unique in their niche** (crowd-reaction simulation; event map), but neither is production-grade.

---

## 2. License matrix — what you can actually do

| License | Repos | Import into our codebase? | Run as separate service? | Key obligation |
|---|---|---|---|---|
| MIT | Vibe-Trading, osiris | ✅ | ✅ | Keep copyright notice. Vibe-Trading bundles Qlib factors under Apache-2.0, so keep its NOTICE too. |
| Apache-2.0 | FinRobot, TradingAgents, Hummingbot | ✅ | ✅ | Keep NOTICE. **FinRobot's trademark policy bans "FinRobot" in our product name**; "Built on FinRobot" is fine. |
| LGPL-3.0 | NautilusTrader | ✅ as a pip/crate dependency, unmodified | ✅ | Changes *to Nautilus itself* must be published if distributed. Statically linking its Rust crates into our binary is a grey area. No network clause. A CLA gives Nautech Systems sub-licensable rights to contributions (single-vendor control). |
| GPL-3.0 | freqtrade | ❌ importing or copying makes the whole platform GPL once distributed | ✅ unmodified, over its REST API | No network clause, so hosting it creates no obligation. |
| AGPL-3.0 | nofx, MiroFish | ❌ | ⚠️ only if any modifications are published (network clause) | Clean-room re-implementation is the safest route. |
| None (de facto) | VibeTradingLabs/vibetrading | ❌ no LICENSE file = no grant | — | Ask the maintainers for a LICENSE before reusing any code. |

**Recommended platform license posture:** keep the MasterTrader core permissive or proprietary. Depend on Nautilus as an unmodified LGPL dependency, behind our own wrapper package. Copy/port only MIT/Apache code (Vibe-Trading, TradingAgents, FinRobot, Hummingbot connectors, osiris snippets). Treat GPL/AGPL projects as **external processes behind an API boundary**, or re-implement their ideas clean-room.

---

## 3. Per-repo deep dives

### 3.1 NautilusTrader — the core engine
- **Architecture:** a deterministic, event-driven kernel; the *same* code runs backtest and live (parity). It is migrating from Cython v1 to a Rust core + Python layer (v2.0.0rc8; `MIGRATION_V2.md`). About 2.19M lines of Rust and 121k of Python, about 31k Rust plus 2.5k Python tests, and 12 CI workflows (CodeQL, OpenSSF, audit, perf, nightly). Releases ship every 2–3 weeks.
- **Asset model:** `AssetClass` covers FX, Equity, Commodity, Debt, Index, Crypto and Alternative. Instruments include equities, futures, options, spreads, CFDs, perps, betting and synthetics.
- **Adapters:**
  - Trading: Interactive Brokers, Binance, Bybit, OKX, Coinbase, Kraken, Deribit, dYdX, Hyperliquid, Lighter, Derive, Architect AX, Polymarket, Betfair.
  - Data-only: Databento, Tardis, CoinAPI.
  - **Interactive Brokers is the multi-asset gateway** (stocks, ETFs, options, futures, FX, bonds, metals, CFDs).
- **Best-in-class backtesting:** L1/L2/L3 order-book replay with queue-position tracking, and pluggable fill/fee/latency models (`crates/execution/src/models/`).
- **Gaps (by design, `ROADMAP.md`):** no UI, no built-in ML or optimisation, no distributed backtesting. No OANDA / MT5 / Alpaca adapters.
- **Risks:**
  - API churn: `RELEASES.md` has 148 lines mentioning "breaking", and v2 currently lacks custom-data support in BacktestNode.
  - Steep learning curve.
  - Single-vendor control.
- **Mitigation:** pin a release and wrap it behind an internal `mt_engine` interface.

### 3.2 Hummingbot — crypto market-making module
- **Scope:** 27 spot and 20 perp connectors; DEX AMMs/CLMMs via the separate Gateway service.
- **Strategies:** pure market making, Avellaneda-Stoikov, cross-exchange MM, plus V2 executors (grid, DCA, TWAP, arbitrage, LP).
- **Weak backtester:** about 2.3k lines, candles only, no order book or latency.
- **⚠️ Telemetry on by default:**
  - `anonymized_metrics_mode` (`client_config_map.py:845`) reports trade volume every 15 minutes to `api.coinalpha.com` (`connector_metrics_collector.py:29`).
  - **Disable it.**
- **⚠️ Monetisation:**
  - Hardcoded broker IDs earn exchange rebates (e.g. Binance `x-MG43PCSN`).
  - Sponsor referral links.
  - Governance runs through the HBOT token.
  - Decide whether to keep or strip the broker IDs.
- **Reality check:** MM loses in trending markets; Hummingbot's own academy documents losing runs.

### 3.3 freqtrade — reference only
- **Scope:** crypto only (ccxt), candle-based backtests.
- **Its own docs state fills happen at the requested price with no slippage**, and there's no latency model.
- **Strengths to replicate:**
  - `lookahead-analysis` and `recursive-analysis`.
  - Hyperopt with many loss functions.
  - FreqAI (LightGBM, XGBoost, PyTorch, transformer, RL).
  - FreqUI, Telegram control, REST API.
- **Main community complaint:** hyperopt overfitting (issues #7190, #5612; one write-up reports −40% out-of-sample).
- **No telemetry found.** One OKX broker ID is hardcoded.

### 3.4 HKUDS/Vibe-Trading — research and strategy-generation layer
- **Stack:** LangGraph agent, FastAPI, MCP server, CLI, React UI. About 508k lines of Python, roughly 231k of them tests across 908 test files.
- **Data:** about 45 data loaders with fallback chains (yfinance, Stooq, akshare, CCXT, EDGAR, Tushare…), China-leaning by default.
- **Strategy generation:** the LLM writes a `SignalEngine` class, often from 90 skills or a factor zoo (alpha101, GTJA191, Qlib158).
- **16 market engines:**
  - A-shares, global, India, Korea, Vietnam and Brazil equities.
  - CN and global futures, which covers commodities.
  - Crypto perps (with funding and liquidation).
  - **Forex including metals** (with spreads and swaps).
  - Options, plus a composite engine.
  - Bonds: analytics only.
- **Backtest hygiene:**
  - Signals are shifted one bar and fill at the next bar's open plus slippage.
  - `validation.py` runs Monte Carlo permutation, bootstrap Sharpe CI and walk-forward analysis.
- **Live trading:**
  - 19 connectors (Alpaca, IBKR, Binance, OKX, MT5, Zerodha, Futu, Tiger, Robinhood, Trading212, Upbit…).
  - **Default-deny order guard** (`agent/src/live/order_guard.py`): mandates, kill switch, notional and leverage caps, audit log, no auto-retry. This is the best LLM-to-live safety design among the repos.
- **⚠️ Code execution risk:** LLM-written strategy code runs **in-process** with only a denylist (`backtest/runner.py`). The agent also has a shell tool. Run it in a credential-less sandbox.
- **Memory:** file-based plus optional SQLite FTS, not vector RAG.
- **Reputation:** big star count, little independent quant review. The README warns that a "$VIBE"-style token and an X account are fake.

### 3.5 VibeTradingLabs/vibetrading — avoid
- **Size and activity:** about 9.5k lines of Python, dormant for about 7 months, commit author looks agent-generated.
- **Likely 1-bar look-ahead:** it uses the close of the still-open bar (`_core/static_sandbox.py` ~365–396).
- **Raw `exec()` of LLM output** in both the backtest (`_core/backtest.py:513`) and **live** (`_core/live_runner.py:180`), in the same process as the wallet private key.
- **Weak cost model:** flat 0.1% fee, slippage off, and a silent 30k-step cap.
- **License:** none (no LICENSE file).

### 3.6 TradingAgents — AI decision layer pattern
- **Pipeline:**
  - Market, sentiment, news and fundamentals analysts.
  - Bull/bear researchers debate; a Research Manager judges.
  - A Trader writes a proposal; aggressive, conservative and neutral risk analysts debate it.
  - A Portfolio Manager decides.
  - Outputs are structured Pydantic models; cheap models serve the workers and strong models the managers.
- **Best ideas to steal:**
  - Strict **point-in-time data enforcement**, with tests (`test_tool_date_enforcement.py`, `test_social_lookahead.py`, `test_memory_pointintime.py`).
  - **Decision settlement + reflection memory:** past calls are scored against realised 5-day alpha and the LLM writes a lesson.
  - Vendor-fallback data router.
  - Broker/MT5-style symbol normalisation covering FX, metals, energy and crypto (`dataflows/symbols.py`).
- **Limits:** no execution, no fees or sizing in `backtest.py`, and LLM training-data contamination is unaddressed.
- **Disputed claims:**
  - One recomputation finds the paper's AAPL buy-and-hold baseline wrong: −5.23% in the paper vs +9.12% recomputed ([dev.to](https://dev.to/trow126/the-most-starred-llm-trading-paper-claims-buy-and-hold-lost-523-it-actually-gained-912-1jj6)).
  - "The Alpha Illusion" (arXiv 2605.16895) reportedly finds it underperforms buy-and-hold after costs **(U)**.
- **Cost:** 10–20+ LLM calls per ticker-date.

### 3.7 FinRobot — valuation desk
- **Three generations:** V0 AutoGen (educational; runs LLM code **unsandboxed**, so avoid it), V1 FastAPI reports, V2 PydanticAI desktop app (production-grade: `mypy --strict`, 176 unit-test files).
- **Best part:** about 32 deterministic valuation operators (`engine/compute/operators/`: DCF, WACC, Monte Carlo, SOTP, audit checks). The principle is "models reason, code computes", and every number carries provenance.
- **Data:** SEC EDGAR / XBRL ingestion and validation.
- **Limits:**
  - US equities only.
  - Its backtester assumes zero commission and slippage (`backtrader_adapter.py:191`).
  - The browser-mode API is unauthenticated.

### 3.8 nofx — avoid the code
- **How it trades:** Go + React. The LLM returns JSON (symbol, action, leverage, size, SL, TP, confidence), broken JSON gets repaired, and it places orders on Binance, OKX, Bitget, Bybit, Gate, KuCoin, Hyperliquid, Aster or Lighter.
- **Coverage:** crypto perps only; no backtester.
- **Weak risk controls:** leverage, R:R, confidence and daily-loss limits are **prompt hints, not enforced**, and there's no kill switch.
- **Good:** AES-256-GCM key encryption, bcrypt passwords, refuses to start with a weak JWT secret.
- **Bad:**
  - **Default-on Google Analytics telemetry of every fill** (symbol, USD size, leverage, user ID). It's off only with `EXPERIENCE_IMPROVEMENT=false`, which isn't in `.env.example`.
  - **A forced Hyperliquid builder fee of +0.05% per order** (trading is blocked until you approve it).
  - **A base64-obfuscated OKX broker tag.**
  - Broker/referral IDs on Binance, Bitget, Bybit and Gate; a KuCoin partner secret.
  - The production compose file binds 0.0.0.0, and **the first registrant owns the instance**.
  - The wallet key sits in plaintext `.env`; the installer is `curl | bash` pulling `:latest` images.
- **Reputation:**
  - A December 2025 equity/IP dispute between its developer, an early participant and its incubator.
  - Older READMEs advertised a "contributor airdrop".
  - The viral "AI trading contest" was Nof1's *Alpha Arena*, a separate project (4 of 6 models lost money).
- **Worth copying (clean-room):** its **Frontier mode**, where the LLM proposes a plan, deterministic code checks fees, R:R and size, and a human approves each order.

### 3.9 MiroFish — crowd-reaction simulator (experimental only)
- **What it is:** a wrapper around CAMEL-AI **OASIS** (Apache-2.0) and **Zep Cloud** (mandatory, no local fallback). Flask backend about 30.7k lines, Vue frontend about 21k.
- **Flow:**
  1. Documents go into a knowledge graph.
  2. An LLM writes personas.
  3. Agents post on simulated Twitter/Reddit for about 72 rounds.
  4. A ReportAgent writes the "prediction".
- **Not a forecaster:**
  - No calibration, accuracy record or backtest.
  - Non-deterministic: unseeded randomness and temperature 0.3–0.7.
  - Historical tests are contaminated by LLM hindsight.
  - Runs consume many tokens.
- **Anecdote:** one modified fork reportedly made 338 Polymarket trades for +$4,266, with an edge on political markets and none on financial ones **(U)**.
- **Security:**
  - No API auth and CORS `*`.
  - Default secret key `mirofish-secret-key`.
  - No eval of LLM output and no telemetry.
- **Popularity:** the star spike is consistent with viral press in March 2026 (a student's 10-day build, reportedly ~30M RMB invested), not star-farming.
- **Use:** an isolated private service fed by our event store, its output only a *candidate feature* tested over many runs on events after the model's training cutoff. **Long term:** rebuild on OASIS (Apache) with a local LLM and our own memory.

### 3.10 osiris — reference only
- **What it is:** a Next.js map dashboard, not a data pipeline, and it keeps no event history.
- **Free feeds:** USGS, GDELT 2.0, GDACS, NASA EONET/FIRMS, NWS, NOAA SWPC, OpenSky, OpenSanctions, Polymarket, Manifold.
- **"Conflict zones" are 15 hardcoded places**, and "country risk" is an editorial ordering.
- **Red flags:**
  - A **$OSIRIS Solana memecoin panel** in the main UI.
  - **Committed `.pyc` without source.**
  - A tutorial for evading CelesTrak rate limits.
  - Vendored `node_modules`.
  - Offensive tools (port scanner, infostealer-leak lookups).
- **Lift (MIT):** the GDELT reader, the SSRF guard and the prediction-market fetchers.
- **Better:** ingest the underlying feeds directly into our own timestamped store.
- **Alternative:** koala73/worldmonitor (~89k★) is the established dashboard but **AGPL**.

---

## 4. Capability crossover map

| Capability | Best source | Runner-up | Notes |
|---|---|---|---|
| Multi-asset execution and live trading | **Nautilus** (via IBKR) | Vibe-Trading connectors | Nautilus for fidelity; Vibe-Trading's Alpaca/MT5/OANDA-style connectors fill gaps |
| High-fidelity backtest (order book, latency) | **Nautilus** | — | Others are all candle-based |
| Fast candle backtest across many markets | **Vibe-Trading** engines | freqtrade (crypto) | Vibe-Trading models FX swaps, metals and futures rules |
| Market making / arbitrage / DEX LP | **Hummingbot** | Nautilus (DIY) | Disable telemetry |
| Look-ahead / bias detection | **freqtrade** (idea) + **TradingAgents** tests | Vibe-Trading validation | Re-implement freqtrade's ideas (GPL) |
| Strategy robustness (Monte Carlo, walk-forward) | **Vibe-Trading** `validation.py` | freqtrade hyperopt | Watch for hyperopt overfit |
| ML / feature models | freqtrade FreqAI (idea), **Qlib** | FinRL | |
| LLM-generated strategies | **Vibe-Trading** | VibeTradingLabs (worse) | Sandbox the generated code |
| LLM multi-agent decision | **TradingAgents** | FinRobot V2 debate, nofx | |
| Fundamental valuation | **FinRobot V2** | — | US equities |
| LLM→order safety rails | **Vibe-Trading** order guard + nofx Frontier (idea) | — | Default-deny plus human approval |
| Crowd / narrative simulation | **MiroFish** (idea, on OASIS) | — | Experimental |
| Global event map | osiris / worldmonitor (ideas) | — | Build our own ingestion |
| Memory and reflection | **TradingAgents** settlement + **Hindsight** | Vibe-Trading FTS | |

---

## 5. Supporting ecosystem — recommended free/open picks

**Market data**
- **Multi-provider normaliser:** **OpenBB Platform**. Its license is now Apache-2.0 per its LICENSE file and PyPI 5.0.0. ⚠️ The repo currently resolves under an unusual org (`openbq-org/OpenBB`); verify provenance before pinning.
- **Crypto:** **ccxt** (MIT).
- **Macro:** **FRED/ALFRED**; its vintages give point-in-time data with no look-ahead.
- **Filings / 13F / Form 4:** **SEC EDGAR via edgartools** (MIT).
- **Government data:** US Treasury, BLS, EIA (energy and commodities), USDA, CFTC COT, World Bank, IMF, ECB.
- **Crypto market and on-chain:** CoinGecko, DefiLlama.
- **FX ticks:** Dukascopy historical.
- **Tick-quality data:** Databento's one-off $125 credit.
- **Free tiers are tiny:** Twelve Data 800 credits/day, FMP 250/day, Alpha Vantage ~25/day (U). **Stooq now needs an API key.**

**Brokers / paper trading**
- **alpaca-py** (US stocks, ETFs and crypto; paper).
- **ib_async** (IBKR; ib_insync is archived).
- **OANDA v20 practice** (FX and metals).
- **MetaTrader5** (Windows-only).
- **ccxt testnets.**
- **Hyperliquid SDK** (US persons restricted (U)).

**News, social and sentiment**
- RSS plus **trafilatura** / **crawl4ai** (Apache-2.0) for article text.
- **FinBERT** / FinGPT for sentiment.
- **GDELT** for global news volume and tone.
- **Polymarket Gamma API** (no auth) for event probabilities.

**Geopolitical and disasters**
- GDELT 2.0, USGS, GDACS, NOAA/NWS/NHC, NASA FIRMS, ReliefWeb and UCDP: all public and free.
- **ACLED's 2025 terms require a corporate license for commercial use and restrict AI/LLM use.**

**Memory and RAG**
- **Hindsight** (vectorize-io, MIT, ~52k★): agent memory of facts, experiences and mental models on Postgres + pgvector.
- **LightRAG** (MIT) for the filings graph.
- mem0 and Graphiti as alternatives. Zep Community Edition is deprecated.

**Storage**
- **Postgres + pgvector + TimescaleDB.** Timescale's compression and continuous aggregates are under the TSL license: free to self-host, but you can't sell it as a managed DB.
- **DuckDB / Parquet** for research.
- Avoid **ArcticDB** (BSL 1.1) if you might ever offer a hosted service.

**Quant libraries**
- **Qlib** (MIT) for factor and ML research.
- **skfolio** / **Riskfolio-Lib** for portfolio construction.
- **alphalens-/pyfolio-/empyrical-reloaded** and **quantstats** for analytics.
- **TA-Lib** for indicators.
- **Chronos / TimesFM / Kronos** time-series models for volatility and volume features (check each model's weights license).

**Orchestration**
- **LangGraph** (MIT), **Prefect** (Apache-2.0).
- **NATS JetStream** or **Valkey** (BSD; prefer it over Redis 8's tri-license).
- **Grafana** (AGPL; fine unmodified).

### License / ToS landmines

- **vectorbt is Apache-2.0 + Commons Clause.** You can't sell services whose value derives from it, and active development has moved to the paid PRO version.
- **AGPL:** Firecrawl server (use crawl4ai instead), backtesting.py, worldmonitor, nofx, MiroFish.
- **GPL:** freqtrade, Lumibot.
- **Proprietary:** kalshi-python.
- **Personal / non-commercial terms only:** Yahoo (so yfinance and Qlib's prebuilt dataset), and the free tiers of CoinGecko Demo, Etherscan, Finnhub and Polygon/Massive. The Reddit API now needs manual approval (U).
- **Scraping explicitly prohibited:** X/Twitter via twscrape or twikit, Discord self-bots, and ForexFactory / Investing.com calendars.
- **Dead, archived or moved:**
  - Gone or unusable: snscrape, pandas-ta (repo 404, so use `pandas-ta-classic` or `ta`), the StockTwits API.
  - Archived: pytrends (April 2025), Polymarket's `py-clob-client`, ib_insync.
  - Telethon: moved to Codeberg.
  - Stale: backtrader (no pushes since 2024-08), zipline-reloaded (maintenance mode).
  - Dune: free plan reportedly cut to view-only (U).
- **Gaps with no maintained OSS project:** airdrop, ICO and token-launch trackers; a free economic-calendar API. We build these ourselves (Section 6).

---

## 6. Proposed v1 architecture (summary)

See [`02-v1-architecture.md`](02-v1-architecture.md) for the full build scope.

```
             ┌─────────────── Ingestion (Prefect flows) ──────────────────────────────┐
 Market:     ccxt · OpenBB · FRED/ALFRED · EDGAR(edgartools) · Treasury/EIA/CFTC · Dukascopy · Databento
 Social/News: RSS+trafilatura/crawl4ai · Reddit(approved API) · Telegram(Telethon) · GDELT · Polymarket
 Events:     USGS · GDACS · NOAA/NHC · NASA FIRMS · ReliefWeb · UCDP (· ACLED if licensed)
 Crypto alt: CoinGecko new listings · DefiLlama · on-chain → airdrop/ICO tracker (built in-house)
             └──────────────────────────┬──────────────────────────────────────────────┘
                                        ▼  (all point-in-time, timestamped, archived)
          Postgres + TimescaleDB (bars, events) · Parquet/DuckDB (research) · pgvector
                                        │
     ┌────────────────┬─────────────────┼──────────────────┬───────────────────────┐
     ▼                ▼                 ▼                  ▼                       ▼
 Feature/Signal   Research Lab      AI Decision        Memory/RAG              Anomaly monitor
 Qlib factors,   Vibe-Trading-     TradingAgents-     Hindsight + LightRAG    z-score/IsolationForest
 FinBERT, TA,    style LLM          style debate       (decision settlement +  on prices, volumes,
 Chronos vol,    strategy gen       graph + FinRobot   reflection, filings)    sentiment, event spikes
 event scores    (sandboxed),       valuation tools
                 walk-forward/MC                       (MiroFish-style crowd sim: optional sidecar)
     └────────────────┴──────────┬──────┴──────────────────┘
                                 ▼
                 Risk & Order Guard (deterministic, default-deny:
                 mandates, kill switch, caps, human approval tier)
                                 ▼
          NautilusTrader core (backtest = sim = live)  ── Hummingbot sidecar (MM/DEX)
          IBKR · Binance/Bybit/OKX/Hyperliquid · (custom) Alpaca · OANDA · MT5
                                 ▼
               Grafana + web UI · audit log · Telegram alerts
```

---

## 7. Sources (selection)

- Repos: the ten GitHub URLs in Section 1; https://github.com/koala73/worldmonitor; https://github.com/vectorize-io/hindsight
- Papers:
  - TradingAgents arXiv [2412.20138](https://arxiv.org/abs/2412.20138)
  - FinRobot [2405.14767](https://arxiv.org/abs/2405.14767), [2411.08804](https://arxiv.org/abs/2411.08804)
  - "Alpha Illusion" [2605.16895](https://www.alphaxiv.org/abs/2605.16895) (U)
- Critiques and reviews:
  - https://dev.to/trow126/the-most-starred-llm-trading-paper-claims-buy-and-hold-lost-523-it-actually-gained-912-1jj6
  - freqtrade issues [#7190](https://github.com/freqtrade/freqtrade/issues/7190), [#5612](https://github.com/freqtrade/freqtrade/issues/5612)
  - https://docs.hummingbot.org/academy-content/top-beginner-misconceptions-about-market-making/
  - https://forklog.com/en/four-out-of-six-ai-models-suffer-losses-in-trading-tournament/
  - https://en.jiemian.com/article/13592098.html
  - https://eu.36kr.com/en/p/3715147673006213
  - https://bullalert.ai/blog/best-python-backtest-engines-2026/
  - https://autotradelab.com/blog/nautilus-vs-vectorbt-vs-freqtrade-20-python-quant-trading-frameworks-compared
- Data / ToS:
  - https://databento.com/docs/faqs/usage-pricing-and-data-credits
  - https://acleddata.com/myacled-faqs
  - https://github.com/pydata/pandas-datareader/issues/1012

> **Disclaimer:** no published result for any of these systems shows durable, cost-adjusted, out-of-sample profitability. Treat every LLM trading claim as unproven until it survives walk-forward testing on post-training-cutoff data with realistic costs, followed by paper trading.
