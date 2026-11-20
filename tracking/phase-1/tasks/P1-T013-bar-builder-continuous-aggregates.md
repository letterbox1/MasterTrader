---
id: P1-T013
kind: task
title: Build 1s and standard-size bars in mt-recorder into monthly partitions
phase: 1
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T010, P1-T007]
requirements: [R1.02]
roadmap_todos: [T1.21]
modules: [M1]
dashboards: [D02]
tools: [git, cargo, uv, supabase, docker]
mcp: []
env: []
services: [nats, supabase-postgres]
branch: p1/P1-T013-bar-builder-continuous-aggregates
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/02-v1-architecture.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-T013 · Build 1s and standard-size bars in mt-recorder into monthly partitions

## Goal / expected outcome

The bar builder in `mt-recorder` (Rust) consumes trades and quotes and writes 1s OHLCV bars **and every standard size** (1m, 5m, 15m, 1h, 4h, 1D, 1W) straight into the monthly native partitions of `market.bar_*` in Supabase Postgres, and publishes live 1s/1m bars on `md.{venue}.{symbol}.bar.{spec}`. There is no TimescaleDB: no hypertables and no continuous aggregates. Any other size is a `date_bin()` query at read time inside `pit(as_of)` ([18 §4.3](../../../docs/18-platform-and-deployment.md#43-bars-without-timescaledb)).

## Context & references

- Roadmap: requirements [R1.02](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.21](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Platform: [18 §4.3](../../../docs/18-platform-and-deployment.md#43-bars-without-timescaledb) (monthly partitions, recorder writes standard sizes, rollup job, `date_bin`, Parquet for old bars) · [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-recorder`, `mt-store`) · [18 §3](../../../docs/18-platform-and-deployment.md#3-repository-layout) (`supabase/migrations/`)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (recording pipeline) · flow [02 §8 F1](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 4 · [02 §5.1](../../../docs/02-v1-architecture.md#51-stores)
- Decision: timeframes run tick → 1W ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B011, gap closed); no TimescaleDB ([17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19))
- Related: P1-T075 (partition job and the Parquet hot window), P1-T076 (rebuild and rollup job for backfills and corrections)
- Depends on (this phase): P1-T010, P1-T007

## Requirements

- Tables `market.bar_1s`, `market.bar_1m`, `market.bar_5m`, `market.bar_15m`, `market.bar_1h`, `market.bar_4h`, `market.bar_1d`, `market.bar_1w`: OHLCV (`numeric`), trade count, VWAP, `event_time` bucket start, `ingest_time`, `bar_source` (trade|mid), provenance; each `PARTITION BY RANGE (event_time)` by month, primary key (instrument, event_time); the migration creates the parents and the current + next 2 months' partitions (P1-T075 keeps creating them ahead)
- Vendor bars from backfills live in separate tables (`market.bar_1s_vendor`, `market.bar_1m_vendor`, `market.bar_daily_vendor`, also monthly partitioned) so they never mix into built bars
- Builder writes 1s bars and every standard size as it builds from ticks (1W buckets start Monday 00:00 UTC; 1D at UTC midnight); writes are upserts by key, so re-runs are idempotent; the open bar of each size is updated in place until it closes
- FX/stock bars from quotes (mid) where no trades exist; `bar_source` = trade|mid recorded
- Late data: messages up to 10 s late (default, configurable) update the affected bars of every size directly; later ones are queued for the rollup job (P1-T076), which rebuilds the affected 1s/1m bars and the higher sizes from 1m (market tables are not WORM)
- Read helper in `mt-store` (`bars::query(instrument, spec, from, to)`, exposed to Python through the `mt_store` PyO3 module and used by `pit(as_of)`): picks the finest stored size ≥ the requested spec and applies `date_bin()` for non-standard sizes, labelled `on_the_fly=true`; `/markets/{id}/bars?spec=` (P1-T046) uses it
- Bars publish to `md.*.bar.1s|1m` for the UI and strategies

## ToDo

- [ ] Supabase migration (`supabase/migrations/*.sql`) for the partitioned bar tables, vendor tables and the first partitions; pgTAP tests for keys, partition bounds and grants
- [ ] Bar builder in `crates/mt-recorder` (multi-size, watermark handling, upsert batching)
- [ ] `mt-store` `bars::query` with `date_bin` for other sizes, plus its Python binding
- [ ] Late-data hand-off to the rollup queue (consumed by P1-T076)
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- `cargo test -p mt-recorder bars`: OHLCV maths, VWAP, mid-bars, watermark/late-data rules
- `cargo test -p mt-recorder bars_all_sizes`: synthetic trades → 1s rows and every standard size (1m … 1W) equal direct aggregation of the 1s bars (exact on OHLC, `rust_decimal`-exact sums)
- `cargo test -p mt-store bars_query`: finest-size choice and `date_bin` results; `uv run pytest -k bars_query` runs the same cases through the Python binding
- `supabase test db`: partition bounds are monthly, a row lands in the right partition, keys reject duplicates
- Golden: recorded hour → bars equal reference CSV

### Scenarios

- Given a 7m spec request, when served, then it is computed from `bar_1m` with `date_bin('7 minutes', …)` and labelled as on-the-fly
- Given a 1W request, when served, then it comes from `market.bar_1w` as written by the recorder, not an on-the-fly bucket
- Given a trade arriving 5 s late, when processed, then the affected 1s, 1m and higher bars are updated in place
- Given a trade arriving 30 s late, when processed, then it is queued for the rollup job and, after it runs, every affected size matches a rebuild from ticks

### Stress / failure injection

- Load: 10 symbols × 1s bars for 30 days generated in a test DB; a 1D query over a year returns < 200 ms
- Fault: kill `mt-recorder` mid-minute and restart; upserts leave no duplicate or half-written bar

## Acceptance criteria

- [ ] Live 1s bars and every standard size (1m, 5m, 15m, 1h, 4h, 1D, 1W) exist for every streaming instrument, in monthly partitions
- [ ] Bar parity against Parquet passes (verified in P1-T058)
- [ ] CI green (`cargo clippy`, `cargo test`, `supabase test db`, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- No trades in a second: no 1s bar written (gaps are expected), the 1m bar still closes; quiet periods are not data gaps
- DST/AEST: bars are UTC; the 1D bucket is UTC midnight (document it; session-aligned daily bars are a later option)
- A month boundary with no partition yet: the write fails loudly and alerts (`alert.critical.bar_partition_missing`); P1-T075 creates partitions ahead so this shouldn't happen

## Cardinal rules (do NOT)

- Do NOT use floats for prices or sizes; `numeric` / `rust_decimal` only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions))
- Do NOT use TimescaleDB, hypertables, continuous aggregates or `time_bucket` ([18 §4.2](../../../docs/18-platform-and-deployment.md#42-extensions))
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)` (`mt-store`, also through its Python binding); research and backtest reads go through `pit` only.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.21 once every task traced to it in PHASE.md is done; note P1-T013 next to it.
- `docs/02-v1-architecture.md` §5.1: list the bar tables, their monthly partitioning and the late-data window
- `docs/03-build-spec.md` §M1: confirm "other sizes = `date_bin` at read time inside `pit`"

## Branch & PR

- Branch: `p1/P1-T013-bar-builder-continuous-aggregates`
- PR title: `P1-T013: Build 1s and standard-size bars in mt-recorder into monthly partitions`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T013` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (timeframes tick → 1W: 1s hypertable + CAGGs 1m…1W, vendor bars in separate tables (P1-B011))
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (no TimescaleDB: `mt-recorder` (Rust) writes 1s and every standard size into monthly native partitions of `market.bar_*`; late corrections go to the rollup job P1-T076; `date_bin` in `mt-store` `bars::query` replaces `time_bucket`; Supabase migrations + pgTAP; title, tools and services updated; file name kept)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (tools +uv for the existing `bars::query` Python-binding test (the binding serves `mt_research`); no other change)
