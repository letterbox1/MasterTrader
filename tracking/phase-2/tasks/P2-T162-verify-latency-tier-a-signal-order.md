---
id: P2-T162
kind: task
title: Verify latency: tier A p99 < 50 µs and signal → order p99 < 5 ms
phase: 2
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T128]
requirements: [R2.N1, R2.47]
roadmap_todos: [T2.66]
modules: [M21, M12, M0]
dashboards: [D01]
branch: p2/P2-T162-verify-latency-tier-a-signal-order
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/10-memory-rag-and-models.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T162 · Verify latency: tier A p99 < 50 µs and signal → order p99 < 5 ms

## Goal / expected outcome

Measured evidence on the production host that a tier-A model trained → calibrated → compiled through the P2 pipeline predicts in-process with p99 < 50 µs, and that strategy signal → order submitted (`auto`/paper path, excluding venue) is p99 < 5 ms. The pre-trade risk p99 < 1 ms and kill → cancels < 1 s benchmarks are part A's (T2.60/T2.61).

## Context & references

- Roadmap: [R2.N1, R2.47](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.66 (shared with part A for the risk-check benchmark)
- [02 §9.2 SLOs](../../../docs/02-v1-architecture.md#92-observability--slos) · [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design)
- Part-A prerequisites: engine trace spans signal → `ord.intent` → M11 → submit (T2.25), Grafana SLO panels (T2.42) in part A (P2-T001–T099)

## Requirements

- Pipeline E2E: run P2-T125 → T126 → T127 on a fixture strategy; load via P2-T128 into the ML-signal template on paper.
- Tier A: ≥ 1,000,000 predictions, single-row, in the engine process under realistic background load; report p50/p99/p99.9 from `mt_tier_a_predict_seconds`; pass p99 < 50 µs.
- Signal → order: ≥ 10,000 signals on paper across ≥ 3 instruments; OpenTelemetry spans from signal emit to submit call (venue excluded); pass p99 < 5 ms.
- Benchmark script committed (`tests/perf/`) and runnable on demand; results attached to the progress log and Grafana snapshot.

## ToDo

- [ ] Write `tests/perf/tier_a_bench.py` and `signal_to_order_bench.py`
- [ ] Run on the host (not a laptop) with the engine up
- [ ] Capture histograms + Grafana snapshot
- [ ] File bug items for any SLO miss

## Verification

### Tests
- Perf benchmarks above; regression thresholds recorded for a nightly perf job.

### Scenarios
- Given 4 cores busy with backtest jobs, then tier-A p99 is still < 50 µs (engine pinned to dedicated cores) — or the CPU pinning gap is filed.
- Given a model 2× larger than budget, then the benchmark shows the miss and the registry marks it non-promotable (P2-T127).

### Stress / failure injection
- Background load: 2 backtest workers at 100% plus NATS at 5k msg/s during the benchmark.
- GC pressure: run with Python GC enabled and record pauses affecting p99.9.

## Acceptance criteria

- [ ] Tier A p99 < 50 µs on the host
- [ ] Signal → order p99 < 5 ms on paper (excl. venue)
- [ ] Benchmarks committed and results recorded

## Exceptions & edge cases

- Clock source: use `time.perf_counter_ns`/span timestamps from one host clock; no cross-host comparisons.

## Cardinal rules (do NOT)

- Do NOT benchmark on a different machine than the production host for the pass/fail result.
- Do NOT exclude slow samples from percentiles.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/02-v1-architecture.md` §9.2: measured values.
- `docs/10-memory-rag-and-models.md` §4.3: measured tier-A latency.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.66 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T162-verify-latency-tier-a-signal-order`
- PR title: `P2-T162: Verify latency: tier A p99 < 50 µs and signal → order p99 < 5 ms`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T162` run

## Progress log

- 2026-10-21 00:00 · planner · created
