---
id: P5-B012
kind: gap
title: EV hurdle default refers to a treasury yield that 13 §5 does not define
phase: 5
type: DOC
status: backlog
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R5.14]
roadmap_todos: []
modules: [M4]
dashboards: []
branch: p5/P5-B012-ev-hurdle-default-undefined
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/13-wallets-treasury-and-onchain.md]
doc_sync_status: n/a
found_in: "docs/08-airdrops-and-token-launches.md §Expected value gate"
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-B012 · EV hurdle default refers to a treasury yield that 13 §5 does not define

## Goal / expected outcome

A concrete default hurdle rate exists until P6's treasury yield is live.

## Context & references

- 08: "hurdle rate (default: the treasury yield in 13 §5)"
- 13 §5 has no yield figure; P6 builds the allocator
- USER item P5-T007 sets it

## Requirements

- **Steps to reproduce:** Look up the treasury yield in 13 §5.
- **Expected:** A figure or a rule.
- **Actual:** None.
- **Suggested fix:** Default to the RBA cash rate + 1% (or a fixed 5% p.a.) until P6 provides a live stablecoin yield; user-editable.
- **Impact:** S4: EV gate needs a number; user can set it.

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
- `docs/13-wallets-treasury-and-onchain.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B012-ev-hurdle-default-undefined`
- PR title: `P5-B012: EV hurdle default refers to a treasury yield that 13 §5 does not define`

## Progress log

- 2026-10-21 00:00 · planner · opened
