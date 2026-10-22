---
id: P1-B011
kind: gap
title: Timeframe range and "arbitrary time_bucket" aggregates are inconsistent
phase: 1
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.02, R1.15]
roadmap_todos: []
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p1/P1-B011-timeframe-range-and-arbitrary-buckets
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/ui/dashboards/D02-markets.md]
doc_sync_status: done
found_in: docs/03-build-spec.md M1; docs/02-v1-architecture.md §5.1; docs/ui/dashboards/D02-markets.md PriceChart
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-B011 · Timeframe range and "arbitrary time_bucket" aggregates are inconsistent

## Goal / expected outcome

Docs say: CAGGs at 5m/15m/1h/4h/1D; any other size (incl. 1W) is `time_bucket` on query over the finest suitable table

## Context & references

- Found in: R1.02/02 §5.1 aggregate "to 1D"; D02 charts go "tick → 1W"; 03 M1 says continuous aggregates for "arbitrary `time_bucket` sizes", but continuous aggregates are fixed-size
- Related items: P1-T013, P1-T050

## Requirements

- **Where:** R1.02/02 §5.1 aggregate "to 1D"; D02 charts go "tick → 1W"; 03 M1 says continuous aggregates for "arbitrary `time_bucket` sizes", but continuous aggregates are fixed-size
- **Expected:** Docs say: CAGGs at 5m/15m/1h/4h/1D; any other size (incl. 1W) is `time_bucket` on query over the finest suitable table
- **Actual:** Wording implies arbitrary CAGGs and leaves 1W undefined
- **Suggested fix:** Adopt the P1-T013 design in 03 M1 and 02 §5.1; D02 lists 1W as on-the-fly
- **Impact:** Minor confusion for implementers (severity S4)

## ToDo

- [x] Decision recorded in docs/17 (17 §D P1-B011/P1-B015): timeframes run tick → 1W with continuous aggregates at 1m, 5m, 15m, 1h, 4h, 1D, 1W; other sizes via `time_bucket` at read time
- [x] Aligned docs carry it: 03 M1 (recording pipeline); 02 §5.1 (Postgres row); D02 (overview, `PriceChart`, acceptance 1); roadmap R1.02, T1.21
- [x] Affected P1 tasks updated in the 2026-10-22 task alignment: P1-T013, P1-T050, P1-T058

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [x] Docs updated and consistent (03 M1 (recording pipeline); 02 §5.1 (Postgres row); D02 (overview, `PriceChart`, acceptance 1); roadmap R1.02, T1.21)
- [x] Decision and owning tasks noted in the progress log

## Exceptions & edge cases

- Until fixed, related tasks follow the interim rule stated in their own files

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a number in code; the decision lands in the docs first
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/03-build-spec.md`: apply the fix above
- `docs/02-v1-architecture.md`: apply the fix above
- `docs/ui/dashboards/D02-markets.md`: apply the fix above

## Branch & PR

- Branch: `p1/P1-B011-timeframe-range-and-arbitrary-buckets`
- PR title: `P1-B011: Timeframe range and "arbitrary time_bucket" aggregates are inconsistent`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-B011` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D P1-B011/P1-B015; docs carry it (03 M1 (recording pipeline); 02 §5.1 (Postgres row); D02 (overview, `PriceChart`, acceptance 1); roadmap R1.02, T1.21); implementation owned by P1-T013, P1-T050, P1-T058
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P1-B011/P1-B015); docs updated: 03 M1 (recording pipeline); 02 §5.1 (Postgres row); D02 (overview, `PriceChart`, acceptance 1); roadmap R1.02, T1.21; implementation owned by P1-T013, P1-T050, P1-T058
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
