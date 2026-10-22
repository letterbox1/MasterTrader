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
depends_on: [P8-T005, P2-T038, P2-T039, P2-T149]
requirements: [R8.04, R8.07]
roadmap_todos: [T8.21]
modules: [M15, M20]
dashboards: [D01, D05, D17]
tools: [uv, pnpm, docker, git]
mcp: []
env: []
services: [postgres, nats, telegram-bot-api]
branch: p8/P8-T014-mcp-approval-cards
pr: ""
doc_sync: [docs/ui/mobile-and-telegram.md, docs/ui/dashboards/D05-execution.md, docs/15-bots-hitl-and-worm-audit.md, docs/roadmap/phase-8-mcp.md]
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

# P8-T014 · MCP source on approval cards (Telegram + web) and source badges

## Goal / expected outcome

Every MCP-originated order and C2 change raises your approval card on Telegram and web (15 §1.3: "MCP-originated orders always raise this approval card", TTL default 5 min, expiry = reject). The card clearly shows **source MCP**, the client identity and Claude's stated reason (as unverified text), plus the usual risk preview, TTL and buttons. You can tell an MCP request from a bot or your own ticket at a glance. Tested with a fake Telegram Bot API; no bot token needed.

## Context & references

- Roadmap: [R8.04, R8.07](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.21](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- HITL card: [15 §1.3](../../../docs/15-bots-hitl-and-worm-audit.md#13-hitl-approval-via-telegram) (order, risk preview, why, links, TTL; Approve / Approve ½ / Reject; TOTP for large orders; bound to your Telegram id)
- UI: [D17 Pending approvals](../../../docs/ui/dashboards/D17-mcp-console.md) (`ApprovalCard` with source "MCP" + conversation excerpt) · [D05 source badges](../../../docs/ui/dashboards/D05-execution.md)
- Decisions: [17 §A P8-B001/B002](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (MCP can never approve; C2 orders always your card, TTL 5 min) · [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) (large-order TOTP threshold) · [17 §D P2-B013…](../../../docs/17-decisions-register.md#d-other-decisions) (no bulk approve except the dynamic-selection batch card)
- Cross-phase (depends_on): P2-T038 (approvals API + `ApprovalCard`), P2-T039 (Telegram HITL cards), P2-T149 (web approvals queue, Cockpit Needs-you).

## Requirements

- Card header "MCP · <client identity>" plus an MCP badge; body adds "Claude says: <reason>" (length-capped setting, escaped, links stripped, labelled "unverified").
- Buttons unchanged: Approve · Approve ½ size · Reject (Pause bot only for bot orders). Large orders (> 2% of sleeve or > A$5,000 notional by default, 16 §2.3) need a TOTP reply on Telegram or hold-to-confirm on web.
- TTL countdown from the MCP approval TTL setting (default 5 min); on expiry the card shows "expired" and the request is rejected.
- Approvals accepted only from your bound Telegram user id or your web session (`web`/`telegram` sources); others ignored and alerted. There is no MCP path to these buttons.
- D05 orders and D01 Needs-you show the MCP source badge; the same `ApprovalCard` is used in D17.
- One card per MCP request: no batching or bulk approve for MCP (batching is reserved for dynamic-selection bots, 15 §1.3). Telegram sends are queued within the Bot API rate limit.

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
- Given two MCP orders within 5 s, then two separate cards are shown, each with its own TTL.

### Stress / failure injection
- 50 MCP approval requests in 10 s (above the write limit, so only the admitted ones create cards) → every admitted card delivered via the send queue; none lost; web queue shows all.

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
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (card mandatory for every MCP order, TTL 5 min, large-order TOTP default from 16 §2.3, no batching for MCP (bulk approve only for dynamic selection), approvals only from web/Telegram; cross-phase deps P2-T038/T039/T149; tools/env/services)
