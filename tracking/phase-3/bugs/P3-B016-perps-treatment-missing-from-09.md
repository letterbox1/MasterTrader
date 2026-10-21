---
id: P3-B016
kind: gap
title: Perpetual swaps treatment missing from AU_2026 rules and agent questions
phase: 3
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R3.06]
roadmap_todos: []
modules: [M18]
dashboards: []
branch: p3/P3-B016-perps-treatment-missing-from-09
pr: ""
doc_sync: [docs/09-journal-and-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: docs/09-journal-and-tax.md §Jurisdiction plugin interface (AU_2026 row)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-B016 · Perpetual swaps treatment missing from AU_2026 rules and agent questions

## Goal / expected outcome

AU_2026 states a default treatment for crypto perpetuals and funding, and the agent question list includes it.

## Context & references

- [09 AU_2026](../../../docs/09-journal-and-tax.md#jurisdiction-plugin-interface) covers CFDs, futures, forex, crypto spot; not perps
- Perps/funding are in scope ([R3.01](../../../docs/roadmap/phase-3-journal-and-tax.md) funding payments)
- Affects: P3-T024, P3-T038

## Requirements

- **Steps to reproduce:** Classify a BTC perp close and its funding in AU_2026 from 09.
- **Expected:** Default (revenue, (U)) + agent question.
- **Actual:** Not mentioned.
- **Impact:** Inconsistent classification of a core P2 product (funding carry). (severity S3)
- **Suggested fix:** Add "perps: revenue by default (U); funding revenue" to 09 and add the question to the seed list.

## ToDo

- [ ] Update 09 AU_2026 row and questions list
- [ ] Update the affected task files (P3-T024, P3-T038) if the decision differs from their default
- [ ] Note the decision and source in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T024, when they read the linked doc, then the rule is unambiguous.

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

- Branch: `p3/P3-B016-perps-treatment-missing-from-09`
- PR title: `P3-B016: Perpetual swaps treatment missing from AU_2026 rules and agent questions`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-B016` run

## Progress log

- 2026-10-21 00:00 · planner · opened
