---
id: P7-T066
kind: task
title: Exit-node tunnel for broadband and 4G with the egress check on the static IP
phase: 7
type: OPS
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T065, P7-T009, P1-T071]
requirements: [R7.14, R7.11]
roadmap_todos: [T7.42]
modules: [M16, M12, M17]
dashboards: [D16, D06]
tools: [git, docker, tailscale, wireguard-tools, uv]
mcp: []
env: []
services: [tailscale, egress exit-node VM (P7-T065), monitor, nats]
branch: p7/P7-T066-exit-node-tunnel-for-broadband-and-4g-with-the-e
pr: ""
doc_sync: [docs/07-security-notes.md, docs/02-v1-architecture.md, docs/ui/dashboards/D16-system.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T066 · Exit-node tunnel for broadband and 4G with the egress check on the static IP

## Goal / expected outcome

All exchange traffic (engine, `deadman` sidecar, monitor reconciliation, `ib-gateway`) leaves through the Sydney exit node over a tunnel that works on both broadband and 4G, so the venues always see the one allow-listed static IP; if the tunnel is down, exchange traffic has **no** other route (no leak via the home IP), the system fails flat via venue timers + resting stops, and the egress check (P1-T071) is pointed at the static IP.

## Context & references

- Roadmap: [R7.14, R7.11 · ToDo T7.42](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Design: [16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys) (exit node, both links tunnel to it, tunnel down → fail-flat via layer 3, egress check every minute) · [16 §3.1](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch) (layer 3: venue cancel-after timers + resting stops) · [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) (which containers use the exit node) · [07 §5](../../../docs/07-security-notes.md#5-network--host) · [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) (egress mismatch → new orders blocked)
- Decision: [17 §A P7-B004](../../../docs/17-decisions-register.md#a-s2-items-all-resolved)
- Cross-phase: P1-T071 (egress IP/country check, `egress.status`), P1-T072 (egress fault test), P2 inline safety checks read `egress.status`.
- Related: P7-T065 (VM), P7-T009 (UPS + 4G router), P7-T033 (dead-man config), P7-T052 (failover drill, T7.64), P7-T047 (key audit)

## Requirements

- **Egress path as code** in `infra/egress/`: a dedicated `egress` network container (Tailscale exit-node client or WireGuard) that exchange-facing containers share (`network_mode: service:egress`); other containers keep the normal route. Image pinned by digest.
- **No leak:** inside the exchange network namespace the only default route is the tunnel; a firewall rule drops anything else. Tunnel down → connections fail (never fall back to the home/4G IP).
- **Both links:** the host reaches the exit node over broadband and over the 4G router (P7-T009); the tunnel re-establishes after a link switch without changing the egress IP. Reconnect target ≤ the venue cancel-after timeout (default 60 s, 16 §3.1); measure it.
- **Egress check:** set P1-T071's `expected_ips` to the exit node's static IP and `residency_country` to your configured residency (change = `system.settings.update`; loosening is C3, tightening C1). Mismatch or unreachable → new orders blocked + critical alert (P1-T071 behaviour).
- **Tunnel-down handling:** tunnel heartbeat published on `sys.heartbeat.egress`; down → critical alert on every channel; the engine treats venues as disconnected (accounts `unconfirmed`, P7-T026); protection relies on layer 3 (venue timers + resting stops).
- D16 Egress panel shows tunnel state, link in use (broadband/4G), observed IP vs expected, last check.
- Defaults (interval, reconnect thresholds) are configuration, linked to 16 §3.2; nothing hard-coded.

## ToDo

- [ ] `infra/egress/` compose service + config (pinned image, health check, `sys.heartbeat.egress` publisher).
- [ ] Attach `engine`, `deadman`, `monitor` (recon/venue calls) and `ib-gateway` to the egress namespace; leave LLM/agent/UI containers off it.
- [ ] Leak-proof firewall rules in the egress namespace (drop non-tunnel egress).
- [ ] Rehearse keyless first: a local two-container WireGuard pair (test profile only) proves routing, leak-proofing and reconnect; then apply to the real exit node from P7-T065.
- [ ] Point the P1-T071 egress check at the static IP (C3 change) and confirm `egress.status = ok`.
- [ ] D16 Egress panel: tunnel state + link in use.
- [ ] Tests (below); docs.

## Verification

### Tests
- Integration (local rehearsal, no keys): from the `engine` namespace `curl api.ipify.org` returns the test exit node's IP; with the tunnel stopped the request fails (no fallback route).
- Integration: stopping the tunnel publishes a missing `sys.heartbeat.egress` and a critical alert within one check interval; `egress.status` goes `unreachable`.
- Config test: only the listed exchange-facing services share the egress namespace (compose assertion).

### Scenarios
- Given broadband is up, when the engine calls a venue, then the venue sees the static exit-node IP.
- Given broadband fails and the 4G router takes over, when the tunnel re-establishes, then the egress IP is unchanged and `egress.status` returns to `ok`.
- Given the tunnel is down for longer than the venue cancel-after timeout, then open orders are cancelled by the venue timers, positions stay under their resting stops, and you get a critical alert on every channel.

### Stress / failure injection
- Flap the tunnel 10 times in 10 minutes: no request ever leaves via a non-tunnel IP (packet capture on the host's WAN shows only tunnel traffic for exchange hosts); alerts grouped; accounts return to `confirmed` only after a clean recon.

## Acceptance criteria

- [ ] All exchange traffic leaves via the static exit-node IP on broadband and on 4G.
- [ ] Tunnel down → no leak, critical alert, venue-side protection only.
- [ ] Egress check configured to the static IP and `ok`; D16 shows tunnel state.
- [ ] CI green (config tests, leak test in the rehearsal profile).

## Exceptions & edge cases

- Exit-node VM rebooting: tunnel down for the reboot; same handling as tunnel down; the static IP survives.
- Tailscale control plane unreachable: existing WireGuard sessions keep working; new sessions may fail → treated as tunnel down.
- MT5 route: the Windows VPS uses its own static IP for FP Markets (07 §5.1); it is not routed through this exit node.

## Cardinal rules (do NOT)

- Do NOT add a fallback route for exchange traffic outside the tunnel, and do NOT widen any key's IP allow-list to make failover "work".
- Do NOT route LLM, data-source or UI traffic through the exit node; only exchange traffic.
- Do NOT use a commercial VPN/proxy or a non-AU exit (12 §3).
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/07-security-notes.md` §3/§5: the egress namespace and which containers use it.
- `docs/02-v1-architecture.md` §3: the `egress` service in the container list.
- `docs/ui/dashboards/D16-system.md`: tunnel state on the Egress panel.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.42 when this item is done.

## Branch & PR

- Branch: `p7/P7-T066-exit-node-tunnel-for-broadband-and-4g-with-the-e`
- PR title: `P7-T066: Exit-node tunnel for broadband and 4G with the egress check on the static IP`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T066` run

## Progress log

- 2026-10-22 02:12 · cloud:vm:be04b6ae61f8 · created
- 2026-10-22 00:00 · aligner · created for docs/16–17 (R7.14/T7.42: exit-node tunnel on both links, no-leak routing, egress check on the static IP, 16 §3.1–3.2)
