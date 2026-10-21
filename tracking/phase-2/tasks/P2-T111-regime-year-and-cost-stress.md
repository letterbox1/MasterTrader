---
id: P2-T111
kind: task
title: Per-year, per-regime, 2×/3× cost stress and benchmark checks
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T102, P2-T106]
requirements: [R2.42]
roadmap_todos: [T2.27]
modules: [M7, M6]
dashboards: [D04, D03]
branch: p2/P2-T111-regime-year-and-cost-stress
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T111 · Per-year, per-regime, 2×/3× cost stress and benchmark checks

## Goal / expected outcome

The harness extensions from 14 §6: results broken down by calendar year and by regime (bull/bear/chop) across several assets, re-run at 2× and 3× measured costs, stress windows replayed, and compared with the asset-class passive benchmark after costs.

## Context & references

- Roadmap: [R2.42](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.27
- [14 §6 gates 4–6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [03 §8 item 7](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) · [14 §3 stress-testing](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) (May 2022, Nov 2022, Aug 2024, Feb–Mar 2026)
- Regime definition is unspecified in the docs: P2-B055; this task implements the price-based default proposed there
- Cost multipliers via `CostModel.scaled(k)` (P2-T102); benchmarks via P2-T106

## Requirements

- Per-year table: return, Sharpe, max DD, trades per calendar year (UTC); pass = profitable in each year.
- Regime labeller (deterministic, price-based, per asset): bull = close above 200-day MA and 90-day return > +10%; bear = below 200-day MA and 90-day return < −10%; chop = otherwise; versioned as `regime_v1` in `features.def` (M6).
- Per-regime table across all traded assets; single-regime edges labelled `regime_only=<label>` instead of failing outright (14 §6 gate 4).
- Cost stress: re-run truth at 2× and 3× costs; pass = net return > 0 and Sharpe > 0 at both; sensitivity at 0.5×/1× also stored for D04.
- Named stress windows replayed and reported separately (May 2022, Nov 2022, Aug 2024, Feb–Mar 2026) where data exists.
- Benchmark gate: excess return after costs > 0 over the evaluation window.

## ToDo

- [ ] Implement `regime_v1` labeller in `mt_features` (registered + versioned) and tests
- [ ] Implement per-year/per-regime breakdown in `mt_lab/validation/breakdown.py`
- [ ] Implement cost-stress sub-jobs (2×, 3×, plus 0.5×/1× sensitivity) and stress-window replays
- [ ] Benchmark comparison output
- [ ] Doc regime definition in 14 §6

## Verification

### Tests
- Unit: regime labeller on a synthetic up/down/flat series labels each segment correctly.
- Integration: a strategy with 2× cost-break-even fails the 3× stress and passes 1×.
- Golden: per-year table for a fixture.

### Scenarios
- Given a trend strategy profitable overall but losing in 2022, then the per-year check fails and names 2022.
- Given a carry strategy that only earns in bull regimes, then it is labelled `regime_only=bull` and the D03 gate shows that label.
- Given no data for the Feb–Mar 2026 window, then that stress window shows 'no data' (not pass).

### Stress / failure injection
- Cost-stress fan-out (4 multipliers × 3 assets) runs in parallel within the worker cap; one failing sub-job fails the section, not silently.

## Acceptance criteria

- [ ] Per-year, per-regime, cost stress (2×, 3×) and benchmark sections produced
- [ ] `regime_v1` registered and versioned
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Partial first/last years flagged 'partial' and reported but judged on available months only if ≥ 3 months.
- Assets with < 200 days of history: regime 'unknown'; excluded from regime judgement with a note.

## Cardinal rules (do NOT)

- Do NOT tune the regime definition per strategy to make it pass; it is a versioned global feature.
- Do NOT read research/backtest data except through `mt_store.pit(as_of=…)`; the `pit` CI bypass test must stay green.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §6: `regime_v1` definition and stress windows.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.27 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T111-regime-year-and-cost-stress`
- PR title: `P2-T111: Per-year, per-regime, 2×/3× cost stress and benchmark checks`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T111` run

## Progress log

- 2026-10-21 00:00 · planner · created
