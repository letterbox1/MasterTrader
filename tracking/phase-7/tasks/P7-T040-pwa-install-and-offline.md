---
id: P7-T040
kind: task
title: PWA install prompts, offline banner and multi-channel Kill
phase: 7
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.12]
roadmap_todos: [T7.25]
modules: [M15]
dashboards: [D01]
branch: p7/P7-T040-pwa-install-and-offline
pr: ""
doc_sync: [docs/ui/mobile-and-telegram.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T040 · PWA install prompts, offline banner and multi-channel Kill

## Goal / expected outcome

The PWA prompts installation on phones, loads offline with the last known state and a clear stale banner, queues nothing offline except Kill, which tries every channel.

## Context & references

- Roadmap: [R7.12 · ToDo T7.25](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [mob §1](../../../docs/ui/mobile-and-telegram.md#1-pwa) (install, offline, no queued actions except Kill) · [mob §4](../../../docs/ui/mobile-and-telegram.md#4-acceptance-criteria) (kill within 1 s of confirm) · [DESIGN.md §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)
- Cross-phase: P0 T0.26 (PWA shell).
- Related: P7-T054

## Requirements

- Install prompt (`beforeinstallprompt` on Android/Chromium; iOS 'Add to Home Screen' guide sheet) shown once after login, dismissible, re-offered from settings.
- Offline: shell + last snapshot from IndexedDB; banner 'Offline: data may be stale' with last-updated time.
- Kill offline: tries web API, then opens Telegram deep link `/kill`, then ntfy action; shows which channel succeeded.
- Manifest uses `brand/app-icon.svg`; Lighthouse PWA installable checks pass.

## ToDo

- [ ] Install prompt component + settings entry.
- [ ] Offline snapshot cache + banner.
- [ ] Kill fallback chain.
- [ ] Tests; docs.

## Verification

### Tests
- Playwright: offline mode shows banner; actions disabled except Kill.
- Lighthouse CI: installable.

### Scenarios
- Given the host is unreachable, when you tap HALT and confirm, then the app falls back to the Telegram `/kill` deep link.

### Stress / failure injection
- n/a: client-side behaviour; covered by offline tests.

## Acceptance criteria

- [ ] PWA installable; offline banner; Kill fallback chain works.
- [ ] CI green.

## Exceptions & edge cases

- iOS lacks `beforeinstallprompt`: guide sheet instead.

## Cardinal rules (do NOT)

- Do NOT queue trading actions offline.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/ui/mobile-and-telegram.md` §1: install prompt and Kill fallback order.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.25 when this item is done.

## Branch & PR

- Branch: `p7/P7-T040-pwa-install-and-offline`
- PR title: `P7-T040: PWA install prompts, offline banner and multi-channel Kill`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T040` run

## Progress log

- 2026-10-21 00:00 · planner · created
