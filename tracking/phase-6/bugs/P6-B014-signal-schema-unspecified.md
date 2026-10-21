---
id: P6-B014
kind: gap
title: `Signal` fields are not specified in any doc (only 'structured Signal with provenance')
phase: 6
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.01]
roadmap_todos: []
modules: []
dashboards: []
branch: p6/P6-B014-signal-schema-unspecified
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md]
doc_sync_status: n/a
found_in: docs/03-build-spec.md M8; docs/02-v1-architecture.md §5.3
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-B014 · `Signal` fields are not specified in any doc (only 'structured Signal with provenance')

## Goal / expected outcome

The docs agree and are specific enough to build from: 03 M8 (or 02 §5.3) lists the Signal fields and provenance structure.

## Context & references

- Found in: docs/03-build-spec.md M8; docs/02-v1-architecture.md §5.3
- [03 M8](../../../docs/03-build-spec.md#m8-ai-decision-layer--mt_agents) · [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) · [D09](../../../docs/ui/dashboards/D09-agents.md) (implies direction, probability/conviction, horizon, provenance)
- Affects: P6-T004, P6-T016

## Requirements

- **Steps to reproduce:** read docs/03-build-spec.md M8; docs/02-v1-architecture.md §5.3 and compare it with the cross-referenced sections listed under Context.
- **Expected:** 03 M8 (or 02 §5.3) lists the Signal fields and provenance structure.
- **Actual:** The core output of the AI layer has no field list; D09 implies some fields, `mt_core` (P0 T0.21) defines a v1 type without a spec.
- **Suggested fix:** Adopt the field list in P6-T004 as the spec.
- **Impact:** Consumers (strategies, D09, distillation) could disagree (severity S3)

## ToDo

- [ ] Copy the P6-T004 field list into 03 M8 when merged.
- [ ] Update the docs listed under Doc sync and link the resolving commit here.

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Field list documented.
- [ ] Root cause noted in the progress log.

## Exceptions & edge cases

- Until resolved, dependent tasks use the conservative interpretation stated under Suggested fix and note it in their progress log.

## Cardinal rules (do NOT)

- Do NOT silently pick a number in code; record the decision in the doc first.
- Do NOT edit docs owned by another phase's planner from a P6 branch without the owner's agreement; propose the change in the PR description.

## Doc sync on completion

- `docs/03-build-spec.md`: resolve the inconsistency.
- `docs/02-v1-architecture.md`: resolve the inconsistency.

## Branch & PR

- Branch: `p6/P6-B014-signal-schema-unspecified`
- PR title: `P6-B014: `Signal` fields are not specified in any doc (only 'structured Signal with provenance')`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-B014` run

## Progress log

- 2026-10-21 00:00 · planner · created
