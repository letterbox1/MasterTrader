---
id: P6-T011
kind: task
title: Hindsight slim container on our Postgres, TEI and the gateway
phase: 6
type: OPS
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.04]
roadmap_todos: [T6.40]
modules: [M9]
dashboards: [D10]
branch: p6/P6-T011-hindsight-slim-container
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/02-v1-architecture.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T011 · Hindsight slim container on our Postgres, TEI and the gateway

## Goal / expected outcome

A `hindsight` service (Hindsight 1.0.0 **slim** image, pinned by digest) runs on the internal network against our Postgres 16 in schema `hindsight`, using TEI for embeddings/rerank and LiteLLM (role `memory`) for retain/consolidate/reflect.

## Context & references

- Roadmap: [R6.04](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.40
- Spec: [10 §1](../../../docs/10-memory-rag-and-models.md#1-hindsight-self-hosted-agent-memory) (deployment table, env vars, 384-d warning) · [03 M9](../../../docs/03-build-spec.md#m9-memory--rag--mt_memory) · [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) (`hindsight` container, phase 6) · [07 §5](../../../docs/07-security-notes.md#5-network--host)
- Gap: P6-B005 (`hindsight` schema not in P0's schema list)
- Cross-phase: P0 R0.02 Compose, R0.09 TEI + LiteLLM

## Requirements

- Env: `HINDSIGHT_API_DATABASE_URL` (least-privilege role), `HINDSIGHT_API_DATABASE_SCHEMA=hindsight`, `VECTOR_EXTENSION=pgvector`, `TEXT_SEARCH_EXTENSION=native`, `HINDSIGHT_API_EMBEDDINGS_PROVIDER=tei` (bge-small-en-v1.5, **384-d**), `HINDSIGHT_API_RERANKER_PROVIDER=tei`, `HINDSIGHT_API_LLM_PROVIDER=litellm` with the `memory` virtual key; for local models `HINDSIGHT_API_LLM_STRICT_SCHEMA=true`, `RETAIN_MAX_COMPLETION_TOKENS` > 3000.
- Reranker candidate count lowered from 300 (start at 100) to keep recall 100–600 ms.
- API :8888 and UI :9999 bound to the internal network only; no published ports; OpenTelemetry/Prometheus opt-in to our stack only.
- Footprint budget: 0.5–1 GB RAM (slim).
- Backups: the `hindsight` schema is covered by pgBackRest like every other schema.

## ToDo

- [ ] Add the service to `docker-compose.yml` with image digest, healthcheck, resource limits, internal network.
- [ ] Create the `hindsight` schema and DB role via Alembic (owner role separate from the app role).
- [ ] Secrets (DB password, LiteLLM `memory` key) via sops → tmpfs.
- [ ] Outbound-traffic check: no phone-home (tcpdump/egress deny test).
- [ ] Smoke: create bank, retain one item, recall it.
- [ ] Docs.

## Verification

### Tests
- Compose health check green; smoke retain/recall script in CI (compose profile).
- Port scan from the Tailscale side shows 8888/9999 closed.
- Egress test: container has no route except Postgres, TEI, LiteLLM.

### Scenarios
- Given TEI is down, when Hindsight recalls, then it errors cleanly and `mt_memory` reports memory unavailable (handled in P6-T012).
- Given the embedding model is changed by mistake, then startup refuses because stored dimension 384 ≠ new dimension.

### Stress / failure injection
- Restart Postgres during a retain: Hindsight reconnects; retain retried by the caller with the same idempotency key.

## Acceptance criteria

- [ ] Service healthy, digest-pinned, internal-only.
- [ ] Smoke retain/recall passes.
- [ ] No egress beyond allowed services.

## Exceptions & edge cases

- No GPU: TEI CPU is fine for bge-small; retain is LLM-bound (seconds).
- Re-embedding (future Qwen3-Embedding) is a planned migration, never an in-place change.

## Cardinal rules (do NOT)

- Do NOT use the full ~9 GB image or its bundled models.
- Do NOT expose the Hindsight MCP endpoint (`/mcp/{bank_id}/`) before Phase 8.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §1: confirmed env values and digest.
- `docs/02-v1-architecture.md` §5.1: `hindsight` schema listed with backup coverage.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.40 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T011-hindsight-slim-container`
- PR title: `P6-T011: Hindsight slim container on our Postgres, TEI and the gateway`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T011` run

## Progress log

- 2026-10-21 00:00 · planner · created
