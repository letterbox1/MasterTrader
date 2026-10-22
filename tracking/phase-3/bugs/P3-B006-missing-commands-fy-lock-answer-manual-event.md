---
id: P3-B006
kind: gap
title: Commands for FY lock/unlock, task answers and manual journal events missing from the API catalogue
phase: 3
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R3.14]
roadmap_todos: []
modules: [M18]
dashboards: []
branch: p3/P3-B006-missing-commands-fy-lock-answer-manual-event
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/dashboards/D15-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: done
found_in: docs/02-v1-architecture.md §7.2 (Journal & tax commands)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P3-B006 · Commands for FY lock/unlock, task answers and manual journal events missing from the API catalogue

## Goal / expected outcome

02 §7.2 lists every command P3 needs with its confirmation level.

## Context & references

- [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) Journal & tax row
- [D15 rules](../../../docs/ui/dashboards/D15-tax.md): locked FYs need explicit unlocking (C1 + reason)
- P3-T021 manual opening lots; P3-T038 answers
- Affects: P3-T039, P3-T021, P3-T038, P3-T041

## Requirements

- **Steps to reproduce:** Look up the command to lock/unlock an FY, to record a tax-agent answer, or to add a manual journal event.
- **Expected:** `tax.fy.lock` (C1), `tax.fy.unlock` (C1 + reason), `task.answer` (C1), `journal.manual_event.add` (C1) in the catalogue.
- **Actual:** None of these exist; D15 describes locking without a command.
- **Impact:** UI/back-end mismatch; manual events tempted via SQL. (severity S3)
- **Suggested fix:** Add the four commands to 02 §7.2 and D15 Actions.

## ToDo

- [x] Decision recorded in docs/17 (17 §D P3-B006/P3-B007): commands `tax.fy.lock`/`tax.fy.unlock` (C3), `task.answer` (C1), `journal.manual_event.add` (C2)
- [x] Owning docs carry it: 02 §7.2 (Tasks and Journal & tax rows); 09 Commands; D15 actions; D14 actions; roadmap R3.16
- [x] Affected tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P3-T055 (FY lock/unlock, manual events), P3-T038 (`task.answer`), P3-T039 (API), P3-T058 (tests)
- [x] Decision and source noted in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T039, when they read the linked doc, then the rule is unambiguous.

### Stress / failure injection

- n/a: documentation/spec gap

## Acceptance criteria

- [x] Decision recorded in the owning doc (02 §7.2 (Tasks and Journal & tax rows); 09 Commands; D15 actions; D14 actions; roadmap R3.16)
- [x] Affected tasks consistent with it (P3-T055 (FY lock/unlock, manual events), P3-T038 (`task.answer`), P3-T039 (API), P3-T058 (tests))
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- Until resolved, the affected tasks use the default stated in their Requirements and label it (U).

## Cardinal rules (do NOT)

- Do NOT resolve by editing WORM data; spec changes apply to new computations (superseding rows).
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."

## Doc sync on completion

- `docs/02-v1-architecture.md`: record the decision.
- `docs/ui/dashboards/D15-tax.md`: record the decision.
- `docs/roadmap/phase-3-journal-and-tax.md`: no ToDo box to tick; note the outcome under §7 Risks if it changes a risk or open question.

## Branch & PR

- Branch: `p3/P3-B006-missing-commands-fy-lock-answer-manual-event`
- PR title: `P3-B006: Commands for FY lock/unlock, task answers and manual journal events missing from the API catalogue`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-B006` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by docs/17 §D P3-B006/P3-B007: commands `tax.fy.lock`/`tax.fy.unlock` (C3), `task.answer` (C1), `journal.manual_event.add` (C2). Docs now carry it: 02 §7.2 (Tasks and Journal & tax rows); 09 Commands; D15 actions; D14 actions; roadmap R3.16. Implementation owned by P3-T055 (FY lock/unlock, manual events), P3-T038 (`task.answer`), P3-T039 (API), P3-T058 (tests). Root cause: D15/D14 needed commands that 02 §7.2 did not list.
- 2026-10-22 02:02 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P3-B006/P3-B007); docs updated: 02 §7.2 (Tasks and Journal & tax rows); 09 Commands; D15 actions; D14 actions; roadmap R3.16; implementation owned by P3-T055 (FY lock/unlock, manual events), P3-T038 (`task.answer`), P3-T039 (API), P3-T058 (tests)
- 2026-10-22 02:02 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:02 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
