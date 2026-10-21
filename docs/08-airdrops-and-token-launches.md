# Airdrops, Token Launches & Community Curation (Module M4)

_Raw evidence: [research/airdrops-rugpull-discord.md](research/airdrops-rugpull-discord.md). Security rules: [07-security-notes.md §4](07-security-notes.md#4-crypto-wallets-airdrops-on-chain-claims). (U) = unverified._

## Principles

1. **Vet first, act second.** Only *viable* opportunities that pass rug-pull/scam screening reach the user or the executor.
2. **Act autonomously only where it's safe and permitted.** In practice that means claiming an airdrop your existing wallet already qualifies for, through a dedicated hot wallet, under a mandate you signed. Everything else becomes **step-by-step instructions** in your task queue.
3. **No fake engagement, no sybil farming, no self-bots.** Social tasks (follow, retweet, join Discord, Galxe/Zealy/Layer3 quests) are always queued for you to do yourself.
4. **Everything is journalled** (tax class, AUD value at receipt, transaction hashes, decision trail).

## Pipeline

```
DISCOVER → NORMALISE/DEDUP → ENRICH → RISK-SCORE → VIABILITY-SCORE → DECIDE → AUTO-CLAIM | USER TASK | WATCH | REJECT → TRACK → JOURNAL
```

| Stage | Free sources / tools |
|---|---|
| Discover | DefiLlama `/protocols` (tokenless protocols with rising TVL); CryptoRank Sandbox (ICO/IDO calendars, launchpads, funding rounds); CoinGecko Demo (new listings, categories); DexScreener (new pairs, profiles); Galxe GraphQL (read-only); Snapshot GraphQL and governance-forum JSON; the **Discord inbox** (followed announcement channels); Telegram channels (**postures only**: addresses, mention counts, channel spread; text never reaches a model, see [12 §4](12-policy-and-compliance.md#4-per-platform-data--automation-rules)); news/RSS; manual `/add <url>` via Telegram |
| Normalise | Key = (chain, contract), else the project slug. **Official domain** resolved from CoinGecko/DefiLlama, cross-checked with WHOIS age and blocklists. **Corroboration score:** how many independent listing sites/sources (DefiLlama, CryptoRank, CoinGecko, official X/Discord/docs) agree on the domain, contract and dates; < 2 independent sources → watch only |
| Enrich | **Blockscout** / own RPC (verified source, proxy/implementation, creator; Etherscan for manual lookups only, its terms bar decision use); Helius (Solana RPC, `getAsset`, mint/freeze authority, holders); DexScreener/GeckoTerminal (liquidity, pair age, volume); CryptoRank (funding) |
| Risk-score | **GoPlus** (EVM, primary) · **Honeypot.is** (EVM sell simulation) · **RugCheck.xyz** (Solana, primary) · re-implemented **solana-rugchecker** heuristics · **CRPWarner** concepts (hidden mint / sell limits / leaking token), plus an optional sandboxed Gigahorse deep-scan worker · optional Slither on verified source · blocklists (MetaMask eth-phishing-detect, ScamSniffer, polkadot-js, Chainabuse) |
| Calibrate | Private evaluation against the **SoK rug-pull dataset** (2,391 labelled ETH/BSC contracts) + CRPWarner ground truth + our own outcomes. The model is advisory; the rule-based baseline is authoritative |
| Act / queue | Policy engine → signer container (hot wallet), or the user-task queue |
| Track | Snapshot dates, claim windows, deadlines, `isClaimed`, vesting unlocks, post-claim liquidity/price, wallet approvals |
| Journal | `airdrop_income_journal` → tax engine. ATO: *general* airdrops are ordinary income at receipt value; *initial allocations* have a $0 cost base, with CGT on disposal (U, confirm with a tax agent) |

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
2. **Claiming an airdrop your hot wallet is already eligible for.** All of these must hold:
   - the claim contract is verified and cross-referenced from at least 2 official sources;
   - the function is on the mandate allow-list (e.g. Merkle `claim(...)`);
   - no approvals, no Permit/Permit2/EIP-712 signatures, `msg.value = 0`;
   - simulation (local **Anvil** mainnet fork / `eth_call` / Solana `simulateTransaction`) shows only "+tokens to me, −gas";
   - gas and daily caps are respected;
   - no hard-fail flags.
3. **Defensive actions:** revoke flagged approvals on the hot wallet; sweep claimed tokens to an **allow-listed** cold address.
4. **Discord bot in your own server:** ingest and classify followed announcements (airdrop, snapshot, claim live, phishing warning).

## Never automated

- **Wallets and keys:**
  - anything on your main or cold wallet;
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

**Task types:**
- **Social and community:** `JOIN_DISCORD`, `FOLLOW_X`, `QUEST` (Galxe/Zealy/Layer3).
- **On-chain:**
  - `ONCHAIN_ACTION_MANUAL` (e.g. use or bridge a protocol, with a step list, estimated gas and capital);
  - `CLAIM_MANUAL` (needs a signature, or the risk is borderline).
- **Review and housekeeping:** `ICO_REVIEW`, `REVOKE_APPROVAL`, `TAX_RECORD`.

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
  - a ranked list (a few new servers a week, to avoid overload);
  - the **specific announcement channel to follow**;
  - the destination channel in your private server (`#mt-inbox` or per-category channels);
  - a "leave when" condition (e.g. 30 days after the claim).
- **When you tap "Done":** the bot confirms that posts from the followed channel are arriving. If nothing arrives within N days, it re-prompts you.
- **Same queue for other platforms:** Telegram channels to join, X accounts to follow (manual), and Galxe spaces all use this queue and digest.

## Additions from the CryptoTrader review (see [11](11-cryptotrader-crossover-review.md), [13](13-wallets-treasury-and-onchain.md))

### Expected value gate (airdrops, ICOs/IDOs, points programmes)

```
EV = P(launch) × E[allocation] × E[price at unlock] × (1 − haircut)
     − gas − fees − capital_lockup_cost − (your_minutes × time_value)
```

- `P(launch)` from funding, team, testnet/points status and corroboration; `haircut` covers vesting, sell pressure and delisting risk.
- `capital_lockup_cost` = capital × days locked × your hurdle rate (default: the treasury yield in 13 §5).
- **Only EV > 0 after the risk score reaches the digest as a task**; the EV and its inputs are shown so you can override.

### Wallet discipline
- **Burner first:** any new or untrusted dApp interaction runs from a fresh **burner** wallet funded with the minimum. Only after the burner run is clean does the task move to the identity wallet.
- **One identity wallet per chain** for genuine participation (no wallet farms, no sybil patterns).
- **Genuine-use tasks:** after a clean burner run, the queue may propose real, modest usage of the protocol from the identity wallet, under a signed mandate with caps. Every step is still your click unless it's a plain claim (see *What may run autonomously*).
- **Disposal rule** (configurable, default: **sell 50% on claim**, hold the rest under the M22 rules) so airdrop income doesn't silently become an unmanaged position. The sale is an order through the risk manager.

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

- **Opportunity and scoring:**
  - `airdrop_opportunity`
  - `token_risk_report`
  - `opportunity_score`
  - `decision`
- **Your tasks and curation:**
  - `user_task`
  - `discord_curation`
  - `community_curation` (Telegram, X, Galxe)
- **Execution:**
  - `mandate`
  - `exec_log`
- **Safety and journal:**
  - `blocklist_domain` / `blocklist_address` / `blacklist_project`
  - `campaign_record`, `project_dossier`, `wallet_cluster`
  - `airdrop_income_journal`
