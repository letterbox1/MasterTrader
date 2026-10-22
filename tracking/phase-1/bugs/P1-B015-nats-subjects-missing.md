---
id: P1-B015
kind: gap
title: recon.* and dq.raw.* subjects are missing from the NATS subject table
phase: 1
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.10, R1.12]
roadmap_todos: []
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p1/P1-B015-nats-subjects-missing
pr: ""
doc_sync: [docs/02-v1-architecture.md]
doc_sync_status: done
found_in: docs/02-v1-architecture.md §4 vs §6
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-B015 · recon.* and dq.raw.* subjects are missing from the NATS subject table

## Goal / expected outcome

02 §6 lists `recon.{venue}` and `dq.raw.*` with payloads, producers and consumers

## Context & references

- Found in: 02 §4 says M16 publishes `recon.*` and M1 publishes `dq.raw.*`; WebSocket topic `recon` exists (02 §7.3); 02 §6 subject table lists neither
- Related items: P1-T004, P1-T010, P1-T041

## Requirements

- **Where:** 02 §4 says M16 publishes `recon.*` and M1 publishes `dq.raw.*`; WebSocket topic `recon` exists (02 §7.3); 02 §6 subject table lists neither
- **Expected:** 02 §6 lists `recon.{venue}` and `dq.raw.*` with payloads, producers and consumers
- **Actual:** Subjects missing from the authoritative table
- **Suggested fix:** Add both rows to 02 §6 (as implemented in P1-T004/T010/T041)
- **Impact:** Schema drift between services (severity S4)

## ToDo

- [x] Decision recorded in docs/17 (17 §D P1-B011/P1-B015): add `recon.*` and `dq.raw.*` to the 02 §6 subject table
- [x] Aligned docs carry it: 02 §6 (`dq.raw.{venue}.{symbol}` and `recon.{venue}` rows)
- [x] Affected P1 tasks updated in the 2026-10-22 task alignment: P1-T004, P1-T010, P1-T041

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [x] Docs updated and consistent (02 §6 (`dq.raw.{venue}.{symbol}` and `recon.{venue}` rows))
- [x] Decision and owning tasks noted in the progress log

## Exceptions & edge cases

- Until fixed, related tasks follow the interim rule stated in their own files

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a number in code; the decision lands in the docs first
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/02-v1-architecture.md`: apply the fix above

## Branch & PR

- Branch: `p1/P1-B015-nats-subjects-missing`
- PR title: `P1-B015: recon.* and dq.raw.* subjects are missing from the NATS subject table`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-B015` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D P1-B011/P1-B015; docs carry it (02 §6 (`dq.raw.{venue}.{symbol}` and `recon.{venue}` rows)); implementation owned by P1-T004, P1-T010, P1-T041
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P1-B011/P1-B015); docs updated: 02 §6 (`dq.raw.{venue}.{symbol}` and `recon.{venue}` rows); implementation owned by P1-T004, P1-T010, P1-T041
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
