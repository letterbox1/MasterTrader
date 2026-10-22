---
id: P6-B002
kind: gap
title: Tier B GPU latency numbers conflict (03 §2 says ~150–300 ms; 10/03 M21/SPEC say ~2–12 ms; SLO p95 < 50 ms)
phase: 6
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.11]
roadmap_todos: []
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p6/P6-B002-tierb-latency-numbers-conflict
pr: ""
doc_sync: [docs/03-build-spec.md]
doc_sync_status: done
found_in: docs/03-build-spec.md §2 (GPU row)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-B002 · Tier B GPU latency numbers conflict (03 §2 says ~150–300 ms; 10/03 M21/SPEC say ~2–12 ms; SLO p95 < 50 ms)

## Goal / expected outcome

The docs agree and are specific enough to build from: one set of tier-B latency expectations (GPU and CPU) matching the SLO.

## Context & references

- Found in: docs/03-build-spec.md §2 (GPU row)
- [03 §2](../../../docs/03-build-spec.md#2-target-environment) · [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) · [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models) · [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos) · [SPEC non-negotiables](../../../SPEC.md#non-negotiable-requirements)
- Affects: P6-T023, P6-T024, P6-T058

## Requirements

- **Steps to reproduce:** read docs/03-build-spec.md §2 (GPU row) and compare it with the cross-referenced sections listed under Context.
- **Expected:** one set of tier-B latency expectations (GPU and CPU) matching the SLO.
- **Actual:** 03 §2 'GPU (recommended)' row says a GPU makes tier B '~150–300 ms/decision' and without one 'seconds-scale'; 10 §4.3 / 03 M21 / SPEC say ~2–12 ms on GPU for 0.6B and 100–400 ms on CPU int8; 02 §9.2 sets p95 < 50 ms.
- **Suggested fix:** Change 03 §2 to '~2–12 ms per decision (0.6B, GPU); CPU ONNX hundreds of ms', citing 10 §4.3; keep the SLO p95 < 50 ms. Interim: build to the SLO.
- **Impact:** A developer could size hardware or timeouts wrongly (severity S3)

## ToDo

- [x] Decision recorded in docs/17 (17 §B P6-B002): tier B latency ~2–12 ms per decision on GPU (0.6B), p95 SLO < 50 ms, CPU 100–400 ms; the '150–300 ms' text is removed
- [x] Owning docs carry it: 03 §2 GPU row and Models row; 10 §4.3 expected latency; 02 §9.2 SLO table; roadmap R6.11 and R6.N3
- [x] Affected tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P6-T023, P6-T024 (serving), P6-T058 (benchmark, T6.71)
- [x] Decision and source noted in the progress log

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (03 §2 GPU row and Models row; 10 §4.3 expected latency; 02 §9.2 SLO table; roadmap R6.11 and R6.N3)
- [x] Affected tasks consistent with it (P6-T023, P6-T024 (serving), P6-T058 (benchmark, T6.71))
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- Until resolved, dependent tasks use the conservative interpretation stated under Suggested fix and note it in their progress log.

## Cardinal rules (do NOT)

- Do NOT silently pick a number in code; record the decision in the doc first.
- Do NOT edit docs owned by another phase's planner from a P6 branch without the owner's agreement; propose the change in the PR description.

## Doc sync on completion

- `docs/03-build-spec.md`: resolve the inconsistency.

## Branch & PR

- Branch: `p6/P6-B002-tierb-latency-numbers-conflict`
- PR title: `P6-B002: Tier B GPU latency numbers conflict (03 §2 says ~150–300 ms; 10/03 M21/SPEC say ~2–12 ms; SLO p95 < 50 ms)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-B002` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · resolved by docs/17 §B P6-B002: tier B latency ~2–12 ms per decision on GPU (0.6B), p95 SLO < 50 ms, CPU 100–400 ms; the '150–300 ms' text is removed. Docs now carry it: 03 §2 GPU row and Models row; 10 §4.3 expected latency; 02 §9.2 SLO table; roadmap R6.11 and R6.N3. Implementation owned by P6-T023, P6-T024 (serving), P6-T058 (benchmark, T6.71). Root cause: 03 §2 carried an old GPU estimate that predated the 0.6B classification-head design.
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P6-B002); docs updated: 03 §2 GPU/Models rows, 10 §4.3 expected latency, 02 §9.2 SLO table, roadmap R6.11/R6.N3; implementation owned by P6-T023, P6-T024, P6-T058
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · doc sync done: docs already updated in this wave
