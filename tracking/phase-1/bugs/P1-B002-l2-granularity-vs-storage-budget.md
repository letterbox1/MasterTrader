---
id: P1-B002
kind: gap
title: L2 recording granularity conflicts with the storage budget
phase: 1
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.01, R1.N3]
roadmap_todos: []
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p1/P1-B002-l2-granularity-vs-storage-budget
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-1-data-and-monitoring.md]
doc_sync_status: done
found_in: docs/roadmap/phase-1-data-and-monitoring.md R1.01 vs R1.N3; docs/03-build-spec.md M1 and §6
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-B002 · L2 recording granularity conflicts with the storage budget

## Goal / expected outcome

The docs say whether raw 100 ms diffs are recorded (and for how many symbols) or 1 s snapshots, and the budget is computed for that choice

## Context & references

- Found in: R1.01 and [03 §6](../../../docs/03-build-spec.md#6-smallest-free-timeframe-by-asset-class) specify L2 **diff** depth (100 ms); the budget in [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) / R1.N3 assumes "L2@1s"
- Related items: P1-T001, P1-T010, P1-T012, P1-T052, P1-T065

## Requirements

- **Where:** R1.01 and [03 §6](../../../docs/03-build-spec.md#6-smallest-free-timeframe-by-asset-class) specify L2 **diff** depth (100 ms); the budget in [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) / R1.N3 assumes "L2@1s"
- **Expected:** The docs say whether raw 100 ms diffs are recorded (and for how many symbols) or 1 s snapshots, and the budget is computed for that choice
- **Actual:** Raw 100 ms diffs for ~10 symbols likely exceed 0.3–1 TB/year; the budget silently assumes 1 s
- **Suggested fix:** Record raw diffs only for `l2: true` symbols (P1-T001) plus 1 s book snapshots for others; update the budget after the soak measures bytes/day (P1-T065)
- **Impact:** Disk overrun or under-recorded L2 for P2 microstructure strategies (severity S3)

## ToDo

- [x] Decision recorded in docs/17 (17 §D P1-B002): native-speed L2 diffs only for symbols whose bots need order-book data (default ≤ 3, configurable); 1 s book snapshots for the rest; budget recalculated from the soak
- [x] Aligned docs carry it: 03 M1 (L2 recording, storage budget); 02 §5.1 (Parquet row); roadmap R1.01, R1.N3
- [x] Affected P1 tasks updated in the 2026-10-22 task alignment: P1-T001, P1-T010, P1-T012, P1-T052, P1-T065

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [x] Docs updated and consistent (03 M1 (L2 recording, storage budget); 02 §5.1 (Parquet row); roadmap R1.01, R1.N3)
- [x] Decision and owning tasks noted in the progress log

## Exceptions & edge cases

- Until fixed, related tasks follow the interim rule stated in their own files

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a number in code; the decision lands in the docs first
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/03-build-spec.md`: apply the fix above
- `docs/roadmap/phase-1-data-and-monitoring.md`: apply the fix above

## Branch & PR

- Branch: `p1/P1-B002-l2-granularity-vs-storage-budget`
- PR title: `P1-B002: L2 recording granularity conflicts with the storage budget`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-B002` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D P1-B002; docs carry it (03 M1 (L2 recording, storage budget); 02 §5.1 (Parquet row); roadmap R1.01, R1.N3); implementation owned by P1-T001, P1-T010, P1-T012, P1-T052, P1-T065
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P1-B002); docs updated: 03 M1 (L2 recording, storage budget); 02 §5.1 (Parquet row); roadmap R1.01, R1.N3; implementation owned by P1-T001, P1-T010, P1-T012, P1-T052, P1-T065
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
