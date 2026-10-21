---
id: P2-T020
kind: task
title: mt_api risk, venue and order command surface
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T017, P2-T019]
requirements: [R2.10, R2.11, R2.16]
roadmap_todos: [T2.22, T2.24]
modules: [M11, M12]
dashboards: [D06, D05]
branch: p2/P2-T020-mt-api-risk-order-surface
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T020 · mt_api risk, venue and order command surface

## Goal / expected outcome

`mt_api` exposes the risk queries, risk/venue commands, order/position commands (all routed as `OrderIntent`s through M11) and WebSocket topics that D06, D05 (Part B UI), D01 and Telegram use.

## Context & references

- Roadmap: [R2.10, R2.11, R2.16](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDos T2.22, T2.24
- API: [02 §7.1 queries](../../../docs/02-v1-architecture.md#7-api-contract-mt_api) · [02 §7.2 commands](../../../docs/02-v1-architecture.md#72-commands-rest-write) · WS topics in 02 §7.3
- UI: [D06 backend contract](../../../docs/ui/dashboards/D06-risk.md) · [D05 manual ticket = manual sleeve](../../../docs/ui/dashboards/D05-execution.md)
- Cross-phase: mt_api command bus, idempotency, audit, WS hub (P0 T0.24).

## Requirements

- Queries: `/risk/policy`, `/risk/state` (+`breakdown`, `ladder`), `/risk/events`, `/risk/changes`, `/venues/registry`, `/positions`, `/orders`, `/fills`; `POST /risk/preview`.
- Commands: `risk.policy.update`, `risk.kill.on|off`, `risk.deadman.ack`, `risk.ladder.set`, `risk.sleeve.resume`, `venue.registry.update`; `order.place|modify|cancel|cancel_all`, `position.close|reduce|set_brackets`, and **flatten-and-halt** (`position.close` with `halt=true`, required `reason`).
- Order commands publish `ord.intent.manual` (sleeve `manual` unless a strategy scope is given) → engine → M11; response returns the risk decision; C2 server-side.
- WS topics: `risk.state`, `risk.event`, `kill`, `heartbeat`, `orders`, `fills`, `positions` with `{topic, seq, ts, data}` envelope and throttling (≤ 1 Hz tables).
- Telegram uses a scoped token with only the commands it needs.

## ToDo

- [ ] Routers under `packages/mt_api/routers/risk.py`, `orders.py`, `venues.py`
- [ ] Command handlers delegating to `mt_risk` / NATS
- [ ] WS topic publishers
- [ ] OpenAPI + typed client regen for the web app
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- API tests for every endpoint (auth, levels, problem+json).
- Integration: `order.place` produces exactly one `ord.intent.manual` and one decision; with M11 reject the response carries reasons.
- Unit: flatten-and-halt without `reason` → 422.

### Scenarios
- Given a manual BUY above the manual sleeve max position, when placed from D05, then 200 with decision `reject` + reason, and no venue order.
- Given kill is ON, when `risk.kill.off` is sent without C3, then it stays pending.

### Stress / failure injection
- 100 concurrent `order.place` with the same idempotency key → one intent only.

## Acceptance criteria

- [ ] All listed endpoints/commands/topics live in OpenAPI
- [ ] No order command reaches a venue without an M11 decision
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Engine unreachable: order commands return 503; kill still works via NATS (P2-T031/T035).

## Cardinal rules (do NOT)

- Do NOT call venue APIs from mt_api.
- Do NOT expose withdrawals or key management.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7: mark endpoints as implemented; add `risk.sleeve.resume` if kept.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.22, T2.24 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T020-mt-api-risk-order-surface`
- PR title: `P2-T020: mt_api risk, venue and order command surface`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T020` run

## Progress log

- 2026-10-21 00:00 · planner · created
