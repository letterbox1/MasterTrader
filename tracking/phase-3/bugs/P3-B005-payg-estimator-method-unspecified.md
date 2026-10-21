---
id: P3-B005
kind: gap
title: PAYG instalment estimator method is unspecified
phase: 3
type: DOC
status: backlog
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
branch: p3/P3-B005-payg-estimator-method-unspecified
pr: ""
doc_sync: [docs/09-journal-and-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: docs/09-journal-and-tax.md §Key findings (BAS row)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-B005 · PAYG instalment estimator method is unspecified

## Goal / expected outcome

09 states the estimator's method: inputs (rate vs amount from the ATO notice), instalment income definition, quarters and due dates.

## Context & references

- [09 BAS finding](../../../docs/09-journal-and-tax.md#️-key-findings-that-shape-the-design) · [D15 PAYG tab](../../../docs/ui/dashboards/D15-tax.md) ("instalment income basis (excluding capital gains)")
- Affects: P3-T027

## Requirements

- **Steps to reproduce:** Try to implement the estimator from 09 alone.
- **Expected:** Explicit method and inputs.
- **Actual:** Only "PAYG-instalment estimator (quarterly)".
- **Impact:** Estimator may compute the wrong base or miss the user-entered rate. (severity S3)
- **Suggested fix:** Adopt P3-T027's method (rate or amount from notice; instalment income excludes capital gains; quarters + default due dates (U)) in 09.

## ToDo

- [ ] Add the method to 09
- [ ] Update the affected task files (P3-T027) if the decision differs from their default
- [ ] Note the decision and source in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T027, when they read the linked doc, then the rule is unambiguous.

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

- `docs/09-journal-and-tax.md`: record the decision.
- `docs/roadmap/phase-3-journal-and-tax.md`: no ToDo box to tick; note the outcome under §7 Risks if it changes a risk or open question.

## Branch & PR

- Branch: `p3/P3-B005-payg-estimator-method-unspecified`
- PR title: `P3-B005: PAYG instalment estimator method is unspecified`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-B005` run

## Progress log

- 2026-10-21 00:00 · planner · opened
