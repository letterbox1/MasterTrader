---
phase: 1
title: Market data, recording & live monitoring
roadmap: docs/roadmap/phase-1-data-and-monitoring.md
status: not_started
opens_after: [0]
force_open: false
started: ""
completed: ""
doc_sync_status: n/a
updated: 2026-10-21
---

# Phase 1 · Market data, recording & live monitoring

## Summary

Free, clean, point-in-time market and macro data for every asset class at every timeframe from ticks to 1D, plus an always-on data-quality, cost and reconciliation monitor that alerts you on Telegram, email and ntfy ([roadmap](../../docs/roadmap/phase-1-data-and-monitoring.md)). Containers added: `ingest-market`, `ingest-batch`, `monitor`, `ntfy`, `telegram-bot` (alerts only). Dashboards: D07 Data & Quality, D02 Markets, notification centre.

The work is split into one task per connector family (crypto WS, recorder, bar builder, each backfill, FX/metals streams, RBA F11, stocks/ETFs, macro/rates, ABS CPI, EDGAR, CoinGecko enrichment), the shared plumbing (connector framework, quota tracker, provenance + retention, instrument master), one task per DQ check (each with its own fault-injection tests), the cost monitor, reconciliation, venue health, alert fan-out, the API and UI, ops, verification items for every roadmap VERIFY ToDo plus end-to-end/stress/UI checks, the 7-day soak and the exit demo. 67 tasks (4 USER · 46 BUILD · 5 OPS · 1 DOC · 10 VERIFY · 1 RUN) and 18 gaps.

## Entry criteria

- [ ] Phase 0 exit criteria met (stack healthy, login + TOTP, `audit.command` hash chain, restore test, shell passes the viewport matrix)
- [ ] P0 schemas include provenance columns (R0.05) and `ops.venue_registry` seeded (R0.06); `pit(as_of)` and the WORM layer (R0.07) in place
- [ ] Practice/testnet accounts exist (T0.09): OANDA practice, IG demo, Alpaca paper, IBKR paper, Binance + Bybit testnets
- [ ] Free API keys in the sops file (T0.10): FRED, EIA, CoinGecko Demo, Finnhub (and others listed there)
- [ ] Telegram bot created via @BotFather (T0.06); chrony running on the host (T0.40)

## Exit criteria

- [ ] Grafana and D02 show live prices at every timeframe from ticks to 1D across crypto, FX/metals and ETFs, plus daily futures and macro (P1-T061, P1-T067)
- [ ] Live spread/funding/swap panels populate; reconciliation runs clean on practice accounts (P1-T064, P1-T067)
- [ ] A deliberately killed feed shows stale in < 2 s and the alert reaches Telegram, email and ntfy (P1-T057, P1-T060, P1-T067)
- [ ] Open provider checks are recorded in 06 (pass/fail) (P1-T056)
- [ ] All P1 tasks are done or cancelled
- [ ] No open S1/S2 bugs or gaps in phase 1

## Workstreams

| Workstream | Tasks |
|---|---|
| Your actions (USER) | P1-T001, P1-T002, P1-T003, P1-T066 |
| Platform & plumbing (OPS/BUILD) | P1-T004, P1-T005, P1-T006, P1-T007, P1-T008, P1-T009 |
| Crypto real-time & recording | P1-T010, P1-T011, P1-T012, P1-T013, P1-T014, P1-T015 |
| FX & metals | P1-T016, P1-T017, P1-T018, P1-T019, P1-T020 |
| Stocks/ETFs & daily futures | P1-T021, P1-T022, P1-T023 |
| Macro, rates, CPI & fundamentals | P1-T024, P1-T025, P1-T026, P1-T027, P1-T028, P1-T029 |
| DQ monitor (M16) | P1-T030, P1-T031, P1-T032, P1-T033, P1-T034, P1-T035, P1-T036, P1-T037 |
| Costs, reconciliation, venue health (M16) | P1-T038, P1-T039, P1-T040, P1-T041, P1-T042, P1-T043 |
| Alerts (M17) | P1-T044, P1-T045 |
| API & UI (D07, D02, notifications) | P1-T046, P1-T047, P1-T048, P1-T049, P1-T050, P1-T051 |
| Ops (storage, schedules, Grafana) & docs | P1-T052, P1-T053, P1-T054, P1-T055 |
| Verify | P1-T056, P1-T057, P1-T058, P1-T059, P1-T060, P1-T061, P1-T062, P1-T063, P1-T064, P1-T067 |
| Run | P1-T065 |
| Gaps found while planning | P1-B001, P1-B002, P1-B003, P1-B004, P1-B005, P1-B006, P1-B007, P1-B008, P1-B009, P1-B010, P1-B011, P1-B012, P1-B013, P1-B014, P1-B015, P1-B016, P1-B017, P1-B018 |

## Critical path

P1-T004 → P1-T005 → P1-T007 → P1-T009 → P1-T010 → P1-T030 → P1-T041 → P1-T046 → P1-T047 → P1-T049 → P1-T050 → P1-T061 → P1-T065 (7 elapsed days) → P1-T066 → P1-T067

Parallel lanes that must also finish before P1-T065/T067: recorder + bars (P1-T012/T013), DQ checks (P1-T031…T036) → P1-T057, alerts (P1-T044/T045) → P1-T060, D07 (P1-T048), storage/schedules/Grafana (P1-T052/T053/T054). Start P1-T001 and P1-T002 on day 1: the soak needs the universe, and recon needs keys.

## Traceability

### Requirements → tasks

| Requirement | Summary | Tasks |
|---|---|---|
| R1.01 | Crypto real-time: public WS trades, L1, L2 diff (Binance, Bybit, OKX, Coinbase, Kraken) v… | P1-T001, P1-T004, P1-T005, P1-T010, P1-T011, P1-T061, P1-T067 |
| R1.02 | Recording: Parquet recorder (1–5 min files, daily compaction); bar builder writes 1s/1m b… | P1-T012, P1-T013, P1-T014, P1-T050, P1-T058, P1-T061, P1-T062, P1-T065, P1-T067 |
| R1.03 | Crypto history: data.binance.vision trades/aggTrades/1s klines backfill | P1-T015, P1-T067 |
| R1.04 | FX & metals: OANDA practice stream, IG demo stream, Dukascopy ticks, ECB/Frankfurter, RBA… | P1-T001, P1-T016, P1-T017, P1-T018, P1-T019, P1-T020, P1-T056, P1-T061, P1-T067 |
| R1.05 | Stocks/ETFs: Alpaca IEX real-time (30 symbols), yfinance daily, FinanceDatabase symbol ma… | P1-T001, P1-T009, P1-T021, P1-T022, P1-T023, P1-T056, P1-T061, P1-T067 |
| R1.06 | Futures/commodities (daily), rates & macro: yfinance futures, EIA, USDA, CFTC COT, Baker… | P1-T001, P1-T023, P1-T024, P1-T025, P1-T026, P1-T027, P1-T053, P1-T056, P1-T061, P1-T067 |
| R1.07 | Fundamentals: SEC EDGAR via edgartools (declared User-Agent, ≤ 10 req/s) | P1-T028, P1-T067 |
| R1.08 | Quota tracker per connector that throttles before each free limit | P1-T005, P1-T006, P1-T029, P1-T046, P1-T048, P1-T053, P1-T054, P1-T067 |
| R1.09 | Provenance: every ingested row tagged (`source`, `licence`, use flags); retention jobs en… | P1-T005, P1-T007, P1-T008, P1-T029, P1-T059, P1-T067 |
| R1.10 | DQ monitor: stale feed, gaps, bad ticks, cross-source divergence, clock skew, book integr… | P1-T004, P1-T030, P1-T031, P1-T032, P1-T033, P1-T034, P1-T035, P1-T036, P1-T037, P1-T046, P1-T048, P1-T054, P1-T055, P1-T057, P1-T065, P1-T066, P1-T067 |
| R1.11 | Cost monitor: fee tiers, funding (predicted + realised), swap/financing, `spread_bps` by… | P1-T002, P1-T038, P1-T039, P1-T040, P1-T046, P1-T048, P1-T054, P1-T064, P1-T067 |
| R1.12 | Reconciliation: balances/positions vs each practice/testnet venue every N minutes and EOD… | P1-T002, P1-T041, P1-T042, P1-T046, P1-T048, P1-T055, P1-T064, P1-T067 |
| R1.13 | Venue-health monitor: withdrawal delays, PoR/incident notes, AUSTRAC re-check reminders →… | P1-T043, P1-T048, P1-T067 |
| R1.14 | Alerts: Grafana Alerting → Telegram + email + ntfy (second independent channel) | P1-T003, P1-T004, P1-T044, P1-T045, P1-T051, P1-T054, P1-T060, P1-T067 |
| R1.15 | UI: D07 (feeds, quotas, DQ events, costs, recon) and D02 (charts, cross-asset matrix, ins… | P1-T009, P1-T046, P1-T047, P1-T048, P1-T049, P1-T050, P1-T051, P1-T061, P1-T063, P1-T067 |
| R1.N1 | Feed staleness detected → `dq.status` stale < 2 s | P1-T031, P1-T057, P1-T062, P1-T067 |
| R1.N2 | UI live update lag p95 < 500 ms; server throttles ≤ 4 Hz charts, ≤ 1 Hz tables | P1-T047, P1-T062, P1-T067 |
| R1.N3 | Storage within budget (~0.3–1 TB/year for ~10 liquid crypto symbols at trades + L1 + L2@1… | P1-T012, P1-T052, P1-T055, P1-T065, P1-T067 |

### Roadmap ToDos → tasks

| ToDo | Summary | Tasks |
|---|---|---|
| T1.01 | Pick the starting universe/watchlist: ~10 crypto pairs, FX/metal pairs, ~30 US ETFs/stock… | P1-T001 |
| T1.02 | Create read-only API keys on practice/testnet accounts (IP-allow-listed) for reconciliati… | P1-T002 |
| T1.03 | Install the ntfy app on your phone and subscribe to the private topic; confirm the email… | P1-T003 |
| T1.04 | Review the first week's DQ alerts and tell us which thresholds are too noisy. | P1-T066 |
| T1.20 | `mt_data.market` crypto WS clients via Nautilus data clients/ccxt; publish `md.*`. | P1-T004, P1-T005, P1-T010, P1-T011 |
| T1.21 | Parquet recorder + daily compaction; bar builder (1s/1m) + Timescale continuous aggregate… | P1-T012, P1-T013, P1-T014 |
| T1.22 | Backfill flows: data.binance.vision, Dukascopy (dukascopy-node or own bi5 parser), Alpaca… | P1-T009, P1-T015, P1-T018, P1-T021, P1-T022, P1-T023 |
| T1.23 | FX/metals streaming: OANDA v20 practice, IG Lightstreamer demo; Frankfurter self-hosted;… | P1-T016, P1-T017, P1-T019, P1-T020 |
| T1.24 | Macro/rates/fundamentals Prefect flows: FRED/ALFRED (vintages), Treasury, `sdmx1`, centra… | P1-T024, P1-T025, P1-T026, P1-T027, P1-T028 |
| T1.25 | Quota tracker (per-connector budgets from live headers where available) shared by all con… | P1-T006 |
| T1.26 | Provenance tagging at write time (defaults from each source's licence tag in 06) + retent… | P1-T007, P1-T008, P1-T029 |
| T1.27 | `mt_monitor` DQ service: per-instrument rolling state, checks table, `dq.status.*`, incid… | P1-T004, P1-T030, P1-T031, P1-T032, P1-T033, P1-T034, P1-T035, P1-T036, P1-T037 |
| T1.28 | `mt_monitor` cost service: fees/tiers, funding, financing, spreads by hour-of-week; TCA s… | P1-T038, P1-T039, P1-T040, P1-T064 |
| T1.29 | Reconciliation jobs (ccxt read-only, OANDA, IG, Alpaca, IBKR paper). | P1-T041, P1-T042, P1-T064 |
| T1.30 | Venue-health collector writing to `ops.venue_registry` health fields; quarterly AUSTRAC r… | P1-T043 |
| T1.31 | Telegram bot (alerts only) + ntfy + email notifier behind one `alert.{severity}.{kind}` c… | P1-T004, P1-T045 |
| T1.32 | UI: D07 Data & Quality, D02 Markets (lightweight-charts, matrix, instrument detail), noti… | P1-T009, P1-T046, P1-T047, P1-T048, P1-T049, P1-T050, P1-T051, P1-T063 |
| T1.40 | Storage layout: NVMe hot Parquet, HDD cold tier, compaction schedule, disk alerts. | P1-T052 |
| T1.41 | Prefect schedules for batch flows (respecting quotas and source update times, AEST/AEDT a… | P1-T053 |
| T1.42 | Grafana boards: live prices by timeframe, spreads/funding/swaps, DQ incidents, quota usag… | P1-T054 |
| T1.43 | ntfy container (self-hosted, auth on, Tailscale only). | P1-T044 |
| T1.60 | Run the open provider checks: OANDA order/position books, TrueFX, IMF SDMX 3.0 URL, IG se… | P1-T056, P1-T067 |
| T1.61 | DQ fault injection: kill a feed (stale < 2 s), inject a bad tick, skew the clock, drop se… | P1-T057, P1-T067 |
| T1.62 | Bar parity: Timescale aggregates vs bars rebuilt from Parquet ticks for a sample day. | P1-T058, P1-T067 |
| T1.63 | Provenance/retention test: CoinGecko rows deleted after 24 h; untagged rows rejected. | P1-T059, P1-T067 |
| T1.64 | Alert path test on all three channels. | P1-T060, P1-T067 |
| T1.80 | 7-day continuous recording soak; gap report per instrument; disk growth vs budget. | P1-T065, P1-T067 |

Tasks without a roadmap ToDo of their own (traced by requirement): P1-T055 (runbooks), P1-T061 (F1 end-to-end), P1-T062 (load + UI lag). P1-T009, P1-T021 trace to T1.22 and P1-T029 to T1.26 only by proximity; see gaps P1-B003 and P1-B004.

## Planning notes & risks

- **Stale SLO definition (P1-B001, S2):** tasks implement two layers (connection-level < 2 s from feed death; per-instrument learned timeouts with a 2 s floor). Confirm before P1-T057 measures it.
- **Disk (R1.N3, P1-B002):** L2 is recorded only for `l2: true` symbols; P1-T052 sheds L2 before quotes and never trades; the soak replaces the estimate with measured bytes/day.
- **Free-tier breakage:** every connector goes through the quota tracker (P1-T006); yfinance and Baker Hughes are fragile and fail loudly; cross-source references exist for crypto and FX majors, stocks rely on Finnhub low-frequency checks or are flagged single-source.
- **IEX ≠ NBBO:** flagged on every Alpaca message and in D02; no scalping-cost conclusions from IEX data.
- **Alerts:** one path for all alerts (P1-B007); email sender (P1-B005) and iOS ntfy behaviour (P1-B006) need your decisions before P1-T060.
- **C3 in P1 (P1-B009):** until the Telegram approve + TOTP leg exists, loosening DQ thresholds is a reviewed config PR approved by you.
- **Read-only keys (P1-B008):** only Binance/Bybit testnets offer read-only scopes; elsewhere a GET-only client allow-list is the control (tested).
- **IBKR paper recon (P1-B013):** needs an IB Gateway container; ships disabled with a reason if not approved in P1.
- **WORM:** P1 adds `audit.dq_event`, `audit.cost_event`, `audit.recon`, `audit.tca`; each carries the 15 §2.4 tests. Incident resolution/ack are new rows (P1-B018).
- **Order surfaces:** D02's order ticket is present but disabled; no P1 code places orders.
- **Soak timing:** P1-T065 needs 7 elapsed days with frozen config; plan the exit demo for a window when US equities, FX and crypto are all open.

## Cross-phase prerequisites

- **P0 (opens_after):** R0.01/T0.20 monorepo; T0.21 `mt_core` types; R0.03–R0.06/T0.22 schemas, provenance columns, `pit`, `ops.venue_registry`, Parquet helpers; R0.07/T0.23 WORM layer; R0.08/T0.24 `mt_api` (auth, commands, confirmation levels, WS envelope); R0.10/T0.25 `mt_obs`; R0.11/T0.26 web app + component library; R0.02/T0.41 Compose; R0.N3/T0.42 networks; R0.N1/T0.43 sops; T0.46 Grafana provisioning; R0.N2/T0.40 chrony + Tailscale; R0.N6/T0.64 Playwright viewport matrix; T0.06 Telegram bot; T0.09 practice accounts; T0.10 free API keys; T0.11 venue checks.
- **Consumers downstream:** P2 R2.16 (DQ status in pre-trade checks), R2.34/T2.26 (TCA on paper fills uses P1-T040 scaffolding), R2.40 (measured costs), R2.52 (Telegram commands extend the P1 alerts bot); P3 R3.03/T3.21 (RBA F11 from P1-T020, ABS CPI from P1-T027); P4 R4.05 (StockTwits decision from P1-T056), store/monitor patterns, D02 intel overlays and positioning (P1-B012).
