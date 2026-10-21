---
id: P7-T009
kind: task
title: Install the UPS and 4G failover for the host and router
phase: 7
type: USER
status: backlog
priority: high
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R7.11]
roadmap_todos: [T7.09]
modules: [M11]
dashboards: [D16]
branch: p7/P7-T009-ups-and-4g-failover
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T009 · Install the UPS and 4G failover for the host and router

## Goal / expected outcome

The host and router run on a UPS with enough runtime to fail flat cleanly, and a 4G failover link takes over on a fixed-line outage while keeping the **same static egress IP** for venue IP allow-lists.

## Context & references

- Roadmap: [R7.11 · ToDo T7.09](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [07 §5](../../../docs/07-security-notes.md#5-network--host) (UPS on host and router, 4G failover, fail flat, resting broker-side stops)
- Cross-phase: P0 T0.02 (UPS and 4G router ordered).
- Related: P7-T033 (dead-man/fail-flat config), P7-T052 (automated failover test), P7-T053 (pull-the-plug drill), gap P7-B004

## Requirements

- UPS runtime ≥ 15 min at host+router load; USB/network signalling to the host (NUT) so a low-battery event triggers the fail-flat path before shutdown.
- 4G router in failover mode; the host's egress must stay on the allow-listed static IP (e.g. both links route through a fixed-IP Tailscale exit node or VPN endpoint you control) — otherwise venue calls fail during failover (P7-B004).
- Failover time ≤ 60 s; the dead-man threshold (P7-T033) is set relative to it.

## ToDo

- [ ] Install the UPS; plug in host, router, 4G router; connect the UPS signal cable to the host.
- [ ] Configure the 4G router for automatic failover; test by unplugging the fixed line.
- [ ] Agree the egress design with the planner (P7-B004) and configure it; record the egress IP(s) on the task.
- [ ] Measure: UPS runtime at load, failover time; record both on the task.
- [ ] Tell the planner so P7-T033 can configure NUT events and dead-man thresholds.

## Verification

### Tests
- n/a (user action); P7-T052 automates the failover test.

### Scenarios
- Given the fixed line is unplugged, when 4G takes over, then the host's public egress IP is unchanged and venue heartbeats continue.
- Given mains power is cut, when the UPS reaches low battery, then NUT signals the host and fail-flat runs before shutdown.

### Stress / failure injection
- Unplug the fixed line 3 times in 10 minutes; record failover each time.

## Acceptance criteria

- [ ] UPS runtime and failover time recorded and meet the numbers above.
- [ ] Egress IP is unchanged across failover (or the gap P7-B004 is resolved another way).

## Exceptions & edge cases

- 4G carrier CGNAT changes IP: route through a fixed-IP exit; never widen key allow-lists.
- UPS battery ages: record the install date; replace per vendor guidance.

## Cardinal rules (do NOT)

- Do NOT widen API key IP allow-lists to make failover 'work'.
- Do NOT run live positions before the pull-the-plug drill passes (P7-T053).
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).

## Doc sync on completion

- `docs/07-security-notes.md` §5: document the egress design used during failover.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.09 when this item is done.

## Branch & PR

- Branch: `p7/P7-T009-ups-and-4g-failover`
- PR title: `P7-T009: Install the UPS and 4G failover for the host and router`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T009` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
