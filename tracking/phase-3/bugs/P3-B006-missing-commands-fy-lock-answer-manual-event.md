---
id: P3-B006
kind: gap
title: Commands for FY lock/unlock, task answers and manual journal events missing from the API catalogue
phase: 3
type: DOC
status: backlog
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
doc_sync_status: n/a
found_in: docs/02-v1-architecture.md §7.2 (Journal & tax commands)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
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

- [ ] Update 02 §7.2 and D15 Actions table
- [ ] Update the affected task files (P3-T039, P3-T021, P3-T038, P3-T041) if the decision differs from their default
- [ ] Note the decision and source in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T039, when they read the linked doc, then the rule is unambiguous.

### Stress / failure injection

- n/a: documentation/spec gap

## Acceptance criteria

- [ ] Decision recorded in the owning doc
- [ ] Affected tasks consistent with it
- [ ] Root cause noted in the progress log

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
