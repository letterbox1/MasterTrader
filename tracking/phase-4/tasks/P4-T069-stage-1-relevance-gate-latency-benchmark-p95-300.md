---
id: P4-T069
kind: task
title: Stage-1 relevance-gate latency benchmark (p95 300 ms GPU / 3 s CPU, off the order path)
phase: 4
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T029, P4-T030, P4-T009]
requirements: [R4.N2, R4.12]
roadmap_todos: [T4.67]
modules: [M21, M2]
dashboards: [D10, D07]
tools: [uv, git]
mcp: []
env: []
services: [decision-svc, nats, postgres, mlflow]
branch: p4/P4-T069-stage-1-relevance-gate-latency-benchmark-p95-300
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/02-v1-architecture.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P4-T069 · Stage-1 relevance-gate latency benchmark (p95 300 ms GPU / 3 s CPU, off the order path)

## Goal / expected outcome

A reproducible benchmark shows the stage-1 SemIf relevance gate meets **p95 ≤ 300 ms per document on GPU and ≤ 3 s on CPU** on this host with the decision-path settings (prefix caching off, fixed batch), that documents are queued, and that no order-path code calls it, so a slow or dead gate can never delay an order.

## Context & references

- Roadmap: [R4.N2](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.67](../../../docs/roadmap/phase-4-intel.md#4-todo-sets) · [R4.12](../../../docs/roadmap/phase-4-intel.md#3-requirements)
- Decision: [17 §A](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (P4-B010) · [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (latency target; prefix caching off on the decision path) · [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos) (stage-1 gate SLO row)
- Related: P4-T009 (serving), P4-T029 (readout, latency histograms), P4-T030 (gate), P4-T053 (flip rate), P4-T058 (decision-svc outage).

## Requirements

- Workload: 1,000 documents sampled from the corpus (fixed seed), realistic length mix; relevance question only; decision-path settings (prefix caching off, fixed batch, pinned revision).
- Measure per-document latency from enqueue to `dec.tierb.relevance.*` publish: p50/p95/p99 on GPU (if present) and CPU profiles; targets are configurable defaults (300 ms / 3 s).
- Queueing: at 2× the observed daily peak arrival rate, the queue stays bounded and drains; `nlp` never blocks on the gate.
- Order-path isolation: a static import check plus a runtime test prove that `mt_risk`/`mt_engine` order handling never calls decision-svc synchronously; killing decision-svc changes no pre-trade latency (P2 p99 budget holds).
- Results in MLflow and summarised in 10 §4.3; a miss on GPU files a bug and keeps stage-1 relevance-only until fixed.

## ToDo

- [ ] Benchmark harness `tools/bench/semif_latency.py` (fixed seed, warm-up, percentiles)
- [ ] Run GPU and CPU profiles; record in MLflow
- [ ] Queue test at 2× peak arrival
- [ ] Order-path isolation checks (static + runtime with decision-svc stopped)
- [ ] Publish the summary; update docs listed under Doc sync

## Verification

### Tests
- Harness unit tests (percentile maths, fixed-seed sampling).
- Static check: no decision-svc client import from order-path modules.
- Runtime: pre-trade latency p99 unchanged with decision-svc stopped (compared with the P2 benchmark).

### Scenarios
- Given CPU-only hardware, then the CPU target (≤ 3 s) is the pass criterion and stage-1 stays relevance-only.
- Given p95 exceeds the target, then the result is recorded, a bug is filed, and the gate keeps its keyword fallback for overflow.

### Stress / failure injection
- 2× peak arrival burst for 30 min: bounded queue, no dropped documents, latency recorded under load.

## Acceptance criteria

- [ ] p95 ≤ 300 ms (GPU) and/or ≤ 3 s (CPU) recorded on this host with decision-path settings
- [ ] Queue bounded and drained under 2× peak
- [ ] Order-path isolation proven (static + runtime)
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- No GPU yet (P0 T0.01): run CPU now; re-run the GPU profile when the GPU arrives.
- Backend upgrade: re-run this benchmark in the upgrade PR.

## Cardinal rules (do NOT)

- Do NOT enable prefix caching or shared-prefix mode to hit the target.
- Do NOT put any tier-B call on the order path.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md`: §4.3: measured stage-1 latency on this host
- `docs/02-v1-architecture.md`: §9.2: confirm the stage-1 gate SLO row with the measured value
- `docs/roadmap/phase-4-intel.md`: tick T4.67

## Branch & PR

- Branch: `p4/P4-T069-stage-1-relevance-gate-latency-benchmark-p95-300`
- PR title: `P4-T069: Stage-1 relevance-gate latency benchmark (p95 300 ms GPU / 3 s CPU, off the order path)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T069` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (R4.N2 / T4.67 per 17 §A P4-B010)
