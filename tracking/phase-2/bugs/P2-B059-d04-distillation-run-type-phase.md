---
id: P2-B059
kind: gap
title: D04 lists a distillation run type that belongs to Phase 6
phase: 2
type: DOC
status: backlog
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.47]
roadmap_todos: []
modules: [M7, M21]
dashboards: [D04]
branch: p2/P2-B059-d04-distillation-run-type-phase
pr: ""
doc_sync: [docs/ui/dashboards/D04-research-lab.md]
doc_sync_status: n/a
found_in: docs/ui/dashboards/D04-research-lab.md (New run panel, Run type)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-B059 · D04 lists a distillation run type that belongs to Phase 6

## Goal / expected outcome

The docs agree and part-B tasks can be built without guessing: D04 lists 'tier A training (P2)' and 'distillation (P6)' with phase availability.

## Context & references

- [D04](../../../docs/ui/dashboards/D04-research-lab.md) · [phase 6](../../../docs/roadmap/phase-6-ai-models-treasury.md) R6.14
- Affects P2-T145

## Requirements

- **Steps to reproduce:** D04 (Phase 2) offers 'distillation (tier A/B)' as a run type; distillation from the teacher is R6.14 (P6). P2 needs a plain 'tier A training' run type instead.
- **Expected:** D04 lists 'tier A training (P2)' and 'distillation (P6)' with phase availability.
- **Actual:** see steps; the sources disagree or are silent.
- **Suggested fix:** Edit the D04 run-type list; P2-T145 hides distillation until P6.
- **Impact:** S4: cosmetic/spec clarity.

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

- `docs/ui/dashboards/D04-research-lab.md`: align with the decision.

## Branch & PR

- Branch: `p2/P2-B059-d04-distillation-run-type-phase`
- PR title: `P2-B059: D04 lists a distillation run type that belongs to Phase 6`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-B059` run

## Progress log

- 2026-10-21 00:00 · planner · opened
