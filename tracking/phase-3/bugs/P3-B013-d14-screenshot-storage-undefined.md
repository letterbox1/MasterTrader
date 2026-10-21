---
id: P3-B013
kind: gap
title: D14 screenshot attachments have no storage or command defined
phase: 3
type: DOC
status: backlog
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R3.13]
roadmap_todos: []
modules: [M18]
dashboards: []
branch: p3/P3-B013-d14-screenshot-storage-undefined
pr: ""
doc_sync: [docs/ui/dashboards/D14-journal.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: docs/ui/dashboards/D14-journal.md §Actions
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-B013 · D14 screenshot attachments have no storage or command defined

## Goal / expected outcome

Screenshots attached to trades have a defined storage location, size limit and command.

## Context & references

- [D14 actions](../../../docs/ui/dashboards/D14-journal.md): "Add note / tag / screenshot" mapped to `journal.note.add`, `journal.tag`
- Affects: P3-T039, P3-T040

## Requirements

- **Steps to reproduce:** Attach a screenshot to a trade.
- **Expected:** Command arg for an attachment + storage path + hash + limit.
- **Actual:** Undefined.
- **Impact:** Minor; inconsistent implementation. (severity S4)
- **Suggested fix:** Allow `journal.note.add` with an attachment (PNG/JPEG ≤ 5 MB) stored under `/srv/mastertrader/journal/attachments/` with sha256 in the WORM note row.

## ToDo

- [ ] Update D14 Actions
- [ ] Update the affected task files (P3-T039, P3-T040) if the decision differs from their default
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

- `docs/ui/dashboards/D14-journal.md`: record the decision.
- `docs/roadmap/phase-3-journal-and-tax.md`: no ToDo box to tick; note the outcome under §7 Risks if it changes a risk or open question.

## Branch & PR

- Branch: `p3/P3-B013-d14-screenshot-storage-undefined`
- PR title: `P3-B013: D14 screenshot attachments have no storage or command defined`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-B013` run

## Progress log

- 2026-10-21 00:00 · planner · opened
