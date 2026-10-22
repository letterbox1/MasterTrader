---
id: P4-T058
kind: task
title: Stress and failure injection for the intel pipeline
phase: 4
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T057, P4-T019, P4-T018]
requirements: [R4.06, R4.02, R4.12, R4.13]
roadmap_todos: []
modules: [M2, M21, M9]
dashboards: [D07, D08]
tools: [docker, uv, git]
mcp: []
env: []
services: [postgres, nats, rss-bridge, decision-svc, tei-embed]
branch: p4/P4-T058-verify-stress-failure-injection
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-4-intel.md]
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

# P4-T058 · Stress and failure injection for the intel pipeline

## Goal / expected outcome

Chaos runs prove degraded modes (02 §9.3) and the roadmap risks: source flood vs relevance gate, decision-svc/GPU down, TEI down, RSS-Bridge down, Postgres down, NATS restart, Telegram FLOOD_WAIT storm — each with the expected behaviour and recovery, and no data loss or Telegram leakage.

## Context & references

- Roadmap: §7 risks (volume vs gate, CPU-only SemIf) · [R4.06, R4.02, R4.12, R4.13](../../../docs/roadmap/phase-4-intel.md#3-requirements)
- Degraded modes: [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) · SLOs [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos)

## Requirements

- Flood: one source at 10× normal (e.g. 2,000 items/h): caps engage, gate queue bounded, D08 warns, other sources' latency p95 ≤ 2× baseline.
- decision-svc down 30 min: keyword fallback, 'Tier B unavailable' in UI, tier A unaffected, no order-path call waits (R4.N2), backlog drained after recovery.
- TEI down: docs stored without embeddings, backfilled on recovery.
- RSS-Bridge down: bridged sources stale; others unaffected.
- Postgres down 5 min: JetStream buffers; zero loss/duplicates after recovery.
- FLOOD_WAIT storm: join queue pauses; ingestion of joined channels continues.
- Telegram gate suite (P4-T050) re-run after chaos: still zero leaks.

## ToDo

- [ ] Chaos scripts in `ops/chaos/p4_*.sh` (docker pause/stop, tc netem latency).
- [ ] Assertions + metrics capture.
- [ ] Report for the exit demo.

## Verification

### Tests
- Each chaos script has pass/fail assertions.

### Scenarios
- Given NATS restarts mid-burst, then durable consumers resume without duplicates (idempotent writes by content hash).

### Stress / failure injection
- The whole task is stress/failure injection (see Requirements).

## Acceptance criteria

- [ ] All chaos scenarios pass with documented recovery times
- [ ] No loss, no duplicates, no Telegram leakage
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Disk-full on JetStream: alert and discard-oldest per stream policy; documented, not silent.

## Cardinal rules (do NOT)

- Do NOT run chaos against live trading accounts.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT touch live money (P7 gates); keys stay trade-only, IP-locked, withdrawals disabled.

## Doc sync on completion

- `docs/02-v1-architecture.md`: §9.3: add intel-pipeline degraded behaviours observed
- `docs/roadmap/phase-4-intel.md`: note the item in §7 risks / progress

## Branch & PR

- Branch: `p4/P4-T058-verify-stress-failure-injection`
- PR title: `P4-T058: Stress and failure injection for the intel pipeline`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T058` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (decision-svc outage asserts nothing on the order path waits (R4.N2, 17 §A P4-B010))
