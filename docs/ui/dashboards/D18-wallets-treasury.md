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
| Allocation | By custody tier, venue, asset class, sleeve; concentration vs the **configured** venue cap (default ≤ 25% of total equity, range 10–30%, [16 §2.1](../../16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown); loosening = C3) | `/wallets?group=` |
| Wallet table | Wallet/account (registry `ops.wallets`), custody tier (vault / HL master / warm / hot / identity / burner), chain/venue, `investment` vs `trading` tag, balance vs float (defaults: hot ≤ A$500 per chain, identity ≤ A$300, burner ≤ A$50; configurable, [16 §2.7](../../16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)), signer cap usage, last activity | `/wallets` |
| Internal transfers | Moves between your own wallets, tagged internal (never disposals) | `/wallets/transfers` |
| Venue health | AUSTRAC status + date checked, withdrawal delays, PoR changes, registry status | `/venues/registry` |

## `/wallets/treasury` and `/wallets/earn`

| Widget | Shows |
|---|---|
| Treasury policy | Cash buffer target, stablecoin mix and depeg threshold (default > 50 bps), yield venues allowed, per-protocol cap (default ≤ 20% of treasury), HLP cap (default ≤ 10% of stablecoins and ≤ 5% of total portfolio, whichever is smaller). All are settings showing their layer and default |
| Hold-and-earn positions | Staking/lending/LP positions: APY (net of fees), lockup/unbonding, protocol risk score, exit cost, P&L incl. rewards |
| Rewards ledger | Rewards accrued/claimed with journal links (income classification) |
| On-chain cost gate | Last quotes: expected edge vs gas + slippage + MEV + fees (default margin: benefit ≥ 2× all-in cost); gas window (base fee below its 7-day 30th percentile unless a deadline is < 48 h); blocked moves with reasons |

## Actions

| Control | Command | Level |
|---|---|---|
| Register wallet/address (proof of control: you sign a one-time challenge in **your own wallet app** (EIP-4361-style text / Solana `signMessage`) and paste it back, or make a tiny self-transfer; the system never signs it) | `wallet.register` | C1 |
| Tag wallet (investment / trading, tier) | `wallet.tag` | C1 |
| Allocate / rebalance treasury | `treasury.allocate` | **C2** (cost-gate preview); loosening policy is **C3** |
| Enter / exit hold-and-earn position | `treasury.earn.enter` / `treasury.earn.exit` | C2 |
| Revoke approval | `wallet.revoke_approval` | C2 |
| Sweep to allow-listed cold address | `wallet.sweep` | C2 |
| Update venue registry entry | `venue.registry.update` | C1 to tighten, **C3** to allow a venue/product |

## Rules & states

- **Never offered:** seed/private-key entry, withdrawal to a non-allow-listed address, unlimited approvals, signing a nonce transaction the system didn't build.
- Vault and warm wallets are **watch-only** (no signing path from the UI): the system never holds their keys. It may *prepare* unsigned transactions (QR / WalletConnect) for you to sign in your own wallet.
- **Signing disabled until confirmed:** signing stays off until you confirm the floats, signer caps and gas budgets on first setup (Phase 5 USER task); the defaults only prefill the form.
- **Kill switch ON:** new treasury moves and hold-and-earn entries are frozen; exits stay available at C2. From Phase 5 (default on) kill also **sweeps hot trading balances to the vault address**; sweeps-to-vault and approval revokes are protective and exempt from the freeze.
- A depeg alert (stablecoin beyond the threshold) shows a banner. Before the Phase 6 treasury exists it raises an alert + task only (no automated reduce); from Phase 6 the banner shows the reduce action taken.

## Acceptance criteria

1. Every balance shows native, USD and AUD with the rate source and timestamp.
2. Internal transfers never show as P&L or disposals, and they link to both wallet rows.
3. Every treasury move shows the on-chain cost gate result before confirmation.
4. Works from 240 px to 2560 px (cards ≤ ph, table ≥ md).

## Backend contract

- **Queries:** `/wallets` (+ `/{id}`, `/transfers`), `/treasury`, `/treasury/earn`, `/venues/registry`.
- **WebSocket topics:** `wallet`, `treasury`, `alert`, `kill`.
- **Commands:** `wallet.register`, `wallet.tag`, `wallet.revoke_approval`, `wallet.sweep`, `treasury.allocate`, `treasury.earn.enter`, `treasury.earn.exit`, `venue.registry.update`.
