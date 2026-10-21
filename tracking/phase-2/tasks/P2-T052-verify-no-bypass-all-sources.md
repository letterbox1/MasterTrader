---
id: P2-T052
kind: task
title: "No-bypass tests: every order source passes M11"
phase: 2
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T021, P2-T035, P2-T020, P2-T038]
requirements: [R2.10]
roadmap_todos: [T2.60]
modules: [M11, M12]
dashboards: []
branch: p2/P2-T052-verify-no-bypass-all-sources
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T052 · No-bypass tests: every order source passes M11

## Goal / expected outcome

Automated tests prove that orders from strategies, bots, an agent-style signal source, the web UI (`mt_api`), Telegram and direct NATS publishing all go through `RiskGate`, and that no code path can reach a venue client without it.

## Context & references

- Roadmap: [R2.10](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.60
- Spec: [SPEC NN2](../../../SPEC.md#non-negotiable-requirements) · [03 M11](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp)
- MCP is Phase 8; its adapter will reuse this test.

## Requirements

- Sources: strategy `submit_intent`; bot; agent stub publishing `sig.agent.*` → strategy; `order.place` via mt_api; Telegram command; raw NATS publish on `ord.intent.*` and on any venue-ish subject.
- For each: a policy that rejects everything → zero venue submissions (adapter spy) and a `ord.risk.reject` per intent.
- Static: import-linter contracts (only `mt_engine.node` and `mt_strategy.base` touch Nautilus exec clients); grep test for adapter calls outside allowed modules; NATS account permissions deny `ord.*` publish to non-engine accounts except `ord.intent.*`.

## ToDo

- [ ] Spy adapter + reject-all policy fixture
- [ ] Per-source integration tests
- [ ] Static/arch tests
- [ ] NATS permission test
- [ ] Record results (numbers, run IDs, screenshots) in the progress log and tick the roadmap ToDo box

## Verification

### Tests
- As described; runs in CI on every PR.

### Scenarios
- Given a reject-all policy, when each source sends an order, then the spy adapter records 0 submits and audit shows 1 reject per intent.

### Stress / failure injection
- Fuzz `ord.intent.*` payloads (schemathesis/hypothesis) for 10 min: never a submit without a gate decision.

## Acceptance criteria

- [ ] All sources covered; 0 bypasses
- [ ] Static contracts in CI

## Exceptions & edge cases

- Protective exits: still pass the gate (kill/venue/duplicate checks) — asserted.

## Cardinal rules (do NOT)

- Do NOT whitelist a source in tests to make them pass.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/03-build-spec.md` M11: reference the bypass test suite.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.60 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T052-verify-no-bypass-all-sources`
- PR title: `P2-T052: No-bypass tests: every order source passes M11`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T052` run

## Progress log

- 2026-10-21 00:00 · planner · created
