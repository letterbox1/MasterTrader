---
id: P8-T014
kind: task
title: MCP source on approval cards (Telegram + web) and source badges
phase: 8
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T005]
requirements: [R8.04, R8.07]
roadmap_todos: [T8.21]
modules: [M15, M20]
dashboards: [D01, D05, D17]
branch: p8/P8-T014-mcp-approval-cards
pr: ""
doc_sync: [docs/ui/mobile-and-telegram.md, docs/ui/dashboards/D05-execution.md, docs/15-bots-hitl-and-worm-audit.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T014 · MCP source on approval cards (Telegram + web) and source badges

## Goal / expected outcome

Approval cards for MCP-originated orders and changes clearly show **source MCP**, the client label and Claude's stated reason (as unverified text), plus the usual risk preview, TTL and buttons. You can tell an MCP request from a bot or your own ticket at a glance.

## Context & references

- Roadmap: [R8.04, R8.07](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.21](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- HITL card: [15 §1.3](../../../docs/15-bots-hitl-and-worm-audit.md#13-hitl-approval-via-telegram) (order, risk preview, why, links, TTL; Approve / Approve ½ / Reject; TOTP for large orders; bound to your Telegram id)
- UI: [D17 Pending approvals](../../../docs/ui/dashboards/D17-mcp-console.md) (`ApprovalCard` with source "MCP" + conversation excerpt) · [D05 source badges](../../../docs/ui/dashboards/D05-execution.md)
- Cross-phase: P2 R2.51 / T2.33 (approval buttons, C3 TOTP prompt), R2.54.

## Requirements

- Card header "MCP · <client_label>" plus an MCP badge; body adds "Claude says: <reason>" (≤ 280 chars, escaped, links stripped, labelled "unverified").
- Buttons unchanged: Approve · Approve ½ · Reject (Pause bot only for bot orders). Large orders above the notional threshold need a TOTP reply (15 §1.3).
- Approvals accepted only from your bound Telegram user id; others ignored and alerted.
- D05 orders and D01 Needs-you show the MCP source badge; the same `ApprovalCard` is used in D17.
- Telegram rate ≤ 30 msg/s; several MCP requests within 10 s may be batched into one card with per-line toggles (15 §1.3 batching).

## ToDo

- [ ] Extend the Telegram card renderer and web `ApprovalCard` with `source`/`client_label`/`reason`.
- [ ] Escape/sanitise the excerpt (Telegram MarkdownV2/HTML).
- [ ] Tests (golden message JSON, Playwright for web card).
- [ ] Update docs.

## Verification

### Tests
- Golden: Telegram message JSON for an MCP order card and an MCP C3 risk-loosening card.
- Unit: an excerpt containing Markdown links, `<a>` tags, fake button text or 5,000 chars is escaped/stripped/truncated.
- Integration: an approval tap from a different Telegram id is ignored and alerts.
- Playwright: D05 badge and D17 card render at 390×844 and 1920×1080.

### Scenarios
- Given Claude's reason contains "[Approve](https://evil)", when the card renders, then no link or extra button appears.
- Given two MCP orders within 5 s, then one batched card with two toggles is shown.

### Stress / failure injection
- 50 MCP approval requests in 10 s → batched; Telegram send rate ≤ 30 msg/s; none lost.

## Acceptance criteria

- [ ] MCP cards show source, client and escaped reason; buttons and TOTP rules unchanged
- [ ] Badges visible in D01/D05/D17
- [ ] CI green (lint, types, tests, `pit` check, viewport matrix + axe)

## Exceptions & edge cases

- Telegram down: the card is still in the web approvals queue (D01/D17).
- Card edited after TTL: it shows "expired" and buttons are removed.

## Cardinal rules (do NOT)

- Do NOT render links, buttons or formatting from Claude-supplied text.
- Do NOT accept approvals from any Telegram id but yours.
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT commit secrets or paste them into chats/issues (including into the Claude conversation); secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

## Doc sync on completion

- `docs/ui/mobile-and-telegram.md` §3: MCP card variant.
- `docs/ui/dashboards/D05-execution.md`: MCP badge.
- `docs/15-bots-hitl-and-worm-audit.md` §1.3: MCP source line.
- `docs/roadmap/phase-8-mcp.md`: progress on T8.21.

## Branch & PR

- Branch: `p8/P8-T014-mcp-approval-cards`
- PR title: `P8-T014: MCP source on approval cards (Telegram + web) and source badges`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T014` run

## Progress log

- 2026-10-21 00:00 · planner · created
