---
id: P0-T012
kind: task
title: Order a UPS and a 4G failover router
phase: 0
type: USER
status: ready
priority: low
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R0.N2]
roadmap_todos: [T0.02]
modules: [ops]
dashboards: []
tools: [upsc]
mcp: []
env: []
services: []
branch: p0/P0-T012-ups-and-4g-failover
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T012 · Order a UPS and a 4G failover router

## Goal / expected outcome

A UPS covering the host and router, and a 4G failover router (or failover-capable router + SIM), are ordered and ideally installed; the UPS is USB-connected so the host sees battery state (NUT) for a clean shutdown. Needed before live (P7), cheap to set up early.

## Context & references

- [Roadmap P0 T0.02](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [07 §5 network & host](../../../docs/07-security-notes.md#5-network--host) (continuity, fail flat)
- Related: P0-T019 (NUT client)
- Unblocks: P7 continuity drills

## Requirements

- UPS: line-interactive or online, ≥ 15 min runtime at host + router load (log estimated W), USB HID for NUT.
- 4G failover: router with automatic WAN failover and a prepaid/data SIM; Tailscale must keep working over it.
- Policy reminder: on lost power/link the system fails **flat**: venue cancel-after timers and resting venue stops protect positions ([16 §3.1–3.2](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)); the three-layer dead-man arrives in P2.
- From P7, broadband and 4G both tunnel to one fixed-IP Sydney exit node, so the exchanges always see the allow-listed IP ([16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys)); the router must allow that WireGuard/Tailscale tunnel over 4G.

## ToDo

- [ ] Estimate load and pick a UPS; order it.
- [ ] Pick a failover router/SIM; order it.
- [ ] When delivered: connect, plug the UPS USB into the host, tell P0-T019 so NUT is configured.
- [ ] Pull the WAN cable once and confirm Tailscale reconnects over 4G; log the result.

## Verification

### Tests
- Confirmation: `upsc <ups>@localhost` shows battery charge once NUT is configured; WAN pull test logged.

### Scenarios
- Given mains power fails, when UPS runtime falls below the threshold, then NUT triggers a clean shutdown.

### Stress / failure injection
- WAN pull test (above).

## Acceptance criteria

- [ ] UPS and failover ordered (dates logged)
- [ ] Once installed: NUT sees the UPS; WAN failover test logged

## Exceptions & edge cases

- Delivery after P0 exit: may close at 'ordered' as long as it's installed before P7 (the exit demo treats it as non-blocking).

## Cardinal rules (do NOT)

- Do NOT send exchange traffic directly over the 4G link (its CGNAT IP isn't allow-listed): from P7 it always leaves via the fixed-IP Sydney exit node, which isn't location masking (12 §3, 16 §3.2).

## Doc sync on completion

- `docs/07-security-notes.md` §5: note the installed UPS/failover (no values).
- `docs/roadmap/phase-0-foundations.md`: tick T0.02 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T012-ups-and-4g-failover`
- PR title: `P0-T012: Order a UPS and a 4G failover router`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T012` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (fail-flat via venue timers + resting stops and fixed-IP exit node over 4G (16 §3.1–3.2) replaces the 'no VPN on failover' rule; run fields added)
