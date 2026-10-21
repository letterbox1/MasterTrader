---
id: P2-B050
kind: gap
title: Deflated Sharpe gate threshold conflicts (> 0 vs > 0.95)
phase: 2
type: DOC
status: backlog
priority: high
size: XS
severity: S2
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.42]
roadmap_todos: []
modules: [M7]
dashboards: [D03, D04]
branch: p2/P2-B050-deflated-sharpe-threshold-conflict
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/14-strategy-evidence-and-validation.md]
doc_sync_status: n/a
found_in: docs/03-build-spec.md §8 items 2 and 7; docs/02-v1-architecture.md §13; docs/14-strategy-evidence-and-validation.md §6–7
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-B050 · Deflated Sharpe gate threshold conflicts (> 0 vs > 0.95)

## Goal / expected outcome

The docs agree and part-B tasks can be built without guessing: one deflated-Sharpe definition and threshold used by the gate evaluator and shown in D03/D04.

## Context & references

- [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) · [02 §13](../../../docs/02-v1-architecture.md#13-asset-coverage--promotion-gates) · [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7)
- Affects P2-T110, P2-T114, P2-T143

## Requirements

- **Steps to reproduce:** Read 03 §8 item 2 ('deflated Sharpe > 0') and 02 §13 item 2 (same), then 03 §8 item 7 and 14 §6 gate 2 ('> 0.95'), then 14 §7 ('deflated Sharpe > 0 at 95%').
- **Expected:** one deflated-Sharpe definition and threshold used by the gate evaluator and shown in D03/D04.
- **Actual:** see steps; the sources disagree or are silent.
- **Suggested fix:** DSR is a probability: state the gate as 'DSR (probability the true Sharpe > 0) > 0.95'; rewrite 03 §8 item 2, 02 §13 and 14 §7 to that wording.
- **Impact:** S2: the gate evaluator could pass strategies that should fail (> 0 is almost always true for a probability).

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

- `docs/03-build-spec.md`: align with the decision.
- `docs/02-v1-architecture.md`: align with the decision.
- `docs/14-strategy-evidence-and-validation.md`: align with the decision.

## Branch & PR

- Branch: `p2/P2-B050-deflated-sharpe-threshold-conflict`
- PR title: `P2-B050: Deflated Sharpe gate threshold conflicts (> 0 vs > 0.95)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-B050` run

## Progress log

- 2026-10-21 00:00 · planner · opened
