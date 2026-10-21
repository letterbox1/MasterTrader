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
depends_on: [P8-T003, P8-T004, P8-T005, P8-T006, P8-T007]
requirements: [R8.03, R8.04]
roadmap_todos: [T8.20]
modules: [M11, M12, M20]
dashboards: [D05, D17]
branch: p8/P8-T010-tools-trade-adjust
pr: ""
doc_sync: [docs/03-build-spec.md, docs/ui/dashboards/D17-mcp-console.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T010 · Trade & adjust tool group

## Goal / expected outcome

Claude can place, modify and cancel orders, adjust or close positions, move stops/targets, scale in/out and flatten an instrument or strategy. Each tool maps to exactly one existing `mt_api` command, and by default every one waits for your Telegram approval and passes M11.

## Context & references

- Roadmap: [R8.03, R8.04](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.20](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Spec: [03 M20 Trade & adjust row](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7.2 Orders group](../../../docs/02-v1-architecture.md#72-commands-rest-write) · [D03 Flatten = `position.close` (strategy scope)](../../../docs/ui/dashboards/D03-strategies.md) · [D05 rules](../../../docs/ui/dashboards/D05-execution.md)
- Security: [07 §6](../../../docs/07-security-notes.md#6-application-controls) · [SPEC NN2](../../../SPEC.md#non-negotiable-requirements)
- Cross-phase: P2 R2.10, R2.16, R2.17, R2.31, R2.32 (M11 checks, registry, STP, idempotent IDs).
- Related: P8-T005 (policy), P8-T014 (approval card).

## Requirements

- Tool map (group `trade`, default disabled until you enable them in P8-T019): `order_place` → `order.place`; `order_modify` → `order.modify`; `order_cancel` → `order.cancel`; `order_cancel_all` (scope instrument/strategy/all) → `order.cancel_all`; `position_close` (full; scope instrument or strategy = flatten) → `position.close`; `position_reduce` (fraction or qty = scale out) → `position.reduce`; scale in = `order_place` with `position_ref`; `position_set_brackets` (stop/target) → `position.set_brackets`; `risk_preview` → `POST /risk/preview` (C0).
- Each write returns `{status: pending_approval|submitted|rejected, approval_id, ttl_s, risk_preview, reasons[]}`; descriptions tell Claude that orders usually wait for your Telegram approval.
- `reason` is required (≤ 500 chars) and appears on the approval card as unverified text.
- "Close half my EURUSD" maps to `position_reduce(instrument=EURUSD, fraction=0.5)`.
- Kill ON → every trade tool except cancel returns `kill_on`. Unreconciled positions → close/reduce refused (D05).
- No composite tools: flatten is one `position.close` call; no tool loops over positions.

## ToDo

- [ ] Add the registry entries (group `trade`, state `disabled`, C2 except cancel of a non-protective order = C1) and regenerate the snapshot.
- [ ] Make sure the command request models carry clear field docs (side, qty as decimal string, order type, TIF, price) for the generator.
- [ ] Integration tests on paper/testnet venues through the full stack.
- [ ] Update docs.

## Verification

### Tests
- Integration (Binance testnet / OANDA practice via mt_api test env): every tool → expected command → pending approval → approve → paper fill/cancel; reject; expire.
- Integration: M11 rejection (max position) is returned to Claude as a problem with `reasons`.
- Integration: 5 retries with the same idempotency key → one order.
- Snapshot: trade group reviewed; no tool named approve/submit_direct exists.

### Scenarios
- Given a 1 BTC long, when Claude moves the stop to break-even, then `position_set_brackets` creates an approval card and the stop moves only after you approve.
- Given Kill ON, when Claude calls `order_place`, then it gets `kill_on`; `order_cancel` still works.
- Given an unreconciled position, when Claude tries `position_close`, then it's refused with a reconcile-first reason.

### Stress / failure injection
- Venue disconnect after approval: the order is flagged unknown and reconciled; no duplicate on reconnect.
- Client retry storm (same key ×20 in 1 s) → one order, 19 idempotent replays.

## Acceptance criteria

- [ ] All M20 trade & adjust actions covered by one-to-one tools
- [ ] Every trade tool result shows pending approval by default; nothing reaches a venue without M11
- [ ] Paper/testnet integration tests green
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- DQ stale/bad on the instrument: M11 rejects at request or release.
- Blackout window (M5): rejected with the blackout reason.
- Approval arrives after TTL: rejected, never executed late.
- Partial fill then reduce: reduce acts on the filled quantity; the remainder is a working order.

## Cardinal rules (do NOT)

- Do NOT add a tool that submits directly to a venue or that approves anything.
- Do NOT build composite tools (business logic) in `mt_mcp`.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT use live money before the P7 gates; keys stay trade-only, IP-locked, withdrawals disabled.
- Do NOT expose withdrawals, API-key management or wallet mandate signing through MCP, in any form (R8.06).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

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
