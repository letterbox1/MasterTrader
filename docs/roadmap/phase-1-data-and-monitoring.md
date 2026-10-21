# Phase 1 · Market Data, Recording & Live Monitoring

| | |
|---|---|
| **Goal** | Free, clean, point-in-time market and macro data for every asset class at every timeframe from ticks to 1D, with an always-on data-quality and cost monitor that alerts you. |
| **Duration** | Weeks 3–6 |
| **Depends on** | P0 (stack, schemas, `pit`, provenance columns, alerts plumbing) |
| **Unlocks** | P2 (strategies need data, measured costs and DQ status), P3 (RBA FX, ABS CPI), P4 (store and monitor patterns) |
| **Modules** | M1 market & macro data, M16 live cost & data-quality monitor, quota tracker, provenance tagging, M17 alerts |
| **Containers** | `ingest-market`, `ingest-batch`, `monitor`, `ntfy`, `telegram-bot` (alerts only) |
| **Dashboards** | [D07](../ui/dashboards/D07-data-quality.md) Data & Quality, [D02](../ui/dashboards/D02-markets.md) Markets, notifications |
| **Primary docs** | [03 M1](../03-build-spec.md#m1-market--macro-data--mt_datamarket) · [03 M16](../03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) · [03 §6](../03-build-spec.md#6-smallest-free-timeframe-by-asset-class) · [06 §3](../06-aggregators-and-market-providers.md#3-additional-forex--multi-asset-providers) · [12 §5](../12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) · [02 F1](../02-v1-architecture.md#8-end-to-end-flows) |

## 1. Scope

**In:** real-time and historical connectors for crypto, FX/metals, stocks/ETFs, futures (daily), rates and macro, fundamentals; the Parquet recorder and bar builder; quota tracking; provenance tags + retention jobs; the DQ monitor, cost monitor and reconciliation (on practice/testnet accounts); venue-health monitoring; alert channels (Telegram, email, ntfy); D07 and D02.

**Out:** calendars and text (P4), TCA on real fills (P2, once orders exist), on-chain data (P5).

## 2. Entry criteria

- P0 exit criteria met.
- Practice/testnet accounts (T0.09) and free API keys (T0.10) exist; Telegram bot exists (T0.06).

## 3. Requirements

| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R1.01 | **Crypto real-time:** public WS trades, L1, L2 diff (Binance, Bybit, OKX, Coinbase, Kraken) via Nautilus/ccxt → NATS `md.*` | [03 M1](../03-build-spec.md#m1-market--macro-data--mt_datamarket), [02 §6](../02-v1-architecture.md#6-messaging-nats) | Live feed |
| R1.02 | **Recording:** Parquet recorder (1–5 min files, daily compaction); bar builder writes 1s/1m bars to Timescale with continuous aggregates to 1D and arbitrary `time_bucket` sizes | [03 M1](../03-build-spec.md#m1-market--macro-data--mt_datamarket), [02 F1](../02-v1-architecture.md#8-end-to-end-flows) | Bar parity test |
| R1.03 | **Crypto history:** data.binance.vision trades/aggTrades/1s klines backfill | [03 M1](../03-build-spec.md#m1-market--macro-data--mt_datamarket) | Backfill report |
| R1.04 | **FX & metals:** OANDA practice stream, IG demo stream, Dukascopy ticks, ECB/Frankfurter, **RBA F11** daily FX; broker XAU/XAG (no LBMA) | [03 M1](../03-build-spec.md#m1-market--macro-data--mt_datamarket), [06 §3](../06-aggregators-and-market-providers.md#market-data-m1) | Live feed |
| R1.05 | **Stocks/ETFs:** Alpaca IEX real-time (30 symbols), yfinance daily, FinanceDatabase symbol master, `exchange_calendars` | [03 M1](../03-build-spec.md#m1-market--macro-data--mt_datamarket) | Live feed |
| R1.06 | **Futures/commodities (daily), rates & macro:** yfinance futures, EIA, USDA, CFTC COT, Baker Hughes; FRED/ALFRED vintages, US Treasury, `sdmx1`, BoE/BoC/RBA/SNB/BoJ, DBnomics, **ABS CPI** | [03 M1](../03-build-spec.md#m1-market--macro-data--mt_datamarket) | Batch flows |
| R1.07 | **Fundamentals:** SEC EDGAR via edgartools (declared User-Agent, ≤ 10 req/s) | [03 M1](../03-build-spec.md#m1-market--macro-data--mt_datamarket) | Batch flow |
| R1.08 | **Quota tracker** per connector that throttles before each free limit | [03 §1](../03-build-spec.md#1-ground-rules) | Quota panel in D07 |
| R1.09 | **Provenance:** every ingested row tagged (`source`, `licence`, use flags); retention jobs enforce `retention_days` (e.g. CoinGecko ≤ 24 h) | [12 §5](../12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms), [12 §4](../12-policy-and-compliance.md#4-per-platform-data--automation-rules) | Provenance test |
| R1.10 | **DQ monitor:** stale feed, gaps, bad ticks, cross-source divergence, clock skew, book integrity, nightly Pandera + Evidently → `dq.status.*` + `audit.dq_event` | [03 M16](../03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) | Fault injection |
| R1.11 | **Cost monitor:** fee tiers, funding (predicted + realised), swap/financing, `spread_bps` by instrument × hour-of-week → `cost.*` | [03 M16](../03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) | Cost panels |
| R1.12 | **Reconciliation:** balances/positions vs each practice/testnet venue every N minutes and EOD; mismatch = incident | [03 M16](../03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) | Recon report |
| R1.13 | **Venue-health monitor:** withdrawal delays, PoR/incident notes, AUSTRAC re-check reminders → `ops.venue_registry` health | [12 §2](../12-policy-and-compliance.md#2-venue-access-registry), [13 §6](../13-wallets-treasury-and-onchain.md#6-monitors-feed-m16-and-m11) | D07 panel |
| R1.14 | **Alerts:** Grafana Alerting → Telegram + email + **ntfy** (second independent channel) | [07 §9](../07-security-notes.md#9-monitoring--incident-response) | Test alerts |
| R1.15 | **UI:** D07 (feeds, quotas, DQ events, costs, recon) and D02 (charts, cross-asset matrix, instrument detail with **finest available resolution**) | [D07](../ui/dashboards/D07-data-quality.md), [D02](../ui/dashboards/D02-markets.md), [03 §6](../03-build-spec.md#6-smallest-free-timeframe-by-asset-class) | Playwright |
| R1.N1 | Feed staleness detected → `dq.status` stale **< 2 s** | [02 §9.2](../02-v1-architecture.md#92-observability--slos) | SLO metric |
| R1.N2 | UI live update lag p95 < 500 ms; server throttles ≤ 4 Hz charts, ≤ 1 Hz tables | [02 §9.2](../02-v1-architecture.md#92-observability--slos), [02 §6](../02-v1-architecture.md#6-messaging-nats) | Client telemetry |
| R1.N3 | Storage within budget (~0.3–1 TB/year for ~10 liquid crypto symbols at trades + L1 + L2@1s); cold Parquet to HDD | [03 M1](../03-build-spec.md#m1-market--macro-data--mt_datamarket) | Disk metrics |

## 4. ToDo sets

### A. Your actions (`USER`)
- [ ] **T1.01** `USER` Pick the starting **universe/watchlist**: ~10 crypto pairs, FX/metal pairs, ~30 US ETFs/stocks (Alpaca IEX limit), macro series you care about. → R1.01–R1.06
- [ ] **T1.02** `USER` Create **read-only** API keys on practice/testnet accounts (IP-allow-listed) for reconciliation and fee-tier reads. → R1.12 · [07 §3](../07-security-notes.md#3-broker--exchange-keys)
- [ ] **T1.03** `USER` Install the ntfy app on your phone and subscribe to the private topic; confirm the email alert address. → R1.14
- [ ] **T1.04** `USER` Review the first week's DQ alerts and tell us which thresholds are too noisy. → R1.10

### B. Build (`BUILD`, code)
- [ ] **T1.20** `BUILD` `mt_data.market` crypto WS clients via Nautilus data clients/ccxt; publish `md.*`. → R1.01
- [ ] **T1.21** `BUILD` Parquet recorder + daily compaction; bar builder (1s/1m) + Timescale continuous aggregates; tick/volume/value bar support. → R1.02
- [ ] **T1.22** `BUILD` Backfill flows: data.binance.vision, Dukascopy (dukascopy-node or own bi5 parser), Alpaca history, yfinance. → R1.03–R1.05
- [ ] **T1.23** `BUILD` FX/metals streaming: OANDA v20 practice, IG Lightstreamer demo; Frankfurter self-hosted; RBA F11 flow. → R1.04
- [ ] **T1.24** `BUILD` Macro/rates/fundamentals Prefect flows: FRED/ALFRED (vintages), Treasury, `sdmx1`, central banks, EIA/USDA/COT/Baker Hughes, ABS CPI, EDGAR. → R1.06, R1.07
- [ ] **T1.25** `BUILD` Quota tracker (per-connector budgets from live headers where available) shared by all connectors. → R1.08
- [ ] **T1.26** `BUILD` Provenance tagging at write time (defaults from each source's licence tag in 06) + retention job. → R1.09
- [ ] **T1.27** `BUILD` `mt_monitor` DQ service: per-instrument rolling state, checks table, `dq.status.*`, incidents. → R1.10
- [ ] **T1.28** `BUILD` `mt_monitor` cost service: fees/tiers, funding, financing, spreads by hour-of-week; TCA scaffolding for P2. → R1.11
- [ ] **T1.29** `BUILD` Reconciliation jobs (ccxt read-only, OANDA, IG, Alpaca, IBKR paper). → R1.12
- [ ] **T1.30** `BUILD` Venue-health collector writing to `ops.venue_registry` health fields; quarterly AUSTRAC re-check task. → R1.13
- [ ] **T1.31** `BUILD` Telegram bot (alerts only) + ntfy + email notifier behind one `alert.{severity}.{kind}` consumer. → R1.14
- [ ] **T1.32** `BUILD` UI: D07 Data & Quality, D02 Markets (lightweight-charts, matrix, instrument detail), notifications centre. → R1.15 · [D07](../ui/dashboards/D07-data-quality.md) · [D02](../ui/dashboards/D02-markets.md)

### C. Ops & config (`OPS`)
- [ ] **T1.40** `OPS` Storage layout: NVMe hot Parquet, HDD cold tier, compaction schedule, disk alerts. → R1.N3
- [ ] **T1.41** `OPS` Prefect schedules for batch flows (respecting quotas and source update times, AEST/AEDT aware). → R1.06
- [ ] **T1.42** `OPS` Grafana boards: live prices by timeframe, spreads/funding/swaps, DQ incidents, quota usage. → R1.10, R1.11
- [ ] **T1.43** `OPS` ntfy container (self-hosted, auth on, Tailscale only). → R1.14

### D. Verify & test (`VERIFY`)
- [ ] **T1.60** `VERIFY` Run the open provider checks: OANDA order/position books, TrueFX, IMF SDMX 3.0 URL, IG sentiment path, StockTwits reachability, Tardis samples, BoC/BoJ keyless. → [06 §3 open checks](../06-aggregators-and-market-providers.md#open-checks-do-these-in-phase-1)
- [ ] **T1.61** `VERIFY` DQ fault injection: kill a feed (stale < 2 s), inject a bad tick, skew the clock, drop sequence IDs. → R1.10, R1.N1
- [ ] **T1.62** `VERIFY` Bar parity: Timescale aggregates vs bars rebuilt from Parquet ticks for a sample day. → R1.02
- [ ] **T1.63** `VERIFY` Provenance/retention test: CoinGecko rows deleted after 24 h; untagged rows rejected. → R1.09
- [ ] **T1.64** `VERIFY` Alert path test on all three channels. → R1.14

### E. Run / soak (`RUN`)
- [ ] **T1.80** `RUN` 7-day continuous recording soak; gap report per instrument; disk growth vs budget. → R1.N3

## 5. Deliverables

Connectors + recorder + bar builder · batch flows · quota tracker · provenance + retention · DQ/cost/recon monitor · venue-health monitor · alerts on 3 channels · D07 + D02.

## 6. Exit criteria (demo)

1. Grafana and D02 show live prices at every timeframe from ticks to 1D across crypto, FX/metals and ETFs, plus daily futures and macro.
2. Live spread/funding/swap panels populate; reconciliation runs clean on practice accounts.
3. A deliberately killed feed shows stale in < 2 s and the alert reaches Telegram, email and ntfy.
4. Open provider checks are recorded in 06 (pass/fail).

## 7. Risks & open questions

| Risk | Mitigation |
|---|---|
| Free-tier changes or API breakage | Quota tracker + monthly ToS check (standing rule); cross-source references for every critical feed |
| Disk growth from L2 | Record L2 only for symbols that need it; compaction; HDD tier |
| IEX ≠ NBBO for US stocks | Flag in D02; avoid scalping-cost conclusions on IEX data (03 §6) |
