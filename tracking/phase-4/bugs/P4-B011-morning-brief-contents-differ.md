---
id: P4-B011
kind: gap
title: Morning brief contents differ between 04, the roadmap and mobile-and-telegram
phase: 4
type: DOC
status: backlog
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R4.14]
roadmap_todos: []
modules: [M15]
dashboards: []
branch: p4/P4-B011-morning-brief-contents-differ
pr: ""
doc_sync: [docs/ui/mobile-and-telegram.md, docs/04-plan-of-action.md]
doc_sync_status: n/a
found_in: docs/04-plan-of-action.md Phase 4 demo; docs/roadmap/phase-4-intel.md R4.14; docs/ui/mobile-and-telegram.md §3 Digests
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-B011 · Morning brief contents differ between 04, the roadmap and mobile-and-telegram

## Goal / expected outcome

One canonical list of brief sections, referenced by all three docs.

## Context & references

- Found in: [R4.14](../../../docs/roadmap/phase-4-intel.md#3-requirements) (news, sentiment movers, events, calendar + blackouts, data/cost health) vs [mobile-and-telegram §3](../../../docs/ui/mobile-and-telegram.md#3-telegram-bot) (positions, P&L, overnight news/events, calendar + blackouts, data health, new vetted airdrops)
- Related: P4-T047 implements the union (airdrops added in P5).

## Requirements

- **Steps to reproduce:** compare the three lists.
- **Expected:** one list: news, sentiment movers, events→assets, calendar + blackouts, Telegram postures (numbers), positions/P&L, data/cost health, airdrops (from P5).
- **Actual:** three slightly different lists.
- **Impact:** S4.
- **Suggested fix:** make mobile-and-telegram §3 canonical and link it from 04/roadmap.

## ToDo

- [ ] Agree the fix with the doc owner (main agent / user)
- [ ] Edit the listed docs (outside this phase folder; done by whoever owns those docs)
- [ ] Re-run `./kanban validate` and link the commit here

## Verification

### Tests
- Doc review: the corrected section is consistent with the linked sources (links resolve).

### Scenarios
- Given P5 adds airdrops, then the brief gains that section without a P4 change.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Docs updated as described under Requirements
- [ ] Root cause noted in the progress log

## Exceptions & edge cases

- None.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/ui/mobile-and-telegram.md`: §3 canonical brief list
- `docs/04-plan-of-action.md`: link

## Branch & PR

- Branch: `p4/P4-B011-morning-brief-contents-differ`
- PR title: `P4-B011: fix morning brief contents differ between 04, the roadmap and mobile-and-telegram`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-B011` run

## Progress log

- 2026-10-21 00:00 · planner · opened
