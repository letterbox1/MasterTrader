---
id: P2-B005
kind: gap
title: Confirmation level for paper to HITL conflicts (C1 vs C2)
phase: 2
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.53, R2.54]
roadmap_todos: []
modules: [M11, M15]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B005-paper-to-hitl-confirmation-level
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/ui/dashboards/D03-strategies.md, docs/ui/mobile-and-telegram.md]
doc_sync_status: done
found_in: docs/15-bots-hitl-and-worm-audit.md §1.2 vs §1.4; docs/ui/dashboards/D03-strategies.md Bots tab
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B005 · Confirmation level for paper to HITL conflicts (C1 vs C2)

## Goal / expected outcome

One level for switching a bot from paper to HITL, used by API, web and Telegram.

## Context & references

- [15 §1.2 modes table](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) · [15 §1.4 commands](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) · [D03 Bots tab](../../../docs/ui/dashboards/D03-strategies.md) · [mob §3](../../../docs/ui/mobile-and-telegram.md#3-telegram-bot)
- Affects P2-T037, P2-T040, P2-T041.

## Requirements

- **Steps to reproduce:** 15 §1.2: hitl 'From paper: C2'. 15 §1.4: '/bot <id> mode paper · mode hitl — Tightening, immediate — C1'. D03 Bots: 'bot.set_mode → HITL/paper (C1)'. D03 strategy actions: 'Mode → approve: C2'.
- **Expected:** paper → hitl = C2 (it starts real venue orders, even if each needs approval); autonomous → hitl and anything → paper = C1.
- **Actual:** Docs say C1 and C2 for the same transition.
- **Suggested fix:** Adopt the expected matrix; P2-T037 implements it server-side (conservative C2 until decided).
- **Impact:** S3: inconsistent prompts between Telegram and web.

## ToDo

- [x] Decision recorded: paper → HITL is C2 everywhere; HITL → autonomous C3; any downgrade C1
- [x] Docs agree: 15 §1.2/§1.4/§1.5, D03, components, 16 §2.3
- [x] Tasks updated: P2-T037, P2-T040, P2-T041, P2-T140

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- Given a paper bot, when `/bot x mode hitl` is sent, then a C2 confirmation with risk preview is required.

### Stress / failure injection
- n/a: documentation/specification gap

## Acceptance criteria

- [x] Docs agree in one place, cross-linked from the others (15 §1.2 modes table, §1.4 Telegram commands, §1.5 `bot.set_mode`; D03 Bots actions; components `ModeSwitch`; 16 §2.3)
- [x] Affected tasks reference the decision (P2-T037, P2-T040, P2-T041, P2-T140)

## Exceptions & edge cases

- Until resolved, the affected task implements the conservative option stated under Suggested fix.

## Cardinal rules (do NOT)

- Do NOT close without the doc fix merged and the dependent task(s) updated to match.
- Do NOT "fix" by silently picking a number in code; the decision is recorded in the doc and in the risk policy (user input).
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md` §1.4, `docs/ui/dashboards/D03-strategies.md`, `docs/ui/mobile-and-telegram.md` §3: levels aligned.

## Branch & PR

- Branch: `p2/P2-B005-paper-to-hitl-confirmation-level`
- PR title: `P2-B005: align paper-to-hitl confirmation level`

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (resolved by 17 §B (P2-B005); docs carry it (15 §1.2 modes table, §1.4 Telegram commands, §1.5 `bot.set_mode`; D03 Bots actions; components `ModeSwitch`; 16 §2.3); implementation owned by P2-T037, P2-T040, P2-T041, P2-T140)
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B (P2-B005)); docs updated: 15 §1.2 modes table, §1.4 Telegram commands, §1.5 `bot.set_mode`; D03 Bots actions; components `ModeSwitch`; 16 §2.3; implementation owned by P2-T037, P2-T040, P2-T041, P2-T140
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
