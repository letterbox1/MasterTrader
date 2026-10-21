---
id: P6-B010
kind: gap
title: LLM calls from P2–P5 (leakage review, SemIf-adjacent jobs, morning brief) run before the `audit.llm_call` writer lands in P6
phase: 6
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.03]
roadmap_todos: []
modules: []
dashboards: []
branch: p6/P6-B010-llm-calls-unaudited-before-p6
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: docs/roadmap/phase-0-foundations.md R0.07/R0.09 vs docs/roadmap/phase-6-ai-models-treasury.md R6.03
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-B010 · LLM calls from P2–P5 (leakage review, SemIf-adjacent jobs, morning brief) run before the `audit.llm_call` writer lands in P6

## Goal / expected outcome

The docs agree and are specific enough to build from: LLM calls are audited from the first phase that makes them (P0/P2).

## Context & references

- Found in: docs/roadmap/phase-0-foundations.md R0.07/R0.09 vs docs/roadmap/phase-6-ai-models-treasury.md R6.03
- [03 M17](../../../docs/03-build-spec.md#m17-observability--audit--mt_obs) (every LLM call audited) · [SPEC non-negotiables](../../../SPEC.md#non-negotiable-requirements) (append-only audit incl. LLM calls)
- P2 T2.27 (leakage review via the gateway), P4 R4.14 (morning brief), P3 T3.64 (prompt audit)
- Affects: P6-T005

## Requirements

- **Steps to reproduce:** read docs/roadmap/phase-0-foundations.md R0.07/R0.09 vs docs/roadmap/phase-6-ai-models-treasury.md R6.03 and compare it with the cross-referenced sections listed under Context.
- **Expected:** LLM calls are audited from the first phase that makes them (P0/P2).
- **Actual:** The gateway exists from P0 and is used from P2, but the LLM-call audit (R6.03) is only scheduled in P6; no earlier roadmap item creates `audit.llm_call` or its writer.
- **Suggested fix:** Move the callback writer (P6-T005 scope) to P0/P2 or add an explicit P2 item; P6-T005 then only extends it (prompt registry, training_cutoff).
- **Impact:** Months of unaudited LLM calls; breaks the 'record everything' principle (severity S3)

## ToDo

- [ ] Raise with P0/P2 planners.
- [ ] If moved, re-scope P6-T005 to the extension only.
- [ ] Update the docs listed under Doc sync and link the resolving commit here.

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Owning phase decided and documented.
- [ ] Root cause noted in the progress log.

## Exceptions & edge cases

- Until resolved, dependent tasks use the conservative interpretation stated under Suggested fix and note it in their progress log.

## Cardinal rules (do NOT)

- Do NOT silently pick a number in code; record the decision in the doc first.
- Do NOT edit docs owned by another phase's planner from a P6 branch without the owner's agreement; propose the change in the PR description.

## Doc sync on completion

- `docs/roadmap/phase-0-foundations.md`: resolve the inconsistency.
- `docs/roadmap/phase-6-ai-models-treasury.md`: resolve the inconsistency.

## Branch & PR

- Branch: `p6/P6-B010-llm-calls-unaudited-before-p6`
- PR title: `P6-B010: LLM calls from P2–P5 (leakage review, SemIf-adjacent jobs, morning brief) run before the `audit.llm_call` writer lands in P6`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-B010` run

## Progress log

- 2026-10-21 00:00 · planner · created
