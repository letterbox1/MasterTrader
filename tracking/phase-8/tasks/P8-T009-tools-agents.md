---
id: P8-T009
kind: task
title: Talk-to-agents tool group (M8 analysis, M9 memory, M10 anomaly explanations)
phase: 8
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T003, P8-T004, P8-T006, P8-T007, P8-B008]
requirements: [R8.03]
roadmap_todos: [T8.20]
modules: [M8, M9, M10, M21, M20]
dashboards: [D09, D17]
branch: p8/P8-T009-tools-agents
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/ui/dashboards/D09-agents.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T009 · Talk-to-agents tool group (M8 analysis, M9 memory, M10 anomaly explanations)

## Goal / expected outcome

Claude can ask the M8 decision graph for an analysis or signal on an instrument, query memory and RAG (M9), and request an anomaly explanation (M10). Results are advisory: nothing in this group places an order.

## Context & references

- Roadmap: [R8.03](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.20](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Spec: [03 M20 Talk to agents row](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 F4](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [D09 Agents](../../../docs/ui/dashboards/D09-agents.md) (anomaly explanations via `/notifications?kind=anomaly`)
- Cross-phase: P6 R6.01 / T6.20 (debate graph), R6.04 (Hindsight), R6.05 / T6.22 (anomaly explain agent), R6.07 (LLM budgets); P4 R4.07 (RAG `as_of`).
- Gap: P8-B008 (no command to request an anomaly explanation).

## Requirements

- `agents_run_analysis` → `agents.run_analysis` (C1, trigger recorded as `manual:mcp`) returns a run id; `get_agents_runs`, `get_agents_run` (debate turns, `Signal` with provenance), `get_signals` read the result.
- `models_tierb_ask` → `models.tierb.ask` (C0, decision question on a subject; option probabilities).
- `memory_search` → `/memory/search` (banks `decisions`, `strategies`, `market-regimes`, `user`, `ops`; point-in-time); `rag_search` → `/rag/search` with `as_of`.
- `get_anomalies` → `/notifications?kind=anomaly`; `anomaly_explain` → new command `anomaly.explain` (C1) that asks `mt_anomaly`'s explain agent to brief an anomaly id. The result lands in notifications. Add it to 02 §7.2 per P8-B008.
- Rate limit 10 agent runs/h per token; LiteLLM per-role budgets apply; agents run on demand only, never per tick.
- Signals from MCP-requested runs enter the normal pipeline as advisory `Signal`s; they never create orders by themselves.
- `memory.delete` and `models.promote/rollback/bakeoff.run` aren't in this group (`memory.delete` never; the others disabled).

## ToDo

- [ ] Add the `anomaly.explain` command in mt_api (publishes an explain request to `mt_anomaly`; C1; audited).
- [ ] Add the registry entries (group `agents`, enabled) and regenerate the snapshot.
- [ ] Tests with a stubbed LiteLLM gateway (deterministic responses) and the local fallback.
- [ ] Update docs.

## Verification

### Tests
- Integration (stub gateway): `agents_run_analysis(BTC-PERP)` → run id → poll → `Signal` JSON with provenance; no order created.
- Integration: `memory_search` respects `as_of`; Telegram-derived memories are filtered by the guard.
- Integration: `anomaly_explain(id)` → notification with brief; unknown id → 404 problem.
- Unit: rate limit 10/h → 429 on the 11th call.

### Scenarios
- Given the LiteLLM budget is exhausted, when Claude asks for analysis, then the run uses local models and the result is marked "local models".
- Given an anomaly alert at 09:00, when you ask "why did that fire?", then Claude calls `anomaly_explain` and returns the brief.

### Stress / failure injection
- 10 concurrent analysis requests → queued by the agents scheduler; no LLM spend above the role budget; mt_api unaffected.

## Acceptance criteria

- [ ] Agents, memory, RAG and anomaly-explain tools work end to end; signals are advisory only
- [ ] `anomaly.explain` command exists, audited, documented
- [ ] Budgets and rate limits enforced
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- GPU unavailable: tier B on CPU or disabled; `models_tierb_ask` returns status `degraded`.
- Hindsight down: `memory_search` returns 503; RAG still works.
- Agent run fails mid-debate: the run status is `failed` with reason; no partial signal.

## Cardinal rules (do NOT)

- Do NOT let an agent result place or modify an order (agents output a `Signal` only, 07 §6).
- Do NOT expose `memory.delete`.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set; Claude via MCP counts as a model input (12 §4–5).
- Do NOT add paid data, APIs or services; free tiers only (03 §1).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

## Doc sync on completion

- `docs/02-v1-architecture.md` §7.2: `anomaly.explain` command.
- `docs/03-build-spec.md` M10/M20.
- `docs/ui/dashboards/D09-agents.md`: explain request via command.
- `docs/roadmap/phase-8-mcp.md`: progress on T8.20.

## Branch & PR

- Branch: `p8/P8-T009-tools-agents`
- PR title: `P8-T009: Talk-to-agents tool group (M8 analysis, M9 memory, M10 anomaly explanations)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T009` run

## Progress log

- 2026-10-21 00:00 · planner · created
