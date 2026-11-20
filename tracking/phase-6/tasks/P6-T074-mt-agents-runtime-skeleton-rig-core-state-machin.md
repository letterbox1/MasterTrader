---
id: P6-T074
kind: task
title: mt-agents runtime skeleton: rig-core, state-machine graph, Postgres checkpoints, gateway client
phase: 6
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T042]
requirements: [R6.01, R6.02, R6.03]
roadmap_todos: [T6.20]
modules: [M8, mt-agents, M17]
dashboards: [D09]
tools: [git, cargo, docker, supabase]
mcp: []
env: []
services: [litellm, llm-local, supabase-postgres, nats]
branch: p6/P6-T074-mt-agents-runtime-skeleton-rig-core-state-machin
pr: ""
doc_sync: [docs/03-build-spec.md, docs/18-platform-and-deployment.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-20
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-T074 · mt-agents runtime skeleton: rig-core, state-machine graph, Postgres checkpoints, gateway client

## Goal / expected outcome

The `mt-agents` crate exists as a small Rust runtime that every agent workload builds on: an explicit state-machine graph on `rig-core`, Postgres checkpoints so a crashed run resumes at its last finished node, one LiteLLM gateway client for every model call, a prompt loader, a read-only tool trait, and a run record linking every call to `audit.llm_call`. The debate graph (P6-T007), the explain agent (P6-T015), research workflows (P6-T071), persona lenses (P6-T072) and the crowd simulator (P6-T050) all sit on it, so it is kept free of Phase 6 dependencies and can be built as soon as the P0 gateway exists.

## Context & references

- Roadmap: [R6.01](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.02](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.03](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.20 (the `mt-agents` runtime part)
- Stack: [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-agents`: `rig-core` (MIT), explicit state-machine graph, Postgres checkpoints, all calls through LiteLLM; replaces LangGraph) · [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20) · [19 §3](../../../docs/19-third-party-register.md#3-borrowed-designs-rebuilt-in-rust-no-third-party-code-in-the-runtime) (designs rebuilt in Rust, NOTICE for copied prompt text)
- Spec: [03 M8](../../../docs/03-build-spec.md#m8-ai-decision-layer) · [03 §7](../../../docs/03-build-spec.md#7-llm-cost-control) (never per tick) · [10 §5](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21) (gateway routes and per-role keys)
- Audit: [03 M17](../../../docs/03-build-spec.md#m17-observability--audit); `audit.llm_call` is written by the P0 LiteLLM callback ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P6-B010), never by a second writer
- Security: [07 §6](../../../docs/07-security-notes.md#6-application-controls) (read-only agent tools, untrusted text wrapped)
- Cross-phase: P0-T042 (LiteLLM gateway, routes, per-role virtual keys, audit callback; it already depends on Compose, secrets, the WORM audit tables and the `mt_store` module). Workspace (P0-T014), Supabase stack (P0-T070) and `mt-core` types (P0-T016) come in through it or are used when present
- Used by: P6-T005 (prompt/model versioning), P6-T006 (tool belt), P6-T007 (debate graph), P6-T008 (triggers), P6-T015 (explain agent), P6-T050 (`mt-crowdsim` persona agents), P6-T071, P6-T072

## Requirements

- **Crate:** `crates/mt-agents` in the Cargo workspace; `rig-core` pinned (MIT; licence row checked by `just licence-audit`, P0-T074).
- **Graph:** a typed, explicit state machine: nodes (`async fn(State, Ctx) -> Result<Transition>`), named edges and conditional edges, a max-step guard, per-node timeout and token cap. A graph is plain Rust data: it can be printed as a diagram and its node order is tested. No hidden loops.
- **Checkpoints:** after every node the run state is written to Postgres (`ops.agent_checkpoint`: run_id, graph, node, step, state JSON, created_at; insert-only), via a plain SQL migration in `supabase/migrations/`. `resume(run_id)` restarts at the last finished node and never repeats a model call that already returned.
- **Gateway client:** one OpenAI-compatible client (rig-core provider) pointed at LiteLLM only; per-role virtual key (`debate`, `strategy-gen`, `explain`, `memory`, `chat`, `shadow`) and route (`research-primary`, `research-custom`, `local-advisor`) chosen per node; request metadata carries `role`, `run_id`, `node`, `prompt_name`, `prompt_version` so the P0 callback stores them. No provider SDK or provider host is reachable from the crate (CI check).
- **Audit:** every call made by the runtime lands in `audit.llm_call` (written by the P0 callback). The run record (`ops.agent_run`: run_id, graph, trigger, status, started/finished, fallback_used) links to those rows by `run_id`; a reconciliation query shows calls per run = audit rows per run.
- **Prompts:** loader for `crates/mt-agents/prompts/<role>/<name>@<semver>.md` and `crates/mt-agents/skills/` (front matter, sha256); P6-T005 adds the version CI check. Copied third-party prompt text keeps its notice in `NOTICE`.
- **Tools:** a `Tool` trait whose implementations may only read through `pit(as_of)` (the `mt-store` crate) and return `sources[]`; no tool can write, place orders or call `mt-api` commands. Untrusted text is wrapped before it reaches a prompt; rows with `model_input_ok = false` (Telegram, synthetic) are refused at the trait boundary. The concrete tools come in P6-T006.
- **Budgets:** budget errors from LiteLLM map to the local route (`fallback_used = true`) per 16 §2.10; nothing is hard-coded (route and role per graph come from settings).
- **Cadence:** the runtime has no market-data subscription at all; runs start only from a command, a schedule or an event (wired in P6-T008).
- **Keyless:** built and tested with a fake OpenAI-compatible server and recorded responses, plus `local-advisor`; no API key needed to finish.
- **Container:** `agents` image built from the workspace, digest-pinned base, internal network only.

## ToDo

- [ ] Create `crates/mt-agents` (graph, node, edge, state, runner, guards) on `rig-core`; add to the workspace.
- [ ] SQL migration in `supabase/migrations/` for `ops.agent_run` and `ops.agent_checkpoint` (insert-only grants for the agents role).
- [ ] Checkpoint writer and `resume(run_id)`; idempotent replay of completed nodes from the checkpoint, not from the model.
- [ ] Gateway client: per-role key and route per node, request metadata, error mapping (budget → local route, gateway down → run fails fast).
- [ ] Prompt loader (prompts and skills directories, sha256); `NOTICE` file in the crate.
- [ ] `Tool` trait with the `pit`-only, read-only contract and the untrusted/`model_input_ok` boundary.
- [ ] Run record + reconciliation query (calls per run vs `audit.llm_call` rows).
- [ ] CI checks: no provider SDKs or hosts in the crate; no `md.*` subscription; `cargo deny` licence row for `rig-core`.
- [ ] A two-node example graph and fake-gateway fixtures used by the tests.
- [ ] `agents` container in Compose (internal network, digest-pinned).
- [ ] Tests (see Verification); docs.

## Verification

### Tests
- `cargo test -p mt-agents` and `cargo clippy`; `supabase test db` for the checkpoint tables (insert-only grants).
- Unit: edge routing, conditional edges, max-step guard, per-node timeout; prompt loader hashing; error mapping.
- Integration (fake gateway + Postgres): a three-node graph runs to completion; every call carries `run_id`, `role`, `node` in its metadata and appears once in `audit.llm_call` via the P0 callback.
- Static: the crate has no dependency on a provider SDK and no NATS `md.*` subscription.

### Scenarios
- Given a run killed after node 2 of 3, when it resumes, then node 3 runs, nodes 1–2 are read from the checkpoint and no extra model call is audited for them.
- Given the `debate` role budget is exhausted, when a node calls the gateway, then the call is served by `local-advisor` and the run shows `fallback_used`.
- Given a tool returns a row with `model_input_ok = false`, then the runtime refuses it before any prompt is built and counts the refusal.

### Stress / failure injection
- 20 concurrent runs of the example graph: no state leaks between runs (run_id isolation), checkpoint write p95 < 20 ms.
- Postgres paused 30 s mid-run: the run waits and resumes; gateway down: the run fails fast with a clear status and no partial output.

## Acceptance criteria

- [ ] `crates/mt-agents` builds in the workspace; the example graph runs keyless.
- [ ] Crash-resume proven without duplicate model calls.
- [ ] Calls per run reconcile with `audit.llm_call` (difference 0).
- [ ] CI green (`cargo test`, `cargo clippy`, `cargo deny`, `supabase test db`, `pit` bypass check).

## Exceptions & edge cases

- `rig-core` lacks a feature we need (e.g. a LiteLLM metadata field): wrap it in our client rather than calling a provider directly.
- Run state that would grow past the checkpoint size cap (default 1 MB, a setting) is truncated with a note in the run record.
- A schema change to a graph's state bumps the graph version; old checkpoints of a different version are not resumed (the run is marked `abandoned`).

## Cardinal rules (do NOT)

- Do NOT call a model provider directly; every call goes through the LiteLLM gateway.
- Do NOT write a second `audit.llm_call` writer; the P0 callback is the only one.
- Do NOT give the runtime or its tools any write path, order path or `mt-api` command; agents output data only.
- Do NOT subscribe to `md.*` or run anything per tick.
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`.
- Do NOT let Telegram text or `synthetic = true` rows (any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT copy code from TradingAgents, FinRobot or any other source into the runtime; designs only, prompts with NOTICE (19 §3).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry in dependencies.

## Doc sync on completion

- `docs/03-build-spec.md` M8: runtime contract (graph, checkpoints, gateway client, tool trait).
- `docs/18-platform-and-deployment.md` §2.1: confirm the `mt-agents` row (rig-core version, checkpoint tables).
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.20 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T074-mt-agents-runtime-skeleton-rig-core-state-machin`
- PR title: `P6-T074: mt-agents runtime skeleton: rig-core, state-machine graph, Postgres checkpoints, gateway client`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T074` run

## Progress log

- 2026-11-20 01:08 · cloud:vm:be04b6ae61f8 · created
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (filled from the stub: `mt-agents` runtime on rig-core with Postgres checkpoints, gateway client and audit link; depends only on P0-T042)
