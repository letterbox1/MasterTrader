---
id: P2-T115
kind: task
title: Optuna sweeps with complexity penalty and A/B on identical data
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T104, P2-T105, P2-T108]
requirements: [R2.44, R2.07]
roadmap_todos: [T2.27]
modules: [M7, M0]
dashboards: [D04]
branch: p2/P2-T115-optuna-sweeps-and-ab
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T115 · Optuna sweeps with complexity penalty and A/B on identical data

## Goal / expected outcome

`lab.sweep.run` optimises a strategy's parameters with Optuna over the manifest's parameter schema, penalising complexity, logging every trial to MLflow and the trial counter, and the lab can run A/B comparisons of two strategy versions on byte-identical data.

## Context & references

- Roadmap: [R2.44, R2.07](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.27 (R2.07 shadow mode is engine-side, part A)
- [03 M7 optimisation](../../../docs/03-build-spec.md#m7-research-lab--mt_lab) · [03 M0 experimentation](../../../docs/03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe) · [01 §3.3 hyperopt overfit warning](../../../docs/01-repo-vetting-report.md#33-freqtrade--reference-only)
- [D04 'Sweep space' and parameter-stability heatmap](../../../docs/ui/dashboards/D04-research-lab.md); parameter schemas from part A's templates (T2.21)

## Requirements

- Search space from the manifest param schema (types, ranges, defaults); objective selectable (Sharpe, Calmar, net return) on in-sample folds only.
- Complexity penalty: objective − λ·(number of free parameters) − μ·(rule count), λ/μ configurable (default λ = 0.05 Sharpe per free parameter); recorded with the study.
- Samplers: TPE default, seeded; pruning via Optuna median pruner; storage in Postgres (`optuna` schema) so studies survive restarts.
- Every trial = MLflow run + trial-counter increment (P2-T108); best params never auto-promoted, they must pass validation.
- Parameter-stability heatmap data (2-D slices around the optimum) for D04 Robustness.
- A/B: two versions run on the same `data_hash` + `cost_snapshot_id` + seed; output a paired comparison (difference of returns, paired bootstrap CI).

## ToDo

- [ ] Implement `mt_lab/optimise/sweep.py` (Optuna study, penalty, pruning, Postgres storage)
- [ ] Implement stability-slice computation
- [ ] Implement `mt_lab/optimise/ab.py` paired comparison
- [ ] Register `sweep` and `ab` JobRunners; MLflow + trial counter hooks
- [ ] Tests + docs

## Verification

### Tests
- Unit: penalty lowers the score of a 6-parameter variant vs a 2-parameter variant with equal raw Sharpe.
- Integration: 30-trial sweep on the screener completes; 30 MLflow runs; trial count +30.
- Integration: A/B on identical data asserts equal data hashes and returns a paired CI.

### Scenarios
- Given the worker restarts mid-sweep, then the study resumes from Postgres storage without repeating finished trials.
- Given the best trial, when the user tries to promote it directly, then lifecycle requires a validation run first.

### Stress / failure injection
- 1,000-trial screener sweep with 4 workers: Optuna storage contention handled (no lost trials); memory bounded.

## Acceptance criteria

- [ ] Sweeps penalise complexity and log every trial
- [ ] A/B uses byte-identical inputs
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Parameters with conditional dependencies (e.g. only when `use_filter=true`) map to Optuna conditional spaces.
- Truth-engine sweeps are expensive: cap trials (default 100) unless overridden.

## Cardinal rules (do NOT)

- Do NOT optimise on out-of-sample or test-fold data.
- Do NOT auto-promote sweep winners.
- Do NOT read research/backtest data except through `mt_store.pit(as_of=…)`; the `pit` CI bypass test must stay green.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M7: penalty definition and defaults.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.27 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T115-optuna-sweeps-and-ab`
- PR title: `P2-T115: Optuna sweeps with complexity penalty and A/B on identical data`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T115` run

## Progress log

- 2026-10-21 00:00 · planner · created
