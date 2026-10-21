---
id: P8-T026
kind: task
title: End-to-end conversational scenarios across all six tool groups
phase: 8
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T008, P8-T009, P8-T010, P8-T011, P8-T012, P8-T013, P8-T014, P8-T016]
requirements: [R8.03, R8.04, R8.05, R8.07]
roadmap_todos: [T8.20, T8.21]
modules: [M20, M8, M11, M19]
dashboards: [D17, D06, D05, D03]
branch: p8/P8-T026-verify-conversational-scenarios
pr: ""
doc_sync: [docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T026 · End-to-end conversational scenarios across all six tool groups

## Goal / expected outcome

A scenario suite (`tests/scenarios/mcp_e2e/`, MCP SDK client against the full compose test stack on paper/testnet) shows each tool group behaving as specified, end to end, including the audit trail and D17.

## Context & references

- Roadmap: [R8.03–R8.05, R8.07](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDos [T8.20, T8.21](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Spec: [03 M20](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [15 §1](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) · [02 §8 flows](../../../docs/02-v1-architecture.md#8-end-to-end-flows)

## Requirements

- S1 read: "how are my strategies doing" → reads only, C0.
- S2 agents: analysis on ETH → run id → `Signal` (advisory, no order); `anomaly_explain` on a seeded anomaly.
- S3 trade: move BTC stop to break-even → approval; scale out a third of SOL → approval; flatten strategy X → approval; cancel a non-protective limit order → immediate (C1).
- S4 strategies/bots: create bot "Trend v3 on gold, hitl" (C1); set autonomous → C3; pause strategy (C1); run a backtest (C1) and read results.
- S5 risk: tighten (instant); loosen (C3); kill on (< 1 s); kill off (C3).
- S6 curation: add an airdrop URL (vetted), mark a task done.
- S7 disabled tool: Claude gets a clear error telling you to enable it in D17.
- Each scenario asserts `audit.mcp_call`/`audit.command` rows and a Playwright check of D17 Session activity.

## ToDo

- [ ] Write the scenario suite with fixtures.
- [ ] Run nightly in CI; record the first green run.
- [ ] Doc sync.

## Verification

### Tests
- The scenario suite (S1–S7).

### Scenarios
- As listed in Requirements (given/when/then encoded per scenario).

### Stress / failure injection
- n/a here: load and faults are covered by P8-T027.

## Acceptance criteria

- [ ] S1–S7 green in CI; audit and D17 assertions pass
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Testnet flakiness: retry the scenario once; a second failure fails the run (no silent retries).

## Cardinal rules (do NOT)

- Do NOT use live accounts.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT use live money before the P7 gates; keys stay trade-only, IP-locked, withdrawals disabled.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: note R8.03 tool tests green.

## Branch & PR

- Branch: `p8/P8-T026-verify-conversational-scenarios`
- PR title: `P8-T026: End-to-end conversational scenarios across all six tool groups`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T026` run

## Progress log

- 2026-10-21 00:00 · planner · created
