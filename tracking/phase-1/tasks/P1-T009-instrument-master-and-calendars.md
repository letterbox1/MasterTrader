---
id: P1-T009
kind: task
title: Build the instrument master with sessions and finest resolution
phase: 1
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T005, P1-T007]
requirements: [R1.05, R1.15]
roadmap_todos: [T1.22, T1.32]
modules: [M1]
dashboards: [D02]
branch: p1/P1-T009-instrument-master-and-calendars
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T009 · Build the instrument master with sessions and finest resolution

## Goal / expected outcome

`market.instrument` holds every universe instrument with venue metadata, FinanceDatabase classification, trading sessions from `exchange_calendars`, and its finest available real-time and history resolution, so D02 and the stale check know what to expect.

## Context & references

- Roadmap: requirements [R1.05](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.15](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.22](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets), [T1.32](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (FinanceDatabase as symbol master) · [03 §6](../../../docs/03-build-spec.md#6-smallest-free-timeframe-by-asset-class) (finest free timeframe per class; "the UI shows each instrument's finest available resolution")
- UI: [D02 Markets](../../../docs/ui/dashboards/D02-markets.md) header "min resolution" and timeframe picker disabling unsupported resolutions with a reason
- Gap: R1.05's FinanceDatabase/`exchange_calendars` have no roadmap ToDo (P1-B003)
- Depends on (this phase): P1-T005, P1-T007

## Requirements

- Instrument IDs use Nautilus `InstrumentId` (`BTCUSDT.BINANCE`); precision, tick size, lot size from venue metadata (Nautilus instrument providers / ccxt `load_markets`)
- FinanceDatabase (MIT) for equities/ETFs classification (sector, asset class, exchange) refreshed weekly
- Sessions: `exchange_calendars` for equities (XNYS/XNAS), FX weekly session (Sun 22:00 → Fri 22:00 UTC, broker-specific), crypto 24/7; stored as `session_calendar` reference used by the stale check (P1-T031)
- Resolution metadata per instrument: `rt_finest` (tick|l2_100ms|quote_4hz|iex_trade|daily|none) and `hist_finest` (trade|1s|tick|1m|daily) with a reason string (e.g. "US stocks: IEX only; no tick L2")
- Exposed via `/markets/instruments` and `/markets/instruments/{id}` (P1-T046)

## ToDo

- [ ] Migration for `market.instrument` columns (resolution, session ref, classification) if not in P0 schema
- [ ] Instrument sync job per venue + FinanceDatabase enrichment
- [ ] Session resolver API `mt_data.calendar.is_open(instrument_id, ts)`
- [ ] Seed resolution metadata from 03 §6 rules per asset class/venue
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: session resolver across DST changes (US and AU), US holidays, FX weekend; resolution rules per class
- Integration: sync against recorded venue metadata fixtures produces stable rows; delisted symbol flagged `active=false`

### Scenarios

- Given SPY on a US holiday, when the stale check asks `is_open`, then it gets false and no stale incident is raised
- Given an IEX stock, when D02 renders the timeframe picker, then tick and L2 are disabled with the reason text

### Stress / failure injection

- n/a: small reference data; covered by unit tests

## Acceptance criteria

- [ ] Every universe instrument has precision, session and resolution metadata
- [ ] Session resolver passes DST and holiday tests for XNYS and FX
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Venue renames/delists: keep the old row, mark inactive, link the successor; never delete instruments that history references
- Half-day sessions (US early close) handled by `exchange_calendars`

## Cardinal rules (do NOT)

- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.22, T1.32 once every task traced to it in PHASE.md is done; note P1-T009 next to it.
- `docs/03-build-spec.md` §6: link the resolution metadata fields that implement this table

## Branch & PR

- Branch: `p1/P1-T009-instrument-master-and-calendars`
- PR title: `P1-T009: Build the instrument master with sessions and finest resolution`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T009` run

## Progress log

- 2026-10-21 00:00 · planner · created
