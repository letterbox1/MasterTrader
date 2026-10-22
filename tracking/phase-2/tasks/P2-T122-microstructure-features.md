---
id: P2-T122
kind: task
title: Microstructure features from ticks and L2
phase: 2
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T120]
requirements: [R2.46]
roadmap_todos: [T2.29]
modules: [M6]
dashboards: [D03]
tools: [uv]
mcp: []
env: []
services: []
branch: p2/P2-T122-microstructure-features
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T122 · Microstructure features from ticks and L2

## Goal / expected outcome

Order-flow imbalance, spread, depth, trade intensity and related microstructure features computed from recorded ticks/L2 (batch) and live book/trade events (incremental), usable by scalping templates and tier A.

## Context & references

- Roadmap: [R2.46](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.29
- [03 M6 microstructure](../../../docs/03-build-spec.md#m6-features--mt_features) · data from P1 Parquet recorder ([phase 1](../../../docs/roadmap/phase-1-data-and-monitoring.md) T1.21)

## Requirements

- Features: OFI (Cont et al.) at levels 1/5/10, quoted and effective spread (bps), depth at ±10/25/50 bps, book imbalance, trade intensity (trades/s), signed volume, micro-price, realised vol (1s/1m).
- Incremental update from book deltas ≤ 20 µs median per event (Rust/numba allowed) so they can feed tier A in-process.
- Batch from the Parquet catalog for the same windows; parity harness passes.
- Book integrity: if the book is flagged bad by M16, features publish `None` with `dq=bad`.

## ToDo

- [ ] Implement `mt_features/micro.py` (numba-accelerated incremental + batch)
- [ ] Register features; parity tests on a recorded L2 fixture
- [ ] Micro-benchmark for per-event update
- [ ] Doc

## Verification

### Tests
- Parity on a 1-hour recorded BTC L2 fixture.
- Unit: OFI sign correct on synthetic bid/ask events.
- Benchmark: per-event update latency.

### Scenarios
- Given a crossed or stale book flagged by M16, then microstructure features stop publishing values (`dq=bad`) and tier A treats them as missing.

### Stress / failure injection
- Replay a high-activity hour (≥ 50k book events/min): incremental update keeps up in real time on one core.

## Acceptance criteria

- [ ] Microstructure features registered with parity
- [ ] Per-event median ≤ 20 µs
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Venues without L2 recording: depth features unavailable; manifest validation flags strategies that need them.
- Sequence gaps in book deltas: rebuild from snapshot; features suppressed until resynced.

## Cardinal rules (do NOT)

- Do NOT compute features on a book flagged bad by M16.
- Do NOT read research/backtest data except through `mt_store.pit(as_of=…)`; the `pit` CI bypass test must stay green.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M6: microstructure list.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.29 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T122-microstructure-features`
- PR title: `P2-T122: Microstructure features from ticks and L2`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T122` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields (no decision change))
