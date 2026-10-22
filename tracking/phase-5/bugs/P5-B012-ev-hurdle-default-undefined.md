---
id: P5-B012
kind: gap
title: EV hurdle default refers to a treasury yield that 13 §5 does not define
phase: 5
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p5/P5-B012-ev-hurdle-default-undefined
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/13-wallets-treasury-and-onchain.md]
doc_sync_status: done
found_in: "docs/08-airdrops-and-token-launches.md §Expected value gate"
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Resolution recorded: Decided (17 §C P5-B012): EV hurdle default 5% p.a. on capital locked (AUD cash-rate proxy), configurable; stays a fixed default until the P6 treasury has a live stablecoin yield you choose to use
- [x] Docs carry it: 16 §2.7 (EV hurdle row), 08 EV gate (`capital_lockup_cost` at 5% p.a.), 13 §5 (EV hurdle), 03 M4, roadmap R5.14/T5.06
- [x] P5 tasks aligned: P5-T040 (EV gate reads the setting), P5-T007 (USER review)

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

- `docs/08-airdrops-and-token-launches.md`: align with the resolution
- `docs/13-wallets-treasury-and-onchain.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B012-ev-hurdle-default-undefined`
- PR title: `P5-B012: EV hurdle default refers to a treasury yield that 13 §5 does not define`

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · aligned for docs/16–17: Decided (17 §C P5-B012): EV hurdle default 5% p.a. on capital locked (AUD cash-rate proxy), configurable; stays a fixed default until the P6 treasury has a live stablecoin yield you choose to use. Docs checked: 16 §2.7 (EV hurdle row), 08 EV gate (`capital_lockup_cost` at 5% p.a.), 13 §5 (EV hurdle), 03 M4, roadmap R5.14/T5.06. Implementation owned by P5-T040 (EV gate reads the setting), P5-T007 (USER review)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §C P5-B012); docs updated: 16 §2.7 (EV hurdle row), 08 EV gate (`capital_lockup_cost` at 5% p.a.), 13 §5 (EV hurdle), 03 M4, roadmap R5.14/T5.06; implementation owned by P5-T040 (EV gate reads the setting), P5-T007 (USER review)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
