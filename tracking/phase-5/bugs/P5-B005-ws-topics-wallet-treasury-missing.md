---
id: P5-B005
kind: gap
title: D18 WebSocket topics `wallet`, `treasury`, `alert` are not in the 02 §7.3 topic list
phase: 5
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p5/P5-B005-ws-topics-wallet-treasury-missing
pr: ""
doc_sync: [docs/02-v1-architecture.md]
doc_sync_status: done
found_in: "docs/ui/dashboards/D18-wallets-treasury.md §Backend contract vs docs/02-v1-architecture.md §7.3"
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Resolution recorded: Decided (17 §D P5-B005): WS topics `wallet`, `treasury` and `alert` are in the API contract
- [x] Docs carry it: 02 §7.3 topic list (`alert`; `wallet` (P5), `treasury` (P6))
- [x] P5 tasks aligned: P5-T011 (topics), P5-T050 (D18 subscriptions)

## Verification

### Tests
- Doc review: every listed doc states the same value/name after the fix; `python3 tools/kanban/kanban.py validate` stays at 0 errors

### Scenarios
- Given the fixed docs, when a developer picks up the affected P5 tasks, then there is exactly one authoritative answer to follow

### Stress / failure injection
- n/a: documentation/spec gap

## Acceptance criteria

- [x] Docs listed under Doc sync (and the other docs named in the ToDo) state the decided value/name
- [x] Affected P5 tasks reference the decided value/name and an owning task exists
- [x] Resolution recorded in the progress log

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
- 2026-10-22 00:00 · aligner · aligned for docs/16–17: Decided (17 §D P5-B005): WS topics `wallet`, `treasury` and `alert` are in the API contract. Docs checked: 02 §7.3 topic list (`alert`; `wallet` (P5), `treasury` (P6)). Implementation owned by P5-T011 (topics), P5-T050 (D18 subscriptions)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P5-B005); docs updated: 02 §7.3 topic list (`alert`; `wallet` (P5), `treasury` (P6)); implementation owned by P5-T011 (topics), P5-T050 (D18 subscriptions)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
