---
id: P8-T016
kind: task
title: D17 MCP Console
phase: 8
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T002, P8-T004, P8-T005, P8-T007, P8-T014, P8-T015, P0-T049, P0-T050]
requirements: [R8.07, R8.08]
roadmap_todos: [T8.22]
modules: [M15, M20]
dashboards: [D17]
tools: [pnpm, uv, docker, git]
mcp: []
env: []
services: [postgres, nats]
branch: p8/P8-T016-d17-mcp-console
pr: ""
doc_sync: [docs/ui/dashboards/D17-mcp-console.md, docs/ui/README.md, docs/roadmap/phase-8-mcp.md]
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

# P8-T016 · D17 MCP Console

## Goal / expected outcome

The `/mcp` route shows the MCP control and audit surface exactly as D17 specifies: connection, tokens, tool registry, pending approvals pinned on top, session activity, and the actions `mcp.tool.set`, `mcp.policy.set`, `mcp.token.create`/`revoke` and approve/reject (all web/Telegram only, never exposed to MCP). It passes the full viewport matrix and is hidden from nav until MCP is enabled. Built against mocked API fixtures and the test stack.

## Context & references

- Roadmap: [R8.07](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.22](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Dashboard: [D17 MCP Console](../../../docs/ui/dashboards/D17-mcp-console.md) (layout by tier, widgets, actions, acceptance criteria, backend contract)
- UI rules: [ui §3.3 confirmations](../../../docs/ui/README.md#33-actions--confirmation) · [DESIGN §6.8 viewport matrix](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)
- Decisions: [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) (token expiry options, indefinite = red warning + C3 + monthly reminder; scopes; limits) · [17 §A P8-B001/B002/B004](../../../docs/17-decisions-register.md#a-s2-items-all-resolved)
- Cross-phase (depends_on): P0-T049 (component library, confirm sheets), P0-T050 (app shell + nav); P2 approvals queue via P8-T014.
- Related: P8-T002 (tokens), P8-T004 (registry), P8-T005 (policy), P8-T007 (audit), P8-T014 (ApprovalCard).

## Requirements

- Widgets: **Connection** (`/system/services?kind=mcp`: status, transport (Streamable HTTP on Tailscale/TLS; stdio locally; optional legacy HTTP+SSE), connected clients) · **Tokens** (`/mcp/tokens`: name, scopes `read`/`analyse`/`trade`/`strategy`/`risk_tighten`/`curation`, created, expiry, last used + client identity, rate limits; never the secret) · **Tool registry** (`/mcp/tools`: grouped Read & analyse / Talk to agents / Trade & adjust / Strategies / Risk / Curation; enabled, level (orders always create an approval card), rate limit (defaults 60 reads/min, 10 writes/min per token; 256 KB cap), calls/day; never-exposed list greyed with a lock) · **Pending approvals** (`/approvals?status=pending&source=mcp`, `/risk/changes?status=pending&source=mcp`; `ApprovalCard` with source MCP + excerpt, TTL default 5 min) · **Session activity** (`/mcp/sessions`, `/audit/log?source=mcp` from `audit.mcp_call`: time, client, every call incl. reads with args redacted, results, linked audit entries, token).
- Actions: `mcp.tool.set` (enable a trade/strategy/risk tool C3, a read/analyse/curation tool C1; disable C1; never-exposed can't be enabled) · `mcp.policy.set` (tighten C1, loosen C3; **no** skip-approval or auto-execute control exists) · `mcp.token.create` (expiry picker 1 day · 7 days · 30 days · 1 year · custom · indefinite; C1 for `read`/`analyse`/`curation`; C3 for `trade`/`strategy`/`risk_tighten` or indefinite; indefinite shows the red exposure/security warning; token shown once with copy button and a "store in keychain/sops, never chat" notice) · `mcp.token.revoke` (C1, immediate) · approve (C2) / reject (C1).
- Never-exposed rows have no enable control (not focusable, `aria-disabled`, lock icon + tooltip).
- Layout: ≥ xl tool registry (12) + session activity (12) with pending approvals pinned top; ≤ ph pending → sessions → tools.
- WS topics `orders`, `risk.event`, `system`; live update p95 < 500 ms; "Re-syncing" chip on WS gap.
- Route hidden from nav until `mcp.enabled`; destructive controls ≥ 8 px from safe ones; idempotency key per confirm sheet.

## ToDo

- [ ] Build the route, widgets and actions on the DESIGN v2 Tailwind preset.
- [ ] Virtualise the session list (10k rows).
- [ ] Playwright E2E + viewport matrix + axe.
- [ ] Update docs.

## Verification

### Tests
- Component tests per widget with mocked API.
- Playwright E2E: enable `order_place` shows the C3 "Approval sent to Telegram" state with countdown, then cool-down timer; revoke a token → session shows revoked and the next MCP call fails.
- Playwright: never-exposed rows can't be enabled by click, keyboard or a direct API call from the page.
- Playwright: token create offers all six expiry options; choosing indefinite shows the red warning and routes through C3; the secret is shown once and gone after closing the sheet.
- Playwright: no control anywhere offers skip-approval or auto-execute.
- Viewport matrix 240×320 → 2560×1440 (DESIGN §6.8) + axe: no violations.

### Scenarios
- Given an MCP close order pending, when you open D17 on your phone, then the card is the first thing shown and Approve works with hold-to-confirm.
- Given a token expiring in 3 days, then Tokens shows an amber expiry chip; an indefinite token shows a red chip.

### Stress / failure injection
- 10,000 session rows: scroll at 60 fps on a mid-range laptop; WS gap → refetch via REST and resume.

## Acceptance criteria

- [ ] All D17 widgets and actions work with the documented levels
- [ ] D17 acceptance criteria 1–3 demonstrably hold (confirmation mapping, never-exposed locked, token expiry incl. indefinite → C3)
- [ ] Viewport matrix + axe green; hidden from nav when MCP is disabled
- [ ] CI green (lint, types, tests, `pit` check, viewport matrix + axe)

## Exceptions & edge cases

- mt-api down: web unreachable (02 §9.3); Telegram remains for approvals and `/kill`.
- Postgres down: read-only banner; actions disabled.
- Kill ON: trade-tool enable actions disabled with a reason.

## Cardinal rules (do NOT)

- Do NOT show token plaintext again after creation, or key values ever.
- Do NOT enforce levels only in the UI; the server decides.
- Do NOT offer a skip-approval or auto-execute option for MCP orders, or any way to enable a never-exposed tool.
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/ui/dashboards/D17-mcp-console.md`: final widget/actions as built (token create).
- `docs/ui/README.md`: nav entry "MCP" visibility rule.
- `docs/roadmap/phase-8-mcp.md`: tick T8.22.

## Branch & PR

- Branch: `p8/P8-T016-d17-mcp-console`
- PR title: `P8-T016: D17 MCP Console`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T016` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (Tokens widget with 16 §2.12 expiry options and indefinite warning + C3, scope names, `/approvals?source=mcp`, `/mcp/sessions`, `/mcp/tokens`, limit defaults shown, no skip-approval control, D17 AC 1–3; added R8.08; cross-phase deps P0-T049/T050; tools/env/services)
