---
id: P1-T037
kind: task
title: Run nightly Pandera validation and Evidently drift reports
phase: 1
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T012, P1-T030]
requirements: [R1.10]
roadmap_todos: [T1.27]
modules: [M16]
dashboards: [D07]
branch: p1/P1-T037-dq-nightly-pandera-evidently
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

# P1-T037 · Run nightly Pandera validation and Evidently drift reports

## Goal / expected outcome

Each night, yesterday's compacted Parquet files are validated with Pandera schemas and Evidently drift reports compare return/spread/volume distributions against a reference window; failures become DQ incidents and reports are linked from D07.

## Context & references

- Roadmap: requirements [R1.10](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.27](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (DQ checks table) · flow [02 §8 F1](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 5 · subjects [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) · degraded modes [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) · UI [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) Quality tab (Batch: nightly Pandera validation of Parquet; Evidently drift reports)
- Depends on (this phase): P1-T012, P1-T030

## Requirements

- Pandera schemas per data type (trades, quotes, L2 deltas, bars): types, non-null, price > 0, monotonic `event_time` within file, `ingest_time ≥ event_time − skew`, provenance present
- Evidently report per instrument: log returns, spread bps, volume, inter-arrival vs trailing 30-day reference; drift flagged with the report URL stored
- Runs after compaction (P1-T012) in Prefect; results to `audit.dq_event` (check `batch_schema` / `batch_drift`) and HTML reports under `/data/reports/dq/<date>/`

## ToDo

- [ ] Write schemas and the flow
- [ ] Report storage and D07 links (`/data/dq-events` includes report path)
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: each schema rejects a crafted bad frame (negative price, null ts, unsorted)
- Integration: flow over a fixture day produces pass + one injected failure

### Scenarios

- Given a compaction run is late, when the nightly flow starts, then it waits for the compaction marker rather than validating fragments

### Stress / failure injection

- Load: one day of 10-symbol L2 data validated within 30 min on the target host

## Acceptance criteria

- [ ] Nightly results visible in D07 Quality; injected failures produce incidents
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Drift is information, not automatically `bad`; only schema failures change status

## Cardinal rules (do NOT)

- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT let any path loosen DQ thresholds, risk or alert routing without C3 (Telegram + TOTP + cool-down); tightening is C1.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.27 once every task traced to it in PHASE.md is done; note P1-T037 next to it.
- `docs/03-build-spec.md` §M16: link schema module and report location

## Branch & PR

- Branch: `p1/P1-T037-dq-nightly-pandera-evidently`
- PR title: `P1-T037: Run nightly Pandera validation and Evidently drift reports`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T037` run

## Progress log

- 2026-10-21 00:00 · planner · created
