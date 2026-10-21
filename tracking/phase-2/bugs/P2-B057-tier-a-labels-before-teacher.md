---
id: P2-B057
kind: gap
title: Tier A training label source before the P6 teacher exists is unspecified
phase: 2
type: DOC
status: backlog
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
branch: p2/P2-B057-tier-a-labels-before-teacher
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: docs/10-memory-rag-and-models.md §4.3; docs/03-build-spec.md M21 (distillation); roadmap R2.47
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- [ ] Decide the resolution (owner: you, with the planner's suggestion as default)
- [ ] Edit the listed docs in one PR so they agree
- [ ] Update the affected part-B task files (Requirements/Acceptance) if the decision differs from the default
- [ ] Add/adjust the regression test named below where code depends on it

## Verification

### Tests
- Doc gap: reviewed diff; where code depends on it, the named test in the affected task asserts the decided value.

### Scenarios
- Given the decided value, when the affected task is implemented, then its tests assert that value (no hard-coded alternative).

### Stress / failure injection
- n/a: documentation/spec consistency item.

## Acceptance criteria

- [ ] Docs listed under Doc sync agree with each other
- [ ] Affected tasks reference the decision
- [ ] Root cause noted in the progress log

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
