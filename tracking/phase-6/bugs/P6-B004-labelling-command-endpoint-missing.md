---
id: P6-B004
kind: gap
title: Labelling queue: `models.label.add` and a labels endpoint are missing from the API contract; D10 tab list omits the queue
phase: 6
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.13, R6.40]
roadmap_todos: []
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p6/P6-B004-labelling-command-endpoint-missing
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/dashboards/D10-models-memory.md]
doc_sync_status: done
found_in: docs/02-v1-architecture.md §7.1–§7.2; docs/ui/dashboards/D10-models-memory.md
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-B004 · Labelling queue: `models.label.add` and a labels endpoint are missing from the API contract; D10 tab list omits the queue

## Goal / expected outcome

The docs agree and are specific enough to build from: 02 §7 lists `models.label.add` (C0) and `GET /models/labels`, `/models/labels/queue`; D10 header lists the Labelling queue tab; Bake-off text includes Kev.

## Context & references

- Found in: docs/02-v1-architecture.md §7.1–§7.2; docs/ui/dashboards/D10-models-memory.md
- [02 §7.1](../../../docs/02-v1-architecture.md#71-queries-rest-read) · [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) · [D10](../../../docs/ui/dashboards/D10-models-memory.md) (Additions: `models.label.add` C0; route lists six tabs only)
- Affects: P6-T019, P6-T043

## Requirements

- **Steps to reproduce:** read docs/02-v1-architecture.md §7.1–§7.2; docs/ui/dashboards/D10-models-memory.md and compare it with the cross-referenced sections listed under Context.
- **Expected:** 02 §7 lists `models.label.add` (C0) and `GET /models/labels`, `/models/labels/queue`; D10 header lists the Labelling queue tab; Bake-off text includes Kev.
- **Actual:** D10 'Additions' defines `models.label.add` (C0) and a Labelling queue tab, but 02 §7.2's command catalogue has no `models.label.add`, 02 §7.1 has no labels/queue query, D10's route header lists tabs without Labelling queue, and D10's Bake-off tab text omits Kev.
- **Suggested fix:** Add them as specified in P6-T019; update D10 header and Bake-off row.
- **Impact:** API drift between UI spec and contract (severity S3)

## ToDo

- [x] Decision recorded in docs/17 (17 §D P6-B004/P6-B014): add the labels endpoint/command and the D10 queue tab
- [x] Owning docs carry it: 02 §7.1 (`/models/labels`, `/models/labels/queue`); 02 §7.2 (`models.label.add` C0); D10 route tab list (Labelling queue) and Bake-off row (Kev, only if a public licence-compatible release exists); roadmap R6.40
- [x] Affected tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P4-T062 (table + command), P6-T019 (queue API), P6-T043 (D10 tab)
- [x] Decision and source noted in the progress log

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (02 §7.1 (`/models/labels`, `/models/labels/queue`); 02 §7.2 (`models.label.add` C0); D10 route tab list (Labelling queue) and Bake-off row (Kev, only if a public licence-compatible release exists); roadmap R6.40)
- [x] Affected tasks consistent with it (P4-T062 (table + command), P6-T019 (queue API), P6-T043 (D10 tab))
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- Until resolved, dependent tasks use the conservative interpretation stated under Suggested fix and note it in their progress log.

## Cardinal rules (do NOT)

- Do NOT silently pick a number in code; record the decision in the doc first.
- Do NOT edit docs owned by another phase's planner from a P6 branch without the owner's agreement; propose the change in the PR description.

## Doc sync on completion

- `docs/02-v1-architecture.md`: resolve the inconsistency.
- `docs/ui/dashboards/D10-models-memory.md`: resolve the inconsistency.

## Branch & PR

- Branch: `p6/P6-B004-labelling-command-endpoint-missing`
- PR title: `P6-B004: Labelling queue: `models.label.add` and a labels endpoint are missing from the API contract; D10 tab list omits the queue`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-B004` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · resolved by docs/17 §D P6-B004/P6-B014: add the labels endpoint/command and the D10 queue tab. Docs now carry it: 02 §7.1 (`/models/labels`, `/models/labels/queue`); 02 §7.2 (`models.label.add` C0); D10 route tab list (Labelling queue) and Bake-off row (Kev, only if a public licence-compatible release exists); roadmap R6.40. Implementation owned by P4-T062 (table + command), P6-T019 (queue API), P6-T043 (D10 tab). Root cause: D10 defined the command and tab before the API catalogue was updated.
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P6-B004); docs updated: 02 §7.1 /models/labels + /models/labels/queue, 02 §7.2 models.label.add (C0), D10 route tabs + Bake-off row, roadmap R6.40; implementation owned by P4-T062, P6-T019, P6-T043
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · doc sync done: docs already updated in this wave
