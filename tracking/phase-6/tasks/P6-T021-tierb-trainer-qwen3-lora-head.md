---
id: P6-T021
kind: task
title: Tier B trainer: Qwen3 + LoRA + classification head (CE + λ·Brier)
phase: 6
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T020]
requirements: [R6.10]
roadmap_todos: [T6.24]
modules: [M21, M7]
dashboards: [D10]
branch: p6/P6-T021-tierb-trainer-qwen3-lora-head
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, third_party/LICENSES.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T021 · Tier B trainer: Qwen3 + LoRA + classification head (CE + λ·Brier)

## Goal / expected outcome

`mt_models.tierb.train` fine-tunes **Qwen3-0.6B or 1.7B** (dense, ONNX-exportable) with LoRA (rank 8–64) and a classification head (`Qwen3ForSequenceClassification` + PEFT `SEQ_CLS`, `modules_to_save=["score"]`), or a Clef-style joint schema head, using CE + λ·Brier, logged to MLflow.

## Context & references

- Roadmap: [R6.10](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.24
- Spec: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) stage 2 · [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models) · [research: decision models](../../../docs/research/decision-models-system-one.md) (HF + PEFT recipe; `MersivMedia/clef-finetune` CE + λ·Brier reference; TEI can't serve Qwen3 classification, issue #643)
- Cross-phase: P2 R2.44 MLflow, T2.41 registry stages
- Depends on (this phase): P6-T020

## Requirements

- Backbones: Qwen3-0.6B and Qwen3-1.7B, pinned HF revision (sha); Qwen3.5 hybrid layers avoided for ONNX.
- Heads: per-question SEQ_CLS head, or joint schema head scoring several questions in one pass (config switch); compare both on the first three questions.
- Loss: cross-entropy + λ·Brier (λ grid {0.1, 0.5, 1.0}); class weights from train fold.
- Hyper-parameters via Optuna with complexity penalty; selection on walk-forward validation folds (never the final holdout).
- Reproducibility: fixed seeds, deterministic CUDA flags where possible, dataset manifest hash and code commit logged; artefacts: LoRA adapter + head weights + tokenizer revision.
- Runs on the GPU (16–24 GB); CPU fallback allowed for 0.6B smoke runs only.
- Refuses datasets whose manifest shows `train_ok=false` rows (defence in depth).

## ToDo

- [ ] Trainer module + config schema (`configs/tierb/<question>.yaml`).
- [ ] Joint-schema-head variant (adapted from the clef-finetune pattern; licence checked; never run on real Clef weights).
- [ ] Optuna study + MLflow logging (metrics per fold: log-loss, Brier, accuracy).
- [ ] Prefect task wrapper for use by P6-T031/P6-T032.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: loss function (CE + λ·Brier) gradients on toy tensors; head config.
- Smoke: 0.6B trains 50 steps on a tiny dataset on CPU in CI (marked slow) and loss decreases.
- Determinism: two runs with the same seed on GPU produce metrics within 1e-3.

### Scenarios
- Given the `news_direction` dataset, when trained, then MLflow holds an adapter, head, metrics per fold and the dataset hash.
- Given a dataset manifest with Telegram-lineage rows, then training refuses to start.

### Stress / failure injection
- GPU OOM injected (batch too large): trainer reduces batch via gradient accumulation and logs it, or fails cleanly without corrupting MLflow.

## Acceptance criteria

- [ ] At least `news_direction`, `event_type`, `veto` trained for 0.6B and 1.7B with MLflow runs.
- [ ] Reproducibility checks pass.
- [ ] CI green.

## Exceptions & edge cases

- GPU unavailable: training jobs queue and alert; never silently fall back to multi-day CPU training.
- Class imbalance extreme (< 2% minority): flag question as unsuitable for SEQ_CLS; keep SemIf.

## Cardinal rules (do NOT)

- Do NOT train on teacher labels alone; outcome-corrected datasets only.
- Do NOT download unpinned model revisions.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: chosen λ, ranks, backbone results.
- `third_party/LICENSES.md`: any vendored training code.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.24 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T021-tierb-trainer-qwen3-lora-head`
- PR title: `P6-T021: Tier B trainer: Qwen3 + LoRA + classification head (CE + λ·Brier)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T021` run

## Progress log

- 2026-10-21 00:00 · planner · created
