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
branch: p2/P2-T054-verify-kill-deadman-drills
pr: ""
doc_sync: [docs/runbooks/kill-switch-drill.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T054 · Kill-switch and dead-man drills with timing

## Goal / expected outcome

Scripted drills on testnet/practice prove kill → all cancels sent < 1 s from web HALT and from Telegram `/kill` (including with mt-api down), and the dead-man fires when the engine, monitor or a DB heartbeat stops.

## Context & references

- Roadmap: [R2.18, R2.N1](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.61
- Flow: [02 F6](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · SLO: [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos) · [mob §4 /kill < 1 s](../../../docs/ui/mobile-and-telegram.md#4-acceptance-criteria)
- Related: P2-T064 (your phone drill), P2-T068 runbook.

## Requirements

- Setup: ≥ 50 resting orders across Binance testnet + OANDA practice + sandbox; 2 open positions with `flatten_on_kill` on one sleeve.
- Kill drill A (web HALT), B (Telegram `/kill` via mt_api), C (Telegram with mt-api stopped → NATS): measure KV ON → last cancel sent (< 1 s) and → last venue ack; verify no new order after ON; flatten done for the configured sleeve only.
- Dead-man drills: stop `engine` (sidecar cancels within N+2 s), stop `monitor` (engine cancels within N+1 s), stop `postgres` (engine continues in memory, dead-man fires after N s).
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
- Given the engine container is killed, when N seconds pass, then the sidecar cancels all testnet orders.

### Stress / failure injection
- Run kill drill A during a 1k intents/s burst: still < 1 s; zero post-ON submissions.

## Acceptance criteria

- [ ] All drill runs < 1 s (max) for cancels sent
- [ ] Dead-man acts within N(+2) s in every drill
- [ ] Report committed

## Exceptions & edge cases

- Venue ack latency is outside our control: SLO measured to 'cancel sent'; ack times reported separately.

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
