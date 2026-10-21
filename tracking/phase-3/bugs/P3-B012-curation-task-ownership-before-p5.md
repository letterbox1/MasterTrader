---
id: P3-B012
kind: gap
title: TAX_QUESTION storage needs curation.task before M19 lands in P5
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
branch: p3/P3-B012-curation-task-ownership-before-p5
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: docs/roadmap/phase-3-journal-and-tax.md §4 (T3.30)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-B012 · TAX_QUESTION storage needs curation.task before M19 lands in P5

## Goal / expected outcome

Clear ownership of the `curation.task` DDL: P3 creates a minimal additive table, P5 extends it.

## Context & references

- T3.30 "queue lands fully in P5; store now" · [D15 Questions](../../../docs/ui/dashboards/D15-tax.md) reads `/tasks?type=TAX_QUESTION` · P5 T5.30 builds `mt_curation`
- Affects: P3-T038

## Requirements

- **Steps to reproduce:** Implement T3.30 and then P5 T5.30 independently.
- **Expected:** One table, additive migrations, no data loss.
- **Actual:** Both phases could create `curation.task` differently.
- **Impact:** Migration collision; lost tax-agent answers. (severity S3)
- **Suggested fix:** State in the P5 roadmap/03 M19 that `curation.task` exists from P3 (P3-T038) and P5 migrates additively.

## ToDo

- [ ] Add boundary note to 03 M19 (and P5 roadmap via main agent)
- [ ] Update the affected task files (P3-T038) if the decision differs from their default
- [ ] Note the decision and source in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T038, when they read the linked doc, then the rule is unambiguous.

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

- `docs/03-build-spec.md`: record the decision.
- `docs/roadmap/phase-3-journal-and-tax.md`: no ToDo box to tick; note the outcome under §7 Risks if it changes a risk or open question.

## Branch & PR

- Branch: `p3/P3-B012-curation-task-ownership-before-p5`
- PR title: `P3-B012: TAX_QUESTION storage needs curation.task before M19 lands in P5`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-B012` run

## Progress log

- 2026-10-21 00:00 · planner · opened
