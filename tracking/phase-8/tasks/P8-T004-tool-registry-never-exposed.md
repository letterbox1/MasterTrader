---
id: P8-T004
kind: task
title: Tool registry and never-exposed filter in mt_api (`/mcp/tools`, `mcp.tool.set`)
phase: 8
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T002, P8-B001, P8-B005]
requirements: [R8.03, R8.06]
roadmap_todos: [T8.21]
modules: [M20]
dashboards: [D17]
branch: p8/P8-T004-tool-registry-never-exposed
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/07-security-notes.md, docs/ui/dashboards/D17-mcp-console.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T004 · Tool registry and never-exposed filter in mt_api (`/mcp/tools`, `mcp.tool.set`)

## Goal / expected outcome

`mt_api` holds the authoritative registry of every query and command, classified for MCP as `enabled`, `disabled` (can be enabled) or `never` (locked). `mt_api` rejects any MCP-sourced call that isn't enabled and in scope, whatever `mt_mcp` sends. The never-exposed set can only change by a reviewed code change.

## Context & references

- Roadmap: [R8.03, R8.06](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.21](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Spec: [03 M20 safeguards](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7.4](../../../docs/02-v1-architecture.md#74-telegram--mcp) ("queries plus a subset of commands"; never withdrawals, keys, mandates) · [07 §6](../../../docs/07-security-notes.md#6-application-controls)
- UI: [D17 Tool registry + Actions](../../../docs/ui/dashboards/D17-mcp-console.md) (`mcp.tool.set`: enabling a trade/risk tool = C3, disabling = C1; never-exposed shown greyed with a lock)
- Command catalogue: [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write)
- Gaps: P8-B001 (approvals and `mcp.*` must be never-exposed), P8-B005 (funds-moving commands not classified).

## Requirements

- `packages/mt_api/mcp/registry.yaml` (versioned, reviewed in PR) lists every OpenAPI operation with `group` (read / agents / trade / strategies / risk / curation / none), `kind`, confirmation level, default state and rate limit. It is loaded into `ops.mcp_tool`, whose state changes go only through `mcp.tool.set`.
- **Never** (code constant + DB check constraint, not toggleable): any withdrawal/transfer-out; key management (`/system/keys`, `system.key.*`); mandates (`airdrop.mandate.create`, `airdrop.mandate.revoke`); approvals (`approval.approve`, `approval.approve_partial`); MCP self-admin (`mcp.tool.set`, `mcp.policy.set`, `mcp.token.*`); auth/session endpoints. Proposed additions pending P8-B005: `wallet.sweep`, `treasury.allocate`, `treasury.earn.enter/exit`, `airdrop.claim.execute`, `system.service.restart`, `system.restore.test`, `memory.delete`, `/system/logs`.
- Default **enabled**: read & analyse, agents and curation tools, plus `risk.kill.on` (protective, never blocked).
- Default **disabled** (enabled by you in D17): trade, strategies and risk-write tools. Enabling them is C3; enabling other tools is C1; disabling anything is C1.
- Default-deny: an operation missing from `registry.yaml` fails CI (completeness test) and is treated as disabled at runtime.
- Guard middleware `McpGuard`: for `source = mcp`, require registry state `enabled` and the tool group in the token's scopes, else 403 `tool_never_exposed` / `tool_disabled` / `scope_missing` plus an audit row.
- `/mcp/tools` returns group, level, state, rate limit and calls/day (from `audit.mcp_call`); `mcp.tool.set` on a `never` tool → 409.
- A registry change publishes WS `system` event `mcp.registry.changed`.

## ToDo

- [ ] Write `registry.yaml` covering the whole current OpenAPI; mark never/enabled/disabled per the rules above.
- [ ] Migration `ops.mcp_tool` with a check constraint that `never` rows can't change state.
- [ ] Implement the loader, `McpGuard` middleware, `/mcp/tools` query and `mcp.tool.set` command (levels via the P0 confirmation engine).
- [ ] CI test: every OpenAPI operation has exactly one registry entry; the never set equals the code constant.
- [ ] Write tests; update docs.

## Verification

### Tests
- Unit: classification loader; check constraint blocks `UPDATE … SET state='enabled'` on a never row.
- Integration: MCP token raw-POSTs `/commands/approval.approve` → 403 `tool_never_exposed` and an audit row; web `mcp.tool.set` on a never tool → 409.
- Integration: enabling `order.place` from web triggers C3 (Telegram + TOTP + cool-down); disabling is immediate (C1).
- Property: for random OpenAPI fixtures, unknown operations are denied for MCP.

### Scenarios
- Given a new mt_api route added without a registry entry, when CI runs, then the completeness test fails.
- Given the trade group is disabled, when Claude calls `order_place` through a stale tool list, then mt_api answers 403 `tool_disabled`.
- Given you disable `position_close` in D17, when the registry event fires, then the tool disappears from the client within 60 s and is refused immediately server-side.

### Stress / failure injection
- Guard overhead < 1 ms p99 at 1,000 req/s (registry cached in memory, invalidated on change).

## Acceptance criteria

- [ ] No never-exposed operation can be called by an MCP principal or enabled by any command
- [ ] Completeness CI test is in place and green
- [ ] Trade/risk enable = C3, disable = C1, per D17
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- DB down: the guard fails closed for MCP (403/503); web unaffected.
- Registry cache stale after restart: reload from DB at startup before serving MCP.
- A never tool appears in an old client's cached list: the server refusal is authoritative.

## Cardinal rules (do NOT)

- Do NOT implement the filter only in `mt_mcp`; `mt_api` is the authority.
- Do NOT make never-exposed state data-driven or toggleable from any UI, Telegram or MCP path.
- Do NOT expose withdrawals, API-key management or wallet mandate signing through MCP, in any form (R8.06).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT update or delete WORM rows; corrections are new rows (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

## Doc sync on completion

- `docs/02-v1-architecture.md` §7.1 (`/mcp/tools`), §7.4 (full never-exposed list).
- `docs/03-build-spec.md` M20 safeguards and `docs/07-security-notes.md` §6: never-exposed list.
- `docs/ui/dashboards/D17-mcp-console.md`: registry states and defaults.
- `docs/roadmap/phase-8-mcp.md`: progress on T8.21.

## Branch & PR

- Branch: `p8/P8-T004-tool-registry-never-exposed`
- PR title: `P8-T004: Tool registry and never-exposed filter in mt_api (`/mcp/tools`, `mcp.tool.set`)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T004` run

## Progress log

- 2026-10-21 00:00 · planner · created
