---
id: P1-B010
kind: gap
title: DQ, cost and recon audit table names differ across docs
phase: 1
type: DOC
status: backlog
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.10, R1.11, R1.12]
roadmap_todos: []
modules: []
dashboards: []
branch: p1/P1-B010-audit-table-names-inconsistent
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md]
doc_sync_status: n/a
found_in: docs/03-build-spec.md M16; docs/02-v1-architecture.md §4 and §5.3; docs/roadmap/phase-1-data-and-monitoring.md R1.10
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-B010 · DQ, cost and recon audit table names differ across docs

## Goal / expected outcome

One name per table (singular, matching 02 §4: `audit.dq_event`, `audit.cost_event`, `audit.recon`)

## Context & references

- Found in: 03 M16 uses `audit.dq_events` / `audit.cost_events`; 02 §4 and R1.10 use `audit.dq_event` / `audit.cost_event`; 02 §4 says `audit.recon` while 02 §5.3 lists `recon_result`
- Related items: P1-T030, P1-T038, P1-T041

## Requirements

- **Where:** 03 M16 uses `audit.dq_events` / `audit.cost_events`; 02 §4 and R1.10 use `audit.dq_event` / `audit.cost_event`; 02 §4 says `audit.recon` while 02 §5.3 lists `recon_result`
- **Expected:** One name per table (singular, matching 02 §4: `audit.dq_event`, `audit.cost_event`, `audit.recon`)
- **Actual:** Plural/singular and recon names conflict
- **Suggested fix:** Use the 02 §4 names in 03 M16 and 02 §5.3
- **Impact:** Migration naming churn (severity S4)

## ToDo

- [ ] Edit 03 M16 and 02 §5.3
- [ ] Update the affected P1 task files if the decision changes their requirements

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [ ] Docs updated and consistent
- [ ] Root cause and decision noted in the progress log

## Exceptions & edge cases

- Until fixed, related tasks follow the interim rule stated in their own files

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a number in code; the decision lands in the docs first
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/03-build-spec.md`: apply the fix above
- `docs/02-v1-architecture.md`: apply the fix above

## Branch & PR

- Branch: `p1/P1-B010-audit-table-names-inconsistent`
- PR title: `P1-B010: DQ, cost and recon audit table names differ across docs`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-B010` run

## Progress log

- 2026-10-21 00:00 · planner · opened
