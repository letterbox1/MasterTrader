---
id: P6-B012
kind: gap
title: LLM budget semantics unclear: monthly cap vs per-role daily budgets vs global provider budget; no defaults
phase: 6
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.07]
roadmap_todos: []
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p6/P6-B012-llm-budget-period-semantics
pr: ""
doc_sync: [docs/03-build-spec.md, docs/10-memory-rag-and-models.md]
doc_sync_status: done
found_in: docs/03-build-spec.md §7; docs/10-memory-rag-and-models.md §5; roadmap R6.07
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-B012 · LLM budget semantics unclear: monthly cap vs per-role daily budgets vs global provider budget; no defaults

## Goal / expected outcome

The docs agree and are specific enough to build from: a documented model: global monthly cap (UTC month) enforced month-to-date; per-role daily budgets; precedence = whichever exhausts first → local fallback; a `shadow` role; suggested default values.

## Context & references

- Found in: docs/03-build-spec.md §7; docs/10-memory-rag-and-models.md §5; roadmap R6.07
- [03 §7](../../../docs/03-build-spec.md#7-llm-cost-control) · [10 §5](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21)
- Affects: P6-T001, P6-T009, P6-T053

## Requirements

- **Steps to reproduce:** read docs/03-build-spec.md §7; docs/10-memory-rag-and-models.md §5; roadmap R6.07 and compare it with the cross-referenced sections listed under Context.
- **Expected:** a documented model: global monthly cap (UTC month) enforced month-to-date; per-role daily budgets; precedence = whichever exhausts first → local fallback; a `shadow` role; suggested default values.
- **Actual:** 03 §7 says 'monthly cap' plus 'per-role daily budgets'; 10 §5 has `budget_duration: 1d` per role and an unspecified 'global provider budget'; R6.07 says 'monthly spend cap; per-role budgets'. Precedence, period alignment and defaults are not stated; the shadow-check role (10 §4.3) has no budget.
- **Suggested fix:** Document as implemented in P6-T009.
- **Impact:** Ambiguous enforcement (severity S3)

## ToDo

- [x] Decision recorded in docs/17 (17 §C P6-B012): LLM budget defaults and semantics
- [x] Owning docs carry it: 16 §2.10 (US$40 monthly cap; daily debate $1.00, strategy-gen $0.50, explain $0.30, memory $0.30, chat $0.40, shadow $0.30; over budget → local fallback); 03 §7 (month-to-date cap, whichever is exhausted first routes to local); 10 §5 (UTC month, precedence, C1 lower / C3 raise); roadmap R6.07 and T6.32
- [x] Affected tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P6-T009 (enforcement, T6.32), P6-T010 (alerts), P6-T053 (budget test, T6.70), P6-T001 (your review)
- [x] Decision and source noted in the progress log

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (16 §2.10 (US$40 monthly cap; daily debate $1.00, strategy-gen $0.50, explain $0.30, memory $0.30, chat $0.40, shadow $0.30; over budget → local fallback); 03 §7 (month-to-date cap, whichever is exhausted first routes to local); 10 §5 (UTC month, precedence, C1 lower / C3 raise); roadmap R6.07 and T6.32)
- [x] Affected tasks consistent with it (P6-T009 (enforcement, T6.32), P6-T010 (alerts), P6-T053 (budget test, T6.70), P6-T001 (your review))
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- Until resolved, dependent tasks use the conservative interpretation stated under Suggested fix and note it in their progress log.

## Cardinal rules (do NOT)

- Do NOT silently pick a number in code; record the decision in the doc first.
- Do NOT edit docs owned by another phase's planner from a P6 branch without the owner's agreement; propose the change in the PR description.

## Doc sync on completion

- `docs/03-build-spec.md`: resolve the inconsistency.
- `docs/10-memory-rag-and-models.md`: resolve the inconsistency.

## Branch & PR

- Branch: `p6/P6-B012-llm-budget-period-semantics`
- PR title: `P6-B012: LLM budget semantics unclear: monthly cap vs per-role daily budgets vs global provider budget; no defaults`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-B012` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · resolved by docs/17 §C P6-B012: LLM budget defaults and semantics. Docs now carry it: 16 §2.10 (US$40 monthly cap; daily debate $1.00, strategy-gen $0.50, explain $0.30, memory $0.30, chat $0.40, shadow $0.30; over budget → local fallback); 03 §7 (month-to-date cap, whichever is exhausted first routes to local); 10 §5 (UTC month, precedence, C1 lower / C3 raise); roadmap R6.07 and T6.32. Implementation owned by P6-T009 (enforcement, T6.32), P6-T010 (alerts), P6-T053 (budget test, T6.70), P6-T001 (your review). Root cause: budgets were described in three places with no defaults or precedence.
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §C P6-B012); docs updated: 16 §2.10 LLM budgets, 03 §7, 10 §5 precedence/UTC month, roadmap R6.07/T6.32; implementation owned by P6-T009, P6-T010, P6-T053, P6-T001
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · doc sync done: docs already updated in this wave
