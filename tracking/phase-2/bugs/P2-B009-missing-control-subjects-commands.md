---
id: P2-B009
kind: gap
title: Engine control NATS subjects and some commands are missing from 02
phase: 2
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.06, R2.07, R2.14]
roadmap_todos: []
modules: [M0, M11, M12]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B009-missing-control-subjects-commands
pr: ""
doc_sync: [docs/02-v1-architecture.md]
doc_sync_status: done
found_in: docs/02-v1-architecture.md §4, §6, §7.2
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B009 · Engine control NATS subjects and some commands are missing from 02

## Goal / expected outcome

02 lists every subject and command Phase 2 uses.

## Context & references

- [02 §6 subjects](../../../docs/02-v1-architecture.md#6-messaging-nats) · [02 §7.2 commands](../../../docs/02-v1-architecture.md#72-commands-rest-write) · [02 §4 `strat.status.*`](../../../docs/02-v1-architecture.md#4-logical-components)
- Affects P2-T021, P2-T012, P2-T030, P2-T038.

## Requirements

- **Steps to reproduce:** 02 §6 has no subject for mt-api → engine control (strategy start/pause/stop, bot lifecycle); `strat.status.*` appears only in §4; no command to restart a sleeve halted by drawdown/health (14 §5 'manual restart'); no command for shadow runs; no `approvals` WS topic.
- **Expected:** Subjects `ctl.engine.{command}` and `strat.status.{strategy}` in §6; commands `risk.sleeve.resume` (C1) and `strategy.run_shadow` (C1); WS topic `approvals`.
- **Actual:** Missing; tasks would invent names independently.
- **Suggested fix:** Add them to 02 §6/§7 as implemented by P2-T021, P2-T012/T034, P2-T030, P2-T038.
- **Impact:** S4: naming drift only.

## ToDo

- [x] Decision recorded: engine control subjects `engine.cmd.*`; sleeve restart is `risk.sleeve.restart` (C3, 16 §2.3) rather than the proposed C1 resume; `strategy.run_shadow` (C1); WS topic `approvals`
- [x] Docs agree: 02 §6/§7.2/§7.3
- [x] Tasks updated: P2-T021, P2-T030, P2-T012/P2-T020 (`risk.sleeve.restart`), P2-T038

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- n/a: documentation.

### Stress / failure injection
- n/a: documentation/specification gap

## Acceptance criteria

- [x] Docs agree in one place, cross-linked from the others (02 §6 subjects (`engine.cmd.{command}`, `strat.status.{strategy}`, `bot.{id}.status`); 02 §7.2 (`strategy.run_shadow` C1, `risk.sleeve.restart` C3); 02 §7.3 WS `approvals`)
- [x] Affected tasks reference the decision (P2-T021, P2-T030, P2-T012, P2-T020, P2-T038)

## Exceptions & edge cases

- Until resolved, the affected task implements the conservative option stated under Suggested fix.

## Cardinal rules (do NOT)

- Do NOT close without the doc fix merged and the dependent task(s) updated to match.
- Do NOT "fix" by silently picking a number in code; the decision is recorded in the doc and in the risk policy (user input).
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/02-v1-architecture.md` §6/§7: additions.

## Branch & PR

- Branch: `p2/P2-B009-missing-control-subjects-commands`
- PR title: `P2-B009: add missing control subjects and commands to 02`

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (resolved by 17 §D (P2-B009, suggested fix adopted with `engine.cmd.*`); docs carry it (02 §6 subjects (`engine.cmd.{command}`, `strat.status.{strategy}`, `bot.{id}.status`); 02 §7.2 (`strategy.run_shadow` C1, `risk.sleeve.restart` C3); 02 §7.3 WS `approvals`); implementation owned by P2-T021, P2-T030, P2-T012, P2-T020, P2-T038)
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D (P2-B009, suggested fix adopted with `engine.cmd.*`)); docs updated: 02 §6 subjects (`engine.cmd.{command}`, `strat.status.{strategy}`, `bot.{id}.status`); 02 §7.2 (`strategy.run_shadow` C1, `risk.sleeve.restart` C3); 02 §7.3 WS `approvals`; implementation owned by P2-T021, P2-T030, P2-T012, P2-T020, P2-T038
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
