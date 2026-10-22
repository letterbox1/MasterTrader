---
id: P7-T028
kind: task
title: Per-bot live promotion HITL → autonomous (C3) with eligibility checks
phase: 7
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T014, P7-T018, P2-T037]
requirements: [R7.08]
roadmap_todos: [T7.06]
modules: [M11, M0, M15]
dashboards: [D03, D01]
tools: [git, uv, pnpm, node>=20]
mcp: []
env: []
services: [postgres, nats, mt-api, telegram bot api]
branch: p7/P7-T028-bot-live-autonomous-promotion
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/ui/dashboards/D03-strategies.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T028 · Per-bot live promotion HITL → autonomous (C3) with eligibility checks

## Goal / expected outcome

Every bot starts live in `hitl` (R7.08); it can move to `autonomous` only through C3 and only when its strategy version has a passing gate report (incl. the paper/HITL period of its gate profile, 16 §2.4), it is funded (≥ `micro_live`), preflight passes and no downgrade trigger is active; the D03 Bots tab shows exactly which condition fails.

## Context & references

- Roadmap: [R7.08 · ToDo T7.06](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [15 §1](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) (modes; autonomous = C3 and only while gates pass; escalation rules) · [02 §8 flows](../../../docs/02-v1-architecture.md#8-end-to-end-flows) F7 (every bot starts live in `hitl`; HITL → autonomous is C3) · [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) (mode changes; the strategy mode caps bot modes) · [17 §B P7-B009](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (modes per bot) · [D03](../../../docs/ui/dashboards/D03-strategies.md) Bots tab · [mob §3](../../../docs/ui/mobile-and-telegram.md#3-telegram-bot)
- Cross-phase: P2-T037 (`depends_on`: bot modes, approval policy, escalation, auto-downgrade); P2-T061 (bot scenarios on paper).
- Related: P7-T014, P7-T018, P7-T011, P7-T029, P7-T058, gap P7-B009 (resolved: modes per bot; the stricter of strategy and bot mode applies)

## Requirements

- Eligibility (server-side, re-evaluated at apply time after the 15-min cool-down): latest gate report `pass` ≤ 7 days (the gate profile includes the paper/HITL period: default ≥ 8 weeks and ≥ 50 trades, 16 §2.4); capital state ≥ `micro_live`; preflight pass; no active downgrade trigger; bot scope ⊆ allowed venues/products; the strategy mode ceiling allows `autonomous`. Requiring a number of clean live HITL weeks first is an optional tightening (C1), off by default.
- `bot.set_mode autonomous` = C3 (approve + TOTP + 15-min cool-down); widening an autonomous bot's scope = C3; escalation rules (notional, hours, new instruments, 15 §1) are prefilled in the bot's approval policy; tightening C1, loosening C3.
- Every mode change is a new `strategy.bot_version` row (WORM) referencing the gate report and preflight snapshot.
- D03 Bots tab: eligibility checklist per bot; the autonomous option is disabled with reasons while any check fails.

## ToDo

- [ ] Eligibility service `packages/mt_strategy/bots/eligibility.py`.
- [ ] Wire into `bot.set_mode` C3 path (check at request and at apply).
- [ ] Default escalation rules for newly autonomous bots.
- [ ] D03 Bots tab eligibility checklist; Telegram C3 message shows the checklist summary.
- [ ] Tests; docs.

## Verification

### Tests
- Integration: each failing condition blocks with its reason; all passing → applies after cool-down; condition breaks during cool-down → not applied.
- Integration: two bots on one strategy (BTC autonomous, gold HITL) stay isolated.
- Playwright: Bots tab eligibility list at §6.8 viewports.

### Scenarios
- Given the gate report's paper/HITL section shows 7 of 8 weeks, then autonomous is disabled with 'paper/HITL period 7/8 weeks'.
- Given eligibility passes, when you approve via Telegram + TOTP, then 15 min later the bot is autonomous and the first large order escalates to an approval card.

### Stress / failure injection
- Telegram outage at apply time: C3 incomplete → no change (fail closed).

## Acceptance criteria

- [ ] Autonomous only via C3 with all eligibility checks at request and apply time.
- [ ] WORM mode history references evidence.
- [ ] CI green.

## Exceptions & edge cases

- Strategy-level mode (`strategy.set_mode`) and bot-level mode disagree: the stricter wins (16 §2.3, 17 §B).
- Bot on MT5/cTrader route: same rules; adapter health is a downgrade trigger.

## Cardinal rules (do NOT)

- Do NOT offer a shortcut to autonomous for 'small' bots.
- Do NOT let protective exits depend on mode.
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md` §1.2: live eligibility conditions.
- `docs/ui/dashboards/D03-strategies.md`: Bots tab eligibility checklist.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.06 when this item is done.

## Branch & PR

- Branch: `p7/P7-T028-bot-live-autonomous-promotion`
- PR title: `P7-T028: Per-bot live promotion HITL → autonomous (C3) with eligibility checks`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T028` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (modes paper/hitl/autonomous per bot (17 §B); eligibility = gate profile incl. paper/HITL period (16 §2.4); the 4-clean-weeks rule is now an optional tightening; dep P2-T037)
