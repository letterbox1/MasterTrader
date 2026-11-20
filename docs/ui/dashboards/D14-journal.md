# D14 · Journal

| | |
|---|---|
| **Routes** | `/journal` (trades & events), `/journal/trades/:id` (trade review), `/journal/reviews` (weekly reviews, Phase 7), `/journal/reviews/scenario-twin` (scenario-twin reports, from Phase 6) |
| **Modules** | M18 journal, M17 audit, M8/M21 decision provenance, M14 scenario twin (report only) |
| **Phase** | 3 |
| **Mock-up reference** | None (new) |

## Purpose

A **fully automatic trading journal**:
- every trade and economic event is recorded without manual entry;
- you can review, annotate and learn from each trade;
- the record is reconciled and audit-ready.

## Layout by tier

| Tier | Layout |
|---|---|
| ≥ xl | KPI strip (trades, win rate, avg R, fees, funding, net P&L for period; paper/live toggle) + filters + trades table + review panel |
| md–lg | Table; review as a drawer |
| ≤ ph | Period selector; `JournalEntry` cards; review page |

## Widgets

| Widget | Shows | Source |
|---|---|---|
| Trades table | Round-trip trades: open/close time, instrument, side, size, entry/exit, P&L (gross, fees, funding, net, R-multiple), strategy, signal source (strategy / agent / tier B / manual / MCP), tags, review status | `/journal/trades` |
| Events | All journal events (fills, fees, funding, swaps, deposits/withdrawals, transfers, airdrops, staking, dividends, interest, FX conversions) with home-currency values and FX source | `/journal/events`, WS `journal` |
| Trade review (`/journal/trades/:id`) | Chart snapshot with entry/exit and signals; the decision provenance (signal → agent run / tier-B scores → risk checks → order → fills); costs vs modelled; notes, tags, screenshots; review prompts ("Followed plan?", "Mistake type") | `/journal/trades/{id}` |
| Analytics | P&L by strategy / instrument / weekday / hour / tag; mistake tags frequency; expectancy | `/journal/trades?analytics=1` |
| Reconciliation status | Journal vs venues daily; mismatches link to D07 | `/data/recon?scope=journal` |
| **Weekly reviews** (Phase 7) | Each weekly review: tracking error vs backtest, realised vs modelled costs, DQ incidents, journal reconciliation, five worst trades, and the week's **scenario-twin report** when one exists; your sign-off (a WORM row) | `/journal/reviews` |
| **Scenario twin** (from Phase 6) | Per bot, for each simulated scenario that week ([18 §2.4](../../18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool)): the scenario (source event, sentiment path, injected price/volatility/spread/liquidity shocks), the twin's P&L, drawdown and the risk rules it hit, next to the real paper run for the same week. Labelled **Simulated** everywhere. An extra input to the weekly review, never a gate ([16 §2.14b](../../16-configuration-and-safety-model.md#214b-scenario--crowd-simulator-m14)). Empty state before the simulator exists: "Scenario twin not running yet" | `/sim/twin/reports` _(added)_ |

## Actions

| Control | Command | Level |
|---|---|---|
| Add note / tag / screenshot | `journal.note.add` (optional attachment: PNG/JPEG, default ≤ 5 MB; stored content-addressed under `data/attachments/`, referenced by hash in the WORM note row), `journal.tag` | C0 |
| Add a manual journal event (e.g. opening lot, off-system transfer) | `journal.manual_event.add` | C2 (reason required) |
| Sign off a weekly review | `journal.review.signoff` | C1 |
| Export (CSV / Beancount) | `tax.export` (journal scope) | C0 |
| Open in tax view (lots) | navigate D15 | C0 |

Records themselves are **never editable**. Corrections are journal events that supersede the original (server-side), and the UI shows the chain.

## Acceptance criteria

1. **Completeness:** each fill appears within 5 s with fees and its home-currency value.
2. **Provenance:** every trade links to its full provenance chain.
3. **Paper vs live:** separated by default, with a toggle.
4. **Simulated stays separate:** scenario-twin numbers are labelled Simulated and never appear in journal totals, analytics, exports or tax.

## Backend contract

- **Queries:** `/journal/trades` (+ `/{id}`, `analytics`), `/journal/events`, `/data/recon?scope=journal`.
- **WebSocket topics:** `journal`, `fills`.
- **Queries (Phase 7):** `/journal/reviews`.
- **Queries (Phase 6):** `/sim/twin/reports` _(added)_.
- **Commands:** `journal.note.add`, `journal.tag`, `journal.manual_event.add`, `journal.review.signoff`, `tax.export`.
