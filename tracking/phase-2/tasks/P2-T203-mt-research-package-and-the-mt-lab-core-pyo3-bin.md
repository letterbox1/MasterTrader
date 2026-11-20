---
id: P2-T203
kind: task
title: mt_research package and the mt-lab-core PyO3 binding
phase: 2
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T101, P2-T102, P2-T103, P0-T071, P2-T202]
requirements: [R2.60, R2.44]
roadmap_todos: [T2.45]
modules: [M7, mt_research, mt-lab-core]
dashboards: [D04]
tools: [git, cargo, uv, maturin]
mcp: []
env: []
services: [supabase-postgres, mlflow, mt-scheduler]
branch: p2/P2-T203-mt-research-package-and-the-mt-lab-core-pyo3-bin
pr: ""
doc_sync: [docs/03-build-spec.md, docs/18-platform-and-deployment.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T203 · mt_research package and the mt-lab-core PyO3 binding

## Goal / expected outcome

The Python research side exists and calls the **same** production harness as Rust: `packages/mt_research` (uv workspace member) holds notebooks, the screener, Optuna sweeps, tier-A training and the Python research strategy base, and a PyO3 binding (`mt_lab_core` module, built with maturin) exposes the `mt-lab-core` datasets, cost models, truth runner, metrics, validation sections, trial counter, setup odds and the Rust templates' batch `signals()` to it. Research reads data only through `pit` ([18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates), [18 §2.2](../../../docs/18-platform-and-deployment.md#22-python-uv-workspace-packages-only-where-absolutely-required), [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20)).

## Context & references

- Roadmap: [R2.60, R2.44](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.45 · verified by P2-T206 (T2.74)
- Spec: [03 M7](../../../docs/03-build-spec.md#m7-research-lab) (lab split) · [03 M0](../../../docs/03-build-spec.md#m0-strategy-framework-strategy-agnostic-any-timeframe) (Python strategies only for ML research on paper)
- Built on: `mt-lab-core` job model, costs and datasets (P2-T101, P2-T102, P2-T103; later sections such as metrics, P2-T106, are added to the binding as they land); the `mt_store` PyO3 module with `mt-core` types and `pit` (P0-T071); the `mt-risk` binding (P2-T202).
- Used by: P2-T003 (Python research base lives here), P2-T104 (screener), P2-T105 (Python truth path), P2-T107/P2-T108 (tracking, trials), P2-T109 (per-fold Optuna), P2-T112 (analysers on Python fixtures), P2-T115 (sweeps), P2-T125–T127 (tier A), P2-T205 (ONNX port path).
- Third-party: [19 §2](../../../docs/19-third-party-register.md#2-python-libraries-we-keep-only-where-absolutely-required-18-22) (PyTorch, LightGBM, scikit-learn, Optuna, Qlib, vectorbt ⚑).

## Requirements

- `packages/mt_research`: subpackages `strategy` (research base, P2-T003), `screener` (P2-T104), `optimise` (P2-T115), `tier_a` (P2-T125–T127), `tracking` (P2-T107), `notebooks/`; job entrypoints runnable as `mt-scheduler` job containers (P2-T101 `ExternalJobRunner`).
- Binding `mt_lab_core` (PyO3 abi3, maturin, `crates/mt-lab-core` `python` feature): `Dataset`/`DatasetSpec`, `CostModel` (incl. `scaled(k)`), `truth.run`, `metrics`, validation sections (folds, stats, breakdown, bias analysers), `trials.register`, `odds.run`, `templates.signals(name, bars, params)`; Arrow (`pyo3-arrow`) for bulk arrays; the lab job schemas from `mt-core` are exposed through `mt_store`.
- No logic duplicated in Python: every function the binding exposes is the Rust implementation; Python adds only exploration, training and orchestration.
- Data only through `pit`: the package has no database driver of its own; an import-linter contract forbids `psycopg`/`sqlalchemy`/raw SQL in `mt_research`.
- Python research strategies: paper only; the binding refuses to start a Python strategy on a node whose mode is not `paper`; each carries `lang=python` in the registry.
- Type stubs (`mt_lab_core.pyi`) checked by mypy `--strict`; the hot calls release the GIL.
- Errors cross the boundary as typed Python exceptions; a Rust panic in a validation section marks that section `failed`, never `passed`.

## ToDo

- [ ] Create `packages/mt_research` (uv workspace member) with the subpackage layout above and job entrypoints
- [ ] Add the `python` feature to `crates/mt-lab-core` with PyO3 wrappers; maturin config; uv workspace wiring
- [ ] Expose the Rust templates' batch `signals()` through the binding
- [ ] Import-linter contracts (no DB drivers; only `mt_research.strategy.base` may call Nautilus `submit_order`)
- [ ] Type stubs + mypy check
- [ ] Example notebook: dataset → screener → truth → validation report, all through the binding
- [ ] Write tests (see Verification)
- [ ] Update docs listed under Doc sync

## Verification

### Tests
- Commands: `cargo test -p mt-lab-core`, `cargo clippy -p mt-lab-core`, `uv run pytest packages/mt_research`, mypy on the stubs.
- Unit: each exposed function round-trips its inputs and returns the same values as the Rust call on a fixture (smoke; the full parity matrix is P2-T206).
- Unit: a panic in a validation section surfaces as `failed`.
- Static: the import-linter contracts fail CI when violated.

### Scenarios
- Given a notebook, when it builds a dataset with an `as_of`, then rows ingested after `as_of` are excluded exactly as in the Rust run.
- Given a Python research strategy, when someone tries to run it on a `hitl` node, then the binding refuses to start it.

### Stress / failure injection
- Pass a 10M-row dataset through the binding with Arrow: no copy beyond one buffer, RSS < 4 GB, GIL released during the run.
- Kill the `mt_research` job container mid-sweep: the scheduler re-queues it (P2-T101) and finished trials are not lost.

## Acceptance criteria

- [ ] `mt_research` installs from the uv workspace and its job entrypoints run under `mt-scheduler`
- [ ] Every listed harness function is reachable from Python through the binding with no Python reimplementation
- [ ] Data access only through `pit` (contract enforced)
- [ ] CI green: `cargo clippy -- -D warnings`, `cargo test -p mt-lab-core`, ruff, mypy, `uv run pytest packages/mt_research`, `pit` check

## Exceptions & edge cases

- A harness feature not yet built in Rust is simply absent from the binding (no Python stand-in).
- vectorbt is research-only ⚑ (Commons Clause): it stays an optional extra of `mt_research`, never a runtime dependency.

## Cardinal rules (do NOT)

- Do NOT reimplement any harness, validation, gate or risk logic in Python.
- Do NOT read data except through `pit(as_of)`; do NOT let Python place orders, sign, or sit on the live decision path (18 §2.2).
- Do NOT put Telegram text (or any `train_ok = false` row) into a model, RAG index or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/logs (07 §2).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M7 and `docs/18-platform-and-deployment.md` §2.2: binding module name and what it exposes.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.45 when this is done.

## Branch & PR

- Branch: `p2/P2-T203-mt-research-package-and-the-mt-lab-core-pyo3-bin`
- PR title: `P2-T203: mt_research package and the mt-lab-core PyO3 binding`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T203` run

## Progress log

- 2026-11-20 00:00 · aligner · created: Rust-max per 17 §H (T2.45/R2.60: no task built the Python research package or the lab binding)
