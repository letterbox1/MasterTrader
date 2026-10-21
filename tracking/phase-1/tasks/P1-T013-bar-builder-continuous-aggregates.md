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
branch: p1/P1-T013-bar-builder-continuous-aggregates
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/02-v1-architecture.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T013 · Build 1s/1m bars into Timescale with continuous aggregates

## Goal / expected outcome

The bar builder consumes trades and quotes, writes 1s and 1m OHLCV bars to Timescale hypertables, publishes `md.{venue}.{symbol}.bar.{spec}`, and continuous aggregates roll them up to 5m, 15m, 1h, 4h and 1D; any other size is served with `time_bucket` on query.

## Context & references

- Roadmap: requirements [R1.02](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.21](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (bar builder; continuous aggregates 5m–1D and arbitrary `time_bucket`) · flow [02 §8 F1](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 4 · [02 §5.1](../../../docs/02-v1-architecture.md#51-stores)
- Gap on "arbitrary sizes" and 1W: P1-B011
- Depends on (this phase): P1-T010, P1-T007

## Requirements

- Hypertables `market.bar_1s` and `market.bar_1m` (OHLCV, trade count, VWAP, `event_time` bucket start, `ingest_time`, provenance), compression after 7 days, keep forever (02 §5.1)
- Hierarchical continuous aggregates `market.bar_5m`, `bar_15m`, `bar_1h`, `bar_4h`, `bar_1d` with refresh policies (5m every 1 min, 1d every 15 min) and real-time aggregation on
- FX/stock bars from quotes (mid) where no trades exist; `bar_source` = trade|mid recorded
- Late data: messages up to 10 s late update the open/last bar; later ones go to a correction path that re-writes the affected 1s/1m bars (market tables are not WORM)
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
- Integration: synthetic trades → 1s/1m rows → CAGG 1d equals direct aggregation of 1m (exact for OHLC, Decimal-exact sums)
- Golden: recorded hour → bars equal reference CSV

### Scenarios

- Given a 7m spec request, when served, then it is computed from `bar_1m` with `time_bucket('7 minutes')` and labelled as on-the-fly
- Given a trade arriving 30 s late, when processed, then the affected 1s and 1m bars are corrected and CAGGs refresh

### Stress / failure injection

- Load: 10 symbols × 1s bars for 30 days generated in a test DB; 1D query over a year returns < 200 ms

## Acceptance criteria

- [ ] Live 1s/1m bars and all CAGG levels exist for every streaming instrument
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
