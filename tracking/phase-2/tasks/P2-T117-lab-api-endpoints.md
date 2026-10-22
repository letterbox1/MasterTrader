---
id: P2-T117
kind: task
title: Lab REST queries, WebSocket topic and commands in mt_api
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T101, P2-T107, P2-T114, P0-T034, P0-T035, P0-T036]
requirements: [R2.40, R2.44, R2.50]
roadmap_todos: [T2.27, T2.32]
modules: [M7, M15]
dashboards: [D04, D03]
tools: [uv, pnpm]
mcp: []
env: []
services: [nats, postgres]
branch: p2/P2-T117-lab-api-endpoints
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T117 · Lab REST queries, WebSocket topic and commands in mt_api

## Goal / expected outcome

`mt_api` serves every lab query, the `lab.job` WebSocket topic and the lab commands that D03/D04 need, with OpenAPI types generated for the web app.

## Context & references

- Roadmap: [R2.40, R2.44, R2.50](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDos T2.27, T2.32
- [02 §7.1 queries](../../../docs/02-v1-architecture.md#71-queries-rest-read) (`/lab/backtests`, `/lab/experiments`, `/lab/jobs`) · [02 §7.2 commands](../../../docs/02-v1-architecture.md#72-commands-rest-write) (`lab.backtest.run`, `lab.sweep.run`, `lab.validate.run`, `lab.generate_strategy`, `lab.job.cancel`) · [02 §7.3 WS](../../../docs/02-v1-architecture.md#73-real-time-websocket-apiv1ws)
- Backend contracts: [D04](../../../docs/ui/dashboards/D04-research-lab.md) and [D03](../../../docs/ui/dashboards/D03-strategies.md) (`/strategies/{id}?gates=1`, `/strategies/templates`)
- Cross-phase (`depends_on`): command bus (P0-T034), confirmation levels (P0-T035), WS hub (P0-T036), all T0.24.
- Decisions: `lab.leakage.waive` is **C2** and tier-A training is `models.tiera.train` (C1) ([17 §D P2-B056/B057](../../../docs/17-decisions-register.md#d-other-decisions), [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write)).

## Requirements

- Queries: `GET /lab/backtests` (cursor pagination, filters strategy/engine/status), `/lab/backtests/{id}` (summary, trades, robustness, bias, costs, gates, reproduce sections), `/lab/experiments`, `/lab/experiments/{id}` (compare ≤ 6 runs), `/lab/jobs`, `/data/costs?snapshot=`.
- `/strategies/{id}?gates=1` returns gate list + reasons from P2-T114; `?metrics=1` returns latest truth metrics.
- Commands: `lab.backtest.run`, `lab.sweep.run`, `lab.validate.run`, `lab.generate_strategy`, `lab.job.cancel`, `lab.gate_report.generate` (C1); `lab.leakage.waive` (**C2**, reason required); `models.tiera.train` (C1: train → calibrate → compile); all with idempotency keys and `audit.command` rows.
- WS topic `lab.job` fans out `lab.job.*` at ≤ 1 Hz per job with `seq` for gap detection.
- Decimals as strings, ISO-8601 UTC times, problem+json errors.

## ToDo

- [ ] Add routers in `packages/mt_api/routers/lab.py` and gates/metrics params on strategies router
- [ ] Register command handlers that enqueue jobs (P2-T101) and the waiver handler (P2-T113)
- [ ] WS fan-out for `lab.job`
- [ ] Regenerate OpenAPI + `openapi-typescript` client for `apps/web`
- [ ] Contract tests vs D03/D04 backend contracts

## Verification

### Tests
- API tests for each endpoint (pagination, filters, 404s, problem+json).
- Command tests: idempotency key dedupes; `audit.command` row written with source=web.
- WS test: progress events received in order; a forced gap triggers REST re-sync.

### Scenarios
- Given the backtest-worker is down, when `lab.backtest.run` is sent, then the job is queued and the UI shows 'queued (no worker)'.
- Given a compare request with 7 runs, then 422 problem+json 'max 6 runs'.

### Stress / failure injection
- 50 concurrent clients subscribed to `lab.job` while 20 jobs run: server throttles to ≤ 1 Hz per job; API p95 < 200 ms for list endpoints.

## Acceptance criteria

- [ ] All D04 and D03 lab/gate contract items served
- [ ] OpenAPI regenerated and web types compile
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- mt-api down: lab jobs already queued keep running in backtest-worker; results visible once API returns.
- Large trade lists paginated server-side (cursor).

## Cardinal rules (do NOT)

- Do NOT expose lab endpoints that write orders or touch venues.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7: confirm `lab.leakage.waive` (C2), `models.tiera.train` (C1) and the gates/metrics query params as built.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.27, T2.32 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T117-lab-api-endpoints`
- PR title: `P2-T117: Lab REST queries, WebSocket topic and commands in mt_api`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T117` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (lab.leakage.waive C2 and models.tiera.train C1 per 17 §D; cross-phase API deps)
