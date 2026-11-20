---
id: P1-T079
kind: task
title: Verify mt-scheduler: retries, resume after restart, cron history, D16 status
phase: 1
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T077, P1-T053]
requirements: [R1.18]
roadmap_todos: [T1.68]
modules: [mt-scheduler, M1]
dashboards: [D16, D07]
tools: [git, cargo, supabase, docker, pnpm]
mcp: []
env: []
services: [supabase-postgres, nats, mt-scheduler]
branch: p1/P1-T079-verify-mt-scheduler-retries-resume-after-restart
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md]
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

# P1-T079 · Verify mt-scheduler: retries, resume after restart, cron history, D16 status

## Goal / expected outcome

On the workstation stack with the real Phase 1 schedules, it is proven that `mt-scheduler` retries a failing job per its policy, resumes a backfill after a scheduler restart without duplicating data, records cron runs in its run history, and shows job status on D16 (and batch-source status on D07). This closes T1.68 and gives R1.18 its "scheduler tests" evidence.

## Context & references

- Roadmap: requirement [R1.18](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.68](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets) ("a failing job retries per its policy, a backfill resumes after a scheduler restart, cron runs land in the run history, and D16 shows job status")
- Platform: [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-scheduler`) · UI [D16 System](../../../docs/ui/dashboards/D16-system.md) Jobs widget · [D07](../../../docs/ui/dashboards/D07-data-quality.md) Feeds (batch sources)
- Depends on (this phase): P1-T077 (scheduler, `/system/jobs`, D16 Jobs widget), P1-T053 (the real P1 schedules and the `ingest-batch` worker; it already depends on every P1 batch job, incl. the data.binance.vision backfill P1-T015 used below)
- Feeds: P1-T067 (exit demo), P1-T065 (the soak runs on these schedules)

## Requirements

- Keyless: uses public sources and recorded fixtures only (a fake data.binance.vision server serving fixture ZIPs); no secrets
- E2E suite in the Rust e2e crate (`tests/e2e`, package `mt-e2e`): `cargo test -p mt-e2e --test scheduler -- --ignored` against `supabase start` + the workstation compose stack (`just e2e-scheduler`)
- Checks:
  - **Retry:** a test job registered with `retry.max_attempts: 3` that fails twice then succeeds shows three attempts in `ops.job_run`; one that always fails ends `failed` after exactly 3 attempts with the configured backoff spacing (± jitter) and raises `alert.warning.job_failed` once
  - **Resume:** start a 14-day P1-T015 backfill on fixtures, `docker kill` the `scheduler` and `ingest-batch` containers mid-run, restart them: the run resumes from its checkpoint, completes, and the row counts and checksums equal an uninterrupted reference run (no duplicates, no gaps)
  - **Cron history:** with the clock-controlled test schedule (every minute for 5 minutes, timezone `Australia/Sydney`), five `cron` runs land in `ops.job_run` with the expected `scheduled_for` times; the real P1 schedules from P1-T053 each show a correct next run in `/system/jobs`
  - **D16/D07:** `pnpm playwright` checks the D16 Jobs widget lists the jobs with last run, result, duration, next run and retries, that "Re-run" on a failed job starts a `manual` run audited in `audit.command`, and that D07 Feeds shows a batch source's last successful run
- Evidence (commands, outputs, screenshots) goes in the progress log and the exit-demo item P1-T067

## ToDo

- [ ] Write the e2e tests in `tests/e2e` (`mt-e2e` crate, test `scheduler`) and the `just e2e-scheduler` entry point
- [ ] Add the Playwright spec for the D16 Jobs widget and the D07 batch-source row
- [ ] Run the suite on the workstation stack; record results and screenshots in the progress log
- [ ] File a bug for any failure (`./kanban new --phase 1 --kind bug --found-in P1-T079`) instead of loosening a check
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- `cargo test -p mt-e2e --test scheduler -- --ignored`: retry, resume, cron-history and API checks all pass
- `pnpm playwright` (D16 Jobs and D07 Feeds specs) across the viewport matrix

### Scenarios

- Given a job that always fails, when its attempts are exhausted, then exactly one `alert.warning.job_failed` reaches the fan-out and D16 shows it red with "Re-run"
- Given the scheduler is killed mid-backfill, when it restarts, then the backfill completes from its checkpoint with data identical to an uninterrupted run
- Given the scheduler is down across a scheduled run for longer than the misfire grace, when it restarts, then the run is recorded `skipped` and the next run is on time

### Stress / failure injection

- Kill and restart Supabase Postgres during the cron-history window; runs resume and no run is executed twice
- Kill a worker holding a lease; the run is re-queued after the lease expires and finishes once

## Acceptance criteria

- [ ] Retry, resume-after-restart, cron-history and D16/D07 status checks pass on the workstation stack, with evidence in the progress log
- [ ] No duplicated or missing rows after the interrupted backfill (row counts and checksums match the reference)
- [ ] CI green (`cargo clippy`, `cargo test`, `pnpm playwright`, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- If a P1 job is still disabled (e.g. a source with `terms: unknown`), it appears in `/system/jobs` as disabled with its reason; that is a pass for the listing check
- Jitter makes exact retry times vary; the check uses the policy's bounds, never a widened tolerance

## Cardinal rules (do NOT)

- Do NOT shorten retry counts or misfire grace in the real `config/jobs.yaml` to make the test faster; use a test job with its own policy
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.68 once every task traced to it in PHASE.md is done; note P1-T079 next to it.

## Branch & PR

- Branch: `p1/P1-T079-verify-mt-scheduler-retries-resume-after-restart`
- PR title: `P1-T079: Verify mt-scheduler: retries, resume after restart, cron history, D16 status`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T079` run

## Progress log

- 2026-11-20 01:11 · cloud:vm:be04b6ae61f8 · created
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (created and filled for roadmap T1.68: scheduler VERIFY on the real P1 schedules, keyless; Rust e2e crate + Playwright; feeds the exit demo P1-T067)
