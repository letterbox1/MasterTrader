---
id: P1-T077
kind: task
title: mt-scheduler skeleton: Postgres-backed jobs, cron, retries, run history
phase: 1
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T004, P0-T024, P0-T018, P0-T034, P0-T051]
requirements: [R1.18]
roadmap_todos: [T1.35]
modules: [mt-scheduler, M16, M17]
dashboards: [D16, D07]
tools: [git, cargo, supabase, docker, pnpm, uv]
mcp: []
env: []
services: [supabase-postgres, nats]
branch: p1/P1-T077-mt-scheduler-skeleton-postgres-backed-jobs-cron-
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/18-platform-and-deployment.md, docs/02-v1-architecture.md, docs/16-configuration-and-safety-model.md, docs/ui/dashboards/D16-system.md]
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

# P1-T077 · mt-scheduler skeleton: Postgres-backed jobs, cron, retries, run history

## Goal / expected outcome

`mt-scheduler` (Rust, `crates/mt-scheduler`) replaces Prefect: a Postgres-backed job queue with timezone-aware cron, retries, resumable backfill runs and run history in Supabase Postgres, with job status on D16 (Jobs) and an API that D07 reads. It runs Rust jobs in-process (in queue workers) and Python `mt_research` jobs as subprocesses in a research worker. The P0 jobs (Merkle seal, monthly WORM export, restore test) move onto it, so the platform has one scheduler. Every batch job in Phase 1 and later phases (connectors, backfills, rollups, retention, nightly DQ reports, training runs, the scenario twin) runs on it.

## Context & references

- Roadmap: requirement [R1.18](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.35](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets); verified by [T1.68](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets) in P1-T079
- Platform: [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-scheduler`: Postgres-backed job queue and cron (`apalis`-style), retries, backfills, run history in Postgres, job status on D16/D07; Rust jobs in-process, Python training jobs as containers/subprocesses) · [18 §2.2](../../../docs/18-platform-and-deployment.md#22-python-uv-workspace-packages-only-where-absolutely-required) (`mt_research` runs as `mt-scheduler` jobs and reads only through `pit`)
- Decision: [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20) (Prefect → `mt-scheduler`)
- Architecture: [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) (`scheduler` container) · [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) (`alert.*`, `sys.heartbeat.*`)
- UI: [D16 System](../../../docs/ui/dashboards/D16-system.md) Jobs widget (`/system/jobs`, WS `system`) and "Re-run a failed job" (`system.job.run`, C1); [D07](../../../docs/ui/dashboards/D07-data-quality.md) Feeds shows batch sources' last run
- Cross-phase prerequisites (depends_on): P0-T024 (Supabase migrations baseline, `ops` schema, roles), P0-T018 (`mt-obs` metrics, logs, heartbeats), P0-T034 (`mt-api` command bus with `audit.command`), P0-T051 (D16 page the Jobs widget sits on)
- Depends on (this phase): P1-T004 (Compose services and NATS streams, incl. `ALERT`)
- Used by: P1-T053 (every P1 schedule and the `ingest-batch` worker), P1-T079 (scheduler VERIFY), the P0 jobs (P0-T037 seal, P0-T040 WORM export, P0-T041 restore test), and later phases' batch jobs

## Requirements

- **Crate and binaries:** `crates/mt-scheduler` (lib + binary). `mt-scheduler serve` runs the cron loop and the queue; `mt-scheduler worker --queue <name>` runs jobs. The library exposes `Worker::new(queue).register(kind, handler)` so other binaries (e.g. `mt-connectors` in P1-T053) become workers of a queue without depending on each other
- **Job definitions** in `config/jobs.yaml`, synced to `ops.job` on start (validated with serde; unknown keys rejected): `id`, `kind` (`rust` = a handler registered in a worker, `command` = a Rust binary subcommand such as `mt-obs seal`, `python` = `python -m mt_research.jobs.<name>`), `queue`, `cron` + `timezone` (IANA, e.g. `Australia/Sydney`, `America/New_York`), `params`, `retry` (max attempts, backoff), `timeout`, `concurrency_key`, `source` (link to `config/sources.yaml`, for quota and D07), `enabled`. Defaults are settings, never constants: retries 3 with exponential backoff 30 s → 10 min plus jitter, timeout 1 h, concurrency 1 per key, misfire grace 1 h, lease 60 s (all in `config/jobs.yaml` `defaults:`; added to 16 §2.15 on doc sync)
- **Queue in Postgres** (Supabase migrations): `ops.job` (definitions), `ops.job_run` (one row per attempt: run id, job id, attempt, trigger `cron|manual|backfill|retry`, scheduled_for, started_at, finished_at, status `queued|running|succeeded|failed|retrying|deferred|skipped|cancelled`, error summary, output summary JSON, checkpoint JSON, trace_id, worker id, lease_until). Workers claim with `SELECT … FOR UPDATE SKIP LOCKED`; a running attempt renews its lease; an expired lease (worker or scheduler crash) re-queues the run from its last checkpoint
- **Cron:** timezone-aware next-run calculation (`cron` + `chrono-tz`); in a DST gap the run happens once at the next valid time, in a repeated hour it runs once; missed runs after downtime run once if inside the misfire grace (coalesced), older ones are recorded `skipped`
- **Retries:** per-job policy; `Retry-After`-style deferrals (`deferred` with a not-before time, e.g. quota exhausted) don't count as failures; after the last attempt the run is `failed` and `alert.warning.job_failed` (job, error, attempts, run link) goes to the one alert fan-out on NATS
- **Backfill runs:** a job run over a range (`--from/--to`) is split into chunks (per day by default) with a checkpoint after each chunk, so a restart resumes at the next unfinished chunk; progress is visible per run (`/lab/jobs?kind=backfill` and D16)
- **Pre-run hook** interface (`PreRun`): a job can be deferred before it starts (P1-T053 plugs in the quota tracker from P1-T006 and source-publication checks)
- **Python jobs:** kind `python` runs as a subprocess in the `research-worker` (image with the `mt_research` uv environment, `mt-scheduler worker --queue research`); run id and params are passed as env/JSON on stdin; exit code decides the result; stdout/stderr tail (secret-scrubbed) goes to the run row; the timeout kills the process group. Python jobs read only through the `pit` binding and write through the `mt_store` binding (18 §2.2)
- **API and UI:** `mt-api` read `/api/v1/system/jobs` (+ `/system/jobs/{id}/runs`) and command `system.job.run` (C1, audited in `audit.command`; re-runs a failed job or starts a backfill range); WS `system` pushes run status changes; D16 Jobs widget per [D16](../../../docs/ui/dashboards/D16-system.md) (last run, result, duration, next run, retries, link to run history; "Re-run" button)
- **Observability:** `sys.heartbeat.scheduler` every 1 s, `/healthz`, Prometheus `mt_job_runs_total{job,status}`, `mt_job_duration_seconds{job}`, `mt_job_last_success_timestamp{job}`, `mt_job_queue_depth{queue}`; structured logs with `trace_id` per run
- **Compose:** `scheduler` and `research-worker` services in the workstation compose file (digest-pinned images built from the Cargo workspace / `mt_research`), on the `core` network, no venue or data API keys (data keys belong to the `ingest-batch` worker added in P1-T053)
- **Move the P0 jobs:** register `mt-obs seal` (daily 00:15 UTC), `mt-obs export` (monthly, 1st), the restore test (monthly) and any other P0 job that a temporary scheduler runs (Prefect deployment, pg_cron entry calling out, or systemd timer) as `command` jobs, and remove the old schedule in the same PR so each job has exactly one scheduler; then remove the Prefect services and the `prefect` database from compose if P0 created them. A P0 job not built yet is registered `enabled: false` and its own task enables it
- Run history is operational data in `ops.*` (status changes allowed); manual runs are audited through `audit.command`, which stays WORM

## ToDo

- [ ] Supabase migration for `ops.job` and `ops.job_run` (indexes for claim and history queries) with pgTAP tests (`supabase test db`)
- [ ] Implement `crates/mt-scheduler`: config loader + sync, cron engine with timezones and misfire handling, queue claim/lease/heartbeat, retry and deferral policy, backfill chunking with checkpoints, `PreRun` hook, `Worker` library API
- [ ] Implement the `command` and `python` job kinds (process group, timeout, secret-scrubbed output tail)
- [ ] Add `mt-api` `/system/jobs`, `/system/jobs/{id}/runs` and `system.job.run` (C1), and WS `system` run events
- [ ] Add the D16 Jobs widget in `apps/web` (Vitest + Playwright viewport matrix)
- [ ] Add `scheduler` and `research-worker` to the workstation compose file with health checks, heartbeats and metrics; Grafana panel for job failures
- [ ] Register the P0 jobs (seal, WORM export, restore test) and remove their previous schedules and, once unused, the Prefect services and `prefect` database
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- `cargo test -p mt-scheduler cron`: next-run times across DST in Australia/Sydney (first Sunday of April and October) and America/New_York (March and November); gap hour runs once, repeated hour runs once; misfire inside grace coalesces to one run, outside grace is `skipped`
- `cargo test -p mt-scheduler queue` (against `supabase start`): two workers never claim the same run (`SKIP LOCKED`); an expired lease re-queues the run; retry backoff follows the policy; a deferral is not counted as an attempt
- `cargo test -p mt-scheduler backfill`: a 30-day backfill is chunked per day, checkpoints after each chunk and resumes at the first unfinished chunk after a kill
- `cargo test -p mt-scheduler python_job` (needs `uv`): a stub `mt_research.jobs.echo` job succeeds; a non-zero exit fails; a timeout kills the process group; a secret-looking string in its output is scrubbed in the run row
- `cargo test -p mt-api system_jobs`: `/system/jobs` lists jobs with last/next run; `system.job.run` is C1, audited, and refuses an unknown job
- `supabase test db`: `ops.job_run` constraints (status enum, one running attempt per run); the app role can't touch `audit.*` from the scheduler
- `pnpm test` and `pnpm playwright`: D16 Jobs widget renders loading/empty/error states and the run list across the viewport matrix
- `cargo clippy --all-targets -- -D warnings`

### Scenarios

- Given a job whose handler fails twice and then succeeds, when it runs, then `ops.job_run` holds three attempts (`retrying`, `retrying`, `succeeded`) and no alert fires
- Given a job that fails on every attempt, when the last attempt fails, then `alert.warning.job_failed` reaches the alert fan-out and D16 shows the job red with a "Re-run" button
- Given the scheduler is stopped for 3 hours across a daily 01:00 job, when it restarts, then the missed run is `skipped` (outside the 1 h grace) and the next run is scheduled normally
- Given you press "Re-run" on a failed job in D16, when the command runs, then a `manual` run starts and `audit.command` records it

### Stress / failure injection

- Kill `mt-scheduler serve` and a worker mid-backfill (`docker kill`); after restart the run resumes from its checkpoint and no chunk is written twice
- Restart Supabase Postgres while 20 runs are queued; the scheduler reconnects with backoff and every run completes exactly once
- Load: 500 queued `rust` no-op jobs across 4 workers drain with no double claim; claim latency p99 < 50 ms on the workstation (recorded in the PR)

## Acceptance criteria

- [ ] `mt-scheduler` runs `rust`, `command` and `python` jobs with cron, retries, deferrals, backfill checkpoints and run history in `ops.job_run`
- [ ] `/system/jobs`, `system.job.run` (C1) and the D16 Jobs widget work; failures raise `alert.warning.job_failed`
- [ ] The P0 seal, WORM export and restore-test jobs run on `mt-scheduler`; no Prefect service or deployment remains
- [ ] CI green (`cargo clippy`, `cargo test`, `supabase test db`, `pnpm test`, `pnpm playwright`, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- A job definition removed from `config/jobs.yaml` is disabled in `ops.job`, never deleted, so its history stays readable
- Two schedulers started by mistake: only one holds the advisory lock that drives cron (`pg_try_advisory_lock`); the second runs as a worker only and logs a warning
- Clock step (chrony): cron uses UTC wall time for schedules and monotonic time for leases and timeouts
- Supabase Postgres down: no runs start; running jobs finish or time out; the scheduler alerts `alert.critical.scheduler_db_down` through the fan-out and recovers without manual steps
- In-database housekeeping that must run even if the scheduler is down (e.g. the partition backstop in P1-T075) may stay a pg_cron SQL function; anything that runs a binary or calls out runs on `mt-scheduler`

## Cardinal rules (do NOT)

- Do NOT add Prefect, Celery, Airflow or another orchestrator; `mt-scheduler` is the one scheduler ([17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20))
- Do NOT give the `scheduler` or `research-worker` containers venue keys, data API keys or signer access; Python jobs never place orders, sign or sit on the live decision path ([18 §2.2](../../../docs/18-platform-and-deployment.md#22-python-uv-workspace-packages-only-where-absolutely-required))
- Do NOT hard-code retry counts, timeouts or schedules; they live in `config/jobs.yaml` and 16
- Do NOT UPDATE or DELETE WORM rows (`audit.*`); manual runs are new `audit.command` rows ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add an image without pinning it by digest, or vendored code that carries telemetry or referral IDs.
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)` (`mt-store`, also through its Python binding); research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.35 once every task traced to it in PHASE.md is done; note P1-T077 next to it.
- `docs/18-platform-and-deployment.md` §2.1: name the `ops.job`/`ops.job_run` tables and the `scheduler`/`research-worker`/`ingest-batch` split
- `docs/02-v1-architecture.md` §3.2: `scheduler` and `research-worker` containers; §5.1: `ops.job`, `ops.job_run`
- `docs/16-configuration-and-safety-model.md` §2.15: scheduler defaults (retries, backoff, timeout, misfire grace, lease)
- `docs/ui/dashboards/D16-system.md`: Jobs widget fields as built

## Branch & PR

- Branch: `p1/P1-T077-mt-scheduler-skeleton-postgres-backed-jobs-cron-`
- PR title: `P1-T077: mt-scheduler skeleton: Postgres-backed jobs, cron, retries, run history`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T077` run

## Progress log

- 2026-11-20 01:08 · cloud:vm:be04b6ae61f8 · created
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (filled the stub: `mt-scheduler` skeleton replacing Prefect per 18 §2.1 and R1.18/T1.35; Postgres queue + cron + retries + backfill checkpoints + run history; `/system/jobs`, `system.job.run`, D16 Jobs widget; moves the P0 seal, WORM-export and restore-test jobs; the T1.68 checks are the separate VERIFY task P1-T079)
