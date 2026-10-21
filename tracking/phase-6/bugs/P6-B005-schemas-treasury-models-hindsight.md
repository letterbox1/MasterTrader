---
id: P6-B005
kind: gap
title: Schema lists disagree: `treasury`, `models`, `rag`, `hindsight` missing from P0/03 §4; wallet registry named both `treasury.wallet` and `ops.wallets`
phase: 6
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.04, R6.20]
roadmap_todos: []
modules: []
dashboards: []
branch: p6/P6-B005-schemas-treasury-models-hindsight
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: docs/02-v1-architecture.md §4 vs §5.1; docs/03-build-spec.md §4; docs/roadmap/phase-0-foundations.md R0.03; docs/roadmap/phase-5-airdrops-wallets-curation.md R5.05
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-B005 · Schema lists disagree: `treasury`, `models`, `rag`, `hindsight` missing from P0/03 §4; wallet registry named both `treasury.wallet` and `ops.wallets`

## Goal / expected outcome

The docs agree and are specific enough to build from: one schema list (02 §5.1 = 03 §4 = P0 R0.03 + later-phase additions) and one name for the wallet registry.

## Context & references

- Found in: docs/02-v1-architecture.md §4 vs §5.1; docs/03-build-spec.md §4; docs/roadmap/phase-0-foundations.md R0.03; docs/roadmap/phase-5-airdrops-wallets-curation.md R5.05
- [02 §4](../../../docs/02-v1-architecture.md#4-logical-components) (M22 owns `treasury.wallet`, `treasury.transfer`, `treasury.position`, `treasury.policy`) · [02 §5.1](../../../docs/02-v1-architecture.md#51-stores) (no `treasury` schema; lists `models`, `rag`, `hindsight`) · [03 §4](../../../docs/03-build-spec.md#4-data-model-overview) (lists neither)
- Affects: P6-T011, P6-T033, P6-T038

## Requirements

- **Steps to reproduce:** read docs/02-v1-architecture.md §4 vs §5.1; docs/03-build-spec.md §4; docs/roadmap/phase-0-foundations.md R0.03; docs/roadmap/phase-5-airdrops-wallets-curation.md R5.05 and compare it with the cross-referenced sections listed under Context.
- **Expected:** one schema list (02 §5.1 = 03 §4 = P0 R0.03 + later-phase additions) and one name for the wallet registry.
- **Actual:** 02 §4 assigns tables in a `treasury` schema, but 02 §5.1 and 03 §4 have no `treasury` schema; P5 R5.05 uses `ops.wallets`; P0 R0.03 creates only nine schemas (no `models`, `rag`, `hindsight`), though 02 §5.1 lists them.
- **Suggested fix:** Add `treasury` (or move M22 tables to `ops`) consistently; state which phase creates `models`/`rag`/`hindsight` (P4 for `models`/`rag`, P6 for `hindsight`, `treasury`). Interim: P6 creates `hindsight` and `treasury` via its own migrations and references P5's `ops.wallets`.
- **Impact:** Migrations may diverge between phases (severity S3)

## ToDo

- [ ] Inventory schemas across docs.
- [ ] Propose one list with creating phase.
- [ ] Update the docs listed under Doc sync and link the resolving commit here.

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] 02 §4, §5.1, 03 §4 and P0/P5 roadmaps agree.
- [ ] Root cause noted in the progress log.

## Exceptions & edge cases

- Until resolved, dependent tasks use the conservative interpretation stated under Suggested fix and note it in their progress log.

## Cardinal rules (do NOT)

- Do NOT silently pick a number in code; record the decision in the doc first.
- Do NOT edit docs owned by another phase's planner from a P6 branch without the owner's agreement; propose the change in the PR description.

## Doc sync on completion

- `docs/02-v1-architecture.md`: resolve the inconsistency.
- `docs/03-build-spec.md`: resolve the inconsistency.

## Branch & PR

- Branch: `p6/P6-B005-schemas-treasury-models-hindsight`
- PR title: `P6-B005: Schema lists disagree: `treasury`, `models`, `rag`, `hindsight` missing from P0/03 §4; wallet registry named both `treasury.wallet` and `ops.wallets``
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-B005` run

## Progress log

- 2026-10-21 00:00 · planner · created
