---
id: P0-T027
kind: task
title: Implement the mt_store.pit(as_of) API and Parquet catalog helpers
phase: 0
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T024]
requirements: [R0.04]
roadmap_todos: [T0.22]
modules: [mt_store]
dashboards: []
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [postgres]
branch: p0/P0-T027-pit-as-of-api
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T027 · Implement the mt_store.pit(as_of) API and Parquet catalog helpers

## Goal / expected outcome

Research and backtests read facts only through `mt_store.pit(as_of)`, which returns rows that were **known** at `as_of` (`ingest_time <= as_of`) and **happened** by then (`event_time <= as_of`), picking the latest version per key; Parquet catalog helpers expose the same contract for raw ticks/L2 via DuckDB.

## Context & references

- [Roadmap P0 R0.04](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.22](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [SPEC non-negotiables](../../../SPEC.md#non-negotiable-requirements) (NN1)
- [03 §4 data model](../../../docs/03-build-spec.md#4-data-model-overview) (point-in-time rule)
- [02 §5.2 key conventions](../../../docs/02-v1-architecture.md#52-key-conventions)
- Bypass test: P0-T028
- Depends on: P0-T024

## Requirements

- API: `pit(as_of: datetime, *, clock: Clock) -> PitReader`; `PitReader.table(name, columns=..., where=..., key=...)` returns a SQLAlchemy selectable/DataFrame (polars) applying `event_time <= :as_of AND ingest_time <= :as_of` and, when `key` is given, `DISTINCT ON (key) ORDER BY key, ingest_time DESC` (latest known version).
- Optional `revisions='as_known'|'latest'` — research defaults to `as_known`; `latest` requires an explicit flag and is logged (for ops use only).
- SQL side: `mt_store` creates `SECURITY DEFINER` functions/views per fact table in a `pit` helper schema (owned by `mt_owner`) that `mt_research_ro` can execute; direct table `SELECT` is not granted (defence in depth with P0-T028).
- Parquet: `mt_store.catalog.pit_scan(dataset, as_of)` wraps DuckDB/Nautilus `ParquetDataCatalog` paths with the same predicates on `ts_event`/`ts_init`.
- `as_of` must be tz-aware UTC; `as_of` in the future raises unless `clock` is a `SimClock`.
- Every call is counted (`mt_store_pit_queries_total{table}`) for later audit.

## ToDo

- [ ] Implement `mt_store.pit` (SQL) and `mt_store.catalog` (Parquet/DuckDB).
- [ ] Create the `pit` helper schema + per-table function generator used by future migrations (`create_fact_table(..., pit=True)`).
- [ ] Write tests with a fixture table holding revised facts (e.g. a macro value revised twice).
- [ ] Document the API with examples in the package README.

## Verification

### Tests
- Golden: fixture series with revisions → `pit(as_of)` returns the vintage known at each date (ALFRED-style).
- Property (hypothesis): for random insert sequences, no returned row has `ingest_time > as_of` or `event_time > as_of`.
- Parquet: same golden on a small Parquet dataset via DuckDB.

### Scenarios
- Given a fact is ingested late (event 09:00, ingested 09:05), when reading `as_of=09:02`, then it is **not** returned.
- Given `revisions='latest'` is used from `mt_lab`, then the bypass check (P0-T028) flags it.

### Stress / failure injection
- Query cost: `pit` over 10 M fixture rows with an `(key, event_time, ingest_time)` index returns a 1-day slice in < 200 ms on the host (logged).

## Acceptance criteria

- [ ] `pit` SQL + Parquet readers implemented with golden + property tests
- [ ] `mt_research_ro` can read only via pit functions
- [ ] API documented
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Clock skew between `event_time` from venues and our `ingest_time`: predicates use both; skew itself is monitored by M16 (P1).

## Cardinal rules (do NOT)

- Do NOT add a 'fast path' that reads fact tables directly for research code.
- Do NOT default `revisions` to `latest`.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/03-build-spec.md` §4: document the `pit` API signature and the `as_known` default.
- `docs/roadmap/phase-0-foundations.md`: tick T0.22 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T027-pit-as-of-api`
- PR title: `P0-T027: Implement the mt_store.pit(as_of) API and Parquet catalog helpers`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T027` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (no decision changes; run fields added)
