---
id: P1-T058
kind: task
title: Verify bar parity between Timescale and Parquet ticks
phase: 1
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T012, P1-T013, P1-T014]
requirements: [R1.02]
roadmap_todos: [T1.62]
modules: [M1]
dashboards: []
branch: p1/P1-T058-verify-bar-parity
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T058 · Verify bar parity between Timescale and Parquet ticks

## Goal / expected outcome

For a sample day, bars rebuilt from Parquet ticks equal the Timescale 1s/1m bars and every continuous-aggregate level, and vendor klines (data.binance.vision) agree within a documented tolerance.

## Context & references

- Roadmap: requirements [R1.02](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.62](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Roadmap T1.62 · [02 §8 F1](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 4
- Depends on (this phase): P1-T012, P1-T013, P1-T014

## Requirements

- Script `tools/verify/bar_parity.py --date --instrument` rebuilding 1s/1m/5m/1h/1d from Parquet trades (DuckDB) and comparing with Timescale (exact on OHLC and volume, Decimal)
- Compare our 1s bars to data.binance.vision 1s klines for the same day: report mismatched seconds (expect only at disconnect edges)
- Run for ≥ 3 instruments across 2 venues and 1 FX (mid bars from quotes)

## ToDo

- [ ] Write the script and a CI job on a fixture day
- [ ] Run on a real recorded day and store the report under `reports/verify/P1-T058/`
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- CI: fixture day passes exactly; an injected one-tick difference is caught

### Scenarios

- Given a recorder gap of 30 s, when parity runs, then the report attributes the mismatched seconds to the gap incident, not to the builder

### Stress / failure injection

- n/a: verification run

## Acceptance criteria

- [ ] Exact parity on a real day for all sampled instruments (or every difference explained by a logged gap); report stored
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Late trades corrected after CAGG refresh: run parity after the refresh horizon

## Cardinal rules (do NOT)

- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.62 once every task traced to it in PHASE.md is done; note P1-T058 next to it.
- `docs/03-build-spec.md` §M1: link the parity report

## Branch & PR

- Branch: `p1/P1-T058-verify-bar-parity`
- PR title: `P1-T058: Verify bar parity between Timescale and Parquet ticks`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T058` run

## Progress log

- 2026-10-21 00:00 · planner · created
