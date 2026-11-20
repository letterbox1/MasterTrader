---
id: P2-T205
kind: task
title: ONNX port path for Python research strategies with Rust parity check
phase: 2
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T203, P2-T127, P2-T128, P2-T008]
requirements: [R2.60, R2.47]
roadmap_todos: [T2.45]
modules: [M0, M7, M21, mt_research, mt-models]
dashboards: []
tools: [git, cargo, uv]
mcp: []
env: []
services: [mlflow]
branch: p2/P2-T205-onnx-port-path-for-python-research-strategies-wi
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-20
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-T205 · ONNX port path for Python research strategies with Rust parity check

## Goal / expected outcome

A Python ML research strategy can leave paper only by being ported: its model is exported to ONNX from `mt_research`, its rules are rewritten as a Rust strategy that runs the model in-process through `mt-models` (`ort`), and a parity check proves the Rust port produces the same signals and orders as the Python original on recorded data before the Rust version may be promoted ([18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates), [03 M0](../../../docs/03-build-spec.md#m0-strategy-framework-strategy-agnostic-any-timeframe)).

## Context & references

- Roadmap: [R2.60, R2.47](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.45 · verified alongside P2-T206
- Built on: P2-T203 (`mt_research` + binding), P2-T127 (ONNX export + registry), P2-T128 (in-process `ort` runtime), P2-T008 (Rust template structure)
- Lifecycle: P2-T007 caps `lang=python` strategies at `paper`; the Rust port is a new strategy version that goes through the normal gates

## Requirements

- `mt_research.port.export(strategy)`: exports every model the strategy uses to ONNX (opset pinned), registers it in MLflow with input/output schema, and writes a port manifest (features used, thresholds, rules as text).
- `cargo generate`-style scaffold for the Rust port in `strategies/<name>/` using `ModelSignalProvider` (P2-T009) and `mt-features`.
- Parity check: replay the same recorded week through the Python strategy (paper node) and the Rust port (backtest): model outputs within 1e-6 absolute; signals and order intents identical; any difference fails with the first diverging timestamp.
- The Rust port records `ported_from=<python strategy version>` and its parity report; promotion beyond `paper` requires a passed parity report.

## ToDo

- [ ] Implement `mt_research.port.export` and the port manifest
- [ ] Rust port scaffold + example (port the Python research example from P2-T003)
- [ ] Parity runner (`cargo test -p mt-models port_parity` + the Python side via the binding) and report storage
- [ ] Lifecycle hook: parity report required for `lang=rust, ported_from≠null` promotions
- [ ] Write tests (see Verification)
- [ ] Update docs listed under Doc sync

## Verification

### Tests
- Commands: `uv run pytest packages/mt_research -k port`, `cargo test -p mt-models port_parity`, `cargo clippy`.
- Unit: ONNX export round-trip (Python model vs `ort` output within 1e-6) for GBDT, linear and MLP fixtures.
- Integration: the example port passes parity; a deliberately changed threshold in the Rust port fails with the first diverging timestamp.

### Scenarios
- Given a Python research strategy, when you try to switch its bot to `hitl`, then it is refused with "port to Rust first" (P2-T007 ceiling).
- Given a Rust port without a parity report, when promotion is requested, then the gate evaluator refuses it.

### Stress / failure injection
- A model op not supported by the pinned ONNX opset: export fails with the op name; nothing is registered.

## Acceptance criteria

- [ ] Export, scaffold and parity check work end to end on the example strategy
- [ ] Promotion of a port requires a passed parity report
- [ ] CI green: `cargo clippy -- -D warnings`, `cargo test`, ruff, mypy, `uv run pytest packages/mt_research`

## Exceptions & edge cases

- Models that don't export cleanly to ONNX (U for some forecast models, 03 M6) can't be ported; the strategy stays paper-only research.

## Cardinal rules (do NOT)

- Do NOT let a Python strategy run outside `paper`; do NOT run Python on the live decision path (18 §2.2).
- Do NOT promote a port whose parity report failed or is missing.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M0/M21: the port path and parity rule.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.45 when this and P2-T203 are done.

## Branch & PR

- Branch: `p2/P2-T205-onnx-port-path-for-python-research-strategies-wi`
- PR title: `P2-T205: ONNX port path for Python research strategies with Rust parity check`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T205` run

## Progress log

- 2026-11-20 00:00 · aligner · created: Rust-max per 17 §H (R2.60: Python research strategies are ported to Rust (ONNX via `ort`) before live; no task built the port path or its parity check)
