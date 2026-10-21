---
id: P2-T125
kind: task
title: Tier A training pipeline (dataset, labels, GBDT/linear/MLP)
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T109, P2-T120, P2-T107]
requirements: [R2.47]
roadmap_todos: [T2.30]
modules: [M21, M7]
dashboards: [D04]
branch: p2/P2-T125-tier-a-training-pipeline
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T125 · Tier A training pipeline (dataset, labels, GBDT/linear/MLP)

## Goal / expected outcome

A lab job that trains a tier-A model (LightGBM/XGBoost/linear/small MLP) for a strategy from versioned M6 features and outcome labels, using time-ordered purged splits, and logs everything to MLflow — the first stage of train → calibrate → compile → in-process.

## Context & references

- Roadmap: [R2.47](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.30
- [10 §4.3 tier A](../../../docs/10-memory-rag-and-models.md#43-design) · [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models) · [12 §5 provenance](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) (training refuses `train_ok=false`)
- Label source before the P6 teacher exists is unspecified: P2-B057 (this task uses outcome labels: forward-return sign / triple-barrier)
- Distillation from the M8 teacher is P6 ([phase 6](../../../docs/roadmap/phase-6-ai-models-treasury.md) R6.14); this pipeline must accept a teacher-label source later without redesign

## Requirements

- Dataset: feature matrix from `features.def` versions listed in the manifest, via `pit`; rows with `train_ok=false` refused (hard error if any present).
- Labels (pluggable `LabelSource`): forward-return sign over horizon h, triple-barrier (tp/sl/time) — teacher labels added in P6.
- Splits: time-ordered train / calibration holdout / test with purge + embargo (P2-T109 utilities); no shuffling.
- Models: LightGBM (default), XGBoost, logistic/linear, small MLP (≤ 2 hidden layers, ≤ 64 units) — all CPU.
- Logged: feature list + versions, label config, data range, as_of, hyper-params, metrics (log-loss, AUC, Brier) per split, model artefact; `run_type=tier_a_train`.
- Model size budget so inference stays < 50 µs p99 after compile (e.g. LightGBM ≤ 300 trees × depth 6; enforced as a warning in training).

## ToDo

- [ ] Implement `packages/mt_models/tier_a/train.py` (dataset, LabelSource, splits, trainers)
- [ ] Register `tier_a_train` JobRunner, the `lab.tier_a.train` command (P2-B056) and the D04 run type
- [ ] Provenance refusal + tests
- [ ] MLflow logging
- [ ] Doc

## Verification

### Tests
- Unit: purged split never lets a label horizon cross into the holdout.
- Unit: a dataset containing one `train_ok=false` row → training refused.
- Integration: LightGBM trains on a fixture and logs to MLflow with all fields.

### Scenarios
- Given features unavailable for part of the range, then rows are dropped and the count is logged (never imputed with future values).
- Given a request to train with shuffled K-fold, then it is refused (time-ordered only).

### Stress / failure injection
- Train on 2M rows × 200 features within 30 min on 8 cores; memory < 16 GB.

## Acceptance criteria

- [ ] End-to-end training job produces an MLflow run with artefact and metrics
- [ ] Provenance refusal enforced
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Class imbalance: report base rate; calibration (P2-T126) handles probability scaling.
- Teacher labels (P6) must be a new `LabelSource`, not a change to existing label versions.

## Cardinal rules (do NOT)

- Do NOT train on rows with `train_ok = false` (incl. any Telegram-derived feature).
- Do NOT use GPU-only models for tier A.
- Do NOT put Telegram text (or any `model_input_ok = false` / `train_ok = false` row) into a model, prompt, RAG index or training set (12 §4–5).
- Do NOT read research/backtest data except through `mt_store.pit(as_of=…)`; the `pit` CI bypass test must stay green.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: P2 label sources.
- `docs/03-build-spec.md` M21: training job.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.30 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T125-tier-a-training-pipeline`
- PR title: `P2-T125: Tier A training pipeline (dataset, labels, GBDT/linear/MLP)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T125` run

## Progress log

- 2026-10-21 00:00 · planner · created
