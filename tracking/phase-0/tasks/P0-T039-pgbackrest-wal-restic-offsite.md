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
depends_on: [P0-T020, P0-T022, P0-T006]
requirements: [R0.N4, R0.07]
roadmap_todos: [T0.44]
modules: [M17, ops]
dashboards: []
branch: p0/P0-T039-pgbackrest-wal-restic-offsite
pr: ""
doc_sync: [docs/07-security-notes.md, docs/02-v1-architecture.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T039 · Set up pgBackRest, WAL archiving and restic off-site backups

## Goal / expected outcome

Postgres is continuously protected: pgBackRest with WAL archiving to the Object-Locked `mt-pgbackrest` bucket (encrypted), weekly full + daily differential backups, and restic snapshots of the non-DB state (MLflow artifacts, Prefect/Grafana config, the encrypted secrets file copy, `infra/seed`) to `mt-restic`. Failures alert; `/system/backups` shows age, size and WAL lag.

## Context & references

- [Roadmap P0 R0.N4](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.44](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [07 §8 backups & audit](../../../docs/07-security-notes.md#8-data-protection-backups--audit)
- [02 §5.1 stores](../../../docs/02-v1-architecture.md#51-stores)
- [02 §8 flows (F5, F6, F11)](../../../docs/02-v1-architecture.md#8-end-to-end-flows) (F11 backup & incident)
- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers) (Backups row)
- Schedule inconsistencies across 07 §8 / 02 §5.1 / F11 are P0-B011.
- Depends on: P0-T020, P0-T022, P0-T006

## Requirements

- pgBackRest stanza `mt`: `repo1-type=s3` (B2 endpoint) or `repo1-type=posix` on a mounted rest-server alternative; `repo1-cipher-type=aes-256-cbc` with pass from tmpfs; `compress-type=zst`; `archive-async=y`; `process-max=4`.
- Schedule (Prefect or systemd timers): **full weekly** (Sun 02:00 Australia/Sydney), **diff daily** (02:00 other days), WAL continuous (`archive_timeout=60`).
- Retention: `repo1-retention-full=4` (≈ 4 weeks); bucket Object Lock 35 days ≥ effective retention so expire never hits a locked object prematurely — document the arithmetic in the PR.
- restic: repo `s3:…/mt-restic` (or `rest:` append-only), password from tmpfs; nightly 03:00; paths `/srv/mastertrader/mlflow`, `/srv/mastertrader/prefect`, `/etc/mastertrader/secrets.sops.yaml` (already encrypted), `infra/` config; `restic forget` policy `--keep-daily 7 --keep-weekly 8 --keep-monthly 24` run **only** from your laptop (the host key has no delete rights in append-only mode).
- Metrics: pgBackRest `info --output=json` and restic `snapshots --json` scraped into Prometheus via a small exporter job (`mt_backup_last_success_timestamp{kind}`, `mt_backup_size_bytes`, `mt_wal_archive_lag_seconds`).
- Alerts (P0-T045): no successful backup in 26 h, WAL archive lag > 15 min, restic failure.
- `ops.backup_run` rows (non-WORM ops table) for D16 history; `system.backup.run` (C1) triggers an on-demand diff.

## ToDo

- [ ] Configure pgBackRest in the Postgres container (included in timescaledb-ha) + `archive_command`.
- [ ] Create the stanza, run the first full backup, check `pgbackrest check`.
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

- [ ] First full backup + continuous WAL to the locked bucket (pgBackRest info attached, no secrets)
- [ ] restic snapshot present; delete with host key fails
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

- `docs/07-security-notes.md` §8 and `docs/02-v1-architecture.md` §5.1: align the schedule to weekly full + daily diff + continuous WAL.
- `docs/roadmap/phase-0-foundations.md`: tick T0.44 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T039-pgbackrest-wal-restic-offsite`
- PR title: `P0-T039: Set up pgBackRest, WAL archiving and restic off-site backups`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T039` run

## Progress log

- 2026-10-21 00:00 · planner · created
