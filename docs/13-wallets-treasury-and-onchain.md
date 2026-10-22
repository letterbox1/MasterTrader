# Wallets, Treasury, Hold-and-Earn & On-Chain Execution (M22, M23)

_Adopted from the CryptoTrader spec ([review](11-cryptotrader-crossover-review.md)). Security rules complement [07](07-security-notes.md) §4. Figures are from CryptoTrader research (Sep–Oct 2026); vendor / secondary / (U) labels are kept. Not financial advice._

## 1. Custody tiers

A fully air-gapped machine can't also serve an API. So bots sign only with **capped hot keys**, and everything above the cap moves through an offline signer.

**Vault and warm are watch-only:** the system never holds their keys. It may *prepare* unsigned transactions (QR / WalletConnect) for you to sign in your own wallet.

| Tier | Holds | Key location | Signs how | Limit |
|---|---|---|---|---|
| **Vault (cold)** | Treasury stablecoins, BTC, long holds | Air-gapped hardware (e.g. your Ellipal Titan: MetaMask-QR signing only, no EIP-712, no xpub) | Unsigned transaction prepared as QR/file, signed offline by you, broadcast from the online side | **Manual only**; watch-only in the system; sweeps *to* it are automatic (receiving needs no key) |
| **Hyperliquid master** (only if Hyperliquid is approved, see 12 §1) | Deposits, withdrawals, agent approval, vault transfers | Hardware signer with EIP-712 (Ledger Flex/Nano X or Trezor Safe 5) | Software builds the action on an offline host; you sign on the device after an independent hash check | Manual only |
| **Warm** | Staking, node collateral, governance | Hardware wallet (yours) | The system prepares an unsigned transaction; you sign it on the device | Manual only; watch-only in the system |
| **Hot (trading)** | Working capital per sleeve | Signer service (isolated) | Automatic after policy + cost gate + simulation | Float default ≤ A$500 per chain; per-transaction and rolling 24 h caps |
| **Airdrop identity** | One long-lived wallet **per chain** (EVM, Solana) with organic history | Signer service (capped) | Mandated claims (all autonomous claims use it, never the hot wallet) / genuine-use tasks | Float default ≤ A$300 per chain; never used for memecoin churn or unvetted contracts |
| **Burner** | Interacting with new dApps/airdrop sites during vetting | Signer service | Automatic, tiny float | Float default ≤ A$50; refilled to the float only |

**Rules:**
- **The burner goes first.** The identity wallet only follows a successful burner run.
- **Separate wallets by purpose**, and keep investment and trading wallets separate for tax.
- **No multi-wallet airdrop participation.**
- **Sweeps:** hot balances above the float sweep to the vault address daily (default). Moving funds *out of* the vault is always manual and signed offline.
- **Kill switch:** stops new trading, cancels orders, applies each bot's failure policy and freezes new treasury/earn moves. From P5 (default on) it also sweeps hot trading balances to the vault address; sweeps *to* the vault and approval revokes are protective, so the freeze doesn't block them.

**Default limits (configurable, [16 §2.7](16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)):**

| Setting | Default |
|---|---|
| Hot (trading) float | ≤ A$500 per chain |
| Airdrop identity float | ≤ A$300 per chain |
| Burner float | ≤ A$50 |
| Signer per-transaction cap | A$250 |
| Signer rolling 24 h cap | A$1,000 per wallet |
| Daily gas budget | Airdrops A$20/day · DEX trading A$50/day (§7) |

Tightening is immediate; loosening is C3. The defaults only prefill the form: **signing stays disabled until you confirm these numbers on first setup** (a USER task in Phase 5).

## 2. Signer service (the only process that sees hot keys)

- **Keys:**
  - stored in **OpenBao** (MPL-2.0 fork of Vault) or as sops-encrypted files;
  - loaded into memory at start;
  - never logged and never in `.env`.
- **Interface:**
  - accepts **intents** over a local socket / mTLS **only from the policy service**, never raw transactions. `airdrop-exec` is the policy service in P5 (claims, revokes, sweeps); treasury (P6) and DEX execution (P7) also go through it, never straight to the signer;
  - re-decodes and re-builds everything itself.
- **Enforced checks:**
  - a per-wallet allow-list of programs/contracts;
  - per-transaction and rolling 24 h caps (defaults in §1);
  - the **cost gate** (§7, the `mt_onchain.costgate` library);
  - **mandatory successful simulation** (Solana `simulateTransaction`; local **Anvil** fork for EVM). These are the only simulators; Tenderly is not used.
  - Simulation is a sanity check only: adversarial tokens can behave differently on execution.
- **Hard blocks (in code):**
  - EIP-2612 `permit` and Permit2 signatures, `setApprovalForAll`, unlimited approvals;
  - Solana `SetAuthority` / SPL `Approve` it didn't build;
  - any unknown program ID or router.
  - **Approvals are sized to the trade and revoked after.**
- **Durable nonces:**
  - Never sign a nonce transaction the system didn't build and decode itself.
  - Advance or close unused nonce accounts after each cold-signing session.
  - Alert on any change of nonce authority.
  - Background: pre-signed durable-nonce transactions never expire, and that's how ~US$270M was drained from Drift in Apr 2026.
- **Hyperliquid:**
  - **Agent keys** trade but can't withdraw. They're rotated to **fresh addresses, never reused**, and approved with a `valid_until` expiry.
  - After deregistration, an agent's nonce state may be pruned, which allows replay of old signed actions.
  - Master actions (`approveAgent`, `usdSend`, `withdraw`, `vaultTransfer`…) are EIP-712 under `HyperliquidSignTransaction` and **only** on the master hardware signer.
- **Audit:** every signature goes to the ledger with the intent that caused it.
- **Third-party code:**
  - **Third-party bot code never runs with a real key.**
  - SlowMist documented open-source pump.fun "sniper" repos that exfiltrated `.env` keys, with fake stars. Popularity is worthless as a trust signal in this niche.

## 3. Unified wallet view

Wallet apps (MetaMask, Trust Wallet, Phantom, Rabby, Ledger, Ellipal) have no portfolio API, so the view is built from **public addresses**.

1. **Register** every address in `ops.wallets`, the one registry for accounts and on-chain addresses (created in P3, extended additively by the P5 wallet-indexer; there is no separate treasury wallet table): address, chain, provider label ("Trust Wallet – phone"), role (vault, warm, hot, identity, burner, governance), tax segregation (investment vs trading).
   - **Proof of control:** you sign a one-time challenge in **your own wallet app** (EIP-4361-style text on EVM, Solana `signMessage`), or make a tiny self-transfer. **The system never signs it.** Signer-created wallets (hot, identity, burner) are registered by the signer itself.
2. **Read** (read-only):
   - Helius DAS `getAssetsByOwner` (Solana);
   - Blockscout/own RPC + DefiLlama adapters logic (EVM positions); Zerion's free tier is optional (U);
   - Hyperliquid `/info`;
   - ccxt with **read-only, IP-locked** keys for exchanges;
   - prices from our own recorded data per the valuation hierarchy ([16 §4.1](16-configuration-and-safety-model.md#41-valuing-crypto-for-the-journal)); CoinGecko (cached ≤ 24 h) is a display cross-check only.
3. **Reconcile** monthly against **rotki** (self-hosted, AGPL; fine privately) and daily against the journal.
4. **Render:** total → chain → provider → protocol → position, in base currency (UI D18).
5. **Manual signing** happens **in your own wallet**, never in the system. The system may prepare an unsigned transaction and hand it over as a QR (vault) or a WalletConnect / EIP-6963 request (phone or browser wallet); you review and sign there. **The system never holds vault or warm keys**, and P5 has no UI signing path (D18 is a view); any later prepare-to-sign feature builds unsigned payloads only and is scoped separately.

## 4. Hold-and-earn module (M22, `mt_treasury`)

Idle capital earns while it waits.
- Every position is scored on **net yield after gas, lock-up and smart-contract risk**.
- Warm-wallet actions need your approval.
- Moves happen only between **allow-listed** protocols, and adding a protocol is a manual decision.
- Automated moves sign only through the policy service and the cost gate (§2, §7).

| Type | Examples | Earns | Main risks | Automation |
|---|---|---|---|---|
| Native / liquid staking | JitoSOL, mSOL (~6–6.7% APY, vendor); stETH (10% protocol fee) | Staking yield (+ points) | Depeg, exploit, unbonding | Rebalance suggestions; you approve; peg alerts |
| Stablecoin lending | Core Aave, Spark, Kamino markets | Interest | Exploit, rate collapse, **curator risk in third-party vaults** (Stream Finance Nov 2025: ~US$160M frozen) | Auto-move within the allow-list + caps |
| Fixed yield | Pendle PTs | Yield to maturity | Protocol, liquidity at exit | Suggest; you approve |
| Hyperliquid HLP (if approved) | HLP vault | Share of the market-making P&L (past-month APR ~4% late Sep 2026) | Shared losses (~US$4M Mar 2025; POPCAT bad debt Nov 2025); **4-day lock that resets on each deposit** | Default **≤ 10% of stablecoins and ≤ 5% of total portfolio, whichever is smaller** ([16 §2.7](16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13); raising it is C3); one deposit per cycle |
| Nodes (light/testnet/incentivised) | Per programme | Possible airdrop/rewards | Malicious node software; rewards never materialise; often KYC / one per person | Pinned container on a separate network; retire when EV < 0 |
| Validators | ETH solo (32 ETH), Lido CSM (2.4 → 1.3 ETH bond), Rocket Pool Saturn I (4 ETH), DVT | Rewards + MEV | Slashing (same key on two machines), penalties | Only with idle long-term ETH; **Solana validators: avoid** (1.6 SOL per epoch admission ≈ 290 SOL/yr) |

**Yield allocator:**
- **Net yield** = `apyBase` (never rely on `apyReward` emissions) − entry/exit gas amortised over the expected hold − a risk haircut (protocol age, audits, TVL trend).
- **Caps:** default ≤ 20% of treasury per protocol ([16 §2.7](16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)), plus per-chain and per-stablecoin caps; all configurable.
- **Discovery:** DefiLlama's official free yields API host `yields.llama.fi` (cached hourly; no site scraping, [12 §4](12-policy-and-compliance.md#4-per-platform-data--automation-rules)).

**Node/validator earnings, monthly:**
- `net = rewards + MEV fees + commission − infra − ops time − E[slash] − opportunity cost`.
- Start only if positive under conservative inputs; retire after two negative months.
- **Operations:**
  - slashing-protection DBs backed up;
  - one key per machine;
  - withdrawal and reward addresses go to the vault/warm wallet;
  - client diversity;
  - missed-duty alerts;
  - hard-fork schedule tracked.

**DAO monitoring:**
- Snapshot GraphQL (100 req/min keyless) and Tally (free key) alert on proposals that change **parameters, oracles or treasuries** in protocols we hold.
- Votes are drafted for your confirmation from a dedicated governance key, one wallet per DAO.

**NFT/payments:** low value.
- x402 / Solana Pay are only useful for our own agents paying per call.
- NFTs are valued at floor minus fees.

## 5. Treasury

- **Your target split:** working floats per sleeve, stablecoin reserve, cold holdings.
- **Daily sweep:** realised profit above the floats → stablecoins → vault address.
- **Stablecoin concentration limits,** so one issuer failing is survivable.
- **Reserve:** a target of 20–40% kept in stables/AUD (your setting in the treasury policy, D18).
- **EV hurdle** for airdrops and launches ([08](08-airdrops-and-token-launches.md#expected-value-gate-airdrops-icosidos-points-programmes)): default 5% p.a. on capital locked (AUD cash-rate proxy), configurable ([16 §2.7](16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)). It stays a fixed default until the P6 treasury has a live stablecoin yield you choose to use instead.

## 6. Monitors (feed M16 and M11)

| Monitor | Rule |
|---|---|
| Stablecoin depeg (USDC, USDT, USDe, USDG…) | Deviation beyond **50 bps** (default, configurable, [16 §2.7](16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)). **Before P6:** alert + task only, with no automated reduce. **From P6:** the treasury reduces exposure, on-chain through the policy service and cost gate |
| Protocol exploit / oracle deviation / sharp TVL drop | Auto-withdraw from that protocol (if allow-listed for auto; from P6), else an urgent task |
| Venue health | Our own measured withdrawal/deposit times, venue deposit/withdraw flags, status pages and proof-of-reserve changes via the venue watch ([06](06-aggregators-and-market-providers.md#regulatory--venue-watch-m5--m16)); **AUSTRAC registration status** is a quarterly USER re-check (`VENUE_CHECK`), not automated (12 §2) |
| Bridge policy | Native USDC via CCTP or canonical bridges only; per-bridge caps; **no bridging inside a live strategy leg** |
| Hyperliquid | HLP lock in the liquidity plan; alerts on manipulation events |
| Concentration | Per protocol, chain, stablecoin and venue. Venue: default **≤ 25% of total equity per venue** [10–30%], one value everywhere, set in the L1 risk policy ([16 §2.1](16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)); loosening is C3 |

## 7. On-chain cost gate & DEX execution (extends M12 / M16)

**Rule:** no on-chain action is signed unless its expected benefit exceeds its all-in cost by a set margin: default **≥ 2×** all-in cost (gas + fees + impact + MEV/tips), configurable ([16 §2.7](16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)). `gate(action) → allow / wait / reject`, with the numbers logged.

The gate is one library, `mt_onchain.costgate`: the signer path uses it from P5 and the treasury from P6. Gas and fees are **live inputs** from our RPCs and venue APIs, never constants ([16 §4.3](16-configuration-and-safety-model.md#43-live-inputs-instead-of-constants)).

| Cost | Formula / source |
|---|---|
| Solana transaction | `C = 5000·n_sig + μ·CU_limit + tip_jito` (lamports); μ is sampled from `getRecentPrioritizationFees` / Helius `getPriorityFeeEstimate`; Jito tip-floor feed (p25–p99), tip **inside** the transaction, min 1,000 lamports, bundles ≤ 5 transactions |
| EVM transaction | `C = gas_used·(baseFee + priorityFee) + L1_data`. `gas_used` comes from the Anvil fork simulation (not the wallet estimate); the L1 data fee comes from the chain's fee oracle (OP-stack formulas changed across upgrades, so never hard-code it); `eth_feeHistory` |
| AMM price impact (constant product, fee φ) | `Δx = x·Δy(1−φ) / (y + Δy(1−φ))`; pump.fun pre-graduation uses the bonding-curve formula; CEX orders walk the L2 book |
| All-in round trip | Entry transaction + exit transaction + entry/exit impact at your size + venue fees + withdrawal fees |

**Policies:**
- **Airdrop/yield gas windows:** by default, wait for a base fee below its 7-day 30th percentile unless the deadline is < 48 h (configurable).
- **Tips:** raise priority/tips only where the edge decays fast.
- **Budgets:** daily gas spend per module, default airdrops A$20/day and DEX trading A$50/day; alert at 80%, stop at 100% (configurable, [16 §2.7](16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)).

**DEX execution (free tiers):**
- **Solana:** Jupiter (Portal key, 1 rps) + Jito.
- **EVM:** 1inch (100k calls/month free) + **Flashbots Protect** (Ethereum L1; free, no fee on reverts).
- **Slippage:** tight slippage and private submission (high-slippage bot users are the main sandwich victims).
- **Raydium:** build instructions from the Apache-2.0 IDLs (the TypeScript SDK v2 is GPL).

**RPC (free tiers, one account each):**
- **Solana:** Helius Free (1M credits, 10 rps) with Chainstack/QuickNode/PublicNode fallbacks.
- **EVM:** Alchemy Free (30M CU/month) with Infura/PublicNode fallbacks.
- **Indexing:** The Graph (100k queries/month).
- **Paid upgrades** (Helius Developer $49, Yellowstone gRPC ~$98) only once logs prove a free tier is losing money.

## 8. Social participation (M23, `mt_social`)

Social tasks run from **your real accounts, with you approving every post**. The system removes the grind (finding tasks, drafting, tracking) without pretending to be anyone.

**What it does:**
- **Task parsing:** quest tasks needing a social action (follow, like, repost, reply, join, link an account) are queued in D13 with the campaign's EV.
- **Drafts:**
  - written by a local model in your voice, grounded in what you actually did or hold;
  - you **approve / edit / skip**;
  - a **holdings disclosure line** is added to any post about a token you hold;
  - drafts never go out unreviewed.
- **Posting:**
  - an **X web-intent link** opens with the text prefilled and **you click Post** (no X API cost);
  - the post URL is captured back (pasted, or read from your timeline if X is ever enabled);
  - the task is marked done with proof links.
- **Credibility scoring:** accounts you follow are scored on their past calls against outcomes in the journal. This becomes a per-account credibility feature.
- **Shill-burst posture:**
  - the ratio of social mentions to on-chain unique-buyer growth;
  - mention spikes from new or low-follower accounts without matching buyers mark a coordinated push;
  - this is a dump-risk signal for strategies and airdrop vetting.
  - Telegram contributes **counts only** (12 §4).

**Not built:** extra accounts/personas, auto-posting, engagement pods, pay-to-post ("yap") schemes, captcha solving.
