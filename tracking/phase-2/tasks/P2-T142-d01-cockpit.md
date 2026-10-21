---
id: P2-T142
kind: task
title: D01 Cockpit dashboard
phase: 2
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T140, P2-T141]
requirements: [R2.50]
roadmap_todos: [T2.32]
modules: [M15, M11, M12, M16]
dashboards: [D01]
branch: p2/P2-T142-d01-cockpit
pr: ""
doc_sync: [docs/ui/dashboards/D01-cockpit.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T142 · D01 Cockpit dashboard

## Goal / expected outcome

The `/` Cockpit answers 'am I safe, what's running, what changed, what needs me, how am I doing' at one glance on every device: KPI strip, Safety tile, Needs-you, Strategy status, main chart, Signals & decisions, Live blotter and Alerts feed, with the per-tier layouts from the D01 spec.

## Context & references

- Roadmap: [R2.50](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.32
- [D01 spec](../../../docs/ui/dashboards/D01-cockpit.md) (widgets, actions, states, acceptance, backend contract) · [ui §2 shell](../../../docs/ui/README.md#2-app-shell-all-routes)
- Backend from part A (P2-T001–T099): `/portfolio/summary`, `/risk/state`, `risk.kill.on|off`, `risk.deadman.ack`, `strategy.pause|resume`, `position.close`, WS `risk.state`, `kill`, `heartbeat`; signals/tier-B tiles show 'no tier B yet' until P4

## Requirements

- Widgets/sources/update rates exactly as the D01 table (KPI 1 Hz; chart ≤ 4 Hz; tables ≤ 1 Hz).
- Kill switch reachable within one tap/click at every tier; state reflected < 1 s after server ack; Kill ON → Safety tile red with reason + trigger source, strategy rows 'halted', chart shaded.
- Approvals actionable from Needs-you without navigation (`ApprovalCard`, top 3 + count).
- Paper vs live never summed without a label; paper-only shows PAPER markers on all money tiles.
- Layouts per tier (3xl/2xl, xl/lg, md, ≤ ph, landscape-short); at 320 px Safety and Needs-you are visible without scrolling past KPIs.
- Empty state: 'Create strategy' (→ D03) and 'Run backtest' (→ D04).
- Workspace layout editing ≥ xl persisted in `ops.user_pref` via `system.settings.update`.
- Every tile implements the [data states](../../../docs/ui/README.md#31-data-states-every-tile-implements-all-of-them) (loading skeleton ≤ 300 ms, live, stale chip, degraded, error card with retry → D16, empty with primary action, PAPER/LIVE markers, unconfirmed hatching).

## ToDo

- [ ] Route + tiles in `apps/web/src/routes/index.tsx` and `src/tiles/cockpit/*`
- [ ] WS subscriptions with background-tab throttling (0.2 Hz except alerts, approvals, kill)
- [ ] Per-tier layouts and workspace persistence
- [ ] Playwright scenarios + matrix; doc sync

## Verification

### Tests
- Playwright: DESIGN.md §6.8 viewport matrix (overflow + fixed-bar overlap checks) and axe on the new routes; Vitest + Testing Library for components.
- Playwright: kill ON via API fixture → banner + Safety red within 1 s; approve from Needs-you.

### Scenarios
- Given the engine heartbeat stops, then the dead-man countdown shows in the Safety tile and the red banner appears.
- Given 3 feeds stale, then the feeds summary shows counts and affected strategy rows show 'paused-by-DQ'.
- Given mt-api restarts, then tiles show 'Re-syncing' and recover without a page reload.

### Stress / failure injection
- Simulate 20 strategies, 500 blotter rows/day and 1 Hz portfolio updates: UI live update lag p95 < 500 ms (02 §9.2).

## Acceptance criteria

- [ ] All D01 acceptance criteria (1–4) pass
- [ ] Viewport matrix + axe green on `/`
- [ ] CI green (lint, types, tests, viewport matrix where UI)

## Exceptions & edge cases

- Read-only mode (DB degraded): actions disabled with tooltip; kill still allowed (it goes via NATS path from part A).
- No tier B before P4: Signals tile hides tier-B column instead of showing zeros.

## Cardinal rules (do NOT)

- Do NOT enforce confirmation levels only in the UI; C1–C3/Kill are enforced server-side by `mt_api`.
- Do NOT use `100vh`/`h-screen`, unprefixed multi-column grids or the Tailwind CDN (DESIGN.md §6.3–6.5).
- Do NOT sum or show paper and live money without a mode label.
- Do NOT let any UI/API path loosen risk, enable autonomous mode or turn the kill switch off without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/dashboards/D01-cockpit.md`: note any deviations (e.g. tier-B tile hidden until P4).
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.32 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T142-d01-cockpit`
- PR title: `P2-T142: D01 Cockpit dashboard`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T142` run · Playwright viewport matrix + axe green

## Progress log

- 2026-10-21 00:00 · planner · created
