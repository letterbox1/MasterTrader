---
id: P1-B010
kind: gap
title: DQ, cost and recon audit table names differ across docs
phase: 1
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p1/P1-B010-audit-table-names-inconsistent
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md]
doc_sync_status: done
found_in: docs/03-build-spec.md M16; docs/02-v1-architecture.md §4 and §5.3; docs/roadmap/phase-1-data-and-monitoring.md R1.10
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Decision recorded in docs/17 (17 §B P0-B017/P1-B010/P8-B007): canonical singular names `audit.dq_event`, `audit.dq_ack`, `audit.cost_event`, `audit.recon`
- [x] Aligned docs carry it: 03 M16 (Outputs, Reconciliation), 03 M17; 02 §5.3 (`audit` row)
- [x] Affected P1 tasks updated in the 2026-10-22 task alignment: P1-T030, P1-T038, P1-T040 (TCA rows in `audit.cost_event`, no `audit.tca`), P1-T041

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [x] Docs updated and consistent (03 M16 (Outputs, Reconciliation), 03 M17; 02 §5.3 (`audit` row))
- [x] Decision and owning tasks noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by 17 §B P0-B017/P1-B010/P8-B007; docs carry it (03 M16 (Outputs, Reconciliation), 03 M17; 02 §5.3 (`audit` row)); implementation owned by P1-T030, P1-T038, P1-T040 (TCA rows in `audit.cost_event`, no `audit.tca`), P1-T041
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P0-B017/P1-B010/P8-B007); docs updated: 03 M16 (Outputs, Reconciliation), 03 M17; 02 §5.3 (`audit` row); implementation owned by P1-T030, P1-T038, P1-T040 (TCA rows in `audit.cost_event`, no `audit.tca`), P1-T041
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
