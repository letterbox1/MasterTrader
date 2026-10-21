# MasterTrader v1 — Specification

Full detail is in [docs/03-build-spec.md](docs/03-build-spec.md) (build spec) and [docs/04-plan-of-action.md](docs/04-plan-of-action.md) (plan); the architecture overview is [docs/02-v1-architecture.md](docs/02-v1-architecture.md).

**Usage:** private, personal use only. GPL/AGPL code is allowed (no distribution, no third-party network users). SaaS implications are in [docs/05-saas-legal-and-licensing.md](docs/05-saas-legal-and-licensing.md). Component choices are justified in [docs/01-repo-vetting-report.md](docs/01-repo-vetting-report.md).

## Core decisions

| Area | Decision |
|---|---|
| Execution / backtest core | **NautilusTrader** (LGPL, used unmodified as a dependency behind an `mt_engine` wrapper) |
| Market-making sidecar | **Hummingbot** (Apache-2.0, telemetry disabled) |
| AI decision layer | **TradingAgents** debate pattern on LangGraph + **FinRobot V2** valuation operators |
| Strategy research lab | **Vibe-Trading** ideas and components (MIT): LLM strategy generation, multi-market engines, Monte Carlo / walk-forward validation, order guard |
| Bias tooling | freqtrade's look-ahead and recursive analysers, vendored (GPL is OK for personal use; isolated in `thirdparty_gpl/`) |
| Memory / RAG | **Hindsight** (MIT) + LightRAG on Postgres/pgvector |
| Storage | Postgres + TimescaleDB + pgvector; Parquet/DuckDB for research |
| Orchestration | Prefect flows; NATS JetStream / Valkey event bus |
| Global events | Direct GDELT/USGS/GDACS/NOAA/FIRMS/ReliefWeb/UCDP ingestion (osiris used as reference only) |
| Crowd simulation | Optional MiroFish experiment run locally (AGPL is fine for personal use), with a later rebuild on OASIS if needed |
| Rejected | VibeTradingLabs/vibetrading (redundant, unsafe); nofx as a platform (hidden fees, default-on telemetry, exposed install). Its ideas are borrowed. |

## Non-negotiable requirements

1. **Point-in-time data.** Every record has `event_time` + `ingest_time`, and backtests can't read rows from their future.
2. **Default-deny order guard.** Mandates, notional, leverage and drawdown caps, kill switch, human-approval tier, audit log.
3. **Sandboxed generated code.** LLM-written code runs with no network access and no credentials.
4. **No telemetry or referral tags** in vendored components.
5. **Licence hygiene (lightweight).** Keep vendored code under `third_party/` with a licence manifest, and keep GPL/AGPL code isolated so a future SaaS could drop it. Keep the repo private.
6. **Live-capital gates.** Out-of-sample performance after costs, MC p < 0.05, testing on data after the model's training cutoff, and ≥ 3 months of paper trading that matches the backtest.

## Phases

0. Foundations
1. Research loop
2. AI layer
3. Paper trading
4. Expansion (trackers, anomaly agent, MM, crowd-sim)
