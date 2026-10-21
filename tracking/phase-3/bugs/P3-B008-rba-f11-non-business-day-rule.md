---
id: P3-B008
kind: gap
title: No rule for RBA F11 rates on weekends, holidays or currencies not in F11
phase: 3
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R3.03]
roadmap_todos: []
modules: [M18]
dashboards: []
branch: p3/P3-B008-rba-f11-non-business-day-rule
pr: ""
doc_sync: [docs/09-journal-and-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: docs/09-journal-and-tax.md §Goals (item 5)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-B008 · No rule for RBA F11 rates on weekends, holidays or currencies not in F11

## Goal / expected outcome

09 specifies which RBA rate applies to an event on a non-publication day and how non-F11 currencies are converted.

## Context & references

- [09 goals §5](../../../docs/09-journal-and-tax.md#goals) · [11 §3 base currency](../../../docs/11-cryptotrader-crossover-review.md#3-conflicts-and-how-they-were-resolved)
- Affects: P3-T010

## Requirements

- **Steps to reproduce:** Stamp a Saturday crypto→USD event in AUD.
- **Expected:** Prior business day F11 rate, flagged; USD cross for non-F11 currencies.
- **Actual:** Only "RBA daily rate".
- **Impact:** Inconsistent AUD values across modules/exports. (severity S3)
- **Suggested fix:** Adopt P3-T010's rule in 09 (and confirm with the agent if they prefer another ATO-accepted rate source).

## ToDo

- [ ] Add the rule to 09
- [ ] Update the affected task files (P3-T010) if the decision differs from their default
- [ ] Note the decision and source in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T010, when they read the linked doc, then the rule is unambiguous.

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

- Branch: `p3/P3-B008-rba-f11-non-business-day-rule`
- PR title: `P3-B008: No rule for RBA F11 rates on weekends, holidays or currencies not in F11`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-B008` run

## Progress log

- 2026-10-21 00:00 · planner · opened
