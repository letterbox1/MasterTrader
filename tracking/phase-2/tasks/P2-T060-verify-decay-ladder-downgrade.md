---
id: P2-T060
kind: task
title: Simulated decay, ladder and auto-downgrade tests
phase: 2
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T034, P2-T018, P2-T037]
requirements: [R2.21, R2.15, R2.53]
roadmap_todos: [T2.22]
modules: [M11]
dashboards: []
tools: [uv]
mcp: []
env: []
services: []
branch: p2/P2-T060-verify-decay-ladder-downgrade
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

# P2-T060 · Simulated decay, ladder and auto-downgrade tests

## Goal / expected outcome

Synthetic paper histories and injected faults prove the signals keep **one meaning each** ([16 §2.6](../../../docs/16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each)): decay signals (rolling 60-trade Sharpe/hit rate below the 5th percentile, CUSUM break, 5 consecutive losing trades) alert and downgrade the bot to HITL; a failed daily health check halts the bot; the ladder moves through all six rungs; and bots auto-downgrade on each trigger.

## Context & references

- Roadmap: [R2.21, R2.15](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.22
- Spec: [14 §5](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) · [15 §1.2 auto-downgrade](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) · [16 §2.6](../../../docs/16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each) · [17 §B P2-B011](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (built for paper here; P7 extends to live)

## Requirements

- Decay: inject a regime shift into simulated P&L → CUSUM alert within expected run length; 60-trade Sharpe below 5th pct → alert; 5 consecutive losing trades → alert; each → autonomous bot downgraded to HITL, never halted. Low-frequency bot → 26-week window used.
- Health: 30d Sharpe < ½ validated → halt the **bot**; DD > 1.5× backtest max → halt the bot; its sleeve keeps trading.
- Ladder: drive inputs to reach each rung 1→6 and back (2–4 auto-recover with hysteresis; 5–6 manual).
- Downgrade: each of the six triggers moves an autonomous bot to hitl within 1 s with audit.

## ToDo

- [ ] Simulation fixtures
- [ ] Test cases
- [ ] Report
- [ ] Record results (numbers, run IDs, screenshots) in the progress log and tick the roadmap ToDo box

## Verification

### Tests
- As above.

### Scenarios
- Given an autonomous bot, when the ladder reaches rung 3 due to a late decision, then it downgrades to hitl and alerts.

### Stress / failure injection
- n/a: deterministic simulations.

## Acceptance criteria

- [ ] All thresholds and triggers verified

## Exceptions & edge cases

- Insufficient trades: decay reports 'insufficient' (asserted).

## Cardinal rules (do NOT)

- Do NOT tune thresholds to pass tests; thresholds come from policy.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §5: link the simulations.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.22 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T060-verify-decay-ladder-downgrade`
- PR title: `P2-T060: Simulated decay, ladder and auto-downgrade tests`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T060` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (signal meanings per 16 §2.6 (decay → downgrade incl. 5 losing trades; health → halt the bot))
