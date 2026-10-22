---
id: P0-B017
kind: gap
title: Audit table names drift across docs (07 §8, 03 M16, 02 §4)
phase: 0
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.03, R0.07]
roadmap_todos: [T0.22]
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p0/P0-B017-audit-table-naming-drift
pr: ""
doc_sync: [docs/07-security-notes.md, docs/03-build-spec.md]
doc_sync_status: done
found_in: docs/07-security-notes.md §8
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-B017 · Audit table names drift across docs (07 §8, 03 M16, 02 §4)

## Goal / expected outcome

The docs agree and the implementing tasks have one unambiguous answer. Suggested fix: Adopt 02 §4 names (singular, schema-qualified); update 07 §8 and 03 M16; `mt_store.lint` can enforce singular names.

## Context & references

- Found in: `docs/07-security-notes.md §8`
- Related: P0-T024, P0-T031
- [02 §5.1 stores](../../../docs/02-v1-architecture.md#51-stores)

## Requirements

- **Steps to reproduce:** Compare 07 §8 (`order_audit`, `risk_change_audit`, `journal_entry`), 03 M16 (`audit.dq_events`, `audit.cost_events`) and 02 §4 (`audit.order`, `risk.change`, `audit.dq_event`, `audit.cost_event`).
- **Expected:** One naming convention (schema-qualified, singular) used everywhere.
- **Actual:** Three conventions.
- **Impact:** Low: later migrations may create duplicates or mismatched names.
- **Suggested fix:** Adopt 02 §4 names (singular, schema-qualified); update 07 §8 and 03 M16; `mt_store.lint` can enforce singular names.

## ToDo

- [x] Decision taken: 17 §B P0-B017 (ratified in 17 §E)
- [x] Docs updated so they agree: 15 §2.1, 02 §4/§5.3 and design rule, 03 §4 `audit` list, D16 Audit list all use the canonical singular names; no `order_audit`/`risk_change_audit`/`dq_events`/`cost_events` remain in docs
- [x] Affected P0 task files reference the resolution: P0-T031, P0-T038, P0-T055
- [x] Regression check owned: grep of docs for the old names returns nothing

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Listed docs carry the 17 §B P0-B017 decision and agree (checked in the alignment wave, 2026-10-22)
- [x] Implementation owned by: P0-T031 (canonical tables; `mt_store.lint` singular-name rule)
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- If the user decides differently from the suggestion, the affected tasks are updated before they start.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/07-security-notes.md`: reconcile as described.
- `docs/03-build-spec.md`: reconcile as described.

## Branch & PR

- Branch: `p0/P0-B017-audit-table-naming-drift`
- PR title: `P0-B017: fix audit table names drift across docs (07 §8, 03 M16, 02 §4)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B017` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §B P0-B017; docs checked: 15 §2.1, 02 §4/§5.3 and design rule, 03 §4 `audit` list, D16 Audit list all use the canonical singular names; no `order_audit`/`risk_change_audit`/`dq_events`/`cost_events` remain in docs. Root cause: three docs named the audit tables independently. Implementation owned by P0-T031 (canonical tables; `mt_store.lint` singular-name rule).
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P0-B017); docs updated: 15 §2.1, 02 §4/§5.3 and design rule, 03 §4 `audit` list, D16 Audit list all use the canonical singular names; no `order_audit`/`risk_change_audit`/`dq_events`/`cost_events` remain in docs; implementation owned by P0-T031 (canonical tables; `mt_store.lint` singular-name rule)
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
