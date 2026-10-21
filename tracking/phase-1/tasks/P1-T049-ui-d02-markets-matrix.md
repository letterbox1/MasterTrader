---
id: P1-T049
kind: task
title: Build the D02 cross-asset markets matrix
phase: 1
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T046, P1-T047]
requirements: [R1.15]
roadmap_todos: [T1.32]
modules: [M15, M1]
dashboards: [D02]
branch: p1/P1-T049-ui-d02-markets-matrix
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/ui/dashboards/D02-markets.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T049 · Build the D02 cross-asset markets matrix

## Goal / expected outcome

`/markets` shows watchlists and asset-class quadrants (Crypto, FX & Metals, Commodities, Stocks/ETFs/Indices, Rates) with live last price, Δ, spread vs normal, funding/swap, feed chip and sparkline, plus a macro strip, per the D02 layout at every tier.

## Context & references

- Roadmap: requirements [R1.15](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.32](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [D02 Markets](../../../docs/ui/dashboards/D02-markets.md) `/markets` layout and widgets · [ui components](../../../docs/ui/components.md) · [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass) · phase note: tier-B and intel overlays come in P4
- Data gaps for macro strip/positioning/correlation: P1-B012
- Depends on (this phase): P1-T046, P1-T047

## Requirements

- Watchlists from `/markets/instruments?watchlist=` with add/remove (`intel.watchlist.update`, C0)
- Quadrant cards: last, Δ 24 h/session, spread bps vs normal (from `cost`), funding/swap where applicable, volume, feed status chip, sparkline; WS `md.quote`, `cost`, `dq.status` at ≤ 1 Hz
- Macro strip: policy rates, 10Y yields, DXY proxy, VIX, gold, oil from P1 macro/daily data; nowcasts shown as "not yet available" until sourced (P1-B012)
- Positioning widget: CFTC COT only in P1; Myfxbook/IG/OANDA books/Kalshi marked "coming in P4" (empty state, no fake data)
- Correlation heatmap from daily returns of the watchlist (ECharts `Heatmap`); cross-venue spreads table (info only, no arb button)
- Tier layouts: ≥ 2xl watchlist + quadrants; xl/lg tabs + drawer; md 2-col cards; ≤ ph segmented control + instrument cards

## ToDo

- [ ] Build `/markets` route, quadrant cards, watchlist panel/drawer, macro strip, positioning, heatmap, cross-venue table
- [ ] Playwright viewport matrix + axe
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Component: card renders stale/degraded/empty states; IEX badge on US stocks
- Playwright: matrix across DESIGN §6.8; cards update ≤ 1 Hz

### Scenarios

- Given a crypto feed goes stale, when viewing the matrix, then its card dims with the stale chip within 2 s
- Given no COT data yet, when the positioning widget loads, then an empty state explains the source, never placeholder numbers

### Stress / failure injection

- Load: 60 instruments in quadrants updating at 1 Hz; no dropped frames below 50 fps on desktop profile

## Acceptance criteria

- [ ] Matrix renders all P1 asset classes with live data at every tier; no fake data anywhere
- [ ] CI green (lint, types, tests, Playwright viewport matrix 240→2560 px per DESIGN §6.8, axe)

## Exceptions & edge cases

- Market closed instruments show a session label, not stale

## Cardinal rules (do NOT)

- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.32 once every task traced to it in PHASE.md is done; note P1-T049 next to it.
- `docs/ui/dashboards/D02-markets.md`: mark which widgets are P1 vs P4 as shipped

## Branch & PR

- Branch: `p1/P1-T049-ui-d02-markets-matrix`
- PR title: `P1-T049: Build the D02 cross-asset markets matrix`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T049` run · viewport matrix + axe green

## Progress log

- 2026-10-21 00:00 · planner · created
