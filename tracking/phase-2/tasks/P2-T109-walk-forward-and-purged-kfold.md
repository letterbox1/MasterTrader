---
id: P2-T109
kind: task
title: Walk-forward (worst fold) and purged K-fold validation
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T105, P2-T106]
requirements: [R2.42]
roadmap_todos: [T2.27]
modules: [M7]
dashboards: [D04, D03]
tools: [uv]
mcp: []
env: []
services: []
branch: p2/P2-T109-walk-forward-and-purged-kfold
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-T109 · Walk-forward (worst fold) and purged K-fold validation

## Goal / expected outcome

`mt_lab.validation.wf` and `.purged_kfold` produce out-of-sample fold results judged on the share of positive folds and the worst fold (never the average), using purging and an embargo so no label overlaps leak across folds.

## Context & references

- Roadmap: [R2.42](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.27
- [14 §6 gate 3](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) (worst fold, share of positive folds) · [03 §8 items 1 and 7](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable)
- Shown in [D04 Robustness tab](../../../docs/ui/dashboards/D04-research-lab.md) and [D03 detail 'worst walk-forward fold'](../../../docs/ui/dashboards/D03-strategies.md)
- Runs on truth results only for gate purposes (P2-T105); screener allowed for exploration
- Gate default ([16 §2.4](../../../docs/16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile), per-strategy gate profile, loosening C3): **≥ 60% of folds positive and worst fold ≥ −(sleeve halt drawdown)** (sleeve halt default 15%).

## Requirements

- Walk-forward: anchored and rolling modes; configurable train/test lengths (defaults: 24 months train / 3 months test for daily/4h strategies; scaled by bar spec); re-optimisation per fold optional (Optuna inside the train window only).
- Outputs per fold: OOS return, Sharpe, max DD, trade count, after measured costs; summary: share of positive folds, worst-fold Sharpe/return/drawdown, fold dispersion; the worst-fold comparison uses the strategy's sleeve halt drawdown from the layered policy, never a constant.
- Purged K-fold (López de Prado): K default 5, purge observations whose label horizon overlaps the test fold, embargo default 1% of observations after each test fold.
- Fold boundaries align to bar closes (P2-T103 convention); each fold's data hash recorded.
- Every fold trial registers with the trial counter (P2-T108).

## ToDo

- [ ] Implement fold generators (anchored, rolling, purged K-fold with embargo) in `mt_lab/validation/folds.py`
- [ ] Implement fold executor that runs truth backtests per fold via `JobRunner` sub-jobs (parallel up to the job's worker cap)
- [ ] Compute summary (positive share, worst fold) and persist to `strategy.experiment` + MLflow
- [ ] Known-answer tests incl. a leakage fixture
- [ ] Doc defaults in 14 §6

## Verification

### Tests
- Unit: purged K-fold drops exactly the overlapping observations on a synthetic label-horizon fixture; embargo size correct.
- Unit: worst fold equals min over folds; positive share counts folds with OOS return > 0 after costs.
- Integration: walk-forward of an EMA template over a 3-year fixture produces N folds with stored data hashes.

### Scenarios
- Given a strategy that only works in one year, when walk-forward runs, then the average looks fine but the worst fold is negative and is what the gate sees.
- Given a label horizon of 10 bars, when purged K-fold runs, then no training sample's horizon intersects a test fold (asserted).

### Stress / failure injection
- 20-fold walk-forward on 1m bars with 4 workers completes within the job's 2 h time cap or fails cleanly with `timed_out`.
- One fold's sub-job crashes: the experiment is marked incomplete, never summarised as if complete.

## Acceptance criteria

- [ ] Fold summaries expose share of positive folds and worst fold
- [ ] Purge/embargo leakage test passes
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Too little data for the requested folds: refuse with the minimum required range.
- Strategies with very few trades per fold: fold flagged 'insufficient trades' (< 10) and counted as non-positive.

## Cardinal rules (do NOT)

- Do NOT judge walk-forward on the mean fold.
- Do NOT optimise on test-fold data.
- Do NOT read research/backtest data except through `mt_store.pit(as_of=…)`; the `pit` CI bypass test must stay green.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §6: default fold lengths, K and embargo.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.27 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T109-walk-forward-and-purged-kfold`
- PR title: `P2-T109: Walk-forward (worst fold) and purged K-fold validation`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T109` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (walk-forward gate default from 16 §2.4 (≥ 60% positive, worst fold ≥ −sleeve halt DD))
