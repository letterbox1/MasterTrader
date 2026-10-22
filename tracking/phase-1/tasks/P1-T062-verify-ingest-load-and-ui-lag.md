---
id: P1-T062
kind: task
title: Stress ingest, recording and UI lag under burst load
phase: 1
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T047, P1-T050, P1-T012, P1-T013, P1-T031]
requirements: [R1.N2, R1.02, R1.N1, R1.17]
roadmap_todos: []
modules: [M1, M16, M15]
dashboards: [D02, D07]
tools: [git, uv, docker, pnpm, node>=20]
mcp: []
env: []
services: [nats, postgres, mt-api]
branch: p1/P1-T062-verify-ingest-load-and-ui-lag
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/02-v1-architecture.md]
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

# P1-T062 · Stress ingest, recording and UI lag under burst load

## Goal / expected outcome

Replaying a volatile market day at 10× through the live pipeline shows the recorder, bar builder, DQ monitor and UI keep up: no loss, stale reaction still ≤ 250 ms p99 after the data-age threshold, UI lag p95 < 500 ms with ≤ 4 Hz charts and ≤ 1 Hz tables.

## Context & references

- Roadmap: requirements [R1.N2](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.02](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.N1](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements)
- SLOs: [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos) · throttles [ui §3.4 real-time](../../../docs/ui/README.md#34-real-time) · R1.N1, R1.N2
- Depends on (this phase): P1-T047, P1-T050, P1-T012, P1-T013, P1-T031

## Requirements

- Replay tool `tools/replay/md_replay.py` publishing recorded `md.*` at N× speed into a staging NATS account
- Measure: recorder consumer lag, bar builder lag, DQ evaluation p99, stale detection with a feed killed mid-burst, WS fan-out rates, UI lag p95 via telemetry (3 browser clients incl. a phone profile)
- Pass thresholds: no dropped messages, consumer lag < 30 s, stale reaction ≤ 250 ms p99 after the threshold, UI lag p95 < 500 ms, chart ≤ 4 Hz, tables ≤ 1 Hz
- Report under `reports/verify/P1-T062/`

## ToDo

- [ ] Write the replay tool and the measurement harness
- [ ] Run 1×, 5× and 10× and store the report
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Harness assertions as listed; 1× run in nightly CI

### Scenarios

- Given 10× replay and a killed feed, when measured, then the stale reaction still meets ≤ 250 ms p99 after the threshold

### Stress / failure injection

- This task is the stress test (10× burst, killed feed during burst, 3 UI clients)

## Acceptance criteria

- [ ] All thresholds met at 10× (or the highest multiple that meets them recorded with the bottleneck named)
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Run on the target host, not a laptop; record hardware in the report

## Cardinal rules (do NOT)

- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: no ToDo box of its own; note P1-T062 as evidence under the requirements it verifies (R1.N2, R1.02, R1.N1).
- `docs/02-v1-architecture.md` §9.2: record measured headroom

## Branch & PR

- Branch: `p1/P1-T062-verify-ingest-load-and-ui-lag`
- PR title: `P1-T062: Stress ingest, recording and UI lag under burst load`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T062` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (stale SLO ≤ 250 ms p99 after the data-age threshold (P1-B001))
