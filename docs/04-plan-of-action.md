# MasterTrader — Plan of Action

Personal-use build, one developer plus AI pair-programming. Time estimates assume evenings and weekends; halve them if full-time. Each phase ends with a **demo you can actually use**, so the project is useful early and doesn't stall.

## Phase 0 — Foundations (week 1–2)
- [ ] Monorepo skeleton (`uv` workspace, packages per [build spec §3](03-build-spec.md#3-repository-layout)), ruff, mypy, pytest, pre-commit
- [ ] `docker-compose.yml`: Postgres 16 + TimescaleDB + pgvector, NATS, Prefect server, Grafana, Ollama
- [ ] `mt_core` types and `mt_store` schema + Alembic migrations, plus the `pit(as_of)` query helper and its tests
- [ ] `.env.example`, secrets in the keychain, Tailscale access, nightly `pg_dump` backup
- [ ] `third_party/LICENSES.md` manifest

**Demo:** `docker compose up` gives an empty but healthy stack with Grafana showing DB health.

## Phase 1 — Data backbone (week 3–5)
- [ ] ccxt crypto bars + funding (top 30 pairs)
- [ ] yfinance stocks/ETFs/futures/indices + Alpaca IEX
- [ ] Dukascopy/OANDA practice FX and metals
- [ ] FRED/ALFRED, Treasury curve, EIA, CFTC COT
- [ ] EDGAR via edgartools (filings, Form 4, 13F, S-1)
- [ ] Prefect schedules, data-freshness dashboard, gap detection

**Demo:** a Grafana board with live prices across all asset classes, and macro series updating.

## Phase 2 — Research lab (week 6–9)
- [ ] `mt_engine` Nautilus wrapper + data catalog export from `mt_store`
- [ ] Fast vectorised screener (Vibe-Trading engines / vectorbt)
- [ ] Validation suite: walk-forward, purged CV, MC permutation, bootstrap Sharpe CI, deflated Sharpe
- [ ] Vendor freqtrade look-ahead and recursive analysers (into `thirdparty_gpl/`)
- [ ] Features: TA-Lib, Qlib Alpha158, COT, macro surprises; IC evaluator
- [ ] Three baseline strategies (trend, mean-reversion, carry/FX) as benchmarks
- [ ] Sandboxed LLM strategy generator (Docker, no network, no secrets)

**Demo:** "Generate a strategy for X" turns into a validated Nautilus backtest report.

## Phase 3 — Text, events & memory (week 10–13)
- [ ] RSS + trafilatura/crawl4ai, Reddit API, Telethon, GDELT GKG
- [ ] Ticker/entity linking, FinBERT sentiment, local embeddings → `document`
- [ ] Event feeds (USGS, GDACS, NOAA/NHC, FIRMS, ReliefWeb, UCDP, OpenSanctions) + exposure map + event scores
- [ ] Hindsight + LightRAG integration
- [ ] Calendars (macro, earnings, IPO) and the crypto airdrop/ICO/listing tracker

**Demo:** a morning Telegram brief covering overnight news, sentiment movers, global events mapped to affected assets, upcoming calendar items, and new airdrops and listings.

## Phase 4 — AI decision layer (week 14–17)
- [ ] LangGraph debate graph (TradingAgents-derived) with a macro/events analyst
- [ ] FinRobot V2 valuation operators as tools
- [ ] Structured `Signal` output with provenance; decision settlement + reflection → Hindsight
- [ ] Evaluate signals on data after the model's training cutoff only; compare against the baseline strategies
- [ ] LLM cost tracking + monthly cap

**Demo:** daily signals on a watchlist, each with a rationale that links to its sources, plus a scorecard of past decisions.

## Phase 5 — Guard, paper trading & anomalies (week 18–21)
- [ ] `mt_guard`: mandates, caps, kill switch, approval flow (Telegram buttons), audit log
- [ ] Paper/testnet connectors: Nautilus (Binance/Bybit testnet, IBKR paper) + custom Alpaca and OANDA practice adapters
- [ ] Anomaly detectors + explain agent
- [ ] Streamlit/NiceGUI dashboard: signals, mandates, positions, approvals

**Demo:** the full loop in paper mode: data → signal → guard → paper order → P&L → settlement → reflection.

## Phase 6 — Prove it (months 6–9)
- [ ] Run paper/approve mode for ≥ 3 months
- [ ] Weekly review: paper vs backtest tracking error, signal hit rate, anomaly precision
- [ ] Kill or iterate strategies that fail the [live-capital gates](03-build-spec.md#8-live-capital-gates-per-strategy)

## Phase 7 — Small live + extras (month 9+)
- [ ] Small live allocations, only for strategies that passed the gates
- [ ] Hummingbot market-making sidecar (optional)
- [ ] MiroFish/OASIS crowd-sim experiment (optional)
- [ ] MT5 bridge if needed; extra venues

## Standing rules
- Paper first, always. Live keys live on a separate mandate with tiny caps.
- Nothing merges without tests passing; the point-in-time and guard tests are mandatory.
- Review every vendored third-party update (diff) before bumping its pinned commit.
- Monthly: check API/ToS changes on data sources (they changed a lot in 2025–26).

## Immediate next steps (this week)
1. Confirm the host (home server vs VPS) and which brokers you already have accounts with (IBKR? Alpaca? OANDA? MT5 broker? which crypto exchanges?).
2. Confirm your country of tax/legal residence: it affects broker and venue availability (e.g., Hyperliquid, some exchanges).
3. Start Phase 0.
