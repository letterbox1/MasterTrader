---
id: P4-T051
kind: task
title: RAG retrieval benchmark and as_of leakage test
phase: 4
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T032]
requirements: [R4.07]
roadmap_todos: [T4.61]
modules: [M9]
dashboards: [D10]
branch: p4/P4-T051-verify-rag-benchmark-asof
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T051 · RAG retrieval benchmark and as_of leakage test

## Goal / expected outcome

A reproducible benchmark measures hybrid retrieval quality (recall@10, nDCG@10, MRR) for vector-only vs keyword-only vs RRF vs RRF+rerank(+decay) on a 100-query finance set over our corpus, plus latency p50/p95; and a leakage test proves no document ingested or published after `as_of` is ever returned.

## Context & references

- Roadmap: [R4.07](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.61](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Design: [10 §2 (FinMTEB: keyword beats dense on finance)](../../../docs/10-memory-rag-and-models.md#2-local-embedders--rerankers) · [10 §3](../../../docs/10-memory-rag-and-models.md#3-document-rag-design-postgres)

## Requirements

- Query set: 100 queries (filings sections, earnings, macro, crypto incidents) with graded relevant chunk ids, built semi-automatically and reviewed (stored in `tests/bench/rag_queries.jsonl`).
- Expect RRF+rerank ≥ each single retriever on nDCG@10; record numbers in MLflow and the doc.
- Leakage: 1,000 random `as_of` values over a corpus with future-dated and late-ingested docs (incl. approximate timestamps); assert zero violations.
- Latency p95 recorded vs the 300 ms target.

## ToDo

- [ ] Build and review the query set.
- [ ] Benchmark harness (`tools/bench/rag_bench.py`).
- [ ] Leakage property test in CI.
- [ ] Write results to MLflow and `docs/10` §3.

## Verification

### Tests
- Benchmark harness unit tests (metric implementations vs reference).
- Leakage property test (CI).

### Scenarios
- Given a doc published 2027-01-05 but ingested 2027-01-07, then a query at `as_of` 2027-01-06 never returns it.
- Given rerank disabled, then the benchmark reports the RRF-only row.

### Stress / failure injection
- Run the benchmark at 50 concurrent queries to record degraded latency.

## Acceptance criteria

- [ ] Benchmark table published (recall@10, nDCG@10, MRR, p50/p95) for all variants
- [ ] Leakage test: 0 violations
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- If RRF+rerank does not beat keyword-only, file a bug and keep keyword-weighted fusion (finance finding).

## Cardinal rules (do NOT)

- Do NOT tune on the test queries without a held-out split.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md`: §3: add benchmark results table
- `docs/roadmap/phase-4-intel.md`: tick T4.61 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T051-verify-rag-benchmark-asof`
- PR title: `P4-T051: RAG retrieval benchmark and as_of leakage test`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T051` run

## Progress log

- 2026-10-21 00:00 · planner · created
