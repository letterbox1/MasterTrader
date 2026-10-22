---
id: P0-B010
kind: gap
title: Provenance column sets differ between 03 §1, 12 §5 and R0.05
phase: 0
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.05]
roadmap_todos: [T0.22]
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p0/P0-B010-provenance-column-set-mismatch
pr: ""
doc_sync: [docs/03-build-spec.md, docs/12-policy-and-compliance.md]
doc_sync_status: done
found_in: docs/03-build-spec.md §1 (Data provenance row)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-B010 · Provenance column sets differ between 03 §1, 12 §5 and R0.05

## Goal / expected outcome

The docs agree and the implementing tasks have one unambiguous answer. Suggested fix: State in 12 §5 and 03 §1 that the flags are seven separate columns as in R0.05.

## Context & references

- Found in: `docs/03-build-spec.md §1 (Data provenance row)`
- Related: P0-T025
- [12 §5 provenance](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms)
- [03 §1 ground rules](../../../docs/03-build-spec.md#1-ground-rules)

## Requirements

- **Steps to reproduce:** Compare 03 §1 (`train_ok`, `model_input_ok`, `retention_days`, `commercial_ok` — no `display_ok`), 12 §5 (`use_flags` grouping incl. `display_ok`), R0.05 and SPEC (seven separate columns).
- **Expected:** Same seven columns everywhere.
- **Actual:** 03 §1 omits `display_ok`; 12 §5 implies a grouped `use_flags` field.
- **Impact:** Low: implementers might build a jsonb `use_flags` or drop `display_ok`.
- **Suggested fix:** State in 12 §5 and 03 §1 that the flags are seven separate columns as in R0.05.

## ToDo

- [x] Decision taken: 17 §B P0-B010 (ratified in 17 §E)
- [x] Docs updated so they agree: 03 §1 Data provenance row (seven separate columns); 12 §5 ('seven separate provenance columns, not a grouped field'); SPEC data-provenance row; roadmap P0 R0.05
- [x] Affected P0 task files reference the resolution: P0-T016, P0-T025
- [x] Regression check owned: P0-T025 schema test (seven columns, deny defaults)

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Listed docs carry the 17 §B P0-B010 decision and agree (checked in the alignment wave, 2026-10-22)
- [x] Implementation owned by: P0-T025
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- If the user decides differently from the suggestion, the affected tasks are updated before they start.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/03-build-spec.md`: reconcile as described.
- `docs/12-policy-and-compliance.md`: reconcile as described.

## Branch & PR

- Branch: `p0/P0-B010-provenance-column-set-mismatch`
- PR title: `P0-B010: fix provenance column sets differ between 03 §1, 12 §5 and R0.05`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B010` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §B P0-B010; docs checked: 03 §1 Data provenance row (seven separate columns); 12 §5 ('seven separate provenance columns, not a grouped field'); SPEC data-provenance row; roadmap P0 R0.05. Root cause: 12 §5 grouped the flags as `use_flags` while R0.05/SPEC listed columns. Implementation owned by P0-T025.
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P0-B010); docs updated: 03 §1 Data provenance row (seven separate columns); 12 §5 ('seven separate provenance columns, not a grouped field'); SPEC data-provenance row; roadmap P0 R0.05; implementation owned by P0-T025
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
