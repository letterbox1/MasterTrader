---
id: P2-T032
kind: task
title: Heartbeats and in-engine dead-man watchdog (layer 1)
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T031, P0-T018]
requirements: [R2.18, R2.56]
roadmap_todos: [T2.23]
modules: [M11, M17]
dashboards: [D06]
tools: [uv, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p2/P2-T032-heartbeats-dead-man-watchdog
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/16-configuration-and-safety-model.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T032 · Heartbeats and in-engine dead-man watchdog (layer 1)

## Goal / expected outcome

Critical services (engine, feeds/monitor, risk, postgres probe, nats probe) publish `sys.heartbeat.{service}` every 1 s, and the **in-engine watchdog** (dead-man layer 1 of three, [16 §3.1](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)) acts when a component goes missing: **5 s → cancel open orders for the affected bots; 10 s → apply each bot's `on_system_failure`** (default `flatten`). Engine death is covered by the external `deadman` sidecar (layer 2, P2-T072) and venue-side timers + resting stops (layer 3, P2-T073), which consume the heartbeat built here.

## Context & references

- Roadmap: [R2.18](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.23 (in-engine watchdog) · three-layer design [R2.56](../../../docs/roadmap/phase-2-strategies-risk-lab.md)
- Decisions: [17 §A P2-B002](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (three layers; per-bot `on_system_failure`, default `flatten`) · [17 §C P2-B003](../../../docs/17-decisions-register.md#c-defaults-that-were-n-or-unspecified) (dead-man 5 s / 10 s) · [16 §3.1](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)
- Architecture: [02 §6 dead-man layers](../../../docs/02-v1-architecture.md#6-messaging-nats) · [02 §9.3 degraded modes](../../../docs/02-v1-architecture.md#93-degraded-modes) · [07 §5 fail flat](../../../docs/07-security-notes.md#5-network--host)
- Cross-phase (`depends_on`): `mt_obs` metrics/logging library (P0-T018), where the heartbeat helper lives.
- UI: [D06 Dead-man tile, countdown ±1 s](../../../docs/ui/dashboards/D06-risk.md)
- Related: P2-T072 sidecar (layer 2), P2-T073 venue-side layer 3, P2-T074 restart flat with bots paused, P2-T054 drill, P2-T075 kill-the-engine drill.

## Requirements

- Heartbeat library `mt_obs.heartbeat` (1 s interval, payload: service, pid, seq, ts, health); KV `heartbeat.{service}` latest. Adopted by engine, monitor (feeds), risk, and probes for postgres/nats.
- In-engine watchdog (layer 1): a watched component missing **5 s** → cancel open orders for the affected bots; missing **10 s** → apply each affected bot's **`on_system_failure`** (`flatten` default: close at market reduce-only; `cancel_orders_only`: keep the position under its resting venue stop; `hold`; hold-and-earn exempt). Timers are L1 defaults ([16 §3.1](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)), editable; loosening them is C3.
- Actions go through the kill/cancel path with `source=deadman` and are WORM-audited.
- The engine's own heartbeat (`sys.heartbeat.engine`) is published for the `deadman` sidecar (P2-T072) and the UI; the engine also watches `sys.heartbeat.deadman` and alerts if the sidecar is missing (does not halt).
- `risk.deadman.ack` (C1) clears the alert after recovery; affected bots stay paused until you resume them (C1).
- D06 countdown data: last beat + thresholds over WS `heartbeat` (server time included for ±1 s accuracy).

## ToDo

- [ ] Heartbeat library + adoption in engine, monitor, risk, probes for postgres/nats
- [ ] In-engine watchdog with 5 s cancel / 10 s `on_system_failure` stages (thresholds from policy)
- [ ] Per-bot `on_system_failure` setting read from the L4 layer (default `flatten`)
- [ ] `risk.deadman.ack` command + WS `heartbeat` topic fields for D06
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: watchdog timers per service; 5 s → cancel only; 10 s → `on_system_failure` per bot (`flatten`, `cancel_orders_only`, `hold` each covered).
- Integration (sandbox venue, no keys): stop the monitor container → affected bots' orders cancelled within 5 s + 1 s; positions flattened at 10 s + 1 s for `flatten` bots.
- Unit: hold-and-earn positions never flattened.

### Scenarios
- Given Postgres stops, when 5 s pass, then the affected bots' open orders are cancelled; at 10 s their `on_system_failure` runs (the engine kept running with in-memory limits until then).
- Given a bot with `on_system_failure: cancel_orders_only`, when the feed heartbeat is missing 10 s, then its orders are cancelled and its position stays protected by the resting venue stop.

### Stress / failure injection
- Network partition between engine and NATS for 20 s: layer 1 acts on its own; no orders submitted after partition start + 5 s.
- Flap a heartbeat every 4 s for 5 min: no false trigger (threshold 5 s), counter metrics recorded.

## Acceptance criteria

- [ ] Heartbeats from all five critical services
- [ ] Layer 1 acts at 5 s (cancel) and 10 s (`on_system_failure` per bot) with defaults from policy
- [ ] Countdown data accurate to ±1 s
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Sidecar itself down: engine alerts on the missing `sys.heartbeat.deadman` (does not halt).
- Clock skew between containers: use monotonic receive time in the watchdog.
- Whole host or internet down: nothing on our side can act; only layer 3 (venue timers + resting stops, P2-T073) protects (16 §3.1).

## Cardinal rules (do NOT)

- Do NOT disable the dead-man in paper mode.
- Do NOT hard-code the 5 s / 10 s timers; they are policy defaults.
- Do NOT make protective exits wait for any approval.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.

## Doc sync on completion

- `docs/02-v1-architecture.md` §6: layer-1 watchdog subjects and timers as built.
- `docs/16-configuration-and-safety-model.md` §3.1: confirm the layer-1 defaults as built (no value change).
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.23 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T032-heartbeats-dead-man-watchdog`
- PR title: `P2-T032: Heartbeats and in-engine dead-man watchdog (layer 1)`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T032` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (reworked to dead-man layer 1 only (5 s cancel / 10 s on_system_failure per bot); sidecar moved to P2-T072, venue layer to P2-T073)
