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
depends_on: [P0-T012]
requirements: [R7.11, R7.14]
roadmap_todos: [T7.09]
modules: [M11]
dashboards: [D16]
tools: []
mcp: []
env: []
services: [UPS, 4G failover router]
branch: p7/P7-T009-ups-and-4g-failover
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

# P7-T009 · Install the UPS and 4G failover for the host and router

## Goal / expected outcome

The host and router run on a UPS with enough runtime to fail flat cleanly, and a 4G failover link takes over on a fixed-line outage while exchange traffic keeps the **same static egress IP** because both links tunnel to the Sydney exit node (16 §3.2).

## Context & references

- Roadmap: [R7.11 · ToDo T7.09](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [07 §5](../../../docs/07-security-notes.md#5-network--host) (UPS on host and router, 4G failover, fail flat, resting broker-side stops)
- Cross-phase: P0-T012 (T0.02, UPS and 4G router ordered) is a `depends_on`.
- Related: P7-T033 (dead-man/fail-flat config), P7-T066 (exit-node tunnel over both links), P7-T052 (failover drill, T7.64), P7-T053 (pull-the-plug drill) · decision [17 §A P7-B004](../../../docs/17-decisions-register.md#a-s2-items-all-resolved), [16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys)

## Requirements

- UPS runtime ≥ 15 min at host+router load; USB/network signalling to the host (NUT) so a low-battery event triggers the fail-flat path before shutdown.
- 4G router in automatic failover mode; it only has to give the host internet: exchange traffic reaches the venues through the exit-node tunnel (P7-T066) on either link, so the allow-listed IP never changes (16 §3.2).
- Failover time (link switch + tunnel re-established) measured and recorded; target ≤ the venue cancel-after timeout (default 60 s, 16 §3.1). The dead-man timings stay the 16 §3.1 defaults (5 s cancel / 10 s `on_system_failure`); they are not derived from the failover time.

## ToDo

- [ ] Install the UPS; plug in host, router, 4G router; connect the UPS signal cable to the host.
- [ ] Configure the 4G router for automatic failover; test by unplugging the fixed line.
- [ ] If the 4G router needs settings for the tunnel to pass, store its admin access in the sops file so P7-T066 can confirm the tunnel works over 4G.
- [ ] Measure: UPS runtime at load, failover time; record both on the task.
- [ ] Tell the agent so P7-T033 can configure the NUT events.

## Verification

### Tests
- n/a (user action); P7-T052 automates the failover test.

### Scenarios
- Given the fixed line is unplugged, when 4G takes over and the tunnel re-establishes, then the venues still see the exit node's IP and venue connections resume.
- Given mains power is cut, when the UPS reaches low battery, then NUT signals the host and fail-flat runs before shutdown.

### Stress / failure injection
- Unplug the fixed line 3 times in 10 minutes; record failover each time.

## Acceptance criteria

- [ ] UPS runtime and failover time recorded and meet the numbers above.
- [ ] The UPS signals the host (NUT) and the 4G link carries the exit-node tunnel (confirmed with P7-T066).

## Exceptions & edge cases

- 4G carrier CGNAT changes the public IP: irrelevant to the venues because exchange traffic exits via the tunnel; never widen key allow-lists.
- UPS battery ages: record the install date; replace per vendor guidance.

## Cardinal rules (do NOT)

- Do NOT widen API key IP allow-lists to make failover 'work'.
- Do NOT run live positions before the pull-the-plug drill passes (P7-T053).
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).

## Doc sync on completion

- `docs/07-security-notes.md` §5: record the measured UPS runtime and failover time.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.09 when this item is done.

## Branch & PR

- Branch: `p7/P7-T009-ups-and-4g-failover`
- PR title: `P7-T009: Install the UPS and 4G failover for the host and router`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T009` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (egress via the exit-node tunnel on both links per 16 §3.2/17 §A P7-B004; dead-man timings per 16 §3.1; dep P0-T012)
