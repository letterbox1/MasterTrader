---
id: P2-T040
kind: task
title: "Telegram bot commands: /bots, /bot, /approvals and mode changes"
phase: 2
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T035, P2-T037]
requirements: [R2.54]
roadmap_todos: [T2.34]
modules: [M15]
dashboards: []
tools: [uv]
mcp: []
env: []
services: []
branch: p2/P2-T040-telegram-bot-commands
pr: ""
doc_sync: [docs/ui/mobile-and-telegram.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T040 · Telegram bot commands: /bots, /bot, /approvals and mode changes

## Goal / expected outcome

`/bots`, `/bot <id>`, `/bot <id> pause|resume|stop`, `/bot <id> mode paper|hitl`, `/bot <id> mode autonomous` (C3) and `/approvals` work from Telegram against `mt_api` with the documented levels.

## Context & references

- Roadmap: [R2.54](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.34
- Design: [15 §1.4 Telegram commands](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) · [mob §3 Bots row](../../../docs/ui/mobile-and-telegram.md#3-telegram-bot)
- Decisions: paper → HITL is C2 ([17 §B P2-B005](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)); `approve`/`auto` are retired aliases (17 §B).

## Requirements

- `/bots`: mode, scope, status, today's P&L per bot (C0).
- `/bot <id>`: positions, open orders, last signals, mode, pending approvals (C0).
- `/bot <id> pause|resume|stop` (C1, inline confirm).
- `/bot <id> mode paper` (C1); `/bot <id> mode hitl` (C1 from autonomous, **C2** from paper); `/bot <id> mode autonomous` → C3 flow (Approve → TOTP → cool-down, default 15 min). `auto` is accepted as a retired alias.
- `/approvals`: pending cards re-sent/linked (C0).
- Fuzzy id/name matching with disambiguation buttons.

## ToDo

- [ ] Handlers + formatting
- [ ] Inline confirm keyboards
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: parsing + disambiguation.
- Flow: mode autonomous requires TOTP and cool-down; mode hitl from autonomous immediate (C1); mode hitl from paper asks for the C2 confirmation.

### Scenarios
- Given a running autonomous bot, when you send `/bot trend-btc mode hitl`, then it switches immediately and replies with the new mode.
- Given `/bot trend-btc mode autonomous` while a gate fails, then the bot replies with the failing gate and no C3 prompt.

### Stress / failure injection
- n/a: thin command layer over mt_api; load covered by mt_api tests.

## Acceptance criteria

- [ ] All 15 §1.4 commands work with correct levels
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Unknown bot id: helpful reply listing close matches.

## Cardinal rules (do NOT)

- Do NOT implement any business logic in the bot; call `mt_api` commands only.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.
- No Telegram text in any model, RAG index or training set (12 §4–5).

## Doc sync on completion

- `docs/ui/mobile-and-telegram.md` §3: command list confirmed.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.34 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T040-telegram-bot-commands`
- PR title: `P2-T040: Telegram bot commands: /bots, /bot, /approvals and mode changes`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T040` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (mode command names and levels per 15 §1.4 / 17 §B (paper→hitl C2, autonomous C3))
