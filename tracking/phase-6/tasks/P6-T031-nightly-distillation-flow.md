---
id: P6-T031
kind: task
title: Nightly distillation flow with gated promotion
phase: 6
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T020, P6-T022, P6-T030, P2-T125]
requirements: [R6.14]
roadmap_todos: [T6.27]
modules: [M21, M7]
dashboards: [D10]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [prefect, mlflow, gpu]
branch: p6/P6-T031-nightly-distillation-flow
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/02-v1-architecture.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T031 · Nightly distillation flow with gated promotion

## Goal / expected outcome

A nightly Prefect flow distils the teacher log + outcomes into tier-A and tier-B candidates, calibrates and benchmarks them, registers them as candidates and opens promotion proposals — never promoting by itself; the teacher stays in shadow.

## Context & references

- Roadmap: [R6.14](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.27
- Spec: [02 F4](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 5–6 · [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models) (distillation into tier A and tier B) · [10 §6](../../../docs/10-memory-rag-and-models.md#6-where-this-lands-in-the-build)
- Cross-phase: P2-T125 (tier-A training pipeline; teacher labels added as an extra source without changing existing model versions, 10 §4.3)
- Depends on (this phase): P6-T020, P6-T022, P6-T030

## Requirements

- Schedule: nightly 02:00 Australia/Sydney (configurable), skip if GPU busy with production > threshold.
- Steps: build datasets (P6-T020) → train tier-B candidate (P6-T021, warm-start from production adapter) and tier-A candidate (P2 pipeline with tier-B scores as features) → calibrate (P6-T022) → quick bake-off subset vs production → register candidate → proposal row for D10.
- Distillation lineage recorded: teacher runs + outcomes used (D10 Registry detail).
- Budget: time cap 4 h; failure alerts; partial results kept as failed runs in MLflow.
- Respects `train_ok`; uses only settled decisions.

## ToDo

- [ ] Prefect flow `distill_nightly`.
- [ ] Proposal table + notification.
- [ ] Lineage writer.
- [ ] Tests; docs.

## Verification

### Tests
- Integration (small data): flow runs end-to-end and registers candidates without touching production routing.
- Unit: skip logic when GPU busy; idempotent re-run for the same date.

### Scenarios
- Given new settled decisions since yesterday, then a candidate with lineage appears in D10 as `candidate`.
- Given the flow fails at calibration, then production is untouched and an alert is sent.

### Stress / failure injection
- Run with 4× usual data volume: finishes within the 4 h cap or stops cleanly at the cap.

## Acceptance criteria

- [ ] Flow green for 3 consecutive nights before P6-T065 starts.
- [ ] No automatic promotions (audit shows none).

## Exceptions & edge cases

- Host reboot mid-flow: next night's run starts fresh; partial artefacts marked failed.

## Cardinal rules (do NOT)

- Do NOT auto-promote; promotion is P6-T030 via commands.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §6: nightly flow steps.
- `docs/02-v1-architecture.md` F4: flow name.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.27 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T031-nightly-distillation-flow`
- PR title: `P6-T031: Nightly distillation flow with gated promotion`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T031` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (cross-phase dep P2-T125; run fields)
