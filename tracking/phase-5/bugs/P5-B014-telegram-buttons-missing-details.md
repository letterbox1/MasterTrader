---
id: P5-B014
kind: gap
title: Telegram task buttons in mobile-and-telegram.md omit Details
phase: 5
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R5.20]
roadmap_todos: []
modules: [M19, M15]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p5/P5-B014-telegram-buttons-missing-details
pr: ""
doc_sync: [docs/ui/mobile-and-telegram.md]
doc_sync_status: done
found_in: "docs/ui/mobile-and-telegram.md §3 (Tasks row)"
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P5-B014 · Telegram task buttons in mobile-and-telegram.md omit Details

## Goal / expected outcome

All docs list the same buttons: Done · Skip · Snooze 1d · Snooze 1w · Details · Never.

## Context & references

- 08 and R5.20 include Details; mobile doc lists Done · Skip · Snooze 1d · Snooze 1w · Never

## Requirements

- **Steps to reproduce:** Compare 08 §User task queue with mobile-and-telegram §3.
- **Expected:** Same list.
- **Actual:** Details missing.
- **Suggested fix:** Add Details (deep link to the task detail) to the mobile doc.
- **Impact:** S4: documentation only.

## ToDo

- [x] Resolution recorded: Decided (17 §D P5-B014): Telegram task buttons include Details (deep link to the task detail)
- [x] Docs carry it: ui/mobile-and-telegram §3 Tasks row (Done · Skip · Snooze 1d · Snooze 1w · Never · Details), D13 actions (Details), ui/components TaskCard, 08 Telegram buttons, roadmap R5.20
- [x] P5 tasks aligned: P5-T030 (Telegram buttons), P5-T049 (D13)

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

- `docs/ui/mobile-and-telegram.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B014-telegram-buttons-missing-details`
- PR title: `P5-B014: Telegram task buttons in mobile-and-telegram.md omit Details`

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · aligned for docs/16–17: Decided (17 §D P5-B014): Telegram task buttons include Details (deep link to the task detail). Docs checked: ui/mobile-and-telegram §3 Tasks row (Done · Skip · Snooze 1d · Snooze 1w · Never · Details), D13 actions (Details), ui/components TaskCard, 08 Telegram buttons, roadmap R5.20. Implementation owned by P5-T030 (Telegram buttons), P5-T049 (D13)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P5-B014); docs updated: ui/mobile-and-telegram §3 Tasks row (Done · Skip · Snooze 1d · Snooze 1w · Never · Details), D13 actions (Details), ui/components TaskCard, 08 Telegram buttons, roadmap R5.20; implementation owned by P5-T030 (Telegram buttons), P5-T049 (D13)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
