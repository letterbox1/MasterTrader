---
id: P2-T147
kind: task
title: D05 Execution: positions, orders, fills, TCA and venues
phase: 2
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T140, P2-T020, P2-T029]
requirements: [R2.50, R2.34]
roadmap_todos: [T2.32]
modules: [M15, M12, M16]
dashboards: [D05]
tools: [pnpm]
mcp: []
env: []
services: []
branch: p2/P2-T147-d05-execution-tabs
pr: ""
doc_sync: [docs/ui/dashboards/D05-execution.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T147 · D05 Execution: positions, orders, fills, TCA and venues

## Goal / expected outcome

`/execution` shows everything in the market — Positions, Orders, Fills, TCA and Venues tabs plus the KPI strip — with the per-tier layouts, reconciliation states and cancel-all from the D05 spec (Approvals tab in P2-T149, manual ticket in P2-T148).

## Context & references

- Roadmap: [R2.50, R2.34](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.32
- [D05 spec](../../../docs/ui/dashboards/D05-execution.md) · Backend from part A (P2-T001–T099): `/positions`, `/orders`, `/fills`, `order.*`, `position.*` (T2.25), TCA `/data/costs?tca=1` (T2.26); `/data/recon`, `/system/services?kind=venue`, `/system/keys` from P1/P0

## Requirements

- KPI strip: gross/net exposure, open orders, pending approvals, today fees, avg slippage bps, unreconciled items.
- Positions/Orders/Fills columns per D05; source badges (strategy/manual/agent/MCP); mode (paper/live) column.
- TCA tab: implementation shortfall by strategy × venue × instrument; delay/spread-impact/fees decomposition; realised vs modelled ratio with alert styling > 1.5× over the last 20 fills (16 §2.1 cost blow-out default); slippage distribution; fill rate; time to fill; sum of fees equals fills' fees (D05 acceptance 3).
- Venues tab: connection, latency, rate-limit headroom, balances, margin, sub-account mode, key age (masked metadata only), last reconciliation; run reconciliation (C1).
- Cancel all with scope (all/venue/strategy/instrument) = C2; toast shows the server-measured time to all cancels sent (< 1 s target, D05 acceptance 2).
- Unreconciled positions hatched + 'unconfirmed'; close requires reconciliation unless via kill flatten.
- Layouts: ≥ 2xl right-dock ticket; xl/lg drawer (`b`/`s` shortcuts); ≤ ph segmented tabs + card lists + sticky New order; landscape-short two-pane.
- Every tile implements the [data states](../../../docs/ui/README.md#31-data-states-every-tile-implements-all-of-them) (loading skeleton ≤ 300 ms, live, stale chip, degraded, error card with retry → D16, empty with primary action, PAPER/LIVE markers, unconfirmed hatching).

## ToDo

- [ ] Route `apps/web/src/routes/execution.tsx` + tab components
- [ ] TCA charts (Distribution, Heatmap)
- [ ] Cancel-all flow with timing toast
- [ ] Playwright + matrix; doc sync

## Verification

### Tests
- Playwright: DESIGN.md §6.8 viewport matrix (overflow + fixed-bar overlap checks) and axe on the new routes; Vitest + Testing Library for components.
- Playwright: cancel-all on 20 fixture orders shows server timing < 1 s; TCA fee sum equals fills sum.

### Scenarios
- Given a venue disconnect, then positions on it show 'unconfirmed' and close is disabled with the reason.
- Given Kill ON, then all trading actions are disabled except cancel and flatten-via-kill.

### Stress / failure injection
- Orders table with 5,000 rows at 1 Hz updates: virtualised, p95 UI lag < 500 ms.

## Acceptance criteria

- [ ] D05 acceptance 2 and 3 pass
- [ ] Viewport matrix + axe green on `/execution`
- [ ] CI green (lint, types, tests, viewport matrix where UI)

## Exceptions & edge cases

- API keys never shown — masked metadata only.
- Paper and live positions visually separated and never summed without label.

## Cardinal rules (do NOT)

- Do NOT enforce confirmation levels only in the UI; C1–C3/Kill are enforced server-side by `mt_api`.
- Do NOT use `100vh`/`h-screen`, unprefixed multi-column grids or the Tailwind CDN (DESIGN.md §6.3–6.5).
- Do NOT sum or show paper and live money without a mode label.
- Do NOT display or fetch key secrets; `/system/keys` is masked metadata only.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file (07 §2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/dashboards/D05-execution.md`: final column sets.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.32 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T147-d05-execution-tabs`
- PR title: `P2-T147: D05 Execution: positions, orders, fills, TCA and venues`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T147` run · Playwright viewport matrix + axe green

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (cost blow-out default; backend deps (orders API, TCA))
