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
updated: 2026-11-20
---

# Phase 1 · Market data, recording & live monitoring

## Summary

Free, clean, point-in-time market and macro data for every asset class at every timeframe from ticks to 1W, plus an always-on data-quality, cost and reconciliation monitor that alerts you through one fan-out to Telegram, ntfy and (if on) email ([roadmap](../../docs/roadmap/phase-1-data-and-monitoring.md)). Containers added: `ingest-market` (`mt-recorder`, Rust), `scheduler` and `research-worker` (`mt-scheduler`, Rust; replaces Prefect), `ingest-batch` (`mt-connectors` jobs on `mt-scheduler`, Rust), `monitor` (`mt-monitor`, Rust), `ntfy`, `telegram-bot` (`mt-telegram-bot`, Rust; alerts only), `ib-gateway` (only when IBKR is used). Dashboards: D07 Data & Quality, D02 Markets, the notification centre and the D16 egress tile.

Aligned on 2026-10-22 with [16](../../docs/16-configuration-and-safety-model.md) and [17](../../docs/17-decisions-register.md): every number is a configurable default linked to 16; stale means **data age** (now − our receive time) over per-bot thresholds (2 s fast / 60 s slow), flipped ≤ 250 ms p99 after the threshold; reconciliation runs at 60 s / 5 min / EOD; alerts use one fan-out; timeframes run tick → 1W; C3 completes via the break-glass CLI until Telegram C3 lands in P2. **Build first, keys last:** every keyed integration is built and tested keyless (fixtures, mocks, public endpoints); the live checks with your keys are the late VERIFY tasks P1-T073 (connectors) and P1-T074 (reconciliation), plus P1-T056 (provider checks) and P1-T060 (alert path).

Re-platformed on 2026-11-19 per [18](../../docs/18-platform-and-deployment.md) ([17 §G](../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19)): streaming, bars, DQ/cost/recon/egress and the alert bot are Rust (`mt-recorder`, `mt-monitor`, `mt-telegram-bot`, `mt-api`, `mt-store`); batch flows that need Python-only SDKs (Prefect, OpenBB, edgartools, fredapi, sdmx1, yfinance, FinanceDatabase, Pandera/Evidently) stay Python; the database is Supabase Postgres with **no TimescaleDB**: `mt-recorder` writes 1s and every standard bar size into monthly partitions (P1-T013), a partition job keeps them ahead and exports old bars to Parquet (P1-T075), a rebuild/rollup job handles backfills and corrections (P1-T076), and other sizes are `date_bin` reads in `pit`. Everything runs on the workstation; Tailscale is optional until go-live, so the phone ntfy subscription (P1-T003) is a pre-go-live USER step no agent task waits on. The universe (P1-T001) and DQ tuning (P1-T066, tightening only) are now agent tasks reviewed in the go-live pack (P7-T070).

Rust-max on 2026-11-20 per [18 §2](../../docs/18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary) and [17 §H](../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20): Prefect is replaced by **`mt-scheduler`** (P1-T077 skeleton, P1-T079 VERIFY for T1.68, P1-T080 moves the P0 host-timer jobs and wires `system.backup.run`/`system.restore.test`, P1-T053 schedules); OpenBB, fredapi, sdmx1, edgartools and yfinance are replaced by typed Rust clients in **`mt-connectors`** (P1-T078 base; SEC XBRL via `companyfacts` JSON; own Rust Dukascopy `bi5` parser); daily stock/ETF/futures bars come only from sources whose terms allow automated personal use (P1-T023 re-scoped: terms check first, Yahoo only if allowed (U)). Python stays only as `mt_research` offline jobs run by `mt-scheduler`: the nightly Pandera/Evidently report (P1-T037), the `exchange_calendars` session tables (P1-T009) and the independent bar-parity checker (P1-T058). E2E suites are Rust (`tests/e2e`, `mt-e2e` crate) with the same cases.

80 tasks (4 USER · 52 BUILD · 8 OPS · 1 DOC · 14 VERIFY · 1 RUN) and 20 gaps (17 closed in the alignment, 3 open S3).

## Entry criteria

With `phase_gating: "dependencies"` each task waits only for its own `depends_on`, which name the Phase 0 tasks it needs (see Cross-phase prerequisites). The checklist below is the summary view.

- [ ] P0 platform tasks the P1 tasks depend on are done (Compose core with the Supabase stack, networks, sops → tmpfs, Supabase migrations with schemas and provenance columns, `pit` in `mt-store` with its Python binding, WORM layer, `mt-api` with confirmation levels and the break-glass CLI, WS hub, web shell and component library, Grafana provisioning)
- [ ] Practice/testnet accounts exist (P0-T009): OANDA practice, IG demo, Alpaca paper, IBKR paper (if used), Binance + Bybit testnets; needed only by the live checks
- [ ] Free API keys in the sops file (P0-T010): FRED, EIA, CoinGecko Demo, Finnhub; needed only by the live checks
- [ ] Telegram bot created via @BotFather (P0-T002), needed only by the live alert check (P1-T060); chrony on the workstation (P0-T019). Tailscale (P0-T003) is optional until go-live

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
| Your actions (USER) | P1-T002 (keys), P1-T068 (SMTP password or email off), P1-T069 (quarterly AUSTRAC check), P1-T003 (phone ntfy, before go-live) |
| Agent seeds and tuning (were USER) | P1-T001 (seed the universe), P1-T066 (tune DQ thresholds, tightening only) |
| Platform & plumbing (OPS/BUILD) | P1-T004, P1-T005, P1-T006, P1-T007, P1-T008, P1-T009 |
| Batch platform: scheduler & connectors | P1-T077 (`mt-scheduler`), P1-T078 (`mt-connectors`), P1-T080 (P0 timer jobs → scheduler), P1-T053 (schedules + `ingest-batch`), P1-T079 (VERIFY) |
| Crypto real-time & recording | P1-T010, P1-T011, P1-T012, P1-T013, P1-T014, P1-T015, P1-T075 (partitions + Parquet export), P1-T076 (rebuild/rollup) |
| FX & metals | P1-T016, P1-T017, P1-T018, P1-T019, P1-T020 |
| Stocks/ETFs & daily futures | P1-T021, P1-T022, P1-T023 |
| Macro, rates, CPI & fundamentals | P1-T024, P1-T025, P1-T026, P1-T027, P1-T028, P1-T029 |
| DQ monitor (M16) | P1-T030, P1-T031, P1-T032, P1-T033, P1-T034, P1-T035, P1-T036, P1-T037 |
| Costs, reconciliation, venue health (M16) | P1-T038, P1-T039, P1-T040, P1-T041, P1-T042, P1-T043, P1-T070 |
| Egress safety check | P1-T071, P1-T072 |
| Alerts (M17) | P1-T044, P1-T045 |
| API & UI (D07, D02, notifications) | P1-T046, P1-T047, P1-T048, P1-T049, P1-T050, P1-T051 |
| Ops (storage, schedules, Grafana) & docs | P1-T052, P1-T053, P1-T054, P1-T055 |
| Verify (keyless) | P1-T057, P1-T058, P1-T059, P1-T062, P1-T063, P1-T079 |
| Verify (live, with your keys) | P1-T056, P1-T060, P1-T061, P1-T064, P1-T073, P1-T074, P1-T067 (exit demo) |
| Run | P1-T065 |
| Gaps | Closed: P1-B001…P1-B015, P1-B017, P1-B018 · Open: P1-B016, P1-B019, P1-B020 |

## Critical path

P0 platform (P0-T014/T016/T018/T020–T022) → P1-T004 → P1-T005 → P1-T007 → P1-T009 → P1-T010 → P1-T013 → P1-T075/P1-T076 → P1-T065 (7 elapsed days) → P1-T066 → P1-T067; the UI lane P1-T013 → P1-T046 → P1-T047 → P1-T049 → P1-T050 → P1-T061 joins at the exit demo

The live branch joins at the exit demo: your keys (P0-T009, P0-T010, P1-T002) → P1-T073/P1-T074 → P1-T061/P1-T064 → P1-T067. The soak (P1-T065) runs on the agent-seeded universe (P1-T001) and never waits for your keys; keyed feeds without credentials run as `credentials_missing`. Do P1-T002 early so the live checks aren't the last thing left. Parallel lanes that must also finish before P1-T065/T067: recorder + bars (P1-T012/T013/T075/T076), DQ checks (P1-T031…T036) → P1-T057, alerts (P1-T044/T045) → P1-T060, reconciliation (P1-T041/T042) → P1-T074 → P1-T064, egress (P1-T071) → P1-T072, D07 (P1-T048), storage/schedules/Grafana (P1-T052/T053/T054), and the batch lane P1-T005 → P1-T006/T007 → P1-T078 → the `mt-connectors` providers → P1-T053 (with P1-T077) → P1-T079; P1-T080 follows P1-T077 once the P0 timer jobs exist.

## Traceability

### Requirements → tasks

| Requirement | Summary | Tasks |
|---|---|---|
| R1.01 | Crypto real-time: public WS trades, L1 and L2 (Binance, Bybit, OKX, Coinbase, Kraken) via… | P1-T001, P1-T004, P1-T005, P1-T010, P1-T011, P1-T061, P1-T067, P1-T073 |
| R1.02 | Recording: `mt-recorder` Parquet catalog (1–5 min files, daily compaction); bars at every standard size in monthly partitions… | P1-T012, P1-T013, P1-T014, P1-T050, P1-T058, P1-T061, P1-T062, P1-T065, P1-T067, P1-T075, P1-T076 |
| R1.03 | Crypto history: data.binance.vision trades/aggTrades/1s klines backfill | P1-T015, P1-T067 |
| R1.04 | FX & metals: OANDA practice stream, IG demo stream, Dukascopy ticks, ECB/Frankfurter, RBA… | P1-T001, P1-T016, P1-T017, P1-T018, P1-T019, P1-T020, P1-T056, P1-T061, P1-T067, P1-T073 |
| R1.05 | Stocks/ETFs: Alpaca IEX real-time (30 symbols), daily bars via `mt-connectors` from terms-checked sources, FinanceDatabase… | P1-T001, P1-T009, P1-T021, P1-T022, P1-T023, P1-T056, P1-T061, P1-T067, P1-T073 |
| R1.06 | Futures/commodities (daily), rates & macro: daily futures via `mt-connectors`, EIA, USDA, CFTC COT, Baker… | P1-T001, P1-T023, P1-T024, P1-T025, P1-T026, P1-T027, P1-T053, P1-T056, P1-T061, P1-T067, P1-T073 |
| R1.07 | Fundamentals: SEC EDGAR submissions and XBRL `companyfacts` JSON via `mt-connectors` (declared User-Agent, ≤ 10 req/s) | P1-T028, P1-T067 |
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
| R1.N3 | Storage within budget (~0.3–1 TB/year for ~10 liquid crypto symbols at trades + L1 + 1 s… | P1-T012, P1-T052, P1-T055, P1-T065, P1-T067, P1-T075 |
| R1.16 | Egress check: every minute, confirm exchange traffic leaves via the allow-listed static I… | P1-T067, P1-T071, P1-T072 |
| R1.18 | Batch orchestration: `mt-scheduler` (Rust; replaces Prefect): Postgres-backed jobs and cron, retries, backfills, run history, D16/D07 status | P1-T037, P1-T053, P1-T077, P1-T079, P1-T080 |
| R1.19 | Batch connectors: typed Rust clients in `mt-connectors` (replacing OpenBB, fredapi, sdmx1, edgartools, yfinance) writing through `pit` with provenance | P1-T023, P1-T053, P1-T078 |
| R1.17 | Data age definition: age = now − our receive time per stream; per-bot thresholds (default… | P1-T030, P1-T031, P1-T057, P1-T062, P1-T067 |

### Roadmap ToDos → tasks

| ToDo | Summary | Tasks |
|---|---|---|
| T1.01 | Seed the starting universe/watchlist from the docs' default lists (agent; was `USER`, reviewed in P7-T070) | P1-T001 |
| T1.02 | `USER` Create read-only API keys where the testnet offers them (Binance/Bybit testnets… | P1-T002 |
| T1.03 | `USER` Install the ntfy app on your phone and subscribe over Tailscale (before go-live; the email address moved to T1.05) | P1-T003 |
| T1.04 | Tune noisy DQ thresholds from the soak week's stats, tightening only (agent; was `USER`; loosening proposals go to P7-T070) | P1-T066 |
| T1.05 | `USER` Create an SMTP app password at your own mail provider and put it in the secrets… | P1-T068 |
| T1.06 | `USER` Each quarter, when the reminder arrives, check every venue you use on the AUSTR… | P1-T069 |
| T1.20 | `BUILD` `mt-recorder` crypto WS clients via Nautilus Rust data clients (where available (U)); publish `md.*` | P1-T004, P1-T005, P1-T010, P1-T011 |
| T1.21 | `BUILD` Parquet recorder + daily compaction; bar builder writing every standard size to monthly partitions; rollup job; `date_bin` reads | P1-T012, P1-T013, P1-T014, P1-T075, P1-T076 |
| T1.22 | `BUILD` Backfill jobs in `mt-connectors`: data.binance.vision, Dukascopy (own `bi5` parser), Alpaca history, daily bars (terms permitting) | P1-T015, P1-T018, P1-T022, P1-T023 |
| T1.23 | `BUILD` FX/metals streaming: OANDA v20 practice, IG Lightstreamer demo; Frankfurter sel… | P1-T016, P1-T017, P1-T019, P1-T020 |
| T1.24 | `BUILD` Macro/rates/fundamentals clients in `mt-connectors`: FRED/ALFRED (vintages), Treasury, SDMX, central banks, EIA/USDA/COT/Baker Hughes, ABS CPI, SEC EDGAR | P1-T024, P1-T025, P1-T026, P1-T027, P1-T028 |
| T1.25 | `BUILD` Quota tracker (per-connector budgets from live headers where available) shared… | P1-T006 |
| T1.26 | `BUILD` Provenance tagging at write time (defaults from each source's licence tag in 06… | P1-T007, P1-T008, P1-T029 |
| T1.27 | `BUILD` `mt-monitor` DQ service: per-instrument rolling state, checks table, `dq.status… | P1-T004, P1-T030, P1-T031, P1-T032, P1-T033, P1-T034, P1-T035, P1-T036, P1-T037 |
| T1.28 | `BUILD` `mt-monitor` cost service: fees/tiers, funding, financing, spreads by hour-of-w… | P1-T038, P1-T039, P1-T040, P1-T064 |
| T1.29 | `BUILD` Reconciliation jobs (read-only Rust venue clients: crypto testnets, OANDA, IG, Alpaca, IBKR paper), built and… | P1-T041, P1-T042, P1-T064 |
| T1.30 | `BUILD` Venue-health collector writing to `ops.venue_registry` health fields from our o… | P1-T043 |
| T1.31 | `BUILD` Telegram bot (`mt-telegram-bot`, alerts only) + ntfy + email notifier behind one `alert.{severity}… | P1-T004, P1-T045 |
| T1.32 | `BUILD` UI: D07 Data & Quality, D02 Markets (lightweight-charts, matrix, instrument det… | P1-T009, P1-T046, P1-T047, P1-T048, P1-T049, P1-T050, P1-T051, P1-T063 |
| T1.33 | `BUILD` Egress IP/country check with GeoIP DB; `egress.status` → M11 + alerts | P1-T071 |
| T1.34 | `BUILD` Alpaca real-time stream, FinanceDatabase symbol master and `exchange_calendars`… | P1-T009, P1-T021, P1-T029 |
| T1.40 | `OPS` Storage layout: NVMe hot Parquet, HDD cold tier, compaction schedule, disk aler… | P1-T052 |
| T1.35 | `BUILD` `mt-scheduler` skeleton: Postgres-backed jobs and cron, retries, backfills, run history, job-status API; move the P0 jobs onto it | P1-T077, P1-T080 |
| T1.36 | `BUILD` `mt-connectors` crate skeleton: shared HTTP client, quota hook, provenance, `pit` writer, fixture harness | P1-T078 |
| T1.41 | `OPS` `mt-scheduler` schedules for the batch jobs (respecting quotas and source update times, A… | P1-T053 |
| T1.42 | `OPS` Grafana boards: live prices by timeframe, spreads/funding/swaps, DQ incidents,… | P1-T054 |
| T1.43 | `OPS` ntfy container (self-hosted, auth on, private: localhost on the workstation, Tailscale once it exists; upstream relay for iOS) | P1-T044 |
| T1.44 | `OPS` `ib-gateway` container (IBC-managed, digest-pinned, read-only API for reconcili… | P1-T070 |
| T1.60 | `VERIFY` Run the open provider checks: OANDA order/position books, TrueFX, IMF SDMX 3.0… | P1-T056, P1-T067 |
| T1.61 | `VERIFY` DQ fault injection: kill a feed (status stale ≤ 250 ms p99 after its data-age t… | P1-T057, P1-T067 |
| T1.62 | `VERIFY` Bar parity: recorder-written bars at every standard size vs bars rebuilt from Parquet ticks; rollup output after a seeded backfill | P1-T058, P1-T067 |
| T1.63 | `VERIFY` Provenance/retention test: CoinGecko rows deleted after 24 h; untagged rows rej… | P1-T059, P1-T067 |
| T1.64 | `VERIFY` Alert path test on all three channels. | P1-T060, P1-T067 |
| T1.65 | `VERIFY` Egress fault test: wrong egress IP or country → new orders blocked and alerted | P1-T072 |
| T1.66 | `VERIFY` Live connector check with your credentials and keys (after T0.09, T0.10, T1.02)… | P1-T073 |
| T1.68 | `VERIFY` Scheduler test: retries, backfill resume after restart, cron run history, D16 job status | P1-T079, P1-T067 |
| T1.67 | `VERIFY` Live reconciliation on practice/testnet accounts with your keys (after T1.02):… | P1-T074 |
| T1.80 | `RUN` 7-day continuous recording soak; gap report per instrument; disk growth vs budg… | P1-T065, P1-T067 |

All requirements (R1.01–R1.19, R1.N1–R1.N3) and ToDos (T1.01–T1.80, incl. T1.35, T1.36, T1.68) are covered. Tasks without a roadmap ToDo of their own (traced by requirement): P1-T055 (runbooks), P1-T061 (F1 end-to-end), P1-T062 (load + UI lag).

## Planning notes & risks

- **Stale = data age (closed P1-B001):** now − our receive time per stream on the monotonic clock; per-bot thresholds (2 s fast / 60 s slow) from settings; closed sessions are `closed`; `stale` within ≤ 250 ms p99 of the threshold (P1-T030/T031, proven in P1-T057/T062). M11's inline order-time check lands in P2 (R2.58).
- **Build first, keys last:** OANDA, IG, Alpaca, FRED, EIA, CoinGecko, Finnhub, testnet fee tiers, financing and reconciliation are built against fixtures; P1-T073 and P1-T074 carry the `env` names and depend on your key tasks. A connector without its secret starts as `credentials_missing`, never crashes.
- **Disk (R1.N3, closed P1-B002):** native L2 diffs only for ≤ 3 order-book symbols by default, 1 s snapshots for the rest; P1-T052 sheds L2 before quotes and never trades; the soak recalculates the budget.
- **Timeframes (closed P1-B011; re-platformed 2026-11-19, [18 §4.3](../../docs/18-platform-and-deployment.md#43-bars-without-timescaledb)):** no TimescaleDB. `mt-recorder` writes `market.bar_1s` and every standard size (1m…1W) into monthly native partitions (P1-T013); P1-T075 creates partitions ahead (pg_partman if available (U), else an `mt-store` job via pg_cron) and exports 1s bars after `db.bars_1s_hot_days` to Parquet; P1-T076 rebuilds and rolls up after backfills and corrections; other sizes are `date_bin` reads in `pit`. Vendor bars (`bar_1s_vendor`, `bar_1m_vendor`, `bar_daily_vendor`) never mix into built bars.
- **Alerts (closed P1-B005/B006/B007):** one fan-out (Grafana → webhook → `alert.*` consumer → Telegram/ntfy/email); P1-T045 removes P0's direct Alertmanager → Telegram route; email is your provider's SMTP app password or off (P1-T068, which also holds the destination address); ntfy iOS push via the upstream relay (message ID only). Workstation first: P1-T060 checks ntfy with a subscriber on the workstation; the phone subscription over Tailscale (P1-T003) is done before go-live. Open: where the consumer sits on the networks (P1-B020, S3).
- **C3 in P1 (closed P1-B009):** loosening DQ thresholds, alert routing, egress settings or venue access completes via the break-glass CLI `mtctl approve` + TOTP until Telegram C3 lands in P2.
- **Reconciliation (closed P1-B008/B013/B017):** 60 s / 5 min / EOD Sydney, exact positions, balances within 0.01% or dust; practice accounts use normal credentials with a GET-only client allow-list as a second safeguard; IBKR via the opt-in `ib-gateway` (P1-T070). In P1 every mismatch is `unexplained` (no journal until P3); the 24 h halt is M11's from P2.
- **WORM / canonical names (closed P1-B010/B018):** P1 adds `audit.dq_event`, `audit.dq_ack`, `audit.cost_event` (incl. TCA rows; no `audit.tca`) and `audit.recon`; each carries the 15 §2.4 tests. Acks are new rows via `data.incident.ack`.
- **Venue health (closed P1-B014):** our measured withdrawal times, flags and your notes in P1; status pages/feeds join via the P4 venue watch (R4.15); the quarterly AUSTRAC check is your task P1-T069.
- **Egress (R1.16):** P1-T071 checks the allow-listed IP and country every minute; before the P7 exit node the expected IP is the one your testnet keys are allow-listed to. Safety only, never a tax input.
- **Open gaps:** P1-B016 (ABS CPI series ID A2325846C is (U); verified in P1-T056), P1-B019 (USDA QuickStats key not in T0.10; QuickStats ships disabled meanwhile), P1-B020 (alert consumer network placement; interim placement in P1-T045).
- **IEX ≠ NBBO:** flagged on every Alpaca message and in D02; no scalping-cost conclusions from IEX data.
- **Order surfaces:** D02's order ticket is present but disabled; no P1 code places orders.
- **Language split ([18 §2](../../docs/18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary), Rust-max [17 §H](../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20)):** Rust for streaming connectors, recorder, bars, batch connectors (`mt-connectors`), the scheduler (`mt-scheduler`), DQ/cost/recon/egress, the alert bot and the API; Python only for `mt_research` offline jobs run by `mt-scheduler` (Pandera/Evidently report, `exchange_calendars` tables, the independent bar-parity checker). Every batch source has a `terms` verdict in `config/sources.yaml` before it can run (Yahoo (U), P1-T023). No ccxt in the Rust path: venue REST via Nautilus Rust clients where available (U) or thin GET-only `reqwest` clients. Open (U) checks are the first ToDo of the task that relies on them: Nautilus Rust data clients (P1-T010/T011), Rust Lightstreamer (P1-T017), Rust TWS client (P1-T042), pg_partman on Postgres 17 (P1-T075).
- **Soak timing:** P1-T065 needs 7 elapsed days with frozen config; plan the exit demo for a window when US equities, FX and crypto are all open.

## Cross-phase prerequisites

These are explicit `depends_on` entries on the tasks (no phase gate):

| P0 task | Used by |
|---|---|
| P0-T002 Telegram bot (your T0.06) | P1-T060 |
| P0-T003 tailnet (your T0.03; optional until go-live) | P1-T003 (pre-go-live phone step only) |
| P0-T009 practice/testnet accounts (your T0.09) | P1-T002, P1-T056, P1-T073, P1-T074 |
| P0-T010 free API keys (your T0.10) | P1-T073 |
| P0-T014 monorepo skeleton · P0-T017 settings + clock | P1-T005 |
| P0-T018 `mt-obs` · P0-T024 migrations/roles (`mt_jobs_rw`) · P0-T034 command bus · P0-T051 D16 page | P1-T077 |
| P0-T037 seal · P0-T038 verify · P0-T039 backups · P0-T040 WORM export · P0-T041 restore test (host timers) | P1-T080 |
| P0-T016 `mt-core` schemas · P0-T018 `mt-obs` · P0-T020 Compose core (incl. Supabase stack) · P0-T021 networks · P0-T022 sops → tmpfs | P1-T004 (P0-T020/T021 also P1-T044, P1-T070; P0-T022 also P1-T070) |
| P0-T019 workstation baseline (chrony metric; no Tailscale precondition) | P1-T035 |
| P0-T023 Alertmanager/Grafana · P0-T045 Grafana provisioning | P1-T045, P1-T054 |
| P0-T024 schemas/roles/Supabase migrations baseline · P0-T025 provenance columns + `ops.venue_registry` | P1-T007, P1-T043 |
| P0-T026 venue registry seeded | P1-T069 |
| P0-T027 `pit` (`mt-store` + Python binding) + Parquet catalog helpers | P1-T008, P1-T012, P1-T020, P1-T024, P1-T075, P1-T078 |
| P0-T029 WORM privileges · P0-T030 hash chain | P1-T030, P1-T038, P1-T041 |
| P0-T032 `mt-api` (Rust, axum) · P0-T034 command bus · P0-T035 confirmation levels + break-glass | P1-T046 (P0-T035 also P1-T030, P1-T071) |
| P0-T036 WS hub · P0-T048 typed clients | P1-T047 |
| P0-T049 component library · P0-T050 app shell | P1-T048, P1-T049 (P0-T050 also P1-T051) |
| P0-T051 D16 Health page | P1-T071 |
| P0-T053 Playwright viewport matrix | P1-T063 |

**Consumers downstream:** P2 R2.16/R2.58 (DQ status and inline data-age, egress and integrity checks in M11), R2.34/T2.26 (TCA on paper fills uses the P1-T040 scaffold), R2.40 (measured costs), R2.52 (Telegram commands extend the P1 alerts bot); P3 R3.03/T3.21 (RBA F11 from P1-T020, ABS CPI from P1-T027); P4 R4.05 (StockTwits result from P1-T056), R4.11/T4.32 (the "Arrives in Phase 4" D02 widgets), R4.15/T4.30 (venue-status signals into P1-T043); P7 R7.14/T7.42 (the egress check points at the static exit node).
