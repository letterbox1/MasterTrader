---
id: P8-T032
kind: task
title: Resource subscriptions (fills, approvals, alerts) and optional legacy HTTP+SSE endpoint
phase: 8
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T003, P8-T006, P8-T007, P0-T036]
requirements: [R8.08, R8.03]
roadmap_todos: [T8.24]
modules: [M20]
dashboards: [D17]
tools: [uv, docker, git]
mcp: []
env: []
services: [postgres, nats]
branch: p8/P8-T032-resource-subscriptions-fills-approvals-alerts-an
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/ui/dashboards/D17-mcp-console.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P8-T032 · Resource subscriptions (fills, approvals, alerts) and optional legacy HTTP+SSE endpoint

## Goal / expected outcome

MCP clients can subscribe to server notifications for **fills, approvals and alerts** through MCP resource subscriptions (`resources/subscribe` → `notifications/resources/updated`), fed from the existing `mt_api` WebSocket topics, guarded like every MCP response and audited. Older clients can use an **optional legacy HTTP+SSE endpoint** (off by default) that serves the same tools and resources. Tested with the SDK client and fixtures; no keys.

## Context & references

- Roadmap: [R8.08](../../../docs/roadmap/phase-8-mcp.md#3-requirements) ("optional legacy HTTP+SSE endpoint; server notifications via resource subscriptions") · ToDo [T8.24](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Decisions: [17 §A P8-B004](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (transport + "server notifications via resource subscriptions (fills, approvals, alerts)") · [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) (256 KB cap, scopes)
- Spec: [03 M20](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7.3 WebSocket topics](../../../docs/02-v1-architecture.md#73-real-time-websocket-apiv1ws) (`orders`, `risk.event`, `alert`, `system`) · [02 §7.4](../../../docs/02-v1-architecture.md#74-telegram--mcp)
- Cross-phase (depends_on): P0-T036 (WebSocket hub with seq gap detection).
- Related: P8-T003 (transports), P8-T006 (guard applies to notifications), P8-T007 (audit), P8-T030 (byte cap).

## Requirements

- Resources (read-only, scope `read`): `mt://fills/recent`, `mt://approvals/pending?source=mcp`, `mt://alerts/recent`. Listed in `resources/list`; readable with `resources/read` (guarded, capped).
- Subscriptions: `resources/subscribe` / `unsubscribe` per session; `mt_mcp` keeps one WS connection to `mt_api` per session with the caller's token and turns `orders`/fill events, approval state changes and `alert.*` events into `notifications/resources/updated` (the client then reads the resource). Payloads pass the response guard (no Telegram text, PII redacted) because the read goes through `mt_api`.
- Notification delivery uses the Streamable HTTP SSE stream (resumable via `Last-Event-ID`, P8-T003) or stdio; WS seq gaps trigger a REST re-sync, never invented events.
- Subscribing is a read: it's logged in `audit.mcp_call`; each resource read after a notification is a normal audited read under the read limit.
- Legacy HTTP+SSE (2024-11-05 MCP transport): a separate path behind Caddy (e.g. `/mcp/sse` + `/mcp/messages`), **disabled by default** (setting `mcp.legacy_sse.enabled`; enabling it is C1 in D17 Policy), same auth, `Origin` check, registry, guard, limits and audit as Streamable HTTP. When disabled it returns 404.
- No subscription can carry anything from the never-exposed list (e.g. no key, token or `approval.*` resource).

## ToDo

- [ ] Implement the resource handlers and subscription manager in `mt_mcp` (thin: WS → notification mapping only; no filtering logic, which stays in `mt_api`).
- [ ] Ensure `mt_api` WS and the resource reads apply `McpResponseGuard` and the cap for `source = mcp`.
- [ ] Implement the legacy HTTP+SSE transport behind a setting; Caddy route template (disabled by default).
- [ ] Tests; update docs.

## Verification

### Tests
- Integration: subscribe to fills → place + approve a sandbox paper order → one `resources/updated` notification → `resources/read` shows the fill; unsubscribe stops notifications.
- Integration: an approval expiring after 5 min (injected clock) → notification on `mt://approvals/pending`.
- Integration: an alert built from a Telegram posture → notification + read show posture numbers only, never text.
- Integration: WS gap injected → REST re-sync, no duplicated or invented notifications.
- Integration: legacy SSE disabled → 404; enabled → `tools/list` + a read tool + a subscription work; bad `Origin` refused.

### Scenarios
- Given you approved an MCP order on Telegram, when the fill arrives, then Claude is notified without polling.
- Given a revoked token, then its subscription stream closes within 1 s.

### Stress / failure injection
- 50 sessions × 3 subscriptions with 100 fills/s for 5 min → notification lag p95 < 1 s; memory bounded.
- `mt_api` restart → sessions re-subscribe after reconnect; no missed state (re-read on reconnect).

## Acceptance criteria

- [ ] Fills, approvals and alerts available as subscribable resources; notifications delivered over Streamable HTTP and stdio
- [ ] Notification content passes the response guard and the byte cap; every subscribe/read audited
- [ ] Optional legacy HTTP+SSE endpoint works when enabled and is off by default
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Client doesn't support subscriptions: it polls the read tools; nothing breaks.
- Too many subscriptions per session: refuse above a settings limit with a clear error.
- WS down: notifications pause; the client sees a `degraded` status in `resources/read`.

## Cardinal rules (do NOT)

- Do NOT put filtering or business logic into `mt_mcp`; the guard, limits and audit stay in `mt_api`.
- Do NOT push raw event payloads that bypass the guard.
- Do NOT enable the legacy endpoint by default or with weaker auth.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set; Claude via MCP counts as a model input (12 §4–5).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7.4 and `docs/03-build-spec.md` M20: resource URIs and legacy path as built.
- `docs/ui/dashboards/D17-mcp-console.md`: Connection shows the legacy endpoint state; subscriptions in Session activity.
- `docs/roadmap/phase-8-mcp.md`: progress on T8.24.

## Branch & PR

- Branch: `p8/P8-T032-resource-subscriptions-fills-approvals-alerts-an`
- PR title: `P8-T032: Resource subscriptions (fills, approvals, alerts) and optional legacy HTTP+SSE endpoint`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T032` run

## Progress log

- 2026-10-22 00:00 · aligner · created for R8.08 / T8.24 (resource subscriptions for fills, approvals, alerts and the optional legacy HTTP+SSE endpoint, per 17 §A P8-B004)
