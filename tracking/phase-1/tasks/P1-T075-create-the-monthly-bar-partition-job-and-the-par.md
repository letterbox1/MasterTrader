---
id: P1-T075
kind: task
title: Create the monthly bar partition job and the Parquet hot-window export
phase: 1
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T013, P1-T012, P0-T027]
requirements: [R1.02, R1.N3]
roadmap_todos: [T1.21]
modules: [M1]
dashboards: [D07]
tools: [git, cargo, supabase, docker]
mcp: []
env: []
services: [supabase-postgres]
branch: p1/P1-T075-create-the-monthly-bar-partition-job-and-the-par
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/18-platform-and-deployment.md, docs/02-v1-architecture.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-19
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-T075 · Create the monthly bar partition job and the Parquet hot-window export

## Goal / expected outcome

Monthly partitions of every `market.bar_*` table (built and vendor) always exist ahead of time, and bars older than their hot window move to the Parquet catalog and are dropped from Postgres, with `pit(as_of)` reading both transparently. This replaces TimescaleDB chunking and compression ([18 §4.3](../../../docs/18-platform-and-deployment.md#43-bars-without-timescaledb)), keeps the recorder from failing at a month boundary, and keeps the database inside the storage budget (R1.N3).

## Context & references

- Roadmap: requirements [R1.02](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.N3](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.21](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Platform: [18 §4.2](../../../docs/18-platform-and-deployment.md#42-extensions) (pg_cron; pg_partman if available (U)) · [18 §4.3](../../../docs/18-platform-and-deployment.md#43-bars-without-timescaledb) (partitions created ahead by pg_partman where available, otherwise by an `mt-store` partition job scheduled with pg_cron; old bars exported to Parquet and dropped) · [18 §10](../../../docs/18-platform-and-deployment.md#10-sources) (Supabase pg_partman guide)
- Defaults: [16 §2.15](../../../docs/16-configuration-and-safety-model.md#215-platform-deployment-and-regions) `db.bars_1s_hot_days` (90), `db.bars_hot_months` (workstation: unlimited for 1m and larger; cloud: 24)
- Built on: P1-T013 (partitioned bar tables), P1-T012 (Parquet catalog layout), P0-T027 (`pit(as_of)` and catalog helpers)
- Related: P1-T052 (storage tiers and disk alerts), P1-T076 (rollup job)

## Requirements

- **Check first (U):** confirm whether pg_partman is available on the Supabase Postgres 17 image we pin (local CLI stack and the self-hosted workstation stack). Record the result in the progress log and in 18 §4.2
- **Partition creation:** with pg_partman, register every `market.bar_*` parent (monthly, premake 3 months by default, configurable); without it, an `mt-store` partition job (`mt-store partitions ensure`, Rust) creates the current + next 3 months' partitions, scheduled daily with pg_cron. Either way it is idempotent and runs in a Supabase migration-defined schedule
- **Hot-window export:** a job (`mt-store bars export-cold`) exports whole monthly partitions past their hot window to the Parquet catalog (zstd, provenance metadata kept, row count and checksum verified), then detaches and drops the partition. 1s bars after `db.bars_1s_hot_days`; other sizes after `db.bars_hot_months` (workstation default: never). Values come from settings, never constants
- **`pit(as_of)` reads both:** `mt-store` `bars::query` unions Postgres partitions and the exported Parquet files for a range, so a query spanning the boundary returns the same rows as before the export (tested through the Python binding too)
- Metrics: partitions ahead per table, last export, rows exported, bytes freed; alert `alert.critical.bar_partition_missing` when fewer than 1 month is premade, `alert.warning.bar_export_failed` on a failed export
- Market tables are not WORM; WORM tables never go through this job

## ToDo

- [ ] Check pg_partman availability on the pinned Supabase Postgres 17 image; record the result
- [ ] Supabase migration: pg_partman registration, or the pg_cron schedule for `mt-store partitions ensure`; pgTAP tests
- [ ] Implement `mt-store partitions ensure` (if needed) and `mt-store bars export-cold` in `crates/mt-store`
- [ ] Extend `bars::query` to read across Postgres and Parquet; Python binding test
- [ ] Metrics and alerts; D07 Storage tab fields (partitions ahead, last export)
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- `supabase test db`: after the job runs, every `market.bar_*` parent has partitions for the current + next 3 months; re-running changes nothing
- `cargo test -p mt-store partitions`: creation is idempotent; a missing month is created; WORM tables are refused
- `cargo test -p mt-store export_cold`: exporting a 1s partition older than `db.bars_1s_hot_days` writes Parquet with the same row count and checksum, then drops the partition; a checksum mismatch aborts before the drop
- `cargo test -p mt-store bars_query_cross_tier` and `uv run pytest -k bars_query_cross_tier`: a range spanning Postgres and Parquet returns identical rows before and after export

### Scenarios

- Given the clock is moved to the last day of a month, when the recorder writes the first bar of the next month, then the partition already exists and no alert fires
- Given `db.bars_1s_hot_days` is 90, when a 1s partition's newest row is 91 days old, then it is exported and dropped, and a `pit` query over that month still returns it
- Given the workstation default for `db.bars_hot_months`, when the job runs, then no 1m or larger partition is exported

### Stress / failure injection

- Fault: kill the export after the Parquet write but before the drop; the re-run verifies the file and finishes the drop without duplicating rows
- Fault: disk full on the cold tier during export; the partition stays in Postgres and `alert.warning.bar_export_failed` fires

## Acceptance criteria

- [ ] Partitions exist at least 3 months ahead for every `market.bar_*` table, created by code (pg_partman or the `mt-store` job via pg_cron)
- [ ] 1s bars past the hot window live only in Parquet and `pit(as_of)` returns the same results across the boundary
- [ ] CI green (`cargo clippy`, `cargo test`, `supabase test db`, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- pg_partman unavailable: the `mt-store` job is the only path; the migration must not require the extension
- Supabase cloud (P7 shift, optional): the same migrations and schedule apply; `db.bars_hot_months` defaults to 24 there
- A late correction (P1-T076) for an exported month: the rollup job re-imports that month's partition from Parquet, corrects it, and re-exports (logged)

## Cardinal rules (do NOT)

- Do NOT use TimescaleDB, hypertables or `time_bucket` ([18 §4.2](../../../docs/18-platform-and-deployment.md#42-extensions))
- Do NOT drop a partition before its Parquet export is verified
- Do NOT run this job on WORM tables (`audit.*`, `journal.*`); their partitions follow the WORM ceremony ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many))
- Do NOT hard-code hot windows; they come from 16 §2.15 settings
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)` (`mt-store`, also through its Python binding); research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.21 once every task traced to it in PHASE.md is done; note P1-T075 next to it.
- `docs/18-platform-and-deployment.md` §4.2/§4.3: record whether pg_partman was available and which path is used (clear the (U))
- `docs/02-v1-architecture.md` §5.1: partition and hot-window behaviour of the bar tables

## Branch & PR

- Branch: `p1/P1-T075-create-the-monthly-bar-partition-job-and-the-par`
- PR title: `P1-T075: Create the monthly bar partition job and the Parquet hot-window export`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T075` run

## Progress log

- 2026-11-19 00:00 · aligner · created in the re-platform wave per docs/18 §4.3 (no task owned the monthly partition job or the Parquet hot-window export that replace TimescaleDB chunks and compression)
