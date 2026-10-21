---
id: P0-T036
kind: task
title: Implement the WebSocket hub with seq gap detection
phase: 0
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T032, P0-T033]
requirements: [R0.08]
roadmap_todos: [T0.24]
modules: [mt_api]
dashboards: []
branch: p0/P0-T036-websocket-hub
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T036 · Implement the WebSocket hub with seq gap detection

## Goal / expected outcome

`/api/v1/ws` authenticates with the session cookie, supports `{op: sub|unsub, topic, params}`, bridges NATS subjects to topics, and sends envelopes `{topic, seq, ts, data}` with a per-connection, per-topic monotonic `seq` so clients detect gaps and re-sync via REST. P0 topics: `system`, `heartbeat`, `kill`, `notifications`.

## Context & references

- [Roadmap P0 R0.08](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [02 §7.3 WebSocket](../../../docs/02-v1-architecture.md#73-real-time-websocket-apiv1ws)
- [02 §6 NATS](../../../docs/02-v1-architecture.md#6-messaging-nats) (UI streams ≤ 4 Hz charts, ≤ 1 Hz tables)
- [ui §3.4 real-time](../../../docs/ui/README.md#34-real-time)
- Depends on: P0-T032, P0-T033

## Requirements

- Auth: cookie session checked at upgrade; Origin header must match the Caddy host; idle sockets closed after session expiry.
- Envelope: `{topic, seq, ts, data}`; `seq` starts at 1 per (connection, topic) and increments per **delivered or dropped** message, so server-side drops (slow consumer) appear as gaps.
- Backpressure: per-connection queue 1,000 messages; overflow drops oldest and increments seq (client re-syncs); `mt_ws_dropped_total` metric.
- Throttle: per-topic max rate (P0 topics 1 Hz except `kill`/`notifications` unthrottled); coalesce to latest value.
- Bridges: `sys.heartbeat.*` → `heartbeat`; KV `kill` watch → `kill`; `audit.command.*` + `alert.*` → `notifications`; service status → `system`.
- Snapshot on subscribe: first message after `sub` is a full snapshot (seq 1) so clients start consistent.
- Ping/pong every 20 s; close code 4401 on auth expiry, 4429 on abuse.

## ToDo

- [ ] Implement hub, topic registry, NATS bridges, throttling/backpressure.
- [ ] Add the four P0 topics with REST counterparts for re-sync (`/system/services`, `/risk/state` kill subset, `/notifications`).
- [ ] Document the protocol in OpenAPI `x-websocket` extension + README.
- [ ] Tests below.

## Verification

### Tests
- Integration: subscribe → snapshot seq 1 → updates seq 2..n.
- Gap: force a slow consumer → client observes a seq jump; re-sync endpoint returns the latest state.
- Auth: no cookie → 4401; wrong Origin → rejected.

### Scenarios
- Given NATS restarts, when bridges reconnect, then subscribers get a new snapshot (seq continues incrementing) and no stale kill state is shown.
- Given the kill switch is set from another device, then every open client receives `kill` within 500 ms (02 §9.2 UI lag p95 < 500 ms).

### Stress / failure injection
- Fan-out: 50 clients × 4 topics with 100 msg/s injected for 10 min → p95 server→client lag < 500 ms, memory stable (logged).

## Acceptance criteria

- [ ] Envelope + seq semantics implemented and documented
- [ ] Gap detection proven with a forced drop
- [ ] Kill propagation < 500 ms p95 in test
- [ ] Auth/Origin enforced
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Browser background tabs throttle to 0.2 Hz client-side (ui §3.4) except kill/approvals/notifications; server keeps sending those.

## Cardinal rules (do NOT)

- Do NOT accept unauthenticated WebSocket connections.
- Do NOT use WS for writes; commands go through `/commands`.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7.3: document seq semantics (per connection/topic, drops count) and snapshot-on-subscribe.
- `docs/roadmap/phase-0-foundations.md`: tick T0.24 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T036-websocket-hub`
- PR title: `P0-T036: Implement the WebSocket hub with seq gap detection`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T036` run

## Progress log

- 2026-10-21 00:00 · planner · created
