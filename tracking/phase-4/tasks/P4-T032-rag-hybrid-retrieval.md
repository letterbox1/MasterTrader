---
id: P4-T032
kind: task
title: Document RAG retrieval: hybrid search, RRF, rerank, recency decay, as_of filter, caches
phase: 4
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T031]
requirements: [R4.07]
roadmap_todos: [T4.24]
modules: [M9]
dashboards: [D08]
branch: p4/P4-T032-rag-hybrid-retrieval
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/02-v1-architecture.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T032 · Document RAG retrieval: hybrid search, RRF, rerank, recency decay, as_of filter, caches

## Goal / expected outcome

`mt_memory.rag.search(query, as_of, filters)` returns provenance-carrying chunks using vector top-50 + keyword top-50, **RRF** in SQL (`Σ 1/(60+rank)`), cross-encoder rerank of the top 30–50 via TEI `/rerank` (bge-reranker-v2-m3), recency decay, and a mandatory `ingested_at <= :as_of AND published_at <= :as_of` filter; exposed as `/rag/search` (incl. `?similar=` for D08 related docs) with embedding and retrieval caches.

## Context & references

- Roadmap: [R4.07](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.24](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Design: [10 §3 items 2, 4, 6](../../../docs/10-memory-rag-and-models.md#3-document-rag-design-postgres) · [03 M9](../../../docs/03-build-spec.md#m9-memory--rag--mt_memory)
- API: [02 §7.1](../../../docs/02-v1-architecture.md#7-api-contract-mt_api) `/rag/search`
- Verified by P4-T051 (benchmark + leakage).

## Requirements

- `as_of` is a **required** argument (no default); the SQL always applies both PIT predicates; `as_of` in the future is clamped to now.
- Filtered vector queries set `hnsw.iterative_scan = relaxed_order` and `ef_search` 100–200.
- Recency decay: score × exp(−Δt/τ), τ configurable per source type (news 3 d, filings 365 d).
- Retrieval cache keyed by `(query, as_of bucket (5 min), filters)`; embedding cache shared with P4-T027.
- Returns chunk id, doc id, source, section, published/ingested times, scores per stage.
- Latency target p95 < 300 ms end-to-end on CPU incl. rerank of 30.
- Guard: results never include `model_input_ok=false` chunks (defence in depth).

## ToDo

- [ ] SQL for vector, keyword (websearch_to_tsquery), RRF CTE.
- [ ] Rerank client + decay.
- [ ] Caches.
- [ ] `/rag/search` handler (through P4-T043 router).
- [ ] Tests incl. PIT property test.

## Verification

### Tests
- Property: for random `as_of`, no returned chunk has `ingested_at > as_of` or `published_at > as_of`.
- Unit: RRF score matches a reference implementation.
- Integration: rerank changes order as expected on a fixture.

### Scenarios
- Given TEI rerank is down, then return RRF order with `reranked=false` flag.
- Given a backtest at 2027-02-01 asks about a company, then documents ingested later are never returned even if published earlier.

### Stress / failure injection
- 200 concurrent queries: p95 < 300 ms target recorded; cache hit-rate reported.

## Acceptance criteria

- [ ] PIT property test green
- [ ] Latency recorded vs target
- [ ] `/rag/search` used by D08 related docs
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Docs with approximate `published_at`: PIT uses `ingested_at` as the binding predicate; both still applied.

## Cardinal rules (do NOT)

- Do NOT add an `as_of`-less code path.
- Do NOT bypass `pit(as_of)` conventions for research callers.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md`: §3: measured latency and decay τ
- `docs/02-v1-architecture.md`: §7.1: `/rag/search` params
- `docs/roadmap/phase-4-intel.md`: tick T4.24 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T032-rag-hybrid-retrieval`
- PR title: `P4-T032: Document RAG retrieval: hybrid search, RRF, rerank, recency decay, as_of filter, caches`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T032` run

## Progress log

- 2026-10-21 00:00 · planner · created
