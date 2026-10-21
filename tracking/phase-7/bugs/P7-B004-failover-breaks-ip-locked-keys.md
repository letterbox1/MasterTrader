---
id: P7-B004
kind: gap
title: 4G failover changes egress IP and breaks IP-locked keys
phase: 7
type: DOC
status: backlog
priority: high
size: S
severity: S2
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.11, R7.04]
roadmap_todos: []
modules: []
dashboards: []
branch: p7/P7-B004-failover-breaks-ip-locked-keys
pr: ""
doc_sync: [docs/07-security-notes.md]
doc_sync_status: n/a
found_in: docs/07-security-notes.md §3 (IP allow-list to static egress IP) vs §5 (4G failover)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-B004 · 4G failover changes egress IP and breaks IP-locked keys

## Goal / expected outcome

The docs agree and are specific enough to implement: route all venue traffic through a fixed-IP egress you control (e.g. a small VPS/Tailscale exit node with a static IP), reachable over either link; allow-list only that IP. Document it in 07 §3 and §5.

## Context & references

- Found in: `docs/07-security-notes.md §3 (IP allow-list to static egress IP) vs §5 (4G failover)`
- Related: P7-T007, P7-T009, P7-T033, P7-T052

## Requirements

- **What:** Keys are allow-listed to one static egress IP, but a consumer 4G link egresses from a different (often CGNAT) IP.
- **Expected:** During failover the host can still reach venues with the same allow-listed IP (or allow-lists contain a second fixed IP you control), so fail-flat and protective orders work.
- **Actual:** No design for egress during failover; the 'fail flat' policy assumes venue calls still succeed on 4G.
- **Impact:** On a fixed-line outage every venue rejects requests, so the system cannot flatten or amend stops — only resting broker-side stops remain. (severity S2)
- **Suggested fix:** Route all venue traffic through a fixed-IP egress you control (e.g. a small VPS/Tailscale exit node with a static IP), reachable over either link; allow-list only that IP. Document it in 07 §3 and §5.

## ToDo

- [ ] Confirm the conflict/omission against the cited sections
- [ ] Agree the resolution (the user decides where it changes risk or money rules)
- [ ] Edit the docs listed under Doc sync in one PR
- [ ] Update any Phase 7 task text that depended on the assumption

## Verification

### Tests
- Doc review: the cited sections now state one consistent rule; affected task files reference it.

### Scenarios
- Given an implementer reads only the fixed docs, then they implement the same behaviour the Phase 7 tasks assume.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Docs updated and consistent
- [ ] Root cause noted in the progress log

## Exceptions & edge cases

- If the user picks a different resolution than suggested, update the dependent Phase 7 tasks in the same PR.

## Cardinal rules (do NOT)

- Do NOT resolve a conflict by picking the looser number.
- Do NOT edit generated files (`KANBAN.md`, boards, README marked blocks) by hand.

## Doc sync on completion

- `docs/07-security-notes.md`: apply the agreed fix.

## Branch & PR

- Branch: `p7/P7-B004-failover-breaks-ip-locked-keys`
- PR title: `P7-B004: fix 4G failover changes egress IP and breaks IP-locked keys`
- PR checklist: doc fix or regression test · root cause in the progress log · `./kanban done` run

## Progress log

- 2026-10-21 00:00 · planner · opened
