---
id: P2-B019
kind: gap
title: 02 F2 says the egress check applies from P7, while R2.58 checks egress status inline from Phase 2
phase: 2
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.58]
roadmap_todos: []
modules: [M11]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B019-f2-egress-from-p7-wording
pr: ""
doc_sync: [docs/02-v1-architecture.md]
doc_sync_status: done
found_in: docs/02-v1-architecture.md F2 step 4
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B019 · 02 F2 says the egress check applies from P7, while R2.58 checks egress status inline from Phase 2

## Goal / expected outcome

02 F2 states that M11 reads the egress status (R1.16) from P2, and that the fixed exit-node IP arrives in P7.

## Context & references

- [02 F2 step 4](../../../docs/02-v1-architecture.md#8-end-to-end-flows): "egress status (from P7)".
- Roadmap [R2.58/T2.39](../../../docs/roadmap/phase-2-strategies-risk-lab.md) (inline in P2) and [P1 R1.16/T1.33](../../../docs/roadmap/phase-1-data-and-monitoring.md) (egress check built in P1).

## Requirements

- **Steps to reproduce:** Compare 02 F2 step 4 with R2.58.
- **Expected:** 'egress status (R1.16; the exit-node IP from P7)'.
- **Actual:** 'from P7'.
- **Suggested fix:** Reword 02 F2. P2-T070 checks `egress.status` from P2.
- **Impact:** S4: wording only.

## ToDo

- [x] Suggested fix applied
- [x] 02 F2 step 4: egress status checked from Phase 1 (P1-T071), fixed exit-node IP from P7
- [x] P2-T070 doc-sync note updated

## Verification

### Tests
- The affected tasks' tests encode the agreed behaviour.

### Scenarios
- Given the fixed docs, when a reader follows either section, then both describe the same behaviour.

### Stress / failure injection
- n/a: documentation gap

## Acceptance criteria

- [x] Docs agree: 02 F2 matches R1.16/R2.58
- [x] Affected tasks reference the decision

## Exceptions & edge cases

- Until resolved, the affected tasks follow 16/17 (the reference docs) as stated under Suggested fix.

## Cardinal rules (do NOT)

- Do NOT close without the doc fix merged and the dependent task(s) updated to match.
- Do NOT "fix" by silently picking a number in code; the decision is recorded in the docs and in policy.

## Doc sync on completion

- The doc(s) in `doc_sync`: aligned wording.

## Branch & PR

- Branch: `p2/P2-B019-f2-egress-from-p7-wording`
- PR title: `P2-B019: align docs`

## Progress log

- 2026-10-22 00:00 · aligner · opened during task alignment (docs/16–17 wave): doc contradiction found while aligning tasks
- 2026-10-22 00:00 · wrap-up doc agent · closed in the wrap-up: 02 F2 no longer says 'from P7'
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · verified: docs/02-v1-architecture.md F2 step 4 (egress check from Phase 1, P1-T071; exit-node IP P7); P2-T070 note updated
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the wrap-up
