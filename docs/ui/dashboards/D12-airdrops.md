# D12 · Airdrops & Launches

| | |
|---|---|
| **Routes** | `/airdrops` (radar), `/airdrops/:id` (opportunity detail), `/airdrops/wallet` (airdrop identity wallets & mandates) |
| **Modules** | M4 airdrops/launches, M19 tasks, M18 journal (income) |
| **Phase** | 5 |
| **Mock-up reference** | `vetted-launch-radar-au-eofy-tax-ledger.png` (remove "sybil task pipeline" / auto-social; see content corrections) |

## Purpose

Show only **vetted, viable** airdrops, token launches and ICO/IDOs:
- with risk scored against rug-pull and scam signals;
- executing safe eligible claims automatically under mandates;
- turning everything else into clear, step-by-step user tasks.

## `/airdrops`: radar

| Tier | Layout |
|---|---|
| ≥ 2xl | Filters (6) · opportunities list (12) · right: claims due + recent auto-claims + rejected-with-reasons (6) |
| xl–md | Filters bar; list; side column stacked |
| ≤ ph | Segmented (Viable · Watching · Rejected · Claims); cards |

**Opportunity card/row:**
- **Identity:** project, chain(s), kind (airdrop / launch / ICO-IDO / quest / points), stage (rumoured / confirmed / snapshot / claim live / ended).
- **Scores:** **risk score** (`RiskScoreBadge`, top 3 reasons) and **viability score** (funding, TVL trend, expected value range vs the EV hurdle (default 5% p.a. on capital locked, configurable, [16 §2.7](../../16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)), cost/time, sybil-filter strictness, **AU geo/KYC restriction**).
- **Timing and status:** deadlines; your eligibility status.
- **Next action:** auto-claim / user task / watch.

**Filters:** chain, kind, stage, min viability, max risk, deadline window, eligibility.

## `/airdrops/:id`: detail

| Section | Shows | Source |
|---|---|---|
| Overview | Official domain (verified via CoinGecko/DefiLlama, WHOIS age), socials, funding, docs, timeline | `/airdrops/{id}` |
| Risk report | Hard-fail checks (blocklists, honeypot/sell simulation, approval-granting signatures, domain mismatch, unverified contract); contract (EVM) / token (Solana) findings; liquidity; holder distribution & insider clusters; deployer history; off-chain signals; per-provider raw reports (GoPlus, RugCheck, Honeypot.is) collapsed | `/airdrops/{id}?risk=1` |
| Viability | Score breakdown + expected value range + cost estimate (gas, capital, time) | `/airdrops/{id}` |
| Eligibility | Checks against the official claim contract / Merkle proof using the **public address only** | `/airdrops/{id}?eligibility=1` |
| Path | **Auto-claim** from the chain's **airdrop identity wallet** (signer-held; never the hot trading wallet): mandate coverage, cost-gate result (benefit ≥ 2× all-in cost by default), simulation result ("+X tokens, −gas, no other state change") **or** user task steps (link to D13) | `/airdrops/{id}`, `/tasks?opportunity=` |
| History | Decisions, executions (tx hash), journal entry (income class: general vs initial allocation) | `/airdrops/{id}?history=1` |

**Actions:**

| Control | Command | Level |
|---|---|---|
| Re-score | `airdrop.rescore` | C0 |
| Reject (with reason) | `airdrop.reject` | C1 |
| Create user task | Auto-created; manual add via `airdrop.add_url` | C0 |
| Execute claim (no mandate) | `airdrop.claim.execute` | **C2** (simulation shown; Telegram notification) |
| Add URL to vet | `airdrop.add_url` | C0 |

## `/airdrops/wallet`: hot wallet & mandates

The wallets here are the **airdrop identity wallets** (signer-held, one per chain) and burners, not the hot trading wallet. The route and heading keep their old name for links.

| Widget | Shows |
|---|---|
| Identity wallets | Address(es) per chain, balances vs float (default ≤ A$300 per chain; burners ≤ A$50), gas reserves, gas budget used today (default A$20/day, alert at 80%), signer cap usage (defaults A$250 per transaction, A$1,000 per rolling 24 h). All defaults configurable ([16 §2.7](../../16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)) |
| Mandates | Wallet, chain, allowed contracts/functions, gas/value caps, expiry, status |
| Approvals audit | Token approvals on the identity and burner wallets, flagged risky ones, last weekly audit |
| Exec log | Claims executed with simulation diff + tx link |

**Actions:**

| Control | Command | Level |
|---|---|---|
| Create mandate | `airdrop.mandate.create` | **C3** |
| Revoke mandate | `airdrop.mandate.revoke` | C1 |
| Revoke approval | `wallet.revoke_approval` | C2 |
| Sweep to the vault address (allow-listed) | `wallet.sweep` | C2 |

## Rules & states

- **Never offered in the UI** (enforced server-side too): connect-wallet, sign permits, approvals to unknown contracts, sybil/multi-wallet, or automated social actions.
- **Links:** every link is re-checked against blocklists when rendered; unsafe links render as plain text with a warning.
- **Kill switch ON:** auto-claims are frozen.
- **Signing disabled until confirmed:** auto-claims stay off until you confirm the wallet floats, signer caps and gas budgets on first setup (a Phase 5 USER task); the defaults only prefill the form.
- **Disposal:** until live execution passes the Phase 7 gates, selling received tokens is a USER task (manual sale).

## Acceptance criteria

1. **Reject reasons:** every rejected opportunity shows its reasons. Every auto-claim shows mandate + simulation + tx + journal links.
2. **AU restrictions:** AU geo/KYC exclusions are visible before any task is created.

## Backend contract

- **Queries:** `/airdrops` (+ `/{id}` with `risk`, `eligibility`, `history`), `/airdrops/mandates`, `/airdrops/wallet`, `/tasks?opportunity=`.
- **WebSocket topics:** `airdrop`, `tasks`, `kill`.
- **Commands:** `airdrop.*`, `wallet.revoke_approval`, `wallet.sweep` _(added to architecture §7.2)_.
