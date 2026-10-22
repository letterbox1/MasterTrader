---
id: P0-B007
kind: gap
title: One `tei` container can't serve both the embedder and the reranker
phase: 0
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p0/P0-B007-tei-one-container-two-models
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md]
doc_sync_status: done
found_in: docs/02-v1-architecture.md §3.2 (`tei` row)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Decision taken: 17 §D P0-B007 (ratified in 17 §E)
- [x] Docs updated so they agree: 02 §3.1 + §3.2 (`tei-embed`, `tei-rerank` rows); 03 §2 Models row + M21; 10 §2 table and §5 roles; 04 Phase 0; roadmap P0 R0.09/R0.13/T0.28
- [x] Affected P0 task files reference the resolution: P0-T043, P0-T021, P0-T042
- [x] Regression check owned: P0-T043 smoke tests on both containers

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Listed docs carry the 17 §D P0-B007 decision and agree (checked in the alignment wave, 2026-10-22)
- [x] Implementation owned by: P0-T043
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

- Branch: `p0/P0-B007-tei-one-container-two-models`
- PR title: `P0-B007: fix one `tei` container can't serve both the embedder and the reranker`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B007` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D P0-B007; docs checked: 02 §3.1 + §3.2 (`tei-embed`, `tei-rerank` rows); 03 §2 Models row + M21; 10 §2 table and §5 roles; 04 Phase 0; roadmap P0 R0.09/R0.13/T0.28. Root cause: the container table predated the decision to run a reranker. Implementation owned by P0-T043.
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P0-B007); docs updated: 02 §3.1 + §3.2 (`tei-embed`, `tei-rerank` rows); 03 §2 Models row + M21; 10 §2 table and §5 roles; 04 Phase 0; roadmap P0 R0.09/R0.13/T0.28; implementation owned by P0-T043
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
