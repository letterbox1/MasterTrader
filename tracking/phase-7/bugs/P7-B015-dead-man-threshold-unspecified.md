---
id: P7-B015
kind: gap
title: Dead-man heartbeat threshold 'N seconds' is never specified
phase: 7
type: DOC
status: done
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
doc_sync_status: done
found_in: docs/07-security-notes.md §6; docs/02-v1-architecture.md §6 rules; docs/03-build-spec.md M11
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
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

- [x] Decision recorded in docs/17 (17 §C P7-B015): three-layer dead-man: in-engine watchdog and deadman sidecar cancel at 5 s and apply each bot's on_system_failure at 10 s; venue cancel-after timers (15 s refresh, 60 s timeout) + resting stops
- [x] Owning docs carry it: 16 §3.1; 07 §5 and §6; D06 Dead-man tile
- [x] Affected Phase 7 tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P7-T033, P7-T052
- [x] Decision and root cause noted in the progress log

## Verification

### Tests
- Doc review: the cited sections now state one consistent rule; affected task files reference it.

### Scenarios
- Given an implementer reads only the fixed docs, then they implement the same behaviour the Phase 7 tasks assume.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (16 §3.1; 07 §5 and §6; D06 Dead-man tile)
- [x] Affected tasks consistent with it (P7-T033, P7-T052)
- [x] Root cause noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by docs/17 17 §C P7-B015: three-layer dead-man: in-engine watchdog and deadman sidecar cancel at 5 s and apply each bot's on_system_failure at 10 s; venue cancel-after timers (15 s refresh, 60 s timeout) + resting stops. Docs now carry it: 16 §3.1; 07 §5 and §6; D06 Dead-man tile. Implementation owned by P7-T033, P7-T052. Root cause: fail-flat timing was written as 'N seconds' everywhere.
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §C P7-B015); docs updated: 16 §3.1; 07 §5 and §6; D06 Dead-man tile; implementation owned by P7-T033, P7-T052
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
