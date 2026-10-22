---
id: P2-T034
kind: task
title: Daily bot health check and decay signals (downgrade or halt)
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
tools: [uv]
mcp: []
env: []
services: [postgres, nats]
branch: p2/P2-T034-health-check-decay-alerts
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T034 · Daily bot health check and decay signals (downgrade or halt)

## Goal / expected outcome

Decay and health signals with **one meaning each** ([16 §2.6](../../../docs/16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each)) run on paper: a bot's rolling 60-trade Sharpe or hit rate below the backtest's 5th percentile (26-week window for low-frequency bots), a CUSUM break on P&L residuals, or 5 consecutive losing trades → **alert + downgrade the bot autonomous → HITL**; the daily health check failing (30-day Sharpe < ½ validated, or drawdown > 1.5× backtest max) → **halt the bot** pending your review. P7 extends these jobs to live and wires the sleeve kill criteria (R7.06/R7.07).

## Context & references

- Roadmap: [R2.21](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.22
- Spec: [14 §5 daily health check](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) · [14 §6 decay monitoring](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [03 §8 item 8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable)
- Inputs: validated Sharpe, backtest max DD and the backtest 60-trade Sharpe/hit-rate distribution from Part B's validation report (stored with the strategy version).
- Decisions: [17 §B P2-B011](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (built in P2 for paper; P7 extends to live with kill criteria) · [16 §2.6](../../../docs/16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each).
- Related: P2-T037 auto-downgrade consumes decay events; P2-T060 simulated decay; P2-T114 stores the baselines.

## Requirements

- Prefect flow `risk_health_daily` at 00:15 Sydney time (schedule configurable) **per bot**: compute paper 30-day Sharpe and drawdown from `audit.fill` + marks.
- Health fail → bot `halted_review`, cancel its entries, alert warning, `risk.event{type: health_halt}`; resume via `bot.resume` after your review (C1, audited, with a reason).
- Decay (per bot, evaluated on every closed trade): rolling 60-trade Sharpe and hit rate vs the 5th percentile of the backtest bootstrap distribution (bots below the low-frequency threshold use a 26-week window); CUSUM (k, h from policy; default k = 0.5σ, h = 5σ) on P&L residuals vs expected; **5 consecutive losing trades**. Each → `alert.warning.decay` + `risk.event{type: decay, signal}` → P2-T037 downgrades autonomous → HITL. One action per signal; never a halt from a decay signal.
- Not enough trades (< 60, outside the low-frequency window) → decay check reports 'insufficient' (no alert).
- All thresholds (60 trades, 5th percentile, ½ Sharpe, 1.5× drawdown, 5 losses, 26 weeks) are L4/L3 defaults from 16 §2.6, editable; loosening is C3.

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
- Given validated Sharpe 1.2 and paper 30-day Sharpe 0.5, when the daily check runs, then the **bot** halts pending review (its sleeve keeps trading) and you get an alert with numbers.
- Given an autonomous bot with 5 consecutive losing trades, when the 5th closes, then an alert fires and the bot is downgraded to HITL (no halt).
- Given a strategy without a validation report, when the check runs, then it is flagged 'no baseline' and cannot be promoted beyond paper.

### Stress / failure injection
- n/a: daily batch; runtime over 50 sleeves × 2 years < 60 s asserted.

## Acceptance criteria

- [ ] Health rule (halt the bot) and decay signals (downgrade to HITL) implemented per 16 §2.6, one meaning each
- [ ] Events feed bot auto-downgrade
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Missing marks (stale feed): check deferred and alerted, not computed on stale data.
- Paper period < 30 days: Sharpe rule reports 'warming up'.

## Cardinal rules (do NOT)

- Do NOT auto-resume a bot halted for review.
- Do NOT give a decay signal any action other than alert + downgrade to HITL (16 §2.6).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §5/§6: CUSUM parameters as defaults.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.22 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T034-health-check-decay-alerts`
- PR title: `P2-T034: Daily bot health check and decay signals (downgrade or halt)`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T034` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (decay/health signal meanings per 16 §2.6 (decay incl. 5 losing trades → downgrade to HITL; health fail → halt the bot), per bot, Sydney schedule, P7 extension)
