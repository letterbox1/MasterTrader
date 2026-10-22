---
id: P1-T013
kind: task
title: Build 1s/1m bars into Timescale with continuous aggregates
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
tools: [git, uv, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p1/P1-T013-bar-builder-continuous-aggregates
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/02-v1-architecture.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-T013 · Build 1s/1m bars into Timescale with continuous aggregates

## Goal / expected outcome

The bar builder consumes trades and quotes, writes 1s OHLCV bars to a Timescale hypertable and publishes live 1s/1m bars on `md.{venue}.{symbol}.bar.{spec}`; hierarchical continuous aggregates roll them up to 1m, 5m, 15m, 1h, 4h, 1D and 1W; any other size is a `time_bucket` query at read time ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B011).

## Context & references

- Roadmap: requirements [R1.02](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.21](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (bar builder writing 1s bars; continuous aggregates at 1m, 5m, 15m, 1h, 4h, 1D, 1W; other sizes via `time_bucket` at read time) · flow [02 §8 F1](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 4 · [02 §5.1](../../../docs/02-v1-architecture.md#51-stores)
- Decision: timeframes run tick → 1W ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B011, gap closed); [02 §5.1](../../../docs/02-v1-architecture.md#51-stores)
- Depends on (this phase): P1-T010, P1-T007

## Requirements

- Hypertable `market.bar_1s` (OHLCV, trade count, VWAP, `event_time` bucket start, `ingest_time`, provenance), compression after 7 days (default), keep forever (02 §5.1). Vendor bars from backfills live in separate tables (`market.bar_1s_vendor`, `market.bar_1m_vendor`, `market.bar_daily_vendor`) so they never mix into the aggregates
- Hierarchical continuous aggregates `market.bar_1m` (over 1s), `bar_5m`, `bar_15m`, `bar_1h`, `bar_4h`, `bar_1d`, `bar_1w` (week buckets from Monday 00:00 UTC) with refresh policies (defaults: 1m/5m every 1 min, 1d/1w every 15 min) and real-time aggregation on
- FX/stock bars from quotes (mid) where no trades exist; `bar_source` = trade|mid recorded
- Late data: messages up to 10 s late (default, configurable) update the open/last bar; later ones go to a correction path that re-writes the affected 1s bars and refreshes the aggregates (market tables are not WORM)
- `/markets/{id}/bars?spec=` (P1-T046) chooses the finest stored table ≥ requested spec and applies `time_bucket` for non-standard sizes
- Bars publish to `md.*.bar.1s|1m` for UI and strategies

## ToDo

- [ ] Migrations for bar hypertables, CAGGs, compression and refresh policies
- [ ] Bar builder service (in `ingest-market`) with watermark handling
- [ ] Query helper `mt_store.bars.query(instrument, spec, from, to)` that picks table + `time_bucket`
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: OHLCV maths, VWAP, mid-bars, watermark/late-data rules
- Integration: synthetic trades → 1s rows → every CAGG level (1m … 1W) equals direct aggregation of 1s (exact for OHLC, Decimal-exact sums)
- Golden: recorded hour → bars equal reference CSV

### Scenarios

- Given a 7m spec request, when served, then it is computed from `bar_1m` with `time_bucket('7 minutes')` and labelled as on-the-fly
- Given a 1W request, when served, then it comes from the `bar_1w` aggregate, not an on-the-fly bucket
- Given a trade arriving 30 s late, when processed, then the affected 1s and 1m bars are corrected and CAGGs refresh

### Stress / failure injection

- Load: 10 symbols × 1s bars for 30 days generated in a test DB; 1D query over a year returns < 200 ms

## Acceptance criteria

- [ ] Live 1s bars and all CAGG levels (1m, 5m, 15m, 1h, 4h, 1D, 1W) exist for every streaming instrument
- [ ] Bar parity against Parquet passes (verified in P1-T058)
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- No trades in a second: no 1s bar written (gaps are expected), 1m bar still closes; quiet periods are not data gaps
- DST/AEST: bars are UTC; the 1D bucket is UTC midnight (document it; session-aligned daily bars are a later option)

## Cardinal rules (do NOT)

- Do NOT use floats for prices or sizes; `numeric`/`Decimal` only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions))
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.21 once every task traced to it in PHASE.md is done; note P1-T013 next to it.
- `docs/02-v1-architecture.md` §5.1: list the CAGG levels and refresh policies
- `docs/03-build-spec.md` §M1: clarify "arbitrary sizes = `time_bucket` on query"

## Branch & PR

- Branch: `p1/P1-T013-bar-builder-continuous-aggregates`
- PR title: `P1-T013: Build 1s/1m bars into Timescale with continuous aggregates`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T013` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (timeframes tick → 1W: 1s hypertable + CAGGs 1m…1W, vendor bars in separate tables (P1-B011))
