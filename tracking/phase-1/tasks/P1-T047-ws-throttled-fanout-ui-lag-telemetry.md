---
id: P1-T047
kind: task
title: Throttle WebSocket fan-out and measure UI update lag
phase: 1
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T046, P0-T036, P0-T048]
requirements: [R1.N2, R1.15]
roadmap_todos: [T1.32]
modules: [M15]
dashboards: [D07, D02]
tools: [git, uv, docker, pnpm, node>=20]
mcp: []
env: []
services: [mt-api, nats]
branch: p1/P1-T047-ws-throttled-fanout-ui-lag-telemetry
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/02-v1-architecture.md, docs/ui/README.md]
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

# P1-T047 · Throttle WebSocket fan-out and measure UI update lag

## Goal / expected outcome

The `mt_api` WebSocket hub fans out `md.*`, `dq.status`, `cost`, `recon` and `notifications` topics with server-side throttling (≤ 4 Hz per symbol for charts, ≤ 1 Hz for tables, 0.2 Hz for background tabs) and the web app reports local server→screen lag so p95 < 500 ms can be proven.

## Context & references

- Roadmap: requirements [R1.N2](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.15](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.32](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- SLO: [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos) (UI live update lag p95 < 500 ms, client telemetry local only) · throttling [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) rules and [ui §3.4 real-time](../../../docs/ui/README.md#34-real-time) · WS protocol [02 §7.3](../../../docs/02-v1-architecture.md#73-real-time-websocket-apiv1ws)
- Depends on (this phase): P1-T046
- Cross-phase prerequisites (depends_on): P0-T036 (WebSocket hub), P0-T048 (typed API and WS client)

## Requirements

- Topics: `md.quote`, `md.trade`, `md.book`, `md.bar`, `dq.status`, `cost`, `recon`, `lab.job`, `notifications`; envelope `{topic, seq, ts, data}` from P0
- Throttle per (client, topic, symbol): latest-value coalescing (never queue stale updates); chart topics ≤ 4 Hz, table topics ≤ 1 Hz; `dq.status` changes are never dropped (state topics bypass coalescing but are rate-limited to 4 Hz)
- Background-tab hint from client → 0.2 Hz except alerts/kill/`dq.status`
- Client telemetry: on render, compute `now − envelope.ts` (clock offset estimated via a `/time` ping), batch to `/api/v1/telemetry/ui-lag` (local only, never external), exported as Prometheus histogram `mt_ui_lag_seconds{topic}`

## ToDo

- [ ] Implement coalescing throttler in the WS hub
- [ ] Implement client lag measurement in `apps/web/src/lib/ws` and the telemetry endpoint
- [ ] Grafana panel for UI lag p95
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: throttler emits ≤ 4 msgs/s per symbol under a 100 Hz input and always the latest value
- Integration: Playwright test subscribes to a synthetic 50 Hz feed; measured lag p95 < 500 ms and update rate ≤ 4 Hz

### Scenarios

- Given a WS gap, when the client detects `seq` skip, then it shows "Re-syncing", refetches via REST and resumes
- Given a tab goes to background, when hinted, then rates drop to 0.2 Hz except `dq.status`

### Stress / failure injection

- Load: 20 clients × 50 symbols at 100 Hz input; hub CPU < 1 core, lag p95 < 500 ms (feeds P1-T062)

## Acceptance criteria

- [ ] Throttle limits enforced in tests; UI lag histogram exported; p95 < 500 ms in the Playwright test
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Client clock skew: offset estimation keeps lag measurement honest; telemetry never leaves the host

## Cardinal rules (do NOT)

- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.32 once every task traced to it in PHASE.md is done; note P1-T047 next to it.
- `docs/02-v1-architecture.md` §9.2: how UI lag is measured
- `docs/ui/README.md` §3.4: confirm throttle behaviour for state topics

## Branch & PR

- Branch: `p1/P1-T047-ws-throttled-fanout-ui-lag-telemetry`
- PR title: `P1-T047: Throttle WebSocket fan-out and measure UI update lag`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T047` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields; P0 WS hub and client deps)
