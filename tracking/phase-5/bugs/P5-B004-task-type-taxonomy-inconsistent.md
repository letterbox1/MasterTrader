---
id: P5-B004
kind: gap
title: Task-type names differ between 08, 03 M19, D13 and the roadmap
phase: 5
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R5.20]
roadmap_todos: []
modules: [M19]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p5/P5-B004-task-type-taxonomy-inconsistent
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/03-build-spec.md, docs/ui/dashboards/D13-tasks-curation.md]
doc_sync_status: done
found_in: "docs/08-airdrops-and-token-launches.md §User task queue; docs/ui/dashboards/D13-tasks-curation.md"
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P5-B004 · Task-type names differ between 08, 03 M19, D13 and the roadmap

## Goal / expected outcome

One canonical task-type enum used by all docs and `mt_curation`.

## Context & references

- 08 lists `TAX_RECORD`; D13 and P3 (T3.30) use `TAX_QUESTION`
- D13 adds FOLLOW_ANNOUNCEMENTS, JOIN_TELEGRAM, GENUINE_USE, PRO_ADVICE, VENUE_CHECK; 08 lacks them; R5.20 also lists approve-mode orders
- Task P5-T029 uses the union with TAX_RECORD as an alias

## Requirements

- **Steps to reproduce:** Compare the task-type lists in 08, 03 M19, D13 and R5.20.
- **Expected:** Identical lists.
- **Actual:** Different names and members.
- **Suggested fix:** Adopt the P5-T029 list: JOIN_DISCORD, FOLLOW_ANNOUNCEMENTS, JOIN_TELEGRAM, FOLLOW_X, QUEST, ONCHAIN_ACTION_MANUAL, CLAIM_MANUAL, ICO_REVIEW, REVOKE_APPROVAL, TAX_QUESTION, GENUINE_USE, PRO_ADVICE, VENUE_CHECK, APPROVE_ORDER; update 08/03/D13.
- **Impact:** S3: naming drift between UI, backend and docs.

## ToDo

- [x] Resolution recorded: Decided (17 §B P5-B004): one canonical task-type list in 03 M19 (JOIN_DISCORD, FOLLOW_ANNOUNCEMENTS, JOIN_TELEGRAM, FOLLOW_X, QUEST, ONCHAIN_ACTION_MANUAL, CLAIM_MANUAL, ICO_REVIEW, REVOKE_APPROVAL, TAX_QUESTION, GENUINE_USE, PRO_ADVICE, VENUE_CHECK, APPROVE_ORDER, REG_CHANGE); `TAX_RECORD` retired; table `curation.task`
- [x] Docs carry it: 03 M19 (canonical list + storage), 08 user task queue (same list, `curation.task`), D13 Inbox, roadmap R5.20/T5.30
- [x] P5 tasks aligned: P5-T009 (type constraint on `curation.task`), P5-T011 (enum), P5-T029 (queue), P5-T049 (D13)

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
- `docs/03-build-spec.md`: align with the resolution
- `docs/ui/dashboards/D13-tasks-curation.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B004-task-type-taxonomy-inconsistent`
- PR title: `P5-B004: Task-type names differ between 08, 03 M19, D13 and the roadmap`

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · aligned for docs/16–17: Decided (17 §B P5-B004): one canonical task-type list in 03 M19 (JOIN_DISCORD, FOLLOW_ANNOUNCEMENTS, JOIN_TELEGRAM, FOLLOW_X, QUEST, ONCHAIN_ACTION_MANUAL, CLAIM_MANUAL, ICO_REVIEW, REVOKE_APPROVAL, TAX_QUESTION, GENUINE_USE, PRO_ADVICE, VENUE_CHECK, APPROVE_ORDER, REG_CHANGE); `TAX_RECORD` retired; table `curation.task`. Docs checked: 03 M19 (canonical list + storage), 08 user task queue (same list, `curation.task`), D13 Inbox, roadmap R5.20/T5.30. Implementation owned by P5-T009 (type constraint on `curation.task`), P5-T011 (enum), P5-T029 (queue), P5-T049 (D13)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P5-B004); docs updated: 03 M19 (canonical list + storage), 08 user task queue (same list, `curation.task`), D13 Inbox, roadmap R5.20/T5.30; implementation owned by P5-T009 (type constraint on `curation.task`), P5-T011 (enum), P5-T029 (queue), P5-T049 (D13)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
