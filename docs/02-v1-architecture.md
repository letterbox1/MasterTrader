# MasterTrader v1 — Build Scope & Architecture

Goal: one unified, self-hostable AI quant platform built from free and open-source parts plus free-tier APIs. It covers ingestion, research, backtesting, simulation, AI decision-making, anomaly detection and automated execution across asset classes. The component choices come from [`01-repo-vetting-report.md`](01-repo-vetting-report.md).

## Design principles

1. **Models reason, code computes, a deterministic guard decides whether anything trades.** No LLM output ever reaches a broker without passing hard-coded risk rules (taken from Vibe-Trading's order guard and nofx's Frontier mode, re-implemented).
2. **Point-in-time everything.** Every record carries `event_time` and `ingest_time`. Research and backtests may only read rows with `ingest_time ≤ simulated now` (the pattern from TradingAgents' date enforcement). Raw news and social snapshots are archived so backtests can be replayed.
3. **One engine for backtest, paper and live.** That engine is NautilusTrader, so a strategy is the same code at every stage.
4. **License firewall (only needed for a SaaS; for personal use see [03-build-spec §1](03-build-spec.md#1-what-personal-use-changes)).**
   - The core stays permissive (MIT/Apache).
   - Nautilus is an unmodified LGPL dependency behind our `mt_engine` wrapper.
   - GPL/AGPL tools (freqtrade, MiroFish, Grafana) run only as separate processes over an API, or get re-implemented clean-room.
5. **Sandbox all generated code.** LLM-written strategies run in a container with no network access and no credentials. They exchange signals only through a typed interface.
6. **Zero telemetry by default.** Strip or disable phone-home and broker-rebate tags from anything we vendor (Hummingbot metrics, broker IDs).

## Modules

| # | Module | Built from | v1 deliverable |
|---|---|---|---|
| M1 | **Ingestion** | Prefect + ccxt, OpenBB (Apache), FRED/ALFRED, edgartools, Treasury/BLS/EIA/CFTC, Dukascopy, CoinGecko/DefiLlama | Scheduled flows → TimescaleDB / Parquet with a point-in-time schema |
| M2 | **News & social** | RSS + trafilatura / crawl4ai, RSS-Bridge, Telegram (Telethon + Bot API), Discord (own bot + followed announcement channels), Bluesky, GDELT, Polymarket Gamma; Reddit/X deferred | Archived text store + FinBERT sentiment + entity/ticker linking |
| M3 | **Global events** | GDELT 2.0, USGS, GDACS, NOAA/NHC, NASA FIRMS, ReliefWeb, UCDP (ACLED only if licensed); ideas from osiris | Geo-tagged event table + an exposure map (event → country → assets: FX, commodities, indices) |
| M4 | **Crypto alt-data** | CoinGecko new listings, DefiLlama, DEX/on-chain feeds | In-house **airdrop / ICO / token-launch tracker** (no maintained OSS exists) |
| M5 | **Calendars** | FRED release calendar, agency schedules, EDGAR S-1/424B (IPOs) | In-house economic + IPO calendar |
| M6 | **Feature store** | Qlib factor zoo (Alpha158), TA-Lib, FinBERT, Chronos/TimesFM (volatility and volume) | Versioned features keyed by (instrument, time) |
| M7 | **Research lab** | Vibe-Trading-style LLM strategy generation (sandboxed), Vibe-Trading `validation.py` ideas (Monte Carlo permutation, bootstrap Sharpe, walk-forward), freqtrade-style look-ahead/recursive analysers (clean-room) | Prompt → strategy → backtest → robustness report |
| M8 | **AI decision layer** | TradingAgents debate graph (LangGraph) + FinRobot V2 valuation operators as tools | Structured signal `{instrument, direction, conviction, horizon, rationale, sources}` |
| M9 | **Memory / RAG** | Hindsight (MIT) on Postgres/pgvector + LightRAG for filings; TradingAgents decision settlement and reflection | Agents recall past decisions, outcomes and lessons |
| M10 | **Anomaly monitor** | Rolling z-scores, IsolationForest, change-point detection on prices, volumes, spreads, sentiment and event counts | Alerts + an "explain this anomaly" agent |
| M11 | **Risk & order guard** | Re-implemented from Vibe-Trading `order_guard` + nofx Frontier mode | Default-deny; mandates; notional, leverage and drawdown caps; kill switch; human-approval tier; audit log |
| M12 | **Execution core** | NautilusTrader (IBKR, Binance, Bybit, OKX, Hyperliquid…) + custom adapters for Alpaca, OANDA v20 and MT5 | Paper first, then live behind a config gate |
| M13 | **Market-making sidecar** | Hummingbot (telemetry off) | Optional crypto MM / arbitrage / DEX LP |
| M14 | **Crowd simulation (experimental)** | Clean-room on CAMEL-AI OASIS (Apache) with a local LLM; MiroFish as reference only | Scenario narratives as a *candidate* feature, never a direct signal |
| M15 | **UI & ops** | FastAPI + web UI, Grafana (unmodified), Telegram alerts | Dashboards, approvals queue, P&L, audit |

## Asset coverage plan

| Asset class | Data (free) | Execution |
|---|---|---|
| Crypto spot / perps | ccxt, CoinGecko, DefiLlama | Nautilus (Binance, Bybit, OKX, Hyperliquid…), Hummingbot |
| Stocks / ETFs | OpenBB providers, EDGAR, (yfinance for personal research only) | Alpaca paper (custom adapter), IBKR |
| Forex | Dukascopy history, OANDA practice, FRED | OANDA v20 (custom adapter), IBKR, MT5 |
| Commodities / metals | EIA, USDA, CFTC COT, futures via IBKR/Databento credit | IBKR futures, OANDA/MT5 CFDs |
| Bonds / rates | US Treasury, FRED/ALFRED, ECB | IBKR (bonds/futures); analytics first |
| IPOs | EDGAR S-1/424B, exchange calendars | IBKR / Alpaca after listing |
| ICOs / airdrops | M4 tracker | Watch-only in v1 |
| Prediction markets | Polymarket Gamma | Nautilus Polymarket adapter (optional) |

## Phased roadmap

1. **Phase 0 (foundations):** repo skeleton, Postgres/Timescale/pgvector via docker-compose, point-in-time schema, Prefect, M1 for crypto + US equities + FRED.
2. **Phase 1 (research loop):** Nautilus wrapper + backtests; M6 features; M7 lab with sandboxing, walk-forward and look-ahead analysers.
3. **Phase 2 (AI layer):** M8 debate graph + M9 memory + M2 news/sentiment + M3 events; signals evaluated only on post-model-cutoff data.
4. **Phase 3 (paper trading):** M11 guard + M12 paper connectors (Alpaca, OANDA practice, exchange testnets) + M15 UI/alerts. Minimum 3 months of paper trading.
5. **Phase 4 (expansion):** M4/M5 trackers, M10 anomaly agent, M13 Hummingbot, M14 crowd-sim experiment, then small live allocations behind the guard.

## Acceptance gates before any live capital

- Walk-forward and out-of-sample Sharpe after fees and slippage beat a buy-and-hold / equal-weight benchmark.
- Monte Carlo permutation p-value < 0.05.
- The look-ahead analyser is clean.
- LLM components are tested only on data after the model's training cutoff.
- The paper-trading P&L matches the backtest within tolerance.
- The kill switch and caps have been exercised in testing.
