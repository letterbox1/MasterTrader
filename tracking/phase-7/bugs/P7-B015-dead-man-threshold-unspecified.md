---
id: P7-B015
kind: gap
title: Dead-man heartbeat threshold 'N seconds' is never specified
phase: 7
type: DOC
status: backlog
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.11]
roadmap_todos: []
modules: []
dashboards: []
branch: p7/P7-B015-dead-man-threshold-unspecified
pr: ""
doc_sync: [docs/07-security-notes.md, docs/ui/dashboards/D06-risk.md]
doc_sync_status: n/a
found_in: docs/07-security-notes.md §6; docs/02-v1-architecture.md §6 rules; docs/03-build-spec.md M11
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-B015 · Dead-man heartbeat threshold 'N seconds' is never specified

## Goal / expected outcome

The docs agree and are specific enough to implement: document defaults (e.g. internal 10 s; venue connectivity = failover time + 30 s, default 90 s) in 07 §6 and D06.

## Context & references

- Found in: `docs/07-security-notes.md §6; docs/02-v1-architecture.md §6 rules; docs/03-build-spec.md M11`
- Related: P7-T033

## Requirements

- **What:** The fail-flat timing depends on N, which is undefined everywhere.
- **Expected:** Defaults per heartbeat class (internal services vs venue connectivity), with venue connectivity N tied to the measured 4G failover time + margin.
- **Actual:** Only 'N seconds' appears.
- **Impact:** Too small → needless flattening on failover; too large → exposure during outages. (severity S4)
- **Suggested fix:** Document defaults (e.g. internal 10 s; venue connectivity = failover time + 30 s, default 90 s) in 07 §6 and D06.

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
- `docs/ui/dashboards/D06-risk.md`: apply the agreed fix.

## Branch & PR

- Branch: `p7/P7-B015-dead-man-threshold-unspecified`
- PR title: `P7-B015: fix dead-man heartbeat threshold 'N seconds' is never specified`
- PR checklist: doc fix or regression test · root cause in the progress log · `./kanban done` run

## Progress log

- 2026-10-21 00:00 · planner · opened
