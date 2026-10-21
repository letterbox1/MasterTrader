---
id: P2-T131
kind: task
title: MasterTradingBot sizing/risk library (vol targeting, caps, correlation buckets)
phase: 2
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T130]
requirements: [R2.48]
roadmap_todos: [T2.31]
modules: [M0, M11]
dashboards: []
branch: p2/P2-T131-mtb-sizing-risk-library
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

# P2-T131 · MasterTradingBot sizing/risk library (vol targeting, caps, correlation buckets)

## Goal / expected outcome

A pure sizing/risk helper library in `mt_strategy.lib.sizing` (vol targeting, stop-distance units, per-asset caps, correlation buckets) that MasterTradingBot-derived strategies use to propose sizes, while M11 remains the authority that checks and can cut them.

## Context & references

- Roadmap: [R2.48](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.31
- [14 §8](../../../docs/14-strategy-evidence-and-validation.md#8-mastertradingbot-integration) · [14 §4 sizing](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) (vol targeting first; `units = capital × risk% ÷ |entry − stop|`; 15–20% annualised for trend from 30–60d realised vol)
- M11 sizing models and limits are part A (T2.22, R2.12/R2.14 in part A (P2-T001–T099)); this library must not duplicate their enforcement and should be importable by M11 if it chooses

## Requirements

- `vol_target_units(capital, target_ann_vol, realised_vol, price, contract_size)`; `stop_distance_units(capital, risk_pct, entry, stop)`; `cap_units(units, max_pct_of_sleeve, price, sleeve_equity)`.
- Correlation buckets: group instruments by rolling 60d correlation > 0.7 (configurable) and cap bucket gross exposure.
- Lot rounding to venue lot size/step (MT5 lots, crypto step size) — never round up past a cap.
- No Kelly here (M11 owns Kelly with quarter-Kelly ceiling, never stacked on vol targeting).
- Golden tests against MasterTradingBot historical position sizes where provided (T2.04).

## ToDo

- [ ] Implement `packages/mt_strategy/lib/sizing.py`
- [ ] Golden + unit tests
- [ ] Doc how M11 interacts (proposal vs enforcement)

## Verification

### Tests
- Unit: stop-distance formula on worked examples; rounding never exceeds caps.
- Golden: MTB historical sizes reproduced (when T2.04 data present).

### Scenarios
- Given a proposed size above M11's max-position limit, then M11 rejects/cuts it (library proposes, M11 decides) — covered by an integration test with part A's API.

### Stress / failure injection
- n/a: pure arithmetic.

## Acceptance criteria

- [ ] Formulas match 14 §4
- [ ] Never rounds past caps
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Realised vol = 0 or NaN (new instrument): size 0 with reason, never infinite.

## Cardinal rules (do NOT)

- Do NOT implement Kelly or stack Kelly on vol targeting here.
- Do NOT treat library output as approval; every order still goes through M11.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §8: sizing library contents.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.31 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T131-mtb-sizing-risk-library`
- PR title: `P2-T131: MasterTradingBot sizing/risk library (vol targeting, caps, correlation buckets)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T131` run

## Progress log

- 2026-10-21 00:00 · planner · created
