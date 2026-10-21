---
id: P2-T101
kind: task
title: mt_lab job model, tables and backtest-worker queue
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.40, R2.44]
roadmap_todos: [T2.27]
modules: [M7]
dashboards: [D04]
branch: p2/P2-T101-lab-job-model-and-worker
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T101 · mt_lab job model, tables and backtest-worker queue

## Goal / expected outcome

`packages/mt_lab` exists with a durable job model: every backtest, sweep, validation and generator run is a row in `strategy.backtest` / `strategy.experiment`, is queued on NATS JetStream, executed by the `backtest-worker` container, reports progress on `lab.job.{id}` and can be cancelled. Everything else in the lab plugs into this.

## Context & references

- Roadmap: [R2.40, R2.44](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.27
- Spec: [03 M7](../../../docs/03-build-spec.md#m7-research-lab--mt_lab) · ownership [02 §4](../../../docs/02-v1-architecture.md#4-logical-components) (M7 owns `strategy.backtest`, `strategy.experiment`, publishes `lab.job.*`)
- Containers: [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) `backtest-worker` (`mt_lab`); the container itself, gVisor and resource limits come from T2.40 in part A (P2-T001–T099)
- Dashboard consumer: [D04 job queue](../../../docs/ui/dashboards/D04-research-lab.md)
- Cross-phase: P0 T0.22 (`mt_store` migrations, `pit`), T0.24 (`mt_api` command bus), T0.41 (NATS JetStream, MLflow)

## Requirements

- Alembic migration in `migrations/` for `strategy.backtest` (id, strategy_id, strategy_version, run_type, engine `screener|truth`, status, params JSON, data_range, as_of, cost_snapshot_id, seed, data_hash, code_sha, mlflow_run_id, metrics JSON, created_at, finished_at) and `strategy.experiment` (id, kind `sweep|validation|ab|generator|tier_a`, parent links, status).
- Job states `queued → running → succeeded | failed | cancelled | timed_out`; transitions published on `lab.job.{id}` (progress 0–100, ETA, message) via `mt_core.schemas` versioned msgspec payloads.
- Queue on a JetStream work-queue stream `LAB_JOBS`; at-least-once delivery with an idempotency key so a redelivered job never runs twice concurrently (lease + heartbeat on `sys.heartbeat.backtest-worker`).
- Resource caps per job from the D04 'Resources' field: max workers (default 2, ceiling = host cores − 4) and time cap (default 2 h); exceeded → `timed_out`.
- Cancel: `lab.job.cancel` stops the job within 5 s and marks it `cancelled`; partial artefacts kept and labelled incomplete.
- Worker is stateless; a worker restart re-queues `running` jobs whose lease expired (≤ 60 s).

## ToDo

- [ ] Create `packages/mt_lab/{__init__,jobs,models,worker}.py` and the Alembic migration for `strategy.backtest` + `strategy.experiment`
- [ ] Define msgspec payloads `LabJobRequest`, `LabJobProgress`, `LabJobResult` in `mt_core.schemas.lab` (versioned)
- [ ] Implement JetStream work queue `LAB_JOBS`, lease/heartbeat, redelivery guard and cancel signal (`lab.job.{id}.cancel`)
- [ ] Implement time cap and worker-count cap enforcement; publish progress at ≤ 1 Hz
- [ ] Expose a `JobRunner` plugin interface (`run(job, ctx) -> Result`) that later tasks (screener, truth, validation, sweep, generator, tier A) register into
- [ ] Add `backtest-worker` entrypoint (`python -m mt_lab.worker`) and its heartbeat
- [ ] Write unit + integration tests (see Verification)
- [ ] Document the job model in `docs/03-build-spec.md` M7 (job states, caps)

## Verification

### Tests
- Unit: state machine rejects illegal transitions; idempotency key dedupes a redelivered message; cap parsing.
- Integration (compose test profile with NATS + Postgres): enqueue a dummy runner job → progress events → `succeeded` row; cancel mid-run → `cancelled` within 5 s.

### Scenarios
- Given a running job, when the worker container is killed, then after the lease (≤ 60 s) another worker picks it up and the job finishes once (no duplicate result rows).
- Given a job exceeding its 2 h time cap, when the cap elapses, then it is `timed_out` and the D04 queue shows the reason.
- Given Postgres is down, when a job is submitted, then the command fails with problem+json and nothing is queued (no orphan job).

### Stress / failure injection
- Enqueue 200 dummy jobs with 4 workers: no lost or duplicated jobs; progress events stay ≤ 1 Hz per job.
- Kill NATS for 30 s mid-run: worker reconnects, job resumes or is re-queued, final state consistent.

## Acceptance criteria

- [ ] Migration applies and rolls back cleanly in CI
- [ ] Dummy job round-trip and cancel tests pass in CI
- [ ] Restart/redelivery test shows exactly one result row per job
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Clock: job timestamps are UTC from `mt_core.clock`; ETA is advisory only.
- Postgres down (02 §9.3): reject new jobs; running jobs buffer their result and retry the write, never drop it.
- A job referencing a strategy version deleted/archived later still keeps its rows (never cascade-delete results).

## Cardinal rules (do NOT)

- Do NOT run strategy code in the API process; jobs run only in `backtest-worker` (or `sandbox` for generated code).
- Do NOT allow a job to place orders or reach venue endpoints; lab jobs have no venue credentials.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file (07 §2).
- Do NOT read research/backtest data except through `mt_store.pit(as_of=…)`; the `pit` CI bypass test must stay green.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M7: job model and caps.
- `docs/02-v1-architecture.md` §6: `lab.job.{id}` payload/cancel subject.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.27 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T101-lab-job-model-and-worker`
- PR title: `P2-T101: mt_lab job model, tables and backtest-worker queue`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T101` run

## Progress log

- 2026-10-21 00:00 · planner · created
