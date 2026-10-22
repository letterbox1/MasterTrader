---
id: P0-B004
kind: gap
title: No numeric SLO for WORM insert throughput or command latency
phase: 0
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.07, R0.08]
roadmap_todos: [T0.61]
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p0/P0-B004-worm-insert-command-latency-slo-missing
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/15-bots-hitl-and-worm-audit.md]
doc_sync_status: done
found_in: docs/15-bots-hitl-and-worm-audit.md §2.4
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-B004 · No numeric SLO for WORM insert throughput or command latency

## Goal / expected outcome

The docs agree and the implementing tasks have one unambiguous answer. Suggested fix: Add to 02 §9.2: `audit.*` insert p99 < 5 ms at ≥ 1,000 rows/s per chain; command bus p99 < 50 ms excl. handler; fills/commands never wait on seals. P0 tasks use these as provisional targets.

## Context & references

- Found in: `docs/15-bots-hitl-and-worm-audit.md §2.4`
- Related: P0-T030, P0-T055, P0-T059
- [02 §9.2 SLOs](../../../docs/02-v1-architecture.md#92-observability--slos)
- [15 §2.4 tests](../../../docs/15-bots-hitl-and-worm-audit.md#24-tests-part-of-every-phase-that-adds-a-worm-table)

## Requirements

- **Steps to reproduce:** 15 §2.4 requires 'insert throughput with hashing stays within the SLOs'; look in 02 §9.2 for an audit or command SLO.
- **Expected:** Numeric targets for audit insert (rows/s, p99 latency) and command-path latency.
- **Actual:** 02 §9.2 has no audit/command SLO, so the WORM test can't pass or fail objectively.
- **Impact:** Performance regressions in the hash chain or command bus go unnoticed until the order path (P2) suffers.
- **Suggested fix:** Add to 02 §9.2: `audit.*` insert p99 < 5 ms at ≥ 1,000 rows/s per chain; command bus p99 < 50 ms excl. handler; fills/commands never wait on seals. P0 tasks use these as provisional targets.

## ToDo

- [x] Decision taken: 17 §D P0-B004 (ratified in 17 §E)
- [x] Docs updated so they agree: 02 §9.2 (WORM insert p99 < 5 ms; command bus p99 < 50 ms); 15 §2.2 Write path + §2.4; 03 §4; roadmap P0 R0.N7/T0.67
- [x] Affected P0 task files reference the resolution: P0-T030, P0-T031, P0-T034, P0-T037, P0-T055, P0-T059
- [x] Regression check owned: P0-T066 gated benchmark

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Listed docs carry the 17 §D P0-B004 decision and agree (checked in the alignment wave, 2026-10-22)
- [x] Implementation owned by: P0-T066 (benchmark)
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- If the user decides differently from the suggestion, the affected tasks are updated before they start.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/02-v1-architecture.md`: reconcile as described.
- `docs/15-bots-hitl-and-worm-audit.md`: reconcile as described.

## Branch & PR

- Branch: `p0/P0-B004-worm-insert-command-latency-slo-missing`
- PR title: `P0-B004: fix no numeric SLO for WORM insert throughput or command latency`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B004` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D P0-B004; docs checked: 02 §9.2 (WORM insert p99 < 5 ms; command bus p99 < 50 ms); 15 §2.2 Write path + §2.4; 03 §4; roadmap P0 R0.N7/T0.67. Root cause: 15 §2.4 referred to 'the SLOs' before 02 §9.2 had a WORM or command row. Implementation owned by P0-T066 (benchmark).
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P0-B004); docs updated: 02 §9.2 (WORM insert p99 < 5 ms; command bus p99 < 50 ms); 15 §2.2 Write path + §2.4; 03 §4; roadmap P0 R0.N7/T0.67; implementation owned by P0-T066 (benchmark)
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
