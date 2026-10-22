---
id: P7-T024
kind: task
title: Live daily health check per bot
phase: 7
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T017, P2-T034]
requirements: [R7.07]
roadmap_todos: [T7.22]
modules: [M11]
dashboards: [D06]
tools: [git, uv]
mcp: []
env: []
services: [postgres, prefect-server, nats]
branch: p7/P7-T024-live-daily-health-check
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

# P7-T024 · Live daily health check per bot

## Goal / expected outcome

A daily job (00:15 UTC) **halts any live bot** pending your review when its live 30-day Sharpe is < ½ the validated figure or its drawdown is > 1.5× the backtest maximum, using the frozen references (one meaning: health check fail → halt the bot, 16 §2.6).

## Context & references

- Roadmap: [R7.07 · ToDo T7.22](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §5](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) (daily health check, per bot) · [16 §2.6](../../../docs/16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each) · [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) item 8
- Cross-phase: P2-T034 (`depends_on`) health-check baseline on paper.
- Related: P7-T017, P7-T020 (halt action), P7-T029, P7-T049

## Requirements

- 30-day Sharpe from the bot's daily returns (annualised, net); validated Sharpe and backtest max DD from `strategy.reference_dist`; the ½ and 1.5× multipliers are settings (16 §2.6).
- Breach → the **bot** is halted (reason `health_check`): its open orders cancel and its positions are handled per its exit rule; other bots in the sleeve continue; capital state → halted (resumes at the starting allocation after review, 16 §2.5); resume via `risk.sleeve.restart` scoped to the bot (C3, reason required, 02 §7.2).
- Fewer than 30 live days → check is 'warming up' (no halt) but drawdown leg still applies.
- Result row per bot per day in `risk.kill_eval`; summary in the weekly pack.

## ToDo

- [ ] Prefect flow `daily_health_check` (00:15 UTC).
- [ ] Reuse the kill-criteria action path.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: Sharpe 0.49× (halt) vs 0.51× validated (ok); DD 1.49× vs 1.51× backtest max.
- Integration: flow halts only the breaching bot (not its sleeve-mates) and alerts.

### Scenarios
- Given DD is 1.6× backtest max on day 12, then the bot halts even though the Sharpe leg is warming up.

### Stress / failure injection
- Flow fails (DB down): retry ×3, then critical alert and capital steps frozen until a run succeeds.

## Acceptance criteria

- [ ] Daily job halts on either leg; results stored.
- [ ] CI green.

## Exceptions & edge cases

- Bot paused for DQ for most of the 30 days: Sharpe computed on active days only, flagged in the result.

## Cardinal rules (do NOT)

- Do NOT skip a day's check silently; a missed run is an alert.
- Do NOT add discretionary overrides; the only manual trading action outside HITL approvals is flatten-and-halt with a required reason (14 §4).
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §5: schedule and warming-up rule.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.22 when this item is done.

## Branch & PR

- Branch: `p7/P7-T024-live-daily-health-check`
- PR title: `P7-T024: Live daily health check per bot`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T024` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (health check halts the bot, not the sleeve (16 §2.6); restart via risk.sleeve.restart C3; dep P2-T034)
