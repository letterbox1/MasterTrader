# D18 · Wallets & Treasury

| | |
|---|---|
| **Routes** | `/wallets` (unified view), `/wallets/:walletId`, `/wallets/treasury`, `/wallets/earn` (hold-and-earn) |
| **Modules** | M22 treasury & hold-and-earn, M4 (hot/burner/identity wallets), M12 (DEX execution), M16 (on-chain monitors), M18 (internal-transfer tagging) |
| **Phase** | 5 (unified view, monitors) / 6 (hold-and-earn, treasury moves) |
| **Mock-up reference** | — (new; reuse the tile language of Cockpit and Launch Radar) |
| **Spec** | [13 Wallets, treasury & on-chain](../../13-wallets-treasury-and-onchain.md) |

## Purpose

One place to see **everything you own, everywhere** (exchange accounts, broker cash, on-chain wallets per custody tier) and to manage idle capital:
- custody tier and limits per wallet;
- treasury allocation (cash buffer, stablecoin yield, hold-and-earn positions);
- on-chain health (approvals, depeg, venue health, nonce authority).

## Layout by tier

| Tier | Layout |
|---|---|
| ≥ 2xl | Net worth + allocation donut (6) · wallet table (12) · right: alerts, approvals, depeg/venue health (6) |
| xl–md | Summary strip; wallet table; side column stacked below |
| ≤ ph | Segmented (Summary · Wallets · Earn · Alerts); cards |

## `/wallets`: unified view

| Widget | Shows | Source |
|---|---|---|
| Net worth | Total in **AUD and USD** (native per row), change 24h / 7d / FY | `/wallets` |
| Allocation | By custody tier, venue, asset class, sleeve; concentration vs venue cap (≤ 25–30%) | `/wallets?group=` |
| Wallet table | Wallet/account, custody tier (vault / HL master / warm / hot / identity / burner), chain/venue, `investment` vs `trading` tag, balance, cap usage, last activity | `/wallets` |
| Internal transfers | Moves between your own wallets, tagged internal (never disposals) | `/wallets/transfers` |
| Venue health | AUSTRAC status + date checked, withdrawal delays, PoR changes, registry status | `/venues/registry` |

## `/wallets/treasury` and `/wallets/earn`

| Widget | Shows |
|---|---|
| Treasury policy | Cash buffer target, stablecoin mix and depeg thresholds, yield venues allowed |
| Hold-and-earn positions | Staking/lending/LP positions: APY (net of fees), lockup/unbonding, protocol risk score, exit cost, P&L incl. rewards |
| Rewards ledger | Rewards accrued/claimed with journal links (income classification) |
| On-chain cost gate | Last quotes: expected edge vs gas + slippage + MEV + fees; blocked moves with reasons |

## Actions

| Control | Command | Level |
|---|---|---|
| Register wallet/address (proof of control) | `wallet.register` | C1 |
| Tag wallet (investment / trading, tier) | `wallet.tag` | C1 |
| Allocate / rebalance treasury | `treasury.allocate` | **C2** (cost-gate preview); loosening policy is **C3** |
| Enter / exit hold-and-earn position | `treasury.earn.enter` / `treasury.earn.exit` | C2 |
| Revoke approval | `wallet.revoke_approval` | C2 |
| Sweep to allow-listed cold address | `wallet.sweep` | C2 |
| Update venue registry entry | `venue.registry.update` | C1 to tighten, **C3** to allow a venue/product |

## Rules & states

- **Never offered:** seed/private-key entry, withdrawal to a non-allow-listed address, unlimited approvals, signing a nonce transaction the system didn't build.
- Vault and warm wallets are **watch-only** (no signing path from the UI).
- **Kill switch ON:** treasury moves and hold-and-earn entries are frozen; exits stay available at C2.
- A depeg alert (stablecoin below threshold) shows a banner and the auto-reduce action taken.

## Acceptance criteria

1. Every balance shows native, USD and AUD with the rate source and timestamp.
2. Internal transfers never show as P&L or disposals, and they link to both wallet rows.
3. Every treasury move shows the on-chain cost gate result before confirmation.
4. Works from 240 px to 2560 px (cards ≤ ph, table ≥ md).

## Backend contract

- **Queries:** `/wallets` (+ `/{id}`, `/transfers`), `/treasury`, `/treasury/earn`, `/venues/registry`.
- **WebSocket topics:** `wallet`, `treasury`, `alert`, `kill`.
- **Commands:** `wallet.register`, `wallet.tag`, `wallet.revoke_approval`, `wallet.sweep`, `treasury.allocate`, `treasury.earn.enter`, `treasury.earn.exit`, `venue.registry.update`.
