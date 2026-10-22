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
updated: 2026-10-22
---

# Phase 1 · Market data, recording & live monitoring

## Summary

Free, clean, point-in-time market and macro data for every asset class at every timeframe from ticks to 1W, plus an always-on data-quality, cost and reconciliation monitor that alerts you through one fan-out to Telegram, ntfy and (if on) email ([roadmap](../../docs/roadmap/phase-1-data-and-monitoring.md)). Containers added: `ingest-market`, `ingest-batch`, `monitor`, `ntfy`, `telegram-bot` (alerts only), `ib-gateway` (only when IBKR is used). Dashboards: D07 Data & Quality, D02 Markets, the notification centre and the D16 egress tile.

Aligned on 2026-10-22 with [16](../../docs/16-configuration-and-safety-model.md) and [17](../../docs/17-decisions-register.md): every number is a configurable default linked to 16; stale means **data age** (now − our receive time) over per-bot thresholds (2 s fast / 60 s slow), flipped ≤ 250 ms p99 after the threshold; reconciliation runs at 60 s / 5 min / EOD; alerts use one fan-out; timeframes run tick → 1W; C3 completes via the break-glass CLI until Telegram C3 lands in P2. **Build first, keys last:** every keyed integration is built and tested keyless (fixtures, mocks, public endpoints); the live checks with your keys are the late VERIFY tasks P1-T073 (connectors) and P1-T074 (reconciliation), plus P1-T056 (provider checks) and P1-T060 (alert path).

74 tasks (6 USER · 47 BUILD · 6 OPS · 1 DOC · 13 VERIFY · 1 RUN) and 20 gaps (17 closed in the alignment, 3 open S3).

## Entry criteria

With `phase_gating: "dependencies"` each task waits only for its own `depends_on`, which name the Phase 0 tasks it needs (see Cross-phase prerequisites). The checklist below is the summary view.

- [ ] P0 platform tasks the P1 tasks depend on are done (Compose core, networks, sops → tmpfs, schemas and provenance columns, `pit`, WORM layer, `mt_api` with confirmation levels and the break-glass CLI, WS hub, web shell and component library, Grafana provisioning)
- [ ] Practice/testnet accounts exist (P0-T009): OANDA practice, IG demo, Alpaca paper, IBKR paper (if used), Binance + Bybit testnets; needed only by the live checks
- [ ] Free API keys in the sops file (P0-T010): FRED, EIA, CoinGecko Demo, Finnhub; needed only by the live checks
- [ ] Telegram bot created via @BotFather (P0-T002); chrony and Tailscale on the host (P0-T019)

## Exit criteria

- [ ] Grafana and D02 show live prices at every timeframe from ticks to 1W across crypto, FX/metals and ETFs, plus daily futures and macro (P1-T061, P1-T073, P1-T067)
- [ ] Live spread/funding/swap panels populate; reconciliation runs clean on practice accounts (P1-T064, P1-T073, P1-T074, P1-T067)
- [ ] A deliberately killed feed shows stale within 250 ms (p99) of its data-age threshold and the alert reaches Telegram, ntfy and (if on) email (P1-T057, P1-T060, P1-T067)
- [ ] Open provider checks are recorded in 06 (pass/fail) (P1-T056)
- [ ] All P1 tasks are done or cancelled
- [ ] No open S1/S2 bugs or gaps in phase 1

## Workstreams

| Workstream | Tasks |
|---|---|
| Your actions (USER) | P1-T001, P1-T002, P1-T003, P1-T066, P1-T068, P1-T069 |
| Platform & plumbing (OPS/BUILD) | P1-T004, P1-T005, P1-T006, P1-T007, P1-T008, P1-T009 |
| Crypto real-time & recording | P1-T010, P1-T011, P1-T012, P1-T013, P1-T014, P1-T015 |
| FX & metals | P1-T016, P1-T017, P1-T018, P1-T019, P1-T020 |
| Stocks/ETFs & daily futures | P1-T021, P1-T022, P1-T023 |
| Macro, rates, CPI & fundamentals | P1-T024, P1-T025, P1-T026, P1-T027, P1-T028, P1-T029 |
| DQ monitor (M16) | P1-T030, P1-T031, P1-T032, P1-T033, P1-T034, P1-T035, P1-T036, P1-T037 |
| Costs, reconciliation, venue health (M16) | P1-T038, P1-T039, P1-T040, P1-T041, P1-T042, P1-T043, P1-T070 |
| Egress safety check | P1-T071, P1-T072 |
| Alerts (M17) | P1-T044, P1-T045 |
| API & UI (D07, D02, notifications) | P1-T046, P1-T047, P1-T048, P1-T049, P1-T050, P1-T051 |
| Ops (storage, schedules, Grafana) & docs | P1-T052, P1-T053, P1-T054, P1-T055 |
| Verify (keyless) | P1-T057, P1-T058, P1-T059, P1-T061, P1-T062, P1-T063, P1-T064, P1-T067 |
| Verify (live, with your keys) | P1-T056, P1-T060, P1-T073, P1-T074 |
| Run | P1-T065 |
| Gaps | Closed: P1-B001…P1-B015, P1-B017, P1-B018 · Open: P1-B016, P1-B019, P1-B020 |

## Critical path

P0 platform (P0-T014/T016/T018/T020–T022) → P1-T004 → P1-T005 → P1-T007 → P1-T009 → P1-T010 → P1-T013 → P1-T046 → P1-T047 → P1-T049 → P1-T050 → P1-T061 → P1-T065 (7 elapsed days) → P1-T066 → P1-T067

The live branch joins at P1-T061: your keys (P0-T009, P0-T010, P1-T002) → P1-T073 → P1-T061. Start P1-T001 and P1-T002 early: the soak needs the universe, and the live checks need the keys; the builds themselves don't wait for either. Parallel lanes that must also finish before P1-T065/T067: recorder + bars (P1-T012/T013), DQ checks (P1-T031…T036) → P1-T057, alerts (P1-T044/T045) → P1-T060, reconciliation (P1-T041/T042) → P1-T074 → P1-T064, egress (P1-T071) → P1-T072, D07 (P1-T048), storage/schedules/Grafana (P1-T052/T053/T054).

## Traceability

### Requirements → tasks

| Requirement | Summary | Tasks |
|---|---|---|
| R1.01 | Crypto real-time: public WS trades, L1 and L2 (Binance, Bybit, OKX, Coinbase, Kraken) via… | P1-T001, P1-T004, P1-T005, P1-T010, P1-T011, P1-T061, P1-T067, P1-T073 |
| R1.02 | Recording: Parquet recorder (1–5 min files, daily compaction); bar builder writes 1s/1m b… | P1-T012, P1-T013, P1-T014, P1-T050, P1-T058, P1-T061, P1-T062, P1-T065, P1-T067 |
| R1.03 | Crypto history: data.binance.vision trades/aggTrades/1s klines backfill | P1-T015, P1-T067 |
| R1.04 | FX & metals: OANDA practice stream, IG demo stream, Dukascopy ticks, ECB/Frankfurter, RBA… | P1-T001, P1-T016, P1-T017, P1-T018, P1-T019, P1-T020, P1-T056, P1-T061, P1-T067, P1-T073 |
| R1.05 | Stocks/ETFs: Alpaca IEX real-time (30 symbols), yfinance daily, FinanceDatabase symbol ma… | P1-T001, P1-T009, P1-T021, P1-T022, P1-T023, P1-T056, P1-T061, P1-T067, P1-T073 |
| R1.06 | Futures/commodities (daily), rates & macro: yfinance futures, EIA, USDA, CFTC COT, Baker… | P1-T001, P1-T023, P1-T024, P1-T025, P1-T026, P1-T027, P1-T053, P1-T056, P1-T061, P1-T067, P1-T073 |
| R1.07 | Fundamentals: SEC EDGAR via edgartools (declared User-Agent, ≤ 10 req/s) | P1-T028, P1-T067 |
| R1.08 | Quota tracker per connector that throttles before each free limit | P1-T005, P1-T006, P1-T029, P1-T046, P1-T048, P1-T053, P1-T054, P1-T067, P1-T073 |
| R1.09 | Provenance: every ingested row tagged (`source`, `licence`, use flags); retention jobs en… | P1-T005, P1-T007, P1-T008, P1-T029, P1-T059, P1-T067 |
| R1.10 | DQ monitor: stale feed, gaps, bad ticks, cross-source divergence, clock skew, book integr… | P1-T004, P1-T030, P1-T031, P1-T032, P1-T033, P1-T034, P1-T035, P1-T036, P1-T037, P1-T046, P1-T048, P1-T054, P1-T055, P1-T057, P1-T065, P1-T066, P1-T067 |
| R1.11 | Cost monitor: fee tiers, funding (predicted + realised), swap/financing, `spread_bps` by… | P1-T002, P1-T038, P1-T039, P1-T040, P1-T046, P1-T048, P1-T054, P1-T064, P1-T067, P1-T073 |
| R1.12 | Reconciliation: vs each practice/testnet venue: positions and open orders every 60 s, bal… | P1-T002, P1-T041, P1-T042, P1-T046, P1-T048, P1-T055, P1-T064, P1-T067, P1-T070, P1-T074 |
| R1.13 | Venue-health monitor: our own measured withdrawal times, PoR/incident notes, venue status… | P1-T043, P1-T048, P1-T067, P1-T069 |
| R1.14 | Alerts, one fan-out: Grafana alerts → webhook → the `alert.*` consumer → Telegram + ntfy… | P1-T003, P1-T004, P1-T044, P1-T045, P1-T051, P1-T054, P1-T060, P1-T067, P1-T068 |
| R1.15 | UI: D07 (feeds, quotas, DQ events, costs, recon) and D02 (charts, cross-asset matrix, ins… | P1-T009, P1-T046, P1-T047, P1-T048, P1-T049, P1-T050, P1-T051, P1-T061, P1-T063, P1-T067 |
| R1.N1 | Feed staleness: `dq.status` → stale within ≤ 250 ms (p99) of the data-age threshold being… | P1-T031, P1-T057, P1-T062, P1-T067 |
| R1.N2 | UI live update lag p95 < 500 ms; server throttles ≤ 4 Hz charts, ≤ 1 Hz tables | P1-T047, P1-T062, P1-T067 |
| R1.N3 | Storage within budget (~0.3–1 TB/year for ~10 liquid crypto symbols at trades + L1 + 1 s… | P1-T012, P1-T052, P1-T055, P1-T065, P1-T067 |
| R1.16 | Egress check: every minute, confirm exchange traffic leaves via the allow-listed static I… | P1-T067, P1-T071, P1-T072 |
| R1.17 | Data age definition: age = now − our receive time per stream; per-bot thresholds (default… | P1-T030, P1-T031, P1-T057, P1-T062, P1-T067 |

### Roadmap ToDos → tasks

| ToDo | Summary | Tasks |
|---|---|---|
| T1.01 | `USER` Pick the starting universe/watchlist: ~10 crypto pairs, FX/metal pairs, ~30 US… | P1-T001 |
| T1.02 | `USER` Create read-only API keys where the testnet offers them (Binance/Bybit testnets… | P1-T002 |
| T1.03 | `USER` Install the ntfy app on your phone and subscribe to the private topic; confirm… | P1-T003 |
| T1.04 | `USER` Review the first week's DQ alerts and tell us which thresholds are too noisy. | P1-T066 |
| T1.05 | `USER` Create an SMTP app password at your own mail provider and put it in the secrets… | P1-T068 |
| T1.06 | `USER` Each quarter, when the reminder arrives, check every venue you use on the AUSTR… | P1-T069 |
| T1.20 | `BUILD` `mt_data.market` crypto WS clients via Nautilus data clients/ccxt; publish `md.… | P1-T004, P1-T005, P1-T010, P1-T011 |
| T1.21 | `BUILD` Parquet recorder + daily compaction; bar builder (1s/1m) + Timescale continuous… | P1-T012, P1-T013, P1-T014 |
| T1.22 | `BUILD` Backfill flows: data.binance.vision, Dukascopy (dukascopy-node or own bi5 parse… | P1-T015, P1-T018, P1-T022, P1-T023 |
| T1.23 | `BUILD` FX/metals streaming: OANDA v20 practice, IG Lightstreamer demo; Frankfurter sel… | P1-T016, P1-T017, P1-T019, P1-T020 |
| T1.24 | `BUILD` Macro/rates/fundamentals Prefect flows: FRED/ALFRED (vintages), Treasury, `sdmx… | P1-T024, P1-T025, P1-T026, P1-T027, P1-T028 |
| T1.25 | `BUILD` Quota tracker (per-connector budgets from live headers where available) shared… | P1-T006 |
| T1.26 | `BUILD` Provenance tagging at write time (defaults from each source's licence tag in 06… | P1-T007, P1-T008, P1-T029 |
| T1.27 | `BUILD` `mt_monitor` DQ service: per-instrument rolling state, checks table, `dq.status… | P1-T004, P1-T030, P1-T031, P1-T032, P1-T033, P1-T034, P1-T035, P1-T036, P1-T037 |
| T1.28 | `BUILD` `mt_monitor` cost service: fees/tiers, funding, financing, spreads by hour-of-w… | P1-T038, P1-T039, P1-T040, P1-T064 |
| T1.29 | `BUILD` Reconciliation jobs (ccxt read-only, OANDA, IG, Alpaca, IBKR paper), built and… | P1-T041, P1-T042, P1-T064 |
| T1.30 | `BUILD` Venue-health collector writing to `ops.venue_registry` health fields from our o… | P1-T043 |
| T1.31 | `BUILD` Telegram bot (alerts only) + ntfy + email notifier behind one `alert.{severity}… | P1-T004, P1-T045 |
| T1.32 | `BUILD` UI: D07 Data & Quality, D02 Markets (lightweight-charts, matrix, instrument det… | P1-T009, P1-T046, P1-T047, P1-T048, P1-T049, P1-T050, P1-T051, P1-T063 |
| T1.33 | `BUILD` Egress IP/country check with GeoIP DB; `egress.status` → M11 + alerts | P1-T071 |
| T1.34 | `BUILD` Alpaca real-time stream, FinanceDatabase symbol master and `exchange_calendars`… | P1-T009, P1-T021, P1-T029 |
| T1.40 | `OPS` Storage layout: NVMe hot Parquet, HDD cold tier, compaction schedule, disk aler… | P1-T052 |
| T1.41 | `OPS` Prefect schedules for batch flows (respecting quotas and source update times, A… | P1-T053 |
| T1.42 | `OPS` Grafana boards: live prices by timeframe, spreads/funding/swaps, DQ incidents,… | P1-T054 |
| T1.43 | `OPS` ntfy container (self-hosted, auth on, Tailscale only; upstream relay allowed fo… | P1-T044 |
| T1.44 | `OPS` `ib-gateway` container (IBC-managed, digest-pinned, read-only API for reconcili… | P1-T070 |
| T1.60 | `VERIFY` Run the open provider checks: OANDA order/position books, TrueFX, IMF SDMX 3.0… | P1-T056, P1-T067 |
| T1.61 | `VERIFY` DQ fault injection: kill a feed (status stale ≤ 250 ms p99 after its data-age t… | P1-T057, P1-T067 |
| T1.62 | `VERIFY` Bar parity: Timescale aggregates vs bars rebuilt from Parquet ticks for a sampl… | P1-T058, P1-T067 |
| T1.63 | `VERIFY` Provenance/retention test: CoinGecko rows deleted after 24 h; untagged rows rej… | P1-T059, P1-T067 |
| T1.64 | `VERIFY` Alert path test on all three channels. | P1-T060, P1-T067 |
| T1.65 | `VERIFY` Egress fault test: wrong egress IP or country → new orders blocked and alerted | P1-T072 |
| T1.66 | `VERIFY` Live connector check with your credentials and keys (after T0.09, T0.10, T1.02)… | P1-T073 |
| T1.67 | `VERIFY` Live reconciliation on practice/testnet accounts with your keys (after T1.02):… | P1-T074 |
| T1.80 | `RUN` 7-day continuous recording soak; gap report per instrument; disk growth vs budg… | P1-T065, P1-T067 |

All requirements (R1.01–R1.17, R1.N1–R1.N3) and ToDos (T1.01–T1.80) are covered. Tasks without a roadmap ToDo of their own (traced by requirement): P1-T055 (runbooks), P1-T061 (F1 end-to-end), P1-T062 (load + UI lag).

## Planning notes & risks

- **Stale = data age (closed P1-B001):** now − our receive time per stream on the monotonic clock; per-bot thresholds (2 s fast / 60 s slow) from settings; closed sessions are `closed`; `stale` within ≤ 250 ms p99 of the threshold (P1-T030/T031, proven in P1-T057/T062). M11's inline order-time check lands in P2 (R2.58).
- **Build first, keys last:** OANDA, IG, Alpaca, FRED, EIA, CoinGecko, Finnhub, testnet fee tiers, financing and reconciliation are built against fixtures; P1-T073 and P1-T074 carry the `env` names and depend on your key tasks. A connector without its secret starts as `credentials_missing`, never crashes.
- **Disk (R1.N3, closed P1-B002):** native L2 diffs only for ≤ 3 order-book symbols by default, 1 s snapshots for the rest; P1-T052 sheds L2 before quotes and never trades; the soak recalculates the budget.
- **Timeframes (closed P1-B011):** `market.bar_1s` hypertable + continuous aggregates 1m…1W; vendor bars (`bar_1s_vendor`, `bar_1m_vendor`, `bar_daily_vendor`) never mix into the aggregates.
- **Alerts (closed P1-B005/B006/B007):** one fan-out (Grafana → webhook → `alert.*` consumer → Telegram/ntfy/email); P1-T045 removes P0's direct Alertmanager → Telegram route; email is your provider's SMTP app password or off (P1-T068); ntfy iOS push via the upstream relay (message ID only). Open: where the consumer sits on the networks (P1-B020, S3).
- **C3 in P1 (closed P1-B009):** loosening DQ thresholds, alert routing, egress settings or venue access completes via the break-glass CLI `mtctl approve` + TOTP until Telegram C3 lands in P2.
- **Reconciliation (closed P1-B008/B013/B017):** 60 s / 5 min / EOD Sydney, exact positions, balances within 0.01% or dust; practice accounts use normal credentials with a GET-only client allow-list as a second safeguard; IBKR via the opt-in `ib-gateway` (P1-T070). In P1 every mismatch is `unexplained` (no journal until P3); the 24 h halt is M11's from P2.
- **WORM / canonical names (closed P1-B010/B018):** P1 adds `audit.dq_event`, `audit.dq_ack`, `audit.cost_event` (incl. TCA rows; no `audit.tca`) and `audit.recon`; each carries the 15 §2.4 tests. Acks are new rows via `data.incident.ack`.
- **Venue health (closed P1-B014):** our measured withdrawal times, flags and your notes in P1; status pages/feeds join via the P4 venue watch (R4.15); the quarterly AUSTRAC check is your task P1-T069.
- **Egress (R1.16):** P1-T071 checks the allow-listed IP and country every minute; before the P7 exit node the expected IP is the one your testnet keys are allow-listed to. Safety only, never a tax input.
- **Open gaps:** P1-B016 (ABS CPI series ID A2325846C is (U); verified in P1-T056), P1-B019 (USDA QuickStats key not in T0.10; QuickStats ships disabled meanwhile), P1-B020 (alert consumer network placement; interim placement in P1-T045).
- **IEX ≠ NBBO:** flagged on every Alpaca message and in D02; no scalping-cost conclusions from IEX data.
- **Order surfaces:** D02's order ticket is present but disabled; no P1 code places orders.
- **Soak timing:** P1-T065 needs 7 elapsed days with frozen config; plan the exit demo for a window when US equities, FX and crypto are all open.

## Cross-phase prerequisites

These are explicit `depends_on` entries on the tasks (no phase gate):

| P0 task | Used by |
|---|---|
| P0-T002 Telegram bot (your T0.06) | P1-T060 |
| P0-T003 tailnet (your T0.03) | P1-T003 |
| P0-T009 practice/testnet accounts (your T0.09) | P1-T002, P1-T056, P1-T073, P1-T074 |
| P0-T010 free API keys (your T0.10) | P1-T073 |
| P0-T014 monorepo skeleton · P0-T017 settings + clock | P1-T005 |
| P0-T016 `mt_core` schemas · P0-T018 `mt_obs` · P0-T020 Compose core · P0-T021 networks · P0-T022 sops → tmpfs | P1-T004 (P0-T020/T021 also P1-T044, P1-T070; P0-T022 also P1-T070) |
| P0-T019 host hardening (Tailscale, chrony metric) | P1-T035, P1-T044 |
| P0-T023 Alertmanager/Grafana · P0-T045 Grafana provisioning | P1-T045, P1-T054 |
| P0-T024 schemas/roles/Alembic · P0-T025 provenance columns + `ops.venue_registry` | P1-T007, P1-T043 |
| P0-T026 venue registry seeded | P1-T069 |
| P0-T027 `pit` + Parquet catalog helpers | P1-T008, P1-T012, P1-T020, P1-T024 |
| P0-T029 WORM privileges · P0-T030 hash chain | P1-T030, P1-T038, P1-T041 |
| P0-T032 `mt_api` · P0-T034 command bus · P0-T035 confirmation levels + break-glass | P1-T046 (P0-T035 also P1-T030, P1-T071) |
| P0-T036 WS hub · P0-T048 typed clients | P1-T047 |
| P0-T049 component library · P0-T050 app shell | P1-T048, P1-T049 (P0-T050 also P1-T051) |
| P0-T051 D16 Health page | P1-T071 |
| P0-T053 Playwright viewport matrix | P1-T063 |

**Consumers downstream:** P2 R2.16/R2.58 (DQ status and inline data-age, egress and integrity checks in M11), R2.34/T2.26 (TCA on paper fills uses the P1-T040 scaffold), R2.40 (measured costs), R2.52 (Telegram commands extend the P1 alerts bot); P3 R3.03/T3.21 (RBA F11 from P1-T020, ABS CPI from P1-T027); P4 R4.05 (StockTwits result from P1-T056), R4.11/T4.32 (the "Arrives in Phase 4" D02 widgets), R4.15/T4.30 (venue-status signals into P1-T043); P7 R7.14/T7.42 (the egress check points at the static exit node).
