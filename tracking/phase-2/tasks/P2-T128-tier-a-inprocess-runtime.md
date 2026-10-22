---
id: P2-T128
kind: task
title: Tier A in-process runtime loader and latency histogram
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T127, P2-T120, P2-T003, P2-T009, P2-T018]
requirements: [R2.47, R2.N1]
roadmap_todos: [T2.30]
modules: [M21, M0]
dashboards: [D03, D01]
tools: [uv]
mcp: []
env: []
services: []
branch: p2/P2-T128-tier-a-inprocess-runtime
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-T128 · Tier A in-process runtime loader and latency histogram

## Goal / expected outcome

`mt_models.tier_a.Runtime` loads a registered compiled model inside the Nautilus strategy process, builds the feature vector incrementally (M6 + cached tier-B flags from NATS KV `tierb_scores`), returns a calibrated edge per event in < 50 µs p99 and exports an in-process latency histogram.

## Context & references

- Roadmap: [R2.47, R2.N1](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.30 · benchmarked in P2-T162
- [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (in-process, no network hop; inputs M6 + cached tier B) · [02 F2 step 2](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [02 §9.2 SLO](../../../docs/02-v1-architecture.md#92-observability--slos)
- Prerequisites (`depends_on`): M0 strategy base classes (P2-T003, T2.20), ML-signal template slot (P2-T009, T2.21), fallback ladder rung 4 'model service down → rules only' (P2-T018, T2.22).

## Requirements

- Load by artefact hash from the registry at strategy start; verify hash, CPU features and feature-version compatibility; refuse to start on mismatch.
- Feature vector assembled from incremental M6 features (P2-T120) with a fixed column order from the model signature; missing tier-B flags (no tier B before P4) use declared defaults and set `tierb_missing=true`.
- Predict returns `Edge(prob, edge, model_version, latency_ns)`; no allocation on the hot path; GIL-free back-end call where possible.
- Prometheus histogram `mt_tier_a_predict_seconds` (buckets 5 µs → 1 ms) per strategy/model; exemplars with trace_id.
- Failure handling: load failure or predict exception → strategy reports `model_down`, which M11 maps to ladder rung 4 (no new entries, exits managed).
- Same runtime used in truth backtests (CPU, deterministic) so backtest and paper predictions match.

## ToDo

- [ ] Implement `mt_models/tier_a/runtime.py` with the three back-end loaders
- [ ] Feature-vector assembler bound to model signature; KV `tierb_scores` reader with staleness check
- [ ] Prometheus histogram + OpenTelemetry span attributes
- [ ] Integration into the ML-signal template hook (coordinate with part A T2.21)
- [ ] Tests + doc

## Verification

### Tests
- Unit: column-order mismatch detected at load.
- Integration: truth backtest and a paper replay produce identical predictions for the same events.
- Benchmark harness reused by P2-T162.

### Scenarios
- Given the model file is corrupted, when the engine starts the strategy, then it refuses to start, reports `model_down` and M11 holds the ladder at rung 4 for that strategy.
- Given NATS KV is unreachable, then tier-B inputs use defaults with `tierb_missing=true`, and predictions continue (tier A unaffected, 02 §9.3).

### Stress / failure injection
- Run predictions at 20k events/s for 10 min alongside the engine: p99 stays < 50 µs, no memory growth.

## Acceptance criteria

- [ ] Model loads in-process and predicts with p99 < 50 µs on the reference host
- [ ] Histogram exported
- [ ] Failure maps to `model_down`
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Hot-swap of a model version only at a strategy restart (no mid-session swap in P2).
- GPU unavailable: irrelevant — tier A is CPU only.

## Cardinal rules (do NOT)

- Do NOT add a network call (gateway, decision-svc, HTTP) to the tier-A predict path.
- Do NOT let a model error open new positions.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: runtime contract.
- `docs/02-v1-architecture.md` §9.2: histogram name.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.30 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T128-tier-a-inprocess-runtime`
- PR title: `P2-T128: Tier A in-process runtime loader and latency histogram`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T128` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (Part A prerequisites made explicit dependencies)
