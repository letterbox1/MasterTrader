---
id: P6-T007
kind: task
title: Debate graph on mt-agents producing a sourced Signal
phase: 6
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T004, P6-T005, P6-T006, P6-T074, P0-T042, P0-T044]
requirements: [R6.01]
roadmap_todos: [T6.20]
modules: [M8]
dashboards: [D09]
tools: [git, cargo, docker]
mcp: []
env: []
services: [litellm, llm-local, supabase-postgres, nats]
branch: p6/P6-T007-debate-graph
pr: ""
doc_sync: [docs/03-build-spec.md, docs/19-third-party-register.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T007 · Debate graph on mt-agents producing a sourced Signal

## Goal / expected outcome

`mt-agents` runs a TradingAgents-style debate graph, rebuilt in Rust on the P6-T074 runtime from TradingAgents' Apache-2.0 design with prompts adapted and NOTICE kept (analysts → bull/bear → research manager → trader → risk debate → portfolio manager) through the gateway and emits one `Signal` v2 with provenance, stored in `audit.decision_run`/`audit.signal`.

## Context & references

- Roadmap: [R6.01](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.20
- Spec: [03 M8](../../../docs/03-build-spec.md#m8-ai-decision-layer--mt_agents) · [02 F4](../../../docs/02-v1-architecture.md#8-end-to-end-flows) steps 1–3 · [research: TradingAgents/FinRobot](../../../docs/research/agents-tradingagents-finrobot.md) (TradingAgents v0.7.0 graph, Pydantic schemas, quick/deep tiers)
- UI: [D09](../../../docs/ui/dashboards/D09-agents.md) `/agents/runs/:id` stage timeline
- Security: [07 §6](../../../docs/07-security-notes.md#6-application-controls), [02 §9.1](../../../docs/02-v1-architecture.md#91-security)
- Cross-phase: P0-T042 (gateway roles, `audit.llm_call` writer), P0-T044 (`local-advisor` for keyless runs)
- Verified by: P6-T067 (sample runs, T6.66, keyless) and P6-T070 (live provider with your keys)
- Depends on (this phase): P6-T004, P6-T005, P6-T006

## Requirements

- **No TradingAgents code** ([19 §3](../../../docs/19-third-party-register.md#3-borrowed-designs-rebuilt-in-rust-no-third-party-code-in-the-runtime)): the design is rebuilt in Rust; the filing look-ahead leak fixed upstream in 0.7.1 is covered by the `pit(as_of)` tools, and memory lessons are keyed by decision date ([01 §3.6](../../../docs/01-repo-vetting-report.md#36-tradingagents--ai-decision-layer-pattern)). The optional research workflows (P6-T071) and persona lenses (P6-T072) plug in as extra debate inputs.
- Stages: analysts (technical, sentiment, news, fundamentals, macro/events) → bull/bear debate (configurable rounds, default 2) → research manager → trader → risk debate (aggressive / conservative / neutral) → PM → Signal.
- Depth presets quick/standard/deep map to model routes: analysts on `local-advisor` or `research-primary` (quick tier), managers/PM on `research-primary` (deep tier); local-only option.
- Each `AgentTurn` stored with role, stance, confidence, text, cited provenance ids, tool calls; turns are part of `decision_run.stages`.
- Built and tested keyless (build first, keys last): `local-advisor` + recorded gateway responses; no API key is needed to finish this task.
- PM output validated against the Signal schema (every 03 M8 field); invalid output → one repair attempt, else run `status=failed` (no Signal).
- Memory recall node (bank `decisions`, `market-regimes`) with `as_of` (wired in P6-T012).
- Checkpointing (P6-T074 Postgres checkpoints) so a crashed run resumes from the last completed stage.
- Budget preflight: estimated tokens/cost shown and checked against the role budget before the run (P6-T009).

## ToDo

- [ ] Build the debate graph in `crates/mt-agents/src/graph/debate.rs` from TradingAgents' design (no code copied); data only from the P6-T006 tools; adapted prompt text noted in `crates/mt-agents/NOTICE`.
- [ ] Prompts per role into the prompt registry (P6-T005) with versions.
- [ ] serde schemas per stage output; PM → Signal v2 mapper (`mt-core` types).
- [ ] Use the P6-T074 checkpoints (`ops.agent_checkpoint`) at every stage.
- [ ] Write `audit.decision_run` + `audit.signal`; publish `sig.agent.*`.
- [ ] Register the debate graph in the `agents` container from P6-T074 (internal network only).
- [ ] Sample-run fixtures (recorded gateway responses) for deterministic tests.

## Verification

### Tests
- `cargo test -p mt-agents debate` and `cargo clippy`.
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
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M8: stage list, depth presets, checkpointing.
- `docs/19-third-party-register.md` §3: confirm the TradingAgents row (design and prompts, NOTICE).
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.20 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T007-debate-graph`
- PR title: `P6-T007: Debate graph on mt-agents producing a sourced Signal`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T007` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (Signal = 03 M8 fields; keyless build on local-advisor/recorded responses, live check in P6-T070; cross-phase deps P0-T042/P0-T044; run fields)
- 2026-11-19 00:00 · coordinator · TradingAgents pin ≥ 0.7.1; links to P6-T071/T072 (17 §F)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (services supabase-postgres; agents stay Python (18 §2.2))
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (debate graph rebuilt in Rust on the `mt-agents` runtime (P6-T074) instead of LangGraph/vendored TradingAgents; checkpoints from P6-T074; tools cargo)
