---
id: P2-T149
kind: task
title: Web approvals queue: D05 Approvals tab, history, bulk approve and Cockpit Needs-you
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T140, P2-T147]
requirements: [R2.51, R2.20, R2.54]
roadmap_todos: [T2.32]
modules: [M15, M11]
dashboards: [D05, D01]
branch: p2/P2-T149-web-approvals-queue
pr: ""
doc_sync: [docs/ui/dashboards/D05-execution.md, docs/ui/dashboards/D01-cockpit.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T149 · Web approvals queue: D05 Approvals tab, history, bulk approve and Cockpit Needs-you

## Goal / expected outcome

The web approvals queue in part B's dashboards — D05 Approvals tab (pending + history of approved/rejected/expired, bulk approve) and the Cockpit Needs-you tile — built on part A's `ApprovalCard`, approvals API and top-bar sheet, actionable in ≤ 2 taps on a phone.

## Context & references

- Roadmap: [R2.51, R2.20, R2.54](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) (web side; Telegram side is part A T2.33/T2.34) · ToDo T2.32 · exit criterion 2
- [D05 Approvals](../../../docs/ui/dashboards/D05-execution.md) · [ui §2.1 top bar approvals](../../../docs/ui/README.md#2-app-shell-all-routes) · [15 §1.3 approval card](../../../docs/15-bots-hitl-and-worm-audit.md#13-hitl-approval-via-telegram) · [mob §2 approve flow](../../../docs/ui/mobile-and-telegram.md) · approvals spec mismatches in P2-B058
- From part A (P2-T001–T099): `/approvals` API, WS approval events, `approval.approve|reject|approve_partial`, `ApprovalCard` and the top-bar approvals sheet (currently P2-T038); TTL/expiry enforcement (T2.25/T2.34)

## Requirements

- List pending requests (strategy and bot) with `ApprovalCard`: order, risk preview (R and % of sleeve, exposure after fill, blackout/DQ warnings), why (signal reasons), chart deep link, TTL countdown, source badge.
- Actions: Approve (C2 hold-to-confirm), Approve ½ (bot requests), Reject (C1), Pause bot; large orders show the extra confirmation requirement.
- Bulk approve ≤ 5 items from the same strategy with a combined risk preview (C2).
- Expiry is decided server-side; the UI moves expired items to history and never sends late approvals (server rejects them anyway).
- Decisions taken on Telegram update the web card within 1 s via WS (`orders` approval events / `risk.approval.result`).
- D05 tab badge count matches the top-bar count from part A; background tabs still receive approvals at full rate (ui §3.4).
- Phone: notification/Telegram deep link → card → hold-to-confirm in ≤ 2 taps (D05 acceptance 1).

## ToDo

- [ ] Approvals tab + history in D05 using part A's `ApprovalCard`
- [ ] Bulk approve (≤ 5, same strategy) with combined RiskPreview
- [ ] Needs-you integration in D01 (top 3 + count)
- [ ] Playwright approve/reject/expire/bulk flows; matrix; doc sync

## Verification

### Tests
- Playwright: DESIGN.md §6.8 viewport matrix (overflow + fixed-bar overlap checks) and axe on the new routes; Vitest + Testing Library for components.
- Playwright: approve on 390×844 in ≤ 2 taps after opening; expiry fixture moves item to history; Telegram-side decision reflected < 1 s.

### Scenarios
- Given a request with 60 s TTL, when the user approves at 61 s, then the server rejects as expired and the card shows 'expired — not executed'.
- Given 6 selected requests, then bulk approve is disabled ('max 5, same strategy').
- Given a protective stop from an HITL bot, then it never appears in the queue (executes automatically).

### Stress / failure injection
- 50 pending requests arriving in 10 s: queue stays responsive; countdowns accurate to ±1 s.

## Acceptance criteria

- [ ] D05 acceptance 1 (≤ 2 taps) passes on phone viewports
- [ ] Telegram/web decisions stay consistent
- [ ] Viewport matrix + axe green
- [ ] CI green (lint, types, tests, viewport matrix where UI)

## Exceptions & edge cases

- Session expired (12 h): approving requires re-login + TOTP; TTL keeps running.
- mt-api down: web approvals unavailable; Telegram path (part A) still works.

## Cardinal rules (do NOT)

- Do NOT enforce confirmation levels only in the UI; C1–C3/Kill are enforced server-side by `mt_api`.
- Do NOT use `100vh`/`h-screen`, unprefixed multi-column grids or the Tailwind CDN (DESIGN.md §6.3–6.5).
- Do NOT sum or show paper and live money without a mode label.
- Do NOT queue approvals offline or retry an approval after TTL.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT let any UI/API path loosen risk, enable autonomous mode or turn the kill switch off without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/dashboards/D05-execution.md`: Approve ½ / Pause bot on the web card (P2-B058).
- `docs/ui/dashboards/D01-cockpit.md`: Needs-you reads `/approvals` (P2-B058).
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.32 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T149-web-approvals-queue`
- PR title: `P2-T149: Web approvals queue: D05 Approvals tab, history, bulk approve and Cockpit Needs-you`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T149` run · Playwright viewport matrix + axe green

## Progress log

- 2026-10-21 00:00 · planner · created
