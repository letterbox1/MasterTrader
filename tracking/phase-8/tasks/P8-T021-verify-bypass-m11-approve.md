---
id: P8-T021
kind: task
title: "Bypass tests: no MCP order can skip M11 or its approval card; MCP can't call `approval.*` or `mcp.*`"
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
tools: [uv, docker, git]
mcp: []
env: []
services: [postgres, nats, mt-engine]
branch: p8/P8-T021-verify-bypass-m11-approve
pr: ""
doc_sync: [docs/roadmap/phase-8-mcp.md, docs/07-security-notes.md]
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

# P8-T021 · Bypass tests: no MCP order can skip M11 or its approval card; MCP can't call `approval.*` or `mcp.*`

## Goal / expected outcome

An adversarial test suite `tests/security/test_mcp_bypass.py`, mandatory for merge, proves T8.60's bypass half: no path from an MCP principal reaches a venue without M11; no MCP order skips your approval card (expiry = reject); MCP can't call `approval.*` or `mcp.*`. Runs on the sandbox paper venue with a fake Telegram harness; no keys.

## Context & references

- Roadmap: [R8.04](../../../docs/roadmap/phase-8-mcp.md#3-requirements) (verified by: bypass tests) · ToDo [T8.60](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Decisions: [17 §A P8-B001/B002](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) · [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl), [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8)
- Spec: [SPEC NN2](../../../SPEC.md#non-negotiable-requirements) · [03 M20](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [07 §6](../../../docs/07-security-notes.md#6-application-controls) · [02 F2](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Precedent: P2-T052 (no-bypass tests for every order source).

## Requirements

- Attack matrix (each is a test): (1) raw mt_api call with an MCP token, skipping `mt_mcp`; (2) forged `source: web` in body/headers; (3) orders via other groups (`strategy.start` live, `bot.create` autonomous, `bot.approval_policy.set` loosen); (4) self-approval: raw `approval.approve` / `approve_partial` / `reject` with an MCP token → 403; (5) self-admin: raw `mcp.policy.set` / `mcp.tool.set` / `mcp.token.create` with an MCP token → 403; (6) idempotency-key replay with changed args → 409; (7) modify a pending order after the card is shown → new card; (8) look for a skip-approval path: every policy field and query parameter fuzzed, none yields `submitted` without approval; (9) M11 rejects at release after approval (limit, DQ stale, blackout, venue not allowed, leverage cap); (10) Kill ON → refused; (11) cancel, bracket widening and protective-stop cancel from MCP → card; (12) approval after TTL (5 min default, injected clock) → rejected; (13) from inside the `mcp` container, publish to `ord.intent.*` on NATS → no route.
- Every case asserts: no order at the paper venue without your approval, and the expected `audit.mcp_call` result status.
- Marked as a required CI check for PRs touching `mt_api`, `mt_risk`, `mt_mcp`.

## ToDo

- [ ] Write the suite against the compose test stack (sandbox paper venue).
- [ ] Make it a required check.
- [ ] Record the run in the Progress log.
- [ ] Doc sync.

## Verification

### Tests
- The suite (≥ 13 cases); plus a mutation check: temporarily disabling the policy hook makes ≥ 1 test fail (proves the tests bite).

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
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: tick T8.60 once P8-T022 and P8-T027 also pass.
- `docs/07-security-notes.md` §6: link to the suite.

## Branch & PR

- Branch: `p8/P8-T021-verify-bypass-m11-approve`
- PR title: `P8-T021: Bypass tests: no MCP order can skip M11 or its approval card; MCP can't call approval.* or mcp.*`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T021` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (auto-rule cases replaced by "no skip-approval path exists" fuzzing; `approval.*` incl. reject and `mcp.*` self-admin cases; TTL 5 min; cancel → card; tools/env/services)
