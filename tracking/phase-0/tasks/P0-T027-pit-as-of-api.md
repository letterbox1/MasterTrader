---
id: P0-T027
kind: task
title: Implement pit(as_of) in the mt-store crate and the Parquet catalog helpers
phase: 0
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T024, P0-T016]
requirements: [R0.04]
roadmap_todos: [T0.22]
modules: [mt-store]
dashboards: []
tools: [git, cargo, supabase]
mcp: []
env: []
services: [supabase-postgres]
branch: p0/P0-T027-pit-as-of-api
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T027 · Implement pit(as_of) in the mt-store crate and the Parquet catalog helpers

## Goal / expected outcome

Research and backtests read facts only through `pit(as_of)`, implemented **once** in the Rust `mt-store` crate (Python calls the same code through the `mt_store` binding, P0-T071). It returns rows that were **known** at `as_of` (`ingest_time <= as_of`) and **happened** by then (`event_time <= as_of`), picking the latest version per key; it reads bars across Postgres monthly partitions and exported Parquet transparently, and derives non-standard bar sizes with `date_bin()` ([18 §4.3](../../../docs/18-platform-and-deployment.md#43-bars-without-timescaledb)). Parquet catalog helpers expose the same contract for raw ticks/L2.

## Context & references

- [Roadmap P0 R0.04](../../../docs/roadmap/phase-0-foundations.md#3-requirements) · [T0.22](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-store` row) · [18 §4.3–4.4](../../../docs/18-platform-and-deployment.md#44-point-in-time-and-worm)
- [SPEC non-negotiables](../../../SPEC.md#non-negotiable-requirements) (NN1)
- [03 §4 data model](../../../docs/03-build-spec.md#4-data-model-overview) (point-in-time rule) · [02 §5.2 key conventions](../../../docs/02-v1-architecture.md#52-key-conventions)
- Python binding: P0-T071 · Bypass guard: P0-T028 · Partitions: P0-T072
- Depends on: P0-T024, P0-T016

## Requirements

- Rust API: `mt_store::pit(as_of: OffsetDateTime, clock: &dyn Clock) -> PitReader`; `PitReader::table(name).columns(..).filter(..).latest_by(key)` builds a query applying `event_time <= $as_of AND ingest_time <= $as_of` and, when `latest_by` is given, `DISTINCT ON (key) ORDER BY key, ingest_time DESC` (latest known version); results stream as Arrow record batches (`arrow-rs`) or typed rows (`mt-core` types). Queries use sqlx with compile-time checks where static.
- `bars(instrument, spec, range)`: standard sizes read from `market.bar*`; any other size uses `date_bin()` over 1m (or 1s) bars at read time; older bars come from Parquet when the partition was exported (P0-T072), with the same results.
- Optional `revisions(As::Known | As::Latest)`: research defaults to `As::Known`; `Latest` requires an explicit flag and is logged (ops use only).
- SQL side: `SECURITY DEFINER` functions/views per fact table in a `pit` helper schema (owned by `mt_owner`, created by migrations in `supabase/migrations/`) that `mt_research_ro` can execute; direct table `SELECT` is not granted (defence in depth with P0-T028). RLS stays deny-all for Supabase roles.
- Parquet: `mt_store::catalog::pit_scan(dataset, as_of)` reads the Nautilus `ParquetDataCatalog` layout (DataFusion or DuckDB via its Rust crate) with the same predicates on `ts_event`/`ts_init`.
- `as_of` must be UTC; `as_of` in the future errors unless `clock` is a `SimClock`.
- Every call is counted (`mt_store_pit_queries_total{table}`) for later audit.

## ToDo

- [ ] Implement `mt_store::pit` (SQL) and `mt_store::catalog` (Parquet).
- [ ] Migration: the `pit` helper schema + per-table function generator used by later migrations (`mt_create_fact_table(..., pit => true)`).
- [ ] `date_bin()` path for non-standard bar sizes; transparent Parquet fallback for exported partitions.
- [ ] Golden fixtures (a macro value revised twice; bars across a partition boundary) shared with the Python binding tests (P0-T071).
- [ ] Document the API with examples in the crate README.

## Verification

### Tests
- Golden (`cargo test -p mt-store pit`): fixture series with revisions → `pit(as_of)` returns the vintage known at each date (ALFRED-style).
- Property (`proptest`): for random insert sequences, no returned row has `ingest_time > as_of` or `event_time > as_of`.
- Bars: `date_bin` 7m bars equal a reference aggregation of 1m bars; results identical before and after a partition export (with P0-T072).
- Parquet: same golden on a small Parquet dataset.
- pgTAP (`supabase test db`): `mt_research_ro` can execute pit functions but can't `SELECT` fact tables.

### Scenarios
- Given a fact is ingested late (event 09:00, ingested 09:05), when reading `as_of=09:02`, then it is **not** returned.
- Given `revisions(As::Latest)` is used from research code, then the bypass check (P0-T028) flags it.

### Stress / failure injection
- Query cost: `pit` over 10 M fixture rows with an `(key, event_time, ingest_time)` index returns a 1-day slice in < 200 ms on the workstation (logged).

## Acceptance criteria

- [ ] `pit` SQL + Parquet readers implemented in Rust with golden + property tests
- [ ] `mt_research_ro` can read only via pit functions
- [ ] Non-standard bar sizes via `date_bin()`; exported partitions read transparently
- [ ] API documented
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, `supabase test db`, gitleaks, `pit` check)

## Exceptions & edge cases

- Clock skew between `event_time` from venues and our `ingest_time`: predicates use both; skew itself is monitored by M16 (P1).
- No bar data exists before P1; bar tests use fixtures.

## Cardinal rules (do NOT)

- Do NOT add a 'fast path' that reads fact tables directly for research code.
- Do NOT default `revisions` to `Latest`.
- Do NOT write a second `pit` implementation in Python; Python uses the binding (P0-T071).
- Do NOT use TimescaleDB functions (`time_bucket`); use `date_bin()`.
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/03-build-spec.md` §4: document the `pit` API signature and the `as_known` default.
- `docs/roadmap/phase-0-foundations.md`: tick T0.22 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T027-pit-as-of-api`
- PR title: `P0-T027: Implement pit(as_of) in the mt-store crate and the Parquet catalog helpers`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T027` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (no decision changes; run fields added)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (`pit` implemented once in the Rust `mt-store` crate (sqlx, Arrow), Python via P0-T071; `date_bin()` and Parquet fallback replace TimescaleDB; pit functions created by Supabase migrations)
