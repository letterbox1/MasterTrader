---
id: P3-B014
kind: gap
title: CommSec statements listed in 09 architecture but not in R3.01
phase: 3
type: DOC
status: backlog
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
doc_sync_status: n/a
found_in: docs/09-journal-and-tax.md §Architecture
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
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

- [ ] Confirm with the user whether CommSec is used; update 09 or add a task
- [ ] Update the affected task files (P3-T003, P3-T015) if the decision differs from their default
- [ ] Note the decision and source in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T003, when they read the linked doc, then the rule is unambiguous.

### Stress / failure injection

- n/a: documentation/spec gap

## Acceptance criteria

- [ ] Decision recorded in the owning doc
- [ ] Affected tasks consistent with it
- [ ] Root cause noted in the progress log

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
