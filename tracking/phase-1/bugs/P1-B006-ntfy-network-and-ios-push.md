---
id: P1-B006
kind: gap
title: ntfy has no network placement and iOS push needs an upstream relay
phase: 1
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.14]
roadmap_todos: []
modules: []
dashboards: []
branch: p1/P1-B006-ntfy-network-and-ios-push
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/07-security-notes.md]
doc_sync_status: n/a
found_in: docs/02-v1-architecture.md §3.1 and §3.2; docs/roadmap/phase-1-data-and-monitoring.md T1.43
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-B006 · ntfy has no network placement and iOS push needs an upstream relay

## Goal / expected outcome

02 §3.1 places `ntfy` (e.g. `edge` behind Caddy) and states how the phone receives pushes (Android via Tailscale websocket; iOS needs APNs via the ntfy.sh upstream relay, which sends only a message ID, or is accepted as best-effort)

## Context & references

- Found in: [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) adds `ntfy` in phase 1 but [02 §3.1](../../../docs/02-v1-architecture.md#31-networks) lists it in no network; T1.43 says "Tailscale only"
- Related items: P1-T003, P1-T044, P1-T060

## Requirements

- **Where:** [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) adds `ntfy` in phase 1 but [02 §3.1](../../../docs/02-v1-architecture.md#31-networks) lists it in no network; T1.43 says "Tailscale only"
- **Expected:** 02 §3.1 places `ntfy` (e.g. `edge` behind Caddy) and states how the phone receives pushes (Android via Tailscale websocket; iOS needs APNs via the ntfy.sh upstream relay, which sends only a message ID, or is accepted as best-effort)
- **Actual:** Network unspecified; iOS instant delivery is impossible with a purely Tailscale-only server unless the upstream relay is allowed
- **Suggested fix:** Document the network and the iOS decision; if upstream relay is allowed, add an egress allow-list entry for the relay
- **Impact:** Second alert channel may silently fail on iOS (severity S3)

## ToDo

- [ ] Decide with the user (phone platform)
- [ ] Edit 02 §3.1 and 07 §9
- [ ] Update the affected P1 task files if the decision changes their requirements

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [ ] Docs updated and consistent
- [ ] Root cause and decision noted in the progress log

## Exceptions & edge cases

- Until fixed, related tasks follow the interim rule stated in their own files

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a number in code; the decision lands in the docs first
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/02-v1-architecture.md`: apply the fix above
- `docs/07-security-notes.md`: apply the fix above

## Branch & PR

- Branch: `p1/P1-B006-ntfy-network-and-ios-push`
- PR title: `P1-B006: ntfy has no network placement and iOS push needs an upstream relay`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-B006` run

## Progress log

- 2026-10-21 00:00 · planner · opened
