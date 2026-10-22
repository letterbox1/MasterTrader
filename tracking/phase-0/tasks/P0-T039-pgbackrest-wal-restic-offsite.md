---
id: P0-T039
kind: task
title: Set up pgBackRest, WAL archiving and restic off-site backups
phase: 0
type: OPS
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T020, P0-T022]
requirements: [R0.N4, R0.07]
roadmap_todos: [T0.44]
modules: [M17, ops]
dashboards: []
tools: [git, uv, python>=3.12, docker, pgbackrest, restic]
mcp: []
env: []
services: [postgres, minio, prefect-server]
branch: p0/P0-T039-pgbackrest-wal-restic-offsite
pr: ""
doc_sync: [docs/07-security-notes.md, docs/02-v1-architecture.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T039 · Set up pgBackRest, WAL archiving and restic off-site backups

## Goal / expected outcome

Postgres is continuously protected: pgBackRest with WAL archiving to the Object-Locked `mt-pgbackrest` bucket (encrypted), weekly full + nightly incremental backups, and restic snapshots of the non-DB state (MLflow artifacts, Prefect/Grafana config, the encrypted secrets file copy, `infra/seed`) to `mt-restic`. Failures alert; `/system/backups` shows age, size and WAL lag.

## Context & references

- [Roadmap P0 R0.N4](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.44](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [07 §8 backups & audit](../../../docs/07-security-notes.md#8-data-protection-backups--audit)
- [02 §5.1 stores](../../../docs/02-v1-architecture.md#51-stores)
- [02 §8 flows (F5, F6, F11)](../../../docs/02-v1-architecture.md#8-end-to-end-flows) (F11 backup & incident)
- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers) (Backups row)
- Schedule decided in [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (P0-B011, closed): continuous WAL archive, nightly incremental, weekly full, monthly restore test, monthly immutable WORM export; no separate `pg_dump`.
- Depends on: P0-T020, P0-T022. Build first, keys last: built and tested against MinIO with Object Lock in CI/dev; the first backup to the real off-site target (P0-T006) happens in P0-T057.

## Requirements

- pgBackRest stanza `mt`: `repo1-type=s3` (B2 endpoint) or `repo1-type=posix` on a mounted rest-server alternative; `repo1-cipher-type=aes-256-cbc` with pass from tmpfs; `compress-type=zst`; `archive-async=y`; `process-max=4`.
- Schedule (Prefect or systemd timers): **full weekly** (Sun 02:00 Australia/Sydney), **incremental nightly** (02:00 other days), WAL continuous (`archive_timeout=60`); times are settings, not literals ([16 §2.14](../../../docs/16-configuration-and-safety-model.md#214-platform--operations)).
- Retention: `repo1-retention-full=4` (≈ 4 weeks); bucket Object Lock 35 days ≥ effective retention so expire never hits a locked object prematurely — document the arithmetic in the PR.
- restic: repo `s3:…/mt-restic` (or `rest:` append-only), password from tmpfs; nightly 03:00; paths `/srv/mastertrader/mlflow`, `/srv/mastertrader/prefect`, `~/.config/mastertrader/secrets.sops.yaml` (already encrypted), `infra/` config; `restic forget` policy `--keep-daily 7 --keep-weekly 8 --keep-monthly 24` run **only** from your laptop (the host key has no delete rights in append-only mode).
- Metrics: pgBackRest `info --output=json` and restic `snapshots --json` scraped into Prometheus via a small exporter job (`mt_backup_last_success_timestamp{kind}`, `mt_backup_size_bytes`, `mt_wal_archive_lag_seconds`).
- Alerts (P0-T045): no successful backup in 26 h, WAL archive lag > 15 min, restic failure.
- `ops.backup_run` rows (non-WORM ops table) for D16 history; `system.backup.run` (C1) triggers an on-demand incremental.

## ToDo

- [ ] Configure pgBackRest in the Postgres container (included in timescaledb-ha) + `archive_command`.
- [ ] Create the stanza against MinIO (CI/dev), run a full + incremental, check `pgbackrest check`.
- [ ] Configure restic and the first snapshot.
- [ ] Write the exporter job and Prometheus scrape.
- [ ] Wire `system.backup.run` handler (Prefect deployment).
- [ ] Record bucket, schedule and retention in the runbook draft for P0-T060.

## Verification

### Tests
- Integration (CI with MinIO object lock): stanza create → full → WAL push → `pgbackrest info` shows backup; `check` passes.
- Integration: host key cannot delete objects (403 / lock error).
- Metric test: exporter emits the three metrics.

### Scenarios
- Given B2 is down for 2 h, when WAL segments accumulate, then `archive-async` queues them locally, lag alert fires after 15 min, and they upload when B2 returns (no gap).
- Given ransomware encrypts the host, when it tries to delete backups with the host key, then Object Lock refuses.

### Stress / failure injection
- Write load: `pgbench -c 8 -T 600` while archiving → WAL lag stays < 2 min; no archive failures.

## Acceptance criteria

- [ ] Full + incremental + continuous WAL to a MinIO Object-Lock target (pgBackRest info attached, no secrets); the real target is P0-T057
- [ ] restic snapshot present; delete with the host key fails (MinIO lock)
- [ ] Backup metrics + alerts live
- [ ] `system.backup.run` works from the API
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Disk full on the WAL spool: Postgres stops accepting writes rather than losing WAL; disk alert at 80 % (P0-T045).
- Backup during a long migration: allowed; restore test catches inconsistency.

## Cardinal rules (do NOT)

- Do NOT give the host credentials that can delete or shorten locks on backup objects.
- Do NOT back up the age identity or the offline worm_owner file to these buckets.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/07-security-notes.md` §8 and `docs/02-v1-architecture.md` §5.1: confirm the schedule matches (continuous WAL, nightly incremental, weekly full); add the retention arithmetic.
- `docs/roadmap/phase-0-foundations.md`: tick T0.44 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T039-pgbackrest-wal-restic-offsite`
- PR title: `P0-T039: Set up pgBackRest, WAL archiving and restic off-site backups`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T039` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (schedule per 17 §B P0-B011 (nightly incremental, weekly full); keyless build on MinIO, real target in P0-T057; run fields added)
