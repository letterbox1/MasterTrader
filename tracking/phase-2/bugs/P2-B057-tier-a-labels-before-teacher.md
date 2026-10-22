---
id: P2-B057
kind: gap
title: Tier A training label source before the P6 teacher exists is unspecified
phase: 2
type: DOC
status: done
priority: low
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.47]
roadmap_todos: []
modules: [M21, M7]
dashboards: [D04]
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B057-tier-a-labels-before-teacher
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/03-build-spec.md]
doc_sync_status: done
found_in: docs/10-memory-rag-and-models.md §4.3; docs/03-build-spec.md M21 (distillation); roadmap R2.47
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B057 · Tier A training label source before the P6 teacher exists is unspecified

## Goal / expected outcome

The docs agree and part-B tasks can be built without guessing: an explicit P2 label source for tier A and a statement that teacher labels are added in P6 as an extra source.

## Context & references

- [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) · [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models) · [phase 6](../../../docs/roadmap/phase-6-ai-models-treasury.md) R6.14
- Affects P2-T125

## Requirements

- **Steps to reproduce:** M21 describes tier A as trained by distillation from M8 debate decisions + outcomes (P6), but R2.47 requires the train → calibrate → compile → runtime pipeline in P2, before any teacher log exists.
- **Expected:** an explicit P2 label source for tier A and a statement that teacher labels are added in P6 as an extra source.
- **Actual:** see steps; the sources disagree or are silent.
- **Suggested fix:** Document outcome labels (forward-return sign over horizon h and triple-barrier) as the P2 `LabelSource`s in 10 §4.3 and 03 M21; P6 adds `teacher` labels without changing existing versions.
- **Impact:** S3: ambiguity about what P2 tier-A models predict.

## ToDo

- [x] Decision recorded: until the P6 teacher exists, tier A trains on forward-return / triple-barrier labels from market data; teacher labels are an extra source later
- [x] Docs agree: 10 §4.3, 03 M21
- [x] Tasks updated: P2-T125

## Verification

### Tests
- Doc gap: reviewed diff; where code depends on it, the named test in the affected task asserts the decided value.

### Scenarios
- Given the decided value, when the affected task is implemented, then its tests assert that value (no hard-coded alternative).

### Stress / failure injection
- n/a: documentation/spec consistency item.

## Acceptance criteria

- [x] Docs agree in one place, cross-linked from the others (10 §4.3 training labels; 03 M21 labels and distillation)
- [x] Affected tasks reference the decision (P2-T125)

## Exceptions & edge cases

- Until resolved, implementations use the suggested default and keep the value configurable.

## Cardinal rules (do NOT)

- Do NOT close without a regression test (code) or a reviewed doc diff (doc gap).
- Do NOT silently pick a value in code without updating the docs.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md`: align with the decision.
- `docs/03-build-spec.md`: align with the decision.

## Branch & PR

- Branch: `p2/P2-B057-tier-a-labels-before-teacher`
- PR title: `P2-B057: Tier A training label source before the P6 teacher exists is unspecified`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-B057` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (resolved by 17 §D (P2-B057); docs carry it (10 §4.3 training labels; 03 M21 labels and distillation); implementation owned by P2-T125)
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D (P2-B057)); docs updated: 10 §4.3 training labels; 03 M21 labels and distillation; implementation owned by P2-T125
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
