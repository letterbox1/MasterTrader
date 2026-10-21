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
depends_on: [P8-T004, P8-T005, P8-T007, P8-T014, P8-T015]
requirements: [R8.07]
roadmap_todos: [T8.22]
modules: [M15, M20]
dashboards: [D17]
branch: p8/P8-T016-d17-mcp-console
pr: ""
doc_sync: [docs/ui/dashboards/D17-mcp-console.md, docs/ui/README.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T016 · D17 MCP Console

## Goal / expected outcome

The `/mcp` route shows the MCP control and audit surface exactly as D17 specifies: connection, tool registry, pending approvals pinned on top, session activity, and the actions `mcp.tool.set`, `mcp.policy.set`, token create/revoke and approve/reject. It passes the full viewport matrix and is hidden from nav until MCP is enabled.

## Context & references

- Roadmap: [R8.07](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.22](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Dashboard: [D17 MCP Console](../../../docs/ui/dashboards/D17-mcp-console.md) (layout by tier, widgets, actions, acceptance criteria, backend contract)
- UI rules: [ui §3.3 confirmations](../../../docs/ui/README.md#33-actions--confirmation) · [DESIGN §6.8 viewport matrix](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)
- Cross-phase: P0 R0.11 (shell), R0.N6 (viewport matrix CI); P2 approvals queue (R2.51).
- Related: P8-T002 (tokens), P8-T004 (registry), P8-T005 (policy), P8-T007 (audit), P8-T014 (ApprovalCard).

## Requirements

- Widgets: **Connection** (`/system/services?kind=mcp`: status, transport, clients, token expiry) · **Tool registry** (`/mcp/tools`: grouped Read & analyse / Talk to agents / Trade & adjust / Strategies / Risk / Curation; enabled, level, rate limit, calls/day; never-exposed greyed with a lock) · **Pending approvals** (`/orders?status=pending_approval&source=mcp`, `/risk/changes?status=pending&source=mcp`) · **Session activity** (`/audit/log?source=mcp`, `/mcp/sessions`: time, client, calls with args redacted, results, linked audit entries, token).
- Actions: enable tool (trade/risk/strategies = C3, others C1), disable (C1), `mcp.policy.set` (loosen C3, tighten C1), token create (C1 read / C3 write scopes; shown once with copy button and a "store in keychain/sops, never chat" notice), `mcp.token.revoke` (C1), approve/reject.
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
- Viewport matrix 240×320 → 2560×1440 (DESIGN §6.8) + axe: no violations.

### Scenarios
- Given an MCP close order pending, when you open D17 on your phone, then the card is the first thing shown and Approve works with hold-to-confirm.
- Given a token expiring in 3 days, then Connection shows an amber expiry chip.

### Stress / failure injection
- 10,000 session rows: scroll at 60 fps on a mid-range laptop; WS gap → refetch via REST and resume.

## Acceptance criteria

- [ ] All D17 widgets and actions work with the documented levels
- [ ] D17 acceptance criteria 1–2 demonstrably hold
- [ ] Viewport matrix + axe green; hidden from nav when MCP is disabled
- [ ] CI green (lint, types, tests, `pit` check, viewport matrix + axe)

## Exceptions & edge cases

- mt-api down: web unreachable (02 §9.3); Telegram remains for approvals and `/kill`.
- Postgres down: read-only banner; actions disabled.
- Kill ON: trade-tool enable actions disabled with a reason.

## Cardinal rules (do NOT)

- Do NOT show token plaintext again after creation, or key values ever.
- Do NOT enforce levels only in the UI; the server decides.
- Do NOT expose withdrawals, API-key management or wallet mandate signing through MCP, in any form (R8.06).
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

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
