---
id: P6-T020
kind: task
title: Outcome-corrected distillation dataset builder
phase: 6
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T013, P6-T018, P6-T019]
requirements: [R6.10, R6.14, R6.13]
roadmap_todos: [T6.24]
modules: [M21, M7, M6]
dashboards: [D10]
branch: p6/P6-T020-distillation-dataset-builder
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T020 · Outcome-corrected distillation dataset builder

## Goal / expected outcome

A reproducible builder turns the teacher log (M8 decisions + tier-B context), feature snapshots, settlements and user labels into per-question training sets, corrected against realised outcomes, split with purged/embargoed walk-forward folds and fully provenance-filtered.

## Context & references

- Roadmap: [R6.10](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.14](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.13](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.24
- Spec: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (distilled from M8, corrected against outcomes, purged/embargoed walk-forward, option shuffle/rename augmentation) · [10 §6](../../../docs/10-memory-rag-and-models.md#6-where-this-lands-in-the-build) (M6 feature snapshots per decision) · [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms)
- Flow: [02 F4](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 5
- Depends on (this phase): P6-T013, P6-T018, P6-T019

## Requirements

- Inputs via `pit`: `audit.decision_run`/`audit.signal` (teacher), `audit.decision_settlement` (outcomes), `models.label` (user/outcome), feature snapshots, source documents (state built by P6-T018).
- Outcome correction: label = outcome where available (forward return sign beyond a cost threshold / barrier hit); teacher label used only as a soft target weight; disagreement stats logged.
- Provenance filter: drop rows with `train_ok=false` or any Telegram lineage; count excluded per reason (shown in D10).
- Splits: purged K-fold walk-forward with embargo ≥ max horizon; fold boundaries recorded.
- Augmentation: option order shuffle and option rename on train folds only.
- Output: Parquet dataset + manifest (row counts, hash, time range, exclusions) logged to MLflow; deterministic given the same inputs.

## ToDo

- [ ] `mt_models.distill.dataset` builder + CLI `mt-models build-dataset --question ... --as-of ...`.
- [ ] Fold generator with purge/embargo; augmentation.
- [ ] Exclusion accounting + MLflow logging.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: purge/embargo leaves no overlap between label horizons and test fold; augmentation only on train.
- Determinism: two builds with the same inputs produce identical hashes.
- Provenance: a seeded Telegram-lineage row never appears in any split.

### Scenarios
- Given the teacher said bull and the outcome was −4%, then the training label is bear (outcome-corrected) and the disagreement is counted.
- Given fewer than the minimum rows per class (default 200), then the builder refuses with a clear message instead of training on noise.

### Stress / failure injection
- 1M rows build in < 15 min on the host; memory < 8 GB (streamed Parquet).

## Acceptance criteria

- [ ] Dataset manifests in MLflow with exclusion counts.
- [ ] Leakage tests (purge/embargo) green.
- [ ] Label-provenance checks green (also P6-T056).

## Exceptions & edge cases

- Unsettled decisions excluded until settled.
- Schema drift in feature snapshots → builder fails closed with the offending feature.

## Cardinal rules (do NOT)

- Do NOT use shadow outputs as labels; do NOT use rows with `train_ok=false`.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: dataset manifest fields and label rule.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.24 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T020-distillation-dataset-builder`
- PR title: `P6-T020: Outcome-corrected distillation dataset builder`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T020` run

## Progress log

- 2026-10-21 00:00 · planner · created
