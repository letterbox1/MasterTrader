---
id: P7-B001
kind: gap
title: Deflated Sharpe gate threshold stated three different ways
phase: 7
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.01]
roadmap_todos: []
modules: []
dashboards: []
branch: p7/P7-B001-deflated-sharpe-threshold-conflict
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/14-strategy-evidence-and-validation.md]
doc_sync_status: n/a
found_in: docs/03-build-spec.md §8 item 2 / item 7; docs/02-v1-architecture.md §13; docs/14-strategy-evidence-and-validation.md §6–§7
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-B001 · Deflated Sharpe gate threshold stated three different ways

## Goal / expected outcome

The docs agree and are specific enough to implement: rewrite 03 §8 item 2 and 02 §13 item 2 as 'deflated Sharpe probability > 0.95 (see item 7)', and make 14 §7's paper row use the same wording.

## Context & references

- Found in: `docs/03-build-spec.md §8 item 2 / item 7; docs/02-v1-architecture.md §13; docs/14-strategy-evidence-and-validation.md §6–§7`
- Related: P7-T012

## Requirements

- **What:** The deflated Sharpe pass rule differs across docs.
- **Expected:** One rule: deflated Sharpe probability (DSR) > 0.95 (equivalently: deflated SR > 0 at 95% confidence), as in R7.01.
- **Actual:** 03 §8 item 2 and 02 §13 say 'deflated Sharpe > 0'; 03 §8 item 7 and 14 §6 say '> 0.95'; 14 §7 says 'deflated Sharpe > 0 at 95%'.
- **Impact:** The gate evaluator (P7-T012) could implement the looser '> 0' reading and pass strategies that should fail. (severity S3)
- **Suggested fix:** Rewrite 03 §8 item 2 and 02 §13 item 2 as 'deflated Sharpe probability > 0.95 (see item 7)', and make 14 §7's paper row use the same wording.

## ToDo

- [ ] Confirm the conflict/omission against the cited sections
- [ ] Agree the resolution (the user decides where it changes risk or money rules)
- [ ] Edit the docs listed under Doc sync in one PR
- [ ] Update any Phase 7 task text that depended on the assumption

## Verification

### Tests
- Doc review: the cited sections now state one consistent rule; affected task files reference it.

### Scenarios
- Given an implementer reads only the fixed docs, then they implement the same behaviour the Phase 7 tasks assume.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Docs updated and consistent
- [ ] Root cause noted in the progress log

## Exceptions & edge cases

- If the user picks a different resolution than suggested, update the dependent Phase 7 tasks in the same PR.

## Cardinal rules (do NOT)

- Do NOT resolve a conflict by picking the looser number.
- Do NOT edit generated files (`KANBAN.md`, boards, README marked blocks) by hand.

## Doc sync on completion

- `docs/03-build-spec.md`: apply the agreed fix.
- `docs/02-v1-architecture.md`: apply the agreed fix.
- `docs/14-strategy-evidence-and-validation.md`: apply the agreed fix.

## Branch & PR

- Branch: `p7/P7-B001-deflated-sharpe-threshold-conflict`
- PR title: `P7-B001: fix deflated Sharpe gate threshold stated three different ways`
- PR checklist: doc fix or regression test · root cause in the progress log · `./kanban done` run

## Progress log

- 2026-10-21 00:00 · planner · opened
