---
id: P6-T028
kind: task
title: Fine-tune Laya on our data for the bake-off
phase: 6
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T020, P6-T027]
requirements: [R6.12]
roadmap_todos: [T6.25]
modules: [M21]
dashboards: [D10]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [mlflow, gpu]
branch: p6/P6-T028-laya-finetune
pr: ""
doc_sync: [docs/research/decision-models-system-one.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T028 · Fine-tune Laya on our data for the bake-off

## Goal / expected outcome

Laya (ModernBERT 322–421M) is fine-tuned and calibrated on the same outcome-corrected datasets as our own head, so the bake-off compares like with like (zero-shot Laya is below the majority baseline).

## Context & references

- Roadmap: [R6.12](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.25
- Spec: [10 §4.1](../../../docs/10-memory-rag-and-models.md#41-what-decision-models-are-and-the-candidates) (Laya weak zero-shot; useful only after fine-tuning; 512–1024 context) · [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design)
- [research: decision models](../../../docs/research/decision-models-system-one.md)
- Depends on (this phase): P6-T020, P6-T027

## Requirements

- Same folds, same states (≤ 320 tokens, inside Laya's 512–1024 context) and same calibration procedure (P6-T022).
- Artefacts in MLflow tagged `contender=laya-ft`.
- Provenance filters identical to our trainer.

## ToDo

- [ ] Laya fine-tune script (`pip install laya` pinned by hash) wrapping our dataset loader.
- [ ] Calibration via the shared module.
- [ ] MLflow logging.
- [ ] Tests; docs.

## Verification

### Tests
- Smoke: fine-tune runs on a tiny dataset; loss decreases.
- Same-fold check: dataset hashes equal those used by the own-head run.

### Scenarios
- Given the `news_direction` dataset, then a calibrated Laya-ft model is registered as a bake-off contender.

### Stress / failure injection
- n/a: offline training job.

## Acceptance criteria

- [ ] Laya-ft registered for the bake-off questions with calibration reports.

## Exceptions & edge cases

- Context overflow → state builder truncation (never raw docs).

## Cardinal rules (do NOT)

- Do NOT compare zero-shot Laya to fine-tuned heads as if equal; label it.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/research/decision-models-system-one.md`: our Laya-ft results.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.25 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T028-laya-finetune`
- PR title: `P6-T028: Fine-tune Laya on our data for the bake-off`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T028` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields only; no decision change)
