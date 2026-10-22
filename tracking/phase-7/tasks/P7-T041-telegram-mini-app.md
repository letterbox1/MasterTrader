---
id: P7-T041
kind: task
title: Telegram Mini App for Cockpit, Approvals and Tasks (optional)
phase: 7
type: BUILD
status: backlog
priority: low
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T039]
requirements: [R7.12]
roadmap_todos: [T7.25]
modules: [M15]
dashboards: [D01, D13]
tools: [git, pnpm, node>=20, uv]
mcp: []
env: []
services: [mt-api, telegram bot api]
branch: p7/P7-T041-telegram-mini-app
pr: ""
doc_sync: [docs/ui/mobile-and-telegram.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T041 · Telegram Mini App for Cockpit, Approvals and Tasks (optional)

## Goal / expected outcome

An optional Telegram Mini App reuses the web routes for Cockpit, Approvals and Tasks inside Telegram, authenticated by validating Telegram init-data server-side and exchanging it for a scoped session.

## Context & references

- Roadmap: [R7.12 · ToDo T7.25](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [mob §3](../../../docs/ui/mobile-and-telegram.md#3-telegram-bot) (optional Mini App, signed init-data → session exchange) · [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (Telegram Bot API: minimal data)
- Related: P7-T039

## Requirements

- Init-data HMAC validated with the bot token (from sops); `auth_date` ≤ 60 s old; Telegram user id must equal the bound user id.
- Session scope: C0–C2 actions; C3 still requires the TOTP step; session TTL 15 min.
- Routes: `/cockpit`, `/approvals`, `/tasks` only; same components as web; viewport matrix applies.
- Served only via Tailscale (Mini App opened on a device on your tailnet); if unreachable, show a clear message.

## ToDo

- [ ] `POST /auth/telegram-miniapp` init-data exchange.
- [ ] Mini App route shell + Telegram theme mapping.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: init-data validation (valid, tampered hash, old auth_date, wrong user id).
- Playwright: routes render inside a Telegram WebApp emulator viewport.

### Scenarios
- Given a forwarded Mini App link opened by another Telegram user, then auth fails.

### Stress / failure injection
- n/a: optional single-user feature.

## Acceptance criteria

- [ ] Mini App works for the three routes with server-validated auth; or task cancelled as optional with a reason.
- [ ] CI green.

## Exceptions & edge cases

- Device not on tailnet: Mini App cannot reach the API; message shown, no fallback to public exposure.

## Cardinal rules (do NOT)

- Do NOT expose the API publicly to make the Mini App reachable.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).
- Do NOT put Telegram text into any model, RAG index or training set (12 §4–5).
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/ui/mobile-and-telegram.md` §3: Mini App auth details.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.25 when this item is done.

## Branch & PR

- Branch: `p7/P7-T041-telegram-mini-app`
- PR title: `P7-T041: Telegram Mini App for Cockpit, Approvals and Tasks (optional)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T041` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (tools/mcp/env/services only; no decision changes it)
