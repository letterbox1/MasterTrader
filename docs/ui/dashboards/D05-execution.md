# D05 · Execution

| | |
|---|---|
| **Route** | `/execution` (tabs: Positions · Orders · Fills · Approvals · TCA · Venues) |
| **Modules** | M12 execution, M11 risk, M16 TCA/reconciliation |
| **Phase** | 2 |
| **Mock-up reference** | `order-execution-hub-smart-routing-engine.png` |

## Purpose

Everything about what is (or should be) in the market:
- positions and orders across all venues;
- the approvals queue;
- manual trading;
- execution quality (TCA);
- venue/account health.

## Layout by tier

| Tier | Layout |
|---|---|
| ≥ 2xl | KPI strip (gross/net exposure, open orders, pending approvals, today fees, avg slippage bps, unreconciled items) + tabs; right dock: `OrderTicket` (pinned) |
| xl/lg | Tabs; ticket as a drawer (`b`/`s` shortcuts) |
| md | Tabs; tables with P1/P2 columns |
| ≤ ph | Segmented tabs (Positions · Orders · Approvals · More); card lists; sticky "New order" button |
| landscape-short | Two-pane: list left, detail right |

## Tabs & widgets

| Tab | Shows | Source |
|---|---|---|
| **Positions** | Per position: instrument, venue/account, side, qty, avg price, mark, unrealised P&L, % of exposure limit, leverage, liquidation distance (perps/CFDs), strategy, mode (paper/live), reconciliation status | `/positions`, WS `positions` |
| **Orders** | Open + recent: time, instrument, side, type, qty, filled, price, status, strategy/source (strategy / manual / agent / MCP), risk decision, TIF | `/orders`, WS `orders` |
| **Fills** | Fills with fees, liquidity (maker/taker), venue, slippage vs decision & arrival | `/fills`, WS `fills` |
| **Approvals** | Pending approval requests (`ApprovalCard`): intent, source, rationale/provenance, risk preview, TTL; history of approved/rejected/expired | `/orders?status=pending_approval`, WS `orders` (approval events) |
| **TCA** | Implementation shortfall by strategy × venue × instrument; delay / spread-impact / fees decomposition; realised vs modelled ratio (alert > 1.5×); slippage distribution; fill rate; time to fill | `/data/costs?tca=1` |
| **Venues** | Per venue/account: connection status, latency, rate-limit headroom, balances, margin, sub-account mode (paper/approve/auto), key age (from metadata), last reconciliation result | `/system/services?kind=venue`, `/data/recon`, `/system/keys` (masked) |

## Actions

| Control | Location | Command | Level |
|---|---|---|---|
| New order | Ticket | `order.place` | C2 (risk preview must pass) |
| Modify order | Order row | `order.modify` | C2 |
| Cancel order | Order row | `order.cancel` | C1 |
| Cancel all (scope: all / venue / strategy / instrument) | Orders header | `order.cancel_all` | C2 |
| Close / reduce position | Position row | `position.close` / `position.reduce` | C2 |
| Set TP/SL brackets | Position row | `position.set_brackets` | C2 |
| Approve / reject | Approvals | `approval.approve` / `approval.reject` | C2 / C1 |
| Bulk approve | Approvals (≤ 5 items, same strategy) | `approval.approve` ×n | C2 (shows the combined risk preview) |
| Run reconciliation now | Venues | `data.recon.run` | C1 |
| Export CSV | Each table | — | C0 |

## States & rules

- **Unreconciled positions:** hatched + "unconfirmed". Close actions require reconciliation first, unless using emergency flatten via the kill switch.
- **Kill ON:** all trading actions disabled except cancel and flatten-via-kill.
- **Approvals:** show a TTL countdown; expired requests move to history automatically.
- **Source badges:** orders from MCP/agents always show a source badge.

## Acceptance criteria

1. **Approvals:** an approval can be completed on a phone in ≤ 2 taps after opening the request (approve → hold-to-confirm).
2. **Cancel all:** works under 1 s from confirm to all cancels sent (server metric shown in the toast).
3. **TCA:** numbers reconcile with fills (the sum of fees equals the fills' fees).

## Backend contract

- **Queries:**
  - `/positions`, `/orders`, `/fills`;
  - `/data/costs?tca=1`, `/data/recon`;
  - `/system/services?kind=venue`, `/system/keys`;
  - `POST /risk/preview`.
- **WebSocket topics:** `positions`, `orders`, `fills`, `risk.event`, `kill`.
- **Commands:** `order.*`, `position.*`, `approval.*`, `data.recon.run`.
