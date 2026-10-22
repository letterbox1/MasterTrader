---
id: P7-T049
kind: task
title: Simulated decay, health-check and auto-downgrade breaches
phase: 7
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T023, P7-T024, P7-T029]
requirements: [R7.07, R7.08]
roadmap_todos: [T7.22, T7.61]
modules: [M11, M16]
dashboards: [D03, D06]
tools: [git, uv]
mcp: []
env: []
services: [postgres, nats]
branch: p7/P7-T049-verify-decay-and-downgrade-simulated
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/15-bots-hitl-and-worm-audit.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T049 · Simulated decay, health-check and auto-downgrade breaches

## Goal / expected outcome

Injected performance decay triggers the rolling-stat and CUSUM alerts, the daily health check halts on either leg, and every downgrade trigger moves autonomous bots to HITL/paused within 2 s — proving the decay-monitoring half of exit criterion 2.

## Context & references

- Roadmap: [R7.07, R7.08 · ToDo T7.22, T7.61](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) (decay) · [14 §5](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) (health check) · [15 §1](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) (auto-downgrade) · [16 §2.6](../../../docs/16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each) (one meaning per signal) · Roadmap R7.07 'Verified by: alerts'
- Related: P7-T023, P7-T024, P7-T029, P7-T064

## Requirements

- Cases: rolling 60-trade hit rate < p5; Sharpe < p5; the 26-week window for a low-frequency bot; CUSUM mean shift −1σ (detected within expected ARL); 5 consecutive losses: each → downgrade to HITL. Health check Sharpe < ½ validated and DD > 1.5× backtest max: each → **halt the bot** (16 §2.6). Each P7-T029 trigger (table-driven).
- Assertions: alert kinds and channels, D03 charts show the breach, bot mode history rows (WORM), clean-week evaluator marks the week dirty, no auto-upgrade after recovery.

## ToDo

- [ ] Synthetic trade-stream generator with controllable drift.
- [ ] Implement the cases in `tests/sim/test_decay.py`.
- [ ] Observed run with two autonomous paper bots; record evidence.
- [ ] File bugs for deviations.

## Verification

### Tests
- Sim suite covering every case above; ARL check over 1,000 runs for CUSUM false alarms (in-control) and detection delay (shifted).

### Scenarios
- Given an autonomous bot whose hit rate decays, then within one trade of crossing p5 it is in HITL and you receive one Telegram message with a C3 re-enable button.

### Stress / failure injection
- Combined triggers (DQ + decay + registry change at once): one downgrade, all reasons recorded.

## Acceptance criteria

- [ ] All cases pass in CI; observed run recorded.
- [ ] Downgrade latency < 2 s in every case.

## Exceptions & edge cases

- Paper bots: decay alerts in shadow must still be testable (same code path).

## Cardinal rules (do NOT)

- Do NOT tune CUSUM parameters looser to reduce alerts without C3.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §6 and `docs/15-bots-hitl-and-worm-audit.md` §1.2: link the suite.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.22, T7.61 when this item is done.

## Branch & PR

- Branch: `p7/P7-T049-verify-decay-and-downgrade-simulated`
- PR title: `P7-T049: Simulated decay, health-check and auto-downgrade breaches`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T049` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (cases per 16 §2.6 incl. 5 losses and the 26-week window; the health check halts the bot)
