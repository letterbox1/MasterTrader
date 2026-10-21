---
id: P5-B004
kind: gap
title: Task-type names differ between 08, 03 M19, D13 and the roadmap
phase: 5
type: DOC
status: backlog
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
branch: p5/P5-B004-task-type-taxonomy-inconsistent
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/03-build-spec.md, docs/ui/dashboards/D13-tasks-curation.md]
doc_sync_status: n/a
found_in: "docs/08-airdrops-and-token-launches.md §User task queue; docs/ui/dashboards/D13-tasks-curation.md"
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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
- `docs/03-build-spec.md`: align with the resolution
- `docs/ui/dashboards/D13-tasks-curation.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B004-task-type-taxonomy-inconsistent`
- PR title: `P5-B004: Task-type names differ between 08, 03 M19, D13 and the roadmap`

## Progress log

- 2026-10-21 00:00 · planner · opened
