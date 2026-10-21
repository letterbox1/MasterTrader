# MasterTrader v1 — Specification

Full detail is in [docs/02-v1-architecture.md](docs/02-v1-architecture.md). Component choices are justified in [docs/01-repo-vetting-report.md](docs/01-repo-vetting-report.md).

## Core decisions

| Area | Decision |
|---|---|
| Execution / backtest core | **NautilusTrader** (LGPL, used unmodified as a dependency behind an `mt_engine` wrapper) |
| Market-making sidecar | **Hummingbot** (Apache-2.0, telemetry disabled) |
| AI decision layer | **TradingAgents** debate pattern on LangGraph + **FinRobot V2** valuation operators |
| Strategy research lab | **Vibe-Trading** ideas and components (MIT): LLM strategy generation, multi-market engines, Monte Carlo / walk-forward validation, order guard |
| Bias tooling | Clean-room re-implementation of freqtrade's look-ahead and recursive analysers (freqtrade itself is GPL) |
| Memory / RAG | **Hindsight** (MIT) + LightRAG on Postgres/pgvector |
| Storage | Postgres + TimescaleDB + pgvector; Parquet/DuckDB for research |
| Orchestration | Prefect flows; NATS JetStream / Valkey event bus |
| Global events | Direct GDELT/USGS/GDACS/NOAA/FIRMS/ReliefWeb/UCDP ingestion (osiris used as reference only) |
| Crowd simulation | Optional experiment built clean-room on CAMEL-AI OASIS (MiroFish used as reference only) |
| Rejected | VibeTradingLabs/vibetrading (redundant, unsafe, no LICENSE file); nofx code (AGPL, hidden fees, default-on telemetry) |

## Non-negotiable requirements

1. **Point-in-time data.** Every record has `event_time` + `ingest_time`, and backtests can't read rows from their future.
2. **Default-deny order guard.** Mandates, notional, leverage and drawdown caps, kill switch, human-approval tier, audit log.
3. **Sandboxed generated code.** LLM-written code runs with no network access and no credentials.
4. **No telemetry or referral tags** in vendored components.
5. **License firewall.** The core stays MIT/Apache; GPL/AGPL tools run only as separate services.
6. **Live-capital gates.** Out-of-sample performance after costs, MC p < 0.05, testing on data after the model's training cutoff, and ≥ 3 months of paper trading that matches the backtest.

## Phases

0. Foundations
1. Research loop
2. AI layer
3. Paper trading
4. Expansion (trackers, anomaly agent, MM, crowd-sim)
