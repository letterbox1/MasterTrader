---
id: P0-T072
kind: task
title: Monthly bar partitions and the mt-store partition job
phase: 0
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T024, P0-T070]
requirements: [R0.03, R0.04]
roadmap_todos: [T0.22]
modules: [mt-store, market]
dashboards: []
tools: [git, cargo, supabase, psql]
mcp: []
env: []
services: [supabase-postgres]
branch: p0/P0-T072-monthly-bar-partitions-and-the-mt-store-partitio
pr: ""
doc_sync: [docs/18-platform-and-deployment.md, docs/03-build-spec.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T072 · Monthly bar partitions and the mt-store partition job

## Goal / expected outcome

Bars live in **native monthly range partitions** instead of TimescaleDB hypertables ([18 §4.3](../../../docs/18-platform-and-deployment.md#43-bars-without-timescaledb)). The `market.bar_*` parent tables exist, future partitions are always created ahead (pg_partman where available, otherwise the `mt-store` partition job on pg_cron), and the cold-partition path (export to Parquet, then drop) is built and tested on fixtures, honouring `db.bars_hot_months` and `db.bars_1s_hot_days` ([16 §2.15](../../../docs/16-configuration-and-safety-model.md#215-platform-deployment-and-regions)). The recorder and rollup job that fill them come in P1.

## Context & references

- [Roadmap P0 R0.03, R0.04](../../../docs/roadmap/phase-0-foundations.md#3-requirements) · [T0.22](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [18 §4.3 bars without TimescaleDB](../../../docs/18-platform-and-deployment.md#43-bars-without-timescaledb) · [18 §4.2 extensions](../../../docs/18-platform-and-deployment.md#42-extensions)
- [03 §4 data model](../../../docs/03-build-spec.md#4-data-model-overview) (`market` bars, "Bars without TimescaleDB")
- Depends on: P0-T024 (schemas), P0-T070 (pg_partman check, pg_cron)
- Related: P0-T027 (`pit` reads hot partitions and Parquet transparently), P1 recorder and rollup job

## Requirements

- Parent tables `market.bar_1s` and `market.bar` (all standard sizes 1m, 5m, 15m, 1h, 4h, 1D, 1W keyed by `bar_spec`), `PARTITION BY RANGE (ts)` monthly; primary key includes `ts`; `event_time` + `ingest_time` + provenance columns as every fact table (P0-T025); RLS deny-all like every table.
- Ahead-creation: at least `db.partitions_ahead_months` (default 3; add to 16 §2.15 at doc sync if absent) future partitions always exist. pg_partman config if P0-T070 found it available; otherwise an idempotent `mt-store` partition job (`mt-store partitions ensure`) scheduled with pg_cron (or the workstation scheduler) and safe to run any number of times.
- Cold path: `mt-store partitions export --older-than …` writes a closed partition to the Parquet catalog (hash recorded), verifies row counts, then detaches and drops it; 1s bars use `db.bars_1s_hot_days` (90), larger sizes `db.bars_hot_months` (workstation: unlimited, so no drop by default; cloud: 24). Values come from settings, never literals.
- `pit(as_of)` reads across Postgres partitions and the exported Parquet files with the same results (contract shared with P0-T027).
- A default partition catches out-of-range rows and raises an alert metric instead of silently growing.

## ToDo

- [ ] Migration for the partitioned parents (+ the default partition) in `supabase/migrations/`.
- [ ] pg_partman config or the `mt-store` partition job (Rust) + its pg_cron schedule.
- [ ] Export-then-drop command with row-count and hash checks.
- [ ] pgTAP tests (partitions exist ahead, RLS on partitions) and Rust tests (job idempotent, export round trip).
- [ ] Update docs listed under Doc sync.

## Verification

### Tests
- `supabase test db`: the parents are partitioned by range on `ts`; ≥ 3 future monthly partitions exist after `ensure`; RLS is on for parents and partitions.
- `cargo test -p mt-store partitions`: `ensure` run twice changes nothing; export of a fixture month to Parquet then `pit` over the same range returns identical rows before and after the drop.

### Scenarios
- Given the job hasn't run for two months, when it runs, then all missing partitions are created and no insert has landed in the default partition.
- Given `db.bars_hot_months` is unlimited (workstation), when the cold job runs, then nothing larger than 1s is dropped.

### Stress / failure injection
- Kill the export between writing Parquet and dropping the partition: the rerun detects the existing file by hash and completes; no rows lost or duplicated.

## Acceptance criteria

- [ ] Partitioned parents and ahead-creation in place (pg_partman or the job, choice logged)
- [ ] Export-then-drop verified; `pit` results identical across the move
- [ ] Settings drive every window; no literal retention values
- [ ] CI green (clippy, cargo test, `supabase test db`, gitleaks, `pit` check)

## Exceptions & edge cases

- pg_partman unavailable (U, 18 §4.2): the `mt-store` job is the only path; documented in 18.
- Cloud mode: partitions export to Parquet in Supabase Storage or the runtime host's catalog (decided at the shift, P7-T073).

## Cardinal rules (do NOT)

- Do NOT use TimescaleDB, hypertables or `time_bucket`; any other size is `date_bin()` at read time in `pit`.
- Do NOT drop a partition before its Parquet export is verified.
- Do NOT hard-code retention windows; they come from 16 §2.15 settings.
- Do NOT skip, weaken or delete a test to get CI green.
- Do NOT bypass `pit(as_of)` for research reads.

## Doc sync on completion

- `docs/18-platform-and-deployment.md` §4.3 and `docs/03-build-spec.md` §4: which ahead-creation path is in use.
- `docs/16-configuration-and-safety-model.md` §2.15: add `db.partitions_ahead_months` if it was introduced (report to the doc owner).
- `docs/roadmap/phase-0-foundations.md`: tick T0.22 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T072-monthly-bar-partitions-and-the-mt-store-partitio`
- PR title: `P0-T072: Monthly bar partitions and the mt-store partition job`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T072` run

## Progress log

- 2026-11-19 00:00 · aligner · created
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (new task: native monthly partitions replace TimescaleDB hypertables; pg_partman or the `mt-store` job; export-then-drop to Parquet)
