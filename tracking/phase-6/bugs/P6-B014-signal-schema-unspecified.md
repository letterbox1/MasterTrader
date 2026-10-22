---
id: P6-B014
kind: gap
title: `Signal` fields are not specified in any doc (only 'structured Signal with provenance')
phase: 6
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p6/P6-B014-signal-schema-unspecified
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md]
doc_sync_status: done
found_in: docs/03-build-spec.md M8; docs/02-v1-architecture.md §5.3
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Decision recorded in docs/17 (17 §D P6-B004/P6-B014): `Signal` fields defined in 03 M8: id, ts, as_of, instrument, horizon, direction, edge, calibrated confidence, rationale summary, sources[], model/prompt versions, run id
- [x] Owning docs carry it: 03 M8 Output; 02 §4 M8 row and §5.1 `audit.signal`; roadmap R6.01 and T6.20; 04 Phase 6 M8 bullet
- [x] Affected tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P6-T004 (schema), P6-T067 (sample-run field check, T6.66)
- [x] Decision and source noted in the progress log

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (03 M8 Output; 02 §4 M8 row and §5.1 `audit.signal`; roadmap R6.01 and T6.20; 04 Phase 6 M8 bullet)
- [x] Affected tasks consistent with it (P6-T004 (schema), P6-T067 (sample-run field check, T6.66))
- [x] Root cause noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by docs/17 §D P6-B004/P6-B014: `Signal` fields defined in 03 M8: id, ts, as_of, instrument, horizon, direction, edge, calibrated confidence, rationale summary, sources[], model/prompt versions, run id. Docs now carry it: 03 M8 Output; 02 §4 M8 row and §5.1 `audit.signal`; roadmap R6.01 and T6.20; 04 Phase 6 M8 bullet. Implementation owned by P6-T004 (schema), P6-T067 (sample-run field check, T6.66). Root cause: the core AI output had no field list.
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P6-B004/P6-B014); docs updated: 03 M8 Output fields, 02 §4/§5.1 audit.signal, roadmap R6.01/T6.20, 04 Phase 6; implementation owned by P6-T004, P6-T067
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · doc sync done: docs already updated in this wave
