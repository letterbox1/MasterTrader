---
id: P3-B013
kind: gap
title: D14 screenshot attachments have no storage or command defined
phase: 3
type: DOC
status: done
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
doc_sync_status: done
found_in: docs/ui/dashboards/D14-journal.md §Actions
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
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

- [x] Decision recorded in docs/17 (17 §D P3-B013/B014/B016): attachments are stored content-addressed under `data/attachments/` and referenced by hash in the WORM note row
- [x] Owning docs carry it: D14 actions; 02 §7.2 `journal.note.add`; 09 Commands; roadmap R3.13
- [x] Affected tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P3-T039 (API), P3-T040 (D14), P3-T005 (`journal.note` hash column), P3-T009 (mount)
- [x] Decision and source noted in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T039, when they read the linked doc, then the rule is unambiguous.

### Stress / failure injection

- n/a: documentation/spec gap

## Acceptance criteria

- [x] Decision recorded in the owning doc (D14 actions; 02 §7.2 `journal.note.add`; 09 Commands; roadmap R3.13)
- [x] Affected tasks consistent with it (P3-T039 (API), P3-T040 (D14), P3-T005 (`journal.note` hash column), P3-T009 (mount))
- [x] Root cause noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by docs/17 §D P3-B013/B014/B016: attachments are stored content-addressed under `data/attachments/` and referenced by hash in the WORM note row. Docs now carry it: D14 actions; 02 §7.2 `journal.note.add`; 09 Commands; roadmap R3.13. Implementation owned by P3-T039 (API), P3-T040 (D14), P3-T005 (`journal.note` hash column), P3-T009 (mount). Root cause: D14 screenshots had no storage rule.
- 2026-10-22 02:03 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P3-B013/B014/B016); docs updated: D14 actions; 02 §7.2 `journal.note.add`; 09 Commands; roadmap R3.13; implementation owned by P3-T039 (API), P3-T040 (D14), P3-T005 (`journal.note` hash column), P3-T009 (mount)
- 2026-10-22 02:03 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:03 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
