---
id: P7-T013
kind: task
title: Gate report: paper/HITL tracking section and period clock
phase: 7
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T012, P2-T029]
requirements: [R7.02, R7.01]
roadmap_todos: [T7.20]
modules: [M7, M16, M18]
dashboards: [D03]
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, prefect-server, backtest-worker]
branch: p7/P7-T013-gate-report-paper-tracking
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

# P7-T013 · Gate report: paper/HITL tracking section and period clock

## Goal / expected outcome

The gate report includes a paper/HITL section per strategy version: elapsed period vs required, trade count, paper P&L and costs vs the backtest's expected range, and a pass/fail on 'within tolerance'.

## Context & references

- Roadmap: [R7.02, R7.01 · ToDo T7.20](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) item 5 (paper/HITL period, P&L and costs track the backtest) · [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) item 7 (≥ 8 weeks and ≥ 50 trades by default; P1 ≥ 8 weeks; memecoin ≥ 300 trades; low-frequency ≥ 26 weeks; live within expected range) · [16 §2.4](../../../docs/16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile) · [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (realised-vs-modelled cost ratio)
- Cross-phase: P2-T029 (TCA and measured costs, `depends_on`); reads P2-T180 (paper clock) and P3-T053 (journalled paper run).
- Related: P7-T012, P7-T015 (weekly review reuses these metrics), gap P7-B002 (resolved: 16 §2.4)

## Requirements

- Required period per bot, from its gate profile (16 §2.4 defaults): ≥ 8 weeks **and** ≥ 50 trades; class overrides: P1 sleeves ≥ 8 weeks; memecoin ≥ 300 trades; low-frequency bots that can't reach the trade count use ≥ 26 weeks. Tightening is free (C1); loosening is C3.
- Tracking error: annualised std of (paper daily return − backtest-replay daily return over the same window); tolerance default ≤ 1.5× the backtest's own daily-return std over walk-forward folds (configurable).
- Paper P&L within the backtest's bootstrap 5th–95th percentile band for the same number of trades/days (uses P7-T017 distributions).
- Costs: realised/modelled cost ratio ≤ 1.5 over the period (the cost blow-out default, 16 §2.1).
- Replays the backtest over the paper window with the same version and measured costs to compute expectation (Nautilus truth replay).

## ToDo

- [ ] `packages/mt_lab/gates/paper.py`: period clock, trade counter, replay-vs-paper comparison.
- [ ] Prefect flow `paper_replay_daily` that replays yesterday per paper strategy and stores `strategy.paper_tracking` rows.
- [ ] Expose results to the gate evaluator as gate `paper_tracking`.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: tracking error and band check on synthetic series; 300-trade counter for memecoin manifests.
- Integration: one week of recorded paper fills vs replay produces the expected tracking error (golden).
- Regression: a paper run with a 3-day outage gap is flagged and does not count those days.

### Scenarios
- Given paper costs are 1.8× modelled, then the paper gate fails with 'cost ratio 1.8 > 1.5'.
- Given a P1 sleeve at day 56 with P&L inside the band, then the paper gate passes.
- Given a memecoin manifest at 280 paper trades, then the gate shows 280/300.
- Given a low-frequency trend bot at 20 weeks with 18 trades, then the gate shows the 26-week window (20/26 weeks), not the trade count.

### Stress / failure injection
- Replay 10 strategies × 90 days on the backtest-worker overnight: < 2 h; a failed replay day marks the gate `incomplete`, never `pass`.

## Acceptance criteria

- [ ] Paper section present in the gate result with period, trades, TE, band and cost ratio.
- [ ] Defaults match the numbers above and are configurable (tighten C1, loosen C3).
- [ ] CI green.

## Exceptions & edge cases

- Venue paper/testnet fills unrealistic (testnet liquidity): flag the venue in the report; costs use M16 measured live costs for modelled values.
- DST/session changes for FX: daily cut at a fixed UTC time (14 §4).

## Cardinal rules (do NOT)

- Do NOT count days where the strategy was paused, halted or the feed was stale toward the paper period.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §6 item 7: state the tracking-error and band definitions used.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.20 when this item is done.

## Branch & PR

- Branch: `p7/P7-T013-gate-report-paper-tracking`
- PR title: `P7-T013: Gate report: paper/HITL tracking section and period clock`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T013` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (paper/HITL period per 16 §2.4 incl. ≥ 50 trades and the 26-week low-frequency window; cost ratio from 16 §2.1; deps)
