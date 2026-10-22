---
id: P4-B006
kind: gap
title: `rag` and `models` schemas missing from the P0 schema list
phase: 4
type: DOC
status: done
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
doc_sync_status: done
found_in: docs/roadmap/phase-0-foundations.md R0.03 vs docs/02-v1-architecture.md §5.1
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
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

- [x] Decision recorded: all 13 schemas (incl. `rag`, `models`, `hindsight`) are created in P0 (17 §B)
- [x] Docs carry it: roadmap phase-0 R0.03 ('all 13 are created in P0; later phases only add tables'); 02 §5.1 ('all 13 schemas created in P0')
- [x] Implementation: P0 creates the schemas (P0-T024); P4-T028 and P4-T031 now only add tables

## Verification

### Tests
- Doc review: the corrected section is consistent with the linked sources (links resolve).

### Scenarios
- Given P0 already created the schemas, then P4 migrations are no-ops (`CREATE SCHEMA IF NOT EXISTS`).

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Schema ownership explicit (checked in docs/roadmap/phase-0-foundations.md R0.03 and 02 §5.1, 2026-10-22)
- [x] Root cause noted: R0.03's list predated the `rag`/`models` schemas in 02

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
- 2026-10-22 00:00 · aligner · resolved by 17 §B (P0-B005, P4-B006); docs checked: docs/roadmap/phase-0-foundations.md R0.03, 02 §5.1; implementation owned by n/a in P4 (P0-T024 creates the schemas; P4-T028/P4-T031 add tables only); root cause: R0.03 list was older than 02 §5.1
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 §B (P0-B005, P4-B006); docs updated: docs/roadmap/phase-0-foundations.md R0.03 (all 13 schemas in P0), 02 §5.1; implementation owned by n/a in P4 (P0-T024; P4-T028/T031 add tables only)
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
