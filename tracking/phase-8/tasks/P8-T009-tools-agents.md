---
id: P8-T009
kind: task
title: Talk-to-agents tool group (M8 analysis, M9 memory, M10 `anomaly.explain`)
phase: 8
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T003, P8-T004, P8-T006, P8-T007, P6-T007, P6-T012, P6-T015, P4-T032, P0-T042]
requirements: [R8.03]
roadmap_todos: [T8.20]
modules: [M8, M9, M10, M21, M20]
dashboards: [D09, D17]
tools: [uv, docker, git]
mcp: []
env: []
services: [postgres, nats, litellm, llm-local, hindsight]
branch: p8/P8-T009-tools-agents
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/ui/dashboards/D09-agents.md, docs/roadmap/phase-8-mcp.md]
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

# P8-T009 · Talk-to-agents tool group (M8 analysis, M9 memory, M10 `anomaly.explain`)

## Goal / expected outcome

Claude can ask the M8 decision graph for an analysis or signal on an instrument, query memory and RAG (M9), and request an anomaly explanation (M10, `anomaly.explain`). Results are advisory: nothing in this group places an order. Tools need the `analyse` scope and are enabled by default. Tested against a stubbed LiteLLM gateway and the local model; no API keys.

## Context & references

- Roadmap: [R8.03](../../../docs/roadmap/phase-8-mcp.md#3-requirements) (incl. `anomaly.explain`) · ToDo [T8.20](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Decisions: [17 §D P8-B008](../../../docs/17-decisions-register.md#d-other-decisions) (`anomaly.explain` added) · [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets) (LLM budgets) · [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) (`analyse` scope; writes 10/min)
- Spec: [03 M20 Talk to agents row](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7.2 Agents & models row](../../../docs/02-v1-architecture.md#72-commands-rest-write) (`agents.run_analysis` C1, `models.tierb.ask` C0, `anomaly.explain` C1) · [02 F4](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [D09 Agents](../../../docs/ui/dashboards/D09-agents.md) (`anomaly.explain` in actions and backend contract)
- Cross-phase (depends_on): P6-T007 (debate graph), P6-T012 (memory API), P6-T015 (explain agent consumer), P4-T032 (RAG retrieval with `as_of`), P0-T042 (LiteLLM gateway with per-role budgets).

## Requirements

- `agents_run_analysis` → `agents.run_analysis` (C1, trigger recorded as `manual:mcp`) returns a run id; `get_agents_runs`, `get_agents_run` (debate turns, `Signal` with provenance), `get_signals` read the result.
- `models_tierb_ask` → `models.tierb.ask` (C0; option probabilities).
- `memory_search` → `/memory/search` (point-in-time); `rag_search` → `/rag/search` with `as_of`.
- `get_anomalies` → `/notifications?kind=anomaly`; `anomaly_explain` → `anomaly.explain` (C1; arg `anomaly_id`; publishes an explain request to `mt_anomaly`; the result arrives as a notification and, if subscribed, via P8-T032). Add the mt_api command here if P6 didn't.
- All results pass the response guard (P8-T006); signals from MCP-requested runs are advisory `Signal`s and never create orders.
- Commands count as writes for the 10 writes/min limit (P8-T030); LiteLLM per-role budgets (16 §2.10) apply; agents run on demand only, never per tick.
- Not in this group: `memory.delete` (never exposed); `models.promote/rollback/bakeoff.run` (disabled).

## ToDo

- [ ] Add the `anomaly.explain` command in mt_api if missing (C1; audited; payload `anomaly_id`).
- [ ] Add the registry entries (scope `analyse`, enabled) and regenerate the snapshot.
- [ ] Tests with a stubbed LiteLLM gateway (deterministic responses) and the local fallback.
- [ ] Update docs.

## Verification

### Tests
- Integration (stub gateway): `agents_run_analysis(BTC-PERP)` → run id → poll → `Signal` JSON with provenance; no order created.
- Integration: `memory_search` respects `as_of`; Telegram-derived memories are filtered by the guard.
- Integration: `anomaly_explain(id)` → notification with brief; unknown id → 404 problem.
- Unit: a token without `analyse` gets 403 `scope_missing`.

### Scenarios
- Given the LiteLLM budget is exhausted, when Claude asks for analysis, then the run uses local models and the result is marked "local models".
- Given an anomaly alert at 09:00, when you ask "why did that fire?", then Claude calls `anomaly_explain` and returns the brief.

### Stress / failure injection
- 10 concurrent analysis requests → queued by the agents scheduler; writes beyond 10/min get 429; no LLM spend above the role budget; mt_api unaffected.

## Acceptance criteria

- [ ] Agents, memory, RAG and anomaly-explain tools work end to end; signals are advisory only
- [ ] `anomaly.explain` command exists, audited, documented
- [ ] Budgets, scope and rate limits enforced
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- GPU unavailable: tier B on CPU or disabled; `models_tierb_ask` returns status `degraded`.
- Hindsight down: `memory_search` returns 503; RAG still works.
- Agent run fails mid-debate: run status `failed` with reason; no partial signal.

## Cardinal rules (do NOT)

- Do NOT let an agent result place or modify an order (agents output a `Signal` only, 07 §6).
- Do NOT expose `memory.delete`.
- Do NOT use real LLM keys in this task's tests; the live gateway check is P6-T070 / P8-T035.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set; Claude via MCP counts as a model input (12 §4–5).
- Do NOT add paid data, APIs or services; free tiers only (03 §1).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7.2: confirm `anomaly.explain` as built.
- `docs/03-build-spec.md` M10/M20.
- `docs/ui/dashboards/D09-agents.md`: explain request via command.
- `docs/roadmap/phase-8-mcp.md`: progress on T8.20.

## Branch & PR

- Branch: `p8/P8-T009-tools-agents`
- PR title: `P8-T009: Talk-to-agents tool group (M8 analysis, M9 memory, M10 anomaly.explain)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T009` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (`analyse` scope; `anomaly.explain` now in 02 §7.2 and D09; agents 10/h replaced by the 10 writes/min default + 16 §2.10 budgets; dropped gap dep P8-B008; cross-phase deps P6-T007/T012/T015, P4-T032, P0-T042; tools/env/services)
