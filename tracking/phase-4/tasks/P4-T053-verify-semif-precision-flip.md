---
id: P4-T053
kind: task
title: SemIf gate precision/recall on your labels and flip rate (determinism)
phase: 4
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T049]
requirements: [R4.12]
roadmap_todos: [T4.63]
modules: [M21]
dashboards: [D10]
branch: p4/P4-T053-verify-semif-precision-flip
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T053 · SemIf gate precision/recall on your labels and flip rate (determinism)

## Goal / expected outcome

A report gives the relevance gate's precision, recall, F1 and balanced accuracy at the calibrated threshold on your ~200 labels (with bootstrap CIs), per source kind, plus the **flip rate** of argmax decisions across 3 repeated runs and across a restart, on the deployed backend.

## Context & references

- Roadmap: [R4.12](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.63](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Design: [10 §4.3 determinism + bake-off metrics](../../../docs/10-memory-rag-and-models.md#43-design) · research [SemIf](../../../docs/research/decision-models-system-one.md) (0.81 balanced accuracy reference; 5–6/777 flips with prefix reuse)

## Requirements

- Precision target at the threshold ≥ 0.9 (from P4-T048); recall reported; balanced accuracy compared with the 0.81 reference.
- Flip rate = share of decisions whose argmax changes across 3 runs (target 0 on CPU, ≤ 0.5% on GPU with determinism controls).
- Latency p50/p95 per document recorded.
- Report logged to MLflow and summarised in `docs/10` §4.3.

## ToDo

- [ ] Evaluation script `tools/bench/semif_eval.py`.
- [ ] Run on labelled batch; bootstrap CIs.
- [ ] Determinism runs (3× + restart).
- [ ] Publish report.

## Verification

### Tests
- Evaluation script unit tests (metric code).

### Scenarios
- Given flip rate > 0.5% on GPU, then file a bug, switch to batch size 1 and re-run.
- Given precision < 0.9 at any threshold, then keep the gate permissive and record it for P6.

### Stress / failure injection
- Repeat determinism run under concurrent load (queue depth 50) to check batching effects.

## Acceptance criteria

- [ ] Report with P/R/F1/balanced accuracy + CIs, flip rate and latency published
- [ ] Results meet targets or bugs filed with decisions
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Small label set: report CIs; don't over-claim.

## Cardinal rules (do NOT)

- Do NOT evaluate on documents used to pick the threshold without reporting it (use cross-validation).
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md`: §4.3: stage-1 measured precision/recall/flip rate
- `docs/roadmap/phase-4-intel.md`: tick T4.63 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T053-verify-semif-precision-flip`
- PR title: `P4-T053: SemIf gate precision/recall on your labels and flip rate (determinism)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T053` run

## Progress log

- 2026-10-21 00:00 · planner · created
