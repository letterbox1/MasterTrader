---
id: P2-B052
kind: gap
title: D04 result tabs omit 2×/3× cost stress, per-year/regime, trial counter and worst fold
phase: 2
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.42]
roadmap_todos: []
modules: [M7, M15]
dashboards: [D04]
branch: p2/P2-B052-d04-missing-harness-extensions
pr: ""
doc_sync: [docs/ui/dashboards/D04-research-lab.md]
doc_sync_status: n/a
found_in: docs/ui/dashboards/D04-research-lab.md (Robustness and Costs tabs)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-B052 · D04 result tabs omit 2×/3× cost stress, per-year/regime, trial counter and worst fold

## Goal / expected outcome

The docs agree and part-B tasks can be built without guessing: D04 result tabs show every harness section the gate evaluator uses: cost sensitivity 0.5×/1×/2×/3× with 2×/3× verdicts, per-year and per-regime tables, trial count next to DSR, worst fold and positive-fold share.

## Context & references

- [D04](../../../docs/ui/dashboards/D04-research-lab.md) · [D03 'Additions from the CryptoTrader review'](../../../docs/ui/dashboards/D03-strategies.md) · [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8)
- Affects P2-T146

## Requirements

- **Steps to reproduce:** D04 Costs tab specifies sensitivity at '0.5×/1×/2× costs'; the Robustness tab lists walk-forward folds, MC, bootstrap, DSR and stability only. 14 §6/R2.42 require 2× and 3× cost stress, per-year and per-regime results, the trial counter and worst-fold judging; only D03 mentions them.
- **Expected:** D04 result tabs show every harness section the gate evaluator uses: cost sensitivity 0.5×/1×/2×/3× with 2×/3× verdicts, per-year and per-regime tables, trial count next to DSR, worst fold and positive-fold share.
- **Actual:** see steps; the sources disagree or are silent.
- **Suggested fix:** Edit D04 Robustness and Costs rows accordingly (P2-T146 already implements this default).
- **Impact:** S3: exit criterion 1 ('validation report shows all harness sections') cannot be shown in D04 as specified.

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

- Branch: `p2/P2-B052-d04-missing-harness-extensions`
- PR title: `P2-B052: D04 result tabs omit 2×/3× cost stress, per-year/regime, trial counter and worst fold`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-B052` run

## Progress log

- 2026-10-21 00:00 · planner · opened
