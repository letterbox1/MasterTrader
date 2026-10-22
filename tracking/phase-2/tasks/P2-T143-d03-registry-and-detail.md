---
id: P2-T143
kind: task
title: D03 Strategies registry and detail (gates, versions, performance)
phase: 2
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T140, P2-T141, P2-T117, P2-T006, P2-T007]
requirements: [R2.50, R2.04, R2.06, R2.42]
roadmap_todos: [T2.32]
modules: [M15, M0, M7]
dashboards: [D03]
tools: [pnpm]
mcp: []
env: []
services: []
branch: p2/P2-T143-d03-registry-and-detail
pr: ""
doc_sync: [docs/ui/dashboards/D03-strategies.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T143 · D03 Strategies registry and detail (gates, versions, performance)

## Goal / expected outcome

`/strategies` (registry) and `/strategies/:id` (detail) show every strategy with lifecycle stage, mode, status and manifest fields, and the detail tabs (Overview, Parameters, Performance, Positions & orders, Signals, Gates, Versions, Logs) including per-year/per-regime, 2×/3× cost stress, trial counter and worst fold. The Bots tab is out of scope (part A).

## Context & references

- Roadmap: [R2.50, R2.04, R2.06, R2.42](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.32
- [D03 spec](../../../docs/ui/dashboards/D03-strategies.md) (registry, detail, actions, CryptoTrader additions, acceptance) · gates from P2-T114 via P2-T117
- Backend from part A (P2-T001–T099): `/strategies*` registry/versions/runs, `strategy.*` commands and lifecycle (T2.20), Bots tab (T2.34)

## Requirements

- Registry: filter bar (type, asset class, timeframe, stage, mode, status); `DataTable` with P1/P2/P3 column priorities; cards ≤ ph; actions clone/archive/bulk pause (C1).
- Manifest fields on registry + detail: counterparty, benchmark, priority (P1/P2/P3/X), sleeve, kill criteria, evidence.
- Detail header: stage stepper ('Stage 4/6' on phones), `ModeSwitch`, status, Start/Pause/Stop.
- Gates tab: checklist per 03 §8 with exact failing gate + reason; worst fold, trial count, DSR, MC p, per-year/per-regime tables, cost-stress results, leakage review items with waivers, paper period elapsed/required.
- The strategy `ModeSwitch` sets the **mode ceiling** (`strategy.set_mode`: allow hitl C2, allow autonomous C3, restrict C1; the stricter of strategy and bot mode applies, 16 §2.3); autonomous can't be selected while gates fail (D03 acceptance 2); edit params: tightening C1, any risk-increasing change C3 (DiffView, 16 §1).
- Gates tab shows the strategy's gate profile (16 §2.4: DSR ≥ 0.95 with trial counter, walk-forward ≥ 60% positive and worst fold ≥ −sleeve halt drawdown, 2× cost gate with 3× reported, per-year/per-regime, paper ≥ 8 weeks and ≥ 50 trades, safety drills) with each threshold (default or overridden) via `GateChecklist`.
- Performance tab: metrics incl. realised vs modelled costs, tracking error vs backtest; equity live vs paper vs backtest expectation.
- Versions tab with DiffView + rollback; Logs tab via `/system/logs?strategy=`.
- Every tile implements the [data states](../../../docs/ui/README.md#31-data-states-every-tile-implements-all-of-them) (loading skeleton ≤ 300 ms, live, stale chip, degraded, error card with retry → D16, empty with primary action, PAPER/LIVE markers, unconfirmed hatching).

## ToDo

- [ ] Routes `apps/web/src/routes/strategies/index.tsx` and `$id.tsx` + tab components
- [ ] Gates tab bound to `/strategies/{id}?gates=1`
- [ ] Mode switch + C3 flow wiring; param edit level logic
- [ ] Playwright scenarios + matrix; doc sync

## Verification

### Tests
- Playwright: DESIGN.md §6.8 viewport matrix (overflow + fixed-bar overlap checks) and axe on the new routes; Vitest + Testing Library for components.
- Playwright: failing DSR fixture → autonomous disabled and 'Deflated Sharpe 0.71 < 0.95' shown.

### Scenarios
- Given a strategy with a waived leakage item, then Gates shows 'waived' with reason, time and audit link.
- Given a risk-increasing param edit on a paper strategy, then C3 flow starts (Telegram + TOTP + cool-down).
- Given lab API is down, then Gates shows an error card with retry, not 'all passed'.

### Stress / failure injection
- Registry with 500 strategies: virtualised table, filter response < 100 ms.

## Acceptance criteria

- [ ] D03 acceptance 2 (auto blocked with exact failing gate) passes
- [ ] All CryptoTrader-addition fields shown
- [ ] Viewport matrix + axe green on both routes
- [ ] CI green (lint, types, tests, viewport matrix where UI)

## Exceptions & edge cases

- Archived strategies hidden by default; filter to show.
- Strategies in 'paused-by-DQ/risk' show the reason chip.

## Cardinal rules (do NOT)

- Do NOT enforce confirmation levels only in the UI; C1–C3/Kill are enforced server-side by `mt_api`.
- Do NOT use `100vh`/`h-screen`, unprefixed multi-column grids or the Tailwind CDN (DESIGN.md §6.3–6.5).
- Do NOT sum or show paper and live money without a mode label.
- Do NOT build the Bots tab here (part A owns it).
- Do NOT let any UI/API path loosen risk, enable autonomous mode or turn the kill switch off without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/dashboards/D03-strategies.md`: Gates tab final field list.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.32 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T143-d03-registry-and-detail`
- PR title: `P2-T143: D03 Strategies registry and detail (gates, versions, performance)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T143` run · Playwright viewport matrix + axe green

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (mode ceiling levels (C2/C3/C1), param edits tighten C1/loosen C3, gate profile per 16 §2.4; backend deps)
