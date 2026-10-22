---
id: P0-B011
kind: gap
title: Backup schedule and method differ across 07 §8, 02 §5.1 and F11
phase: 0
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.N4]
roadmap_todos: [T0.44]
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p0/P0-B011-backup-schedule-inconsistent
pr: ""
doc_sync: [docs/07-security-notes.md, docs/02-v1-architecture.md]
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

# P0-B011 · Backup schedule and method differ across 07 §8, 02 §5.1 and F11

## Goal / expected outcome

The docs agree and the implementing tasks have one unambiguous answer. Suggested fix: Adopt the P0-T039 schedule in all three places; drop pg_dump (monthly WORM Parquet export covers logical export needs).

## Context & references

- Found in: `docs/07-security-notes.md §8`
- Related: P0-T039
- [07 §8 backups & audit](../../../docs/07-security-notes.md#8-data-protection-backups--audit)
- [02 §5.1 stores](../../../docs/02-v1-architecture.md#51-stores)

## Requirements

- **Steps to reproduce:** Compare 07 §8 ('nightly pg_dump + WAL archiving (pgBackRest)'), 02 §5.1 ('full weekly, WAL continuous'), 02 F11 ('nightly backup → weekly full').
- **Expected:** One schedule: weekly full + daily diff + continuous WAL (pgBackRest), no separate pg_dump.
- **Actual:** Three phrasings; 07 adds pg_dump.
- **Impact:** Low: duplicate or missing backup jobs.
- **Suggested fix:** Adopt the P0-T039 schedule in all three places; drop pg_dump (monthly WORM Parquet export covers logical export needs).

## ToDo

- [x] Decision taken: 17 §B P0-B011 (ratified in 17 §E)
- [x] Docs updated so they agree: 07 §8 (no separate `pg_dump`); 02 §5.1 Postgres row and §8 F11; 15 §2.2 Backups row; D16 Backups schedule; 04 Phase 0; roadmap P0 R0.N4
- [x] Affected P0 task files reference the resolution: P0-T039, P0-T051, P0-T060
- [x] Regression check owned: P0-T039 schedule config and P0-T057 first real run

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Listed docs carry the 17 §B P0-B011 decision and agree (checked in the alignment wave, 2026-10-22)
- [x] Implementation owned by: P0-T039
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- If the user decides differently from the suggestion, the affected tasks are updated before they start.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/07-security-notes.md`: reconcile as described.
- `docs/02-v1-architecture.md`: reconcile as described.

## Branch & PR

- Branch: `p0/P0-B011-backup-schedule-inconsistent`
- PR title: `P0-B011: fix backup schedule and method differ across 07 §8, 02 §5.1 and F11`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B011` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §B P0-B011; docs checked: 07 §8 (no separate `pg_dump`); 02 §5.1 Postgres row and §8 F11; 15 §2.2 Backups row; D16 Backups schedule; 04 Phase 0; roadmap P0 R0.N4. Root cause: three docs described the schedule independently. Implementation owned by P0-T039.
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P0-B011); docs updated: 07 §8 (no separate `pg_dump`); 02 §5.1 Postgres row and §8 F11; 15 §2.2 Backups row; D16 Backups schedule; 04 Phase 0; roadmap P0 R0.N4; implementation owned by P0-T039
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
