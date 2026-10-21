---
id: P6-B007
kind: gap
title: D18 WebSocket topics `wallet`, `treasury`, `alert` are not in the 02 §7.3 topic list
phase: 6
type: DOC
status: backlog
priority: medium
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.40]
roadmap_todos: []
modules: []
dashboards: []
branch: p6/P6-B007-ws-topics-wallet-treasury-missing
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/dashboards/D18-wallets-treasury.md]
doc_sync_status: n/a
found_in: docs/ui/dashboards/D18-wallets-treasury.md (Backend contract) vs docs/02-v1-architecture.md §7.3
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-B007 · D18 WebSocket topics `wallet`, `treasury`, `alert` are not in the 02 §7.3 topic list

## Goal / expected outcome

The docs agree and are specific enough to build from: 02 §7.3 lists `wallet` and `treasury` topics, and D18 uses `notifications` (or 02 adds `alert`).

## Context & references

- Found in: docs/ui/dashboards/D18-wallets-treasury.md (Backend contract) vs docs/02-v1-architecture.md §7.3
- [D18](../../../docs/ui/dashboards/D18-wallets-treasury.md) · [02 §7.3](../../../docs/02-v1-architecture.md#73-real-time-websocket-apiv1ws)
- Affects: P6-T038, P6-T045

## Requirements

- **Steps to reproduce:** read docs/ui/dashboards/D18-wallets-treasury.md (Backend contract) vs docs/02-v1-architecture.md §7.3 and compare it with the cross-referenced sections listed under Context.
- **Expected:** 02 §7.3 lists `wallet` and `treasury` topics, and D18 uses `notifications` (or 02 adds `alert`).
- **Actual:** D18 subscribes to WS topics `wallet`, `treasury`, `alert`, `kill`; 02 §7.3 lists `kill` and `notifications` but no `wallet`, `treasury` or `alert` topic.
- **Suggested fix:** Add `wallet`, `treasury` to 02 §7.3; change D18 `alert` → `notifications`.
- **Impact:** Minor contract drift (severity S4)

## ToDo

- [ ] Propose the edits.
- [ ] Update the docs listed under Doc sync and link the resolving commit here.

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Topic lists consistent.
- [ ] Root cause noted in the progress log.

## Exceptions & edge cases

- Until resolved, dependent tasks use the conservative interpretation stated under Suggested fix and note it in their progress log.

## Cardinal rules (do NOT)

- Do NOT silently pick a number in code; record the decision in the doc first.
- Do NOT edit docs owned by another phase's planner from a P6 branch without the owner's agreement; propose the change in the PR description.

## Doc sync on completion

- `docs/02-v1-architecture.md`: resolve the inconsistency.
- `docs/ui/dashboards/D18-wallets-treasury.md`: resolve the inconsistency.

## Branch & PR

- Branch: `p6/P6-B007-ws-topics-wallet-treasury-missing`
- PR title: `P6-B007: D18 WebSocket topics `wallet`, `treasury`, `alert` are not in the 02 §7.3 topic list`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-B007` run

## Progress log

- 2026-10-21 00:00 · planner · created
