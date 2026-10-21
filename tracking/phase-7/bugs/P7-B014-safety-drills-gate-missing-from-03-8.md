---
id: P7-B014
kind: gap
title: 'Safety drills' is a promotion gate in 02 §13 and D03 but not in 03 §8
phase: 7
type: DOC
status: backlog
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.01]
roadmap_todos: []
modules: []
dashboards: []
branch: p7/P7-B014-safety-drills-gate-missing-from-03-8
pr: ""
doc_sync: [docs/03-build-spec.md]
doc_sync_status: n/a
found_in: docs/02-v1-architecture.md §13 item 6; docs/ui/dashboards/D03-strategies.md Gates tab; docs/03-build-spec.md §8
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-B014 · 'Safety drills' is a promotion gate in 02 §13 and D03 but not in 03 §8

## Goal / expected outcome

The docs agree and are specific enough to implement: add item 'Safety drills exercised' to 03 §8.

## Context & references

- Found in: `docs/02-v1-architecture.md §13 item 6; docs/ui/dashboards/D03-strategies.md Gates tab; docs/03-build-spec.md §8`
- Related: P7-T012, P7-T044

## Requirements

- **What:** 02 §13 lists 'Safety drills: kill switch, dead-man's switch and DQ pause exercised' as gate 6 and D03 shows it, but 03 §8 (the gate source of truth) omits it.
- **Expected:** 03 §8 includes the safety-drills gate (P7-T012 evaluates it from `ops.drill_log`).
- **Actual:** Gate lists differ by one item.
- **Impact:** Minor: P7-T012 already includes it; docs disagree. (severity S4)
- **Suggested fix:** Add item 'Safety drills exercised' to 03 §8.

## ToDo

- [ ] Confirm the conflict/omission against the cited sections
- [ ] Agree the resolution (the user decides where it changes risk or money rules)
- [ ] Edit the docs listed under Doc sync in one PR
- [ ] Update any Phase 7 task text that depended on the assumption

## Verification

### Tests
- Doc review: the cited sections now state one consistent rule; affected task files reference it.

### Scenarios
- Given an implementer reads only the fixed docs, then they implement the same behaviour the Phase 7 tasks assume.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Docs updated and consistent
- [ ] Root cause noted in the progress log

## Exceptions & edge cases

- If the user picks a different resolution than suggested, update the dependent Phase 7 tasks in the same PR.

## Cardinal rules (do NOT)

- Do NOT resolve a conflict by picking the looser number.
- Do NOT edit generated files (`KANBAN.md`, boards, README marked blocks) by hand.

## Doc sync on completion

- `docs/03-build-spec.md`: apply the agreed fix.

## Branch & PR

- Branch: `p7/P7-B014-safety-drills-gate-missing-from-03-8`
- PR title: `P7-B014: fix 'Safety drills' is a promotion gate in 02 §13 and D03 but not in 03 §8`
- PR checklist: doc fix or regression test · root cause in the progress log · `./kanban done` run

## Progress log

- 2026-10-21 00:00 · planner · opened
