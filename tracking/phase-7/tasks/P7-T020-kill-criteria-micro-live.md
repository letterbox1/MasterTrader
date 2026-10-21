---
id: P7-T020
kind: task
title: Kill-criteria evaluators: implementation shortfall and 60-trade Sharpe
phase: 7
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T017]
requirements: [R7.06]
roadmap_todos: [T7.21]
modules: [M11, M16]
dashboards: [D06, D03]
branch: p7/P7-T020-kill-criteria-micro-live
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/03-build-spec.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T020 · Kill-criteria evaluators: implementation shortfall and 60-trade Sharpe

## Goal / expected outcome

A kill-criteria framework in M11 evaluates each live sleeve's written kill criteria continuously and halts the sleeve (cancel orders, close per sleeve rule, alert, capital state → halted) on breach; this task adds the framework plus the two micro-live criteria.

## Context & references

- Roadmap: [R7.06 · ToDo T7.21](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) (kill if live implementation shortfall > 2× modelled; live Sharpe after 60 trades < backtest 5th percentile) · [14 §5](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) (kill criteria written before deployment, stored in the manifest; fallback ladder rung 5) · [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (TCA)
- Cross-phase: P2 T2.04/T2.05 manifests with kill criteria; P2 T2.26 TCA.
- Related: P7-T017 (reference p5), P7-T021, P7-T022, P7-T027, P7-T048 (simulated breaches), gap P7-B006 (alert vs kill ambiguity)

## Requirements

- Framework: `KillCriterion` interface (scope: sleeve | system; evaluate(state) → ok/warn/breach + evidence); criteria loaded from the manifest + policy defaults; a manifest can only **tighten** defaults.
- Shortfall: rolling implementation shortfall (bps, from M16 TCA) over the last 20 live fills or 7 days (whichever larger) > 2.0× the modelled shortfall → breach; > 1.5× → warn.
- Sharpe: once ≥ 60 live trades, rolling 60-trade Sharpe < reference p5 (P7-T017) → breach.
- Breach action: rung 5 — halt sleeve, cancel open orders, close per the sleeve rule, alert critical (Telegram + ntfy + email), capital state → halted, bots → paused; restart only via C3 after a written reason.
- Evaluation on every fill and every 5 min; breach → halt latency < 5 s; every evaluation result stored in `risk.kill_eval` (WORM, sampled: all warn/breach + hourly ok).

## ToDo

- [ ] `packages/mt_risk/kill_criteria/` framework + two criteria.
- [ ] Migration `risk.kill_eval` (WORM); NATS `risk.event` type `kill_criterion`.
- [ ] Restart command `risk.sleeve.restart` (C3, reason required).
- [ ] D06 kill-criteria panel per sleeve (status, value, threshold, last eval).
- [ ] Tests; docs.

## Verification

### Tests
- Unit: thresholds at 1.99× (ok), 2.01× (breach); 59 trades (n/a), 60 trades below p5 (breach).
- Integration: injected breach halts only that sleeve within 5 s; other sleeves continue.
- Property: a manifest cannot loosen a default threshold.

### Scenarios
- Given live shortfall is 2.3× modelled, then the sleeve halts, open orders cancel and a critical alert names the criterion and values.
- Given a halted sleeve, when you try `strategy.resume`, then it is refused until `risk.sleeve.restart` (C3) with a reason.

### Stress / failure injection
- Fill burst of 500 fills/min on one sleeve: evaluation keeps up (< 5 s lag); TCA feed missing → criterion 'unknown' → warn and no capital steps (never silently ok).

## Acceptance criteria

- [ ] Framework + two criteria live; breaches halt the right sleeve.
- [ ] Restart needs C3 with reason; all evaluations auditable.
- [ ] CI green.

## Exceptions & edge cases

- Shortfall on very few fills: minimum 20 fills before breach (warn allowed earlier).
- Paper sleeves: criteria evaluated in shadow (alerts only) so P7-T048 can simulate.

## Cardinal rules (do NOT)

- Do NOT auto-restart a halted sleeve.
- Do NOT let a kill criterion wait for approval to act.
- Do NOT add discretionary overrides; the only manual action outside approve mode is flatten-and-halt with a required reason (14 §4).
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §7: evaluation windows and actions.
- `docs/03-build-spec.md` M11: kill-criteria framework.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.21 when this item is done.

## Branch & PR

- Branch: `p7/P7-T020-kill-criteria-micro-live`
- PR title: `P7-T020: Kill-criteria evaluators: implementation shortfall and 60-trade Sharpe`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T020` run

## Progress log

- 2026-10-21 00:00 · planner · created
