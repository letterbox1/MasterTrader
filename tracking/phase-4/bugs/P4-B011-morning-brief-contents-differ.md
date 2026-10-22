---
id: P4-B011
kind: gap
title: Morning brief contents differ between 04, the roadmap and mobile-and-telegram
phase: 4
type: DOC
status: done
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
doc_sync_status: done
found_in: docs/04-plan-of-action.md Phase 4 demo; docs/roadmap/phase-4-intel.md R4.14; docs/ui/mobile-and-telegram.md §3 Digests
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
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

- [x] Decision recorded: morning-brief content is canonical in mobile-and-telegram §3 (17 §D)
- [x] Docs carry it: mobile-and-telegram §3 'Morning brief (canonical contents)' (8 items); 04 Phase 4 demo and roadmap R4.14 link to it; D08 links to it
- [x] Implementation owned by P4-T047 (brief job follows the canonical list) and P4-T060 (two-week run)

## Verification

### Tests
- Doc review: the corrected section is consistent with the linked sources (links resolve).

### Scenarios
- Given P5 adds airdrops, then the brief gains that section without a P4 change.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] One canonical brief list referenced by 04 and the roadmap (checked in docs/ui/mobile-and-telegram.md §3, 04 Phase 4, roadmap R4.14, 2026-10-22)
- [x] Root cause noted: three docs listed the brief independently

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
- 2026-10-22 00:00 · aligner · resolved by 17 §D (P4-B011); docs checked: docs/ui/mobile-and-telegram.md §3, 04 Phase 4 demo, roadmap R4.14, D08; implementation owned by P4-T047, P4-T060; root cause: three independent lists
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 §D (P4-B011); docs updated: docs/ui/mobile-and-telegram.md §3 canonical list, 04 Phase 4 demo, roadmap R4.14, D08; implementation owned by P4-T047, P4-T060
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
