---
id: P0-T057
kind: task
title: Run the first restore test from the off-site backup
phase: 0
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T041, P0-T006, P0-T019, P0-T022]
requirements: [R0.N4, R0.07]
roadmap_todos: [T0.63]
modules: [M17]
dashboards: []
tools: [docker, pgbackrest, restic, sops]
mcp: []
env: [PGBACKREST_REPO1_S3_KEY, PGBACKREST_REPO1_S3_KEY_SECRET, PGBACKREST_REPO1_CIPHER_PASS, RESTIC_PASSWORD, B2_ACCOUNT_ID, B2_ACCOUNT_KEY]
services: [backblaze-b2, postgres, prefect-server]
branch: p0/P0-T057-first-offsite-restore-test
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md]
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

# P0-T057 · Run the first restore test from the off-site backup

## Goal / expected outcome

On the real host, the backups are pointed at the real Object-Locked target from P0-T006 for the first time (first full + incremental + WAL; delete probe fails), and then the restore-test flow restores the latest **off-site** backup into a scratch DB, all checks pass (including `audit.verify` against external seals), and the result is visible in D16 Backups — the evidence for exit criterion 3.

## Context & references

- [Roadmap P0 R0.N4](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.63](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [Roadmap P0 §6 exit criteria](../../../docs/roadmap/phase-0-foundations.md#6-exit-criteria-demo) (3)
- [07 §8 backups & audit](../../../docs/07-security-notes.md#8-data-protection-backups--audit)
- Flow: P0-T041; backup config: P0-T039 (built keyless on MinIO)
- This is the late live check for the backup target (build first, keys last): it carries the env names (values only in the secrets file) and depends on the USER task that provides them.
- Depends on: P0-T041, P0-T006 (real target + keys), P0-T019 (production host), P0-T022 (secrets on the host)

## Requirements

- Real target: the production stanza and restic repo point at the P0-T006 buckets (or the append-only rest-server); credentials come from the secrets file, never from the task or logs; the Object Lock delete probe from P0-T006 runs here and must fail.
- Source: off-site repo only (temporarily rename the local spool to prove it's not used).
- At least one full + one diff + WAL since; target time = now − 5 min.
- Checks all pass; duration and backup label recorded in `ops.restore_test`; screenshot of D16 Backups.
- Repeat once after a deliberate `pgbench` write burst to confirm WAL replay reaches the target time.

## ToDo

- [ ] Point the production stanza/restic repo at the real target; run the first full + incremental; run the delete probe (must fail).
- [ ] Trigger `system.restore.test` from D16 (C1).
- [ ] Watch the Prefect run; collect logs (no secrets).
- [ ] Record results here and attach the D16 screenshot.
- [ ] File a bug for any failure.

## Verification

### Tests
- The restore-test flow checks (row counts, alembic head, pit sample, audit.verify full).

### Scenarios
- Given the local disk is lost, when restoring from B2 only, then the scratch DB matches production as of the target time.

### Stress / failure injection
- Second run after write burst (above).

## Acceptance criteria

- [ ] First full + incremental + WAL on the real off-site target; delete probe fails
- [ ] Restore from off-site succeeds with all checks green
- [ ] Result visible in D16 and `ops.restore_test`
- [ ] Evidence attached for exit criterion 3
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Slow restore over home broadband: acceptable; log duration for the runbook RTO.

## Cardinal rules (do NOT)

- Do NOT restore into the production cluster.
- Do NOT count a restore that skipped `audit.verify`.
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/runbooks/`: record measured restore duration (RTO) in the backup & restore runbook (P0-T060).
- `docs/roadmap/phase-0-foundations.md`: tick T0.63 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T057-first-offsite-restore-test`
- PR title: `P0-T057: Run the first restore test from the off-site backup`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T057` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keys-last: now the late live check for the real backup target (after P0-T006) with env names; size S→M; run fields added)
