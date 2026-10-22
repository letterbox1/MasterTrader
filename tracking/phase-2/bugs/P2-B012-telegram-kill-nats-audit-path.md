---
id: P2-B012
kind: gap
title: Telegram /kill via NATS when mt-api is down has no defined audit path or NATS permissions
phase: 2
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.52, R2.18]
roadmap_todos: []
modules: [M15, M17]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B012-telegram-kill-nats-audit-path
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/mobile-and-telegram.md]
doc_sync_status: done
found_in: docs/ui/mobile-and-telegram.md §3; docs/02-v1-architecture.md §7.2/§9.3
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B012 · Telegram /kill via NATS when mt-api is down has no defined audit path or NATS permissions

## Goal / expected outcome

A kill sent by the Telegram bot straight to NATS is still audited (WORM) and the bot's NATS rights are minimal.

## Context & references

- [mob §3 security row](../../../docs/ui/mobile-and-telegram.md#3-telegram-bot) · [02 §7.2 'every command written to audit.command'](../../../docs/02-v1-architecture.md#72-commands-rest-write) · [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes)
- Affects P2-T035, P2-T031, P2-T059.

## Requirements

- **Steps to reproduce:** `audit.command` rows are written by mt-api; when mt-api is down the bot publishes `kill.set` directly, so no command row is written and the bot needs some NATS publish permission not specified anywhere.
- **Expected:** Telegram NATS account may publish only `kill.set` and `audit.telegram.*`; the event is persisted in JetStream and ingested into `audit.command` (source telegram, `via=nats`) when mt-api returns; the engine also records `risk.event{type: kill}`.
- **Actual:** Unspecified.
- **Suggested fix:** Document the above in 02 §7.4/§9.3 and mob §3; implemented in P2-T035.
- **Impact:** S3: gap in the audit trail for the most critical command.

## ToDo

- [x] Decision recorded: Telegram `/kill` via NATS uses credentials limited to publishing `kill.set`; the engine writes the kill event to WORM with source `telegram` (no separate `audit.telegram.*` path)
- [x] Docs agree: 02 §3.2/§6/§9.3, mob §3, 03 M15
- [x] Tasks updated: P2-T035 (credentials + engine-side WORM write), P2-T052 (permission test), P2-T059 (degraded test)

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- Given mt-api down, when `/kill` is used, then after recovery `audit.command` contains the kill with `via=nats`.

### Stress / failure injection
- n/a: documentation/specification gap

## Acceptance criteria

- [x] Docs agree in one place, cross-linked from the others (02 §3.2 telegram-bot row, §6 `kill.set`, §9.3 mt-api-down row; mobile-and-telegram §3 Security row; 03 M15)
- [x] Affected tasks reference the decision (P2-T035, P2-T052, P2-T059)

## Exceptions & edge cases

- Until resolved, the affected task implements the conservative option stated under Suggested fix.

## Cardinal rules (do NOT)

- Do NOT close without the doc fix merged and the dependent task(s) updated to match.
- Do NOT "fix" by silently picking a number in code; the decision is recorded in the doc and in the risk policy (user input).
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7.4/§9.3 and `docs/ui/mobile-and-telegram.md` §3.

## Branch & PR

- Branch: `p2/P2-B012-telegram-kill-nats-audit-path`
- PR title: `P2-B012: define audit path for NATS-direct kill`

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (resolved by 17 §D (P2-B012); docs carry it (02 §3.2 telegram-bot row, §6 `kill.set`, §9.3 mt-api-down row; mobile-and-telegram §3 Security row; 03 M15); implementation owned by P2-T035, P2-T052, P2-T059)
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D (P2-B012)); docs updated: 02 §3.2 telegram-bot row, §6 `kill.set`, §9.3 mt-api-down row; mobile-and-telegram §3 Security row; 03 M15; implementation owned by P2-T035, P2-T052, P2-T059
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
