---
id: P4-B010
kind: gap
title: SemIf 'shared-prefix mode' conflicts with 'prefix caching off'; no stage-1 latency target
phase: 4
type: DOC
status: backlog
priority: high
size: XS
severity: S2
owner: agent
claimed_by: ""
depends_on: []
requirements: [R4.12]
roadmap_todos: []
modules: [M21]
dashboards: [D10]
branch: p4/P4-B010-semif-shared-prefix-vs-determinism
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/02-v1-architecture.md]
doc_sync_status: n/a
found_in: docs/10-memory-rag-and-models.md §4.3 (Stage 1 vs Determinism controls); docs/02-v1-architecture.md §9.2
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-B010 · SemIf 'shared-prefix mode' conflicts with 'prefix caching off'; no stage-1 latency target

## Goal / expected outcome

10 §4.3 states which questions may use shared-prefix evaluation (if any) and under what precision, and 02 §9.2 has a stage-1 SemIf latency target, so P4-T029/T053 have unambiguous pass criteria.

## Context & references

- Found in: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) Stage 1 'shared-prefix mode for many criteria per document' vs Determinism 'Prefix caching: off on the decision path (SemIf saw 5–6/777 flips from prefix reuse in BF16)'
- [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos) tier B p95 < 50 ms applies to the P6 0.6B head only
- Related: P4-T009, P4-T029, P4-T053.

## Requirements

- **Steps to reproduce:** read both bullets in 10 §4.3.
- **Expected:** e.g. 'prefix reuse allowed only for flag questions in FP32 with flip-rate monitoring; never for `veto` or any score that feeds tier A'; plus a stage-1 target (e.g. relevance p95 ≤ 1 s/doc on GPU, measured on CPU).
- **Actual:** contradictory guidance; no target.
- **Impact:** S2 — determinism (backtest reproducibility) vs throughput is undecided for the main P4 model path.
- **Suggested fix:** decide and document; P4-T029 defaults to prefix caching **off** until decided.

## ToDo

- [ ] Agree the fix with the doc owner (main agent / user)
- [ ] Edit the listed docs (outside this phase folder; done by whoever owns those docs)
- [ ] Re-run `./kanban validate` and link the commit here

## Verification

### Tests
- Doc review: the corrected section is consistent with the linked sources (links resolve).

### Scenarios
- Given prefix caching stays off, then throughput is lower (~2.3 docs/s for 21 criteria on a 3090 per research) and the relevance-only CPU mode applies.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Docs updated as described under Requirements
- [ ] Root cause noted in the progress log

## Exceptions & edge cases

- None.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md`: §4.3 reconcile
- `docs/02-v1-architecture.md`: §9.2 stage-1 SLO row

## Branch & PR

- Branch: `p4/P4-B010-semif-shared-prefix-vs-determinism`
- PR title: `P4-B010: fix semIf 'shared-prefix mode' conflicts with 'prefix caching off'; no stage-1 latency target`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-B010` run

## Progress log

- 2026-10-21 00:00 · planner · opened
