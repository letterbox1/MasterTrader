---
id: P4-B007
kind: gap
title: T4.04 labelling has no tool in P4; `models.label.add` missing from the command catalogue
phase: 4
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R4.12]
roadmap_todos: [T4.04]
modules: [M21]
dashboards: [D10, D08]
branch: p4/P4-B007-no-p4-labelling-tool
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/dashboards/D10-models-memory.md]
doc_sync_status: done
found_in: docs/roadmap/phase-4-intel.md T4.04 vs docs/ui/dashboards/D10-models-memory.md (labelling queue, Phase 6) and docs/02-v1-architecture.md §7.2
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P4-B007 · T4.04 labelling has no tool in P4; `models.label.add` missing from the command catalogue

## Goal / expected outcome

The docs acknowledge an interim P4 labelling mode (D08 Label mode, P4-T048) and `models.label.add` (C0) is in the 02 §7.2 command catalogue.

## Context & references

- Found in: [T4.04](../../../docs/roadmap/phase-4-intel.md#4-todo-sets) needs ~200 labels in P4 · [D10](../../../docs/ui/dashboards/D10-models-memory.md) labelling queue is P6 · [02 §7.2](../../../docs/02-v1-architecture.md#7-api-contract-mt_api) has no `models.label.add`
- Related: P4-T048, P4-T049.

## Requirements

- **Steps to reproduce:** look for a P4 labelling UI or command — none; D10 is Phase 6.
- **Expected:** a minimal labelling path in P4 and the command listed in the catalogue.
- **Actual:** missing.
- **Impact:** S3 — T4.04/T4.63 cannot run as written.
- **Suggested fix:** add `models.label.add` (C0) to 02 §7.2 'Agents & models'; note the interim D08 Label mode in D08/D10.

## ToDo

- [x] Decision recorded: add `models.label.add` and a minimal labelling tool in P4 (17 §D)
- [x] Docs carry it: 02 §7.2 'Agents & models' lists `models.label.add` (C0); D08 'Label mode (Phase 4)'; D10 notes labels from D08 Label mode; 10 §4.3; roadmap R4.16 + T4.31
- [x] Implementation owned by P4-T062 (labelling tool + command, new), P4-T049 (your labels), P4-T048 (calibration)

## Verification

### Tests
- Doc review: the corrected section is consistent with the linked sources (links resolve).

### Scenarios
- Given P6 builds the D10 queue, then it reuses `models.label` written in P4.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Labelling path and command documented (checked in 02 §7.2, D08, D10, roadmap R4.16/T4.31, 2026-10-22)
- [x] Root cause noted: T4.04 asked for labels before any labelling UI existed (D10 is P6)

## Exceptions & edge cases

- None.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/02-v1-architecture.md`: §7.2 command catalogue
- `docs/ui/dashboards/D10-models-memory.md`: note P4 interim labels

## Branch & PR

- Branch: `p4/P4-B007-no-p4-labelling-tool`
- PR title: `P4-B007: fix t4.04 labelling has no tool in P4; `models.label.add` missing from the command catalogue`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-B007` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D (P4-B007); docs checked: 02 §7.2, docs/ui/dashboards/D08-intel.md (Label mode), D10, 10 §4.3, roadmap R4.16/T4.31; implementation owned by P4-T062, P4-T049, P4-T048; root cause: labels were needed in P4 but the queue was planned for P6
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 §D (P4-B007); docs updated: 02 §7.2 models.label.add (C0), D08 Label mode, D10, 10 §4.3, roadmap R4.16/T4.31; implementation owned by P4-T062, P4-T049, P4-T048
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
