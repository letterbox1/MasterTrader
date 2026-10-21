---
id: P2-T032
kind: task
title: Heartbeats and dead-man watchdog
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T031]
requirements: [R2.18]
roadmap_todos: [T2.23]
modules: [M11, M17]
dashboards: [D06]
branch: p2/P2-T032-heartbeats-dead-man-watchdog
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/07-security-notes.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T032 · Heartbeats and dead-man watchdog

## Goal / expected outcome

Critical services (engine, monitor, risk, postgres probe, nats probe) publish `sys.heartbeat.{service}`; a watchdog cancels open orders (and flattens where configured) when any critical heartbeat is missing for N seconds — including when the engine itself is the one that died.

## Context & references

- Roadmap: [R2.18](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.23
- Architecture: [02 §6 dead-man rule](../../../docs/02-v1-architecture.md#6-messaging-nats) · [02 §9.3 Postgres down](../../../docs/02-v1-architecture.md#93-degraded-modes) · [07 §5 fail flat](../../../docs/07-security-notes.md#5-network--host)
- UI: [D06 Dead-man tile, countdown ±1 s](../../../docs/ui/dashboards/D06-risk.md)
- Related: P2-B002 (engine-death coverage), P2-B003 (N unspecified), P2-T054 drill.

## Requirements

- Heartbeat library `mt_obs.heartbeat` (1 s interval, payload: service, pid, seq, ts, health); KV `heartbeat.{service}` latest.
- In-engine watchdog: missing monitor/risk/postgres/nats heartbeat for N s (policy, proposed default 10 s; fast sleeves may set lower) → cancel-all (+ flatten if configured) via the kill path with `source=deadman`.
- Out-of-process watchdog (`deadman` sidecar in its own container, own trade-only keys scoped to cancel): engine heartbeat missing for N s → cancel all open orders directly via venue REST cancel-all endpoints; flatten only if policy allows.
- `risk.deadman.ack` (C1) clears the alert after recovery; trading stays halted until ack.
- D06 countdown data: last beat + threshold over WS `heartbeat` (server time included for ±1 s accuracy).

## ToDo

- [ ] Heartbeat library + adoption in engine, monitor, risk, probes for postgres/nats
- [ ] In-engine watchdog
- [ ] `deadman` sidecar service + minimal venue cancel clients (Binance testnet, Alpaca, OANDA, IG)
- [ ] Compose service + secrets scoping
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: watchdog timers and thresholds per service.
- Integration: stop monitor container → engine cancels all within N+1 s.
- Integration: `docker kill engine` → sidecar cancels testnet orders within N+2 s.

### Scenarios
- Given the engine process is killed with 10 open testnet orders, when N seconds pass, then the sidecar cancels them and alerts critical.
- Given Postgres stops, when N seconds pass, then dead-man fires (engine kept running with in-memory limits until then).

### Stress / failure injection
- Network partition between engine and NATS for 2×N s: both watchdogs act; no orders submitted after partition start + N.

## Acceptance criteria

- [ ] Heartbeats from all five critical services
- [ ] Engine death covered by the sidecar
- [ ] Countdown data accurate to ±1 s
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Sidecar itself down: engine monitors `sys.heartbeat.deadman` and alerts (does not halt).
- Clock skew between containers: use monotonic receive time in watchdog.

## Cardinal rules (do NOT)

- Do NOT give the sidecar any permission beyond cancel/read (and reduce-only close where flatten is enabled).
- Do NOT disable dead-man in paper mode.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.

## Doc sync on completion

- `docs/02-v1-architecture.md` §3.2/§6: add the `deadman` sidecar and N default (after P2-B002/B003).
- `docs/07-security-notes.md` §6: dead-man design.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.23 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T032-heartbeats-dead-man-watchdog`
- PR title: `P2-T032: Heartbeats and dead-man watchdog`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T032` run

## Progress log

- 2026-10-21 00:00 · planner · created
