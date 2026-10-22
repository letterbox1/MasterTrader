---
id: P0-T048
kind: task
title: Build the typed API client and WebSocket client with gap re-sync
phase: 0
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T047, P0-T036]
requirements: [R0.08, R0.11]
roadmap_todos: [T0.26]
modules: [M15]
dashboards: []
tools: [git, node>=20, pnpm]
mcp: []
env: []
services: []
branch: p0/P0-T048-web-typed-api-and-ws-client
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md]
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

# P0-T048 · Build the typed API client and WebSocket client with gap re-sync

## Goal / expected outcome

The web app talks to mt-api through a generated, typed REST client (TanStack Query) and a typed WebSocket client that feeds the Query cache, detects `seq` gaps, shows a "Re-syncing" state, refetches the matching REST query and resumes; commands go through a helper that handles preview tokens, idempotency keys and problem+json.

## Context & references

- [Roadmap P0 R0.08, R0.11](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [02 §7.3 WebSocket](../../../docs/02-v1-architecture.md#73-real-time-websocket-apiv1ws)
- [02 §10 frontend](../../../docs/02-v1-architecture.md#10-frontend-architecture)
- [ui §3.4 real-time](../../../docs/ui/README.md#34-real-time)
- [ui §3.3 confirmation](../../../docs/ui/README.md#33-actions--confirmation) (idempotency per confirm sheet)
- Depends on: P0-T047, P0-T036

## Requirements

- REST: `fetch` wrapper with `credentials: 'same-origin'`, CSRF header, problem+json → typed `ApiError` (with `trace_id`), 401 → login route.
- Commands: `useCommand(name)` → `preview()` then `execute({args, idempotency_key: uuidv7(), confirm_token})` (02 §7.2); handles 428 `confirmation_required` and `reauth_required` (C2 needs a re-auth within 12 h → re-auth prompt, then retry), 409 replay, C3 pending states (incl. 'Waiting for break-glass approval', ui §3.3).
- WS: single connection, auto-reconnect (backoff 0.5 s → 30 s, jitter), subscriptions restored on reconnect; per-topic `lastSeq`; on gap (`seq != lastSeq+1`) mark topic `resyncing`, invalidate the mapped query, resume after refetch.
- Background tabs: drop to 0.2 Hz except `kill`, `notifications` (ui §3.4).
- Decimals stay strings in JS (no `parseFloat` on money); formatters in P0-T049.

## ToDo

- [ ] Implement `src/lib/api` and `src/lib/ws` with topic→query mapping.
- [ ] Implement `useCommand`.
- [ ] Unit tests with a mock WS server (mock-socket) and MSW for REST.

## Verification

### Tests
- Unit: gap detection triggers refetch exactly once; reconnect restores subscriptions.
- Unit: 428 → preview flow; 428 `reauth_required` → re-auth prompt → retry; 409 replay surfaces the original result.
- Unit: no `parseFloat` on decimal fields (eslint rule + test).

### Scenarios
- Given the server drops messages for a slow client, then the UI shows 'Re-syncing' briefly and ends consistent with REST.
- Given the session expires, when the WS closes with 4401, then the app routes to login and preserves the target route.

### Stress / failure injection
- Mock 1,000 msgs/s on one topic for 30 s → UI thread stays responsive (throttled to 1 Hz render), memory stable.

## Acceptance criteria

- [ ] Typed REST + WS clients with tests
- [ ] Gap → re-sync proven
- [ ] Command helper handles preview, idempotency, 428/409
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check, Playwright viewport matrix)

## Exceptions & edge cases

- Clock skew between client and server: display uses server `ts`; relative times computed against a server-offset estimate.

## Cardinal rules (do NOT)

- Do NOT call brokers or any backend other than mt-api from the browser.
- Do NOT convert money strings to floats.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- None beyond the roadmap tick.
- `docs/roadmap/phase-0-foundations.md`: tick T0.26 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T048-web-typed-api-and-ws-client`
- PR title: `P0-T048: Build the typed API client and WebSocket client with gap re-sync`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T048` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (confirm_token name and C2 12 h re-auth handling (02 §7.2, 17 §D P0-B003); run fields added)
