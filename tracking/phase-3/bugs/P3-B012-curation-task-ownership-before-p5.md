---
id: P3-B012
kind: gap
title: TAX_QUESTION storage needs curation.task before M19 lands in P5
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
branch: p3/P3-B012-curation-task-ownership-before-p5
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: done
found_in: docs/roadmap/phase-3-journal-and-tax.md §4 (T3.30)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
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

- [x] Decision recorded in docs/17 (17 §D P3-B011/P3-B012): P3 adds a minimal `curation.task` table for `TAX_QUESTION` tasks; P5 (M19) extends it additively
- [x] Owning docs carry it: 03 M19 Storage; 03 §4 `curation`; 02 §4 M19 row; 04 Phase 3 checklist; roadmap R3.18
- [x] Affected tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P3-T038 (minimal table + seed)
- [x] Decision and source noted in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T038, when they read the linked doc, then the rule is unambiguous.

### Stress / failure injection

- n/a: documentation/spec gap

## Acceptance criteria

- [x] Decision recorded in the owning doc (03 M19 Storage; 03 §4 `curation`; 02 §4 M19 row; 04 Phase 3 checklist; roadmap R3.18)
- [x] Affected tasks consistent with it (P3-T038 (minimal table + seed))
- [x] Root cause noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by docs/17 §D P3-B011/P3-B012: P3 adds a minimal `curation.task` table for `TAX_QUESTION` tasks; P5 (M19) extends it additively. Docs now carry it: 03 M19 Storage; 03 §4 `curation`; 02 §4 M19 row; 04 Phase 3 checklist; roadmap R3.18. Implementation owned by P3-T038 (minimal table + seed). Root cause: no owner for `curation.task` DDL before P5.
- 2026-10-22 02:03 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P3-B011/P3-B012); docs updated: 03 M19 Storage; 03 §4 `curation`; 02 §4 M19 row; 04 Phase 3 checklist; roadmap R3.18; implementation owned by P3-T038 (minimal table + seed)
- 2026-10-22 02:03 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:03 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
