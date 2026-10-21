# Phase 5 · Airdrops, Launches, Wallets & Curation

| | |
|---|---|
| **Goal** | Vetted airdrops/launches arrive as a weekly digest with step-by-step tasks; safe eligible claims execute automatically from capped wallets under signed mandates with simulation proof; scams are rejected with reasons; every wallet you own is visible in one place. |
| **Duration** | Weeks 20–23 |
| **Depends on** | P3 (journal, wallet registry), P4 (Discord/Telegram discovery, text pipeline) |
| **Unlocks** | P6 (hold-and-earn uses the signer, cost gate and wallet view), P7 (DEX execution path) |
| **Modules** | M4 airdrops/launches, M19 task queue & curation, M22 (custody tiers, signer, unified wallet view, monitors), M18 airdrop/staking income |
| **Containers** | `airdrop`, `airdrop-exec` + `signer`, `anvil`, `wallet-indexer`, `curation` |
| **Dashboards** | [D12](../ui/dashboards/D12-airdrops.md) Airdrops & Launches, [D13](../ui/dashboards/D13-tasks-curation.md) Tasks & Curation, [D18](../ui/dashboards/D18-wallets-treasury.md) Wallets & Treasury (view) |
| **Primary docs** | [08](../08-airdrops-and-token-launches.md) · [13 §1](../13-wallets-treasury-and-onchain.md#1-custody-tiers) · [13 §2](../13-wallets-treasury-and-onchain.md#2-signer-service-the-only-process-that-sees-hot-keys) · [13 §3](../13-wallets-treasury-and-onchain.md#3-unified-wallet-view) · [13 §6](../13-wallets-treasury-and-onchain.md#6-monitors-feed-m16-and-m11) · [13 §7](../13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16) · [03 M4](../03-build-spec.md#m4-airdrops-token-launches--icos--mt_airdrop) · [03 M19](../03-build-spec.md#m19-user-task-queue--community-curation--mt_curation) · [07 §4](../07-security-notes.md#4-crypto-wallets-airdrops-on-chain-claims) · [02 F8/F10](../02-v1-architecture.md#8-end-to-end-flows) |

## 1. Scope

**In:** custody tiers; the intents-only signer with hard blocks, durable-nonce block, simulation and the on-chain cost gate; wallet-indexer and unified wallet view; approval/nonce/depeg/venue monitors; the full M4 pipeline (discover, normalise + corroboration, enrich, risk, viability + EV, decide, mandates, claims, track, journal) with burner-first, identity wallets, disposal rule, campaign records, dossiers, blacklist and wallet-cluster detection; the M19 queue, digests and community curation; D12, D13, D18 (view).

**Out:** hold-and-earn moves and treasury allocation (P6), social drafts (P6, optional), live DEX trading strategies (P7).

## 2. Entry criteria

- P3 journal live; P4 Discord inbox and Telegram postures flowing.
- Wallets created by you (T5.01–T5.03).

## 3. Requirements

### Wallets, signer, monitors (M22 part 1)
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R5.01 | Six custody tiers (vault, Hyperliquid master if approved, warm, hot, airdrop identity per chain, burner) with limits; vault/warm watch-only in the system | [13 §1](../13-wallets-treasury-and-onchain.md#1-custody-tiers) | Config review |
| R5.02 | **Signer accepts intents only** (local socket/mTLS from the policy service), re-builds transactions, per-wallet allow-lists, per-tx and rolling-24h caps, mandatory simulation (Anvil / `simulateTransaction`) | [13 §2](../13-wallets-treasury-and-onchain.md#2-signer-service-the-only-process-that-sees-hot-keys), [SPEC NN6](../../SPEC.md#non-negotiable-requirements) | Signer tests |
| R5.03 | **Hard blocks:** permit/Permit2, `setApprovalForAll`, unlimited approvals, foreign `SetAuthority`/SPL `Approve`, unknown programs/routers; approvals sized and revoked; **durable-nonce block** + nonce-authority alerts | [13 §2](../13-wallets-treasury-and-onchain.md#2-signer-service-the-only-process-that-sees-hot-keys), [07 §4](../07-security-notes.md#4-crypto-wallets-airdrops-on-chain-claims) | Drainer tests |
| R5.04 | **On-chain cost gate** (Solana/EVM cost formulas, AMM impact, all-in round trip; gas windows; daily gas budgets) → allow/wait/reject, logged | [13 §7](../13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16) | Gate tests |
| R5.05 | **Unified wallet view:** `ops.wallets` registry (role, provider, tax tag), read-only aggregation (Helius DAS, Blockscout/RPC, Hyperliquid `/info`, ccxt read-only), daily journal reconciliation, monthly rotki | [13 §3](../13-wallets-treasury-and-onchain.md#3-unified-wallet-view) | Recon report |
| R5.06 | Monitors: approvals, nonce authority, **stablecoin depeg > 50 bps**, exploit/oracle/TVL drop, venue health, bridge policy, concentration | [13 §6](../13-wallets-treasury-and-onchain.md#6-monitors-feed-m16-and-m11) | Simulated events |
| R5.07 | Scheduled sweeps of hot/burner balances above float to the vault address; kill switch sweeps hot balances | [13 §1](../13-wallets-treasury-and-onchain.md#1-custody-tiers), [14 §5 ladder](../14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) | Sweep test |

### Airdrops & launches (M4)
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R5.10 | Discovery: DefiLlama tokenless protocols, CryptoRank, CoinGecko, DexScreener, Galxe (read-only), Snapshot/forums, Discord inbox, Telegram postures, news, `/add <url>` | [08 pipeline](../08-airdrops-and-token-launches.md#pipeline) | Discovery tests |
| R5.11 | Normalise by (chain, contract)/slug; official domain verified; **corroboration score** (< 2 independent sources → watch only) | [08 pipeline](../08-airdrops-and-token-launches.md#pipeline) | Unit tests |
| R5.12 | Enrichment via **Blockscout/own RPC** (Etherscan manual only), Helius, DexScreener/GeckoTerminal, CryptoRank | [08 pipeline](../08-airdrops-and-token-launches.md#pipeline), [12 §4](../12-policy-and-compliance.md#4-per-platform-data--automation-rules) | Source audit |
| R5.13 | Risk score: GoPlus, Honeypot.is, RugCheck, solana-rugchecker + CRPWarner heuristics, blocklists, **wallet-cluster detection**, **blacklist**; hard-fail = reject; calibrated on SoK (+ SolRPDS / Pump.fun corpus / MemeTrans, private) | [08 risk score](../08-airdrops-and-token-launches.md#risk-score-0100-any-hard-fail--100--reject), [03 M4](../03-build-spec.md#m4-airdrops-token-launches--icos--mt_airdrop) | Calibration report |
| R5.14 | Viability score incl. **AU geo/KYC exclusion** + **EV gate** (EV > 0 to reach the digest) | [08 viability](../08-airdrops-and-token-launches.md#viability-score), [08 EV gate](../08-airdrops-and-token-launches.md#expected-value-gate-airdrops-icosidos-points-programmes) | Unit tests |
| R5.15 | Autonomy limited to: read-only work; eligible claims from the identity wallet under a signed, expiring mandate with simulation + cost gate; genuine-use tasks after a clean burner run; defensive revokes/sweeps | [08 autonomous](../08-airdrops-and-token-launches.md#what-may-run-autonomously), [03 M4](../03-build-spec.md#m4-airdrops-token-launches--icos--mt_airdrop) | Policy tests |
| R5.16 | **Never automated** list enforced server-side (permits, SIWE on unknown domains, approvals, buying/bridging into launches, connecting wallets, sybil, social actions, captchas, KYC) | [08 never automated](../08-airdrops-and-token-launches.md#never-automated) | Policy tests |
| R5.17 | Burner-first; one identity wallet per chain; **disposal rule** (default sell 50% on claim, via M11); fresh launches default-rejected | [08 wallet discipline](../08-airdrops-and-token-launches.md#wallet-discipline) | Flow tests |
| R5.18 | Records: campaign record, project dossier, blacklist, wallet clusters; airdrop/staking income journalled with classification evidence | [08 records](../08-airdrops-and-token-launches.md#records), [09 key findings](../09-journal-and-tax.md#️-key-findings-that-shape-the-design) | Journal link test |

### Curation (M19) & UI
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R5.20 | One task queue (social tasks, ICO reviews, manual claims, communities, revokes, tax questions, approve-mode orders, `GENUINE_USE`, `PRO_ADVICE`, `VENUE_CHECK`); Telegram Done/Skip/Snooze/Details/Never; auto-expiry; feedback ranking | [03 M19](../03-build-spec.md#m19-user-task-queue--community-curation--mt_curation), [D13](../ui/dashboards/D13-tasks-curation.md) | Flow tests |
| R5.21 | Community curation: invites from **official sources only**, blocklist-checked, "which announcement channel to Follow", "leave when", **bot verifies delivery** after Done | [08 Discord queue](../08-airdrops-and-token-launches.md#discord-curation-queue) | Delivery test |
| R5.22 | Cadence: instant urgent alerts, daily digest, weekly curation/review digest (AU timezone, quiet hours) | [08 task queue](../08-airdrops-and-token-launches.md#user-task-queue--digests) | Digest preview |
| R5.23 | D12 (radar, detail, wallet & mandates), D13 (inbox, communities, digests, history), D18 view (net worth, allocation, wallet table, transfers, venue health) | [D12](../ui/dashboards/D12-airdrops.md) [D13](../ui/dashboards/D13-tasks-curation.md) [D18](../ui/dashboards/D18-wallets-treasury.md) | Playwright |
| R5.N1 | Signer and Anvil on the isolated network; no LLM can reach keys | [07 §5](../07-security-notes.md#5-network--host), [02 §3.1](../02-v1-architecture.md#31-networks) | Network test |
| R5.N2 | Kill switch ON freezes auto-claims and treasury moves | [02 F6](../02-v1-architecture.md#8-end-to-end-flows) | Drill |
| R5.24 | **Wallet, signer and gas limits are configuration** (floats, per-tx/24 h caps, gas budgets, cost-gate margin, EV hurdle; defaults in 16 §2.7); **signing stays disabled until you confirm them** | [16 §2.7](../16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13) | Config test |

## 4. ToDo sets

### A. Your actions (`USER`)
- [ ] **T5.01** `USER` Set up the **vault** (air-gapped hardware) and **warm** hardware wallet yourself; the system only gets public addresses. → R5.01
- [ ] **T5.02** `USER` **Seed backup:** Shamir (SLIP-39) shares or multisig, stored in separate locations; write the sealed **estate letter** (where shares are, how to unwind, no secrets). → [07 §4](../07-security-notes.md#4-crypto-wallets-airdrops-on-chain-claims)
- [ ] **T5.03** `USER` Approve creation of the hot, identity (one per chain) and burner keys in the signer; fund them with minimal floats. → R5.01, R5.07
- [ ] **T5.04** `USER` Register every address/account you own (proof of control), with role and investment/trading tag. → R5.05
- [ ] **T5.05** `USER` Sign the first **mandates** (C3): wallet, chain, allowed contracts/functions, caps, expiry. → R5.15
- [ ] **T5.06** `USER` Set the disposal rule (default sell 50% on claim) and EV hurdle. → R5.14, R5.17
- [ ] **T5.07** `USER` Work the task queue: join/follow communities, do social tasks yourself, ICO reviews. → R5.20, R5.21
- [ ] **T5.08** `USER` Review and confirm the wallet/signer/gas limits (prefilled defaults) to enable signing. → R5.24

### B. Build (`BUILD`, code)
- [ ] **T5.20** `BUILD` `mt_signer`: intent API, builders/decoders (EVM, Solana), allow-lists, caps, hard blocks, durable-nonce rules, simulation hooks, ledger of signatures. → R5.02, R5.03
- [ ] **T5.21** `BUILD` On-chain cost gate service (fee sampling, Anvil gas, impact formulas, gas windows, budgets). → R5.04
- [ ] **T5.22** `BUILD` `wallet-indexer`: registry, aggregators, transfer classifier (internal tagging into M18), reconciliation, rotki export. → R5.05
- [ ] **T5.23** `BUILD` Monitors: approvals, nonce authority, depeg, exploit/TVL, venue health, bridge policy, concentration → M16/M11. → R5.06
- [ ] **T5.24** `BUILD` Sweep scheduler + kill-switch sweep. → R5.07, R5.N2
- [ ] **T5.25** `BUILD` `mt_airdrop` discovery, normalisation + corroboration, enrichment. → R5.10–R5.12
- [ ] **T5.26** `BUILD` Risk scoring: provider clients, heuristics, blocklists, wallet-cluster graph, blacklist; SoK/SolRPDS/Pump.fun calibration notebook. → R5.13
- [ ] **T5.27** `BUILD` Viability + EV gate; decision engine (reject / task / watch / auto-claim). → R5.14, R5.15
- [ ] **T5.28** `BUILD` Mandates + claim executor + burner-first/identity flow + disposal-rule order via M11. → R5.15–R5.17
- [ ] **T5.29** `BUILD` Campaign records, dossiers, income journal linking. → R5.18
- [ ] **T5.30** `BUILD` `mt_curation`: task types, queue, ranking, expiry, digests, Telegram buttons, Discord delivery verification. → R5.20–R5.22
- [ ] **T5.31** `BUILD` UI: D12, D13, D18 (view). → R5.23

### C. Ops & config (`OPS`)
- [ ] **T5.40** `OPS` `signer` + `anvil` containers on the isolated network; keys in OpenBao or sops files. → R5.N1 · [07 §2](../07-security-notes.md#2-secrets)
- [ ] **T5.41** `OPS` RPC accounts (Helius, Alchemy) and fallbacks; per-provider quotas. → R5.05 · [13 §7](../13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16)
- [ ] **T5.42** `OPS` Blocklist refresh jobs (MetaMask eth-phishing-detect, ScamSniffer, polkadot-js, Chainabuse). → R5.13

### D. Verify & test (`VERIFY`)
- [ ] **T5.60** `VERIFY` **Drainer test suite:** permit, Permit2, `setApprovalForAll`, unlimited approval, unknown router, "claim fee" to an EOA, foreign durable nonce → all refused. → R5.03, R5.16
- [ ] **T5.61** `VERIFY` Testnet claim: simulation shows only "+tokens, −gas", mandate respected, journal entry created. → R5.15, R5.18
- [ ] **T5.62** `VERIFY` SoK evaluation report (precision/recall vs the rule-based baseline). → R5.13
- [ ] **T5.63** `VERIFY` Depeg and exploit simulations trigger auto-reduce / urgent task. → R5.06
- [ ] **T5.64** `VERIFY` Kill switch freezes claims and sweeps hot balances. → R5.N2
- [ ] **T5.65** `VERIFY` Wallet view total reconciles with the journal for a test week. → R5.05

### E. Run / soak (`RUN`)
- [ ] **T5.80** `RUN` Two weekly digests; review rejected-with-reasons for false positives. → R5.22

### F. Docs
- [ ] **T5.90** `BUILD` Runbook: wallet drained (revoke, isolate, sweep). → [07 §9](../07-security-notes.md#9-monitoring--incident-response)

## 5. Deliverables

Signer + cost gate · wallet-indexer + monitors · full M4 pipeline with records · task queue + digests + community curation · D12, D13, D18 (view).

## 6. Exit criteria (demo)

1. A weekly digest of vetted airdrops/launches with EV, steps and verified links.
2. A testnet auto-claim with simulation proof, mandate and journal links; a scam rejected with reasons.
3. The drainer test suite passes; D18 shows every registered wallet reconciled to the journal.

## 7. Risks & open questions

| Risk | Mitigation |
|---|---|
| Adversarial tokens behave differently on execution than in simulation | Simulation is a sanity check only; caps + burner-first + hard blocks |
| Free RPC limits | One account per provider, fallbacks; upgrade only when logs prove losses |
| Airdrop tax classification | Campaign records attach "activity done to earn it"; confirm with the tax agent |
