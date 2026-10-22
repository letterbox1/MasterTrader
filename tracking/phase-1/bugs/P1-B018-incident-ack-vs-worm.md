---
id: P1-B018
kind: gap
title: D07 incident acknowledge maps to system.settings.update and conflicts with WORM
phase: 1
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.10, R1.15]
roadmap_todos: []
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p1/P1-B018-incident-ack-vs-worm
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/dashboards/D07-data-quality.md]
doc_sync_status: done
found_in: docs/ui/dashboards/D07-data-quality.md Actions; docs/02-v1-architecture.md §7.2; docs/15-bots-hitl-and-worm-audit.md §2
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-B018 · D07 incident acknowledge maps to system.settings.update and conflicts with WORM

## Goal / expected outcome

A dedicated command (e.g. `data.incident.ack`, C0) that appends an ack row referencing the incident (`supersedes_id`), listed in 02 §7.2

## Context & references

- Found in: D07 "Acknowledge incident → `system.settings.update` (incident ack), C0"; incidents live in WORM `audit.dq_event` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)) and cannot be updated; the command catalogue has no incident command
- Related items: P1-T030, P1-T046, P1-T048

## Requirements

- **Where:** D07 "Acknowledge incident → `system.settings.update` (incident ack), C0"; incidents live in WORM `audit.dq_event` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)) and cannot be updated; the command catalogue has no incident command
- **Expected:** A dedicated command (e.g. `data.incident.ack`, C0) that appends an ack row referencing the incident (`supersedes_id`), listed in 02 §7.2
- **Actual:** Settings command misused for incident state; an implementer might UPDATE a WORM row
- **Suggested fix:** Add `data.incident.ack` to 02 §7.2 Data group and D07 actions
- **Impact:** WORM violation risk (severity S3)

## ToDo

- [x] Decision recorded in docs/17 (17 §D P1-B018): incident acknowledgement is a new WORM row (`audit.dq_ack`) via `data.incident.ack` (C0), never an update
- [x] Aligned docs carry it: 02 §7.2 (Data commands); 03 M16 (Outputs), 03 M17; D07 (Quality tab, Acknowledge incident action)
- [x] Affected P1 tasks updated in the 2026-10-22 task alignment: P1-T030, P1-T046, P1-T048

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [x] Docs updated and consistent (02 §7.2 (Data commands); 03 M16 (Outputs), 03 M17; D07 (Quality tab, Acknowledge incident action))
- [x] Decision and owning tasks noted in the progress log

## Exceptions & edge cases

- Until fixed, related tasks follow the interim rule stated in their own files

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a number in code; the decision lands in the docs first
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/02-v1-architecture.md`: apply the fix above
- `docs/ui/dashboards/D07-data-quality.md`: apply the fix above

## Branch & PR

- Branch: `p1/P1-B018-incident-ack-vs-worm`
- PR title: `P1-B018: D07 incident acknowledge maps to system.settings.update and conflicts with WORM`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-B018` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D P1-B018; docs carry it (02 §7.2 (Data commands); 03 M16 (Outputs), 03 M17; D07 (Quality tab, Acknowledge incident action)); implementation owned by P1-T030, P1-T046, P1-T048
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P1-B018); docs updated: 02 §7.2 (Data commands); 03 M16 (Outputs), 03 M17; D07 (Quality tab, Acknowledge incident action); implementation owned by P1-T030, P1-T046, P1-T048
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
