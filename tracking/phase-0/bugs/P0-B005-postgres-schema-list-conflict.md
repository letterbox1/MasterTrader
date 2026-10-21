---
id: P0-B005
kind: gap
title: Postgres schema lists disagree across docs
phase: 0
type: DOC
status: ready
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.03]
roadmap_todos: [T0.22]
modules: []
dashboards: []
branch: p0/P0-B005-postgres-schema-list-conflict
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: docs/roadmap/phase-0-foundations.md R0.03 vs docs/02-v1-architecture.md §5.1
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-B005 · Postgres schema lists disagree across docs

## Goal / expected outcome

The docs agree and the implementing tasks have one unambiguous answer. Suggested fix: P0 creates the nine in R0.03; add a 'schema → phase' table to 02 §5.1 (models P4/P6, rag P4, hindsight P6, treasury P5, research P6) and fix the 03 §3 comment.

## Context & references

- Found in: `docs/roadmap/phase-0-foundations.md R0.03 vs docs/02-v1-architecture.md §5.1`
- Related: P0-T024
- [02 §5.1 stores](../../../docs/02-v1-architecture.md#51-stores)
- [03 §3 repo layout](../../../docs/03-build-spec.md#3-repository-layout)

## Requirements

- **Steps to reproduce:** Compare R0.03 (9 schemas), 02 §5.1 (12: adds `models`, `rag`, `hindsight`), 02 §4 (`treasury.*`, `research.crowdsim_run`), 03 §3 mt_store comment (market, audit, journal, ops, curation).
- **Expected:** One authoritative schema list with the phase that creates each.
- **Actual:** Four different lists.
- **Impact:** P0 migrations may miss or pre-create schemas; later phases may collide.
- **Suggested fix:** P0 creates the nine in R0.03; add a 'schema → phase' table to 02 §5.1 (models P4/P6, rag P4, hindsight P6, treasury P5, research P6) and fix the 03 §3 comment.

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

- `docs/02-v1-architecture.md`: reconcile as described.
- `docs/03-build-spec.md`: reconcile as described.

## Branch & PR

- Branch: `p0/P0-B005-postgres-schema-list-conflict`
- PR title: `P0-B005: fix postgres schema lists disagree across docs`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B005` run

## Progress log

- 2026-10-21 00:00 · planner · opened
