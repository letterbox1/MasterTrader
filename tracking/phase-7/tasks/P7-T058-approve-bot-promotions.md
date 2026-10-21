---
id: P7-T058
kind: task
title: Approve each bot promotion HITL → autonomous (C3)
phase: 7
type: USER
status: backlog
priority: medium
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P7-T028, P7-T057]
requirements: [R7.08]
roadmap_todos: [T7.06]
modules: [M11]
dashboards: [D03]
branch: p7/P7-T058-approve-bot-promotions
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T058 · Approve each bot promotion HITL → autonomous (C3)

## Goal / expected outcome

For each live bot you decide to automate, you approve the promotion to autonomous through C3 once its eligibility checklist is fully green — or you consciously keep it in HITL.

## Context & references

- Roadmap: [R7.08 · ToDo T7.06](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [15 §1](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) (autonomous = C3, per bot) · [02 §8 flows](../../../docs/02-v1-architecture.md#8-end-to-end-flows) F7 · [mob §3](../../../docs/ui/mobile-and-telegram.md#3-telegram-bot)
- Related: P7-T028 (eligibility), P7-T029 (auto-downgrade), P7-T054

## Requirements

- Only bots whose D03 eligibility checklist is all green (gate report, ≥ 4 clean HITL weeks live, preflight, no downgrade triggers).
- C3: Telegram approve → TOTP → 15-min cool-down; review the first escalated approval cards afterwards.
- Record per bot: promoted (date) or kept HITL (reason).

## ToDo

- [ ] Open D03 → Bots; review each live bot's checklist.
- [ ] For each bot you choose: start `/bot <id> mode auto` (or the D03 control) and complete the C3 steps.
- [ ] Record decisions in the progress log.

## Verification

### Tests
- n/a (user action).

### Scenarios
- Given a downgrade triggers after promotion, then the bot returns to HITL and needs your C3 again.

### Stress / failure injection
- n/a.

## Acceptance criteria

- [ ] Each live bot is either promoted via C3 (record) or kept in HITL with a reason.

## Exceptions & edge cases

- You may keep every bot in HITL; this item is then done with 'kept HITL' records.

## Cardinal rules (do NOT)

- Do NOT promote a bot whose checklist shows any red item.
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md`: none unless behaviour differed from spec.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.06 when this item is done.

## Branch & PR

- Branch: `p7/P7-T058-approve-bot-promotions`
- PR title: `P7-T058: Approve each bot promotion HITL → autonomous (C3)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T058` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
