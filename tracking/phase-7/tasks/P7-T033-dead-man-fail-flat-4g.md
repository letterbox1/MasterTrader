---
id: P7-T033
kind: task
title: Dead-man fail-flat configuration with UPS and 4G signals
phase: 7
type: OPS
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T009, P7-T030, P2-T032]
requirements: [R7.11]
roadmap_todos: [T7.41]
modules: [M11]
dashboards: [D06, D16]
tools: [git, docker, uv, nut]
mcp: []
env: []
services: [postgres, nats, UPS (NUT)]
branch: p7/P7-T033-dead-man-fail-flat-4g
pr: ""
doc_sync: [docs/07-security-notes.md, docs/ui/dashboards/D06-risk.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T033 · Dead-man fail-flat configuration with UPS and 4G signals

## Goal / expected outcome

The three-layer dead-man's switch (16 §3.1) is configured for live sub-accounts and wired to the UPS: the in-engine watchdog and the `deadman` sidecar cancel at 5 s and apply each bot's `on_system_failure` at 10 s; venue cancel-after timers (refresh 15 s, timeout 60 s) and resting stops cover a dead host or tunnel; UPS low battery triggers fail-flat before shutdown.

## Context & references

- Roadmap: [R7.11 · ToDo T7.41](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [16 §3.1](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch) (three layers, timings, `on_system_failure`, restart flat) · [07 §5](../../../docs/07-security-notes.md#5-network--host) (fail flat on link/power loss) · [07 §6](../../../docs/07-security-notes.md#6-application-controls) (dead-man's switch) · [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) (heartbeat rules) · [D06](../../../docs/ui/dashboards/D06-risk.md) (dead-man tile)
- Cross-phase: P2-T032 (`depends_on`: heartbeats + in-engine watchdog, layer 1); P2 R2.56/T2.36 (sidecar and venue timers, being split into new P2 tasks), P2-T054 (drills).
- Related: P7-T009 (hardware), P7-T030 (resting stops), P7-T052, P7-T053, gap P7-B015 (resolved: 16 §3.1 defaults)

## Requirements

- Timings (16 §3.1 defaults, settings): layers 1 (in-engine watchdog) and 2 (`deadman` sidecar): heartbeat missing 5 s → cancel open orders; 10 s → apply each bot's `on_system_failure`. Layer 3: venue cancel-after timers refreshed every 15 s with a 60 s timeout, plus resting venue stops (P7-T030).
- Per-bot `on_system_failure: flatten | cancel_orders_only | hold` (default `flatten`; `cancel_orders_only` keeps the position under its resting stop, useful for long-horizon holds; hold-and-earn exempt).
- Link failover: a broadband → 4G switch shows up as a short tunnel outage (P7-T066); feeds go stale and M11 rejects new orders inline; if the outage outlasts the 10 s feed threshold, bots apply `on_system_failure`. The measured failover time (P7-T009) is recorded next to these timings; changing a timing is your call (loosening C3), never automatic.
- Restart after an unplanned stop: the engine starts with every bot paused, reconciles, flattens/cancels residuals per policy and waits for your resume (C1) unless `auto_resume_after_crash: true` (16 §3.1).
- NUT (Network UPS Tools) on the host: `ONBATT` → alert warning; `LOWBATT` or runtime < 5 min → kill ON (reason `power`) with each bot's `on_system_failure`, then clean shutdown.
- All config versioned in the risk policy (tighten C1, loosen C3).

## ToDo

- [ ] NUT install/config in infra (pinned image or host package), event hooks → `kill.set` via NATS.
- [ ] Live values of the 16 §3.1 timings and per-bot `on_system_failure` in the policy (defaults, not code).
- [ ] Enable venue cancel-after timers (refresh 15 s / timeout 60 s) on every live venue that supports them (e.g. Kraken `CancelAllOrdersAfter`, OKX cancel-all-after; others as recorded in P7-T003).
- [ ] D06 dead-man tile shows the three layers' timings and the UPS state.
- [ ] Tests; docs.

## Verification

### Tests
- Integration: simulate `LOWBATT` via NUT dummy driver → kill ON within 1 s, cancels sent < 1 s (02 §9.2).
- Integration: stop the engine heartbeat → sidecar cancels within 5 s and applies `on_system_failure` at 10 s; block the tunnel for 70 s → venue cancel-after timers cancel open orders (testnet/sandbox), resting stops remain.

### Scenarios
- Given mains fails, then you get 'on battery' immediately and, at low battery, positions flatten before shutdown.
- Given broadband fails and the tunnel is back over 4G in 8 s, then no bot reaches its 10 s `on_system_failure` threshold, orders resume after recon, and the venues only ever saw the exit-node IP.

### Stress / failure injection
- Repeated failover flaps (5 in 10 min): `on_system_failure` applies only when an outage exceeds 10 s; alerts grouped; accounts reconfirmed by recon each time.

## Acceptance criteria

- [ ] 16 §3.1 timings configured for live, with the measured failover time recorded next to them.
- [ ] UPS events drive fail-flat.
- [ ] CI green.

## Exceptions & edge cases

- Both links or the tunnel down: host-side cancels can't reach the venue — resting stops and venue cancel-after timers (layer 3) cover it (16 §3.1–3.2).
- Host clock jumps after power loss: chrony resync before resuming.

## Cardinal rules (do NOT)

- Do NOT loosen any dead-man timing to avoid flattening without C3.
- Do NOT disable cancel-on-disconnect on live accounts.
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/07-security-notes.md` §5: UPS hooks and the measured failover time.
- `docs/ui/dashboards/D06-risk.md`: UPS state on the dead-man tile.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.41 when this item is done.

## Branch & PR

- Branch: `p7/P7-T033-dead-man-fail-flat-4g`
- PR title: `P7-T033: Dead-man fail-flat configuration with UPS and 4G signals`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T033` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (three-layer dead-man per 16 §3.1: 5 s cancel / 10 s on_system_failure, venue timers 15 s/60 s; dropped the invented 90 s N (P7-B015); restart flat/paused; dep P2-T032)
