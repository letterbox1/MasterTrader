---
id: P2-B020
kind: gap
title: Roadmap phase 2 entry criterion requires trade-only keys before the phase, contradicting build first, keys last
phase: 2
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.N3, R2.30]
roadmap_todos: []
modules: [M12]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B020-entry-criterion-keys-vs-keys-last
pr: ""
doc_sync: [docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: done
found_in: docs/roadmap/phase-2-strategies-risk-lab.md §2 Entry criteria
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B020 · Roadmap phase 2 entry criterion requires trade-only keys before the phase, contradicting build first, keys last

## Goal / expected outcome

The phase-2 entry criteria no longer require keys up front: keys are needed only for the late keyed check T2.72.

## Context & references

- Roadmap §2: "Testnet/practice **trade-only** keys exist (T2.03)" as an entry criterion.
- [17 §E 'build first, keys last'](../../../docs/17-decisions-register.md#e-ratification-2026-10-22); roadmap T2.25 (keyless build) and T2.72 (late keyed check after T2.03).

## Requirements

- **Steps to reproduce:** Read roadmap phase 2 §2 and T2.25/T2.72.
- **Expected:** keys listed as a precondition of T2.72 only.
- **Actual:** keys listed as a phase entry criterion.
- **Suggested fix:** Drop the entry criterion or reword it to 'needed before T2.72'. PHASE.md already treats it that way.
- **Impact:** S4: wording; with dependency gating the tasks already carry the real precondition (P2-T071 → P2-T001).

## ToDo

- [x] Suggested fix applied (17 §E build first, keys last)
- [x] Roadmap phase 2 §2 entry criteria no longer require keys; T2.03 keys are needed only before T2.72
- [x] PHASE.md and P2-T071 → P2-T001 dependency already carry it; no task change needed

## Verification

### Tests
- The affected tasks' tests encode the agreed behaviour.

### Scenarios
- Given the fixed docs, when a reader follows either section, then both describe the same behaviour.

### Stress / failure injection
- n/a: documentation gap

## Acceptance criteria

- [x] Docs agree: roadmap §2 links 17 §E
- [x] Affected tasks reference the decision

## Exceptions & edge cases

- Until resolved, the affected tasks follow 16/17 (the reference docs) as stated under Suggested fix.

## Cardinal rules (do NOT)

- Do NOT close without the doc fix merged and the dependent task(s) updated to match.
- Do NOT "fix" by silently picking a number in code; the decision is recorded in the docs and in policy.

## Doc sync on completion

- The doc(s) in `doc_sync`: aligned wording.

## Branch & PR

- Branch: `p2/P2-B020-entry-criterion-keys-vs-keys-last`
- PR title: `P2-B020: align docs`

## Progress log

- 2026-10-22 00:00 · aligner · opened during task alignment (docs/16–17 wave): doc contradiction found while aligning tasks
- 2026-10-22 00:00 · wrap-up doc agent · closed in the wrap-up: entry criterion reworded per 17 §E
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · verified: docs/roadmap/phase-2-strategies-risk-lab.md §2 Entry criteria (keys only before T2.72)
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the wrap-up
