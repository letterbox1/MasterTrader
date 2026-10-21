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
depends_on: []
requirements: [R4.11]
roadmap_todos: [T4.27]
modules: [M6, M21]
dashboards: [D02]
branch: p4/P4-T042-vol-forecast-models
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T042 · Volatility and volume forecasts with Chronos, TimesFM and Kronos

## Goal / expected outcome

A nightly (and optional intraday hourly) batch produces realised-volatility and volume forecasts per instrument from pinned Chronos (Bolt small), TimesFM and Kronos checkpoints running locally on CPU/GPU, stored as versioned PIT features with model revision, for the IC evaluator and strategies.

## Context & references

- Roadmap: [R4.11](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.27](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Spec: [03 M6 forecast models](../../../docs/03-build-spec.md#m6-features--mt_features)
- Cross-phase: P1 bars (R1.02), P2 MLflow + feature framework (R2.44, R2.46).

## Requirements

- Inputs: daily and 1-h bars via `pit(as_of)`; horizons 1 d and 5 d (daily), 4 h (hourly).
- Targets: realised vol (Parkinson/close-to-close), log volume.
- Pinned checkpoints (revision hashes in `config/models/forecasters.yaml`); licences recorded in `third_party/LICENSES.md`.
- Baselines: EWMA vol and GARCH(1,1) for comparison; all logged to MLflow.
- Runtime budget: nightly run < 1 h for the universe on CPU.

## ToDo

- [ ] Forecast runner (Prefect flow) per model.
- [ ] Baselines + evaluation (QLIKE, MAE).
- [ ] Feature writer with model revision.
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
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Kronos availability/licence uncertain: if the licence is restrictive, drop it and document.

## Cardinal rules (do NOT)

- Do NOT read bars outside `pit(as_of)`.
- Do NOT auto-download unpinned model revisions.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
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
