---
id: P8-T005
kind: task
title: "MCP order policy: approve-mode default, confirmation mapping and rate limits (`mcp.policy.set`)"
phase: 8
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T004, P8-B002]
requirements: [R8.04, R8.05]
roadmap_todos: [T8.21]
modules: [M20, M11]
dashboards: [D17, D06, D05]
branch: p8/P8-T005-mcp-order-policy
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/07-security-notes.md, docs/15-bots-hitl-and-worm-audit.md, docs/ui/dashboards/D17-mcp-console.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T005 · MCP order policy: approve-mode default, confirmation mapping and rate limits (`mcp.policy.set`)

## Goal / expected outcome

Every MCP-sourced command is routed by a **server-side** policy in `mt_api`. C0/C1 run immediately (with a Telegram notice for writes). C2 trading commands become pending approvals (Telegram button) unless an explicit per-venue/size rule you set allows auto. C3 always runs the full Telegram + TOTP + cool-down flow. Kill ON is immediate. Every order still passes M11.

## Context & references

- Roadmap: [R8.04, R8.05](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.21](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Spec: [03 M20 safeguards](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [SPEC NN2](../../../SPEC.md#non-negotiable-requirements) · [07 §6](../../../docs/07-security-notes.md#6-application-controls) · [02 §7.2 confirmation levels](../../../docs/02-v1-architecture.md#72-commands-rest-write) · [02 F2, F5, F6](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- HITL rules: [15 §1.2–1.3](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) (TTL, expiry = reject, protective exits never wait, approval bound to your Telegram id)
- UI: [D17 Actions](../../../docs/ui/dashboards/D17-mcp-console.md) (`mcp.policy.set`, loosening = C3)
- Cross-phase: P0 T0.24 confirmation engine; P2 R2.10 (M11), R2.13 (`manual` sleeve), R2.19 / T2.24 (change control), R2.20, R2.51 / T2.33 (approvals + Telegram C3).
- Gap: P8-B002 (C1/C2 mapping and TTL for MCP unspecified); numbers below are its proposal.

## Requirements

- Mapping for `source = mcp`: **C0** → immediate. **C1** → immediate, plus a Telegram notice "MCP did X" for writes. **C2** → `pending_approval` → `risk.approval.request` (source mcp) → approve in Telegram or web within TTL, else rejected (never act late). **C3** → standard C3 (Telegram approve + TOTP + 15-min default cool-down), never shortened by MCP policy. **Kill ON** → immediate. **Kill OFF** → C3.
- C2 via MCP includes `order.place`, `order.modify`, `order.cancel_all`, `position.close`, `position.reduce`, `position.set_brackets`, and `order.cancel` when the order is a protective stop/target. `order.cancel` of a non-protective working order is C1.
- MCP approval TTL: default 15 min, configurable 1–60 min in `mcp.policy.set`. Expiry = reject, logged "expired".
- `ops.mcp_policy` (versioned rows): auto rules `{venue, asset_class?, max_notional_aud, max_orders_per_day}`; default **none**. Adding/raising a rule = C3; removing/lowering = C1. Rules never apply to `position.set_brackets` widening a stop, nor to any C3 command.
- M11 runs at request time (its preview goes on the card) and again at release; the order is submitted only if M11 passes at release. Venue registry, 2× cap, STP and DQ checks are unchanged.
- MCP orders book to the `manual` sleeve unless a strategy/bot is named; client order IDs are idempotent from `idempotency_key`.
- Rate limits (proposed): reads 60/min, agents 10/h, trade commands 10/min and 50/day, risk tighten 10/min, kill unlimited. Excess → 429 problem+json and `alert.warn.mcp_rate`; MCP counts toward the 07 §9 "unusual order rate" alert.
- Protective exits (entry stop/TP, kill flatten, risk-forced reductions) are outside MCP policy and never wait.

## ToDo

- [ ] Implement `packages/mt_api/mcp/policy.py` hooked into the confirmation engine before command dispatch.
- [ ] Migration `ops.mcp_policy`; command `mcp.policy.set` (web/Telegram only) with tighten/loosen classification.
- [ ] Pending-approval path: reuse `risk.approval` and the `risk.approval.request/result` NATS subjects; add `source` and `reason` to the payload (P8-T014 renders it).
- [ ] TTL expiry worker (server UTC); auto-reject pending MCP approvals on Kill ON.
- [ ] Token-bucket rate limiter keyed by (token_id, tool) in NATS KV, with Prometheus metrics.
- [ ] Golden decision table `tests/golden/mcp_policy.csv` (command × level × policy × kill state → outcome) as a mandatory-for-merge test.
- [ ] Update docs.

## Verification

### Tests
- Golden: full decision table (≥ 60 rows) incl. protective-stop cancel, bracket widening, auto-rule boundary ±0.01 AUD, kill ON.
- Integration (paper venue): MCP `order.place` → pending → Telegram approve → M11 passes → paper fill; reject path; expiry path.
- Integration: auto rule allows a small order but M11 still rejects it when it breaches a limit, DQ is `stale` or the venue isn't `allowed`.
- Integration: MCP `risk.kill.on` → engine cancels all in < 1 s; pending MCP approvals auto-rejected.
- Unit: rate limiter buckets, 429 shape.

### Scenarios
- Given no auto rules, when Claude closes half of EURUSD, then a Telegram card appears and nothing executes until you tap Approve.
- Given a rule `{venue: binance-testnet, max_notional_aud: 200}`, when Claude places a 150 AUD order, then it goes straight to M11; at 201 AUD it waits for approval.
- Given you tap Approve after the 15-min TTL, then the order is rejected as expired.

### Stress / failure injection
- 100 MCP order requests in 60 s → 10 reach the approval queue, the rest get 429; Telegram output stays ≤ 30 msg/s.
- Pre-trade risk check p99 stays < 1 ms with MCP load (02 §9.2).

## Acceptance criteria

- [ ] Golden decision table green and marked mandatory for merge
- [ ] No MCP order reaches a venue without M11; none skips approval unless a matching C3-approved auto rule exists
- [ ] C3 flows never shortened by MCP policy; kill ON immediate, kill OFF C3
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Telegram down: approvals still possible from web (D01/D17); otherwise they expire as rejects.
- mt_api restart with pending approvals: they persist in `risk.approval`; TTL keeps running on wall clock; expired ones are rejected on startup.
- Kill ON: all MCP trade commands except cancel are rejected with `kill_on`; pending MCP approvals are auto-rejected.
- DQ degraded or blackout at release time: M11 rejects; the card shows the reason.
- Unreconciled position: close/reduce rejected (D05 rule) except flatten via kill.

## Cardinal rules (do NOT)

- Do NOT let any MCP policy setting skip M11, the venue registry, STP or DQ checks.
- Do NOT let MCP approve its own requests or change its own policy.
- Do NOT decide confirmation levels in `mt_mcp`.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT use live money before the P7 gates; keys stay trade-only, IP-locked, withdrawals disabled.
- Do NOT update or delete WORM rows; corrections are new rows (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

## Doc sync on completion

- `docs/02-v1-architecture.md` §7.2 (MCP mapping row) and §7.4.
- `docs/03-build-spec.md` M20 and `docs/07-security-notes.md` §6: mapping, TTL, rate limits.
- `docs/15-bots-hitl-and-worm-audit.md` §1.5: MCP uses the same commands; MCP approval TTL.
- `docs/ui/dashboards/D17-mcp-console.md`: policy fields.
- `docs/roadmap/phase-8-mcp.md`: tick T8.21 when P8-T004, T006 and T014 are also done.

## Branch & PR

- Branch: `p8/P8-T005-mcp-order-policy`
- PR title: `P8-T005: MCP order policy: approve-mode default, confirmation mapping and rate limits (`mcp.policy.set`)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T005` run

## Progress log

- 2026-10-21 00:00 · planner · created
