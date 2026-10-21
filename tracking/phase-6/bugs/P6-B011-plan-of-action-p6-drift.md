---
id: P6-B011
kind: gap
title: 04 Phase 6 list omits Kev from bake-off contenders and its demo adds 'LLM-signal strategies run on paper' (not in roadmap exit criteria)
phase: 6
type: DOC
status: backlog
priority: medium
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.12, R6.06]
roadmap_todos: []
modules: []
dashboards: []
branch: p6/P6-B011-plan-of-action-p6-drift
pr: ""
doc_sync: [docs/04-plan-of-action.md]
doc_sync_status: n/a
found_in: docs/04-plan-of-action.md Phase 6
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-B011 · 04 Phase 6 list omits Kev from bake-off contenders and its demo adds 'LLM-signal strategies run on paper' (not in roadmap exit criteria)

## Goal / expected outcome

The docs agree and are specific enough to build from: 04 and the roadmap describe the same contenders and the same demo.

## Context & references

- Found in: docs/04-plan-of-action.md Phase 6
- [04 Phase 6](../../../docs/04-plan-of-action.md#phase-6--ai-decision-layer-memory--anomalies-weeks-2428) · [roadmap §6 exit criteria](../../../docs/roadmap/phase-6-ai-models-treasury.md#6-exit-criteria-demo)

## Requirements

- **Steps to reproduce:** read docs/04-plan-of-action.md Phase 6 and compare it with the cross-referenced sections listed under Context.
- **Expected:** 04 and the roadmap describe the same contenders and the same demo.
- **Actual:** 04 lists contenders 'own head vs Laya vs Clef-flash vs SemIf vs JSON' (Kev only in a later bullet) and the demo includes 'LLM-signal strategies run on paper'; roadmap §6 exit criteria don't include the paper item (it is T6.80 RUN).
- **Suggested fix:** Add Kev to the 04 contender list; state that LLM-signal paper trading starts in P6 (T6.80) and is checked at P7 entry.
- **Impact:** Minor drift (severity S4)

## ToDo

- [ ] Propose the edit.
- [ ] Update the docs listed under Doc sync and link the resolving commit here.

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] 04 Phase 6 consistent with roadmap.
- [ ] Root cause noted in the progress log.

## Exceptions & edge cases

- Until resolved, dependent tasks use the conservative interpretation stated under Suggested fix and note it in their progress log.

## Cardinal rules (do NOT)

- Do NOT silently pick a number in code; record the decision in the doc first.
- Do NOT edit docs owned by another phase's planner from a P6 branch without the owner's agreement; propose the change in the PR description.

## Doc sync on completion

- `docs/04-plan-of-action.md`: resolve the inconsistency.

## Branch & PR

- Branch: `p6/P6-B011-plan-of-action-p6-drift`
- PR title: `P6-B011: 04 Phase 6 list omits Kev from bake-off contenders and its demo adds 'LLM-signal strategies run on paper' (not in roadmap exit criteria)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-B011` run

## Progress log

- 2026-10-21 00:00 · planner · created
