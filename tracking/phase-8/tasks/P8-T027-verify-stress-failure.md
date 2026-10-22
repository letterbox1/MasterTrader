---
id: P8-T027
kind: task
title: Stress and failure injection on the MCP path
phase: 8
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T005, P8-T010, P8-T015, P8-T016, P8-T030, P8-T032]
requirements: [R8.02, R8.04, R8.07]
roadmap_todos: [T8.60]
modules: [M20, M11, M17]
dashboards: [D17, D16]
tools: [uv, docker, git, tc, iptables]
mcp: []
env: []
services: [postgres, nats, caddy, mt-engine]
branch: p8/P8-T027-verify-stress-failure
pr: ""
doc_sync: [docs/roadmap/phase-8-mcp.md, docs/runbooks/mcp-incident.md]
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

# P8-T027 · Stress and failure injection on the MCP path

## Goal / expected outcome

Fault-injection runs show the MCP path fails **closed** and never degrades the trading core. Nothing executes without M11, approval or an audit row; protective behaviour and SLOs hold under load and component failures.

## Context & references

- Roadmap: [R8.02, R8.04, R8.07](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.60](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Architecture: [02 §9.2 SLOs](../../../docs/02-v1-architecture.md#92-observability--slos) · [02 §9.3 degraded modes](../../../docs/02-v1-architecture.md#93-degraded-modes)
- Decisions: [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) (limits) · [16 §3.3](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check) (write path) · [16 §2.11](../../../docs/16-configuration-and-safety-model.md#211-worm-integrity)
- Related: P8-T005 (policy), P8-T015 (container), P8-T017 (runbook), P8-T030 (limits), P8-T032 (subscriptions).

## Requirements

- Load: 100 calls/s for 60 s from 3 tokens → 429s per the per-token limits (default 60 reads/min, 10 writes/min); pre-trade risk p99 < 1 ms and kill → cancels < 1 s unaffected; mt_api web p95 regression ≤ 10%.
- mt-api down: tools return "mt_api unavailable"; no command is queued and replayed later; Telegram `/kill` still works via NATS.
- Telegram API unreachable: approvals still possible in D17/D01; otherwise they expire as rejects.
- Postgres down: MCP returns 503; nothing executes; no audit gap after recovery.
- `mcp` container restart during a pending approval and an open subscription stream: the approval survives (TTL keeps running); the client resumes or re-subscribes and reads the outcome.
- Token revoked mid-session; Kill ON with pending MCP approvals (auto-rejected); LiteLLM budget exhausted (local fallback); `tc netem` 2 s latency + 10% loss between `mcp` and `mt-api` (clean timeouts; idempotent retries → one order); chrony stopped with 5 s skew (TTL server-side).
- Results in `docs/reports/p8-stress.md`.

## ToDo

- [ ] Write the fault scripts `tests/chaos/mcp/` (docker stop, iptables/netem, clock).
- [ ] Run all cases on the test stack; record metrics.
- [ ] Update the runbook with anything learned; doc sync.

## Verification

### Tests
- Each case asserts venue state, audit rows and SLO metrics from Prometheus.

### Scenarios
- Given Postgres is down when you approve an MCP order, then the order isn't submitted and the card says so; after recovery it's expired, not executed late.

### Stress / failure injection
- This item is the stress/failure work: all cases above.

## Acceptance criteria

- [ ] All cases fail closed; SLOs held; report merged
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Chaos on the shared host: run on the test stack only, never the paper/live stack that holds the paper clock.

## Cardinal rules (do NOT)

- Do NOT run chaos against the stack that holds the P7 paper clock or any live account.
- Do NOT use live money before the P7 gates; keys stay trade-only, IP-locked, withdrawals disabled.
- Do NOT update or delete WORM rows; corrections are new rows (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: part of T8.60.
- `docs/runbooks/mcp-incident.md`: lessons learned.

## Branch & PR

- Branch: `p8/P8-T027-verify-stress-failure`
- PR title: `P8-T027: Stress and failure injection on the MCP path`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T027` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (per-token limit defaults from 16 §2.12, subscription stream restart case, 16 §3.3/§2.11 references; deps P8-T030/T032; tools/env/services)
