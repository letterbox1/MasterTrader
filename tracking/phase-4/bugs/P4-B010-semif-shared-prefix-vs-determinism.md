---
id: P4-B010
kind: gap
title: SemIf 'shared-prefix mode' conflicts with 'prefix caching off'; no stage-1 latency target
phase: 4
type: DOC
status: done
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
doc_sync_status: done
found_in: docs/10-memory-rag-and-models.md §4.3 (Stage 1 vs Determinism controls); docs/02-v1-architecture.md §9.2
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
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

- [x] Decision recorded: decision path = prefix caching off + fixed batch; shared-prefix mode only for offline/backfill scoring, marked non-deterministic, never used for decisions or backtests; stage-1 gate p95 ≤ 300 ms GPU / ≤ 3 s CPU, queued, never on the order path (17 §A)
- [x] Docs carry it: 10 §4.3 stage 1 (prefix caching, shared-prefix, latency target) and determinism controls; 02 §3.2 decision-svc row; 02 §9.2 'Stage-1 relevance gate (nlp)' SLO row; roadmap R4.12, R4.N2, T4.67
- [x] Implementation owned by P4-T009 (serving profiles), P4-T029 (readout, offline mode tagging), P4-T030 (queued gate), P4-T053 (flip rate), P4-T069 (latency benchmark, new)

## Verification

### Tests
- Doc review: the corrected section is consistent with the linked sources (links resolve).

### Scenarios
- Given prefix caching stays off, then throughput is lower (~2.3 docs/s for 21 criteria on a 3090 per research) and the relevance-only CPU mode applies.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Determinism vs throughput and the stage-1 latency target are documented (checked in 10 §4.3 and 02 §9.2, 2026-10-22)
- [x] Root cause noted: 10 §4.3 copied SemIf's shared-prefix trick without reconciling it with the determinism rule

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
- 2026-10-22 00:00 · aligner · resolved by 17 §A (P4-B010); docs checked: 10 §4.3 (stage 1 + determinism controls), 02 §3.2 decision-svc row, 02 §9.2 stage-1 SLO row, roadmap R4.12/R4.N2/T4.67; implementation owned by P4-T009, P4-T029, P4-T030, P4-T053, P4-T069; root cause: research note's shared-prefix mode conflicted with the determinism rule
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 §A (P4-B010); docs updated: 10 §4.3 stage 1 + determinism controls, 02 §3.2 decision-svc row, 02 §9.2 stage-1 SLO row, roadmap R4.12/R4.N2/T4.67; implementation owned by P4-T009, P4-T029, P4-T030, P4-T053, P4-T069
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
