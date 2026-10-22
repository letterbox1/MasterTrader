---
id: P8-T008
kind: task
title: Read & analyse tool group
phase: 8
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T003, P8-T004, P8-T006, P8-T007, P2-T020, P2-T036, P2-T117, P4-T043]
requirements: [R8.01, R8.03]
roadmap_todos: [T8.20]
modules: [M20, M15, M16, M18]
dashboards: [D17]
tools: [uv, docker, git]
mcp: []
env: []
services: [postgres, nats]
branch: p8/P8-T008-tools-read-analyse
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

# P8-T008 · Read & analyse tool group

## Goal / expected outcome

Claude can answer "how are my strategies doing?"-type questions using read-only MCP tools generated from `mt_api` queries that cover the 03 M20 read & analyse scope, including `/bots`, `/approvals` and the `source=` filters. All are C0, need the `read` scope and are enabled by default. Tested with the SDK client against seeded fixtures.

## Context & references

- Roadmap: [R8.01, R8.03](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.20](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Spec: [03 M20 Read & analyse row](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7.1 queries](../../../docs/02-v1-architecture.md#71-queries-rest-read) (incl. `/bots`, `/approvals?status=&source=`, `/orders?source=`)
- Decisions: [17 §D P8-B009](../../../docs/17-decisions-register.md#d-other-decisions) (`/bots`, `/approvals`, `source=` filters) · [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) (scopes; 60 reads/min default)
- Bots queries: [15 §1.5](../../../docs/15-bots-hitl-and-worm-audit.md#15-api-data-and-ui)
- Cross-phase (depends_on): P2-T020 (risk/order queries), P2-T036 (bots queries), P2-T117 (lab queries), P4-T043 (intel queries).
- Related: P8-T003 (generator), P8-T004 (registry), P8-T006 (guard), P8-T007 (audit), P8-T030 (limits).

## Requirements

- Tool ↔ endpoint map (registry entries, scope `read`, state `enabled`, C0):
  - Positions, orders, fills → `/positions`, `/orders` (incl. `source=`), `/fills`.
  - P&L, exposure, drawdown → `/portfolio/summary`, `/risk/state`, `/risk/policy`, `/risk/changes` (incl. `source=`).
  - Strategy status and performance → `/strategies`, `/strategies/{id}`, `/strategies/{id}/runs`, `/bots`, `/bots/{id}`, `/bots/{id}/approvals`, `/approvals?status=&source=`.
  - Backtest/experiment results → `/lab/backtests` (+ `/{id}`), `/lab/experiments`, `/lab/jobs`.
  - Cost/TCA and DQ status → `/data/costs`, `/data/dq-events`, `/data/feeds`, `/data/recon`.
  - Market data and features → `/markets/instruments`, `/markets/{id}/bars` (page size a setting), `/markets/{id}/book`, `/markets/matrix`.
  - News/event summaries → `/intel/documents`, `/intel/events`, `/intel/calendar`, `/intel/sentiment` (guarded by P8-T006).
  - Journal/tax summaries → `/journal/trades`, `/tax/summary?fy=` (PII redacted).
  - Task queue → `/tasks`; risk dry-run → `POST /risk/preview` (no side effects, C0).
- Never exposed (P8-T004): `/system/keys`, `/system/logs`. Disabled by default (enable later via `mcp.tool.set`, C1): `/wallets*`, `/treasury*`, `/tax/residency`, `/tax/reports` downloads, `/airdrops/mandates`.
- Each tool description states units (AUD base, decimals as strings, UTC) and pagination; `as_of` is passed through where the endpoint supports it.
- Rate limit class `read` (default 60 reads/min per token, 16 §2.12, enforced by P8-T030); results capped at 256 KB with a marker and a cursor.
- No new endpoints for convenience; if a needed query is missing, file a gap against the owning phase.

## ToDo

- [ ] Add the registry entries (scope `read`, state `enabled`, class `read`) and regenerate `tools.snapshot.json`.
- [ ] Write tool descriptions in the OpenAPI summaries (source of truth) so the generator picks them up.
- [ ] Contract tests per tool against mt_api fixtures.
- [ ] Update docs.

## Verification

### Tests
- Contract: each read tool against seeded fixtures returns the documented shape (golden JSON).
- Guard: `/intel/documents` via MCP never returns Telegram text (re-uses P8-T006 fixtures).
- Pagination: `get_fills` with 12,000 fills walks all pages via cursor.
- `get_approvals(source=mcp)` returns only MCP-originated approvals.
- Snapshot: read group in `tools.snapshot.json` reviewed.

### Scenarios
- Given 3 running strategies, when you ask "how are my strategies doing?", then Claude calls `get_strategies` + `get_portfolio_summary` and every call shows in D17.
- Given a stale feed, when Claude asks for DQ status, then `get_data_feeds` shows the instrument as `stale`.
- Given a `read`-only token, when Claude calls `get_wallets`, then 403 `tool_disabled`.

### Stress / failure injection
- 60 reads/min sustained for 1 h within the rate limit; p95 tool latency < 300 ms for summary endpoints (target).

## Acceptance criteria

- [ ] Every M20 read item has a tool, all C0, `read` scope, enabled; `/bots`, `/approvals` and `source=` filters included
- [ ] Never/disabled endpoints aren't listed and are refused server-side
- [ ] Contract tests green; snapshot reviewed
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Postgres down: UI is read-only per 02 §9.3, and MCP reads return 503.
- Venue disconnect: positions carry `unconfirmed`; Claude sees that flag (it's in the payload).
- Huge bar ranges: paged; results over 256 KB are capped with a marker.

## Cardinal rules (do NOT)

- Do NOT add new mt_api endpoints just for MCP convenience or put aggregation logic in `mt_mcp`.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set; Claude via MCP counts as a model input (12 §4–5).
- Do NOT expose anything on the 16 §2.12 never-exposed list.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M20: read tool list.
- `docs/ui/dashboards/D17-mcp-console.md`: Read & analyse group contents.
- `docs/roadmap/phase-8-mcp.md`: progress on T8.20.

## Branch & PR

- Branch: `p8/P8-T008-tools-read-analyse`
- PR title: `P8-T008: Read & analyse tool group`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T008` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (`/bots`, `/approvals`, `source=` filters now in 02 §7.1; `read` scope; 60 reads/min and 256 KB cap via P8-T030; never list per 16 §2.12; cross-phase deps P2-T020/T036/T117, P4-T043; tools/env/services)
