---
id: P2-T075
kind: task
title: "Kill-the-engine drill: sidecar cancels in 5 s, flattens in 10 s, restart flat with bots paused"
phase: 2
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T072, P2-T073, P2-T074, P2-T054]
requirements: [R2.56, R2.18]
roadmap_todos: [T2.70]
modules: [M11, M12]
dashboards: [D06]
tools: [uv, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p2/P2-T075-verify-kill-the-engine-drill
pr: ""
doc_sync: [docs/runbooks/kill-switch-drill.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T075 · Kill-the-engine drill: sidecar cancels in 5 s, flattens in 10 s, restart flat with bots paused

## Goal / expected outcome

A scripted drill SIGKILLs the engine while paper positions and orders are open on the venue emulator and proves all three dead-man layers: the `deadman` sidecar cancels everything in ≤ 5 s and flattens per `on_system_failure` in ≤ 10 s; with the sidecar also down, venue timers cancel and resting stops remain; the restart starts flat with bots paused until resumed.

## Context & references

- Roadmap: [R2.56](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.70
- Decisions: [16 §3.1](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch) · [17 §A P2-B002](../../../docs/17-decisions-register.md#a-s2-items-all-resolved)
- Inputs: P2-T072 (sidecar), P2-T073 (venue timers, resting stops), P2-T074 (restart flat), P2-T054 (kill/layer-1 drill harness). The same drill runs once per real venue with your keys in P2-T071.
- Keyless: paper accounts on an external venue emulator container (the in-engine sandbox venue dies with the engine, so it can't show layer 2).

## Requirements

- Setup: 3 bots on the emulator (`flatten`, `cancel_orders_only`, `hold`), each with an open position (resting stop at the emulator) and 5 resting orders.
- Drill A: `docker kill -s KILL engine` → measure engine-heartbeat loss → sidecar cancels (≤ 5 s + 1 s) → `flatten` bot flat (≤ 10 s + 1 s); others per policy.
- Drill B: kill engine **and** sidecar, and block the host from the emulator → emulator countdown cancels resting orders after the timeout; resting stops remain and fire on a simulated price move.
- Restart: engine boots with all bots paused, reconciles, residue handled per policy, summary sent; resume one bot (C1) and confirm only it trades.
- Each drill run 3×; p50/max recorded; WORM rows for every action.

## ToDo

- [ ] Drill script `ops/drills/kill_engine_drill.py` (emulator setup, kill, measure, restart, resume)
- [ ] Run drills A and B 3× each; record timings and audit IDs
- [ ] Add results to `docs/runbooks/kill-switch-drill.md`
- [ ] Record results (numbers, run IDs) in the progress log and tick the roadmap ToDo box

## Verification

### Tests
- Drills A and B × 3 runs with timings; restart flow assertions.

### Scenarios
- Given the engine is SIGKILLed with 15 open orders, when 5 s pass, then the sidecar has cancelled all of them; at 10 s the `flatten` bot is flat.
- Given engine and sidecar are both down and the host is cut off, when the emulator's timer expires, then resting orders are cancelled and positions keep their stops.
- Given the engine restarts after drill A, then every bot is paused and trading resumes only for the bot you resume.

### Stress / failure injection
- Run drill A while the lab runs a sweep and 1k intents/s are flowing: timings still within 5 s / 10 s (+1 s).

## Acceptance criteria

- [ ] Sidecar cancels ≤ 5 s (+1 s) and flattens ≤ 10 s (+1 s) in every run
- [ ] Layer 3 (timers + resting stops) shown with engine and sidecar down
- [ ] Restart flat with bots paused in every run

## Exceptions & edge cases

- Emulator behaviour differs from a real venue: the per-venue live drill in P2-T071 is the confirmation; differences filed as bugs.

## Cardinal rules (do NOT)

- Do NOT run the drill against live accounts.
- Do NOT relax the 5 s / 10 s targets to pass; investigate and fix.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file outside the repo (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows (15 §2).
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/runbooks/kill-switch-drill.md`: kill-the-engine section with measured numbers (file created by P2-T068).
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.70 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T075-verify-kill-the-engine-drill`
- PR title: `P2-T075: Kill-the-engine drill: sidecar cancels in 5 s, flattens in 10 s, restart flat with bots paused`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T075` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (T2.70: R2.56, R2.18)
