---
id: P0-T043
kind: task
title: Deploy TEI for bge-small-en-v1.5 embeddings and bge-reranker-v2-m3
phase: 0
type: OPS
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T020]
requirements: [R0.09, R0.13]
roadmap_todos: [T0.41, T0.45, T0.28]
modules: [M21, M9]
dashboards: []
tools: [docker, curl]
mcp: []
env: []
services: [tei-embed, tei-rerank]
branch: p0/P0-T043-tei-embed-and-rerank
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T043 · Deploy TEI for bge-small-en-v1.5 embeddings and bge-reranker-v2-m3

## Goal / expected outcome

Two TEI containers (`tei-embed` with `BAAI/bge-small-en-v1.5`, `tei-rerank` with `BAAI/bge-reranker-v2-m3`) run digest-pinned on `core` with model revisions pinned and weights cached locally, answering `/embed` and `/rerank`.

## Context & references

- [Roadmap P0 R0.09](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [10 §2 embedders](../../../docs/10-memory-rag-and-models.md#2-local-embedders--rerankers)
- [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models) (TEI container)
- [02 §3.2 containers](../../../docs/02-v1-architecture.md#32-containers) (`tei-embed`, `tei-rerank` rows)
- Two containers (`tei-embed`, `tei-rerank`) decided in [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P0-B007, closed).
- Depends on: P0-T020

## Requirements

- Image `ghcr.io/huggingface/text-embeddings-inference:cpu-<ver>` by digest (GPU variant later if P0-T005 adds a GPU).
- `--model-id BAAI/bge-small-en-v1.5 --revision <sha>` (384 dims, 512 tokens) and `--model-id BAAI/bge-reranker-v2-m3 --revision <sha>`; weights in `/srv/mastertrader/models/hf` volume; `HF_HUB_OFFLINE=1` after first download.
- Health: `/health`; bound to `core` only; API key not supported by TEI → access restricted by network (no `edge`/`scrape` membership).
- Licences recorded in `third_party/LICENSES.md` (bge models MIT (U); TEI Apache-2.0).

## ToDo

- [ ] Add both services with pinned revisions and a one-time model download job.
- [ ] Add smoke tests.
- [ ] Record licences.

## Verification

### Tests
- Smoke: `/embed` of 3 strings returns 3×384 floats; `/rerank` ranks a relevant passage above an irrelevant one for a fixed query (golden).

### Scenarios
- Given HF Hub is unreachable after first download, when TEI restarts, then it serves from the cache (offline mode).

### Stress / failure injection
- Embed 1,000 short docs in batches of 32 on CPU; throughput logged (expect hundreds/s for bge-small).

## Acceptance criteria

- [ ] Both containers healthy and digest-pinned with pinned model revisions
- [ ] Smoke tests pass
- [ ] Licences recorded
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Rerank model memory on CPU (~2 GB): set `mem_limit` and `--max-batch-tokens` accordingly.

## Cardinal rules (do NOT)

- Do NOT use Ollama for embeddings under load (10 §2).
- Do NOT expose TEI outside `core`.
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.
- Do NOT put Telegram text into any model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/02-v1-architecture.md` §3.2: confirm the `tei-embed` / `tei-rerank` rows match the images and model revisions used.
- `docs/roadmap/phase-0-foundations.md`: tick T0.41, T0.45 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T043-tei-embed-and-rerank`
- PR title: `P0-T043: Deploy TEI for bge-small-en-v1.5 embeddings and bge-reranker-v2-m3`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T043` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (two TEI containers per 17 §D P0-B007 (closed); R0.13/T0.28; run fields added)
