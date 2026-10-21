---
id: P2-B009
kind: gap
title: Engine control NATS subjects and some commands are missing from 02
phase: 2
type: DOC
status: backlog
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
branch: p2/P2-B009-missing-control-subjects-commands
pr: ""
doc_sync: [docs/02-v1-architecture.md]
doc_sync_status: n/a
found_in: docs/02-v1-architecture.md §4, §6, §7.2
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- [ ] Decide the rule with the user (or record the decision taken in the linked task)
- [ ] Update the source doc(s) so they agree
- [ ] Update the affected task file(s) to match

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- n/a: documentation.

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

- `docs/02-v1-architecture.md` §6/§7: additions.

## Branch & PR

- Branch: `p2/P2-B009-missing-control-subjects-commands`
- PR title: `P2-B009: add missing control subjects and commands to 02`

## Progress log

- 2026-10-21 00:00 · planner · opened
