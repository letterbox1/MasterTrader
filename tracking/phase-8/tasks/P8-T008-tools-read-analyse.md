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
depends_on: [P8-T003, P8-T004, P8-T006, P8-T007]
requirements: [R8.01, R8.03]
roadmap_todos: [T8.20]
modules: [M20, M15, M16, M18]
dashboards: [D17]
branch: p8/P8-T008-tools-read-analyse
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

# P8-T008 · Read & analyse tool group

## Goal / expected outcome

Claude can answer "how are my strategies doing?"-type questions using read-only MCP tools generated from `mt_api` queries that cover the 03 M20 read & analyse scope. All are C0, `read` scope and enabled by default.

## Context & references

- Roadmap: [R8.01, R8.03](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.20](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Spec: [03 M20 Read & analyse row](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7.1 queries](../../../docs/02-v1-architecture.md#71-queries-rest-read)
- Bots queries: [15 §1.5](../../../docs/15-bots-hitl-and-worm-audit.md#15-api-data-and-ui)
- Related: P8-T003 (generator), P8-T004 (registry), P8-T006 (guard), P8-T007 (audit); gap P8-B009 (`/bots`, `/approvals` missing from 02 §7.1).

## Requirements

- Tool ↔ endpoint map (registry entries, group `read`):
- Map: Positions, orders, fills → `/positions`, `/orders`, `/fills`
- Map: P&L, exposure, drawdown → `/portfolio/summary`, `/risk/state`
- Map: Strategy status and performance → `/strategies`, `/strategies/{id}`, `/strategies/{id}/runs`, `/bots`, `/bots/{id}` (15 §1.5)
- Map: Backtest/experiment results → `/lab/backtests` (+ `/{id}`), `/lab/experiments`, `/lab/jobs`
- Map: Cost/TCA and DQ status → `/data/costs`, `/data/dq-events`, `/data/feeds`, `/data/recon`
- Map: Market data and features → `/markets/instruments`, `/markets/{id}/bars` (≤ 5,000 bars per call), `/markets/{id}/book`, `/markets/matrix`
- Map: News/event summaries → `/intel/documents`, `/intel/events`, `/intel/calendar`, `/intel/sentiment` (guarded by P8-T006)
- Map: Journal/tax summaries → `/journal/trades`, `/tax/summary?fy=` (PII redacted)
- Map: Task queue → `/tasks`; risk dry-run → `POST /risk/preview` (no side effects, C0)
- Excluded from this group (never or disabled): `/system/keys`, `/system/logs`, `/airdrops/mandates`, `/tax/residency`, `/tax/reports` downloads, `/wallets*`, `/treasury*` (out of M20 read scope; enable later only via `mcp.tool.set`).
- Each tool description states units (AUD base, decimals as strings, UTC) and pagination; `as_of` is passed through where the endpoint supports it.
- No new endpoints for convenience; if a needed query is missing, file a gap against the owning phase.

## ToDo

- [ ] Add the registry entries (group `read`, state `enabled`, rate limit 60/min) and regenerate `tools.snapshot.json`.
- [ ] Write tool descriptions in the OpenAPI summaries (source of truth) so the generator picks them up.
- [ ] Contract tests per tool against mt_api fixtures.
- [ ] Update docs.

## Verification

### Tests
- Contract: each read tool against seeded fixtures returns the documented shape (golden JSON).
- Guard: `/intel/documents` via MCP never returns a Telegram doc (re-uses P8-T006 fixtures).
- Pagination: `get_fills` with 12,000 fills walks all pages via cursor.
- Snapshot: read group in `tools.snapshot.json` reviewed.

### Scenarios
- Given 3 running strategies, when you ask "how are my strategies doing?", then Claude calls `get_strategies` + `get_portfolio_summary` and every call shows in D17.
- Given a stale feed, when Claude asks for DQ status, then `get_data_feeds` shows the instrument as `stale`.

### Stress / failure injection
- 60 reads/min sustained for 1 h within the rate limit; p95 tool latency < 300 ms for summary endpoints (proposed target).

## Acceptance criteria

- [ ] Every M20 read item has a tool, all C0, `read` scope, enabled
- [ ] Excluded endpoints aren't listed and are refused server-side
- [ ] Contract tests green; snapshot reviewed
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Postgres down: UI is read-only per 02 §9.3, and MCP reads return 503.
- Venue disconnect: positions carry `unconfirmed`; Claude must see that flag (it's in the payload).
- Huge bar ranges: capped at 5,000 bars; Claude must page.

## Cardinal rules (do NOT)

- Do NOT add new mt_api endpoints just for MCP convenience or put aggregation logic in `mt_mcp`.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set; Claude via MCP counts as a model input (12 §4–5).
- Do NOT expose withdrawals, API-key management or wallet mandate signing through MCP, in any form (R8.06).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

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
