---
id: P1-T058
kind: task
title: Verify bar parity between the partitioned bar tables and Parquet ticks
phase: 1
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T012, P1-T013, P1-T014, P1-T076]
requirements: [R1.02]
roadmap_todos: [T1.62]
modules: [M1]
dashboards: []
tools: [git, uv, cargo, docker]
mcp: []
env: []
services: [supabase-postgres]
branch: p1/P1-T058-verify-bar-parity
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
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

# P1-T058 · Verify bar parity between the partitioned bar tables and Parquet ticks

## Goal / expected outcome

For a sample day, bars rebuilt independently from Parquet ticks equal the bars `mt-recorder` wrote at every standard size (1s … 1W) into the monthly partitions; after a seeded backfill the rollup job's (P1-T076) output matches too; and vendor klines (data.binance.vision) agree within a documented tolerance.

## Context & references

- Roadmap: requirements [R1.02](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.62](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Roadmap T1.62 · [02 §8 F1](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 4 · [18 §4.3](../../../docs/18-platform-and-deployment.md#43-bars-without-timescaledb)
- Depends on (this phase): P1-T012, P1-T013, P1-T014

## Requirements

- Script `mt_research.verify.bar_parity --date --instrument` (in `packages/mt_research`; Python + DuckDB on purpose, an independent re-implementation in another language so it can't share a bug with the Rust builder; reads Parquet and bars only through the `mt_store` `pit` binding, [18 §2.2](../../../docs/18-platform-and-deployment.md#22-python-uv-workspace-packages-only-where-absolutely-required)) rebuilding 1s/1m/5m/15m/1h/4h/1D/1W from Parquet trades and comparing with `market.bar_*` in Supabase Postgres (exact on OHLC and volume, Decimal)
- Rollup check: seed a backfill of a past day (the P1-T015 `mt-connectors` job on fixtures), run the rollup job (P1-T076), then run the same parity on that day
- Compare our 1s bars to data.binance.vision 1s klines (`market.bar_1s_vendor`) for the same day: report mismatched seconds (expect only at disconnect edges)
- Run for ≥ 3 instruments across 2 venues and 1 FX (mid bars from quotes)

## ToDo

- [ ] Write the script and a CI job on a fixture day
- [ ] Run on a real recorded day and store the report under `reports/verify/P1-T058/`
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- CI (`uv run pytest packages/mt_research -k bar_parity`): fixture day passes exactly, including the seeded-backfill rollup day; an injected one-tick difference is caught

### Scenarios

- Given a recorder gap of 30 s, when parity runs, then the report attributes the mismatched seconds to the gap incident, not to the builder

### Stress / failure injection

- n/a: verification run

## Acceptance criteria

- [ ] Exact parity on a real day for all sampled instruments (or every difference explained by a logged gap); report stored
- [ ] CI green (`cargo clippy`, `cargo test`, ruff, mypy, `uv run pytest`, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Late trades corrected by the rollup job: run parity after the late-data window and any queued rollups have finished

## Cardinal rules (do NOT)

- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)` (`mt-store`, also through its Python binding); research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.62 once every task traced to it in PHASE.md is done; note P1-T058 next to it.
- `docs/03-build-spec.md` §M1: link the parity report

## Branch & PR

- Branch: `p1/P1-T058-verify-bar-parity`
- PR title: `P1-T058: Verify bar parity between the partitioned bar tables and Parquet ticks`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T058` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (parity covers every aggregate up to 1W; vendor klines table)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (parity against the partitioned bar tables (no Timescale/CAGGs), plus a rollup check after a seeded backfill (new dep P1-T076); title updated; services supabase-postgres)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (the independent parity checker stays Python on purpose but lives in `mt_research` (one of the allowed Python packages) and reads through the `pit` binding; backfill seeded by the Rust `mt-connectors` job)
