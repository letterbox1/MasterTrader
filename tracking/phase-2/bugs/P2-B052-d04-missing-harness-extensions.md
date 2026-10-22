---
id: P2-B052
kind: gap
title: D04 result tabs omit 2×/3× cost stress, per-year/regime, trial counter and worst fold
phase: 2
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B052-d04-missing-harness-extensions
pr: ""
doc_sync: [docs/ui/dashboards/D04-research-lab.md]
doc_sync_status: done
found_in: docs/ui/dashboards/D04-research-lab.md (Robustness and Costs tabs)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Decision recorded: D04 result tabs show every harness section the gate evaluator uses
- [x] Docs agree: D04 Robustness and Costs rows
- [x] Tasks updated: P2-T146

## Verification

### Tests
- Doc gap: reviewed diff; where code depends on it, the named test in the affected task asserts the decided value.

### Scenarios
- Given the decided value, when the affected task is implemented, then its tests assert that value (no hard-coded alternative).

### Stress / failure injection
- n/a: documentation/spec consistency item.

## Acceptance criteria

- [x] Docs agree in one place, cross-linked from the others (D04 Robustness row (positive-fold share, worst fold, DSR + trial counter, per-year/per-regime) and Costs row (0.5×/1×/2×/3×, 2× verdict, 3× reported))
- [x] Affected tasks reference the decision (P2-T146)

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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (resolved by 17 §D (P2-B052, suggested fix adopted); docs carry it (D04 Robustness row (positive-fold share, worst fold, DSR + trial counter, per-year/per-regime) and Costs row (0.5×/1×/2×/3×, 2× verdict, 3× reported)); implementation owned by P2-T146)
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D (P2-B052, suggested fix adopted)); docs updated: D04 Robustness row (positive-fold share, worst fold, DSR + trial counter, per-year/per-regime) and Costs row (0.5×/1×/2×/3×, 2× verdict, 3× reported); implementation owned by P2-T146
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
