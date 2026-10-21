---
id: P4-T027
kind: task
title: nlp stages: FinBERT sentiment, TEI embeddings, store and publish
phase: 4
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T026]
requirements: [R4.06]
roadmap_todos: [T4.23]
modules: [M2, M9]
dashboards: [D08]
branch: p4/P4-T027-nlp-finbert-embeddings-store
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T027 · nlp stages: FinBERT sentiment, TEI embeddings, store and publish

## Goal / expected outcome

Relevant, provenance-cleared documents get FinBERT sentiment (positive/negative/neutral probabilities) and a bge-small-en-v1.5 384-d embedding from TEI, are written to `text.document` (approximate timestamps flagged), handed to the RAG indexer (P4-T031), and announced on `text.doc.new` with id, tickers and scores.

## Context & references

- Roadmap: [R4.06](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.23](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Flow: [02 F3](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · Embedders: [10 §2](../../../docs/10-memory-rag-and-models.md#2-local-embedders--rerankers) (TEI, bge-small 384-d, embedding cache)
- Cross-phase: P0 R0.09 (TEI container).

## Requirements

- FinBERT (ProsusAI/finbert, pinned revision) via ONNX Runtime CPU, batch 16; sentence-windowed for long docs, aggregated by length-weighted mean.
- Embeddings from TEI (`/embed`), cached by `sha256(model||text)` in `rag.emb_cache`.
- `text.doc.new` payload: `{id, source, tickers, published_at, published_approx, sentiment, relevance, dup_cluster}` (schema versioned).
- End-to-end ingest → `text.doc.new` p95 < 3 s (so D08 can show within 5 s).

## ToDo

- [ ] FinBERT ONNX export + runner.
- [ ] TEI client with cache + retry + circuit breaker.
- [ ] Writer + publisher.
- [ ] Metrics (stage latencies, cache hit rate).
- [ ] Tests.

## Verification

### Tests
- Unit: FinBERT on 20 labelled finance sentences matches expected label ≥ 85%.
- Unit: embedding cache hit on identical text.
- Integration: raw item → `text.doc.new` with scores.

### Scenarios
- Given TEI is down, then documents are stored with `emb=null`, `text.doc.new` still fires, and a backfill job embeds them on recovery.
- Given a doc has `display_ok=false`, then it is still scored if `model_input_ok=true`, but the body is not exposed to the UI.

### Stress / failure injection
- 2,000 docs in 10 min: p95 ingest→publish < 3 s, CPU < 4 cores.

## Acceptance criteria

- [ ] p95 ingest→`text.doc.new` < 3 s under normal load
- [ ] Sentiment + embedding present on ≥ 99% of eligible docs in a 24-h run
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- GPU absent: FinBERT stays on CPU (it is small).
- Postgres down (02 §9.3): consumers pause and resume from the JetStream durable cursor; no item lost or duplicated.

## Cardinal rules (do NOT)

- Do NOT score Telegram or any `model_input_ok=false` row (guarded by P4-T025).
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT use unpinned images (`:latest`) or vendored code with telemetry/referral IDs; pin by digest.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.

## Doc sync on completion

- `docs/02-v1-architecture.md`: §6: `text.doc.new` payload schema
- `docs/roadmap/phase-4-intel.md`: tick T4.23 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T027-nlp-finbert-embeddings-store`
- PR title: `P4-T027: nlp stages: FinBERT sentiment, TEI embeddings, store and publish`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T027` run

## Progress log

- 2026-10-21 00:00 · planner · created
