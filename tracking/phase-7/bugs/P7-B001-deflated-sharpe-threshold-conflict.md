---
id: P7-B001
kind: gap
title: Deflated Sharpe gate threshold stated three different ways
phase: 7
type: DOC
status: done
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
doc_sync_status: done
found_in: docs/03-build-spec.md §8 item 2 / item 7; docs/02-v1-architecture.md §13; docs/14-strategy-evidence-and-validation.md §6–§7
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
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

- [x] Decision recorded in docs/17 (17 §B P7-B001/P2-B060): deflated Sharpe ratio (DSR) is a probability; gate passes at DSR ≥ 0.95 ("> 0" was an error), a gate-profile default
- [x] Owning docs carry it: 16 §2.4; 03 §8 items 2 and 7; 02 §13 item 2; 14 §6 gate 2 and §7 paper row
- [x] Affected Phase 7 tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P7-T012
- [x] Decision and root cause noted in the progress log

## Verification

### Tests
- Doc review: the cited sections now state one consistent rule; affected task files reference it.

### Scenarios
- Given an implementer reads only the fixed docs, then they implement the same behaviour the Phase 7 tasks assume.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (16 §2.4; 03 §8 items 2 and 7; 02 §13 item 2; 14 §6 gate 2 and §7 paper row)
- [x] Affected tasks consistent with it (P7-T012)
- [x] Root cause noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by docs/17 17 §B P7-B001/P2-B060: deflated Sharpe ratio (DSR) is a probability; gate passes at DSR ≥ 0.95 ("> 0" was an error), a gate-profile default. Docs now carry it: 16 §2.4; 03 §8 items 2 and 7; 02 §13 item 2; 14 §6 gate 2 and §7 paper row. Implementation owned by P7-T012. Root cause: 03 §8 item 2 and 02 §13 stated "DSR > 0" while other sections said 0.95.
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P7-B001/P2-B060); docs updated: 16 §2.4; 03 §8 items 2 and 7; 02 §13 item 2; 14 §6 gate 2 and §7 paper row; implementation owned by P7-T012
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
