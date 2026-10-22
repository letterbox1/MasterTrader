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
depends_on: [P8-T008, P8-T009, P8-T010, P8-T011, P8-T012, P8-T013, P8-T014, P8-T016, P8-T032]
requirements: [R8.03, R8.04, R8.05, R8.07, R8.08]
roadmap_todos: [T8.20, T8.21]
modules: [M20, M8, M11, M19]
dashboards: [D17, D06, D05, D03]
tools: [uv, pnpm, docker, git]
mcp: []
env: []
services: [postgres, nats, litellm, llm-local, mt-engine]
branch: p8/P8-T026-verify-conversational-scenarios
pr: ""
doc_sync: [docs/roadmap/phase-8-mcp.md]
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

# P8-T026 · End-to-end conversational scenarios across all six tool groups

## Goal / expected outcome

A scenario suite (`tests/scenarios/mcp_e2e/`, MCP SDK client against the full compose test stack on the sandbox paper venue/testnets, fake Telegram harness, local models) shows each tool group behaving as specified, end to end, including resource notifications, the audit trail and D17. No real client or keys.

## Context & references

- Roadmap: [R8.03–R8.05, R8.07](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDos [T8.20, T8.21](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Spec: [03 M20](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [15 §1](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) · [02 §7.4](../../../docs/02-v1-architecture.md#74-telegram--mcp) · [02 §8 flows](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Decisions: [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl), [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) · [17 §A P8-B002](../../../docs/17-decisions-register.md#a-s2-items-all-resolved)

## Requirements

- S1 read: "how are my strategies doing" → reads only, C0 (incl. `get_bots`, `get_approvals(source=mcp)`).
- S2 agents: analysis on ETH → run id → `Signal` (advisory, no order); `anomaly_explain` on a seeded anomaly.
- S3 trade: move BTC stop to break-even → card; scale out a third of SOL → card; flatten strategy X → card; cancel a working limit order → card; one card left to expire after 5 min (injected clock) → rejected.
- S4 strategies/bots: create bot "Trend v3 on gold" in `paper` (C1); `paper` → `hitl` → card (C2); set `autonomous` → C3; pause strategy (C1); run a backtest (C1) and read results.
- S5 risk: tighten (instant); loosen (C3); kill on (< 1 s); kill off (C3).
- S6 curation: add an airdrop URL (vetted), mark a task done.
- S7 disabled tool / missing scope: the client gets a clear error telling you to enable it in D17 or use a token with that scope.
- S8 notifications: subscribed to fills and approvals (P8-T032), the client receives a fill notification after an approved order and an approval-state notification on expiry, both guarded.
- Each scenario asserts `audit.mcp_call`/`audit.command` rows and a Playwright check of D17 Session activity.

## ToDo

- [ ] Write the scenario suite with fixtures.
- [ ] Run nightly in CI; record the first green run.
- [ ] Doc sync.

## Verification

### Tests
- The scenario suite (S1–S8).

### Scenarios
- As listed in Requirements (given/when/then encoded per scenario).

### Stress / failure injection
- n/a here: load and faults are covered by P8-T027.

## Acceptance criteria

- [ ] S1–S8 green in CI; audit and D17 assertions pass
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Testnet flakiness: retry the scenario once; a second failure fails the run (no silent retries).

## Cardinal rules (do NOT)

- Do NOT use live accounts.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT use live money before the P7 gates; keys stay trade-only, IP-locked, withdrawals disabled.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: note R8.03 tool tests green.

## Branch & PR

- Branch: `p8/P8-T026-verify-conversational-scenarios`
- PR title: `P8-T026: End-to-end conversational scenarios across all six tool groups`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T026` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (every trade action incl. cancel → card with TTL 5 min expiry case, modes `paper`/`hitl`/`autonomous` with paper → hitl C2, scope errors, S8 resource notifications; dep P8-T032; added R8.08; tools/env/services)
