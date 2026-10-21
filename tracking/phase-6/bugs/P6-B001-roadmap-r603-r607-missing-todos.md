---
id: P6-B001
kind: gap
title: Roadmap P6: R6.03 has no ToDo; R6.07 enforcement and several 'Verified by' checks have no BUILD/VERIFY ToDo
phase: 6
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.03, R6.07, R6.01, R6.02, R6.05, R6.06]
roadmap_todos: []
modules: []
dashboards: []
branch: p6/P6-B001-roadmap-r603-r607-missing-todos
pr: ""
doc_sync: [docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: docs/roadmap/phase-6-ai-models-treasury.md §3–§4
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-B001 · Roadmap P6: R6.03 has no ToDo; R6.07 enforcement and several 'Verified by' checks have no BUILD/VERIFY ToDo

## Goal / expected outcome

The docs agree and are specific enough to build from: every requirement is reached by at least one ToDo, and every 'Verified by' has a VERIFY ToDo; security items have R6.N IDs.

## Context & references

- Found in: docs/roadmap/phase-6-ai-models-treasury.md §3–§4
- Roadmap: [§4 ToDo sets](../../../docs/roadmap/phase-6-ai-models-treasury.md#4-todo-sets)
- Covered in this phase by P6-T005, P6-T009, P6-T052, P6-T053, P6-T061, P6-T062, P6-T063

## Requirements

- **Steps to reproduce:** read docs/roadmap/phase-6-ai-models-treasury.md §3–§4 and compare it with the cross-referenced sections listed under Context.
- **Expected:** every requirement is reached by at least one ToDo, and every 'Verified by' has a VERIFY ToDo; security items have R6.N IDs.
- **Actual:** R6.03 (every LLM call audited) is not referenced by any T6.xx; R6.07 has only USER T6.01 and OPS T6.41 (no BUILD for the cap/fallback); 'Sample runs' (R6.01), 'Scheduler tests' (R6.02), 'Seeded anomaly' (R6.05), 'Gate check' (R6.06), 'Budget test' (R6.07) have no VERIFY ToDo; the phase has no R6.N* non-functional rows although T6.65 (prompt injection) and T6.40 (local model auth) are security requirements.
- **Suggested fix:** Add BUILD ToDos for R6.03 and R6.07 enforcement, VERIFY ToDos for the listed checks, and R6.N1 (prompt-injection resistance, 02 §9.1) / R6.N2 (local inference servers 127.0.0.1 + API key, 07 §5) / R6.N3 (tier B p95 < 50 ms, 02 §9.2).
- **Impact:** Traceability holes; work could be skipped by a reader of the roadmap alone (severity S3)

## ToDo

- [ ] Draft the roadmap additions (IDs and wording) in this file.
- [ ] Agree them with the roadmap owner.
- [ ] Update the docs listed under Doc sync and link the resolving commit here.

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Roadmap §3/§4 updated; kanban validate shows the new IDs mapped to P6 tasks.
- [ ] Root cause noted in the progress log.

## Exceptions & edge cases

- Until resolved, dependent tasks use the conservative interpretation stated under Suggested fix and note it in their progress log.

## Cardinal rules (do NOT)

- Do NOT silently pick a number in code; record the decision in the doc first.
- Do NOT edit docs owned by another phase's planner from a P6 branch without the owner's agreement; propose the change in the PR description.

## Doc sync on completion

- `docs/roadmap/phase-6-ai-models-treasury.md`: resolve the inconsistency.

## Branch & PR

- Branch: `p6/P6-B001-roadmap-r603-r607-missing-todos`
- PR title: `P6-B001: Roadmap P6: R6.03 has no ToDo; R6.07 enforcement and several 'Verified by' checks have no BUILD/VERIFY ToDo`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-B001` run

## Progress log

- 2026-10-21 00:00 · planner · created
