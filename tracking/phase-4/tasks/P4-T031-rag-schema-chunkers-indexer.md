---
id: P4-T031
kind: task
title: Document RAG: rag schema, section-aware chunkers and indexer
phase: 4
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T027]
requirements: [R4.07]
roadmap_todos: [T4.24]
modules: [M9]
dashboards: [D08]
branch: p4/P4-T031-rag-schema-chunkers-indexer
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

# P4-T031 · Document RAG: rag schema, section-aware chunkers and indexer

## Goal / expected outcome

The `rag` schema holds `rag.doc_chunk(id, doc_id, source, tickers[], published_at, ingested_at, valid_from, section, text, tsv tsvector GENERATED, emb halfvec(384))` with HNSW/GIN/trigram/B-tree indexes, and an indexer chunks relevant documents (filings by Item/section with context headers, news one chunk per article) and inserts chunks with TEI embeddings, never updating in place.

## Context & references

- Roadmap: [R4.07](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.24](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Design: [10 §3 items 1, 3, 5](../../../docs/10-memory-rag-and-models.md#3-document-rag-design-postgres) · [03 M9](../../../docs/03-build-spec.md#m9-memory--rag--mt_memory)
- Gap: P4-B006 (`rag` schema ownership).
- Related: P4-T014 (filings), P4-T032 (retrieval).

## Requirements

- HNSW on `emb` (`halfvec_cosine_ops`, m=16, ef_construction=64); GIN on `tsv`; GIN trigram on tickers/entities; B-tree on `ingested_at` and `(ticker, published_at)`.
- Filings: split by Item (1A Risk Factors, 7 MD&A, …), then 512–800 tokens with ~15% overlap; tables become separate markdown chunks; header `{ticker} {form} {period} {section}`.
- News: one chunk per article; paragraph windows if > 800 tokens; wire copies already clustered (index only the cluster representative).
- Insert-only: a revision is a new chunk row with new `valid_from`.
- Only `model_input_ok=true` docs are indexed (guard); Telegram never.

## ToDo

- [ ] Migrations (`rag` schema, extension checks for pgvector/pg_trgm).
- [ ] Chunkers (`mt_memory.rag.chunk_filing`, `chunk_news`).
- [ ] Indexer consumer on `text.doc.new` (relevant only) + backfill command.
- [ ] Tests.

## Verification

### Tests
- Unit: 10-K fixture → Items detected, header present, overlap ≈ 15%.
- Unit: table extraction to markdown chunk.
- Integration: doc → chunks with embeddings; guard refuses a flagged doc.

### Scenarios
- Given a 10-K/A amends a section, then new chunks are added with later `valid_from`; old ones remain for PIT queries.
- Given TEI is down, then chunks are queued and embedded later (no partial rows without `emb`).

### Stress / failure injection
- Index 5,000 filings sections + 50k news: indexing throughput recorded; HNSW build time and index size recorded for P4-T051.

## Acceptance criteria

- [ ] Indexes created as specified; chunkers pass golden tests
- [ ] Guard enforced at indexer boundary
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Extremely long filings (S-1 > 300 pages): chunk lazily in a batch flow, not in the live consumer.

## Cardinal rules (do NOT)

- Do NOT UPDATE chunk rows.
- Do NOT use VectorChord or pg_textsearch (licence/PG17).
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md`: §3: confirm implemented DDL and chunk sizes
- `docs/roadmap/phase-4-intel.md`: tick T4.24 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T031-rag-schema-chunkers-indexer`
- PR title: `P4-T031: Document RAG: rag schema, section-aware chunkers and indexer`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T031` run

## Progress log

- 2026-10-21 00:00 · planner · created
