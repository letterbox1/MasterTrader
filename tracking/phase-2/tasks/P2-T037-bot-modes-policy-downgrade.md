---
id: P2-T037
kind: task
title: Bot modes, approval policy, escalation and auto-downgrade
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T036, P2-T033, P2-T034, P2-T018]
requirements: [R2.53, R2.20]
roadmap_todos: [T2.34]
modules: [M11]
dashboards: [D03]
tools: [uv]
mcp: []
env: []
services: [nats, postgres]
branch: p2/P2-T037-bot-modes-policy-downgrade
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T037 · Bot modes, approval policy, escalation and auto-downgrade

## Goal / expected outcome

Each bot's mode (`paper` / `hitl` / `autonomous`), approval policy and escalation rules are enforced server-side; autonomous needs C3 and passing gates, and drops automatically to `hitl` (or `paused`) on a decay signal (rolling Sharpe/hit rate, CUSUM, 5 consecutive losing trades; 16 §2.6), ladder ≥ 3, DQ degraded on its instruments, model service down or a venue registry change, with the mode history kept in WORM. A bot's effective mode is capped by its strategy's mode ceiling (16 §2.3).

## Context & references

- Roadmap: [R2.53, R2.20](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.34
- Design: [15 §1.2 modes + auto-downgrade + escalation](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) · [15 §1.3 settings](../../../docs/15-bots-hitl-and-worm-audit.md#13-hitl-approval-via-telegram)
- Decisions: [17 §B P2-B005](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (paper → HITL is C2 everywhere) · [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) (mode levels, TTLs, large-order rule, strategy mode ceiling) · [16 §2.6](../../../docs/16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each) (decay → downgrade).
- Related: P2-T034 decay events, P2-T018 ladder, P2-T016 registry changes, P2-T060/T061 tests.

## Requirements

- `bot.set_mode`: → paper C1; → hitl from autonomous C1 (tightening); → hitl from paper **C2**; → autonomous **C3** and only while the strategy version passes every gate of its profile and its mode ceiling allows it (P2-T007). When the strategy ceiling is restricted, bots above it drop to it immediately (audited).
- `bot.approval_policy.set`: TTL (defaults 60 s intraday · 15 min swing · 4 h position), large-order threshold (default > 2% of sleeve or > A$5,000 → TOTP on Telegram / hold-to-confirm on web), escalation rules (notional above X, outside hours, newly added instruments), quiet hours with 'wake me', batching for dynamic bots; tighten C1, loosen C3.
- Escalation: an autonomous bot's order matching a rule becomes an approval card instead of executing.
- Quiet hours: hitl bots open no new entries during your quiet hours unless 'wake me'.
- Auto-downgrade triggers → target configurable (`hitl` default, or `paused`): decay signal from P2-T034 (rolling 60-trade Sharpe/hit rate below the 5th percentile, CUSUM break, **5 consecutive losing trades** by default), ladder rung ≥ 3, `dq.status` degraded/stale/bad on any scoped instrument, model service heartbeat missing, `venue.registry.changed` for its venue. (A failed daily health check halts the bot instead, P2-T034.) Downgrade is immediate, audited as a new `bot_version` row + `risk.event{type: bot_downgrade, trigger}`, alerts you. Upgrade back = C3.

## ToDo

- [ ] Mode/policy service in `packages/mt_strategy/bots/modes.py`
- [ ] Trigger subscribers (risk.event, KV ladder, dq.status, heartbeat, venue.registry.changed)
- [ ] Escalation evaluator in routing (P2-T033)
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: level matrix for every mode transition.
- Unit: each downgrade trigger → hitl within 1 s, audited.
- Unit: escalation rule converts an autonomous order into an approval request.
- Unit: quiet hours suppress hitl entries.

### Scenarios
- Given an autonomous bot on BTC, when BTC `dq.status` becomes degraded, then the bot switches to hitl within 1 s, you get an alert, and its next entry needs approval.
- Given you request autonomous for a bot whose strategy fails the deflated-Sharpe gate, when submitted, then it is refused naming the gate.

### Stress / failure injection
- Flap DQ status for a bot's instrument every second for 1 min: one downgrade, no re-upgrade (upgrade needs C3).

## Acceptance criteria

- [ ] Mode levels enforced server-side
- [ ] All six downgrade triggers wired and audited
- [ ] Escalation + quiet hours work
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Downgrade target `paused` with open positions: protective exits keep running.
- Gate provider unavailable: autonomous requests refused.

## Cardinal rules (do NOT)

- Do NOT auto-upgrade a bot back to autonomous.
- Do NOT let escalation be bypassed by order splitting (rule evaluated on parent intent notional).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows with `supersedes_id` (15 §2).
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md` §1.2: confirm the mode levels (paper → HITL C2) and the downgrade triggers as built.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.34 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T037-bot-modes-policy-downgrade`
- PR title: `P2-T037: Bot modes, approval policy, escalation and auto-downgrade`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T037` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (paper→HITL C2, strategy ceiling caps bots, decay signals per 16 §2.6 incl. 5 losing trades, TTL/large-order defaults)
