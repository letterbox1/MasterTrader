---
id: P6-T058
kind: task
title: Stress: tier B p95 < 50 ms on GPU and degraded CPU behaviour
phase: 6
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T024, P6-T023]
requirements: [R6.11]
roadmap_todos: [T6.61]
modules: [M21]
dashboards: [D10]
branch: p6/P6-T058-verify-tierb-latency-slo
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/02-v1-architecture.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T058 · Stress: tier B p95 < 50 ms on GPU and degraded CPU behaviour

## Goal / expected outcome

A load test proves the tier-B SLO (p95 < 50 ms per decision, GPU, 0.6B head) at realistic and burst rates, and characterises the CPU ONNX fallback so the GPU-unavailable mode is known.

## Context & references

- Roadmap: [R6.11](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.61
- SLO: [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos) · [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (expected ~2–12 ms GPU; 100–400 ms CPU int8 est.)
- Gap: P6-B002
- Depends on (this phase): P6-T024, P6-T023

## Requirements

- Load profiles: steady (news rate × questions), burst (100 `text.doc.new` in 1 s), sustained 1 h.
- Measure p50/p95/p99, queue depth, GPU memory, errors; batch=1 determinism settings on.
- CPU mode: same profiles; record latencies and which questions should be disabled on CPU.
- Tier A unaffected (its p99 < 50 µs reading KV) during the test.

## ToDo

- [ ] k6/locust script against decision-svc.
- [ ] Run profiles on the host; capture Grafana snapshots.
- [ ] Write results + CPU-mode question list.

## Verification

### Tests
- Load script committed; smoke version in CI.

### Scenarios
- Given burst load, then p95 stays < 50 ms or excess is queued without dropping decisions.

### Stress / failure injection
- GPU removed mid-test: fallback to CPU within 30 s; no crashed requests.

## Acceptance criteria

- [ ] p95 < 50 ms on GPU documented.
- [ ] CPU fallback numbers documented.

## Exceptions & edge cases

- No GPU on the host: SLO can't be met; record and keep SemIf/slow flags only (exit criterion 3 still satisfiable by keeping SemIf).

## Cardinal rules (do NOT)

- Do NOT disable determinism controls to hit the SLO.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: measured latency.
- `docs/02-v1-architecture.md` §9.2: confirm SLO.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.61 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T058-verify-tierb-latency-slo`
- PR title: `P6-T058: Stress: tier B p95 < 50 ms on GPU and degraded CPU behaviour`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T058` run

## Progress log

- 2026-10-21 00:00 · planner · created
