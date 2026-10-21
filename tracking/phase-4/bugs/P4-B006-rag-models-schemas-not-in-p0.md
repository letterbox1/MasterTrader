---
id: P4-B006
kind: gap
title: `rag` and `models` schemas missing from the P0 schema list
phase: 4
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R4.07, R4.12]
roadmap_todos: []
modules: [M9, M21]
dashboards: []
branch: p4/P4-B006-rag-models-schemas-not-in-p0
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md, docs/02-v1-architecture.md]
doc_sync_status: n/a
found_in: docs/roadmap/phase-0-foundations.md R0.03 vs docs/02-v1-architecture.md §5.1
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-B006 · `rag` and `models` schemas missing from the P0 schema list

## Goal / expected outcome

Schema ownership is explicit: either P0 creates `rag`, `models` (and `hindsight`) empty, or the docs say P4 creates `rag`/`models` and P6 creates `hindsight`.

## Context & references

- Found in: [phase-0 R0.03](../../../docs/roadmap/phase-0-foundations.md#3-requirements) lists `market, text, features, strategy, risk, audit, journal, curation, ops`
- [02 §5.1](../../../docs/02-v1-architecture.md#51-stores) lists also `models`, `rag`, `hindsight`
- Related: P4-T028 and P4-T031 create the schemas idempotently.

## Requirements

- **Steps to reproduce:** compare the two lists.
- **Expected:** one owner per schema, with grants (app roles, WORM for `audit.tierb_decision`).
- **Actual:** `rag` and `models` have no creating phase.
- **Impact:** S3 — migration ordering/grants may be missed.
- **Suggested fix:** amend R0.03 or note in 02 §5.1 which phase creates each schema.

## ToDo

- [ ] Agree the fix with the doc owner (main agent / user)
- [ ] Edit the listed docs (outside this phase folder; done by whoever owns those docs)
- [ ] Re-run `./kanban validate` and link the commit here

## Verification

### Tests
- Doc review: the corrected section is consistent with the linked sources (links resolve).

### Scenarios
- Given P0 already created the schemas, then P4 migrations are no-ops (`CREATE SCHEMA IF NOT EXISTS`).

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Docs updated as described under Requirements
- [ ] Root cause noted in the progress log

## Exceptions & edge cases

- None.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/roadmap/phase-0-foundations.md`: R0.03 schema list (or a note)
- `docs/02-v1-architecture.md`: §5.1 owner note

## Branch & PR

- Branch: `p4/P4-B006-rag-models-schemas-not-in-p0`
- PR title: `P4-B006: fix `rag` and `models` schemas missing from the P0 schema list`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-B006` run

## Progress log

- 2026-10-21 00:00 · planner · opened
