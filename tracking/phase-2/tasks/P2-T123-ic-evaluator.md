---
id: P2-T123
kind: task
title: Feature IC, rank-IC and decay evaluator
phase: 2
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T121, P2-T122]
requirements: [R2.46]
roadmap_todos: [T2.29]
modules: [M6, M7]
dashboards: [D04]
branch: p2/P2-T123-ic-evaluator
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

# P2-T123 · Feature IC, rank-IC and decay evaluator

## Goal / expected outcome

An evaluator that reports, per feature version and instrument set, the information coefficient, rank-IC and IC decay across horizons, logged to MLflow, so features are chosen on evidence.

## Context & references

- Roadmap: [R2.46](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.29
- [03 M6 versioning and evaluation](../../../docs/03-build-spec.md#m6-features--mt_features)

## Requirements

- IC (Pearson) and rank-IC (Spearman) between feature at t and forward return over horizons {1, 5, 20, 60} bars; per period and aggregate with t-stat (Newey-West).
- Decay curve: IC vs horizon; half-life estimate.
- Point-in-time: features and forward returns from P2-T103 datasets; forward returns never enter the feature computation.
- Run as a lab job (`run_type=feature_eval`), results to MLflow and `features.def` metadata (latest IC summary).

## ToDo

- [ ] Implement `mt_features/evaluate.py`
- [ ] Register `feature_eval` JobRunner
- [ ] Tests on synthetic predictive/non-predictive features
- [ ] Doc

## Verification

### Tests
- Unit: synthetic feature = future return + noise yields positive IC decaying with horizon; random feature IC ~ 0.

### Scenarios
- Given a feature that leaks the future (uses forward return), then the evaluator's leakage guard (feature timestamp ≥ return start) raises.

### Stress / failure injection
- Evaluate 158 Alpha158 features × 30 symbols in one job within the 2 h cap.

## Acceptance criteria

- [ ] IC, rank-IC, decay reported per feature
- [ ] Results in MLflow
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Overlapping forward returns inflate t-stats: Newey-West lag = horizon − 1.

## Cardinal rules (do NOT)

- Do NOT use IC results computed on the test period to select features for that same test.
- Do NOT read research/backtest data except through `mt_store.pit(as_of=…)`; the `pit` CI bypass test must stay green.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M6: evaluator outputs.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.29 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T123-ic-evaluator`
- PR title: `P2-T123: Feature IC, rank-IC and decay evaluator`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T123` run

## Progress log

- 2026-10-21 00:00 · planner · created
