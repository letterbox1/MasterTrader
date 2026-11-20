---
id: P1-T080
kind: task
title: Move the P0 host-timer jobs onto mt-scheduler and wire the backup and restore commands
phase: 1
type: OPS
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T077, P0-T037, P0-T038, P0-T039, P0-T040, P0-T041]
requirements: [R1.18]
roadmap_todos: [T1.35]
modules: [mt-scheduler, M17]
dashboards: [D16]
tools: [git, cargo, supabase, docker]
mcp: []
env: []
services: [supabase-postgres, mt-scheduler]
branch: p1/P1-T080-move-the-p0-host-timer-jobs-onto-mt-scheduler-an
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/18-platform-and-deployment.md, docs/07-security-notes.md, docs/ui/dashboards/D16-system.md]
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

# P1-T080 · Move the P0 host-timer jobs onto mt-scheduler and wire the backup and restore commands

## Goal / expected outcome

Every P0 job that runs from a host timer (`infra/timers/`, installed by `just timers-install`) runs on `mt-scheduler` on the same schedule, with run history in `ops.job_run` and status on D16, and its timer is gone. `mt-api`'s `system.backup.run` and `system.restore.test` stop answering `job_runner_unavailable` and enqueue the matching scheduler jobs. After this the platform has one scheduler (T1.35, the "move the P0 jobs onto it" part).

## Context & references

- Roadmap: requirement [R1.18](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.35](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets) ("move the P0 restore-test and WORM-export jobs onto it")
- Platform: [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-scheduler` replaces Prefect) · [18 §4.7](../../../docs/18-platform-and-deployment.md#47-backups) (backups) · [07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit) (restore tested monthly)
- P0 hand-over (from the Phase 0 alignment): P0 runs these as host timers because P0 needs them before the scheduler exists; `system.backup.run` and `system.restore.test` answer `job_runner_unavailable` until it does (P0-T034, P0-T051). The scheduler DB role is `mt_jobs_rw` (renamed from `mt_flows_rw`, P0-T024)
- The timers to move (names from P0): `mt-seal` (P0-T037), `mt-verify-incr` hourly and `mt-verify-full` daily 01:00 UTC (P0-T038), `mt-backup-full` Sun 02:00 and `mt-backup-incr` 02:00 other days Australia/Sydney plus `mt-restic` 03:00 (P0-T039), the monthly WORM export (P0-T040), `mt-restore-test` 1st Sunday 04:00 Australia/Sydney (P0-T041); times are settings ([16 §2.11](../../../docs/16-configuration-and-safety-model.md#211-worm-integrity), [16 §2.14](../../../docs/16-configuration-and-safety-model.md#214-platform--operations))
- Depends on (this phase): P1-T077 (`mt-scheduler`, `command` jobs, `/system/jobs`, D16 Jobs widget)
- Cross-phase prerequisites (depends_on): P0-T037, P0-T038, P0-T039, P0-T040, P0-T041 (the jobs and their timers exist)

## Requirements

- Each timer job becomes a `command` job in `config/jobs.yaml` with the same command, schedule and timezone (read from the same settings, never copied as literals) and a retry policy suited to it (the restore test and full backup don't auto-retry more than once; the seal catches up missed runs as its timer did)
- Jobs that must run on the database host (pgBackRest, restic, the restore test's compose profile) run in a `host` queue worker (`mt-scheduler worker --queue host`) started as one long-running service on the workstation; it has only the backup credentials those jobs already use (from tmpfs, P0-T022) and no venue or data keys
- Remove each moved timer (its unit files under `infra/timers/` and its `just timers-install` entry) in the same PR; `just timers-install` then installs nothing for these jobs (or is removed if nothing else uses it)
- `system.backup.run` (kind full/incremental) and `system.restore.test` in `mt-api` enqueue the matching job with trigger `manual` (C-levels as P0 defined them; audited in `audit.command`) and return the run id; D16 Backups links to the run in the Jobs widget
- Results the P0 jobs already write (`ops.restore_test`, `audit.verify_run`, seal rows, export manifests, backup metrics) stay as they are; the scheduler adds `ops.job_run` history and `alert.warning.job_failed` on top, and the existing staleness alerts (e.g. restore test > 35 days, seal missing) keep firing
- The scheduler and workers connect as `mt_jobs_rw`

## ToDo

- [ ] Add the job definitions for every timer in `infra/timers/` (seal, verify incremental/full, backup full/incremental, restic, WORM export, restore test)
- [ ] Add the `host` queue worker service on the workstation
- [ ] Wire `system.backup.run` and `system.restore.test` to enqueue jobs and return the run id; remove the `job_runner_unavailable` path
- [ ] Remove the moved timers and their `just timers-install` entries
- [ ] Run each job once on the workstation stack through the scheduler and record the result in the progress log
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- `cargo test -p mt-scheduler p0_jobs`: for each moved job, the scheduler's next runs on a fixed clock equal the former timer's `OnCalendar` next runs (across an Australia/Sydney DST change); a clock-controlled run of each (stub command) lands in `ops.job_run`
- `cargo test -p mt-scheduler timers_removed` (or `just timers-check`): no unit in `infra/timers/` remains for a job that `config/jobs.yaml` schedules
- `cargo test -p mt-api backup_restore_commands`: `system.backup.run` and `system.restore.test` enqueue their jobs, are audited in `audit.command`, and never return `job_runner_unavailable`
- `supabase test db`: `mt_jobs_rw` can enqueue and read `ops.job*` and can't UPDATE or DELETE `audit.*`

### Scenarios

- Given the workstation stack with the scheduler, when the seal time passes, then the seal runs once from `mt-scheduler`, `ops.job_run` records it and no host timer fires
- Given you press "Back up now" in D16, when the command runs, then a `manual` incremental backup job starts and D16 links to its run
- Given the restore test fails, when its run ends, then `alert.warning.job_failed` and the existing restore-test alert both fire

### Stress / failure injection

- Stop the scheduler across the seal time and restart it inside the misfire grace: the seal runs once (catch-up), never twice
- Kill the `host` worker during an incremental backup: the run is re-queued after its lease expires and pgBackRest's own locking prevents two concurrent backups

## Acceptance criteria

- [ ] Every former P0 timer job runs on `mt-scheduler` on its former schedule, with history in `ops.job_run`; no such timer remains
- [ ] `system.backup.run` and `system.restore.test` enqueue scheduler jobs
- [ ] CI green (`cargo clippy`, `cargo test`, `supabase test db`, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- A P0 job not built yet: its definition is added `enabled: false` and its task enables it; its timer, if any, is removed only once the job is enabled
- WAL archiving (`archive_command`, continuous) is not a timer job and stays in Postgres config
- The off-site `restic forget` runs only from the separate admin machine (P0-T039); it is never scheduled here

## Cardinal rules (do NOT)

- Do NOT leave a job scheduled twice (timer and scheduler) or not at all; the parity test must pass before a timer is removed
- Do NOT give the `host` worker venue keys, data API keys or delete rights on the backup repositories
- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.35 once every task traced to it in PHASE.md is done; note P1-T080 next to it.
- `docs/18-platform-and-deployment.md` §4.7: backups and the restore test run on `mt-scheduler` (host queue worker); host timers retired
- `docs/07-security-notes.md` §8: the monthly restore test is an `mt-scheduler` job
- `docs/ui/dashboards/D16-system.md`: Backups actions enqueue scheduler jobs and link to their runs

## Branch & PR

- Branch: `p1/P1-T080-move-the-p0-host-timer-jobs-onto-mt-scheduler-an`
- PR title: `P1-T080: Move the P0 host-timer jobs onto mt-scheduler and wire the backup and restore commands`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T080` run

## Progress log

- 2026-11-20 01:20 · cloud:vm:be04b6ae61f8 · created
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (created from the Phase 0 hand-over: moves the `infra/timers/` jobs (seal, verify, backups, restic, WORM export, restore test) onto `mt-scheduler` with a schedule-parity test and timer removal, and wires `system.backup.run`/`system.restore.test` to enqueue jobs; DB role `mt_jobs_rw`; split from P1-T077 so the shared scheduler skeleton doesn't wait for the P0 backup chain)
