---
id: P6-T051
kind: task
title: Optional: LightRAG offline graph over filings (research path)
phase: 6
type: BUILD
status: backlog
priority: low
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T003]
requirements: [R6.32]
roadmap_todos: [T6.30]
modules: [M9]
dashboards: [D10]
branch: p6/P6-T051-lightrag-filings-graph
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T051 · Optional: LightRAG offline graph over filings (research path)

## Goal / expected outcome

An offline batch LightRAG graph (suppliers, customers, subsidiaries, litigation) over EDGAR filings runs on Postgres for the research path only, point-in-time filtered, benchmarked against plain hybrid retrieval.

## Context & references

- Roadmap: [R6.32](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.30
- Optional: only if P6-T003 recorded `yes`; otherwise cancel this item.
- Spec: [10 §3](../../../docs/10-memory-rag-and-models.md#3-document-rag-design-postgres) item 7 · [10 §1](../../../docs/10-memory-rag-and-models.md#1-hindsight-self-hosted-agent-memory) (LightRAG needs ~30B-A3B-class model for extraction) · [03 M9](../../../docs/03-build-spec.md#m9-memory--rag--mt_memory)
- Depends on (this phase): P6-T003

## Requirements

- Batch extraction with a local ~30B-A3B model (GPU) or budgeted gateway role; never on the hot path.
- Graph nodes/edges carry filing `published_at`/`ingested_at`; queries filter `≤ as_of`.
- Benchmark vs P4 hybrid retrieval on a fixed question set; keep only if better.

## ToDo

- [ ] LightRAG (MIT) pinned; Postgres storage in `rag_graph` schema.
- [ ] Batch flow over a filings subset.
- [ ] Benchmark notebook.
- [ ] Docs.

## Verification

### Tests
- PIT: graph query as_of before a filing excludes its edges.
- Smoke batch on 10 filings.

### Scenarios
- Given a question about a supplier relationship, then the graph answer cites filing chunks.

### Stress / failure injection
- n/a: offline batch.

## Acceptance criteria

- [ ] Benchmark notes with keep/drop decision.

## Exceptions & edge cases

- GPU busy with production → batch deferred.

## Cardinal rules (do NOT)

- Do NOT use LightRAG outputs in live decisions in P6.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §3.7: results.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.30 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T051-lightrag-filings-graph`
- PR title: `P6-T051: Optional: LightRAG offline graph over filings (research path)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T051` run

## Progress log

- 2026-10-21 00:00 · planner · created
