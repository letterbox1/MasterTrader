---
id: P7-B012
kind: gap
title: 12-month review outlasts every phase; nothing owns its completion
phase: 7
type: DOC
status: done
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
doc_sync_status: done
found_in: docs/roadmap/phase-7-prove-and-go-live.md T7.10, T7.82; docs/roadmap/README.md §6
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
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

- [x] Decision recorded in docs/17 (17 §D P7-B012): P7 closes once micro-live is stable; the 12-month review is a scheduled recurring calendar review, not a phase item
- [x] Owning docs carry it: roadmap README §10 standing operations; roadmap T7.10, T7.82, R7.05 and §6 exit 4; 14 §7 note; 02 §12 Phase 7 row
- [x] Affected Phase 7 tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P7-T042 (yearly REVIEW_12M schedule + report), P7-T063 (you diary it); P7-T062 cancelled
- [x] Decision and root cause noted in the progress log

## Verification

### Tests
- Doc review: the cited sections now state one consistent rule; affected task files reference it.

### Scenarios
- Given an implementer reads only the fixed docs, then they implement the same behaviour the Phase 7 tasks assume.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (roadmap README §10 standing operations; roadmap T7.10, T7.82, R7.05 and §6 exit 4; 14 §7 note; 02 §12 Phase 7 row)
- [x] Affected tasks consistent with it (P7-T042 (yearly REVIEW_12M schedule + report), P7-T063 (you diary it); P7-T062 cancelled)
- [x] Root cause noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by docs/17 17 §D P7-B012: P7 closes once micro-live is stable; the 12-month review is a scheduled recurring calendar review, not a phase item. Docs now carry it: roadmap README §10 standing operations; roadmap T7.10, T7.82, R7.05 and §6 exit 4; 14 §7 note; 02 §12 Phase 7 row. Implementation owned by P7-T042 (yearly REVIEW_12M schedule + report), P7-T063 (you diary it); P7-T062 cancelled. Root cause: a 12-month RUN item outlived every phase with no owner.
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P7-B012); docs updated: roadmap README §10 standing operations; roadmap T7.10, T7.82, R7.05 and §6 exit 4; 14 §7 note; 02 §12 Phase 7 row; implementation owned by P7-T042 (yearly REVIEW_12M schedule + report), P7-T063 (you diary it); P7-T062 cancelled
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
