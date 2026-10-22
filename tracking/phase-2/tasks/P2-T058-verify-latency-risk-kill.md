---
id: P2-T058
kind: task
title: "Latency benchmarks: pre-trade risk check and kill-to-cancels"
phase: 2
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T017, P2-T031, P2-T047, P2-T070]
requirements: [R2.N1]
roadmap_todos: [T2.66]
modules: [M11]
dashboards: []
tools: [uv]
mcp: []
env: []
services: []
branch: p2/P2-T058-verify-latency-risk-kill
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T058 · Latency benchmarks: pre-trade risk check and kill-to-cancels

## Goal / expected outcome

Reproducible benchmarks on the host show pre-trade risk check p99 < 1 ms and kill → all cancels sent < 1 s, with CI regression guards; tier-A and signal→order benchmarks are P2-T162's share of T2.66.

## Context & references

- Roadmap: [R2.N1](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.66 (risk + kill part)
- SLO: [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos)
- P2-T162: tier A p99 < 50 µs, signal → order p99 < 5 ms.
- The pre-trade check includes the inline safety-state checks (P2-T070) and the layer merge (P2-T069) in the measured path.

## Requirements

- Risk check: pytest-benchmark + in-engine histogram under realistic policy size (50 venues × 200 strategies × 1,000 instruments) and load (1k intents/s), p99 < 1 ms on the host.
- Kill: from P2-T054 drill metrics, p100 of cancels-sent < 1 s with 100 open orders across 3 venues.
- CI guard: benchmark regression > 20% vs stored baseline fails (on the self-hosted runner).

## ToDo

- [ ] Benchmark harness + baseline file
- [ ] Run on host, record numbers
- [ ] CI regression job
- [ ] Record results (numbers, run IDs, screenshots) in the progress log and tick the roadmap ToDo box

## Verification

### Tests
- Benchmarks themselves.

### Scenarios
- Given a PR adds an O(n) scan in the gate, when CI benchmarks run, then the regression guard fails.

### Stress / failure injection
- Run risk benchmark with 4 strategies' worth of concurrent intents and GC pressure; p99 still < 1 ms.

## Acceptance criteria

- [ ] Risk check p99 < 1 ms recorded
- [ ] Kill < 1 s recorded
- [ ] Regression guard active

## Exceptions & edge cases

- Shared host noise: pin the benchmark to isolated cores (`taskset`) and report environment.

## Cardinal rules (do NOT)

- Do NOT measure on a laptop and claim the SLO; use the host.
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/02-v1-architecture.md` §9.2: measured values next to targets.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.66 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T058-verify-latency-risk-kill`
- PR title: `P2-T058: Latency benchmarks: pre-trade risk check and kill-to-cancels`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T058` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (benchmark includes safety-state checks and layer merge; Part B links)
