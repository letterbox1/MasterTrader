# MasterTrader — Architecture Overview (v2)

A one-page view of how the modules fit together. The detail lives in [03-build-spec.md](03-build-spec.md); the order of work is in [04-plan-of-action.md](04-plan-of-action.md).

## Design principles

1. **A platform, not a strategy.** Any strategy type on any timeframe (tick/L2 → 1D+). Styles, timeframes, capital and risk limits are user inputs.
2. **Models reason, code computes, the risk manager decides.**
   - No order from any source (strategy, LLM agent, UI, Telegram, MCP) reaches a broker without passing the deterministic risk manager.
   - The design borrows from Vibe-Trading's order guard and nofx's "Frontier" mode, re-implemented.
3. **Point-in-time everything.**
   - Every record carries `event_time` + `ingest_time`.
   - Raw news/social is archived so backtests can be replayed.
4. **One engine for backtest, paper and live:** NautilusTrader.
5. **Costs and data quality are measured live and fed back.** Backtests use the costs you actually pay. Bad data pauses trading.
6. **Record everything.** Append-only audit, journal and tax records; logs for operations.
7. **One command layer (`mt_api`).** The UI, Telegram and (later) MCP are just front-ends to it.
8. **Free only, personal use, no telemetry**; sandbox generated code; GPL/AGPL code kept isolated.

## Diagram

```
                     ┌──────────────────────────── DATA (free only, quota-tracked) ─────────────────────────────┐
 Market (M1):  crypto WS ticks/L2 · OANDA/IG streams · Dukascopy · Alpaca IEX · yfinance · data.binance.vision
 Macro (M1):   FRED/ALFRED · Treasury · sdmx1 (ECB/IMF/OECD/BIS) · central banks · EIA/USDA/COT · ABS CPI · RBA FX
 Text (M2):    RSS + RSS-Bridge · GDELT · Telegram · Discord (followed channels) · Bluesky · Mastodon · EDGAR
 Events (M3):  USGS · GDACS · NOAA · FIRMS · ReliefWeb · UCDP · Kalshi/Polymarket     Calendars (M5): FRED dates · ForexFactory · CB schedules
 Crypto alt (M4): DefiLlama · CryptoRank · CoinGecko · DexScreener · GoPlus · RugCheck · Honeypot.is · blocklists
                     └───────────────────────────────┬───────────────────────────────────────────────────────────┘
                                                     ▼  NATS JetStream
        ┌───────────────────────────┬────────────────┴──────────────┬────────────────────────────┐
        ▼                           ▼                               ▼                            ▼
  Parquet catalog (ticks/L2)   Timescale (bars 1s→1D+,        M16 Live monitor              Text/doc store + pgvector
  + DuckDB                     costs, business data)          (DQ · costs · TCA · recon)    (FinBERT, embeddings)
        │                           │                               │ pause/alert               │
        └────────────┬──────────────┴───────────────┬───────────────┘                            │
                     ▼                              ▼                                            ▼
          M6 Features ── M7 Research lab ── M0 Strategy framework ◄── M8 AI agents ◄── M9 Memory (Hindsight) + RAG
          (TA, factors,   (backtest/validate/   (any type, any         (debate graph,      M10 Anomaly + explain
           micro, macro)   optimise, MLflow)     timeframe)              valuation tools)
                            M21 Decision One: tier A in-process GBDT (~µs) · tier B decision models (one-pass option probabilities, async)
                            LiteLLM gateway → Claude / custom endpoint / local (research, chat, debate; never hot path)
                                                     │ OrderIntent
                                                     ▼
                              M11 RISK MANAGER (default-deny · limits · sizing · kill/dead-man switch)
                                                     ▼
                     M12 NautilusTrader execution (IBKR · Binance/Bybit/OKX/… · Alpaca · OANDA · IG)   M13 Hummingbot (MM)
                                                     ▼
                  M17 Audit (Postgres, append-only) + Loki/Prometheus/Grafana   ──►   M18 Journal & tax (AU/AE/EG/CY plugins)
                                                     ▲
     mt_api command layer ◄── M15 Web UI · Telegram bot (alerts, approvals, /kill)    M19 Task queue & community curation
                         ◄── M20 MCP (Phase 8, optional: analyse, talk to agents, trade/adjust, risk)
     M4 Airdrops: vet → auto-claim (hot wallet, mandate, simulation) | user task → journal
```

## Asset coverage

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

## Promotion gates before live capital

1. **Performance:** walk-forward out-of-sample results beat the benchmark after **measured** costs.
2. **Robustness statistics:** Monte Carlo permutation p < 0.05; deflated Sharpe > 0.
3. **Bias checks:** look-ahead and recursive analysers clean.
4. **LLM components:** tested only on data after the model's training cutoff.
5. **Paper/approve period:**
   - configurable, default ≥ 3 months;
   - P&L and costs track the backtest.
6. **Safety drills:** kill switch, dead-man's switch and DQ pause exercised in testing.
