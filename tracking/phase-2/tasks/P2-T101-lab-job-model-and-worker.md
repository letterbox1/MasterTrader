---
id: P2-T101
kind: task
title: mt-lab-core crate, lab job model, tables and backtest-worker queue
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T024, P0-T027, P0-T020, P1-T077]
requirements: [R2.40, R2.44, R2.60]
roadmap_todos: [T2.27]
modules: [M7]
dashboards: [D04]
tools: [cargo, docker, supabase]
mcp: []
env: []
services: [nats, supabase-postgres, mt-scheduler]
branch: p2/P2-T101-lab-job-model-and-worker
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T101 · mt-lab-core crate, lab job model, tables and backtest-worker queue

## Goal / expected outcome

The `crates/mt-lab-core` crate (Rust, the production side of M7, [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates), [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20)) exists with a durable job model: every backtest, sweep, validation and generator run is a row in `strategy.backtest` / `strategy.experiment`, is queued as an `mt-scheduler` job on the `lab` queue, executed by the `backtest-worker` container (Rust runners in-process; `mt_research` Python jobs as separate job containers), reports progress on `lab.job.{id}` and can be cancelled. Everything else in the lab plugs into this.

## Context & references

- Roadmap: [R2.40, R2.44, R2.60](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.27
- Spec: [03 M7](../../../docs/03-build-spec.md#m7-research-lab--mt_lab) · ownership [02 §4](../../../docs/02-v1-architecture.md#4-logical-components) (M7 owns `strategy.backtest`, `strategy.experiment`, publishes `lab.job.*`)
- Containers: [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) `backtest-worker`; the container itself, gVisor and resource limits come from T2.40 in part A (P2-T044)
- Dashboard consumer: [D04 job queue](../../../docs/ui/dashboards/D04-research-lab.md)
- Cross-phase (`depends_on`): Supabase migrations baseline (P0-T024) and `pit(as_of)` (P0-T027, T0.22); compose stack with NATS JetStream + MLflow (P0-T020, T0.41); `mt-scheduler` skeleton (P1-T077: Postgres-backed queue, leases, retries, run history). The `mt-api` command bus (P0-T034, Rust) is used by P2-T117. The Python side (`mt_research` job kinds and the binding) is P2-T203.
- Defaults: job caps (2 workers, 2 h) are D04 settings with documented defaults, not constants.

## Requirements

- SQL migration in `supabase/migrations/` for `strategy.backtest` (id, strategy_id, strategy_version, run_type, engine `screener|truth`, lang `rust|python`, status, params JSON, data_range, as_of, cost_snapshot_id, seed, data_hash, code_sha, mlflow_run_id, metrics JSON, created_at, finished_at) and `strategy.experiment` (id, kind `sweep|validation|ab|generator|tier_a`, parent links, status).
- Job states `queued → running → succeeded | failed | cancelled | timed_out`; transitions published on `lab.job.{id}` (progress 0–100, ETA, message) via versioned `mt-core` message schemas (serde; exposed to Python through the `mt_store` module by P2-T203).
- Queue: `mt-scheduler` jobs of kind `lab.*` on queue `lab` (Postgres-backed); at-least-once delivery with an idempotency key so a redelivered job never runs twice concurrently (scheduler lease + heartbeat on `sys.heartbeat.backtest-worker`). Python job kinds (screener, Optuna sweeps, tier-A training) are launched by the worker as `mt_research` job containers with the same lease and cancel contract.
- Resource caps per job from the D04 'Resources' field: max workers (default 2, ceiling = workstation cores − 4) and time cap (default 2 h); exceeded → `timed_out`.
- Cancel: `lab.job.cancel` stops the job within 5 s and marks it `cancelled`; partial artefacts kept and labelled incomplete.
- Worker is stateless; a worker restart re-queues `running` jobs whose lease expired (≤ 60 s).

## ToDo

- [ ] Create the `crates/mt-lab-core` crate (`jobs`, `models`, `worker` modules) and the SQL migration in `supabase/migrations/` for `strategy.backtest` + `strategy.experiment` (pgTAP test)
- [ ] Define payloads `LabJobRequest`, `LabJobProgress`, `LabJobResult` in `crates/mt-core/src/schemas/lab.rs` (versioned)
- [ ] Register the `lab` queue and `lab.*` job kinds with `mt-scheduler` (P1-T077); lease/heartbeat, redelivery guard and cancel signal (`lab.job.{id}.cancel` on NATS)
- [ ] Implement time cap and worker-count cap enforcement; publish progress at ≤ 1 Hz
- [ ] Expose a `JobRunner` trait (`run(job, ctx) -> Result`) that later tasks (truth, validation, generator) register into, plus an `ExternalJobRunner` that launches `mt_research` job containers (screener, sweeps, tier A) and relays their progress
- [ ] Add the `backtest-worker` entrypoint (the `mt-lab-core worker` binary) and its heartbeat
- [ ] Write unit + integration tests (see Verification)
- [ ] Document the job model in `docs/03-build-spec.md` M7 (job states, caps)

## Verification

### Tests
- Commands: `cargo test -p mt-lab-core jobs`, `cargo clippy -p mt-lab-core`, `supabase test db`.
- Unit: state machine rejects illegal transitions; idempotency key dedupes a redelivered job; cap parsing.
- Integration (compose test profile with NATS + the Supabase CLI stack + `mt-scheduler`): enqueue a dummy runner job → progress events → `succeeded` row; cancel mid-run → `cancelled` within 5 s; a dummy external (Python) job behaves the same.

### Scenarios
- Given a running job, when the worker container is killed, then after the lease (≤ 60 s) another worker picks it up and the job finishes once (no duplicate result rows).
- Given a job exceeding its 2 h time cap, when the cap elapses, then it is `timed_out` and the D04 queue shows the reason.
- Given Postgres is down, when a job is submitted, then the command fails with problem+json and nothing is queued (no orphan job).

### Stress / failure injection
- Enqueue 200 dummy jobs with 4 workers: no lost or duplicated jobs; progress events stay ≤ 1 Hz per job.
- Kill NATS for 30 s mid-run: the worker reconnects, progress resumes (the queue itself is in Postgres), job finishes or is re-queued, final state consistent.

## Acceptance criteria

- [ ] Migration applies and rolls back cleanly in CI
- [ ] Dummy job round-trip and cancel tests pass in CI (Rust runner and external Python runner)
- [ ] Restart/redelivery test shows exactly one result row per job
- [ ] CI green: `cargo clippy -- -D warnings`, `cargo test -p mt-lab-core`, `supabase test db`, `pit` check

## Exceptions & edge cases

- Clock: job timestamps are UTC from the `mt-core` clock; ETA is advisory only.
- Postgres down (02 §9.3): reject new jobs; running jobs buffer their result and retry the write, never drop it.
- A job referencing a strategy version deleted/archived later still keeps its rows (never cascade-delete results).

## Cardinal rules (do NOT)

- Do NOT run strategy code in the API process; jobs run only in `backtest-worker` (or `sandbox` for generated code).
- Do NOT allow a job to place orders or reach venue endpoints; lab jobs have no venue credentials.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file (07 §2).
- Do NOT read research/backtest data except through `pit(as_of)` (the `mt-store` crate; `mt_research` uses its `mt_store` binding); the `pit` CI bypass test must stay green.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M7: job model and caps.
- `docs/02-v1-architecture.md` §6: `lab.job.{id}` payload/cancel subject.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.27 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T101-lab-job-model-and-worker`
- PR title: `P2-T101: mt-lab-core crate, lab job model, tables and backtest-worker queue`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T101` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (cross-phase deps (migrations, pit, NATS); caps as settings)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (stays Python (uv); `pit` via the `mt_store` binding of `mt-store`; Supabase Postgres; commands line; Alembic → `supabase/migrations`; msgspec → `mt-core` schemas; dep P0-T071; depends_on + P0-T071; tools [uv, docker] → [uv, docker, supabase]; services [nats, postgres] → [nats, supabase-postgres])
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (`packages/mt_lab` → `crates/mt-lab-core` (Rust crate skeleton + job model); JetStream work queue → `mt-scheduler` `lab` queue (Postgres-backed; NATS keeps progress/cancel); Python job kinds run as `mt_research` containers; depends_on + P1-T077, − P0-T071 (Python exposure moves to P2-T203); same test cases under `cargo test`; tools [uv, docker, supabase] → [cargo, docker, supabase]; services + mt-scheduler)
