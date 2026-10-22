---
id: P1-T051
kind: task
title: Build the notifications centre
phase: 1
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T045, P1-T046, P0-T050]
requirements: [R1.15, R1.14]
roadmap_todos: [T1.32]
modules: [M15]
dashboards: [D07]
tools: [git, pnpm, node>=20]
mcp: []
env: []
services: [mt-api]
branch: p1/P1-T051-ui-notifications-centre
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/ui/README.md]
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

# P1-T051 · Build the notifications centre

## Goal / expected outcome

The top-bar notifications icon shows an unread count and opens a notification centre listing alerts (DQ, quota, recon, venue health, system) with severity, time, link to the source screen and per-channel delivery status.

## Context & references

- Roadmap: requirements [R1.15](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.14](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.32](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Shell: [ui §2 top bar](../../../docs/ui/README.md#21-top-bar-always-visible) (notifications icon + unread count) · [ui components](../../../docs/ui/components.md) (`TopBar.notificationsCount`) · [mobile & Telegram](../../../docs/ui/mobile-and-telegram.md)
- Data: `ops.notification` from P1-T045 via `/notifications` and WS `notifications`
- Depends on (this phase): P1-T045, P1-T046
- Cross-phase prerequisites (depends_on): P0-T050 (app shell)

## Requirements

- Sheet/drawer listing notifications newest first, virtualised, filter by severity/kind; mark read (C0)
- Each item links to its screen (DQ incident → D07 Quality filtered; recon → D07 Reconciliation)
- Shows delivery result per channel (Telegram/email/ntfy) for audit of the alert path
- Phone (≤ ph): full-screen sheet; desktop: right drawer

## ToDo

- [ ] Build the component and wire `/notifications` + WS
- [ ] Unread badge in `TopBar`
- [ ] Playwright matrix + axe
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Component: unread count updates on WS message; mark-read persists
- Playwright: matrix; keyboard navigation and focus trap in the drawer

### Scenarios

- Given a critical DQ alert, when it arrives, then the badge increments within 500 ms and the item links to the incident

### Stress / failure injection

- Load: 5k notifications list scrolls smoothly (virtualised)

## Acceptance criteria

- [ ] Notification centre works at every viewport; links resolve; delivery status visible
- [ ] CI green (lint, types, tests, Playwright viewport matrix 240→2560 px per DESIGN §6.8, axe)

## Exceptions & edge cases

- Notifications are not WORM; marking read never alters `audit.*`

## Cardinal rules (do NOT)

- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.32 once every task traced to it in PHASE.md is done; note P1-T051 next to it.
- `docs/ui/README.md` §2.1: describe the notification centre behaviour shipped

## Branch & PR

- Branch: `p1/P1-T051-ui-notifications-centre`
- PR title: `P1-T051: Build the notifications centre`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T051` run · viewport matrix + axe green

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields; P0 shell dep)
