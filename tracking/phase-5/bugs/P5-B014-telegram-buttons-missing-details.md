---
id: P5-B014
kind: gap
title: Telegram task buttons in mobile-and-telegram.md omit Details
phase: 5
type: DOC
status: backlog
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
branch: p5/P5-B014-telegram-buttons-missing-details
pr: ""
doc_sync: [docs/ui/mobile-and-telegram.md]
doc_sync_status: n/a
found_in: "docs/ui/mobile-and-telegram.md §3 (Tasks row)"
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- `docs/ui/mobile-and-telegram.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B014-telegram-buttons-missing-details`
- PR title: `P5-B014: Telegram task buttons in mobile-and-telegram.md omit Details`

## Progress log

- 2026-10-21 00:00 · planner · opened
