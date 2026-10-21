---
id: P2-B054
kind: gap
title: D03 builder template list differs from the R2.02 / 03 M0 template set
phase: 2
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.02]
roadmap_todos: []
modules: [M0, M15]
dashboards: [D03]
branch: p2/P2-B054-d03-template-list-mismatch
pr: ""
doc_sync: [docs/ui/dashboards/D03-strategies.md]
doc_sync_status: n/a
found_in: docs/ui/dashboards/D03-strategies.md (builder 'Template' tab)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-B054 · D03 builder template list differs from the R2.02 / 03 M0 template set

## Goal / expected outcome

The docs agree and part-B tasks can be built without guessing: D03 states that the template tab is driven by `/strategies/templates` and lists the R2.02 set, with phase availability for market making (P6, optional) and LLM-signal (P6).

## Context & references

- [D03 builder](../../../docs/ui/dashboards/D03-strategies.md) · [03 M0](../../../docs/03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe) · [R2.02](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements)
- Affects P2-T144

## Requirements

- **Steps to reproduce:** D03 lists scalping, intraday, EMA/MA, mean reversion, breakout, swing, grid/DCA, market making, pairs, event, ML-signal, LLM/decision-model signal. R2.02 adds deterministic rule-based, funding carry, cross-sectional momentum, token unlock and memecoin momentum (paper-only), and puts market making and LLM-signal in later phases (P6).
- **Expected:** D03 states that the template tab is driven by `/strategies/templates` and lists the R2.02 set, with phase availability for market making (P6, optional) and LLM-signal (P6).
- **Actual:** see steps; the sources disagree or are silent.
- **Suggested fix:** Edit the D03 template list; P2-T144 renders from the API so no hard-coded list exists in the UI.
- **Impact:** S3: confusion over which templates must exist in P2 and which must be hidden.

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

- `docs/ui/dashboards/D03-strategies.md`: align with the decision.

## Branch & PR

- Branch: `p2/P2-B054-d03-template-list-mismatch`
- PR title: `P2-B054: D03 builder template list differs from the R2.02 / 03 M0 template set`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-B054` run

## Progress log

- 2026-10-21 00:00 · planner · opened
