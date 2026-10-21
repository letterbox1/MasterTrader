---
id: P2-B060
kind: gap
title: Default paper period differs between 03 §8 (3 months) and 14 §6 (2–4 weeks)
phase: 2
type: DOC
status: backlog
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.06]
roadmap_todos: []
modules: [M0, M7]
dashboards: [D03]
branch: p2/P2-B060-paper-period-default-conflict
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: docs/03-build-spec.md §8 item 5; docs/14-strategy-evidence-and-validation.md §6 gate 7; docs/02-v1-architecture.md §13
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-B060 · Default paper period differs between 03 §8 (3 months) and 14 §6 (2–4 weeks)

## Goal / expected outcome

The docs agree and part-B tasks can be built without guessing: one rule shown in D03 Gates: default ≥ 3 months, P1 sleeves ≥ 8 weeks, memecoin ≥ 300 trades.

## Context & references

- [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) · [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [phase 7](../../../docs/roadmap/phase-7-prove-and-go-live.md) R7.02
- Affects P2-T143 (Gates 'paper period elapsed / required'), P2-T180

## Requirements

- **Steps to reproduce:** 03 §8 item 5 and 02 §13 say paper/approve default 3 months; 14 §6 gate 7 says ≥ 2–4 weeks (≥ 8 weeks for P1 sleeves, ≥ 300 trades memecoin). R7.02 combines them ('default ≥ 3 months; P1 sleeves ≥ 8 weeks').
- **Expected:** one rule shown in D03 Gates: default ≥ 3 months, P1 sleeves ≥ 8 weeks, memecoin ≥ 300 trades.
- **Actual:** see steps; the sources disagree or are silent.
- **Suggested fix:** Align 14 §6 gate 7 with R7.02 wording.
- **Impact:** S4: D03 could display the wrong 'required' period.

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

- `docs/14-strategy-evidence-and-validation.md`: align with the decision.
- `docs/03-build-spec.md`: align with the decision.

## Branch & PR

- Branch: `p2/P2-B060-paper-period-default-conflict`
- PR title: `P2-B060: Default paper period differs between 03 §8 (3 months) and 14 §6 (2–4 weeks)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-B060` run

## Progress log

- 2026-10-21 00:00 · planner · opened
