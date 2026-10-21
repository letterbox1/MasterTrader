---
id: P5-B011
kind: gap
title: Discord delivery "N days" and "a few new servers a week" are unspecified
phase: 5
type: DOC
status: backlog
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R5.21]
roadmap_todos: []
modules: [M19]
dashboards: []
branch: p5/P5-B011-curation-n-days-weekly-cap-unspecified
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md]
doc_sync_status: n/a
found_in: "docs/08-airdrops-and-token-launches.md §Discord curation queue"
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-B011 · Discord delivery "N days" and "a few new servers a week" are unspecified

## Goal / expected outcome

Defaults exist for the re-prompt window and the weekly community cap.

## Context & references

- 08: "If nothing arrives within N days, it re-prompts you"; "a few new servers a week"
- Task P5-T047 uses N = 7 days and ≤ 3 servers/week

## Requirements

- **Steps to reproduce:** Read 08 §Discord curation queue.
- **Expected:** Numbers (configurable).
- **Actual:** Placeholders.
- **Suggested fix:** Set N = 7 days and ≤ 3 new servers/week as defaults in 08.
- **Impact:** S4: cosmetic/config default.

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

- `docs/08-airdrops-and-token-launches.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B011-curation-n-days-weekly-cap-unspecified`
- PR title: `P5-B011: Discord delivery "N days" and "a few new servers a week" are unspecified`

## Progress log

- 2026-10-21 00:00 · planner · opened
