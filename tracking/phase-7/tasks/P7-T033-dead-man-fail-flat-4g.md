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
depends_on: [P7-T009, P7-T030]
requirements: [R7.11]
roadmap_todos: [T7.41]
modules: [M11]
dashboards: [D06, D16]
branch: p7/P7-T033-dead-man-fail-flat-4g
pr: ""
doc_sync: [docs/07-security-notes.md, docs/ui/dashboards/D06-risk.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T033 · Dead-man fail-flat configuration with UPS and 4G signals

## Goal / expected outcome

The dead-man's switch and UPS events are configured for live: missing heartbeats beyond the threshold cancel all orders and flatten configured strategies; UPS low battery triggers fail-flat before shutdown; the thresholds tolerate a normal 4G failover.

## Context & references

- Roadmap: [R7.11 · ToDo T7.41](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [07 §5](../../../docs/07-security-notes.md#5-network--host) (fail flat on link/power loss) · [07 §6](../../../docs/07-security-notes.md#6-application-controls) (dead-man's switch) · [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) (heartbeat rules) · [D06](../../../docs/ui/dashboards/D06-risk.md) (dead-man tile)
- Cross-phase: P2 T2.23 (dead-man watchdog), P2 T2.61 (drill).
- Related: P7-T009 (hardware), P7-T030 (resting stops), P7-T052, P7-T053, gap P7-B015 (N unspecified)

## Requirements

- Heartbeat threshold N = failover time measured in P7-T009 + 30 s (default 90 s) for venue-connectivity heartbeats; internal heartbeats (engine, risk, postgres, nats) keep the P2 value.
- Per-strategy `fail_flat: flatten|cancel_only` (default `flatten` for intraday, `cancel_only` for swing/position with resting stops).
- NUT (Network UPS Tools) on the host: `ONBATT` → alert warning; `LOWBATT` or runtime < 5 min → kill ON (reason `power`) with fail-flat actions, then clean shutdown.
- Venue-side cancel-on-disconnect (dead-man endpoints) enabled where offered (e.g. venue 'cancel all after' timers) with timeout = N.
- All config versioned in the risk policy (tighten C1, loosen C3).

## ToDo

- [ ] NUT install/config in infra (pinned image or host package), event hooks → `kill.set` via NATS.
- [ ] Dead-man thresholds per heartbeat class in policy.
- [ ] Venue cancel-after timers in adapters that support them.
- [ ] D06 dead-man tile shows per-class thresholds and the UPS state.
- [ ] Tests; docs.

## Verification

### Tests
- Integration: simulate `LOWBATT` via NUT dummy driver → kill ON within 1 s, cancels sent < 1 s (02 §9.2).
- Integration: block egress for 60 s (simulated failover) → no fail-flat; block for 120 s → fail-flat fires.

### Scenarios
- Given mains fails, then you get 'on battery' immediately and, at low battery, positions flatten before shutdown.
- Given 4G takes over in 40 s, then trading continues without flattening.

### Stress / failure injection
- Repeated failover flaps (5 in 10 min): no flatten unless one exceeds N; alerts grouped.

## Acceptance criteria

- [ ] Thresholds configured relative to measured failover time.
- [ ] UPS events drive fail-flat.
- [ ] CI green.

## Exceptions & edge cases

- Both links down: dead-man fires host-side cancels which cannot reach the venue — resting stops and venue cancel-after timers cover it.
- Host clock jumps after power loss: chrony resync before resuming.

## Cardinal rules (do NOT)

- Do NOT raise N to avoid flattening without C3.
- Do NOT disable cancel-on-disconnect on live accounts.
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/07-security-notes.md` §5: thresholds and UPS hooks.
- `docs/ui/dashboards/D06-risk.md`: UPS state on the dead-man tile.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.41 when this item is done.

## Branch & PR

- Branch: `p7/P7-T033-dead-man-fail-flat-4g`
- PR title: `P7-T033: Dead-man fail-flat configuration with UPS and 4G signals`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T033` run

## Progress log

- 2026-10-21 00:00 · planner · created
