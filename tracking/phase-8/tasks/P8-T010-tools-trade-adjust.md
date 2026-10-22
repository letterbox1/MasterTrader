---
id: P8-T010
kind: task
title: Trade & adjust tool group
phase: 8
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T003, P8-T004, P8-T005, P8-T006, P8-T007, P2-T021, P2-T023, P2-T031]
requirements: [R8.03, R8.04]
roadmap_todos: [T8.20]
modules: [M11, M12, M20]
dashboards: [D05, D17]
tools: [uv, docker, git]
mcp: []
env: []
services: [postgres, nats, mt-engine]
branch: p8/P8-T010-tools-trade-adjust
pr: ""
doc_sync: [docs/03-build-spec.md, docs/ui/dashboards/D17-mcp-console.md, docs/roadmap/phase-8-mcp.md]
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

# P8-T010 · Trade & adjust tool group

## Goal / expected outcome

Claude can place, modify and cancel orders, adjust or close positions, move stops/targets, scale in/out and flatten an instrument or strategy. Each tool maps to exactly one existing `mt_api` command, needs the `trade` scope (which "creates approval cards only", 16 §2.12), **always** creates your approval card (TTL default 5 min, expiry = reject) and passes M11. Built and tested on the sandbox paper venue and testnets without keys.

## Context & references

- Roadmap: [R8.03, R8.04](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.20](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Decisions: [17 §A P8-B002](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (C2 orders always your card; no skip option) · [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) · [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8)
- Spec: [03 M20 Trade & adjust row](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) ("each one creates an approval card for you") · [02 §7.2 Orders group](../../../docs/02-v1-architecture.md#72-commands-rest-write) · [D03 Flatten = `position.close` (strategy scope)](../../../docs/ui/dashboards/D03-strategies.md) · [D05 rules](../../../docs/ui/dashboards/D05-execution.md)
- Security: [07 §6](../../../docs/07-security-notes.md#6-application-controls) · [SPEC NN2](../../../SPEC.md#non-negotiable-requirements)
- Cross-phase (depends_on): P2-T021 (engine intent actor + order audit), P2-T023 (testnet configs and sandbox paper venue), P2-T031 (kill switch).
- Related: P8-T005 (policy), P8-T014 (approval card), P8-T030 (10 writes/min).

## Requirements

- Tool map (scope `trade`, default **disabled** until you enable them in P8-T019): `order_place` → `order.place`; `order_modify` → `order.modify`; `order_cancel` → `order.cancel`; `order_cancel_all` (scope instrument/strategy/all) → `order.cancel_all`; `position_close` (full; strategy scope = flatten) → `position.close`; `position_reduce` (fraction or qty = scale out) → `position.reduce`; scale in = `order_place` with `position_ref`; `position_set_brackets` (stop/target) → `position.set_brackets`. `risk_preview` → `POST /risk/preview` (C0, `read` scope).
- **Every** trade tool is C2 for `source = mcp` and returns `{status: pending_approval|rejected, approval_id, ttl_s, risk_preview, reasons[]}`; status becomes `submitted` only after you approve and M11 passes at release. Descriptions tell Claude that you approve each one on Telegram/web and that it can't approve.
- `reason` is required (length-capped) and appears on the approval card as unverified text.
- "Close half my EURUSD" maps to `position_reduce(instrument=EURUSD, fraction=0.5)`.
- Kill ON → trade tools return `kill_on`. Unreconciled positions → close/reduce refused (D05).
- No composite tools: flatten is one `position.close` call; no tool loops over positions.
- Each call counts as a write (default 10 writes/min per token, P8-T030).

## ToDo

- [ ] Add the registry entries (scope `trade`, state `disabled`, C2) and regenerate the snapshot.
- [ ] Make sure the command request models carry clear field docs (side, qty as decimal string, order type, TIF, price) for the generator.
- [ ] Integration tests on the sandbox paper venue and testnets through the full stack (fake Telegram harness for approvals).
- [ ] Update docs.

## Verification

### Tests
- Integration (sandbox paper venue + Binance testnet / OANDA practice configs from P2-T023, no live keys): every tool → expected command → pending approval → approve on web → paper fill/cancel; reject; expire (injected clock, TTL 5 min).
- Integration: M11 rejection (max position) is returned to Claude as a problem with `reasons`.
- Integration: 5 retries with the same idempotency key → one approval card, one order.
- Snapshot: trade group reviewed; no tool named approve/submit_direct/auto exists.

### Scenarios
- Given a 1 BTC long, when Claude moves the stop to break-even, then `position_set_brackets` creates an approval card and the stop moves only after you approve.
- Given Kill ON, when Claude calls `order_place`, then it gets `kill_on`.
- Given an unreconciled position, when Claude tries `position_close`, then it's refused with a reconcile-first reason.
- Given Claude cancels a working limit order, then a card appears; the order stays live until you approve.

### Stress / failure injection
- Venue disconnect after approval: the order is flagged unknown and reconciled; no duplicate on reconnect.
- Client retry storm (same key ×20 in 1 s) → one card, 19 idempotent replays.

## Acceptance criteria

- [ ] All M20 trade & adjust actions covered by one-to-one tools under the `trade` scope
- [ ] Every trade tool result is `pending_approval` (or rejected); nothing reaches a venue without your approval and M11
- [ ] Sandbox/testnet integration tests green without live keys
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- DQ stale/bad on the instrument: M11 rejects at request or release.
- Blackout window (M5): rejected with the blackout reason.
- Approval arrives after TTL: rejected, never executed late.
- Partial fill then reduce: reduce acts on the filled quantity; the remainder is a working order.

## Cardinal rules (do NOT)

- Do NOT add a tool that submits directly to a venue, skips the approval card or approves anything.
- Do NOT build composite tools (business logic) in `mt_mcp`.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT use live money before the P7 gates; keys stay trade-only, IP-locked, withdrawals disabled.
- Do NOT expose anything on the 16 §2.12 never-exposed list.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M20: trade tool list.
- `docs/ui/dashboards/D17-mcp-console.md`: Trade & adjust group.
- `docs/roadmap/phase-8-mcp.md`: progress on T8.20.

## Branch & PR

- Branch: `p8/P8-T010-tools-trade-adjust`
- PR title: `P8-T010: Trade & adjust tool group`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T010` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (every trade tool C2 → your card incl. cancel, TTL 5 min, `trade` scope creates cards only, no skip option, 10 writes/min; cross-phase deps P2-T021/T023/T031; tools/env/services)
