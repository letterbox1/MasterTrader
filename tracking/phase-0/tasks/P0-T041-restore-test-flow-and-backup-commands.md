---
id: P0-T041
kind: task
title: Build the monthly restore-test Prefect flow
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
branch: p0/P0-T041-restore-test-flow-and-backup-commands
pr: ""
doc_sync: [docs/runbooks/README.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T041 · Build the monthly restore-test Prefect flow

## Goal / expected outcome

A Prefect flow restores the latest off-site pgBackRest backup (+ WAL to a target time) into a throwaway `postgres-restore` container, runs integrity checks including `audit.verify` against the external seals, records the result in `ops.restore_test`, tears down, and alerts on failure. It runs monthly and on demand via `system.restore.test` (C1).

## Context & references

- [Roadmap P0 R0.N4](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [07 §8 backups & audit](../../../docs/07-security-notes.md#8-data-protection-backups--audit) (restore tested monthly)
- [02 §9.2 SLOs](../../../docs/02-v1-architecture.md#92-observability--slos) (Backup restore test: monthly pass)
- [15 §2.4 tests](../../../docs/15-bots-hitl-and-worm-audit.md#24-tests-part-of-every-phase-that-adds-a-worm-table) (restore re-verifies)
- [04 standing rules](../../../docs/04-plan-of-action.md#standing-rules) (monthly restore test)
- Depends on: P0-T039, P0-T034, P0-T038

## Requirements

- Restore source: the off-site repo only (never the local spool), `--type=time` to now − 5 min or latest.
- Scratch target: `postgres-restore` service (same digest as `postgres`), on `core` network, data in a temp volume, destroyed after.
- Checks: Postgres starts; `alembic current` == expected head; row counts per schema within tolerance of prod snapshot taken at backup time; `audit.verify` (full mode) on the restored DB against external seals = ok; a sample `pit()` query returns.
- Result in `ops.restore_test` (started, finished, duration, backup label, checks, status) and metric `mt_restore_test_last_success_timestamp`; alert if > 35 days since last pass.
- Schedule: 1st Sunday of the month 04:00 Australia/Sydney; on-demand via `system.restore.test`.

## ToDo

- [ ] Write the flow and the compose profile for `postgres-restore`.
- [ ] Implement the checks; reuse the verifier from P0-T038.
- [ ] Wire the command handler and D16 data (`/system/backups`).
- [ ] Tests below; the first real off-site run is P0-T057.

## Verification

### Tests
- Integration (CI with MinIO): backup fixture DB → restore → all checks pass; corrupt one WAL file → flow fails and alerts.
- Unit: check result aggregation and status rules.

### Scenarios
- Given the restored DB's audit chain differs from the anchored seal, then the restore test fails and raises a critical incident (backup tampering).

### Stress / failure injection
- Restore of a 50 GB fixture completes within 60 min on the host (log actual).

## Acceptance criteria

- [ ] Flow runs end to end on CI fixtures
- [ ] Results visible via `/system/backups` and metrics
- [ ] Alert on failure and on > 35 days without a pass
- [ ] Scheduled monthly
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Disk space for the scratch restore: flow checks free space ≥ 1.5× backup size first and fails early with a clear message.

## Cardinal rules (do NOT)

- Do NOT restore over the production database.
- Do NOT mark a restore test passed if `audit.verify` was skipped.
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/runbooks/README.md`: link the restore-test flow from the backup & restore runbook.
- `docs/roadmap/phase-0-foundations.md`: tick T0.44 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T041-restore-test-flow-and-backup-commands`
- PR title: `P0-T041: Build the monthly restore-test Prefect flow`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T041` run

## Progress log

- 2026-10-21 00:00 · planner · created
