# D12 · Airdrops & Launches

| | |
|---|---|
| **Routes** | `/airdrops` (radar), `/airdrops/:id` (opportunity detail), `/airdrops/wallet` (hot wallet & mandates) |
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
- **Scores:** **risk score** (`RiskScoreBadge`, top 3 reasons) and **viability score** (funding, TVL trend, expected value range, cost/time, sybil-filter strictness, **AU geo/KYC restriction**).
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
| Path | **Auto-claim** (mandate coverage, simulation result: "+X tokens, −gas, no other state change") **or** user task steps (link to D13) | `/airdrops/{id}`, `/tasks?opportunity=` |
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

| Widget | Shows |
|---|---|
| Hot wallet | Address(es) per chain, balances (small by policy), gas reserves, cap usage today |
| Mandates | Wallet, chain, allowed contracts/functions, gas/value caps, expiry, status |
| Approvals audit | Token approvals on the hot wallet, flagged risky ones, last weekly audit |
| Exec log | Claims executed with simulation diff + tx link |

**Actions:**

| Control | Command | Level |
|---|---|---|
| Create mandate | `airdrop.mandate.create` | **C3** |
| Revoke mandate | `airdrop.mandate.revoke` | C1 |
| Revoke approval | `wallet.revoke_approval` | C2 |
| Sweep to cold address (allow-listed) | `wallet.sweep` | C2 |

## Rules & states

- **Never offered in the UI** (enforced server-side too): connect-wallet, sign permits, approvals to unknown contracts, sybil/multi-wallet, or automated social actions.
- **Links:** every link is re-checked against blocklists when rendered; unsafe links render as plain text with a warning.
- **Kill switch ON:** auto-claims are frozen.

## Acceptance criteria

1. **Reject reasons:** every rejected opportunity shows its reasons. Every auto-claim shows mandate + simulation + tx + journal links.
2. **AU restrictions:** AU geo/KYC exclusions are visible before any task is created.

## Backend contract

- **Queries:** `/airdrops` (+ `/{id}` with `risk`, `eligibility`, `history`), `/airdrops/mandates`, `/airdrops/wallet`, `/tasks?opportunity=`.
- **WebSocket topics:** `airdrop`, `tasks`, `kill`.
- **Commands:** `airdrop.*`, `wallet.revoke_approval`, `wallet.sweep` _(added to architecture §7.2)_.
