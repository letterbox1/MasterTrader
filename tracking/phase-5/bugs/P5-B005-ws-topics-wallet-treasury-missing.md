---
id: P5-B005
kind: gap
title: D18 WebSocket topics `wallet`, `treasury`, `alert` are not in the 02 §7.3 topic list
phase: 5
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R5.23]
roadmap_todos: []
modules: [M15, M22]
dashboards: [D18]
branch: p5/P5-B005-ws-topics-wallet-treasury-missing
pr: ""
doc_sync: [docs/02-v1-architecture.md]
doc_sync_status: n/a
found_in: "docs/ui/dashboards/D18-wallets-treasury.md §Backend contract vs docs/02-v1-architecture.md §7.3"
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-B005 · D18 WebSocket topics `wallet`, `treasury`, `alert` are not in the 02 §7.3 topic list

## Goal / expected outcome

02 §7.3 lists every WS topic the dashboards subscribe to.

## Context & references

- D18 backend contract: topics `wallet`, `treasury`, `alert`, `kill`
- 02 §7.3 has `notifications` but no `wallet`, `treasury` or `alert`
- Task P5-T011 adds `wallet` (and `alert`)

## Requirements

- **Steps to reproduce:** Compare D18's topic list with 02 §7.3.
- **Expected:** Topics present in the API contract.
- **Actual:** Missing.
- **Suggested fix:** Add `wallet` (P5), `treasury` (P6) and `alert` (or map D18 to `notifications`) to 02 §7.3.
- **Impact:** S3: contract drift; UI would subscribe to undefined topics.

## ToDo

- [ ] Agree the resolution with the user (or record the decision in the progress log)
- [ ] Edit the source docs listed under Doc sync so they agree
- [ ] Update the affected P5 task files if the numbers/names change

## Verification

### Tests
- Doc review: every listed doc states the same value/name after the fix; `python3 tools/kanban/kanban.py validate` stays at 0 errors

### Scenarios
- Given the fixed docs, when a developer picks up the affected P5 tasks, then there is exactly one authoritative answer to follow

### Stress / failure injection
- n/a: documentation/spec gap

## Acceptance criteria

- [ ] Docs listed under Doc sync are consistent
- [ ] Affected P5 tasks reference the resolved value/name
- [ ] Resolution recorded in the progress log

## Exceptions & edge cases

- Until resolved, implementers use the suggested fix as the default and flag it in their PR description

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a looser (less safe) value; when in doubt choose the stricter option.
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/02-v1-architecture.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B005-ws-topics-wallet-treasury-missing`
- PR title: `P5-B005: D18 WebSocket topics `wallet`, `treasury`, `alert` are not in the 02 §7.3 topic list`

## Progress log

- 2026-10-21 00:00 · planner · opened
