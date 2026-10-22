---
id: P3-B004
kind: gap
title: Wash-sale reacquisition window N days is unspecified
phase: 3
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R3.06]
roadmap_todos: []
modules: [M18]
dashboards: []
branch: p3/P3-B004-wash-sale-window-unspecified
pr: ""
doc_sync: [docs/09-journal-and-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: done
found_in: docs/09-journal-and-tax.md §Key findings (wash sales)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P3-B004 · Wash-sale reacquisition window N days is unspecified

## Goal / expected outcome

A documented default window (and the agent's view) for wash-sale flags.

## Context & references

- [09 key findings](../../../docs/09-journal-and-tax.md#️-key-findings-that-shape-the-design): "re-entered within N days (especially May–July)"
- Affects: P3-T026, P3-T038

## Requirements

- **Steps to reproduce:** Implement the wash-sale flag from 09.
- **Expected:** A number (default) and a definition of "substantially identical".
- **Actual:** N undefined; identical-asset rule undefined.
- **Impact:** Inconsistent flags; agent can't rely on them. (severity S3)
- **Suggested fix:** Default N = 30 days either side, EOFY emphasis 1 May–31 July; add as an agent question; document in 09.

## ToDo

- [x] Decision recorded in docs/17 (17 §C P3-B004): wash-sale flag: re-acquisition of the same asset within 30 days either side of a loss disposal, flag only (default, configurable); near-identical assets are tax-agent Q12
- [x] Owning docs carry it: 16 §4.4; 09 wash-sale finding + question 12; 03 M18; roadmap R3.06
- [x] Affected tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P3-T026 (flags), P3-T038 (question seed), P3-T045 (golden case)
- [x] Decision and source noted in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T026, when they read the linked doc, then the rule is unambiguous.

### Stress / failure injection

- n/a: documentation/spec gap

## Acceptance criteria

- [x] Decision recorded in the owning doc (16 §4.4; 09 wash-sale finding + question 12; 03 M18; roadmap R3.06)
- [x] Affected tasks consistent with it (P3-T026 (flags), P3-T038 (question seed), P3-T045 (golden case))
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- Until resolved, the affected tasks use the default stated in their Requirements and label it (U).

## Cardinal rules (do NOT)

- Do NOT resolve by editing WORM data; spec changes apply to new computations (superseding rows).
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."

## Doc sync on completion

- `docs/09-journal-and-tax.md`: record the decision.
- `docs/roadmap/phase-3-journal-and-tax.md`: no ToDo box to tick; note the outcome under §7 Risks if it changes a risk or open question.

## Branch & PR

- Branch: `p3/P3-B004-wash-sale-window-unspecified`
- PR title: `P3-B004: Wash-sale reacquisition window N days is unspecified`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-B004` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by docs/17 §C P3-B004: wash-sale flag: re-acquisition of the same asset within 30 days either side of a loss disposal, flag only (default, configurable); near-identical assets are tax-agent Q12. Docs now carry it: 16 §4.4; 09 wash-sale finding + question 12; 03 M18; roadmap R3.06. Implementation owned by P3-T026 (flags), P3-T038 (question seed), P3-T045 (golden case). Root cause: 09 flagged wash sales without a window.
- 2026-10-22 02:02 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §C P3-B004); docs updated: 16 §4.4; 09 wash-sale finding + question 12; 03 M18; roadmap R3.06; implementation owned by P3-T026 (flags), P3-T038 (question seed), P3-T045 (golden case)
- 2026-10-22 02:02 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:02 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
