---
id: P0-B005
kind: gap
title: Postgres schema lists disagree across docs
phase: 0
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p0/P0-B005-postgres-schema-list-conflict
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md]
doc_sync_status: done
found_in: docs/roadmap/phase-0-foundations.md R0.03 vs docs/02-v1-architecture.md §5.1
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Decision taken: 17 §B P0-B005 (ratified in 17 §E)
- [x] Docs updated so they agree: 03 §4 (13 schemas, all in P0) and §3 (`mt_store` comment); 02 §5.1 Stores row; 04 Phase 0; roadmap P0 R0.03
- [x] Affected P0 task files reference the resolution: P0-T024
- [x] Regression check owned: P0-T024 migration test (all 13 schemas exist)

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Listed docs carry the 17 §B P0-B005 decision and agree (checked in the alignment wave, 2026-10-22)
- [x] Implementation owned by: P0-T024
- [x] Root cause noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by 17 §B P0-B005; docs checked: 03 §4 (13 schemas, all in P0) and §3 (`mt_store` comment); 02 §5.1 Stores row; 04 Phase 0; roadmap P0 R0.03. Root cause: schemas were added per module in different docs without one canonical list. Implementation owned by P0-T024.
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P0-B005); docs updated: 03 §4 (13 schemas, all in P0) and §3 (`mt_store` comment); 02 §5.1 Stores row; 04 Phase 0; roadmap P0 R0.03; implementation owned by P0-T024
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
