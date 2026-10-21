---
id: P1-T061
kind: task
title: Verify flow F1 end to end across all asset classes
phase: 1
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T011, P1-T015, P1-T016, P1-T017, P1-T021, P1-T023, P1-T024, P1-T050, P1-T030, P1-T054]
requirements: [R1.01, R1.02, R1.04, R1.05, R1.06, R1.15]
roadmap_todos: []
modules: [M1, M16, M15]
dashboards: [D02, D07]
branch: p1/P1-T061-verify-f1-end-to-end-all-asset-classes
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/02-v1-architecture.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T061 · Verify flow F1 end to end across all asset classes

## Goal / expected outcome

A scripted walk-through proves F1 for every asset class: venue → `md.*` → Parquet → bars → CAGGs → `dq.status` → D02/Grafana at every timeframe from ticks to 1D (crypto, FX/metals, ETFs live; futures and macro daily).

## Context & references

- Roadmap: requirements [R1.01](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.02](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.04](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.05](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.06](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.15](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements)
- Flow: [02 §8 F1](../../../docs/02-v1-architecture.md#8-end-to-end-flows) F1 · exit criterion 1 ([phase 1 §6 exit criteria](../../../docs/roadmap/phase-1-data-and-monitoring.md#6-exit-criteria-demo))
- Depends on (this phase): P1-T011, P1-T015, P1-T016, P1-T017, P1-T021, P1-T023, P1-T024, P1-T050, P1-T030, P1-T054

## Requirements

- Script `tests/e2e/f1_flow.py` that, per asset class instrument, asserts: live `md.*` within the last minute (in session), recorder file for today, 1s/1m bars, every CAGG level, `dq.status ok`, `/markets/{id}/bars` for each spec, D02 chart renders (Playwright)
- Futures and macro: daily bars/obs present and shown on D02 at 1D
- Grafana Markets board shows the same last price (± one bar) as D02
- Report with screenshots per class under `reports/verify/P1-T061/`

## ToDo

- [ ] Write the e2e script and Playwright captures
- [ ] Run during overlapping market hours (US + crypto + FX) and store the report
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- E2E suite as described; part of the exit demo

### Scenarios

- Given one instrument per class, when the script runs, then every assertion passes or the report names the exact missing step

### Stress / failure injection

- n/a: functional end-to-end; load is P1-T062

## Acceptance criteria

- [ ] All classes pass every F1 step; report stored
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Run outside US hours: ETF live step is skipped with reason and re-run in hours before sign-off

## Cardinal rules (do NOT)

- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: no ToDo box of its own; note P1-T061 as evidence under the requirements it verifies (R1.01, R1.02, R1.04, R1.05, R1.06, R1.15).
- `docs/02-v1-architecture.md` §8: note F1 verified and link the report

## Branch & PR

- Branch: `p1/P1-T061-verify-f1-end-to-end-all-asset-classes`
- PR title: `P1-T061: Verify flow F1 end to end across all asset classes`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T061` run

## Progress log

- 2026-10-21 00:00 · planner · created
