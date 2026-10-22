---
id: P2-T102
kind: task
title: Measured cost model loader from M16 snapshots
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T101, P1-T038, P1-T039, P1-T040]
requirements: [R2.40, R2.41, R2.42]
roadmap_todos: [T2.27]
modules: [M7, M16]
dashboards: [D04]
tools: [uv]
mcp: []
env: []
services: [postgres]
branch: p2/P2-T102-measured-cost-model
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T102 · Measured cost model loader from M16 snapshots

## Goal / expected outcome

A `mt_lab.costs.CostModel` built from a named, immutable M16 cost snapshot (fees by tier, spread by instrument × hour-of-week, size-dependent slippage/impact, latency, funding/swap) that both backtest engines use, with cost multipliers for stress tests and a refresh path for realised TCA from paper fills.

## Context & references

- Roadmap: [R2.40–R2.42](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.27
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (`market.spread_*`, `audit.cost_event`, `cost.{venue}.{symbol}`) · [14 §4 costs](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) (re-measured monthly) · [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) (no fixed-bps slippage for illiquid assets)
- Cross-phase (`depends_on`): P1 cost service (T1.28): fees/tiers (P1-T038), funding/swap (P1-T039), spreads by hour-of-week (P1-T040). Realised TCA comes from P2-T029 (T2.26) for the monthly refresh (not a precondition for the first snapshot).
- D04 'Cost model' field and Costs tab: [D04](../../../docs/ui/dashboards/D04-research-lab.md)

## Requirements

- Snapshot = frozen set of cost series read via `pit(as_of)` with an id + content hash; `/data/costs?snapshot=` returns it; every backtest row stores `cost_snapshot_id`.
- Components: maker/taker fee by venue tier, spread_bps by instrument × hour-of-week, impact as a function of order size vs book depth / 1-min volume (from L2 where recorded), latency distribution, funding (perps, realised history) and swap/financing (FX/CFD).
- Illiquid instruments (no L2 / thin volume) must use the depth/volume impact curve, never a fixed-bps slippage (14 §6).
- `CostModel.scaled(k)` for k ∈ {0.5, 1, 2, 3} drives sensitivity and 2×/3× cost stress.
- Custom override (D04 'custom fees/slippage/latency/funding') is allowed but flags the run `cost_source=custom`; a zero-cost run gets `unrealistic_costs=true`.
- Realised-vs-modelled: ingest paper TCA ratios (from part A T2.26) monthly into a new snapshot; never mutate an old snapshot.

## ToDo

- [ ] Implement `mt_lab/costs.py`: `CostSnapshot` loader (pit), `CostModel` with fee/spread/impact/latency/funding/swap components
- [ ] Implement impact curve fitting from recorded L2 depth and 1-min volume; fallback order when data is missing (instrument → asset-class median → refuse)
- [ ] Implement `scaled(k)`, custom override and `unrealistic_costs` flag
- [ ] Prefect flow `lab-cost-snapshot-monthly` creating a new snapshot incl. realised TCA ratios
- [ ] Adapters exposing the model to the screener (per-trade cost function) and to Nautilus (`FeeModel`, `FillModel`, latency model)
- [ ] Tests and docs

## Verification

### Tests
- Unit: fee/spread lookup by hour-of-week; impact monotonic in size; `scaled(3)` triples every component; zero-cost flag.
- Golden: a fixed snapshot fixture produces byte-identical cost totals for a fixed trade list.
- Integration: snapshot built from P1 cost tables via `pit(as_of)`; `ingest_time > as_of` rows excluded.

### Scenarios
- Given an instrument without L2, when a 5% of 1-min volume order is costed, then impact comes from the volume curve, not a fixed bps.
- Given no cost data for an instrument at all, when a truth backtest is requested, then the job fails with 'no measured costs' instead of assuming zero.
- Given a new monthly snapshot, when an old backtest is re-run, then it still uses its original snapshot id.

### Stress / failure injection
- Load a snapshot covering 50 instruments × 2 years of hour-of-week spreads in < 5 s; memory < 1 GB.
- Corrupt one cost row (NaN): loader rejects the snapshot with a clear error, D04 shows it.

## Acceptance criteria

- [ ] Every backtest row carries a `cost_snapshot_id`; screener and truth use the same model
- [ ] Zero/custom costs flagged; missing costs fail loudly
- [ ] Monthly snapshot flow scheduled in Prefect
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Funding history gaps: forward-fill at most one funding interval, else mark the period cost-unknown and fail truth runs over it.
- Venue fee-tier change mid-range: use the tier valid at each trade's event_time.
- Snapshots are immutable; corrections create a new snapshot id.

## Cardinal rules (do NOT)

- Do NOT default to zero or fixed-bps costs silently; costs are measured or the run is flagged/failed.
- Do NOT read research/backtest data except through `mt_store.pit(as_of=…)`; the `pit` CI bypass test must stay green.
- Do NOT add paid data/APIs or services; free tiers and self-hosted components only (03 §1).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M7/M16: cost snapshot contract and monthly refresh.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.27 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T102-measured-cost-model`
- PR title: `P2-T102: Measured cost model loader from M16 snapshots`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T102` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (cross-phase cost-service deps)
