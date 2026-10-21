---
id: P7-B012
kind: gap
title: 12-month review outlasts every phase; nothing owns its completion
phase: 7
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.05]
roadmap_todos: []
modules: []
dashboards: []
branch: p7/P7-B012-twelve-month-review-has-no-owner-phase
pr: ""
doc_sync: [docs/roadmap/README.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: docs/roadmap/phase-7-prove-and-go-live.md T7.10, T7.82; docs/roadmap/README.md §6
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-B012 · 12-month review outlasts every phase; nothing owns its completion

## Goal / expected outcome

The docs agree and are specific enough to implement: add a 'Standing operations' section to the roadmap README listing the 12-month review, quarterly registry re-checks, and capital steps after exit, with owners.

## Context & references

- Found in: `docs/roadmap/phase-7-prove-and-go-live.md T7.10, T7.82; docs/roadmap/README.md §6`
- Related: P7-T062, P7-T063, P7-T042

## Requirements

- **What:** T7.10 (12-month review) and T7.82 (12 months live) finish ~12 months after Phase 7's exit; Phase 8 doesn't own them.
- **Expected:** A standing-operations track (or an explicit note) that owns long-running reviews after phase exit; Phase 7 tracks only the clock start and pre-committed criteria.
- **Actual:** No phase or board owns completing the review; it will look 'done' when only scheduled.
- **Impact:** The single most important keep/kill decision could be missed. (severity S3)
- **Suggested fix:** Add a 'Standing operations' section to the roadmap README listing the 12-month review, quarterly registry re-checks, and capital steps after exit, with owners.

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
- `docs/roadmap/phase-7-prove-and-go-live.md`: apply the agreed fix.

## Branch & PR

- Branch: `p7/P7-B012-twelve-month-review-has-no-owner-phase`
- PR title: `P7-B012: fix 12-month review outlasts every phase; nothing owns its completion`
- PR checklist: doc fix or regression test · root cause in the progress log · `./kanban done` run

## Progress log

- 2026-10-21 00:00 · planner · opened
