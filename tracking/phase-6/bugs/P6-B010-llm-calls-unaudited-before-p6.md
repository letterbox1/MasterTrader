---
id: P6-B010
kind: gap
title: LLM calls from P2–P5 (leakage review, SemIf-adjacent jobs, morning brief) run before the `audit.llm_call` writer lands in P6
phase: 6
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p6/P6-B010-llm-calls-unaudited-before-p6
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: done
found_in: docs/roadmap/phase-0-foundations.md R0.07/R0.09 vs docs/roadmap/phase-6-ai-models-treasury.md R6.03
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Decision recorded in docs/17 (17 §D P6-B010): `audit.llm_call` is written from P0 via the LiteLLM callback; P6 only extends it (prompt registry, training cutoff)
- [x] Owning docs carry it: 10 §5 (Audit from P0); 03 M8 and §7; 15 §2 audit list; roadmap R6.03 (R0.13) and T6.31; 04 Phase 6 'Evaluation and cost'
- [x] Affected tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P0-T042 (writer), P0-T031 (table), P6-T005 (extension, T6.31), P6-T052 (audit check)
- [x] Decision and source noted in the progress log

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (10 §5 (Audit from P0); 03 M8 and §7; 15 §2 audit list; roadmap R6.03 (R0.13) and T6.31; 04 Phase 6 'Evaluation and cost')
- [x] Affected tasks consistent with it (P0-T042 (writer), P0-T031 (table), P6-T005 (extension, T6.31), P6-T052 (audit check))
- [x] Root cause noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by docs/17 §D P6-B010: `audit.llm_call` is written from P0 via the LiteLLM callback; P6 only extends it (prompt registry, training cutoff). Docs now carry it: 10 §5 (Audit from P0); 03 M8 and §7; 15 §2 audit list; roadmap R6.03 (R0.13) and T6.31; 04 Phase 6 'Evaluation and cost'. Implementation owned by P0-T042 (writer), P0-T031 (table), P6-T005 (extension, T6.31), P6-T052 (audit check). Root cause: the audit writer was scheduled with the agents instead of with the gateway.
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P6-B010); docs updated: 10 §5 audit from P0, 03 M8/§7, 15 §2 audit list, roadmap R6.03/T6.31 (R0.13), 04 Phase 6; implementation owned by P0-T042, P0-T031, P6-T005, P6-T052
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · doc sync done: docs already updated in this wave
