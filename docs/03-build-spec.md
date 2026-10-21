# MasterTrader — Build Spec (personal-use edition)

**Context:** a proprietary, private project for the owner's personal use only. The aim is **minimal hoops**: use whatever works best (including GPL/AGPL code), self-host on one machine, avoid enterprise ceremony. The few disciplines kept are the ones that protect your money and your future options (Section 9).

---

## 1. What "personal use" changes

| Before (SaaS-safe posture) | Now (personal use) |
|---|---|
| GPL/AGPL code only as separate services or clean-room rewrites | **Use it directly.** You don't distribute and nobody else uses it over a network, so the GPL/AGPL obligations never trigger. |
| freqtrade = reference only | You may vendor freqtrade modules (look-ahead analysis, hyperopt loss functions, FreqAI ideas) directly |
| MiroFish / nofx = reference only | You may run or modify them. Security issues still apply: keep them on localhost, telemetry off, fee/referral tags stripped. |
| yfinance / Yahoo = avoid | **Fine.** Yahoo's terms allow personal, non-commercial use. |
| Free-tier APIs marked "non-commercial" | Fine for personal use |
| Commons Clause (vectorbt), BSL (ArcticDB), TSL (TimescaleDB) | Fine. They only restrict *selling* or *hosting for others*. |

**Still applies even for personal use:**
- Data-source terms that forbid scraping at all: X/Twitter scraping, Discord self-bots, ForexFactory/Investing.com scraping, CelesTrak rate-limit evasion. The risk is an account ban or IP block, not lawsuits for one person; it's your call, but prefer official APIs and RSS.
- Broker and exchange terms (no wash trading or spoofing; some venues restrict certain countries' residents, e.g. Hyperliquid for US persons).
- Tax reporting of your gains.

---

## 2. Target environment

| Item | Choice | Why |
|---|---|---|
| Host | One Linux box (home server or a ~8 vCPU / 32 GB RAM / 1 TB NVMe VPS); optional GPU for local LLMs | Simple; everything runs on `docker compose` |
| Language | Python 3.12 (core), small TS UI later if needed | Nautilus, Hummingbot, TradingAgents, FinRobot and Vibe-Trading are all Python |
| Packaging | `uv` workspace monorepo | Fast, one lockfile |
| Runtime | Docker Compose | One command up/down |
| LLMs | Claude API for manager/decision roles; **Ollama** (Qwen/Llama class) for cheap analyst, sentiment and summarisation work | Keeps per-run cost low |
| Secrets | `.env` (git-ignored) + OS keychain for broker keys; never in the repo | Minimal-hoop but safe |
| Access | Bound to `127.0.0.1`; remote access only via **Tailscale** (or WireGuard) | No public ports, no auth system to build |

---

## 3. Repository layout

```
MasterTrader/
├── pyproject.toml              # uv workspace root
├── docker-compose.yml          # postgres(timescale+pgvector), nats, prefect, grafana, ollama, app services
├── .env.example
├── packages/
│   ├── mt_core/                # shared types: Instrument, Bar, Event, Signal, Order, Mandate; config; logging
│   ├── mt_data/                # ingestion connectors + Prefect flows (M1–M5)
│   ├── mt_store/               # DB schema, migrations (alembic), point-in-time query helpers
│   ├── mt_features/            # factors, TA, sentiment, event scores, TS-foundation-model features (M6)
│   ├── mt_lab/                 # strategy gen + backtest + validation + bias analysers (M7)
│   ├── mt_agents/              # LangGraph debate graph, valuation tools, prompts (M8)
│   ├── mt_memory/              # Hindsight + LightRAG adapters, decision settlement/reflection (M9)
│   ├── mt_anomaly/             # detectors + explain agent (M10)
│   ├── mt_guard/               # risk/order guard, mandates, kill switch, approvals (M11)
│   ├── mt_engine/              # NautilusTrader wrapper + custom adapters (Alpaca, OANDA, MT5) (M12)
│   └── mt_ui/                  # FastAPI + simple dashboard (Streamlit/NiceGUI for v1) + Telegram bot (M15)
├── services/
│   ├── hummingbot/             # sidecar config (M13), telemetry off
│   └── crowdsim/               # optional OASIS/MiroFish experiment (M14)
├── third_party/                # vendored code; pinned commit + upstream licence kept per folder
│   └── LICENSES.md             # manifest: what came from where, under what licence (see §9)
├── strategies/                 # your strategies (Nautilus Strategy classes)
├── notebooks/                  # research
├── tests/
└── docs/
```

---

## 4. Data model (point-in-time core)

All tables live in Postgres + TimescaleDB. Every fact carries **two timestamps**.

```sql
instrument(id PK, symbol, venue, asset_class, currency, multiplier, meta jsonb)

bar(instrument_id, ts_event, ts_ingest, timeframe, o,h,l,c,v, source)        -- hypertable
tick/quote (optional, Parquet on disk for heavy data)

macro_series(series_id, ts_event, ts_vintage, value, source)                -- ALFRED vintages
filing(cik, form, ts_filed, ts_ingest, url, parsed jsonb)                    -- EDGAR
document(id, kind[news|social|report], ts_published, ts_ingest, source, url,
         title, body, lang, entities text[], tickers text[], sentiment float, embedding vector)
geo_event(id, kind[quake|storm|conflict|fire|disaster|sanction|...], ts_event, ts_ingest,
          lat, lon, country, severity, source, payload jsonb)
crypto_launch(id, kind[airdrop|ico|listing|tge], chain, token, ts_announced, ts_event, source, payload)
calendar_event(id, kind[macro|earnings|ipo], ts_scheduled, ts_ingest, country, importance, actual, forecast, previous)
exposure_map(country|region|commodity -> instrument_id, weight)              -- event→asset linking

feature(instrument_id, ts, name, value, version)
signal(id, ts, instrument_id, direction, conviction 0-1, horizon, rationale, sources jsonb, model, run_id)
decision_log(signal_id, settled_at, realised_return, alpha_vs_bench, reflection)
order_audit(id, ts, mandate_id, signal_id, request jsonb, guard_result, broker_response jsonb)
mandate(id, name, venues, instruments, max_notional, max_leverage, max_daily_loss, mode[paper|approve|auto], active)
```

**Rule:** research and backtest code reads data only through `mt_store.pit(as_of=...)`, which filters on `ts_ingest <= as_of`. A test fails the build if any module queries the raw tables directly.

---

## 5. Module specs (v1)

### M1 Market & macro ingestion — `mt_data`
- Crypto: **ccxt** (OHLCV, funding, order book snapshots) for Binance, Bybit, OKX, Coinbase, Kraken, Hyperliquid.
- Equities/ETFs: **yfinance** (personal use OK) + OpenBB providers; Alpaca market data (free IEX feed).
- FX & metals: **Dukascopy** history, **OANDA practice** stream; XAU/XAG via OANDA.
- Commodities: **EIA** (energy), **USDA**, **CFTC COT**; futures bars via yfinance (`GC=F`, `CL=F`…) to start.
- Rates/bonds: **US Treasury** yield curve, **FRED/ALFRED** (with vintages), ECB SDW.
- Fundamentals: **SEC EDGAR via edgartools** (10-K/10-Q XBRL, 13F, Form 4 insiders, S-1/424B for IPOs).
- Schedules: Prefect deployments (1-minute crypto, hourly/daily others), with idempotent upserts.

### M2 News & social — `mt_data.text`
- **RSS** (Reuters, AP, CNBC, central banks, CoinDesk/The Block, regulator feeds) → **trafilatura** full text.
- **crawl4ai** for sites without RSS.
- **Reddit**: official API (r/wallstreetbets, r/stocks, r/CryptoCurrency, r/Forex…); Telegram channels via **Telethon** (your own account).
- **GDELT** 2.0 GKG for global news volume and tone.
- X/Twitter: official API if you pay; otherwise skip (scraping is against its terms).
- Processing: language detection → ticker/entity linking → **FinBERT** sentiment (local) → embeddings (local `bge`/`nomic` via Ollama) → `document`.

### M3 Global events — `mt_data.events`
- **USGS** quakes, **GDACS** disasters, **NOAA/NHC** storms, **NASA FIRMS** fires, **ReliefWeb**, **UCDP** conflict, **GDELT** events, **OpenSanctions**; ACLED with a free research account is OK for personal use.
- `exposure_map` seeds: country → FX pair, main index ETF, sovereign bond ETF; commodity regions (e.g., Gulf of Mexico → CL/NG; Chile/Peru → copper; Ukraine/Russia → wheat, NG, EUR).
- Event score = severity × exposure weight × novelty (dedupe within 24h).
- Optional: run **osiris** locally as a visual map (MIT; remove the token panel).

### M4 Crypto alt-data tracker — `mt_data.crypto_alt`
- CoinGecko "new coins" + categories, DefiLlama (protocols, airdrops page, raises, unlocks), exchange listing announcement RSS, and on-chain (Etherscan free tier) for token-contract creation and large transfers.
- Output: `crypto_launch` with status pipeline (announced → snapshot → claim → listed), plus Telegram alerts.

### M5 Calendars — `mt_data.calendar`
- FRED release calendar, BLS/BEA/Fed/ECB/BoE schedules, EDGAR earnings (8-K) and IPO (S-1/424B) parsing, plus Nasdaq/NYSE IPO calendar pages (personal use).

### M6 Features — `mt_features`
- TA-Lib indicators; the **Qlib Alpha158** factor set; Vibe-Trading factor zoo (alpha101/GTJA191).
- Sentiment aggregates per instrument (count, mean, z-score), event scores, COT positioning, macro surprises (actual − forecast).
- **Chronos/TimesFM/Kronos** forecasts as *volatility/volume* features.
- Features are versioned; there is a feature-to-forward-return evaluator (IC, rank-IC, decay).

### M7 Research lab — `mt_lab`
- **Fast path:** vectorised candle backtests (Vibe-Trading engines, or vectorbt for personal use) for screening.
- **Truth path:** **NautilusTrader** backtests with fees, slippage and latency for anything that survives screening.
- **Validation:** walk-forward, purged K-fold, Monte Carlo permutation, bootstrap Sharpe CI, deflated Sharpe ratio; **freqtrade's lookahead-analysis and recursive-analysis** (vendored; GPL is fine for personal use).
- **LLM strategy generation** (Vibe-Trading pattern) → code runs in a **Docker sandbox with no network and no secrets**, and strategies must implement the `mt_core.Strategy` interface.
- **Optimisation:** Optuna, plus a penalty for parameter count to discourage overfitting.

### M8 AI decision layer — `mt_agents`
- A LangGraph graph adapted from **TradingAgents**:
  1. Analysts (technical, sentiment, news, fundamentals, **macro/events**) run in parallel.
  2. Bull/bear debate.
  3. Research manager.
  4. Trader proposal.
  5. Risk debate.
  6. Portfolio manager.
  7. The output is a `signal` row.
- Tools: **FinRobot V2 valuation operators** (DCF, WACC, comps), the `mt_store.pit` data tools, memory recall.
- Model tiers: analysts on Ollama/local; managers on Claude.
- Every claim in the rationale must cite a `document`/`bar`/`filing` id (provenance).

### M9 Memory — `mt_memory`
- **Hindsight** (MIT) for agent memory: facts, experiences, mental models.
- **LightRAG** over filings and long reports.
- **Decision settlement** (TradingAgents): after the horizon expires, compute the realised return and alpha, have the LLM write a reflection, and store it in Hindsight so similar future setups recall it.

### M10 Anomaly monitor — `mt_anomaly`
- Detectors include:
  - Rolling robust z-scores on returns, volume, spread and funding.
  - IsolationForest on a multi-feature vector.
  - Change-point detection (ruptures).
  - Sentiment and news-volume spikes, and event-score spikes.
  - Cross-asset correlation breaks.
- An "Explain" agent pulls the surrounding news, events and filings, writes a short brief, and sends it to Telegram.

### M11 Guard — `mt_guard` (non-negotiable, even for personal use)
- **Default-deny.** An order passes only if:
  - an active `mandate` covers the venue and instrument;
  - it stays within notional, leverage and daily-loss limits and the max open positions;
  - the price is within X% of the last trade;
  - the kill switch is off.
- **Modes per mandate:**
  - `paper`: simulated fills.
  - `approve`: Telegram/UI button per order, the nofx "Frontier" idea.
  - `auto`: unattended, but only after the live-capital gates in §8.
- Every request and decision goes to `order_audit`. No automatic retries on rejects.

### M12 Execution — `mt_engine`
- **NautilusTrader**, pinned version, behind a thin wrapper.
- Venues out of the box: IBKR, Binance, Bybit, OKX, Coinbase, Kraken, Hyperliquid, Polymarket.
- **Custom adapters to write:** Alpaca (stocks/ETFs/crypto paper), OANDA v20 (FX/metals/CFDs), and MT5 if your broker is MT5-only (Windows bridge).
- Start everything on paper/testnet.

### M13 Market-making sidecar
- **Hummingbot** in Docker with `anonymized_metrics_mode: disabled`.
- Strip the broker IDs if you want (personal use, your call).
- It is controlled through its API and treated as another "venue" by the guard.

### M14 Crowd simulation (optional)
- Run **MiroFish** locally as-is (personal use = fine). Zep Cloud needs an account, so consider swapping in Graphiti later.
- Use it only for scenario narratives on big events; log its outputs and evaluate them as a feature before trusting it.

### M15 UI & alerts
- Telegram bot: alerts, daily brief, approval buttons, `/kill`.
- Grafana: P&L, exposure, data freshness, LLM spend.
- A Streamlit/NiceGUI app for signals, decisions, the backtest reports viewer and mandates.

---

## 6. Interfaces (contracts between modules)

```python
class Signal(BaseModel):
    instrument_id: str; ts: datetime; direction: Literal["long","short","flat"]
    conviction: float  # 0..1
    horizon: timedelta; rationale: str; sources: list[str]; model: str; run_id: str

class OrderIntent(BaseModel):
    mandate_id: str; instrument_id: str; side: Literal["buy","sell"]
    qty: Decimal | None; notional: Decimal | None; order_type: str; limit_price: Decimal | None
    signal_id: str | None

class GuardResult(BaseModel):
    allowed: bool; reasons: list[str]; requires_approval: bool
```

Position sizing is **deterministic**, never LLM-chosen: volatility-targeted, conviction-scaled and capped by the mandate.

---

## 7. LLM cost control

- Analysts run on local models; only the managers and the final PM call Claude.
- Run cadence: daily for swing positions, plus event-triggered runs (anomaly or big event) — **not** every minute.
- Cache tool outputs per (instrument, as_of).
- A monthly spend cap lives in config; Grafana panel shows LLM spend.

---

## 8. Live-capital gates (per strategy)

1. The strategy beats its benchmark on walk-forward, out-of-sample data after fees and slippage.
2. Monte Carlo permutation p < 0.05, and the deflated Sharpe ratio is above 0.
3. The look-ahead and recursive analysers come back clean.
4. LLM-driven strategies were evaluated only on data after the model's training cutoff.
5. At least 3 months of paper or approve mode, with live P&L tracking the backtest within tolerance.
6. Start live at a small size; scale only after another 3 months.

---

## 9. Minimal "future-proof" hygiene (cheap now, saves a rewrite if you ever go SaaS)

1. Put all copied third-party code under `third_party/<name>/` with its LICENSE and pinned commit, and list it in `third_party/LICENSES.md`. That's ~1 line per import.
2. Keep GPL/AGPL-derived code in **separate modules or services** where it costs nothing to do so: freqtrade bits in `mt_lab/thirdparty_gpl/`, MiroFish in `services/crowdsim/`. Then a SaaS version can drop or replace them without untangling the core.
3. Tag each data source in config with `license: personal|commercial_ok|unknown`. A SaaS build can then filter to `commercial_ok`.
4. Keep the repo **private**. Making it public would count as distributing any GPL code it contains.
