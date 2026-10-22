---
id: P7-T023
kind: task
title: Live decay monitoring: rolling 60-trade stats vs p5 and CUSUM
phase: 7
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T017, P2-T034]
requirements: [R7.07]
roadmap_todos: [T7.22]
modules: [M11, M16]
dashboards: [D03, D06]
tools: [git, uv, pnpm]
mcp: []
env: []
services: [postgres, nats]
branch: p7/P7-T023-live-decay-rolling-and-cusum
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/03-build-spec.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T023 · Live decay monitoring: rolling 60-trade stats vs p5 and CUSUM

## Goal / expected outcome

Every live (and paper, in shadow) strategy version is monitored for decay: rolling 60-trade Sharpe and hit rate (26-week window for low-frequency bots) vs the frozen backtest 5th percentile, a CUSUM on P&L residuals, and 5 consecutive losing trades per bot; each fires an alert + downgrade to HITL (one meaning per signal, 16 §2.6) and marks the week not clean.

## Context & references

- Roadmap: [R7.07 · ToDo T7.22](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) (decay monitoring live) · [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) item 8 · [15 §1](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) (decay alert → autonomous bot downgrades) · [16 §2.6](../../../docs/16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each) · [17 §B P7-B006](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)
- Cross-phase: P2-T034 (`depends_on`) built the decay signals on paper (R2.21); this task runs them on live fills against frozen references and wires the live actions.
- Related: P7-T017, P7-T024, P7-T029, P7-T049

## Requirements

- Rolling 60-trade Sharpe and hit rate (net of costs) per bot (strategy version × sub-account); low-frequency bots use a 26-week window (16 §2.6); alert `decay` when either < reference p5.
- 5 consecutive losing trades per bot (default 5, a bot setting) → alert `decay_losses`.
- CUSUM (Page's two-sided, on standardised residual = live trade R − backtest expected R; k = 0.5σ, h = 5σ defaults, configurable tighter) → alert `decay_cusum` on crossing.
- Alerts published on `risk.event` (type `decay`) and `alert.warning.decay`; state in `risk.decay_state`; D03 Performance tab shows rolling stats with the p5 band and the CUSUM chart.
- Action mapping (16 §2.6, one meaning each): every signal here → alert + downgrade autonomous → HITL (P7-T029) and the week is not clean; halting stays with the daily health check (bot, P7-T024) and the kill criteria (sleeve, P7-T020).
- Runs on each closed trade; < 1 s compute.

## ToDo

- [ ] `packages/mt_monitor/decay/` (rolling window, CUSUM).
- [ ] Migration `risk.decay_state` (latest per version; history in `risk.kill_eval`).
- [ ] D03 Performance: rolling-stat chart with p5 band, CUSUM chart (ECharts).
- [ ] Tests; docs.

## Verification

### Tests
- Unit: CUSUM detects a mean shift of 1σ within the expected ARL on synthetic data; no false alarm on 1,000 in-control trades with h = 5σ (ARL0 check).
- Unit: rolling stats over exactly 60 trades; < 60 → 'warming up'; a low-frequency bot uses the 26-week window instead.
- Integration: decay alert published and consumed by the auto-downgrade handler (mock).

### Scenarios
- Given hit rate drops from 45% to 30% over 60 trades and p5 is 34%, then a decay alert fires and autonomous bots for that version downgrade to HITL.
- Given 5 consecutive losing trades on an autonomous bot, then it downgrades to HITL with reason `decay_losses`.
- Given a strategy in paper, then decay runs in shadow and only notifies.

### Stress / failure injection
- Replay 5 years of trades for 20 versions: alerts reproducible; monitor restart rebuilds state from fills (no lost window).

## Acceptance criteria

- [ ] Rolling stats and CUSUM live per version with charts.
- [ ] Alerts feed downgrade and clean-week logic.
- [ ] CI green.

## Exceptions & edge cases

- Trades with zero R (scratch) count as trades.
- Version change: a new version starts a fresh window and fresh CUSUM.

## Cardinal rules (do NOT)

- Do NOT reset CUSUM manually to silence an alert; reset only on a new version.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT add discretionary overrides; the only manual trading action outside HITL approvals is flatten-and-halt with a required reason (14 §4).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §6: CUSUM parameters.
- `docs/03-build-spec.md` §8 item 8: link to the monitor.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.22 when this item is done.

## Branch & PR

- Branch: `p7/P7-T023-live-decay-rolling-and-cusum`
- PR title: `P7-T023: Live decay monitoring: rolling 60-trade stats vs p5 and CUSUM`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T023` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (signals per 16 §2.6: 26-week low-frequency window, 5 consecutive losses, all → downgrade to HITL; dep P2-T034)
