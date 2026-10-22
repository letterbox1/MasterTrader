---
id: P1-B001
kind: gap
title: Stale-feed SLO does not say where the 2 s starts
phase: 1
type: DOC
status: done
priority: high
size: S
severity: S2
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.N1, R1.10]
roadmap_todos: []
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p1/P1-B001-stale-slo-start-point-undefined
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/roadmap/phase-1-data-and-monitoring.md, docs/ui/dashboards/D07-data-quality.md]
doc_sync_status: done
found_in: docs/02-v1-architecture.md §9.2; docs/roadmap/phase-1-data-and-monitoring.md R1.N1; docs/ui/dashboards/D07-data-quality.md acceptance 1
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-B001 · Stale-feed SLO does not say where the 2 s starts

## Goal / expected outcome

One definition: the clock starts at feed death (socket close / last heartbeat) for connection-level staleness, and at timeout expiry for per-instrument silence; per-instrument timeouts are documented separately

## Context & references

- Found in: [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos) "Feed staleness detection → strategy paused < 2 s"; R1.N1 "Feed staleness detected → dq.status stale < 2 s"; [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) "within 2 s of detection"; exit criterion 3 "killed feed shows stale in < 2 s"
- Related items: P1-T031, P1-T057, P1-T067

## Requirements

- **Where:** [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos) "Feed staleness detection → strategy paused < 2 s"; R1.N1 "Feed staleness detected → dq.status stale < 2 s"; [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) "within 2 s of detection"; exit criterion 3 "killed feed shows stale in < 2 s"
- **Expected:** One definition: the clock starts at feed death (socket close / last heartbeat) for connection-level staleness, and at timeout expiry for per-instrument silence; per-instrument timeouts are documented separately
- **Actual:** Three different start/end points; a quiet instrument cannot be declared stale 2 s after its last message without false positives
- **Suggested fix:** Define two layers in 02 §9.2 and 03 M16 (connection-level < 2 s from death; instrument-level = learned timeout + < 2 s), as implemented in P1-T031
- **Impact:** P1-T031/T057/T067 cannot prove the SLO unambiguously; P2 risk pausing depends on it (severity S2)

## ToDo

- [x] Decision recorded in docs/17 (17 §A P1-B001): data age = now − our receive time per stream; per-bot thresholds (2 s fast / 60 s slow, configurable, session-aware); the monitor flips `dq.status` ≤ 250 ms p99 after the threshold; M11 checks data age inline on every order
- [x] Aligned docs carry it: 16 §2.2; 02 §9.2 (SLO row); 03 M16 (stale feed row); roadmap R1.N1, R1.17; D07 ("What stale means", acceptance 1)
- [x] Affected P1 tasks updated in the 2026-10-22 task alignment: P1-T030, P1-T031, P1-T048, P1-T057, P1-T062, P1-T067

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [x] Docs updated and consistent (16 §2.2; 02 §9.2 (SLO row); 03 M16 (stale feed row); roadmap R1.N1, R1.17; D07 ("What stale means", acceptance 1))
- [x] Decision and owning tasks noted in the progress log

## Exceptions & edge cases

- Until fixed, related tasks follow the interim rule stated in their own files

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a number in code; the decision lands in the docs first
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/02-v1-architecture.md`: apply the fix above
- `docs/03-build-spec.md`: apply the fix above
- `docs/roadmap/phase-1-data-and-monitoring.md`: apply the fix above
- `docs/ui/dashboards/D07-data-quality.md`: apply the fix above

## Branch & PR

- Branch: `p1/P1-B001-stale-slo-start-point-undefined`
- PR title: `P1-B001: Stale-feed SLO does not say where the 2 s starts`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-B001` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §A P1-B001; docs carry it (16 §2.2; 02 §9.2 (SLO row); 03 M16 (stale feed row); roadmap R1.N1, R1.17; D07 ("What stale means", acceptance 1)); implementation owned by P1-T030, P1-T031, P1-T048, P1-T057, P1-T062, P1-T067
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §A P1-B001); docs updated: 16 §2.2; 02 §9.2 (SLO row); 03 M16 (stale feed row); roadmap R1.N1, R1.17; D07 ("What stale means", acceptance 1); implementation owned by P1-T030, P1-T031, P1-T048, P1-T057, P1-T062, P1-T067
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
