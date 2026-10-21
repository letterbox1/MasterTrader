---
id: P2-T127
kind: task
title: Tier A compile (ONNX/Treelite/lleaves) and MLflow registry
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T126]
requirements: [R2.47]
roadmap_todos: [T2.30]
modules: [M21]
dashboards: [D04]
branch: p2/P2-T127-tier-a-compile-and-registry
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

# P2-T127 · Tier A compile (ONNX/Treelite/lleaves) and MLflow registry

## Goal / expected outcome

Calibrated tier-A models are compiled to ONNX Runtime, Treelite or lleaves, verified numerically equal to the Python model, benchmarked, and registered in the MLflow model registry (and `models.registry`) with version, training range, calibration and benchmark latency.

## Context & references

- Roadmap: [R2.47](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.30
- [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) · [03 M21 model registry in MLflow](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models) · registry stages/artefact storage from T2.41 in part A (P2-T001–T099)
- [02 §4](../../../docs/02-v1-architecture.md#4-logical-components) M21 owns `models.registry`

## Requirements

- Compilers: lleaves (LightGBM → LLVM), Treelite (XGBoost/LightGBM), ONNX (linear/MLP and fallback); pick the fastest that passes parity.
- Parity: |compiled − python| ≤ 1e-6 on 10,000 holdout rows (probabilities after calibration).
- Benchmark: single-row in-process prediction latency histogram (p50/p99/p99.9) on the target host CPU; p99 must be < 50 µs to register as `promotable`.
- Register in MLflow (`tier_a/<strategy>`), stages None → Staging (promotion beyond Staging follows §8 gates); mirror row in `models.registry` (version, data range, feature versions, calibration metrics, latency).
- Artefacts pinned by hash; the engine loads by hash, not by 'latest'.

## ToDo

- [ ] Implement `mt_models/tier_a/compile.py` for the three back-ends
- [ ] Parity and latency benchmark harness (pytest-benchmark + hdrhistogram)
- [ ] Migration for `models.registry`; MLflow registration
- [ ] Tests + doc

## Verification

### Tests
- Integration: LightGBM fixture compiled via lleaves and Treelite; parity within 1e-6.
- Benchmark (CI perf job on the reference host or marked slow): p99 < 50 µs single-row.

### Scenarios
- Given a model whose compiled p99 is 80 µs, then it registers as `not_promotable: latency` and the D03 decision section cannot select it.
- Given compile fails for lleaves, then it falls back to Treelite/ONNX and records which back-end won.

### Stress / failure injection
- Benchmark under background load (4 busy cores) to record the degraded p99 alongside the idle p99.

## Acceptance criteria

- [ ] Compiled artefacts pass parity
- [ ] Latency recorded; p99 < 50 µs required for promotable
- [ ] Registered in MLflow + `models.registry`
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- CPU without AVX2: compile flags chosen at build time for the host; mismatch detected on load (P2-T128).

## Cardinal rules (do NOT)

- Do NOT load models by floating 'latest' tags in the engine.
- Do NOT add telemetry or referral IDs via vendored code; pin images by digest; record vendored code in `third_party/LICENSES.md`.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: chosen back-ends and measured latency.
- `docs/03-build-spec.md` M21: registry fields.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.30 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T127-tier-a-compile-and-registry`
- PR title: `P2-T127: Tier A compile (ONNX/Treelite/lleaves) and MLflow registry`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T127` run

## Progress log

- 2026-10-21 00:00 · planner · created
