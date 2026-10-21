---
id: P0-B012
kind: gap
title: `system.service.restart` needs Docker control from mt-api with no safe mechanism defined
phase: 0
type: DOC
status: ready
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
branch: p0/P0-B012-service-restart-mechanism-unspecified
pr: ""
doc_sync: [docs/ui/dashboards/D16-system.md, docs/07-security-notes.md]
doc_sync_status: n/a
found_in: docs/ui/dashboards/D16-system.md (Actions)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- [ ] Confirm the decision with the user (or take the suggested fix if no objection)
- [ ] Update the listed docs so they agree
- [ ] Update the affected P0 task files' Context if the decision differs from the suggestion
- [ ] Add/adjust a regression check where one is possible (see Verification)

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Listed docs updated and consistent
- [ ] Affected tasks reference the resolution
- [ ] Root cause (how the drift happened) noted in the progress log

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
