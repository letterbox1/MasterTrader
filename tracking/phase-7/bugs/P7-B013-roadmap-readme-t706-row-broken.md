---
id: P7-B013
kind: gap
title: Roadmap README USER register row T7.06 has a stray '|' that breaks the table
phase: 7
type: DOC
status: backlog
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.05, R7.08]
roadmap_todos: []
modules: []
dashboards: []
branch: p7/P7-B013-roadmap-readme-t706-row-broken
pr: ""
doc_sync: [docs/roadmap/README.md]
doc_sync_status: n/a
found_in: docs/roadmap/README.md §6 (USER action register, row T7.06)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-B013 · Roadmap README USER register row T7.06 has a stray '|' that breaks the table

## Goal / expected outcome

The docs agree and are specific enough to implement: fix the row (or the generator, if that block is generated from the phase doc).

## Context & references

- Found in: `docs/roadmap/README.md §6 (USER action register, row T7.06)`

## Requirements

- **What:** The row reads 'Approve each promotion (approve | auto is C3); … → R7.05, R7.08 |' — the '→' became '|', shifting columns.
- **Expected:** 'Approve each promotion (approve → auto is C3); approve each capital step after 4 clean weeks.' | 'R7.05, R7.08'.
- **Actual:** The 'Feeds / blocks' column shows the wrong text and an extra cell.
- **Impact:** Cosmetic; the rendered table is misaligned. (severity S4)
- **Suggested fix:** Fix the row (or the generator, if that block is generated from the phase doc).

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

- `docs/roadmap/README.md`: apply the agreed fix.

## Branch & PR

- Branch: `p7/P7-B013-roadmap-readme-t706-row-broken`
- PR title: `P7-B013: fix roadmap README USER register row T7.06 has a stray '|' that breaks the table`
- PR checklist: doc fix or regression test · root cause in the progress log · `./kanban done` run

## Progress log

- 2026-10-21 00:00 · planner · opened
