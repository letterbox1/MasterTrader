---
id: P0-B004
kind: gap
title: No numeric SLO for WORM insert throughput or command latency
phase: 0
type: DOC
status: ready
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
branch: p0/P0-B004-worm-insert-command-latency-slo-missing
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/15-bots-hitl-and-worm-audit.md]
doc_sync_status: n/a
found_in: docs/15-bots-hitl-and-worm-audit.md §2.4
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- `docs/02-v1-architecture.md`: reconcile as described.
- `docs/15-bots-hitl-and-worm-audit.md`: reconcile as described.

## Branch & PR

- Branch: `p0/P0-B004-worm-insert-command-latency-slo-missing`
- PR title: `P0-B004: fix no numeric SLO for WORM insert throughput or command latency`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B004` run

## Progress log

- 2026-10-21 00:00 · planner · opened
