---
id: P6-T005
kind: task
title: Prompt and model versioning on top of the P0 LLM-call audit
phase: 6
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T042, P0-T031, P4-T028]
requirements: [R6.03]
roadmap_todos: [T6.31]
modules: [M17, M21, M8]
dashboards: [D10]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [litellm, postgres, nats, grafana]
branch: p6/P6-T005-llm-call-audit-prompt-registry
pr: ""
doc_sync: [docs/03-build-spec.md, docs/10-memory-rag-and-models.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T005 · Prompt and model versioning on top of the P0 LLM-call audit

## Goal / expected outcome

Every LLM call already lands in `audit.llm_call` from Phase 0 (the LiteLLM callback built in P0-T042, R0.13). This task adds what Phase 6 needs on top: a **versioned prompt registry** so every agent call names its `prompt_version`, **model versioning** (`models.registry` rows for the gateway routes with resolved revision and `training_cutoff`), the extra audit columns that carry them (an additive migration, never a new table or second writer), and a drift check proving gateway requests = audit rows.

## Context & references

- Roadmap: [R6.03](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.31
- Spec: [03 M17](../../../docs/03-build-spec.md#m17-observability--audit--mt_obs) (every LLM call: model, prompt/response hash + text, tokens, cost, latency) · [03 M8](../../../docs/03-build-spec.md#m8-ai-decision-layer--mt_agents) (prompts/models versioned; `audit.llm_call` written from P0) · [10 §5](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21) (audit from P0; P6 only extends it with the prompt registry and training cutoff)
- Decisions: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P6-B010: `audit.llm_call` is written from P0 via the LiteLLM callback, not P6) · [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (canonical audit names) · [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P6-B001: R6.03 now has ToDo T6.31)
- WORM: [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)
- Cross-phase: P0-T042 (LiteLLM + callback writer), P0-T031 (`audit.llm_call` table, NATS buffer), P4-T028 (`models.registry`)
- Used by: P6-T007, P6-T015, P6-T017 (`training_cutoff`), P6-T052 (audit check)

## Requirements

- Don't re-create `audit.llm_call` or its writer. An additive migration adds nullable columns the P0 table lacks (`prompt_name`, `prompt_version`, `model_revision`, `run_id`); old rows stay untouched (WORM).
- Prompt registry: `packages/mt_agents/prompts/<role>/<name>@<semver>.md` with front matter; the loader computes sha256; changing text without bumping the version fails CI.
- Metadata plumbing: callers pass `prompt_name`, `prompt_version`, `run_id` and `role` in LiteLLM request metadata; the P0 callback copies them into the row.
- Model registry: `models.registry` rows for each gateway route (`research-primary`, `research-custom`, `local-advisor`) with resolved model id, revision and `training_cutoff` plus its source; unknown = NULL (P6-T017 fails closed on NULL).
- Secrets never logged: the P0 redaction stays in force; a test asserts no secret value or sops key name appears in stored P6 prompts.
- Drift panel: gateway request count vs `audit.llm_call` rows per role (expected difference 0).

## ToDo

- [ ] Additive Alembic migration for the extra `audit.llm_call` columns (skip any P0 already has).
- [ ] Prompt registry loader + CI check (hash vs version).
- [ ] Request-metadata plumbing from `mt_agents` callers into the P0 callback.
- [ ] Seed `models.registry` gateway entries with `training_cutoff` and its source (marked (U) if unverified).
- [ ] Grafana drift panel (gateway requests − audit rows).
- [ ] Tests; docs.

## Verification

### Tests
- Unit: prompt hash stability, version check, metadata mapping.
- Integration: a call through LiteLLM with `prompt_version` produces exactly one `audit.llm_call` row carrying it; failure and fallback calls carry it too.
- WORM: the 15 §2.4 suite stays green on `audit.llm_call` after the migration.

### Scenarios
- Given a prompt file edited without a version bump, when CI runs, then it fails with the file name.
- Given a call falls back from `research-primary` to `local-advisor`, then the row shows both models, `fallback_used=true` and the same `prompt_version`.
- Given a gateway model with no known cutoff, then its registry row has `training_cutoff=NULL` and P6-T017 refuses LLM strategies that use it.

### Stress / failure injection
- Burst 200 concurrent gateway calls with metadata: added callback overhead p95 < 5 ms; drift 0.
- Pause Postgres 60 s mid-burst: rows buffer in NATS (P0 path) and land with their metadata; no duplicates.

## Acceptance criteria

- [ ] Every P6 call carries `prompt_version` (and `run_id` where there is a run).
- [ ] Drift panel shows 0 over 24 h.
- [ ] No second `audit.llm_call` table or writer exists (code review check).
- [ ] CI green.

## Exceptions & edge cases

- Calls from P0–P5 jobs that predate the registry carry `prompt_version=NULL`; that's expected.
- Streaming responses and client disconnects are handled by the P0 callback; this task only adds metadata.
- Telegram-derived text must never be in a prompt; callers refuse it before the call (P6-T006).

## Cardinal rules (do NOT)

- Do NOT create a second `audit.llm_call` table or writer; extend the P0 one (17 §D, P6-B010).
- Do NOT log API keys or any secret; redact before write.
- Do NOT block the gateway on DB writes.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `journal.*`, policy changes); corrections are new rows referencing the original (15 §2).
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M17: prompt registry and the extra `audit.llm_call` columns.
- `docs/10-memory-rag-and-models.md` §5: prompt registry + training cutoff.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.31 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T005-llm-call-audit-prompt-registry`
- PR title: `P6-T005: Prompt and model versioning on top of the P0 LLM-call audit`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T005` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (re-scoped to T6.31: audit.llm_call writer exists from P0 (P0-T042, 17 §D P6-B010); this adds prompt registry, model versioning, training_cutoff and additive columns only; deps P0-T042/P0-T031/P4-T028)
