---
id: P2-B002
kind: gap
title: Dead-man watchdog lives in the engine, so engine death is not covered
phase: 2
type: DOC
status: done
priority: high
size: XS
severity: S2
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.18]
roadmap_todos: []
modules: [M11]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B002-deadman-engine-death-coverage
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/07-security-notes.md]
doc_sync_status: done
found_in: docs/02-v1-architecture.md §6 rules; docs/03-build-spec.md M11
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B002 · Dead-man watchdog lives in the engine, so engine death is not covered

## Goal / expected outcome

The dead-man design covers a dead or hung engine (the most important case) with an independent process that can cancel venue orders.

## Context & references

- [02 §6 dead-man rule](../../../docs/02-v1-architecture.md#6-messaging-nats) · [03 M11](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) · [07 §5 fail flat](../../../docs/07-security-notes.md#5-network--host)
- Affects P2-T032, P2-T044, P2-T054.

## Requirements

- **Steps to reproduce:** 02 §6: 'the engine's watchdog consumes sys.heartbeat.* … missing critical heartbeat (engine, …) triggers cancel-all'. If the engine process dies, its own watchdog dies with it.
- **Expected:** An out-of-process watchdog with cancel-only venue access acts when the engine heartbeat stops.
- **Actual:** No component is specified to act on a missing engine heartbeat; only broker-side resting stops remain.
- **Suggested fix:** Add a small `deadman` sidecar container (own cancel-capable trade-only keys, no other permissions) that cancels via venue REST cancel-all endpoints; engine keeps its in-process watchdog for the other services. Planned in P2-T032/P2-T044.
- **Impact:** S2: open orders could keep working after an engine crash; R2.18 drill can't pass as specified.

## ToDo

- [x] Decision recorded: in-engine watchdog + external `deadman` sidecar with its own keys/connections + venue cancel-after timers and resting stops; per-bot `on_system_failure` (default `flatten`); restart flat with bots paused
- [x] Docs agree: 16 §3.1, 02 §3.2/§6/F6/§9.3, 03 M11, 07 §3
- [x] Tasks updated/created: P2-T032, P2-T072, P2-T073, P2-T074, P2-T075

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- Given `docker kill engine` with open testnet orders, when N seconds pass, then the sidecar cancels them.

### Stress / failure injection
- n/a: documentation/specification gap

## Acceptance criteria

- [x] Docs agree in one place, cross-linked from the others (16 §3.1 (three-layer dead-man); 02 §3.2 `deadman` container, §6 dead-man layers, F6, §9.3 engine-down row; 03 M11 dead-man; 07 §3 deadman keys)
- [x] Affected tasks reference the decision (P2-T032 (layer 1), P2-T072 (sidecar), P2-T073 (venue timers + resting stops), P2-T074 (restart flat), P2-T075 (drill))

## Exceptions & edge cases

- Until resolved, the affected task implements the conservative option stated under Suggested fix.

## Cardinal rules (do NOT)

- Do NOT close without the doc fix merged and the dependent task(s) updated to match.
- Do NOT "fix" by silently picking a number in code; the decision is recorded in the doc and in the risk policy (user input).
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/02-v1-architecture.md` §3.2/§6, `docs/03-build-spec.md` M11, `docs/07-security-notes.md` §6: add the sidecar.

## Branch & PR

- Branch: `p2/P2-B002-deadman-engine-death-coverage`
- PR title: `P2-B002: specify an out-of-process dead-man watchdog`

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (resolved by 17 §A P2-B002; docs carry it (16 §3.1 (three-layer dead-man); 02 §3.2 `deadman` container, §6 dead-man layers, F6, §9.3 engine-down row; 03 M11 dead-man; 07 §3 deadman keys); implementation owned by P2-T032 (layer 1), P2-T072 (sidecar), P2-T073 (venue timers + resting stops), P2-T074 (restart flat), P2-T075 (drill))
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §A P2-B002); docs updated: 16 §3.1 (three-layer dead-man); 02 §3.2 `deadman` container, §6 dead-man layers, F6, §9.3 engine-down row; 03 M11 dead-man; 07 §3 deadman keys; implementation owned by P2-T032 (layer 1), P2-T072 (sidecar), P2-T073 (venue timers + resting stops), P2-T074 (restart flat), P2-T075 (drill)
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
