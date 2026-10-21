---
id: P1-B017
kind: gap
title: Key operating numbers are left as N or undefined
phase: 1
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.10, R1.11, R1.12]
roadmap_todos: []
modules: []
dashboards: []
branch: p1/P1-B017-unspecified-operating-parameters
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/ui/dashboards/D07-data-quality.md]
doc_sync_status: n/a
found_in: docs/03-build-spec.md M16; docs/roadmap/phase-1-data-and-monitoring.md R1.12; docs/02-v1-architecture.md §9.2
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-B017 · Key operating numbers are left as N or undefined

## Goal / expected outcome

Defaults documented: recon 15 min + EOD 00:05 UTC; spread 3×; stale timeouts learned with a 2 s floor; alert delivery target; divergence 25 bps crypto / 5 bps FX majors; robust z 8

## Context & references

- Found in: Reconciliation "every N minutes"; spread pause "> N× normal" (03) vs "> 3× normal" (D07); per-instrument stale timeouts; alert delivery latency target; divergence thresholds; bad-tick z threshold
- Related items: P1-T031, P1-T033, P1-T034, P1-T040, P1-T041, P1-T045

## Requirements

- **Where:** Reconciliation "every N minutes"; spread pause "> N× normal" (03) vs "> 3× normal" (D07); per-instrument stale timeouts; alert delivery latency target; divergence thresholds; bad-tick z threshold
- **Expected:** Defaults documented: recon 15 min + EOD 00:05 UTC; spread 3×; stale timeouts learned with a 2 s floor; alert delivery target; divergence 25 bps crypto / 5 bps FX majors; robust z 8
- **Actual:** Each implementer would invent numbers
- **Suggested fix:** Adopt the defaults used in P1-T031/T033/T034/T040/T041/T045 in 03 M16 and 02 §9.2, editable per the C1/C3 rules
- **Impact:** Inconsistent behaviour, hard-to-verify acceptance (severity S3)

## ToDo

- [ ] Confirm defaults with the user
- [ ] Edit 03 M16, 02 §9.2 and D07
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

- `docs/03-build-spec.md`: apply the fix above
- `docs/02-v1-architecture.md`: apply the fix above
- `docs/ui/dashboards/D07-data-quality.md`: apply the fix above

## Branch & PR

- Branch: `p1/P1-B017-unspecified-operating-parameters`
- PR title: `P1-B017: Key operating numbers are left as N or undefined`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-B017` run

## Progress log

- 2026-10-21 00:00 · planner · opened
