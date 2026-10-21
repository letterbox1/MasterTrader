---
id: P2-T034
kind: task
title: Daily sleeve health check and decay alerts
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T014, P2-T007]
requirements: [R2.21]
roadmap_todos: [T2.22]
modules: [M11]
dashboards: [D06, D03]
branch: p2/P2-T034-health-check-decay-alerts
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

# P2-T034 · Daily sleeve health check and decay alerts

## Goal / expected outcome

A daily per-sleeve health check halts a sleeve pending review when its 30-day Sharpe is below half the validated figure or its drawdown exceeds 1.5× the backtest maximum, and decay alerts fire when the rolling 60-trade Sharpe or hit rate falls below the backtest's 5th percentile or CUSUM on P&L residuals signals a shift.

## Context & references

- Roadmap: [R2.21](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.22
- Spec: [14 §5 daily health check](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) · [14 §6 decay monitoring](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [03 §8 item 8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable)
- Inputs: validated Sharpe, backtest max DD and the backtest 60-trade Sharpe/hit-rate distribution from Part B's validation report (stored with the strategy version).
- Related: P2-T037 auto-downgrade consumes decay alerts; P2-B011 (P7 overlap); P2-T060 simulated decay.

## Requirements

- Prefect flow `risk_health_daily` at 00:15 UTC per sleeve and strategy version: compute live (paper) 30-day Sharpe and drawdown from `audit.fill` + marks.
- Halt rule → sleeve `halted_review`, cancel entries, alert warning, `risk.event{type: health_halt}`; resume via `risk.sleeve.resume` (C1, audited).
- Decay: rolling 60-trade Sharpe and hit rate vs 5th percentile of the backtest bootstrap distribution; CUSUM (k, h from policy; default k = 0.5σ, h = 5σ) on P&L residuals vs expected; alert `alert.warning.decay` + `risk.event{type: decay}`.
- Not enough trades (< 60) → decay check reports 'insufficient' (no alert).

## ToDo

- [ ] `packages/mt_risk/health.py` (metrics, CUSUM)
- [ ] Prefect flow + schedule
- [ ] Event + alert wiring
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: CUSUM detects a mean shift injected at trade 100 within expected ARL.
- Unit: halt thresholds at boundary values.
- Integration: flow run over a synthetic paper history writes events and halts.

### Scenarios
- Given validated Sharpe 1.2 and live 30-day Sharpe 0.5, when the daily check runs, then the sleeve halts pending review and you get an alert with numbers.
- Given a strategy without a validation report, when the check runs, then it is flagged 'no baseline' and cannot be promoted beyond paper.

### Stress / failure injection
- n/a: daily batch; runtime over 50 sleeves × 2 years < 60 s asserted.

## Acceptance criteria

- [ ] Health rule and decay alerts implemented per 14 §5/§6
- [ ] Events feed bot auto-downgrade
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Missing marks (stale feed): check deferred and alerted, not computed on stale data.
- Paper period < 30 days: Sharpe rule reports 'warming up'.

## Cardinal rules (do NOT)

- Do NOT auto-resume a sleeve halted for review.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §5/§6: CUSUM parameters as defaults.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.22 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T034-health-check-decay-alerts`
- PR title: `P2-T034: Daily sleeve health check and decay alerts`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T034` run

## Progress log

- 2026-10-21 00:00 · planner · created
