---
id: P0-B012
kind: gap
title: `system.service.restart` needs Docker control from mt-api with no safe mechanism defined
phase: 0
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.11]
roadmap_todos: [T0.26]
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p0/P0-B012-service-restart-mechanism-unspecified
pr: ""
doc_sync: [docs/ui/dashboards/D16-system.md, docs/07-security-notes.md]
doc_sync_status: done
found_in: docs/ui/dashboards/D16-system.md (Actions)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-B012 · `system.service.restart` needs Docker control from mt-api with no safe mechanism defined

## Goal / expected outcome

The docs agree and the implementing tasks have one unambiguous answer. Suggested fix: Decide the mechanism before P2 (engine restarts matter there) and document it in 07 §6 and D16.

## Context & references

- Found in: `docs/ui/dashboards/D16-system.md (Actions)`
- Related: P0-T034, P0-T046, P0-T051
- [D16 System](../../../docs/ui/dashboards/D16-system.md)

## Requirements

- **Steps to reproduce:** D16 lists 'Restart service' (C2); look for how mt-api restarts containers.
- **Expected:** A least-privilege mechanism (e.g. a host-side systemd unit triggered via a restricted socket with an allow-list) or deferral.
- **Actual:** Unspecified; the obvious route (Docker socket in mt-api) is a host-root escalation path contrary to 07.
- **Impact:** Low: P0 ships the command as 501 with the button disabled.
- **Suggested fix:** Decide the mechanism before P2 (engine restarts matter there) and document it in 07 §6 and D16.

## ToDo

- [x] Decision taken: 17 §D P0-B012 (ratified in 17 §E)
- [x] Docs updated so they agree: 02 §3.1 (`ctl` network) + §3.2 (`docker-proxy` row) + §7.2 (`system.service.restart` allow-listed via `docker-proxy`); 07 §5 ('No Docker socket in app containers'); D16 Restart service row; 04 Phase 0; roadmap P0 R0.14/T0.47/T0.68
- [x] Affected P0 task files reference the resolution: P0-T021, P0-T034, P0-T046, P0-T051, P0-T056
- [x] Regression check owned: P0-T067 refusal suite

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Listed docs carry the 17 §D P0-B012 decision and agree (checked in the alignment wave, 2026-10-22)
- [x] Implementation owned by: P0-T065 (docker-proxy), P0-T067 (refusal test)
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- If the user decides differently from the suggestion, the affected tasks are updated before they start.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/ui/dashboards/D16-system.md`: reconcile as described.
- `docs/07-security-notes.md`: reconcile as described.

## Branch & PR

- Branch: `p0/P0-B012-service-restart-mechanism-unspecified`
- PR title: `P0-B012: fix `system.service.restart` needs Docker control from mt-api with no safe mechanism defined`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B012` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D P0-B012; docs checked: 02 §3.1 (`ctl` network) + §3.2 (`docker-proxy` row) + §7.2 (`system.service.restart` allow-listed via `docker-proxy`); 07 §5 ('No Docker socket in app containers'); D16 Restart service row; 04 Phase 0; roadmap P0 R0.14/T0.47/T0.68. Root cause: D16 listed a restart action without a least-privilege mechanism. Implementation owned by P0-T065 (docker-proxy), P0-T067 (refusal test).
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P0-B012); docs updated: 02 §3.1 (`ctl` network) + §3.2 (`docker-proxy` row) + §7.2 (`system.service.restart` allow-listed via `docker-proxy`); 07 §5 ('No Docker socket in app containers'); D16 Restart service row; 04 Phase 0; roadmap P0 R0.14/T0.47/T0.68; implementation owned by P0-T065 (docker-proxy), P0-T067 (refusal test)
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
