---
id: P7-T052
kind: task
title: Failover drill: 4G through the tunnel keeps the egress IP; tunnel down fails flat
phase: 7
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T033, P7-T066]
requirements: [R7.14, R7.11]
roadmap_todos: [T7.64, T7.41]
modules: [M11, M12]
dashboards: [D06, D16]
tools: [git, uv, docker, nut]
mcp: []
env: []
services: [postgres, nats, tailscale, egress exit-node VM, 4G router, venue testnet with cancel-after timers]
branch: p7/P7-T052-verify-fail-flat-and-failover
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T052 · Failover drill: 4G through the tunnel keeps the egress IP; tunnel down fails flat

## Goal / expected outcome

A scripted drill with paper/testnet positions proves (T7.64): cutting broadband moves traffic to 4G **through the tunnel with the same egress IP**; cutting the tunnel lets the venue cancel-after timers cancel open orders while resting stops remain; dead-man layers 1–2 act at 5 s / 10 s; UPS low battery fails flat before shutdown.

## Context & references

- Roadmap: [R7.14, R7.11 · ToDo T7.64, T7.41](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [16 §3.1](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch) · [16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys) · [07 §5](../../../docs/07-security-notes.md#5-network--host) · Roadmap R7.14 'Verified by: failover drill' and R7.11 'pull-the-plug drill' (this is the automated precursor)
- Related: P7-T033, P7-T030, P7-T009, P7-T066 (tunnel), P7-T053

## Requirements

- Cases: (1) broadband cut → 4G takes over, the tunnel re-establishes, `egress.status` returns `ok` with the same IP and venue calls succeed; (2) tunnel cut for longer than the venue timeout (default 60 s) → venue cancel-after timers cancel open orders, resting stops remain, critical alert, no request leaves outside the tunnel; (3) engine heartbeat stopped → sidecar cancels ≤ 5 s, `on_system_failure` at 10 s; (4) NUT `LOWBATT` → kill + `on_system_failure`, then clean shutdown. Timings are read from the policy (16 §3.1 defaults).
- After each: recon clean; resting stops present for remaining positions; timings recorded.

## ToDo

- [ ] Script `tools/drills/failover_drill.sh` (router WAN switch or interface down for broadband, tunnel stop, engine heartbeat stop, NUT dummy driver).
- [ ] Run on the host with paper/testnet positions on a venue with cancel-after timers.
- [ ] Attach results.

## Verification

### Tests
- The script asserts each case's outcome via `mt_api` queries and venue REST.

### Scenarios
- Given the tunnel is down for 90 s, then the venue's timer has cancelled open orders by ~60 s, positions sit under resting stops, and after reconnection recon shows the cancels and the accounts return to `confirmed`.

### Stress / failure injection
- The drill is the fault injection; repeat case 2 three times and case 1 with an open order.

## Acceptance criteria

- [ ] All four cases pass and are recorded.

## Exceptions & edge cases

- Script must restore networking on exit (trap).

## Cardinal rules (do NOT)

- Do NOT run this with live positions.
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/07-security-notes.md` §5: measured results.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.64, T7.41 when this item is done.

## Branch & PR

- Branch: `p7/P7-T052-verify-fail-flat-and-failover`
- PR title: `P7-T052: Failover drill: 4G through the tunnel keeps the egress IP; tunnel down fails flat`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T052` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (re-scoped to the T7.64 failover drill per 16 §3.1–3.2: same egress IP on 4G, tunnel down → venue timers + resting stops; dropped the invented N)
