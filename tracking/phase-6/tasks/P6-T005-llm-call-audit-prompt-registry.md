---
id: P6-T005
kind: task
title: Audit every LLM call and version prompts and models
phase: 6
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.03]
roadmap_todos: [T6.20]
modules: [M17, M21, M8]
dashboards: [D10]
branch: p6/P6-T005-llm-call-audit-prompt-registry
pr: ""
doc_sync: [docs/03-build-spec.md, docs/10-memory-rag-and-models.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T005 · Audit every LLM call and version prompts and models

## Goal / expected outcome

Every call through the LiteLLM gateway (agents, explain, memory, shadow, strategy-gen, chat) lands as a WORM row in `audit.llm_call` with model, prompt/response hashes and text, tokens, cost and latency; prompts live in a versioned registry so every call names its `prompt_version`.

## Context & references

- Roadmap: [R6.03](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.20
- Spec: [03 M17](../../../docs/03-build-spec.md#m17-observability--audit--mt_obs) (every LLM call: model, prompt/response hash + text, tokens, cost, latency) · [03 M8](../../../docs/03-build-spec.md#m8-ai-decision-layer--mt_agents) (prompts/models versioned) · [10 §5](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21)
- WORM: [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)
- Gaps: P6-B001 (R6.03 has no ToDo), P6-B010 (gateway used since P2 without this writer)
- Cross-phase: P0 R0.07 WORM, R0.09 LiteLLM

## Requirements

- LiteLLM custom success/failure callback (`mt_obs.llm_audit`) writes `audit.llm_call`: call_id, trace_id, role (virtual key alias), route model + resolved model + revision, `prompt_version`, `prompt_hash` (sha256), `response_hash`, prompt text, response text, tokens in/out, cost, latency_ms, fallback_used, status, caller (`run_id` / job id).
- Writes are async and buffered (NATS JetStream `audit.llm_call.buffer`) so a slow DB never blocks the gateway; no call is lost on restart (at-least-once + idempotent `call_id`).
- Prompt registry: `packages/mt_agents/prompts/<role>/<name>@<semver>.md` with front matter; loader computes the hash; changing text without bumping the version fails CI.
- Model registry rows (`models.registry`) for gateway models carry `training_cutoff` (used by P6-T017).
- Secrets never logged: redact `Authorization`, keys and anything matching the sops key list before writing.

## ToDo

- [ ] Implement `mt_obs.llm_audit` callback and mount it in the LiteLLM container config (pinned image unchanged; callback via mounted module).
- [ ] Migration for `audit.llm_call` (WORM) if P0 did not create it; otherwise extend columns via a new migration.
- [ ] NATS buffer stream + consumer that inserts with idempotency on `call_id`.
- [ ] Prompt registry loader + CI check (hash vs version).
- [ ] Add `training_cutoff` column to `models.registry` for gateway models; seed Claude/custom/local entries.
- [ ] Grafana: count of gateway requests vs `audit.llm_call` rows (drift panel).
- [ ] Tests; docs.

## Verification

### Tests
- Unit: redaction, hash stability, prompt version check.
- Integration: a call through LiteLLM produces exactly one `audit.llm_call` row; failure and fallback calls are recorded with `status`/`fallback_used`.
- WORM: 15 §2.4 suite on `audit.llm_call`.

### Scenarios
- Given the DB is down, when 50 calls happen, then they buffer in NATS and all 50 rows appear after recovery with no duplicates.
- Given a prompt file edited without a version bump, when CI runs, then it fails with the file name.
- Given a call falls back from `research-primary` to `local-advisor`, then the row shows both models and `fallback_used=true`.

### Stress / failure injection
- Burst 200 concurrent gateway calls: gateway overhead added by the callback p95 < 5 ms; zero lost rows.
- Kill the consumer mid-burst; restart; row count equals LiteLLM request count.

## Acceptance criteria

- [ ] Gateway request count == `audit.llm_call` count over a 24 h window (drift panel 0).
- [ ] No secret strings in any stored prompt (redaction test).
- [ ] CI green.

## Exceptions & edge cases

- Streaming responses: write the row on stream completion; on client disconnect write `status=aborted` with partial tokens.
- Very large prompts: store text compressed; hashes over the uncompressed text.
- Telegram-derived text must never be in a prompt; if a provenance flag says so the caller is refused before the call (P6-T006).

## Cardinal rules (do NOT)

- Do NOT log API keys or any secret; redact before write.
- Do NOT block the gateway on DB writes.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `journal.*`, policy changes); corrections are new rows referencing the original (15 §2).
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M17: name the callback and buffer.
- `docs/10-memory-rag-and-models.md` §5: audit callback + prompt registry.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.20 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T005-llm-call-audit-prompt-registry`
- PR title: `P6-T005: Audit every LLM call and version prompts and models`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T005` run

## Progress log

- 2026-10-21 00:00 · planner · created
