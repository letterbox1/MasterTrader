---
id: P2-T054
kind: task
title: Kill-switch and dead-man drills with timing
phase: 2
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T031, P2-T032, P2-T035, P2-T023]
requirements: [R2.18, R2.N1]
roadmap_todos: [T2.61]
modules: [M11, M12]
dashboards: [D06]
tools: [uv, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p2/P2-T054-verify-kill-deadman-drills
pr: ""
doc_sync: [docs/runbooks/kill-switch-drill.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T054 · Kill-switch and dead-man drills with timing

## Goal / expected outcome

Scripted drills on the sandbox venue and mock venues (no keys) prove kill → all cancels sent < 1 s from web HALT and from Telegram `/kill` (fake Bot API, including with mt-api down), and the in-engine dead-man (layer 1) fires when the monitor or a DB heartbeat stops. Engine death (layer 2 sidecar) is the kill-the-engine drill P2-T075; the drill on testnet/practice with your keys is part of P2-T071; your phone drill is P2-T064.

## Context & references

- Roadmap: [R2.18, R2.N1](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.61
- Flow: [02 F6](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · SLO: [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos) · [mob §4 /kill < 1 s](../../../docs/ui/mobile-and-telegram.md#4-acceptance-criteria)
- Defaults: dead-man layer 1 cancels at 5 s and applies `on_system_failure` at 10 s ([16 §3.1](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)).
- Related: P2-T064 (your phone drill), P2-T068 runbook, P2-T075 (kill-the-engine drill), P2-T071 (testnet drill with your keys).

## Requirements

- Setup: ≥ 50 resting orders across the sandbox venue and mock Binance/OANDA venues; open positions on bots with `on_system_failure` = `flatten`, `cancel_orders_only` and `hold`.
- Kill drill A (web HALT), B (Telegram `/kill` via mt_api), C (Telegram with mt-api stopped → NATS `kill.set`): measure KV ON → last cancel sent (< 1 s) and → last venue ack; verify no new order after ON; each bot's `on_system_failure` applied; the WORM kill event has the right source (`web`/`telegram`).
- Layer-1 dead-man drills: stop `monitor` (affected bots' orders cancelled within 5 s + 1 s, `on_system_failure` at 10 s + 1 s), stop `postgres` (engine continues in memory, layer 1 fires after 5 s / 10 s).
- Turn-off check: kill OFF requires C3 and cause cleared.

## ToDo

- [ ] Drill script `ops/drills/kill_drill.py` (seeds orders, triggers, measures from `mt_kill_to_cancels_seconds` + audit timestamps)
- [ ] Dead-man drill script
- [ ] Run each drill 5×, record p50/max
- [ ] Store drill report in `docs/runbooks/drill-reports/`
- [ ] Record results (numbers, run IDs, screenshots) in the progress log and tick the roadmap ToDo box

## Verification

### Tests
- Drills A, B, C × 5 runs; dead-man drills × 3 runs.

### Scenarios
- Given mt-api is stopped, when `/kill` is confirmed on Telegram, then the engine halts and all cancels are sent < 1 s.
- Given the monitor container is stopped, when 5 s pass, then the affected bots' orders are cancelled; at 10 s `flatten` bots are flat and `cancel_orders_only` bots keep their position with a resting stop.

### Stress / failure injection
- Run kill drill A during a 1k intents/s burst: still < 1 s; zero post-ON submissions.

## Acceptance criteria

- [ ] All drill runs < 1 s (max) for cancels sent
- [ ] Layer-1 dead-man acts within 5 s (+1 s) for cancels and 10 s (+1 s) for `on_system_failure` in every drill
- [ ] Report committed

## Exceptions & edge cases

- Venue ack latency is outside our control: SLO measured to 'cancel sent'; ack times reported separately.
- Postgres-stop drill: expected outcome follows 16 §3.1 until gap P2-B015 settles the 02 §9.3 wording; the drill records both the buffer behaviour and the layer-1 action.

## Cardinal rules (do NOT)

- Do NOT run drills against live accounts.
- Do NOT relax the 1 s target; investigate and fix.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.

## Doc sync on completion

- `docs/runbooks/kill-switch-drill.md`: add measured numbers (file created by P2-T068).
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.61 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T054-verify-kill-deadman-drills`
- PR title: `P2-T054: Kill-switch and dead-man drills with timing`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T054` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keyless drills (sandbox/mock venues, fake Bot API), layer-1 timers 5 s/10 s with per-bot on_system_failure; engine-death drill moved to P2-T075)
