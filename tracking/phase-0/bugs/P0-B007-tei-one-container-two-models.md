---
id: P0-B007
kind: gap
title: One `tei` container can't serve both the embedder and the reranker
phase: 0
type: DOC
status: ready
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.09]
roadmap_todos: [T0.41, T0.45]
modules: []
dashboards: []
branch: p0/P0-B007-tei-one-container-two-models
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: docs/02-v1-architecture.md §3.2 (`tei` row)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-B007 · One `tei` container can't serve both the embedder and the reranker

## Goal / expected outcome

The docs agree and the implementing tasks have one unambiguous answer. Suggested fix: Split into `tei-embed` and `tei-rerank` in 02 §3.2 and 03 M21.

## Context & references

- Found in: `docs/02-v1-architecture.md §3.2 (`tei` row)`
- Related: P0-T043
- [02 §3.2 containers](../../../docs/02-v1-architecture.md#32-containers)
- [10 §2 embedders](../../../docs/10-memory-rag-and-models.md#2-local-embedders--rerankers)

## Requirements

- **Steps to reproduce:** R0.09 requires bge-small-en-v1.5 **and** bge-reranker-v2-m3 on TEI; 02 §3.2 lists one `tei` container.
- **Expected:** Two containers (`tei-embed`, `tei-rerank`) or an explicit alternative (fastembed in-process for one of them).
- **Actual:** TEI serves one model per instance; the single row is unimplementable as written.
- **Impact:** Minor: container list and memory budget are understated.
- **Suggested fix:** Split into `tei-embed` and `tei-rerank` in 02 §3.2 and 03 M21.

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

- Branch: `p0/P0-B007-tei-one-container-two-models`
- PR title: `P0-B007: fix one `tei` container can't serve both the embedder and the reranker`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B007` run

## Progress log

- 2026-10-21 00:00 · planner · opened
