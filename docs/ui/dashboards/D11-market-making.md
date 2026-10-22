# D11 · Market Making (Hummingbot sidecar)

| | |
|---|---|
| **Route** | `/mm` |
| **Modules** | M13 Hummingbot sidecar (behind M11), M16 costs |
| **Phase** | 6 (optional module; hidden from nav when disabled) |
| **Mock-up reference** | `hummingbot-high-frequency-market-making-pure-mm-terminal.png` |

## Purpose

Run and supervise crypto market-making / arbitrage bots (pure MM, Avellaneda, cross-exchange, grid, LP) as one more "venue" governed by the risk manager.

## Layout by tier

| Tier | Layout |
|---|---|
| ≥ 2xl | Bots table (12) + selected bot detail (12): spread ladder, inventory gauge, P&L decomposition, order book with own quotes |
| xl–md | Bots table; detail below |
| ≤ ph | Bot cards → detail page |

## Widgets

| Widget | Shows | Source |
|---|---|---|
| Bots table | Bot, strategy type, pair(s), venue(s), status, uptime, P&L (spread capture vs inventory P&L), inventory skew, fill rate, fees/rebates, risk status | `/mm/bots`, WS `mm` |
| Quote ladder | Own bid/ask levels vs book, current spreads, order refresh rate | WS `mm`, `md.book` |
| Inventory gauge | Base/quote balance vs target, skew limit | WS `mm` |
| P&L decomposition | Spread capture, inventory mark-to-market, fees/rebates, funding | `/mm/bots/{id}/pnl` |
| Config | Strategy parameters (spread, order levels, refresh, inventory target/skew, hanging orders) in `ParamForm` | `/mm/bots/{id}` |
| Health | Hummingbot API connectivity, telemetry **disabled** check, broker-ID stripping check, API rate headroom | `/system/services?kind=hummingbot` |

## Actions

| Control | Command | Level |
|---|---|---|
| Create bot from template | `mm.bot.create` | C1 (paper) |
| Start / stop bot | `mm.bot.start` / `mm.bot.stop` | Start: C1 paper, C3 live (quotes on its own, like `autonomous`). Stop: C1 |
| Edit params | `mm.bot.update` | C1 paper; C2 live; C3 if risk increases (size, levels, inventory limits) |
| Cancel all MM orders | `mm.bot.cancel_all` | C1 |

**Kill switch ON:** all bots stop (a server-side guarantee); the UI shows "Stopped by kill switch".

## Acceptance criteria

1. **Risk limits:** every bot's exposure counts toward global risk limits (shown in D06).
2. **Telemetry check:** a bot can't start if the telemetry-disabled check fails.

## Backend contract

- **Queries:** `/mm/bots` (+ `/{id}`, `/{id}/pnl`), `/system/services?kind=hummingbot`.
- **WebSocket topics:** `mm`, `md.book`, `kill`.
- **Commands:** `mm.bot.create|start|stop|update|cancel_all` _(added to architecture §7.2)_.
