---
id: P7-T017
kind: task
title: Backtest reference distributions for live decay and kill checks
phase: 7
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T012]
requirements: [R7.07, R7.06, R7.01]
roadmap_todos: [T7.20, T7.22]
modules: [M7, M11]
dashboards: [D03]
tools: [git, uv]
mcp: []
env: []
services: [postgres, mlflow, backtest-worker]
branch: p7/P7-T017-backtest-reference-distributions
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

# P7-T017 · Backtest reference distributions for live decay and kill checks

## Goal / expected outcome

At gate-report time each strategy version stores frozen reference distributions (bootstrap of 60-trade Sharpe and hit rate, 26-week Sharpe and hit rate for low-frequency bots, 30-day Sharpe, max drawdown, per-trade implementation shortfall, weekly P&L band) so live monitors compare against the same numbers that justified promotion.

## Context & references

- Roadmap: [R7.07, R7.06, R7.01 · ToDo T7.20, T7.22](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) (decay: 60-trade Sharpe/hit rate vs 5th percentile, CUSUM) · [14 §5](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) (daily health check) · [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) (kill: live Sharpe after 60 trades < backtest 5th percentile; shortfall > 2× modelled) · [16 §2.5–2.6](../../../docs/16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each) (weekly P&L 5th–95th band for clean weeks; 26-week window for low-frequency bots)
- Related: P7-T020, P7-T023, P7-T024 (consumers), P7-T013 (paper band)

## Requirements

- Stationary block bootstrap (block length = mean holding period in trades, min 5) over OOS walk-forward trades; 10,000 resamples; seed recorded.
- Stored per version in `strategy.reference_dist` (WORM): metric, window (60 trades; 26 weeks for bots marked low-frequency; 1 week for the weekly P&L band), percentiles p1/p5/p10/p50/p90/p95, validated Sharpe, backtest max DD, modelled shortfall bps per venue.
- Recomputed only on a new strategy version; never altered for a running version.
- Deterministic given the seed; computation < 60 s per version.

## ToDo

- [ ] `packages/mt_lab/gates/reference.py` (bootstrap, percentiles).
- [ ] Migration `strategy.reference_dist` (WORM).
- [ ] Call from gate evaluation; expose `/strategies/{id}/reference`.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: bootstrap percentiles on a known normal series within tolerance; fixed seed → identical output.
- Property: p5 ≤ p50 ≤ p95; block length ≥ 5.

### Scenarios
- Given a version with 120 OOS trades, then 60-trade windows are bootstrapped and p5 Sharpe stored.
- Given a version with < 60 OOS trades, then the reference is marked `insufficient` and the gate report fails (P7-T012).

### Stress / failure injection
- 10 versions in parallel on the backtest-worker < 5 min.

## Acceptance criteria

- [ ] Reference distributions stored per version and immutable.
- [ ] Monitors read them via one API.
- [ ] CI green.

## Exceptions & edge cases

- Low-frequency bots (daily trend): the 26-week time window is stored alongside the 60-trade window (16 §2.4, §2.6; [17 §C P7-B016](../../../docs/17-decisions-register.md#c-defaults-that-were-n-or-unspecified)); a window without enough OOS data is stored `insufficient`, never extrapolated.

## Cardinal rules (do NOT)

- Do NOT recompute references for a live version to make live results 'fit'.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §6: document the bootstrap method.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.20, T7.22 when this item is done.

## Branch & PR

- Branch: `p7/P7-T017-backtest-reference-distributions`
- PR title: `P7-T017: Backtest reference distributions for live decay and kill checks`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T017` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (26-week low-frequency window and weekly P&L band per 16 §2.5–2.6 (P7-B016))
