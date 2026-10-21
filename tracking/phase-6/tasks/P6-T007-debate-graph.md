---
id: P6-T007
kind: task
title: LangGraph debate graph producing a sourced Signal
phase: 6
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T004, P6-T005, P6-T006]
requirements: [R6.01]
roadmap_todos: [T6.20]
modules: [M8]
dashboards: [D09]
branch: p6/P6-T007-debate-graph
pr: ""
doc_sync: [docs/03-build-spec.md, third_party/LICENSES.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T007 · LangGraph debate graph producing a sourced Signal

## Goal / expected outcome

`mt_agents` runs a TradingAgents-style LangGraph debate (analysts → bull/bear → research manager → trader → risk debate → portfolio manager) through the gateway and emits one `Signal` v2 with provenance, stored in `audit.decision_run`/`audit.signal`.

## Context & references

- Roadmap: [R6.01](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.20
- Spec: [03 M8](../../../docs/03-build-spec.md#m8-ai-decision-layer--mt_agents) · [02 F4](../../../docs/02-v1-architecture.md#8-end-to-end-flows) steps 1–3 · [research: TradingAgents/FinRobot](../../../docs/research/agents-tradingagents-finrobot.md) (TradingAgents v0.7.0 graph, Pydantic schemas, quick/deep tiers)
- UI: [D09](../../../docs/ui/dashboards/D09-agents.md) `/agents/runs/:id` stage timeline
- Security: [07 §6](../../../docs/07-security-notes.md#6-application-controls), [02 §9.1](../../../docs/02-v1-architecture.md#91-security)
- Cross-phase: P0 R0.09 gateway roles
- Depends on (this phase): P6-T004, P6-T005, P6-T006

## Requirements

- Stages: analysts (technical, sentiment, news, fundamentals, macro/events) → bull/bear debate (configurable rounds, default 2) → research manager → trader → risk debate (aggressive / conservative / neutral) → PM → Signal.
- Depth presets quick/standard/deep map to model routes: analysts on `local-advisor` or `research-primary` (quick tier), managers/PM on `research-primary` (deep tier); local-only option.
- Each `AgentTurn` stored with role, stance, confidence, text, cited provenance ids, tool calls; turns are part of `decision_run.stages`.
- PM output validated against the Signal v2 schema; invalid output → one repair attempt, else run `status=failed` (no Signal).
- Memory recall node (bank `decisions`, `market-regimes`) with `as_of` (wired in P6-T012).
- Checkpointing so a crashed run resumes from the last completed stage.
- Budget preflight: estimated tokens/cost shown and checked against the role budget before the run (P6-T009).

## ToDo

- [ ] Vendor/adapt the TradingAgents graph (Apache-2.0) into `packages/mt_agents/mt_agents/graph/`; strip its own data vendors and replace with P6-T006 tools.
- [ ] Prompts per role into the prompt registry (P6-T005) with versions.
- [ ] Pydantic/msgspec schemas per stage output; PM → Signal v2 mapper.
- [ ] LangGraph checkpointer on Postgres (`agents` schema or `ops.agent_checkpoint`).
- [ ] Write `audit.decision_run` + `audit.signal`; publish `sig.agent.*`.
- [ ] `agents` container in Compose (internal network only, digest-pinned base image).
- [ ] Sample-run fixtures (recorded gateway responses) for deterministic tests.

## Verification

### Tests
- Unit: stage schemas, PM→Signal mapper, repair path.
- Integration (recorded LLM responses): full graph on BTCUSDT.BINANCE and an equity produces a valid Signal with ≥ 1 provenance per numeric claim.
- Golden: stage order and turn count for a fixed config.

### Scenarios
- Given a request for `EURUSD` standard depth, when run, then D09 receives `agents.run` events per stage and a Signal is stored.
- Given the PM returns malformed JSON twice, then the run fails cleanly, cost is still audited and no Signal is emitted.
- Given the gateway budget for `debate` is exhausted, then the run uses local routes and the run row shows `fallback_used`.

### Stress / failure injection
- Kill the `agents` container mid-risk-debate; on restart the run resumes from checkpoint without duplicating LLM calls already audited.
- Run 5 analyses concurrently: no cross-run state leakage (run_id isolation test).

## Acceptance criteria

- [ ] A standard-depth run produces a Signal with provenance in ≤ the configured timeout (default 10 min).
- [ ] Every LLM call of the run is in `audit.llm_call` with the run's `run_id`.
- [ ] CI green.

## Exceptions & edge cases

- Instrument without fundamentals → fundamentals analyst returns `DATA_UNAVAILABLE`, not invented numbers.
- Gateway fully down → run fails fast with a clear status; no partial Signal.
- Long debates truncated by a per-stage token cap; truncation noted in the turn.

## Cardinal rules (do NOT)

- Do NOT let the graph place orders or call commands; the Signal is its only output.
- Do NOT run the graph per tick.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M8: stage list, depth presets, checkpointing.
- `third_party/LICENSES.md`: TradingAgents entry.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.20 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T007-debate-graph`
- PR title: `P6-T007: LangGraph debate graph producing a sourced Signal`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T007` run

## Progress log

- 2026-10-21 00:00 · planner · created
