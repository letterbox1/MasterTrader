---
id: P0-T044
kind: task
title: Deploy a CPU local-advisor model server for the gateway fallback
phase: 0
type: OPS
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T020, P0-T022]
requirements: [R0.09]
roadmap_todos: [T0.45]
modules: [M21]
dashboards: []
branch: p0/P0-T044-local-advisor-model-server
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/10-memory-rag-and-models.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T044 · Deploy a CPU local-advisor model server for the gateway fallback

## Goal / expected outcome

A local OpenAI-compatible model server (`llama-server` from llama.cpp, digest-pinned) serves a small quantised instruct model on CPU as LiteLLM's `local-advisor`, bound to `core`, requiring an API key, so budget exhaustion and provider outages degrade to local instead of failing.

## Context & references

- [Roadmap P0 R0.09 (a local model)](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [10 §5 model gateway](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21) (`local-advisor`: vLLM / llama-server Qwen3.5-4B or 9B)
- [07 §5 network & host](../../../docs/07-security-notes.md#5-network--host) (local inference binds localhost + API key)
- No P0 container is defined for this route: P0-B008.
- Depends on: P0-T020, P0-T022

## Requirements

- Image: `ghcr.io/ggml-org/llama.cpp:server` by digest; model: a Qwen instruct GGUF Q4_K_M sized to RAM (≈ 4B params; log exact file + sha256); context 8k.
- `--api-key` from tmpfs secret; `--host 0.0.0.0` inside the container but only on `core` network; no published port.
- Health `/health`; `mem_limit` sized to model (~4–6 GB); threads = physical cores − 2.
- GPU later: swap to vLLM when P0-T005's GPU decision lands (P4/P6); config change only.

## ToDo

- [ ] Add the service + model download job with checksum verification.
- [ ] Add API key to secrets; wire into LiteLLM config.
- [ ] Smoke test.

## Verification

### Tests
- Smoke: `/v1/chat/completions` with the key → 200; without the key → 401.

### Scenarios
- Given Anthropic budget is exhausted, when an agent calls the gateway, then `local-advisor` answers (slower) instead of an error.

### Stress / failure injection
- 5 concurrent requests → server queues; tokens/s logged for the CPU.

## Acceptance criteria

- [ ] Server healthy, digest-pinned, API key enforced
- [ ] Model file checksum logged
- [ ] LiteLLM `local-advisor` smoke passes
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Insufficient RAM: pick a smaller model (≈ 1.7B) and log it.

## Cardinal rules (do NOT)

- Do NOT expose the model server outside `core` or without an API key.
- Do NOT feed Telegram text to the model.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT put Telegram text into any model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/02-v1-architecture.md` §3.2 and `docs/10-memory-rag-and-models.md` §5: add the P0 `local-advisor` container.
- `docs/roadmap/phase-0-foundations.md`: tick T0.45 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T044-local-advisor-model-server`
- PR title: `P0-T044: Deploy a CPU local-advisor model server for the gateway fallback`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T044` run

## Progress log

- 2026-10-21 00:00 · planner · created
