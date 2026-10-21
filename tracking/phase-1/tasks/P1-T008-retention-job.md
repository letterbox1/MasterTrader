---
id: P1-T008
kind: task
title: Enforce retention_days with a scheduled retention job
phase: 1
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T007]
requirements: [R1.09]
roadmap_todos: [T1.26]
modules: [M1]
dashboards: [D07]
branch: p1/P1-T008-retention-job
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/12-policy-and-compliance.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T008 · Enforce retention_days with a scheduled retention job

## Goal / expected outcome

A Prefect flow deletes rows and Parquet files whose age exceeds their `retention_days`, logs what it removed, and never touches WORM tables, so terms like CoinGecko's ≤ 24 h cache are enforced automatically.

## Context & references

- Roadmap: requirements [R1.09](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.26](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Policy: [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) (retention jobs enforce `retention_days`, e.g. CoinGecko ≤ 1 day) · [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (CoinGecko: cache ≤ 24 h, encrypted, deleted on exit)
- WORM scope (never deleted): [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)
- Depends on (this phase): P1-T007

## Requirements

- Flow `mt_data.flows.retention` runs hourly; for each ingest table with provenance it deletes rows where `ingest_time < now() - retention_days`
- Parquet: files whose metadata `retention_days` has expired are deleted from hot and cold tiers
- Writes a summary row per run to `ops.retention_run` (table, rows deleted, oldest kept) and a metric `mt_retention_deleted_total`
- Hard allow-list of tables it may touch; any `audit.*`, `journal.*`, `risk.change` table in scope → refuse to run and alert
- Short-retention caches (CoinGecko) also purge on service shutdown (12 §4 "deleted on exit")

## ToDo

- [ ] Implement the flow with a table allow-list built from tables that have provenance columns and are not WORM
- [ ] Implement Parquet expiry using the catalog helpers
- [ ] Add the shutdown purge hook used by P1-T029
- [ ] Migration for `ops.retention_run`
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: cut-off computation per row; NULL retention never deleted
- Integration: rows with `retention_days=1` older than 24 h are deleted, younger kept; WORM table in config → flow refuses
- Integration: Parquet file with expired metadata is removed from both tiers

### Scenarios

- Given CoinGecko rows ingested 25 h ago, when the hourly job runs, then they are gone and `ops.retention_run` records the count
- Given someone adds `audit.dq_event` to the allow-list, when the job starts, then it aborts with `alert.critical.retention_worm_guard`

### Stress / failure injection

- Load: delete 10 M expired rows in batches of 50k without locking the hypertable for > 1 s per batch

## Acceptance criteria

- [ ] CoinGecko-style rows never survive more than 24 h + one job interval (≤ 25 h); P1-T059 verifies end to end
- [ ] Job cannot be pointed at WORM tables (tested)
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Job down for a day: next run catches up; alert if any expired row is older than 2× its retention
- Timescale compressed chunks: decompress-delete or drop whole chunks when the entire chunk is expired

## Cardinal rules (do NOT)

- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.26 once every task traced to it in PHASE.md is done; note P1-T008 next to it.
- `docs/12-policy-and-compliance.md` §5: state the hourly cadence and the WORM guard

## Branch & PR

- Branch: `p1/P1-T008-retention-job`
- PR title: `P1-T008: Enforce retention_days with a scheduled retention job`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T008` run

## Progress log

- 2026-10-21 00:00 · planner · created
