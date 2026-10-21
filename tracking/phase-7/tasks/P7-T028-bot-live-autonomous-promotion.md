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
depends_on: [P7-T014, P7-T018]
requirements: [R7.08]
roadmap_todos: [T7.06]
modules: [M11, M0, M15]
dashboards: [D03, D01]
branch: p7/P7-T028-bot-live-autonomous-promotion
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/ui/dashboards/D03-strategies.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T028 · Per-bot live promotion HITL → autonomous (C3) with eligibility checks

## Goal / expected outcome

A live bot can move from `hitl` to `autonomous` only through C3 and only when its strategy version has a passing gate report, its sleeve is at least `micro_live` with ≥ 4 clean weeks in HITL, preflight passes, and no downgrade trigger is active; the D03 Bots tab shows exactly which condition fails.

## Context & references

- Roadmap: [R7.08 · ToDo T7.06](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [15 §1](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) (modes; autonomous = C3 and only while gates pass; escalation rules) · [02 §8 flows](../../../docs/02-v1-architecture.md#8-end-to-end-flows) F7 (approve mode first, auto is C3) · [D03](../../../docs/ui/dashboards/D03-strategies.md) Bots tab · [mob §3](../../../docs/ui/mobile-and-telegram.md#3-telegram-bot)
- Cross-phase: P2 T2.34 (bots, `bot.set_mode`, approval policy) and T2.69 (bot scenarios on paper).
- Related: P7-T014, P7-T018, P7-T011, P7-T029, P7-T058, gap P7-B009 (per-strategy vs per-bot mode)

## Requirements

- Eligibility (server-side, re-evaluated at apply time after the cool-down): latest gate report `pass` ≤ 7 days; sleeve state ≥ `micro_live`; ≥ 4 consecutive clean weeks with this bot in `hitl` on live; preflight pass; no active downgrade trigger; bot scope ⊆ allowed venues/products.
- `bot.set_mode autonomous` = C3 (approve + TOTP + 15-min cool-down); widening an autonomous bot's scope = C3; escalation rules (notional, hours, new instruments) default ON for the first 4 autonomous weeks.
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
- Given 3 clean HITL weeks, then autonomous is disabled with 'clean weeks 3/4'.
- Given eligibility passes, when you approve via Telegram + TOTP, then 15 min later the bot is autonomous and the first large order escalates to an approval card.

### Stress / failure injection
- Telegram outage at apply time: C3 incomplete → no change (fail closed).

## Acceptance criteria

- [ ] Autonomous only via C3 with all eligibility checks at request and apply time.
- [ ] WORM mode history references evidence.
- [ ] CI green.

## Exceptions & edge cases

- Strategy-level mode (`strategy.set_mode`) and bot-level mode disagree: the stricter wins (see P7-B009).
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
