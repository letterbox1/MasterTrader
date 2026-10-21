---
id: P6-B003
kind: gap
title: Kev-4B/9B bake-off challenger has no source, licence or serving notes anywhere
phase: 6
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.12]
roadmap_todos: []
modules: []
dashboards: []
branch: p6/P6-B003-kev-source-licence-unspecified
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/research/decision-models-system-one.md]
doc_sync_status: n/a
found_in: docs/10-memory-rag-and-models.md §4.3 (bake-off contenders)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-B003 · Kev-4B/9B bake-off challenger has no source, licence or serving notes anywhere

## Goal / expected outcome

The docs agree and are specific enough to build from: Kev has a row in 10 §4.1 (publisher, licence, size, serving, latency) or is explicitly excluded.

## Context & references

- Found in: docs/10-memory-rag-and-models.md §4.3 (bake-off contenders)
- [10 §4.1](../../../docs/10-memory-rag-and-models.md#41-what-decision-models-are-and-the-candidates) (candidate table omits Kev) · [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) · [11 review](../../../docs/11-cryptotrader-crossover-review.md) · [research: decision models](../../../docs/research/decision-models-system-one.md)
- Affects: P6-T002, P6-T027, P6-T029

## Requirements

- **Steps to reproduce:** read docs/10-memory-rag-and-models.md §4.3 (bake-off contenders) and compare it with the cross-referenced sections listed under Context.
- **Expected:** Kev has a row in 10 §4.1 (publisher, licence, size, serving, latency) or is explicitly excluded.
- **Actual:** Kev-4B/9B is named as a contender in 10 §4.3, R6.12, T6.40, D10 and 04, but no doc says who publishes it, its licence, weights location, context length or how to serve it; it is absent from the 10 §4.1 candidate table and the research notes.
- **Suggested fix:** Add the row after P6-T002 confirms the source; if not free/self-hostable, mark it excluded like Jev.
- **Impact:** Bake-off scope unclear; risk of pulling unvetted weights (severity S3)

## ToDo

- [ ] Collect Kev details via P6-T002.
- [ ] Draft the 10 §4.1 row.
- [ ] Update the docs listed under Doc sync and link the resolving commit here.

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] 10 §4.1 lists Kev with licence or exclusion; D10 and R6.12 consistent.
- [ ] Root cause noted in the progress log.

## Exceptions & edge cases

- Until resolved, dependent tasks use the conservative interpretation stated under Suggested fix and note it in their progress log.

## Cardinal rules (do NOT)

- Do NOT download or run weights without a confirmed licence.
- Do NOT silently pick a number in code; record the decision in the doc first.
- Do NOT edit docs owned by another phase's planner from a P6 branch without the owner's agreement; propose the change in the PR description.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md`: resolve the inconsistency.
- `docs/research/decision-models-system-one.md`: resolve the inconsistency.

## Branch & PR

- Branch: `p6/P6-B003-kev-source-licence-unspecified`
- PR title: `P6-B003: Kev-4B/9B bake-off challenger has no source, licence or serving notes anywhere`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-B003` run

## Progress log

- 2026-10-21 00:00 · planner · created
