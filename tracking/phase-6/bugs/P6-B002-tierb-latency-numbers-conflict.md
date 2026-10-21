---
id: P6-B002
kind: gap
title: Tier B GPU latency numbers conflict (03 §2 says ~150–300 ms; 10/03 M21/SPEC say ~2–12 ms; SLO p95 < 50 ms)
phase: 6
type: DOC
status: backlog
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
branch: p6/P6-B002-tierb-latency-numbers-conflict
pr: ""
doc_sync: [docs/03-build-spec.md]
doc_sync_status: n/a
found_in: docs/03-build-spec.md §2 (GPU row)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- [ ] Confirm with measured numbers from P6-T058.
- [ ] Propose the 03 §2 wording.
- [ ] Update the docs listed under Doc sync and link the resolving commit here.

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] 03 §2 consistent with 10 §4.3 and 02 §9.2.
- [ ] Root cause noted in the progress log.

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
