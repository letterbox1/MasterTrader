---
id: P7-B004
kind: gap
title: 4G failover changes egress IP and breaks IP-locked keys
phase: 7
type: DOC
status: done
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
doc_sync_status: done
found_in: docs/07-security-notes.md §3 (IP allow-list to static egress IP) vs §5 (4G failover)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
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

- [x] Decision recorded in docs/17 (17 §A P7-B004): static AU egress via a WireGuard/Tailscale exit node with a fixed Sydney IP; only that IP allow-listed; broadband and 4G both tunnel to it; tunnel down → fail-flat via venue timers + resting stops; egress IP/country check
- [x] Owning docs carry it: 16 §3.2; 07 §3 and §5 (and the threats table); roadmap R7.14 and T7.11/T7.42/T7.64
- [x] Affected Phase 7 tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P7-T065, P7-T066, P7-T007, P7-T047, P7-T052
- [x] Decision and root cause noted in the progress log

## Verification

### Tests
- Doc review: the cited sections now state one consistent rule; affected task files reference it.

### Scenarios
- Given an implementer reads only the fixed docs, then they implement the same behaviour the Phase 7 tasks assume.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (16 §3.2; 07 §3 and §5 (and the threats table); roadmap R7.14 and T7.11/T7.42/T7.64)
- [x] Affected tasks consistent with it (P7-T065, P7-T066, P7-T007, P7-T047, P7-T052)
- [x] Root cause noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by docs/17 17 §A P7-B004: static AU egress via a WireGuard/Tailscale exit node with a fixed Sydney IP; only that IP allow-listed; broadband and 4G both tunnel to it; tunnel down → fail-flat via venue timers + resting stops; egress IP/country check. Docs now carry it: 16 §3.2; 07 §3 and §5 (and the threats table); roadmap R7.14 and T7.11/T7.42/T7.64. Implementation owned by P7-T065, P7-T066, P7-T007, P7-T047, P7-T052. Root cause: IP-locked keys and a CGNAT 4G backup were specified separately with no egress design.
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §A P7-B004); docs updated: 16 §3.2; 07 §3 and §5 (and the threats table); roadmap R7.14 and T7.11/T7.42/T7.64; implementation owned by P7-T065, P7-T066, P7-T007, P7-T047, P7-T052
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
