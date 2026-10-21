---
id: P1-T050
kind: task
title: Build D02 instrument detail with charts at every timeframe
phase: 1
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T049, P1-T014]
requirements: [R1.15, R1.02]
roadmap_todos: [T1.32]
modules: [M15, M1, M16]
dashboards: [D02]
branch: p1/P1-T050-ui-d02-instrument-detail
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

# P1-T050 · Build D02 instrument detail with charts at every timeframe

## Goal / expected outcome

`/markets/:instrumentId` shows a lightweight-charts `PriceChart` from tick/1s to 1D (1W as an on-the-fly bucket), a timeframe picker that disables unsupported resolutions with a reason, L2 `OrderBook` where available, `TradesTape`, Costs and Info tabs, with the order ticket present but disabled until P2.

## Context & references

- Roadmap: requirements [R1.15](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.02](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.32](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [D02 Markets](../../../docs/ui/dashboards/D02-markets.md) instrument detail layout, widgets, states, acceptance · [03 §6](../../../docs/03-build-spec.md#6-smallest-free-timeframe-by-asset-class) (finest available resolution shown) · [ui components](../../../docs/ui/components.md) (`PriceChart`, `TimeframePicker`, `OrderBook`, `TradesTape`) · [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)
- Order ticket and risk preview land in P2 (M11); P1 shows a disabled ticket with "Trading arrives in Phase 2"
- Depends on (this phase): P1-T049, P1-T014

## Requirements

- Header: symbol, venue, last, Δ, feed chip, min resolution (from instrument metadata), "IEX only" badge for US stocks
- `PriceChart` (TradingView lightweight-charts, Apache-2.0): specs tick, 1s, 1m, 5m, 15m, 1h, 4h, 1D, 1W (time_bucket), info bars (`t500`, `v…`); live updates via `md.bar`/`md.trade` at ≤ 4 Hz
- `TimeframePicker`: unsupported resolutions disabled with reason (e.g. "US stocks: IEX only; no tick L2"; "Futures: daily only")
- `OrderBook` L2 for crypto (levels 25/15/10/5 by tier, spread row pinned), top-of-book for FX/stocks; `TradesTape`
- Tabs: Costs (spread hour-of-week heatmap, fee tier, funding/swap now + history), Info (venues, tick size, lot, trading hours, data sources and licence flags); Features/News tabs show "coming in P4"
- States: feed stale → chart and book dimmed, ticket disabled "Feed stale: risk manager blocks orders"; market closed → session banner
- Layouts: ≥ 2xl chart + right dock; xl/lg dock as tabbed drawer; md chart + tabs; ≤ ph compact chart (min 220 px) with full-screen, sticky Buy/Sell bar (disabled in P1); landscape-short chart fills height
- D02 acceptance 1: switching timeframe tick → 1W re-renders in < 500 ms for cached ranges

## ToDo

- [ ] Build route, chart wrapper with spec switching and caching, picker, book, tape, tabs
- [ ] Disabled ticket component with P2 placeholder
- [ ] Playwright: viewport matrix, axe, timeframe-switch timing test, 320×568 layout check
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Component: picker disables unsupported specs with reason text; book renders depth bars and pinned spread row
- Playwright: timeframe switch timing (cached) < 500 ms across 9 specs; matrix including 320×568 and 240×320 floor

### Scenarios

- Given XAUUSD, when opening detail, then the picker shows quotes at ~4/s finest and no L2, with the reason
- Given BTCUSDT feed goes stale, when viewing, then chart and book dim and the ticket shows the stale reason

### Stress / failure injection

- Load: BTCUSDT tick chart at 4 Hz updates for 10 min; memory stable (< 50 MB growth) and no frame drops on desktop profile

## Acceptance criteria

- [ ] Every universe instrument opens with its finest available resolution and charts at every supported timeframe (exit criterion 1 UI part)
- [ ] D02 acceptance 1 and the 320×568 no-horizontal-scroll check pass
- [ ] CI green (lint, types, tests, Playwright viewport matrix 240→2560 px per DESIGN §6.8, axe)

## Exceptions & edge cases

- Instruments with daily-only data (futures, macro proxies) open on 1D with intraday specs disabled

## Cardinal rules (do NOT)

- Do NOT enable order submission in P1; the ticket stays disabled until P2 wires M11 risk preview
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT place, modify or cancel orders from this code; P1 is read-only toward venues (orders arrive in P2 through M11).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.32 once every task traced to it in PHASE.md is done; note P1-T050 next to it.
- `docs/ui/dashboards/D02-markets.md`: note P1 vs P2/P4 widgets as shipped and the 1W handling

## Branch & PR

- Branch: `p1/P1-T050-ui-d02-instrument-detail`
- PR title: `P1-T050: Build D02 instrument detail with charts at every timeframe`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T050` run · viewport matrix + axe green

## Progress log

- 2026-10-21 00:00 · planner · created
