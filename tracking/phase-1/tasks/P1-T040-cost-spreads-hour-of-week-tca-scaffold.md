---
id: P1-T040
kind: task
title: Measure spreads by hour-of-week and scaffold TCA
phase: 1
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T038, P1-T013]
requirements: [R1.11]
roadmap_todos: [T1.28]
modules: [M16]
dashboards: [D07, D02]
tools: [git, uv, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p1/P1-T040-cost-spreads-hour-of-week-tca-scaffold
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
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

# P1-T040 · Measure spreads by hour-of-week and scaffold TCA

## Goal / expected outcome

`spread_bps` is aggregated per instrument × hour-of-week with a "normal" baseline, spread blow-outs raise incidents, and TCA tables and interfaces exist for P2 to fill with paper fills.

## Context & references

- Roadmap: requirements [R1.11](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.28](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (Spreads by instrument × hour-of-week; TCA implementation shortfall; M11 told to pause on spread > 3× normal, default) · UI [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) Costs heatmap, alert at spread > 3× normal
- Defaults: [16 §2.2](../../../docs/16-configuration-and-safety-model.md#22-data-freshness-what-stale-means) wide spread > 3× normal → pause the affected bots; [16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown) cost blow-out realised ÷ modelled > 1.5× over the last 20 fills → pause the bot (P2 applies both via M11)
- Canonical audit names ([17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)): TCA results go to `audit.cost_event`; there is no `audit.tca` table
- P2 continues: R2.34 TCA per order ([P2 roadmap](../../../docs/roadmap/phase-2-strategies-risk-lab.md))
- Depends on (this phase): P1-T038, P1-T013

## Requirements

- Continuous aggregate `market.spread_how` (instrument, hour_of_week 0–167, p50/p90 spread bps, samples) from quotes, refreshed hourly; trailing 4-week baseline
- Live check: current spread > 3× baseline p50 (default multiple, configurable) for ≥ 10 s (default) → `audit.cost_event` incident + `alert.warning.spread`; payload includes the ratio so P2's M11 can pause the affected bots
- `cost.{venue}.{symbol}` snapshot at ≤ 1 Hz: spread_bps, normal_bps, ratio, fee tier, funding/swap
- TCA scaffold: per-order TCA results are WORM rows in `audit.cost_event` (`kind=tca`: order, decision/arrival price, fill VWAP, fees, funding, delay/spread-impact/fee components); `market.cost_model` holds the rolling realised-vs-modelled ratio per strategy × venue × instrument (last 20 fills by default, for the 1.5× blow-out rule); interface `mt_monitor.tca.compute(order, fills)` with tests on synthetic fills

## ToDo

- [ ] Implement spread aggregation and the blow-out check
- [ ] Implement the cost snapshot publisher at ≤ 1 Hz
- [ ] Add the `kind=tca` payload to `audit.cost_event`, create `market.cost_model`, and the compute function with synthetic tests
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: hour-of-week bucketing in UTC; TCA decomposition sums to total shortfall (property)
- Integration: quotes fixture → heatmap rows; injected spread blow-out → incident
- WORM: `audit.cost_event` TCA rows pass the 15 §2.4 tests

### Scenarios

- Given a weekend with thin crypto books, when spreads widen, then the baseline for that hour-of-week already reflects it and no false incident fires

### Stress / failure injection

- Load: one month of quotes for 30 instruments aggregated within 5 min

## Acceptance criteria

- [ ] D07 Costs heatmap populated for every streaming instrument; spread incident fires on injection
- [ ] TCA compute passes synthetic tests (ready for P2-T2.26)
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Hour-of-week in UTC; the UI converts to local time (default Australia/Sydney)

## Cardinal rules (do NOT)

- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.28 once every task traced to it in PHASE.md is done; note P1-T040 next to it.
- `docs/03-build-spec.md` §M16: N = 3 default for spread blow-out; TCA table names

## Branch & PR

- Branch: `p1/P1-T040-cost-spreads-hour-of-week-tca-scaffold`
- PR title: `P1-T040: Measure spreads by hour-of-week and scaffold TCA`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T040` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (canonical names: TCA in audit.cost_event, no audit.tca (17 §B); spread 3× and cost blow-out 1.5× as 16 defaults)
