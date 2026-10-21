---
id: P6-B016
kind: gap
title: Hindsight point-in-time recall unverified, especially for consolidated/reflected memories
phase: 6
type: BUILD
status: backlog
priority: high
size: S
severity: S2
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.04]
roadmap_todos: []
modules: []
dashboards: []
branch: p6/P6-B016-hindsight-pit-consolidated-memories
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md]
doc_sync_status: n/a
found_in: docs/10-memory-rag-and-models.md §1 (Point-in-time recall)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-B016 · Hindsight point-in-time recall unverified, especially for consolidated/reflected memories

## Goal / expected outcome

Memory recall in backtests provably never returns information created after `as_of`, including Hindsight's consolidated/derived memories, and 10 §1 documents the mechanism.

## Context & references

- Found in: docs/10-memory-rag-and-models.md §1 (Point-in-time recall)
- [10 §1](../../../docs/10-memory-rag-and-models.md#1-hindsight-self-hosted-agent-memory) · [SPEC non-negotiables](../../../SPEC.md#non-negotiable-requirements) NN1
- Affects: P6-T012 (fix), P6-T055 (test)

## Requirements

- **Steps to reproduce:** read docs/10-memory-rag-and-models.md §1 (Point-in-time recall) and compare it with the cross-referenced sections listed under Context.
- **Expected:** a verified PIT mechanism covering raw and derived memories, tested in CI.
- **Actual:** 10 §1 states PIT recall 'filters by memory creation time ≤ as_of', but it is not verified that Hindsight's API supports a creation-time filter, and consolidation/reflect create derived memories (observations, mental models) whose sources may post-date `as_of` even if the derived item's own timestamp does not — or whose timestamp is 'now' while summarising old facts.
- **Suggested fix:** Implement in `mt_memory` a post-filter with over-fetch plus lineage check (exclude derived memories unless all sources ≤ as_of), or disable consolidation for backtest banks; document the mechanism in 10 §1.
- **Impact:** Backtests could 'remember the future' — breaks a non-negotiable (severity S2)

## ToDo

- [ ] Inspect Hindsight 1.0.0 API for time filters and derived-memory lineage.
- [ ] Choose mechanism; implement in P6-T012.
- [ ] Prove with P6-T055.
- [ ] Update the docs listed under Doc sync and link the resolving commit here.

## Verification

### Tests
- Regression test: P6-T055 PIT recall test (raw + consolidated memories).

### Scenarios
- Given a consolidated observation built from memories at t1 and t5, when recalling at as_of=t3, then it is excluded.

### Stress / failure injection
- 10k memories with heavy consolidation enabled; replay recall at 250 dates: zero violations (P6-T055).

## Acceptance criteria

- [ ] Mechanism documented and P6-T055 green.
- [ ] Root cause noted in the progress log.

## Exceptions & edge cases

- Until resolved, dependent tasks use the conservative interpretation stated under Suggested fix and note it in their progress log.

## Cardinal rules (do NOT)

- Do NOT accept 'same-day' tolerance in PIT filters.
- Do NOT silently pick a number in code; record the decision in the doc first.
- Do NOT edit docs owned by another phase's planner from a P6 branch without the owner's agreement; propose the change in the PR description.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md`: resolve the inconsistency.

## Branch & PR

- Branch: `p6/P6-B016-hindsight-pit-consolidated-memories`
- PR title: `P6-B016: Hindsight point-in-time recall unverified, especially for consolidated/reflected memories`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-B016` run

## Progress log

- 2026-10-21 00:00 · planner · created
