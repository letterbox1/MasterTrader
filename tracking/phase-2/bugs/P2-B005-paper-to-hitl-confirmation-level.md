---
id: P2-B005
kind: gap
title: Confirmation level for paper to HITL conflicts (C1 vs C2)
phase: 2
type: DOC
status: backlog
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
branch: p2/P2-B005-paper-to-hitl-confirmation-level
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/ui/dashboards/D03-strategies.md, docs/ui/mobile-and-telegram.md]
doc_sync_status: n/a
found_in: docs/15-bots-hitl-and-worm-audit.md §1.2 vs §1.4; docs/ui/dashboards/D03-strategies.md Bots tab
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- [ ] Decide the rule with the user (or record the decision taken in the linked task)
- [ ] Update the source doc(s) so they agree
- [ ] Update the affected task file(s) to match

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- Given a paper bot, when `/bot x mode hitl` is sent, then a C2 confirmation with risk preview is required.

### Stress / failure injection
- n/a: documentation/specification gap

## Acceptance criteria

- [ ] Docs agree in one place, cross-linked from the others
- [ ] Affected tasks reference the decision

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
