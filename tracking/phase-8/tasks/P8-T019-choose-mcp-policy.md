---
id: P8-T019
kind: task
title: Choose token scopes and expiry per client and enable the write tool groups you want
phase: 8
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P8-T016, P8-T018]
requirements: [R8.04, R8.08]
roadmap_todos: [T8.03]
modules: [M20, M11]
dashboards: [D17]
tools: [claude-desktop]
mcp: []
env: []
services: [tailscale, telegram-bot]
branch: p8/P8-T019-choose-mcp-policy
pr: ""
doc_sync: [docs/roadmap/phase-8-mcp.md]
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

# P8-T019 · Choose token scopes and expiry per client and enable the write tool groups you want

## Goal / expected outcome

For each MCP client you use, you've chosen its token scopes and expiry, enabled the trade, strategy and risk tools you want, and recorded the choices. Every write-scope token and every enable went through C3. MCP orders always need your approval card; there is no option to skip it.

## Context & references

- Roadmap: [R8.04, R8.08](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.03](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Decisions: [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) (scopes; `trade` creates approval cards only; C3 for `trade`/`strategy`/`risk_tighten` and indefinite) · [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) (MCP orders always need your card, TTL 5 min) · [17 §D P8-B010](../../../docs/17-decisions-register.md#d-other-decisions) (no skip-approval)
- Spec: [03 M20 safeguards](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [12 §4 Anthropic row](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (human approval on trade decisions)
- UI: [D17 Tokens + Tool registry](../../../docs/ui/dashboards/D17-mcp-console.md)
- Unblocks P8-T028, P8-T029, P8-T035.

## Requirements

- Per client: label, scopes (`read`, `analyse`, `curation` C1; `trade`, `strategy`, `risk_tighten` C3), expiry (1 day · 7 days · 30 days · 1 year · custom · indefinite; indefinite = red warning + C3 + monthly reminder).
- Enabling each trade/strategy/risk tool is C3 (Telegram approve + TOTP + cool-down, default 15 min); enabling read/analyse/curation tools is C1; disabling later is C1 and instant.
- Optional tightening in `mcp.policy.set` (C1): lower rate limits, a venue allow-list for MCP orders. Loosening those is C3. There is no skip-approval setting.
- Only if your P8-T001 decision was `go-full`; with `go-read-only` you keep read/analyse/curation only.

## ToDo

- [ ] Decide per client: scopes and expiry (an expiring token is recommended).
- [ ] D17 → Tokens: create the write-scope token(s) (C3 on Telegram with TOTP; wait out the cool-down); store as in P8-T018; revoke the read-only token if it's replaced.
- [ ] D17 → Tool registry: enable the Trade & adjust, Strategies and Risk tools you want (each C3).
- [ ] Optional: tighten limits or set a venue allow-list in D17 → Policy.
- [ ] Check `/mcp/tools` and `/mcp/tokens` in D17 show what you expect.
- [ ] Write the choices in the Progress log (clients, scopes, expiry, tools enabled, policy tightening or "none"; no token values).

## Verification

### Tests
- n/a: user configuration; confirmed by D17 state and the `audit.command` rows of the C3 approvals.

### Scenarios
- Given `order_place` is enabled, when Claude places any order, then it waits for your card on Telegram/web.
- Given you enable `order_place`, when the cool-down ends, then the tool appears in your client (tools list refresh).
- Given you look for an "auto-approve" option in D17, then there is none.

### Stress / failure injection
- n/a: one-off configuration.

## Acceptance criteria

- [ ] Scopes and expiry chosen and recorded per client
- [ ] Chosen write tools enabled via C3 and visible in D17

## Exceptions & edge cases

- You change your mind during the cool-down: cancel the pending C3 in D17.
- Kill ON while enabling: enable still possible, but trade tools return `kill_on` until you turn kill off (C3).

## Cardinal rules (do NOT)

- Do NOT approve C3 cards you didn't start yourself.
- Do NOT choose indefinite expiry without accepting the warning on purpose.
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT commit secrets or paste them into chats/issues (including the Claude conversation); secrets live in the sops/age file (07 §2).
- Do NOT use live money before the P7 gates; keys stay trade-only, IP-locked, withdrawals disabled.

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: tick T8.03 with the chosen scopes/expiry.

## Branch & PR

- Branch: `p8/P8-T019-choose-mcp-policy`
- PR title: `P8-T019: Choose token scopes and expiry per client and enable the write tool groups you want`
- PR checklist: no PR (user setup) · Progress log entry written · `./kanban done P8-T019` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (T8.03 is now scopes + expiry per client; auto rules / skip-approval removed (17 §D P8-B010); write-scope tokens and tool enables are C3; dropped gap dep P8-B010; added R8.08; tools/env/services)
