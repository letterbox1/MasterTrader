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
depends_on: [P0-T020, P0-T022, P0-T031, P0-T071]
requirements: [R0.09, R0.13]
roadmap_todos: [T0.45, T0.41, T0.28]
modules: [M21, mt-models, mt-obs]
dashboards: []
tools: [git, docker, cargo, maturin, supabase]
mcp: []
env: []
services: [litellm, supabase-postgres, tei-embed]
branch: p0/P0-T042-litellm-gateway-config
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T042 · Deploy the LiteLLM gateway with routes, per-role keys and budgets

## Goal / expected outcome

The `litellm` container (≥ 1.83, pinned by official image digest, **never** 1.82.7/1.82.8) runs on the `core` network with the 10 §5 model list (`research-primary`, `research-custom`, `local-advisor`, `local-embed`), fallbacks, per-role virtual keys with daily budgets that fall back to local models when exhausted, spend metrics to Prometheus and every call written to `audit.llm_call` from day one (R0.13). Built and tested against a mock provider with no real keys; live calls with your keys are P0-T068.

## Context & references

- [Roadmap P0 R0.09](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.45](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [10 §5 model gateway](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21)
- [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving) (Model gateway)
- [03 §7 LLM cost control](../../../docs/03-build-spec.md#7-llm-cost-control)
- [07 §7 supply chain](../../../docs/07-security-notes.md#7-supply-chain) (LiteLLM supply chain)
- Decisions: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P6-B010 (`audit.llm_call` from P0), P0-B008 (`llm-local`); budgets [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets)
- Related: P0-T043, P0-T044, P0-T068 (live smoke with your keys, after P0-T007)
- Depends on: P0-T020, P0-T022, P0-T031. Build first, keys last: `research-primary`/`research-custom` point at a mock OpenAI/Anthropic-compatible provider (recorded fixtures) in CI and dev.

## Requirements

- Image `ghcr.io/berriai/litellm` at a ≥ 1.83 tag resolved to digest; CI check rejects versions < 1.83 and exactly 1.82.7/1.82.8.
- `infra/litellm/config.yaml`: `research-primary` (Anthropic Claude, prompt caching on), `research-custom` (OpenAI-compatible base URL from secrets; disabled if absent), `local-advisor` (`llm-local`, P0-T044), `local-embed` (`tei-embed`, bge-small, P0-T043); `router_settings.routing_strategy: latency-based-routing`; `fallbacks: [{research-primary: [research-custom, local-advisor]}]`; `context_window_fallbacks: [{local-advisor: [research-primary]}]`.
- Virtual keys per role with the [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets) defaults read from settings (never literals): debate $1.00, strategy-gen $0.50, explain $0.30, memory $0.30, chat $0.40, shadow $0.30 per day (`budget_duration: 1d`) and a monthly cap of US$40. Whichever runs out first routes the call to `local-advisor`, marked `fallback_used`, instead of failing (10 §5; custom router hook or per-key `model` fallback, document the mechanism). Raising a budget is C3 (`system.settings.update`).
- LiteLLM DB: database `litellm` on the Supabase Postgres (P0-T020/P0-T070) with its own role, outside the MasterTrader schemas; master key from tmpfs; UI disabled or bound internal only; `telemetry: false`.
- Callbacks (LiteLLM is a third-party Python service, so its callback is a Python plugin by necessity; there is no `mt_models` Python package any more, 17 §H): success/failure → a LiteLLM `CustomLogger` plugin `infra/litellm/mt_audit_callback.py`, baked into the derived LiteLLM image and not a uv workspace package, calling the one Rust audit writer through the `mt_store` binding (`mt_store.obs`, P0-T031, P0-T071; the wheel is built by maturin and installed in the image) to write `audit.llm_call` (hashes + text + tokens + cost + latency + `trace_id`); Prometheus callback for spend (`litellm_spend_metric`).
- Only LLM keys are mounted (07 §2); no broker keys; `core` network only; outbound to `api.anthropic.com` and the custom endpoint host.

## ToDo

- [ ] Add the service, config, DB and secrets mounts.
- [ ] Implement `infra/litellm/mt_audit_callback.py` (via the `mt_store` binding) and a derived LiteLLM image (pinned base digest) that installs it and the `mt_store` wheel.
- [ ] Create the six virtual keys (script `infra/litellm/bootstrap_keys` via the LiteLLM admin API, keys stored in tmpfs secrets for consumers).
- [ ] Add the version guard to CI.
- [ ] Mock-provider smoke tests below (live calls are P0-T068).

## Verification

### Tests
- Smoke (mock provider, no keys): one completion per route (`research-primary`, `research-custom`, `local-advisor`) returns 200; one embedding via `local-embed` returns 384 dims.
- Budget: set `chat` budget to $0.0001, call twice → second call served by `local-advisor` (response header shows model).
- Audit: each smoke call produces an `audit.llm_call` row with matching `trace_id`.

### Scenarios
- Given the (mock) Anthropic provider is down, when `research-primary` is called, then LiteLLM falls back to `research-custom` then `local-advisor` and the response says which.
- Given an engine/hot-path container tries to reach LiteLLM, then there is no dependency (10 §5): the gateway is never on the hot path (documented; enforced in P2).

### Stress / failure injection
- 20 concurrent `local-advisor` calls → queueing, no crashes; p95 latency logged for the model profile in use (CPU by default, `models.gpu_profile: auto`).

## Acceptance criteria

- [ ] LiteLLM ≥ 1.83 pinned by digest; version guard in CI
- [ ] All routes answer mock-provider smoke calls (live: P0-T068)
- [ ] Budget exhaustion falls back to local (tested); budgets come from the 16 §2.10 defaults in settings
- [ ] Every call audited in `audit.llm_call`; spend metric in Prometheus
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, `supabase test db`, gitleaks, `pit` check)

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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keyless build vs a mock provider, live smoke split to P0-T068 (T0.69); budgets = 16 §2.10 defaults incl. shadow + US$40 cap; audit.llm_call from P0 (R0.13, T0.28); run fields added)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (callback lives in `mt_models` and writes through the Rust audit writer via the `mt_store` binding (depends on P0-T071); LiteLLM DB on the Supabase Postgres)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (callback moves from the retired `mt_models` Python package to a LiteLLM plugin file in the derived image (`infra/litellm/mt_audit_callback.py`) writing through `mt_store.obs`; module `mt-models`; tools cargo/maturin instead of uv)
