---
id: P0-T050
kind: task
title: Build the app shell, navigation, banners, status bar and login/TOTP screens
phase: 0
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T049, P0-T048, P0-T033, P0-T035]
requirements: [R0.11, R0.N6, R0.08]
roadmap_todos: [T0.26]
modules: [M15]
dashboards: [D16]
branch: p0/P0-T050-app-shell-login-totp
pr: ""
doc_sync: [docs/ui/README.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T050 · Build the app shell, navigation, banners, status bar and login/TOTP screens

## Goal / expected outcome

Every route renders inside `AppShell` per DESIGN §6.4: top bar (brand, palette trigger, mode badge, **kill switch**, approvals, notifications, system pulse, profile), sidebar/rail/bottom nav + More sheet per tier, global banners, status bar (≥ md), plus first-boot setup, TOTP enrolment and login screens. Routes for D01–D18 exist as empty states naming their phase.

## Context & references

- [Roadmap P0 R0.11, R0.N6](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [ui §2 app shell](../../../docs/ui/README.md#2-app-shell-all-routes)
- [DESIGN §6.4 app shell](../../../DESIGN.md#64-app-shell-by-tier)
- [ui §1 IA](../../../docs/ui/README.md#1-information-architecture)
- [ui §3.6 sessions](../../../docs/ui/README.md#36-permissions--sessions)
- [components §1 shell](../../../docs/ui/components.md#1-shell--navigation)
- USER step: P0-T062
- Depends on: P0-T049, P0-T048, P0-T033, P0-T035

## Requirements

- Layouts per tier: 3xl/2xl sidebar 240 + top 56 + status 28 (+ right dock slot); xl sidebar collapsible; lg/md rail 64; ph/sm/xs top 48 + bottom nav 56 (+ safe area); xxs top 44 (mark only) + bottom nav 4 + More; `landscape-short` rail 56, top 40, no bottom nav; `very-short` drops decorative headers.
- Kill switch and mode badge visible at **every** tier (icon + accessible name ≤ sm); kill wired to `risk.kill.on` (Kill level) and shows `HALTED` + reason from WS `kill`; OFF opens `C3Flow`.
- Mode badge in P0 reads `PAPER` (no strategies yet) from `/risk/state` stub.
- Banners (ui §2.2) driven by WS: kill ON (red), verify-mismatch/trading halt (red, from P0-T038), read-only mode (grey) when `db: down`.
- Status bar: engine version (`n/a` in P0), feed summary (`n/a`), risk state `ARMED/HALTED`, backup age, local clock with UTC tooltip; sticky with reserved space (no overlap).
- Nav groups and order from ui §1; phone bottom nav Cockpit · Markets · Execution · Tasks · More; unbuilt dashboards show `EmptyState` 'Arrives in Phase N'.
- Auth screens: first-boot setup (setup token + password + QR from provisioning URI rendered client-side + confirm code + recovery codes shown once), login (password + TOTP), session-expired re-login preserving the route.
- Keyboard: `⌘/Ctrl+K` palette (routes + commands list), `Shift+Esc` kill confirm, `?` shortcuts sheet, `g` sequences for built routes.
- Never `100vh`; `min-h-dvh`; no horizontal page scroll at any width ≥ 240px.

## ToDo

- [ ] Implement `AppShell`, `TopBar`, `SideNav`/`NavRail`/`BottomNav`/`MoreSheet`, `StatusBar`, banners container.
- [ ] Implement auth routes and guards.
- [ ] Implement route stubs for D01–D18 with phase labels.
- [ ] Implement command palette v0 and shortcuts.
- [ ] Vitest tests; viewport matrix in P0-T053.

## Verification

### Tests
- Unit: tier layout switches by viewport (mock matchMedia); kill button present in every layout.
- Integration (Playwright smoke): setup → enrol → login → land on `/system`; kill ON → banner appears on another tab within 500 ms.

### Scenarios
- Given a 240×320 viewport, then the top bar shows the mark, the kill button (with accessible name) and mode; bottom nav shows 4 + More.
- Given Postgres goes down, then a grey read-only banner appears and command buttons are disabled with a reason.

### Stress / failure injection
- n/a here; viewport/zoom matrix and a11y are P0-T053.

## Acceptance criteria

- [ ] Shell renders correctly in every tier (unit + smoke)
- [ ] Kill switch visible and keyboard-reachable within 2 tabs everywhere
- [ ] Auth screens complete the first-boot flow
- [ ] Routes D01–D18 stubbed with phase labels
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check, Playwright viewport matrix)

## Exceptions & edge cases

- Very short landscape (568×320): bottom nav hidden, rail 56; modals become side sheets (DESIGN §6.2).

## Cardinal rules (do NOT)

- Do NOT hide the kill switch behind a menu at any tier.
- Do NOT render fake data in stubs (empty states only, DESIGN §10).
- Do NOT store the session token in localStorage.
- Loosening risk, autonomous mode and mandates are C3 (Telegram + TOTP + cool-down); Kill ON and protective exits never wait for approval.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/ui/README.md` §2: note P0 placeholders (engine version, feed summary `n/a`) and the auth screens.
- `docs/roadmap/phase-0-foundations.md`: tick T0.26 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T050-app-shell-login-totp`
- PR title: `P0-T050: Build the app shell, navigation, banners, status bar and login/TOTP screens`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T050` run

## Progress log

- 2026-10-21 00:00 · planner · created
