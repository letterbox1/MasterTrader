---
id: P4-T042
kind: task
title: Volatility and volume forecasts with Chronos, TimesFM and Kronos
phase: 4
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T120, P2-T046, P1-T013, P1-T077]
requirements: [R4.11]
roadmap_todos: [T4.27]
modules: [M6, M21]
dashboards: [D02]
tools: [cargo, uv, git]
mcp: []
env: []
services: [supabase-postgres, mlflow, mt-scheduler]
branch: p4/P4-T042-vol-forecast-models
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-4-intel.md]
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

# P4-T042 · Volatility and volume forecasts with Chronos, TimesFM and Kronos

## Goal / expected outcome

A nightly (and optional intraday hourly) batch produces realised-volatility and volume forecasts per instrument from pinned Chronos (Bolt small), TimesFM and Kronos checkpoints running locally on CPU/GPU as `mt-scheduler` jobs (ONNX through `ort` in `mt-models` where a model exports cleanly, else the Python `mt_research` runner writing through the `mt_store` binding; (U) per model, [03 M6](../../../docs/03-build-spec.md#m6-features--mt_features), [18 §2.2](../../../docs/18-platform-and-deployment.md#22-python-uv-workspace-packages-only-where-absolutely-required); export parity in P4-T073), stored as versioned PIT features with model revision, for the IC evaluator and strategies.

## Context & references

- Roadmap: [R4.11](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.27](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Spec: [03 M6 forecast models](../../../docs/03-build-spec.md#m6-features--mt_features)
- Cross-phase (`depends_on`): P1-T013 (R1.02 bars), P2-T046 (R2.44 MLflow), P2-T120 (R2.46 feature framework), P1-T077 (`mt-scheduler`).

## Requirements

- Inputs: daily and 1-h bars via `pit(as_of)`; horizons 1 d and 5 d (daily), 4 h (hourly).
- Targets: realised vol (Parkinson/close-to-close), log volume.
- Pinned checkpoints (revision hashes in `config/models/forecasters.yaml`); licences recorded in `third_party/LICENSES.md`.
- Baselines: EWMA vol and GARCH(1,1) for comparison; all logged to MLflow.
- Runtime budget: nightly run < 1 h for the universe on CPU.

## ToDo

- [ ] Forecast runner per model as an `mt-scheduler` job: ONNX export script in `mt_research` and the `ort` runner in `mt-models` for models that export cleanly; the Python `mt_research` runner for the rest (offline batch only, never on the decision path).
- [ ] Baselines + evaluation (QLIKE, MAE) in `mt_research`, logged to MLflow.
- [ ] Feature writer with model revision (Rust `mt-features`).
- [ ] Tests.

## Verification

### Tests
- Unit: input windows end strictly before the forecast origin (no look-ahead).
- Integration: one instrument end-to-end → features + MLflow run.

### Scenarios
- Given a model checkpoint download fails, then that model is skipped and others run; alert.
- Given a new bar arrives late, then the forecast uses only data available at the origin.

### Stress / failure injection
- Full-universe nightly run timed; must stay < 1 h on CPU (record).

## Acceptance criteria

- [ ] Three models + two baselines produce features nightly; QLIKE comparison in MLflow
- [ ] CI green (`cargo test -p mt-models -p mt-features`, `cargo clippy`, ruff, mypy, `uv run pytest` (`mt_research`), `pit` bypass check)

## Exceptions & edge cases

- Kronos availability/licence uncertain: if the licence is restrictive, drop it and document.

## Cardinal rules (do NOT)

- Do NOT read bars outside `pit(as_of)`.
- Do NOT auto-download unpinned model revisions.
- Do NOT bypass `mt-api`, the risk manager (M11, `mt-risk`) or `pit(as_of)` (`mt-store`); every order goes through M11.
- Do NOT skip, weaken or delete a test to get green.
- Do NOT use unpinned images (`:latest`) or vendored code with telemetry/referral IDs; pin by digest.

## Doc sync on completion

- `docs/03-build-spec.md`: M6: forecasters used and their revisions
- `docs/roadmap/phase-4-intel.md`: tick T4.27 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T042-vol-forecast-models`
- PR title: `P4-T042: Volatility and volume forecasts with Chronos, TimesFM and Kronos`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T042` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (explicit cross-phase depends_on P1-T013, P2-T046, P2-T120)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (services postgres → supabase-postgres; CI commands per 18 (cargo/uv/supabase/pnpm))
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (Prefect flow → `mt-scheduler` jobs (depends_on +P1-T077; services prefect-server → mt-scheduler); ONNX/`ort` in `mt-models` where export works (U), else `mt_research`; parity in new P4-T073; tools +cargo)
