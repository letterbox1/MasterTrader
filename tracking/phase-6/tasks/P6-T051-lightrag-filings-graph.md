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
depends_on: [P6-T003, P4-T031, P1-T077]
requirements: [R6.35]
roadmap_todos: [T6.35]
modules: [M9, mt-memory]
dashboards: [D10]
tools: [git, cargo, docker]
mcp: []
env: []
services: [supabase-postgres, litellm, tei-embed, mt-scheduler]
branch: p6/P6-T051-lightrag-filings-graph
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/19-third-party-register.md, docs/18-platform-and-deployment.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-T051 · Optional: LightRAG offline graph over filings (research path)

## Goal / expected outcome

An offline batch LightRAG graph (suppliers, customers, subsidiaries, litigation) over EDGAR filings serves the research path only, point-in-time filtered, benchmarked against plain hybrid retrieval. LightRAG (MIT, Python) runs **unmodified as a separate, digest-pinned third-party container** (its own server and REST API, the same pattern as Hindsight, [18 §2.3](../../../docs/18-platform-and-deployment.md#23-third-party-services-any-language-run-unmodified-as-pinned-containers)); we write no Python around it: an `mt-scheduler` job feeds it filing chunks and `mt-memory` queries it over HTTP.

## Context & references

- Roadmap: [R6.35](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.35
- Optional module, off by default (P6-T003, 16 §2.14a); built once you enable it in settings.
- Spec: [10 §3](../../../docs/10-memory-rag-and-models.md#3-document-rag-design-postgres) item 7 · [10 §1](../../../docs/10-memory-rag-and-models.md#1-hindsight-self-hosted-agent-memory) (LightRAG needs ~30B-A3B-class model for extraction) · [03 M9](../../../docs/03-build-spec.md#m9-memory--rag)
- Depends on (this phase): P6-T003
- Cross-phase: P4-T031 (`rag` schema, chunker)

## Requirements

- Container `lightrag` (official server image pinned by digest, telemetry check, internal network only, bound to `127.0.0.1`, API key required: a generated `MT_LIGHTRAG_API_KEY` line goes into `.env.example` §14 first); its LLM and embedding calls point at the LiteLLM gateway and TEI.
- Batch extraction with a local ~30B-A3B model (GPU profile) or a budgeted gateway role (CPU profile, `models.gpu_profile: auto`); never on the hot path.
- Storage: LightRAG's Postgres backends in the `rag` schema (`lightrag_*` tables) where they work on Supabase; its Postgres graph store needs Apache AGE (U: not offered on Supabase), so otherwise the graph uses its default file store on a local volume.
- Graph nodes/edges carry filing `published_at`/`ingested_at`; an entity merged from several filings carries the latest source time. `mt-memory` filters every answer `≤ as_of` (LightRAG itself has no `as_of`), or the research run uses a graph snapshot built only from filings `≤ as_of`.
- Benchmark vs P4 hybrid retrieval on a fixed question set; keep only if better.

## ToDo

- [ ] `lightrag` container pinned by digest (MIT, unmodified); storage per the requirement above; API key wiring.
- [ ] `mt-scheduler` batch job that sends a filings subset to the LightRAG insert API; `mt-memory` HTTP client with the `as_of` filter.
- [ ] Benchmark report (fixed question set: P4 hybrid retrieval vs the graph) stored with the run; exploration notebooks optional in `mt_research`.
- [ ] Docs.

## Verification

### Tests
- `cargo test -p mt-memory lightrag` (HTTP client and `as_of` filter on recorded responses).
- PIT: graph query as_of before a filing excludes its edges.
- Smoke batch on 10 filings.

### Scenarios
- Given a question about a supplier relationship, then the graph answer cites filing chunks.

### Stress / failure injection
- n/a: offline batch.

## Acceptance criteria

- [ ] Benchmark notes with keep/drop decision.

## Exceptions & edge cases

- GPU busy with production (GPU profile) → batch deferred.
- Optional module, **off by default** (P6-T003 records `modules.*.enabled: false`). Build it only once you enable it in settings; while it stays off at phase exit, P6-T066 cancels this item with reason "optional module off by default (P6-T003)" and it can be re-opened any time you enable it.

## Cardinal rules (do NOT)

- Do NOT use LightRAG outputs in live decisions in P6.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §3.7: results.
- `docs/19-third-party-register.md` §1 and `docs/18-platform-and-deployment.md` §2.3: add LightRAG as a run-unmodified service (MIT).
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.35 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T051-lightrag-filings-graph`
- PR title: `P6-T051: Optional: LightRAG offline graph over filings (research path)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T051` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (cross-phase dep P4-T031; run fields)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (optional module off by default; extraction model per `models.gpu_profile: auto`; gpu service removed)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (LightRAG kept optional (16 §2.14a) and run unmodified as a third-party container per 18 §2.3, not as a Python package (not in 18 §2.2); batch via `mt-scheduler`, PIT filter in `mt-memory`; R6.32 → R6.35, T6.30 → T6.35; tools cargo)
