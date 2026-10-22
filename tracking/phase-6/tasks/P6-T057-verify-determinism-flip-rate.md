---
id: P6-T057
kind: task
title: Determinism: flip rate on repeated inputs and CPU ONNX FP32 reproducibility
phase: 6
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T024]
requirements: [R6.11]
roadmap_todos: [T6.61]
modules: [M21]
dashboards: [D10]
tools: [git, uv, python>=3.12, docker, nvidia-smi]
mcp: []
env: []
services: [decision-svc, gpu]
branch: p6/P6-T057-verify-determinism-flip-rate
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T057 · Determinism: flip rate on repeated inputs and CPU ONNX FP32 reproducibility

## Goal / expected outcome

Measured flip rate (decisions that change on identical repeated inputs, incl. across restarts and batch positions) is ≤ the gate (default 0.1%) on GPU, and backtests using CPU ONNX FP32 reproduce bit-identically across runs.

## Context & references

- Roadmap: [R6.11](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.61
- Spec: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) determinism controls (SemIf saw 5–6/777 flips with prefix reuse in BF16) · [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models)
- Depends on (this phase): P6-T024
- Defaults: flip rate ≤ 0.1% ([16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets)); prefix caching off on the decision path ([17 §A](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) P4-B010)

## Requirements

- GPU: 10k states × 5 repeats, varying restart and neighbouring batch content; count argmax flips and probability deltas.
- CPU ONNX FP32: two full backtests over the same window produce identical decision hashes and identical P&L.
- Report flip rate per question/model in D10.

## ToDo

- [ ] Script `tools/verify/flip_rate.py`.
- [ ] Backtest reproducibility test in CI (small window) + full run once.
- [ ] Record results.

## Verification

### Tests
- CI reproducibility test (small window).

### Scenarios
- Given prefix caching accidentally enabled, then the flip-rate test fails (negative control).

### Stress / failure injection
- Repeat under GPU memory pressure (other model loaded): flip rate still ≤ gate or the question is flagged.

## Acceptance criteria

- [ ] Flip rate ≤ 0.1% (or the documented gate) per production-candidate model.
- [ ] Backtest hashes identical.

## Exceptions & edge cases

- Abstain/near-threshold flips reported separately.

## Cardinal rules (do NOT)

- Do NOT round probabilities to hide flips.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: measured flip rates.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.61 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T057-verify-determinism-flip-rate`
- PR title: `P6-T057: Determinism: flip rate on repeated inputs and CPU ONNX FP32 reproducibility`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T057` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (flip-rate default 16 §2.10, prefix caching off (17 §A); run fields)
