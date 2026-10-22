---
id: P6-T009
kind: task
title: Enforce the monthly LLM cap, per-role budgets and local fallback
phase: 6
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T042, P0-T044, P2-T019]
requirements: [R6.07]
roadmap_todos: [T6.32]
modules: [M21, M15]
dashboards: [D10, D09]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [litellm, llm-local, postgres, prometheus]
branch: p6/P6-T009-llm-budgets-local-fallback
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/03-build-spec.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T009 · Enforce the monthly LLM cap, per-role budgets and local fallback

## Goal / expected outcome

Spend can't creep: a monthly global cap plus per-role daily budgets are enforced in LiteLLM, exhausted budgets fall back to `local-advisor` instead of failing, raises are C3, and `/models/gateway/spend` reports it.

## Context & references

- Roadmap: [R6.07](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.32
- Spec: [03 §7](../../../docs/03-build-spec.md#7-llm-cost-control) (monthly cap, spend panel) · [10 §5](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21) (virtual keys, `max_budget`, `budget_duration`, fallbacks) · [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) ("Local models" badge)
- UI: [D10](../../../docs/ui/dashboards/D10-models-memory.md) Gateway tab (raise = C3, lower = C1) · [D09](../../../docs/ui/dashboards/D09-agents.md) budget estimate
- Decision: [17 §C](../../../docs/17-decisions-register.md#c-defaults-that-were-n-or-unspecified) (P6-B012) → defaults [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets): monthly cap US$40 per UTC month (month-to-date); daily per-role budgets debate $1.00, strategy-gen $0.50, explain $0.30, memory $0.30, chat $0.40, shadow $0.30; whichever runs out first routes to `local-advisor`
- Cross-phase: P0-T042 (LiteLLM per-role keys, `audit.llm_call` writer), P0-T044 (`local-advisor` on `llm-local`), P2-T019 (tighten/loosen classifier + C3 flow)
- Depends on (this phase): none; built and tested against a fake provider (no keys). Verified by P6-T053 (T6.70); live check P6-T070

## Requirements

- Per-role virtual keys (`debate`, `strategy-gen`, `explain`, `memory`, `chat`, `shadow`) with `max_budget` + `budget_duration: 1d`, values from the settings (defaults 16 §2.10, never hard-coded); extend the keys P0-T042 provisions, don't duplicate them.
- Global monthly cap (default US$40 per UTC month) checked month-to-date by a pre-call hook reading spend from `audit.llm_call`.
- On budget exhaustion for a role or the global cap: route to `local-advisor` (and mark responses `fallback_used`), never hard-fail unless local is down.
- `system.settings.update` for budgets: lowering = C1, raising = C3 (server-side diff classification).
- `GET /models/gateway/spend`: by role, today vs budget, month-to-date vs cap, requests, errors, fallbacks, latency, provider status.
- UI flag `local_models=true` exposed via `/system/health` for the global badge.
- Spend events `llm.budget.warn` / `llm.budget.exhausted` (role, period, spend, budget) on NATS for P6-T010 alerts and D10.

## ToDo

- [ ] Budget sync job: settings → LiteLLM key budgets (admin API on the internal network).
- [ ] Month-to-date guard (LiteLLM pre-call hook) reading spend from `audit.llm_call`.
- [ ] Settings diff classifier for budget fields (tighten/loosen) using the P0 C3 flow.
- [ ] Spend query endpoint + Prometheus metrics `llm_spend_usd{role}` and `llm_fallback_total{role}`.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: diff classifier (raise → C3, lower → C1).
- Integration: exhaust the `explain` budget with a fake provider → next call served by `local-advisor`, flagged.
- Integration: month-to-date over cap → all roles fall back.

### Scenarios
- Given a C1 request to raise the debate budget, then the server rejects it and requires C3.
- Given the local model is also down, when the budget is exhausted, then calls fail with `budget_exhausted_no_local` and an alert fires.

### Stress / failure injection
- Concurrent calls straddling the budget boundary: overspend ≤ one call's cost (race tolerance documented).

## Acceptance criteria

- [ ] Budget raise impossible without C3 (API test).
- [ ] Fallback observable in spend endpoint and `audit.llm_call`.
- [ ] CI green.

## Exceptions & edge cases

- Month rollover in UTC vs Australia/Sydney: use UTC for accounting, display local.
- Provider price changes: cost taken from LiteLLM's response cost; unknown cost → estimate flagged.

## Cardinal rules (do NOT)

- Do NOT give LiteLLM keys it doesn't need; keep it on the internal network (LiteLLM ≥ 1.83, pinned digest).
- Do NOT loosen anything (risk, LLM budgets, treasury policy, allow-list, autonomous mode, mandates) without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §5: month-to-date guard and `shadow` role.
- `docs/03-build-spec.md` §7: cap semantics.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.32 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T009-llm-budgets-local-fallback`
- PR title: `P6-T009: Enforce the monthly LLM cap, per-role budgets and local fallback`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T009` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (maps to new T6.32; 16 §2.10 defaults incl. shadow, month-to-date US$40 cap, precedence; spend events; keyless vs fake provider; deps P0-T042/P0-T044/P2-T019 (no longer P6-T005); run fields)
