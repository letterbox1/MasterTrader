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
depends_on: [P8-T002, P0-T035]
requirements: [R8.03, R8.06]
roadmap_todos: [T8.21]
modules: [M20]
dashboards: [D17]
tools: [uv, docker, git]
mcp: []
env: []
services: [postgres, nats]
branch: p8/P8-T004-tool-registry-never-exposed
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/07-security-notes.md, docs/ui/dashboards/D17-mcp-console.md, docs/roadmap/phase-8-mcp.md]
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

# P8-T004 · Tool registry and never-exposed filter in mt_api (`/mcp/tools`, `mcp.tool.set`)

## Goal / expected outcome

`mt_api` holds the authoritative registry of every query and command, classified for MCP as `enabled`, `disabled` (can be enabled by you) or `never` (locked), each with the token scope it needs. `mt_api` rejects any MCP-sourced call that isn't enabled and covered by the token's scopes, whatever `mt_mcp` sends. The never-exposed set is exactly the list in [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) / [02 §7.4](../../../docs/02-v1-architecture.md#74-telegram--mcp) and changes only by a reviewed code change.

## Context & references

- Roadmap: [R8.03, R8.06](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.21](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets) (never-exposed filter)
- Decisions: [17 §A P8-B001](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (MCP can never approve; `approval.*`, `mcp.*` never exposed) · [17 §D P8-B005](../../../docs/17-decisions-register.md#d-other-decisions) (never-exposed list in 16 §2.12)
- Spec: [03 M20 safeguards](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7.4](../../../docs/02-v1-architecture.md#74-telegram--mcp) · [07 §6](../../../docs/07-security-notes.md#6-application-controls)
- UI: [D17 Tool registry + Actions](../../../docs/ui/dashboards/D17-mcp-console.md) (`mcp.tool.set`: disable C1; enable read/analyse/curation C1; enable trade/strategy/risk C3; never-exposed greyed with a lock)
- Command catalogue: [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write)
- Cross-phase (depends_on): P0-T035 (confirmation engine used for `mcp.tool.set` levels).

## Requirements

- `packages/mt_api/mcp/registry.yaml` (versioned, reviewed in PR) lists every OpenAPI operation with `group` (read & analyse / talk to agents / trade & adjust / strategies / risk / curation / none), required `scope` (`read`, `analyse`, `trade`, `strategy`, `risk_tighten`, `curation`), confirmation level for `source = mcp`, default state and kind (read/write, used by P8-T030 limits). Loaded into `ops.mcp_tool`; state changes only through `mcp.tool.set`.
- **Never** (code constant + DB check constraint, not toggleable), per 16 §2.12 and 02 §7.4: withdrawals; `wallet.sweep`; `treasury.*` moves; `airdrop.claim.execute`; mandates (`airdrop.mandate.*`); key and token management (`/system/keys`, `system.key.*`, `mcp.token.*`); `approval.*` (incl. `approval.reject`); `mcp.*` (`mcp.tool.set`, `mcp.policy.set`, `mcp.token.*`, and the `/mcp/*` admin queries); restore/delete (`system.restore.test`, `memory.delete`, any delete); `system.service.restart`; `risk.deadman.ack`; `/system/logs`; audit writes (`audit.*` acks/annotations, `audit.integrity.ack`); auth/session endpoints.
- **No scope ever applies a loosening:** loosening requests reachable from MCP (loosening fields of `risk.policy.update`, `risk.kill.off`, bot/strategy loosening) are always C3 and complete only through your Telegram approve + TOTP + cool-down, out of band (P8-T005). Risk commands outside the 03 M20 Risk row (`risk.sleeve.restart`, `risk.capital.*`, `risk.review.close`) are `disabled` and not enableable for MCP in v1.
- Default **enabled**: `read`, `analyse` and `curation` scope tools. Default **disabled** (you enable them in D17, P8-T019): `trade`, `strategy` and `risk_tighten` tools. Enabling a trade/strategy/risk tool is C3; enabling a read/analyse/curation tool is C1; disabling anything is C1 (02 §7.2, D17).
- Default-deny: an operation missing from `registry.yaml` fails CI (completeness test) and is treated as `never` at runtime.
- Guard middleware `McpGuard`: for `source = mcp`, require state `enabled` and the tool's scope on the token, else 403 `tool_never_exposed` / `tool_disabled` / `scope_missing` plus an `audit.mcp_call` row (P8-T007).
- `/mcp/tools` returns group, scope, level, state, rate-limit class and calls/day (from `audit.mcp_call`); `mcp.tool.set` on a `never` tool → 409.
- A registry change publishes WS `system` event `mcp.registry.changed`.

## ToDo

- [ ] Write `registry.yaml` covering the whole current OpenAPI; classify never/enabled/disabled and scope per the rules above.
- [ ] Migration `ops.mcp_tool` with a check constraint that `never` rows can't change state.
- [ ] Implement the loader, `McpGuard` middleware, `/mcp/tools` query and `mcp.tool.set` command (web/Telegram only; levels via the P0 confirmation engine).
- [ ] CI test: every OpenAPI operation has exactly one registry entry; the never set equals the code constant and contains every 16 §2.12 / 02 §7.4 item.
- [ ] Write tests; update docs.

## Verification

### Tests
- Unit: classification loader; check constraint blocks `UPDATE … SET state='enabled'` on a never row.
- Unit: the never constant contains `approval.approve`, `approval.approve_partial`, `approval.reject`, every `mcp.*`, `wallet.sweep`, `airdrop.claim.execute`, `system.restore.test`, `memory.delete`, `system.service.restart`, `risk.deadman.ack`, `/system/keys`, `/system/logs`; and `risk.kill.off` is classified C3 for `source = mcp`.
- Integration: MCP token raw-POSTs `/commands/approval.approve` → 403 `tool_never_exposed` and an audit row; web `mcp.tool.set` on a never tool → 409.
- Integration: enabling `order.place` from web triggers C3 (Telegram + TOTP + cool-down); enabling `get_positions` is C1; disabling is immediate (C1).
- Property: for random OpenAPI fixtures, unknown operations are denied for MCP.

### Scenarios
- Given a new mt_api route added without a registry entry, when CI runs, then the completeness test fails.
- Given the trade group is disabled, when Claude calls `order_place` through a stale tool list, then mt_api answers 403 `tool_disabled`.
- Given a token without `risk_tighten`, when it calls `risk_policy_update`, then 403 `scope_missing`.
- Given you disable `position_close` in D17, when the registry event fires, then the tool disappears from the client and is refused immediately server-side.

### Stress / failure injection
- Guard overhead < 1 ms p99 at 1,000 req/s (registry cached in memory, invalidated on change).
- DB unavailable at startup: MCP calls refused (503) until the registry loads; web unaffected.

## Acceptance criteria

- [ ] No never-exposed operation can be called by an MCP principal or enabled by any command
- [ ] No scope applies a loosening (always C3 out of band); `approval.*` and `mcp.*` unreachable from MCP
- [ ] Completeness CI test is in place and green
- [ ] Enable trade/strategy/risk = C3, enable read/analyse/curation = C1, disable = C1, per D17
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- DB down: the guard fails closed for MCP (403/503); web unaffected.
- Registry cache stale after restart: reload from DB at startup before serving MCP.
- A never tool appears in an old client's cached list: the server refusal is authoritative.

## Cardinal rules (do NOT)

- Do NOT implement the filter only in `mt_mcp`; `mt_api` is the authority.
- Do NOT make never-exposed state data-driven or toggleable from any UI, Telegram or MCP path.
- Do NOT expose anything on the 16 §2.12 never-exposed list (withdrawals, `wallet.sweep`, `treasury.*` moves, `airdrop.claim.execute`, mandates, key/token management, `approval.*`, `mcp.*`, restore/delete, audit writes).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT update or delete WORM rows; corrections are new rows (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7.1 (`/mcp/tools`) and §7.4: registry as built.
- `docs/03-build-spec.md` M20 safeguards and `docs/07-security-notes.md` §6: confirm the never-exposed list matches the code constant.
- `docs/ui/dashboards/D17-mcp-console.md`: registry states, scopes and defaults.
- `docs/roadmap/phase-8-mcp.md`: progress on T8.21.

## Branch & PR

- Branch: `p8/P8-T004-tool-registry-never-exposed`
- PR title: `P8-T004: Tool registry and never-exposed filter in mt_api (/mcp/tools, mcp.tool.set)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T004` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (full 16 §2.12 / 02 §7.4 never-exposed list incl. `approval.*` and `mcp.*`, 16 §2.12 scopes per tool, loosening never a scope (always C3), enable levels per 02 §7.2; dropped gap deps P8-B001/B005; cross-phase dep P0-T035; tools/env/services)
