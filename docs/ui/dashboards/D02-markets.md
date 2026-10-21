# D02 · Markets

| | |
|---|---|
| **Routes** | `/markets` (cross-asset matrix), `/markets/:instrumentId` (instrument detail) |
| **Modules** | M1 data, M6 features, M16 costs/DQ, M21 tier B, M5 calendar, M3 events |
| **Phase** | 1 (charts, matrix); tier-B and intel overlays in 4 |
| **Mock-up reference** | `cross-asset-terminal-free-liquidity-matrix.png` |

## Purpose

See every tradable market at a glance, then drill into one instrument with:
- charts at any timeframe (tick → 1W);
- book and costs;
- features, decision-model scores and news;
- a manual order ticket.

## `/markets`: cross-asset matrix

### Layout

| Tier | Layout |
|---|---|
| ≥ 2xl | Watchlist panel (left, 6 col) + asset-class quadrants (18 col): Crypto, FX & Metals, Commodities, Stocks/ETFs/Indices, Rates; correlation heatmap + regime strip below |
| xl/lg | Asset-class tabs above a 2-column grid; watchlist in a drawer |
| md | Tabs; 2-column cards |
| ≤ ph | Asset-class segmented control; instrument cards list (symbol, last, Δ%, spread, feed chip, sparkline) |

### Widgets

| Widget | Shows | Source |
|---|---|---|
| Watchlists | User lists (pinned, positions, custom); add/remove; sort | `/markets/instruments?watchlist=`, WS `md.quote` |
| Quadrant cards | Per instrument: last price, Δ (24h / session), spread (bps) vs normal, funding/swap (if applicable), volume, feed status chip, sparkline, tier-B regime chip | `/markets/matrix`, WS `md.quote`, `cost`, `dq.status`, `tierb` |
| Macro strip | Policy rates, 10Y yields, DXY proxy, VIX, gold, oil; nowcasts (GDPNow, Cleveland inflation) | `/markets/matrix?group=macro` |
| Positioning | COT net positioning, retail sentiment (Myfxbook / IG / OANDA books), Kalshi/Polymarket event probabilities | `/markets/matrix?group=positioning` |
| Correlation heatmap | Rolling correlations (selectable window) across the watchlist | `/markets/matrix?group=correlation` |
| Cross-venue spreads | Same instrument across venues: mid difference, fees, net edge (info only; not an auto-arb button) | `/data/costs?compare=1` |

### Actions

| Control | Command | Level |
|---|---|---|
| Open instrument | navigate | C0 |
| Edit watchlist | `intel.watchlist.update` | C0 |
| Quick ticket (b/s) | opens `OrderTicket` | (C2 on submit) |

## `/markets/:instrumentId`: instrument detail

### Layout

| Tier | Layout |
|---|---|
| ≥ 2xl | Header (symbol, venue, last, Δ, feed chip, min resolution); chart (16 col) + right dock (8): order book + trades tape + order ticket; below: tabs (Positions & orders, Costs, Features & scores, News & events, Info) |
| xl/lg | Chart full width; dock as a tabbed drawer (Book / Tape / Ticket) |
| md | Chart; tabs below; ticket opens as a sheet |
| ≤ ph | Header; compact chart (min 220px) with a full-screen button; sticky Buy / Sell bar at the bottom (opens a ticket sheet); tabs as accordions |
| landscape-short | Chart fills the height; Buy/Sell as a floating pair; dock hidden |

### Widgets

| Widget | Shows | Source |
|---|---|---|
| `PriceChart` | Candles at any spec from tick/1s to 1W (incl. tick/volume bars); overlays: indicators (user-selectable), own fills, strategy signals, Decision One nodes, calendar/event markers, blackout windows (shaded) | `/markets/{id}/bars`, WS `md.bar`/`md.trade`, `fills`, `signals`, `cal`, `evt` |
| Timeframe picker | Unsupported resolutions disabled with a reason (e.g. "US stocks: IEX only; no tick L2") | `/markets/instruments/{id}` (min resolution) |
| `OrderBook` | L2 where available (crypto); top of book for FX/stocks | WS `md.book` |
| `TradesTape` | Last trades | WS `md.trade` |
| `OrderTicket` + `RiskPreview` | Manual order with live pre-trade checks | `POST /risk/preview` (dry-run), `order.place` |
| Positions & orders | For this instrument | `/positions?instrument=`, `/orders?instrument=` |
| Costs | Spread by hour-of-week heatmap, current fee tier, funding/swap now and history, realised slippage for own fills | `/data/costs?instrument=` |
| Features & scores | Key feature values; tier-B question probabilities (`TierBScore`) with model version and calibration badge | `/models/tierb/decisions?subject=`, WS `tierb` |
| News & events | Linked documents (sentiment, relevance), geo events, upcoming calendar items | `/intel/documents?ticker=`, `/intel/events?instrument=`, `/intel/calendar?instrument=` |
| Info | Instrument metadata: venue(s), tick size, lot, trading hours, data sources and licence flags | `/markets/instruments/{id}` |

### Actions

| Control | Command | Level |
|---|---|---|
| Place order | `order.place` | C2 (risk preview must pass; failing checks disable Submit with reasons) |
| Modify / cancel order | `order.modify` / `order.cancel` | C2 / C1 |
| Close / reduce position | `position.close` / `position.reduce` | C2 |
| Set brackets | `position.set_brackets` | C2 |
| Ask decision model | `models.tierb.ask` (question picker) | C0 |
| Request agent analysis | `agents.run_analysis` (→ D09) | C1 (uses LLM budget) |
| Save chart layout / drawings | prefs | C0 |

## States

- **Feed stale:** chart and book dimmed; ticket disabled with "Feed stale: risk manager blocks orders".
- **Market closed:** session banner; orders queued only if the venue supports it.
- **Kill ON:** ticket disabled.

## Acceptance criteria

1. **Timeframes:** switching timeframe from tick to 1W re-renders in < 500 ms for cached ranges.
2. **Ticket:** the order ticket shows risk checks before submit, and never submits while the preview fails.
3. **Phones:** the Buy/Sell bar is reachable with one thumb; the ticket fits on a 320×568 screen without horizontal scroll.

## Backend contract

- **Queries:**
  - `/markets/matrix`, `/markets/instruments`, `/markets/{id}/bars`, `/markets/{id}/book`;
  - `/data/costs`, `/positions`, `/orders`;
  - `/models/tierb/decisions`;
  - `/intel/documents`, `/intel/events`, `/intel/calendar`;
  - `POST /risk/preview` (dry-run, no side effects).
- **WebSocket topics:** `md.quote`, `md.trade`, `md.book`, `md.bar`, `cost`, `dq.status`, `tierb`, `fills`, `signals`, `cal`, `evt`.
- **Commands:** `order.*`, `position.*`, `models.tierb.ask`, `agents.run_analysis`, `intel.watchlist.update`.
