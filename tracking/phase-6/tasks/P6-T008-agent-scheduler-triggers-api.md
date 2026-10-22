---
id: P6-T008
kind: task
title: Agent scheduler, event triggers and the agents API
phase: 6
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T007, P6-T009, P0-T034, P0-T036]
requirements: [R6.02, R6.01]
roadmap_todos: [T6.20]
modules: [M8, M15]
dashboards: [D09]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [prefect, nats, postgres, mt-api]
branch: p6/P6-T008-agent-scheduler-triggers-api
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T008 · Agent scheduler, event triggers and the agents API

## Goal / expected outcome

Agent runs start only on a configured cadence, on events (anomaly, calendar, big news) or on request (`agents.run_analysis`), **never per tick**, with debounce and budget preflight; `/agents/runs`, `/signals` and WS `agents.run`/`signals` serve D09.

## Context & references

- Roadmap: [R6.02](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.01](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.20
- Spec: [03 §7](../../../docs/03-build-spec.md#7-llm-cost-control) (cadence, event-triggered, never per tick) · [02 F4](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 1 · [02 §7.1](../../../docs/02-v1-architecture.md#71-queries-rest-read) · [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) (`agents.run_analysis` C1) · [02 §7.3](../../../docs/02-v1-architecture.md#73-real-time-websocket-apiv1ws)
- UI: [D09](../../../docs/ui/dashboards/D09-agents.md) (New analysis, Runs list, Signals; Schedule recurring analysis via `system.settings.update`)
- Depends on (this phase): P6-T007, P6-T009
- Cross-phase: P0-T034 (command bus, `audit.command`), P0-T036 (WebSocket hub)
- Verified by: P6-T052 (scheduler test, T6.67)

## Requirements

- Prefect deployment per schedule (`agents-scheduled-<id>`), cron from settings; LLM-signal strategies declare cadence in their manifest.
- NATS triggers: `alert.anomaly.*` (P6-T014), `cal.*` within N minutes of high-impact events, `text.doc.new` with tier-B `event_type` severity ≥ threshold; trigger rules in settings.
- Debounce: max 1 run per (subject, trigger kind) per configurable window (default 30 min); global max concurrent runs (default 2); no subscription to `md.*` at all.
- `agents.run_analysis` command (C1) with args subject, depth, route, context toggles; response returns `run_id` and budget estimate.
- API: `GET /agents/runs` (+ `/{id}`, `?settled=1&metrics=1`), `GET /signals`; WS topics `agents.run` (stage progress) and `signals`.

## ToDo

- [ ] Scheduler module `mt_agents.scheduler` (Prefect deployments + NATS consumer for triggers).
- [ ] Trigger rules + debounce store (NATS KV `agent_debounce`).
- [ ] `mt_api` command handler + queries + WS fan-out.
- [ ] Static check/test: `mt_agents` never subscribes to `md.*`.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: debounce, trigger rule matching, budget preflight rejection.
- Integration: anomaly event → exactly one run; 20 duplicate events in 5 min → one run.
- API tests: command levels enforced server-side (C1), idempotency key honoured.

### Scenarios
- Given a tick storm on BTCUSDT, when 100k `md.*` messages arrive, then zero agent runs start.
- Given an FOMC calendar item 30 min ahead and the rule enabled, then one macro run starts for the configured instruments.
- Given the role budget is exhausted and local fallback disabled, then the command returns problem+json `budget_exhausted`.

### Stress / failure injection
- Flood 1,000 `text.doc.new` events/min: run count stays ≤ concurrency cap; queue drains; no OOM.

## Acceptance criteria

- [ ] Scheduler tests prove no per-tick path.
- [ ] D09 can list runs and signals via the API.
- [ ] Command written to `audit.command` with source.

## Exceptions & edge cases

- Prefect down: scheduled runs are missed and alerted (not back-filled in a burst); event triggers still work via NATS.
- Restart: debounce state survives in KV.

## Cardinal rules (do NOT)

- Do NOT subscribe agents to tick/quote/book streams.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7: confirm `/agents/runs` params and WS payloads.
- `docs/03-build-spec.md` §7: trigger list and debounce defaults.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.20 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T008-agent-scheduler-triggers-api`
- PR title: `P6-T008: Agent scheduler, event triggers and the agents API`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T008` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (cross-phase deps P0-T034/P0-T036; scheduler test is T6.67 (P6-T052); run fields)
