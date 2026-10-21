---
id: P6-B015
kind: gap
title: Tier-B promotion/abstention/veto thresholds have no numbers (target precision, ECE max, flip-rate max, veto precision)
phase: 6
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.10, R6.14]
roadmap_todos: []
modules: []
dashboards: []
branch: p6/P6-B015-model-gate-thresholds-undefined
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md]
doc_sync_status: n/a
found_in: docs/10-memory-rag-and-models.md §4.3; docs/03-build-spec.md M21
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-B015 · Tier-B promotion/abstention/veto thresholds have no numbers (target precision, ECE max, flip-rate max, veto precision)

## Goal / expected outcome

The docs agree and are specific enough to build from: documented defaults (user-editable) for each threshold.

## Context & references

- Found in: docs/10-memory-rag-and-models.md §4.3; docs/03-build-spec.md M21
- [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) ('target precision', 'calibrated high-precision threshold') · [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models)
- Affects: P6-T022, P6-T026, P6-T030, P6-T057

## Requirements

- **Steps to reproduce:** read docs/10-memory-rag-and-models.md §4.3; docs/03-build-spec.md M21 and compare it with the cross-referenced sections listed under Context.
- **Expected:** documented defaults (user-editable) for each threshold.
- **Actual:** Docs require abstention 'at a target precision', veto 'above a calibrated high-precision threshold' and promotion 'via gates', but give no default numbers for precision targets, ECE/Brier limits, flip-rate limit or shadow duration.
- **Suggested fix:** Proposed defaults (used by P6 tasks until decided): target precision 0.75, veto precision 0.90, ECE ≤ 0.05, flip rate ≤ 0.1%, shadow ≥ 14 days, worst fold ≥ frozen baseline.
- **Impact:** Gates could be set arbitrarily per implementer (severity S3)

## ToDo

- [ ] Confirm defaults with the user.
- [ ] Document them in 10 §4.3.
- [ ] Update the docs listed under Doc sync and link the resolving commit here.

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Defaults documented.
- [ ] Root cause noted in the progress log.

## Exceptions & edge cases

- Until resolved, dependent tasks use the conservative interpretation stated under Suggested fix and note it in their progress log.

## Cardinal rules (do NOT)

- Do NOT silently pick a number in code; record the decision in the doc first.
- Do NOT edit docs owned by another phase's planner from a P6 branch without the owner's agreement; propose the change in the PR description.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md`: resolve the inconsistency.

## Branch & PR

- Branch: `p6/P6-B015-model-gate-thresholds-undefined`
- PR title: `P6-B015: Tier-B promotion/abstention/veto thresholds have no numbers (target precision, ECE max, flip-rate max, veto precision)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-B015` run

## Progress log

- 2026-10-21 00:00 · planner · created
