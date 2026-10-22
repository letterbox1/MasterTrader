---
id: P7-T021
kind: task
title: Memecoin sleeve kill criteria
phase: 7
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T020, P5-T036]
requirements: [R7.06]
roadmap_todos: [T7.21]
modules: [M11]
dashboards: [D06]
tools: [git, uv]
mcp: []
env: []
services: [postgres, nats]
branch: p7/P7-T021-kill-criteria-memecoin
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T021 · Memecoin sleeve kill criteria

## Goal / expected outcome

The memecoin sleeve has its four kill criteria implemented on the P7-T020 framework, so it can only scale while they hold.

## Context & references

- Roadmap: [R7.06 · ToDo T7.21](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) (memecoin kill: sleeve DD > 30%; negative expectancy after 200 live trades; rug rate among entries > 5%; any single loss > 1% of total equity) · [14 §3](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) (memecoin P2, paper ≥ 300 trades) · [14 §4](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) (memecoin sizing; 0.25–0.5% of total equity per trade, max position 2%, [16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown))
- Cross-phase: **P5-T036** (risk providers and hard-fail rules producing `token_risk_report`) supplies the rug label; it's a `depends_on` because this item needs that P5 deliverable ([17 §D P7-B011](../../../docs/17-decisions-register.md#d-other-decisions)). The memecoin sleeve can't be funded before this item is done; P1 sleeves don't wait for it. P2 memecoin template (paper-only).
- Related: P7-T020, P7-T048 (general kill suite; the memecoin cases are verified here because they wait on P5)

## Requirements

- Sleeve drawdown from peak > 30% → breach.
- After ≥ 200 live trades: mean R per trade (net of all costs) < 0 → breach.
- Rug rate: share of entries whose token is later flagged rugged (liquidity pulled / honeypot / > 90% drop in 1 h) > 5% over the last 100 entries → breach.
- Any single realised loss > 1% of **total** equity → breach immediately.
- Same breach actions as P7-T020.
- Thresholds (30% DD, 200 trades, 5% rug rate over 100 entries, 1% single loss) are sleeve/manifest settings with these defaults (14 §7); tightening C1, loosening C3.

## ToDo

- [ ] Four criteria in `packages/mt_risk/kill_criteria/memecoin.py`.
- [ ] Rug labeller consuming `token_risk_report` updates post-entry.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: each criterion at boundary values (30.0% vs 30.1%; 199 vs 200 trades; 5/100 vs 6/100; loss 0.99% vs 1.01%).
- Integration: injected rug labels breach the sleeve and halt only memecoin bots.
- Sim (`tests/sim/test_kill_memecoin.py`): the four criteria breached on paper venues with injected fills and rug labels; scope, alerts, WORM rows and C3 restart gating asserted (the memecoin half of R7.06's simulated breach).

### Scenarios
- Given one trade loses 1.2% of total equity, then the memecoin sleeve halts immediately even though sleeve DD is 8%.

### Stress / failure injection
- Rug labels arriving late (hours after exit): rate recomputed; a breach found late still halts and alerts.

## Acceptance criteria

- [ ] Four criteria implemented, tested at boundaries and breached in simulation.
- [ ] CI green.

## Exceptions & edge cases

- Memecoin sleeve not live (paper-only in P7 unless it passes its gate profile incl. ≥ 300 paper trades, 16 §2.4): criteria run in shadow.

## Cardinal rules (do NOT)

- Do NOT average down or widen memecoin limits to avoid a breach (14 §4).
- Do NOT add discretionary overrides; the only manual trading action outside HITL approvals is flatten-and-halt with a required reason (14 §4).
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §7: rug definition used.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.21 when this item is done.

## Branch & PR

- Branch: `p7/P7-T021-kill-criteria-memecoin`
- PR title: `P7-T021: Memecoin sleeve kill criteria`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T021` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (depends on P5-T036 rug labels per 17 §D P7-B011; memecoin simulated breaches moved here from P7-T048; settings per 14 §7/16 §2.1)
