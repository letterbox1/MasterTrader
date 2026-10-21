---
id: P0-T042
kind: task
title: Deploy the LiteLLM gateway with routes, per-role keys and budgets
phase: 0
type: OPS
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T020, P0-T022, P0-T031, P0-T007]
requirements: [R0.09]
roadmap_todos: [T0.45, T0.41]
modules: [M21]
dashboards: []
branch: p0/P0-T042-litellm-gateway-config
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T042 · Deploy the LiteLLM gateway with routes, per-role keys and budgets

## Goal / expected outcome

The `litellm` container (≥ 1.83, pinned by official image digest, **never** 1.82.7/1.82.8) runs on the `core` network with the 10 §5 model list (`research-primary`, `research-custom`, `local-advisor`, `local-embed`), fallbacks, per-role virtual keys with daily budgets that fall back to local models when exhausted, spend metrics to Prometheus and every call written to `audit.llm_call`.

## Context & references

- [Roadmap P0 R0.09](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.45](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [10 §5 model gateway](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21)
- [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models) (Model gateway)
- [03 §7 LLM cost control](../../../docs/03-build-spec.md#7-llm-cost-control)
- [07 §7 supply chain](../../../docs/07-security-notes.md#7-supply-chain) (LiteLLM supply chain)
- Related: P0-T043, P0-T044, P0-T007
- Depends on: P0-T020, P0-T022, P0-T031, P0-T007

## Requirements

- Image `ghcr.io/berriai/litellm` at a ≥ 1.83 tag resolved to digest; CI check rejects versions < 1.83 and exactly 1.82.7/1.82.8.
- `infra/litellm/config.yaml`: `research-primary` (Anthropic Claude, prompt caching on), `research-custom` (OpenAI-compatible base URL from secrets; disabled if absent), `local-advisor` (P0-T044), `local-embed` (TEI bge-small, P0-T043); `router_settings.routing_strategy: latency-based-routing`; `fallbacks: [{research-primary: [research-custom, local-advisor]}]`; `context_window_fallbacks: [{local-advisor: [research-primary]}]`.
- Virtual keys per role: `debate`, `strategy-gen`, `explain`, `memory`, `chat` with `max_budget` + `budget_duration: 1d` from P0-T007; global provider budget; on budget exhaustion route to `local-advisor` instead of failing (custom router hook or per-key `model` fallback — document the mechanism chosen).
- LiteLLM DB: Postgres database `litellm` with its own role; master key from tmpfs; UI disabled or bound internal only; `telemetry: false`.
- Callbacks: success/failure → `mt_obs` callback writing `audit.llm_call` (hashes + text + tokens + cost + latency + `trace_id`); Prometheus callback for spend (`litellm_spend_metric`).
- Only LLM keys are mounted (07 §2); no broker keys; `core` network only; outbound to `api.anthropic.com` and the custom endpoint host.

## ToDo

- [ ] Add the service, config, DB and secrets mounts.
- [ ] Implement the `mt_obs` LiteLLM callback module.
- [ ] Create the five virtual keys (script `infra/litellm/bootstrap_keys.py`, keys stored in tmpfs secrets for consumers).
- [ ] Add the version guard to CI.
- [ ] Smoke tests below.

## Verification

### Tests
- Smoke: one completion per route (`research-primary`, `research-custom` if configured, `local-advisor`) returns 200; one embedding via `local-embed` returns 384 dims.
- Budget: set `chat` budget to $0.0001, call twice → second call served by `local-advisor` (response header shows model).
- Audit: each smoke call produces an `audit.llm_call` row with matching `trace_id`.

### Scenarios
- Given the Anthropic API is down, when `research-primary` is called, then LiteLLM falls back to `research-custom` then `local-advisor` and the response says which.
- Given an engine/hot-path container tries to reach LiteLLM, then there is no dependency (10 §5): the gateway is never on the hot path (documented; enforced in P2).

### Stress / failure injection
- 20 concurrent `local-advisor` calls → queueing, no crashes; p95 latency logged for the CPU model.

## Acceptance criteria

- [ ] LiteLLM ≥ 1.83 pinned by digest; version guard in CI
- [ ] All configured routes answer smoke calls
- [ ] Budget exhaustion falls back to local (tested)
- [ ] Every call audited in `audit.llm_call`; spend metric in Prometheus
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- No custom endpoint yet: route omitted and fallback chain skips it.
- Claude prompt caching unavailable for a model: log and continue.

## Cardinal rules (do NOT)

- Do NOT install LiteLLM from PyPI unpinned or use 1.82.7/1.82.8.
- Do NOT mount broker/exchange keys into LiteLLM.
- Do NOT route any Telegram-derived text to a model.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT put Telegram text into any model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §5: record the budget-exhaustion fallback mechanism and the digest/version.
- `docs/roadmap/phase-0-foundations.md`: tick T0.45, T0.41 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T042-litellm-gateway-config`
- PR title: `P0-T042: Deploy the LiteLLM gateway with routes, per-role keys and budgets`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T042` run

## Progress log

- 2026-10-21 00:00 · planner · created
