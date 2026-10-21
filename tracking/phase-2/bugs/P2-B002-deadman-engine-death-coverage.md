---
id: P2-B002
kind: gap
title: Dead-man watchdog lives in the engine, so engine death is not covered
phase: 2
type: DOC
status: backlog
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
branch: p2/P2-B002-deadman-engine-death-coverage
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/07-security-notes.md]
doc_sync_status: n/a
found_in: docs/02-v1-architecture.md §6 rules; docs/03-build-spec.md M11
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- [ ] Decide the rule with the user (or record the decision taken in the linked task)
- [ ] Update the source doc(s) so they agree
- [ ] Update the affected task file(s) to match

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- Given `docker kill engine` with open testnet orders, when N seconds pass, then the sidecar cancels them.

### Stress / failure injection
- n/a: documentation/specification gap

## Acceptance criteria

- [ ] Docs agree in one place, cross-linked from the others
- [ ] Affected tasks reference the decision

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
