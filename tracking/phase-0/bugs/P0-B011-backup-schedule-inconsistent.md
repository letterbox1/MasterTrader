---
id: P0-B011
kind: gap
title: Backup schedule and method differ across 07 §8, 02 §5.1 and F11
phase: 0
type: DOC
status: ready
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
branch: p0/P0-B011-backup-schedule-inconsistent
pr: ""
doc_sync: [docs/07-security-notes.md, docs/02-v1-architecture.md]
doc_sync_status: n/a
found_in: docs/07-security-notes.md §8
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- [ ] Confirm the decision with the user (or take the suggested fix if no objection)
- [ ] Update the listed docs so they agree
- [ ] Update the affected P0 task files' Context if the decision differs from the suggestion
- [ ] Add/adjust a regression check where one is possible (see Verification)

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Listed docs updated and consistent
- [ ] Affected tasks reference the resolution
- [ ] Root cause (how the drift happened) noted in the progress log

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
