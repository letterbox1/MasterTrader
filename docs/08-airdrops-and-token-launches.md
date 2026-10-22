# Airdrops, Token Launches & Community Curation (Module M4)

_Raw evidence: [research/airdrops-rugpull-discord.md](research/airdrops-rugpull-discord.md). Security rules: [07-security-notes.md §4](07-security-notes.md#4-crypto-wallets-airdrops-on-chain-claims). (U) = unverified._

## Principles

1. **Vet first, act second.** Only *viable* opportunities that pass rug-pull/scam screening reach the user or the executor.
2. **Act autonomously only where it's safe and permitted.** In practice that means claiming an airdrop your existing wallet already qualifies for, through that chain's **airdrop identity wallet** (signer-held, capped; never the hot trading wallet, [13 §1](13-wallets-treasury-and-onchain.md#1-custody-tiers)), under a mandate you signed. Everything else becomes **step-by-step instructions** in your task queue.
3. **No fake engagement, no sybil farming, no self-bots.** Social tasks (follow, retweet, join Discord, Galxe/Zealy/Layer3 quests) are always queued for you to do yourself.
4. **Everything is journalled** (tax class, AUD value at receipt per the valuation hierarchy in [16 §4.1](16-configuration-and-safety-model.md#41-valuing-crypto-for-the-journal), transaction hashes, decision trail).
5. **Numbers are configuration.** Wallet floats, signer caps, gas budgets and the EV hurdle below are **defaults, configurable** ([16 §2.7](16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)); loosening any of them is C3.

## Pipeline

```
DISCOVER → NORMALISE/DEDUP → ENRICH → RISK-SCORE → VIABILITY-SCORE → DECIDE → AUTO-CLAIM | USER TASK | WATCH | REJECT → TRACK → JOURNAL
```

| Stage | Free sources / tools |
|---|---|
| Discover | DefiLlama `/protocols` via the official API host `api.llama.fi` (tokenless protocols with rising TVL); CryptoRank Sandbox (ICO/IDO calendars, launchpads, funding rounds); CoinGecko Demo (new listings, categories); DexScreener (new pairs, profiles); Galxe GraphQL (read-only); Snapshot GraphQL and governance-forum JSON; the **Discord inbox** (followed announcement channels); Telegram channels (**postures only**: addresses, mention counts, channel spread; text never reaches a model, see [12 §4](12-policy-and-compliance.md#4-per-platform-data--automation-rules)); news/RSS; manual `/add <url>` via Telegram |
| Normalise | Key = (chain, contract), else the project slug. **Official domain** resolved from CoinGecko/DefiLlama, cross-checked with WHOIS age and blocklists. **Corroboration score:** how many independent listing sites/sources (DefiLlama, CryptoRank, CoinGecko, official X/Discord/docs) agree on the domain, contract and dates; < 2 independent sources → watch only |
| Enrich | **Blockscout** / own RPC (verified source, proxy/implementation, creator; Etherscan for manual lookups only, its terms bar decision use); Helius (Solana RPC, `getAsset`, mint/freeze authority, holders); DexScreener/GeckoTerminal (liquidity, pair age, volume); CryptoRank (funding) |
| Risk-score | **GoPlus** (EVM, primary) · **Honeypot.is** (EVM sell simulation) · **RugCheck.xyz** (Solana, primary) · re-implemented **solana-rugchecker** heuristics · **CRPWarner** concepts (hidden mint / sell limits / leaking token), plus an optional sandboxed Gigahorse deep-scan worker · optional Slither on verified source · blocklists (MetaMask eth-phishing-detect, ScamSniffer, polkadot-js, Chainabuse) |
| Calibrate | Private evaluation against the **SoK rug-pull dataset** (2,391 labelled ETH/BSC contracts) + CRPWarner ground truth + our own outcomes. The model is advisory; the rule-based baseline is authoritative |
| Act / queue | Policy service (`airdrop-exec` in P5) → intents-only signer ([13 §2](13-wallets-treasury-and-onchain.md#2-signer-service-the-only-process-that-sees-hot-keys)), using the airdrop identity wallet (or a burner during vetting), or the user-task queue |
| Track | Snapshot dates, claim windows, deadlines, `isClaimed`, vesting unlocks, post-claim liquidity/price, wallet approvals |
| Journal | Airdrop events in `journal.event` (airdrop established / initial allocation), linked to the campaign record → tax engine ([09](09-journal-and-tax.md)). ATO: *general* airdrops are ordinary income at receipt value; *initial allocations* have a $0 cost base, with CGT on disposal (U, confirm with a tax agent) |

### Risk score (0–100; any hard-fail = 100 = reject)

**Hard fails:**
- domain, claim contract or deployer on a blocklist;
- honeypot / sell simulation fails;
- the claim needs an approval-granting off-chain signature;
- the claim domain ≠ the official domain;
- unverified contract (for any autonomous path).

**Scored features:**
- **Contract (EVM):**
  - owner not renounced, with privileged functions;
  - hidden mint / owner can change balances;
  - blacklist or trading pause;
  - modifiable taxes;
  - upgradeable proxy with an EOA admin and no timelock;
  - `selfdestruct` / mutable `delegatecall`;
  - Slither high-severity findings.
- **Token (Solana):**
  - mint or freeze authority still active;
  - mutable metadata;
  - Token-2022 transfer-fee / permanent-delegate / transfer-hook / default-frozen extensions;
  - RugCheck flags.
- **Liquidity:**
  - LP burned or locked %, and when the lock expires;
  - liquidity in USD, and liquidity relative to FDV;
  - pair age.
- **Distribution:**
  - top-10/20 holder share, excluding pools, lockers and burn addresses;
  - insider or bundled-buy clusters (same funding source or same-slot buys);
  - deployer's share.
- **Deployer:**
  - wallet age;
  - previous tokens deployed and how many were rugs;
  - funded via a mixer.
- **Market:**
  - wash-trading patterns;
  - sudden liquidity pulls.
- **Off-chain:**
  - domain age;
  - age and consistency of social accounts;
  - audit from an allow-listed firm;
  - documentation exists;
  - copy-paste site template.

### Viability score

- **Strength of the opportunity:**
  - credible funding (investors, round size);
  - TVL and user trend;
  - confirmed vs rumoured token or points programme;
  - expected value from comparable airdrops.
- **Cost to take part:**
  - gas, capital and time per task;
  - how close the deadline is.
- **Fit for you:**
  - how strict the sybil filters are;
  - **geo/KYC restrictions (Australia excluded?)**;
  - your current eligibility (on-chain history vs the stated criteria).

## What may run autonomously

The executor only acts inside an active, user-signed, expiring **mandate**: one wallet, one chain, allow-listed contracts and functions, a gas/value cap, and an expiry.

1. **Read-only work, unrestricted:** discovery, enrichment, scoring, monitoring, digests, and eligibility checks using only the **public address** against official Merkle proofs or claim contracts.
2. **Claiming an airdrop your airdrop identity wallet is already eligible for** (signer-held; never the hot trading wallet). All of these must hold:
   - the claim contract is verified and cross-referenced from at least 2 official sources;
   - the function is on the mandate allow-list (e.g. Merkle `claim(...)`);
   - no approvals, no Permit/Permit2/EIP-712 signatures, `msg.value = 0`;
   - simulation (local **Anvil** mainnet fork / `eth_call` / Solana `simulateTransaction`) shows only "+tokens to me, −gas";
   - the signer's per-transaction and rolling 24 h caps and the daily gas budget are respected (defaults A$250 per transaction, A$1,000 per 24 h, airdrop gas A$20/day; configurable, [16 §2.7](16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13));
   - the on-chain cost gate (`mt_onchain.costgate`) passes: expected benefit ≥ 2× all-in cost by default ([13 §7](13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16));
   - no hard-fail flags.
3. **Defensive actions:** revoke flagged approvals on signer-held wallets (identity, burner, hot); sweep claimed tokens to the **allow-listed** vault address.
4. **Discord bot in your own server:** ingest and classify followed announcements (airdrop, snapshot, claim live, phishing warning).

## Never automated

- **Wallets and keys:**
  - anything on your main or cold wallet (vault and warm are watch-only; the system never holds their keys, [13 §1](13-wallets-treasury-and-onchain.md#1-custody-tiers));
  - any key the LLM can see.
- **Signatures and approvals:**
  - Permit/Permit2/EIP-712/`personal_sign` of arbitrary payloads;
  - SIWE on unknown domains;
  - approvals or `setApprovalForAll`.
- **Trading and connections:**
  - buying, swapping or bridging into new launches (**ICO/IDO participation is always a user task**);
  - connecting a wallet to any site or "eligibility checker".
- **Gaming eligibility:**
  - multiple wallets per campaign or any other sybil pattern;
  - **any social action**;
  - captcha solving;
  - Discord self-bots.
- **Identity:** KYC or launchpad registrations.
- **Drainer patterns:**
  - "claim fee" payments to an EOA;
  - any simulation that shows an outflow other than gas.

## User task queue & digests

**Task types** (the canonical list is in [03 M19](03-build-spec.md#m19-user-task-queue--community-curation--mt_curation); D13 and the roadmap use the same names):
- **Social and community:** `JOIN_DISCORD`, `FOLLOW_ANNOUNCEMENTS`, `JOIN_TELEGRAM`, `FOLLOW_X`, `QUEST` (Galxe/Zealy/Layer3).
- **On-chain:**
  - `ONCHAIN_ACTION_MANUAL` (e.g. use or bridge a protocol, or a manual sale, with a step list, estimated gas and capital);
  - `CLAIM_MANUAL` (needs a signature, or the risk is borderline);
  - `GENUINE_USE` (modest real use from the identity wallet after a clean burner run).
- **Review and housekeeping:** `ICO_REVIEW`, `REVOKE_APPROVAL`, `TAX_QUESTION` (formerly `TAX_RECORD`), `PRO_ADVICE`, `VENUE_CHECK`, `APPROVE_ORDER`.

**Each task carries:**
- numbered steps;
- **official links only**, each tagged with how it was verified and re-checked against blocklists when the task is shown;
- deadline and estimated minutes;
- risk and viability scores with the top 3 reasons;
- standing warnings ("never connect your main wallet; never sign Permit").

**Cadence (Australian time):**
- **Instant** Telegram alert: an eligible claim is live, a deadline is under 48 hours away, or there's a phishing warning about a tracked project.
- **Daily digest** (morning): new high-viability items, tasks due, auto-claims executed.
- **Weekly digest:**
  - **the Discord curation queue**;
  - pipeline review;
  - tasks about to expire;
  - approvals audit;
  - airdrop income summary for tax.

**Telegram buttons:** `✅ Done` · `⏭ Skip` · `💤 Snooze 1d/1w` · `🔍 Details` · `🚫 Never (project)`. Skips and "nevers" feed back into the viability weights, and tasks expire automatically after their deadline.

## Discord curation queue

- **The constraint:** bots can't join servers or follow channels in servers they aren't members of, and user-account automation (self-bots) breaks Discord's terms.
- **The design:** the system *curates* and you *click*.
- **Discovery of invites:** from **official sources only**: CoinGecko `links.chat_url`, project website footers and docs, the official X bio, governance forums.
- **Verification:** each invite is cross-checked against the project's verified domain and the blocklists. Fake Discord invites are a common phishing vector.
- **Queue entries:**
  - a ranked list (default ≤ 3 new servers per week, configurable ([16 §2.13](16-configuration-and-safety-model.md#213-curation)), to avoid overload);
  - the **specific announcement channel to follow**;
  - the destination channel in your private server (`#mt-inbox` or per-category channels);
  - a "leave when" condition (e.g. 30 days after the claim).
- **When you tap "Done":** the bot confirms that posts from the followed channel are arriving. If nothing arrives within 7 days (default, configurable, [16 §2.13](16-configuration-and-safety-model.md#213-curation)), it re-prompts you.
- **Same queue for other platforms:** Telegram channels to join, X accounts to follow (manual), and Galxe spaces all use this queue and digest.

## Additions from the CryptoTrader review (see [11](11-cryptotrader-crossover-review.md), [13](13-wallets-treasury-and-onchain.md))

### Expected value gate (airdrops, ICOs/IDOs, points programmes)

```
EV = P(launch) × E[allocation] × E[price at unlock] × (1 − haircut)
     − gas − fees − capital_lockup_cost − (your_minutes × time_value)
```

- `P(launch)` from funding, team, testnet/points status and corroboration; `haircut` covers vesting, sell pressure and delisting risk.
- `capital_lockup_cost` = capital × days locked × your hurdle rate (default **5% p.a.** on capital locked, an AUD cash-rate proxy; configurable, [16 §2.7](16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)).
- **Only EV > 0 after the risk score reaches the digest as a task**; the EV and its inputs are shown so you can override.

### Wallet discipline
- **Burner first:** any new or untrusted dApp interaction runs from a fresh **burner** wallet funded with the minimum (float default ≤ A$50, refilled to the float only). Only after the burner run is clean does the task move to the identity wallet.
- **One airdrop identity wallet per chain** for genuine participation and autonomous claims (no wallet farms, no sybil patterns). Signer-held and capped (float default ≤ A$300 per chain, [16 §2.7](16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)); never the hot trading wallet. Registered in `ops.wallets` ([13 §3](13-wallets-treasury-and-onchain.md#3-unified-wallet-view)).
- **Genuine-use tasks:** after a clean burner run, the queue may propose real, modest usage of the protocol from the identity wallet, under a signed mandate with caps. Every step is still your click unless it's a plain claim (see *What may run autonomously*).
- **Disposal rule** (configurable, default: **sell 50% on claim**, hold the rest under the M22 rules) so airdrop income doesn't silently become an unmanaged position.
  - **Before Phase 7:** the sale is a USER task (`ONCHAIN_ACTION_MANUAL`, manual sale, with the cost-gate numbers); nothing is sold automatically.
  - **From Phase 7:** once live execution passes the P7 gates, the sale is an order through the risk manager (M11), via an allowed venue or the DEX path.

### Records
- **Campaign record:** one row per campaign: wallet used, tasks done ("activity done to earn it", which matters for the tax classification in 09), dates, costs, outcome.
- **Project dossier:** domain, contracts, team/funding, corroboration, risk reports, Discord/X/docs links, incidents, our notes. Shown on D12.
- **Blacklist:** projects, deployers, domains and funding wallets confirmed as scams; any later project linked to them is a hard fail.

### Fresh launches & memecoins
- **Default-reject fresh launches** (< 24 h, unverified, or no locked liquidity). Only the momentum/memecoin template in 14 §3 may touch them, inside its own sleeve and caps.
- **Wallet-cluster detection** (MemeTrans-style): funding-graph clustering of early buyers; a large share of supply held by wallets with a common funder → hard fail.
- **What flags a single wallet:** funded minutes before launch from a mixer or a fresh exchange withdrawal; buys in the deploy block; links to blacklisted deployers; sells into every pump.
- **Datasets for calibration** (private use only): **SolRPDS** (CC BY), the **Pump.fun corpus** (CC BY), **MemeTrans** (CC BY-NC-SA, so models trained on it are flagged `commercial_ok = false`).

## Data model (Postgres)

Everything below lives in the `curation` schema ([02 §4](02-v1-architecture.md#4-logical-components)) unless noted; wallets are in the one registry, `ops.wallets` ([13 §3](13-wallets-treasury-and-onchain.md#3-unified-wallet-view)).

- **Opportunity and scoring:**
  - `curation.airdrop_opportunity`
  - `curation.token_risk_report`
  - `curation.opportunity_score`
  - `curation.decision`
- **Your tasks and curation** (M19):
  - `curation.task` (all task types; replaces `user_task`, [02 §4](02-v1-architecture.md#4-logical-components))
  - `curation.community` (Discord, Telegram, X and Galxe curation entries; replaces `discord_curation` / `community_curation`)
- **Execution:**
  - `curation.mandate`
  - `curation.exec_log`
- **Safety and journal:**
  - `curation.blocklist_domain` / `curation.blocklist_address` / `curation.blacklist_project`
  - `curation.campaign_record`, `curation.project_dossier`, `curation.wallet_cluster`
  - Airdrop income is a `journal.event` row (airdrop established / initial allocation) linked to the campaign record; there is no separate airdrop income table ([09](09-journal-and-tax.md))
