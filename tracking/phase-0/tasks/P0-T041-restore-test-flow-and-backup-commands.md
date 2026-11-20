---
id: P0-T041
kind: task
title: Build the monthly restore-test job
phase: 0
type: OPS
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T039, P0-T034, P0-T038]
requirements: [R0.N4, R0.07]
roadmap_todos: [T0.44]
modules: [M17, ops]
dashboards: []
tools: [git, docker, supabase, pgbackrest, cargo]
mcp: []
env: []
services: [supabase-postgres, minio]
branch: p0/P0-T041-restore-test-flow-and-backup-commands
pr: ""
doc_sync: [docs/runbooks/README.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T041 · Build the monthly restore-test job

## Goal / expected outcome

A restore-test job (`just restore-test`: the `restore` compose profile, pgBackRest restore, then the Rust `mt-obs restore-check`) restores the latest off-site pgBackRest backup (+ WAL to a target time) into a throwaway `postgres-restore` container (the same Supabase Postgres image digest), runs integrity checks including `audit.verify` against the external seals, records the result in `ops.restore_test`, tears down, and alerts on failure. In P0 it runs monthly from a host timer (`infra/timers/`, P0-T037) and on demand with `just restore-test` from the runbook (roadmap T0.44); P1-T077 moves it onto `mt-scheduler` (T1.35) and wires the `system.restore.test` (C1) command to it.

## Context & references

- [Roadmap P0 R0.N4](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [07 §8 backups & audit](../../../docs/07-security-notes.md#8-data-protection-backups--audit) (restore tested monthly)
- [02 §9.2 SLOs](../../../docs/02-v1-architecture.md#92-observability--slos) (Backup restore test: monthly pass)
- [15 §2.4 tests](../../../docs/15-bots-hitl-and-worm-audit.md#24-tests-part-of-every-phase-that-adds-a-worm-table) (restore re-verifies)
- [04 standing rules](../../../docs/04-plan-of-action.md#standing-rules) (monthly restore test)
- Depends on: P0-T039, P0-T034, P0-T038

## Requirements

- Restore source: the off-site repo only (never the local spool), `--type=time` to now − 5 min or latest.
- Scratch target: `postgres-restore` service (same digest as the Supabase Postgres image, P0-T070), on `core` network, data in a temp volume, destroyed after.
- Checks: Postgres starts; the latest version in `supabase_migrations.schema_migrations` == the newest file in `supabase/migrations/`; `supabase test db`-equivalent pgTAP invariants pass against the restored DB; row counts per schema within tolerance of prod snapshot taken at backup time; `audit.verify` (full mode) on the restored DB against external seals = ok; a sample `pit(as_of)` query (`mt-store`) returns.
- Result in `ops.restore_test` (started, finished, duration, backup label, checks, status) and metric `mt_restore_test_last_success_timestamp`; alert if > 35 days since last pass.
- Schedule: 1st Sunday of the month 04:00 Australia/Sydney (setting) via the host timer `mt-restore-test`; on demand `just restore-test`; `system.restore.test` (C1) through `mt-scheduler` from P1-T077.

## ToDo

- [ ] Write the `just restore-test` job and the `restore` compose profile for `postgres-restore`.
- [ ] Implement the checks in `mt-obs restore-check` (Rust); reuse the verifier from P0-T038.
- [ ] Feed D16 data (`/system/backups`) and add the host timer; the `system.restore.test` handler is wired to `mt-scheduler` in P1-T077.
- [ ] Tests below; the first real off-site run is P0-T057.

## Verification

### Tests
- Integration (CI with MinIO): backup fixture DB → restore → all checks pass; corrupt one WAL file → job fails and alerts.
- Unit: check result aggregation and status rules.

### Scenarios
- Given the restored DB's audit chain differs from the anchored seal, then the restore test fails and raises a critical incident with the integrity response ([16 §2.11](../../../docs/16-configuration-and-safety-model.md#211-worm-integrity)).

### Stress / failure injection
- Restore of a 50 GB fixture completes within 60 min on the workstation (log actual).

## Acceptance criteria

- [ ] Job runs end to end on CI fixtures
- [ ] Results visible via `/system/backups` and metrics
- [ ] Alert on failure and on > 35 days without a pass
- [ ] Scheduled monthly (host timer; `mt-scheduler` from P1-T077)
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, `supabase test db`, gitleaks, `pit` check)

## Exceptions & edge cases

- Disk space for the scratch restore: job checks free space ≥ 1.5× backup size first and fails early with a clear message.

## Cardinal rules (do NOT)

- Do NOT restore over the production database.
- Do NOT mark a restore test passed if `audit.verify` was skipped.
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/runbooks/README.md`: link the restore-test job from the backup & restore runbook.
- `docs/roadmap/phase-0-foundations.md`: tick T0.44 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T041-restore-test-flow-and-backup-commands`
- PR title: `P0-T041: Build the monthly restore-test job`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T041` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (integrity response wording (16 §2.11); keyless on MinIO, real target in P0-T057; run fields added)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (restore target uses the Supabase Postgres image; Alembic head check → `supabase_migrations` version + pgTAP invariants)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (Prefect flow → `just restore-test` job (Rust checks in `mt-obs restore-check`) on a host timer in P0, as roadmap T0.44 says; P1-T077 moves it onto `mt-scheduler` and wires `system.restore.test`; title no longer says Prefect)
