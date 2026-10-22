---
id: P3-B014
kind: gap
title: CommSec statements listed in 09 architecture but not in R3.01
phase: 3
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R3.01]
roadmap_todos: []
modules: [M18]
dashboards: []
branch: p3/P3-B014-commsec-in-09-not-in-r301
pr: ""
doc_sync: [docs/09-journal-and-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: done
found_in: docs/09-journal-and-tax.md §Architecture
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P3-B014 · CommSec statements listed in 09 architecture but not in R3.01

## Goal / expected outcome

R3.01 and 09 list the same broker statement formats.

## Context & references

- [09 architecture](../../../docs/09-journal-and-tax.md#architecture) lists IBKR Flex, CommSec, OANDA, IG
- R3.01 lists IBKR Flex, OANDA, IG
- Affects: P3-T003, P3-T015

## Requirements

- **Steps to reproduce:** Compare the two lists.
- **Expected:** Same list (or CommSec marked optional).
- **Actual:** CommSec only in 09.
- **Impact:** Trivial; possible missing adapter if you hold CommSec shares. (severity S4)
- **Suggested fix:** Mark CommSec as optional/later in 09 unless you use it (then add an adapter task).

## ToDo

- [x] Decision recorded in docs/17 (17 §D P3-B013/B014/B016): CommSec is optional in R3.01 (optional/later in 09)
- [x] Owning docs carry it: 09 architecture (CommSec optional/later); roadmap R3.01
- [x] Affected tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by n/a (no CommSec adapter in P3; P3-T003/P3-T015 note it as optional)
- [x] Decision and source noted in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T003, when they read the linked doc, then the rule is unambiguous.

### Stress / failure injection

- n/a: documentation/spec gap

## Acceptance criteria

- [x] Decision recorded in the owning doc (09 architecture (CommSec optional/later); roadmap R3.01)
- [x] Affected tasks consistent with it (n/a (no CommSec adapter in P3; P3-T003/P3-T015 note it as optional))
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- Until resolved, the affected tasks use the default stated in their Requirements and label it (U).

## Cardinal rules (do NOT)

- Do NOT resolve by editing WORM data; spec changes apply to new computations (superseding rows).
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."

## Doc sync on completion

- `docs/09-journal-and-tax.md`: record the decision.
- `docs/roadmap/phase-3-journal-and-tax.md`: no ToDo box to tick; note the outcome under §7 Risks if it changes a risk or open question.

## Branch & PR

- Branch: `p3/P3-B014-commsec-in-09-not-in-r301`
- PR title: `P3-B014: CommSec statements listed in 09 architecture but not in R3.01`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-B014` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by docs/17 §D P3-B013/B014/B016: CommSec is optional in R3.01 (optional/later in 09). Docs now carry it: 09 architecture (CommSec optional/later); roadmap R3.01. Implementation owned by n/a (no CommSec adapter in P3; P3-T003/P3-T015 note it as optional). Root cause: 09 listed CommSec while R3.01 did not.
- 2026-10-22 02:03 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P3-B013/B014/B016); docs updated: 09 architecture (CommSec optional/later); roadmap R3.01; implementation owned by n/a (no CommSec adapter in P3; P3-T003/P3-T015 note it as optional)
- 2026-10-22 02:03 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:03 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
