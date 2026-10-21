---
id: P1-B001
kind: gap
title: Stale-feed SLO does not say where the 2 s starts
phase: 1
type: DOC
status: backlog
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
branch: p1/P1-B001-stale-slo-start-point-undefined
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/roadmap/phase-1-data-and-monitoring.md, docs/ui/dashboards/D07-data-quality.md]
doc_sync_status: n/a
found_in: docs/02-v1-architecture.md §9.2; docs/roadmap/phase-1-data-and-monitoring.md R1.N1; docs/ui/dashboards/D07-data-quality.md acceptance 1
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- [ ] Agree the definition with the user
- [ ] Edit 02 §9.2, 03 M16, R1.N1 wording and D07 acceptance 1
- [ ] Update the affected P1 task files if the decision changes their requirements

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [ ] Docs updated and consistent
- [ ] Root cause and decision noted in the progress log

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
