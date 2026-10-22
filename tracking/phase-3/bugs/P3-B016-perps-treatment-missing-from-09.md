---
id: P3-B016
kind: gap
title: Perpetual swaps treatment missing from AU_2026 rules and agent questions
phase: 3
type: DOC
status: done
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
doc_sync_status: done
found_in: docs/09-journal-and-tax.md §Jurisdiction plugin interface (AU_2026 row)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
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

- [x] Decision recorded in docs/17 (17 §D P3-B013/B014/B016): perpetual futures and funding are revenue by default (U); added to the tax-agent questions (Q8)
- [x] Owning docs carry it: 09 AU_2026 row + question 8; D15 Questions tab; roadmap R3.06
- [x] Affected tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P3-T024 (revenue rules), P3-T020 (derivative P&L), P3-T038 (question seed), P3-T001 (agent)
- [x] Decision and source noted in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T024, when they read the linked doc, then the rule is unambiguous.

### Stress / failure injection

- n/a: documentation/spec gap

## Acceptance criteria

- [x] Decision recorded in the owning doc (09 AU_2026 row + question 8; D15 Questions tab; roadmap R3.06)
- [x] Affected tasks consistent with it (P3-T024 (revenue rules), P3-T020 (derivative P&L), P3-T038 (question seed), P3-T001 (agent))
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

- Branch: `p3/P3-B016-perps-treatment-missing-from-09`
- PR title: `P3-B016: Perpetual swaps treatment missing from AU_2026 rules and agent questions`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-B016` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by docs/17 §D P3-B013/B014/B016: perpetual futures and funding are revenue by default (U); added to the tax-agent questions (Q8). Docs now carry it: 09 AU_2026 row + question 8; D15 Questions tab; roadmap R3.06. Implementation owned by P3-T024 (revenue rules), P3-T020 (derivative P&L), P3-T038 (question seed), P3-T001 (agent). Root cause: 09 omitted perps treatment.
- 2026-10-22 02:03 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P3-B013/B014/B016); docs updated: 09 AU_2026 row + question 8; D15 Questions tab; roadmap R3.06; implementation owned by P3-T024 (revenue rules), P3-T020 (derivative P&L), P3-T038 (question seed), P3-T001 (agent)
- 2026-10-22 02:03 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:03 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
