---
id: P8-T021
kind: task
title: "Bypass tests: no MCP order can skip M11 or approve mode"
phase: 8
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T005, P8-T010, P8-T011, P8-T012, P8-T014]
requirements: [R8.04]
roadmap_todos: [T8.60]
modules: [M20, M11, M12]
dashboards: [D17, D05]
branch: p8/P8-T021-verify-bypass-m11-approve
pr: ""
doc_sync: [docs/roadmap/phase-8-mcp.md, docs/07-security-notes.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T021 · Bypass tests: no MCP order can skip M11 or approve mode

## Goal / expected outcome

An adversarial test suite `tests/security/test_mcp_bypass.py`, mandatory for merge, proves that no path from an MCP principal reaches a venue without M11. No order skips the Telegram approval except under an explicit C3-approved auto rule, and even then M11 still decides.

## Context & references

- Roadmap: [R8.04](../../../docs/roadmap/phase-8-mcp.md#3-requirements) (verified by: Bypass tests) · ToDo [T8.60](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Spec: [SPEC NN2](../../../SPEC.md#non-negotiable-requirements) · [03 M20](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [07 §6](../../../docs/07-security-notes.md#6-application-controls) · [02 F2](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Cross-phase: P2 R2.N2 (risk golden tests mandatory for merge) as the precedent.

## Requirements

- Attack matrix (each is a test): (1) raw mt_api call with an MCP token, skipping `mt_mcp`; (2) forged `source: web` in body/headers; (3) orders via other groups (`strategy.start` live, `bot.create` autonomous, `bot.approval_policy.set` loosen); (4) self-approval: raw `approval.approve` / `approve_partial` with an MCP token; (5) idempotency-key replay with changed args → 409; (6) modify a pending order after the card is shown → new approval; (7) auto-rule boundary +0.01 AUD and order splitting past `max_orders_per_day`; (8) M11 rejects under an auto rule (limit, DQ stale, blackout, venue not allowed, 2× cap); (9) Kill ON → refused; (10) bracket widening and protective-stop cancel → approval; (11) approval after TTL → rejected; (12) from inside the `mcp` container, publish to `ord.intent.*` on NATS → no route.
- Every case asserts: no order at the paper venue, and the expected `audit.mcp_call` result status.
- Marked as a required CI check for PRs touching `mt_api`, `mt_risk`, `mt_mcp`.

## ToDo

- [ ] Write the suite against the compose test stack (paper venues).
- [ ] Make it a required check.
- [ ] Record the run in the Progress log.
- [ ] Doc sync.

## Verification

### Tests
- The suite (≥ 12 cases); plus a mutation check: temporarily disabling the policy hook makes ≥ 1 test fail (proves the tests bite).

### Scenarios
- Given an attacker controls the conversation, when they try every listed path, then zero orders reach the venue without your approval.

### Stress / failure injection
- Run the suite with 10 parallel workers × 3 repetitions to catch race conditions (approve vs modify, expiry vs approve).

## Acceptance criteria

- [ ] All bypass cases pass; required check in CI
- [ ] Mutation check proves the suite detects a removed policy hook
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Testnet venue unavailable: run against the Nautilus sandbox venue; note it.

## Cardinal rules (do NOT)

- Do NOT mark any case xfail/skip to get green.
- Do NOT run against live accounts.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT use live money before the P7 gates; keys stay trade-only, IP-locked, withdrawals disabled.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: tick T8.60 once P8-T022 and P8-T027 also pass.
- `docs/07-security-notes.md` §6: link to the suite.

## Branch & PR

- Branch: `p8/P8-T021-verify-bypass-m11-approve`
- PR title: `P8-T021: Bypass tests: no MCP order can skip M11 or approve mode`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T021` run

## Progress log

- 2026-10-21 00:00 · planner · created
