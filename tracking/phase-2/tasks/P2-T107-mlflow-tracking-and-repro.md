---
id: P2-T107
kind: task
title: MLflow experiment tracking and reproducible re-runs
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T101, P2-T106, P2-T046]
requirements: [R2.44]
roadmap_todos: [T2.27]
modules: [M7]
dashboards: [D04]
tools: [uv]
mcp: []
env: []
services: [mlflow, postgres]
branch: p2/P2-T107-mlflow-tracking-and-repro
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T107 · MLflow experiment tracking and reproducible re-runs

## Goal / expected outcome

Every lab run (screener, truth, validation, sweep trial, generator, tier-A training) is an MLflow run with code version, parameters, data range, cost snapshot, seed and results, and the D04 'Reproduce → Re-run' button reproduces it bit-for-bit.

## Context & references

- Roadmap: [R2.44](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.27
- Spec: [03 M7 optimisation/MLflow](../../../docs/03-build-spec.md#m7-research-lab--mt_lab) · [D04 Reproduce tab + acceptance 4](../../../docs/ui/dashboards/D04-research-lab.md)
- MLflow server from P0 (P0-T020, T0.41); artefact storage + registry stages from P2-T046 (T2.41)

## Requirements

- Logged per run: git SHA (dirty tree refused), manifest hash, strategy id/version, params, data range, `as_of`, data_hash + snapshot ids, cost_snapshot_id, seed, engine + Nautilus version, metrics, artefacts (equity, trades, report).
- MLflow experiment per strategy; run name `<strategy>@<version>/<run_type>/<id>`; tags `engine`, `gate_eligible`, `trial_no`.
- `lab.backtest.run` with `rerun_of=<id>` reuses all recorded inputs; result compared by trade-list hash and flagged `reproduced=true|false`.
- MLflow outage must not lose results: buffer to the backtest row and sync later.

## ToDo

- [ ] Implement `mt_lab/tracking.py` (MLflow client wrapper, buffering, tags)
- [ ] Hook all `JobRunner`s through a common `tracked_run` context manager
- [ ] Implement re-run path and reproduction comparison
- [ ] Tests incl. MLflow-down buffering
- [ ] Docs

## Verification

### Tests
- Integration: a truth run appears in MLflow with every required field.
- Integration: re-run of a fixture backtest → identical trade hash, `reproduced=true`.
- Unit: dirty git tree → job refused with a clear message.

### Scenarios
- Given MLflow is down, when a backtest finishes, then the result is stored in Postgres with `mlflow_sync=pending` and synced after MLflow returns.
- Given a re-run on a newer engine version, then `reproduced=false` with the version diff shown.

### Stress / failure injection
- 1,000 sweep trials logging concurrently: MLflow logging batched; no dropped runs.

## Acceptance criteria

- [ ] Required fields present on every run type
- [ ] Re-run reproduces fixture results
- [ ] MLflow-down buffering test passes
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Large artefacts (tick trade lists) stored as Parquet in the artefact store, not as MLflow params.
- Secrets never logged: params are filtered against a deny-list (api keys, tokens).

## Cardinal rules (do NOT)

- Do NOT log secrets or full environment variables to MLflow.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M7: tracked fields list.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.27 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T107-mlflow-tracking-and-repro`
- PR title: `P2-T107: MLflow experiment tracking and reproducible re-runs`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T107` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (MLflow storage dep (P2-T046))
