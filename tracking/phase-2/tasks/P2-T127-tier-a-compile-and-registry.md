---
id: P2-T127
kind: task
title: Tier A ONNX export, ort parity and MLflow registry
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
tools: [uv, cargo]
mcp: []
env: []
services: [mlflow]
branch: p2/P2-T127-tier-a-compile-and-registry
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-T127 · Tier A ONNX export, ort parity and MLflow registry

## Goal / expected outcome

Calibrated tier-A models are exported to **ONNX** (the only runtime format: inference runs in Rust via `ort` in `mt-models`, [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates)), verified numerically equal to the Python model, benchmarked through `ort`, and registered in the MLflow model registry (and `models.registry`) with version, training range, calibration and benchmark latency.

## Context & references

- Roadmap: [R2.47](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.30
- [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) · [03 M21 model registry in MLflow](../../../docs/03-build-spec.md#m21-decision-one--model-serving) · registry stages/artefact storage from P2-T046 (T2.41)
- [02 §4](../../../docs/02-v1-architecture.md#4-logical-components) M21 owns `models.registry`

## Requirements

- Export: ONNX for every model type (LightGBM/XGBoost via onnxmltools/hummingbird-style converters, linear/MLP via the framework exporter), opset pinned; lleaves and Treelite are dropped because the runtime is Rust (`ort`), not Python.
- Parity: |ONNX (`ort`, Rust) − python| ≤ 1e-6 on 10,000 holdout rows (probabilities after calibration).
- Benchmark: single-row in-process prediction latency histogram (p50/p99/p99.9) through `mt-models`/`ort` on the workstation CPU (the runtime host until the P7 shift); p99 must be < 50 µs to register as `promotable`.
- Register in MLflow (`tier_a/<strategy>`), stages None → Staging (promotion beyond Staging follows §8 gates); mirror row in `models.registry` (version, data range, feature versions, calibration metrics, latency, ONNX opset).
- Artefacts pinned by hash; the engine loads by hash, not by 'latest'.

## ToDo

- [ ] Implement `packages/mt_research/tier_a/export.py` (ONNX export per model type, opset pinned)
- [ ] Parity and latency harness: Python side computes reference outputs; `cargo test -p mt-models onnx_parity` and `cargo bench -p mt-models tier_a` (criterion + hdrhistogram) run the `ort` side
- [ ] Migration for `models.registry`; MLflow registration
- [ ] Tests + doc

## Verification

### Tests
- Commands: `uv run pytest packages/mt_research -k export`, `cargo test -p mt-models onnx_parity`, `cargo bench -p mt-models tier_a`.
- Integration: LightGBM, XGBoost, linear and MLP fixtures exported to ONNX; `ort` parity within 1e-6 for each (the LightGBM parity case kept from the lleaves/Treelite plan, now against ONNX).
- Benchmark (perf job on the workstation or marked slow): p99 < 50 µs single-row.

### Scenarios
- Given a model whose ONNX p99 is 80 µs, then it registers as `not_promotable: latency` and the D03 decision section cannot select it.
- Given ONNX export fails for a model (unsupported op), then nothing is registered and the failing op is named (replaces the old lleaves → Treelite fallback case).

### Stress / failure injection
- Benchmark under background load (4 busy cores) to record the degraded p99 alongside the idle p99.

## Acceptance criteria

- [ ] Compiled artefacts pass parity
- [ ] Latency recorded; p99 < 50 µs required for promotable
- [ ] Registered in MLflow + `models.registry`
- [ ] CI green: `cargo clippy -- -D warnings`, `cargo test -p mt-models`, ruff, mypy, `uv run pytest packages/mt_research`, `pit` check

## Exceptions & edge cases

- CPU without AVX2: compile flags chosen at build time for the target CPU; mismatch detected on load (P2-T128).

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
- PR title: `P2-T127: Tier A ONNX export, ort parity and MLflow registry`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T127` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields; MLflow storage link)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (stays Python (uv); `pit` via the `mt_store` binding of `mt-store`; Supabase Postgres; commands line; host → workstation)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (compile → ONNX-only export (lleaves/Treelite dropped: inference is Rust `ort` in `mt-models`, 18 §2.1); export in `mt_research`, parity + benchmark on the `ort` side under `cargo`; LightGBM parity case kept against ONNX; fallback case replaced by an export-failure case; tools [uv] → [uv, cargo])
