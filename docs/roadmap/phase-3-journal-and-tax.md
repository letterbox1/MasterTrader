# Phase 3 · Journal & Tax

| | |
|---|---|
| **Goal** | Every economic event is journalled automatically, append-only, in native + USD + AUD, and the system produces Australian FY-to-date tax figures and the PAYG-instalment estimate, with pluggable jurisdictions. |
| **Duration** | Weeks 12–15 (can overlap P4 if time allows) |
| **Depends on** | P1 (RBA F11 FX, ABS CPI), P2 (paper fills and venue ledgers) |
| **Unlocks** | P5 (airdrop/staking income), P7 (live trading needs tax records and the tax agent's answer) |
| **Modules** | M18 journal & tax |
| **Containers** | `journal` |
| **Dashboards** | [D14](../ui/dashboards/D14-journal.md) Journal, [D15](../ui/dashboards/D15-tax.md) Tax & Reports |
| **Primary docs** | [09](../09-journal-and-tax.md) · [03 M18](../03-build-spec.md#m18-trading-journal--tax--mt_journal) · [02 F9](../02-v1-architecture.md#8-end-to-end-flows) · [12 §6](../12-policy-and-compliance.md#6-professional-advice-triggers-tracked-as-tasks-in-d13--d15) |

## 1. Scope

**In:** ingestion from fills, exchange ledgers, broker statements and on-chain events; FX service; lot engine; AU_2026 rules + PAYG estimator + wash-sale flags + myTax worksheet; AU_2027_REFORM behind a flag + the 30 June 2027 snapshot job; residency timeline and plugin stubs; wallet/account registry tags; exports; reconciliation; D14 and D15.

**Out:** on-chain wallet decoding at scale (P5 wallet-indexer), airdrop income classification evidence (P5 campaign records).

## 2. Entry criteria

- P2 paper fills flowing; RBA F11 and ABS CPI series loaded (P1).

## 3. Requirements

| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R3.01 | Journal ingestion: Nautilus fills, ccxt ledgers (funding, fees, transfers), broker statements (IBKR Flex, OANDA, IG; CommSec optional), on-chain events | [09 architecture](../09-journal-and-tax.md#architecture), [02 F9](../02-v1-architecture.md#8-end-to-end-flows) | Ingest tests |
| R3.02 | Append-only journal; corrections supersede, never edit; ≥ 7-year retention | [09 quality](../09-journal-and-tax.md#quality), [SPEC NN7](../../SPEC.md#non-negotiable-requirements) | Audit tests |
| R3.03 | Every event stored in **native, USD and AUD** with rate source + timestamp (RBA F11 for AUD; a day with no publication uses the last published business day; currencies not in F11 go via USD) | [09 goals](../09-journal-and-tax.md#goals) | Unit tests |
| R3.04 | **Account/wallet registry `ops.wallets`** (accounts and on-chain addresses; created here, extended by the P5 wallet-indexer): internal transfers tagged and never disposals; `investment` vs `trading` tags | [09 goals](../09-journal-and-tax.md#goals), [13 §3](../13-wallets-treasury-and-onchain.md#3-unified-wallet-view), [17 §B](../17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) | Unit tests |
| R3.05 | Lot engine: specific-ID → FIFO fallback; FX-cash lots (Div 775); Decimal everywhere | [03 M18](../03-build-spec.md#m18-trading-journal--tax--mt_journal) | Property tests |
| R3.06 | **AU_2026** plugin: 50% discount, revenue-account CFD/FX/futures, perpetual swaps on revenue account by default (U, tax agent), Div 775, crypto income, wash-sale flags (re-acquisition within 30 days either side of a loss disposal, flag only; default, configurable, [16 §4.4](../16-configuration-and-safety-model.md#44-tax-flags)), myTax mapping, **PAYG-instalment estimator** (instalment-amount and instalment-rate methods both computed; your ATO notice decides (U, tax agent)); GST/BAS mode dormant | [09 plugin interface](../09-journal-and-tax.md#jurisdiction-plugin-interface), [09 key findings](../09-journal-and-tax.md#️-key-findings-that-shape-the-design), [17 §C](../17-decisions-register.md#c-defaults-that-were-n-or-unspecified), [17 §D](../17-decisions-register.md#d-other-decisions) | Golden tests |
| R3.07 | Tax regime is a per-FY, per-activity setting (investor / trader-in-business / revenue); reports **both ways** until your tax agent decides | [09 key findings](../09-journal-and-tax.md#️-key-findings-that-shape-the-design) | Report test |
| R3.08 | **AU_2027_REFORM behind a flag** (status conflicts between sources) + the **30 June 2027 market-value snapshot job** of every open lot, using the per-asset-class price convention in [16 §4.2](../16-configuration-and-safety-model.md#42-market-value-snapshot-30-june-2027-and-any-residency-change) | [09 key findings](../09-journal-and-tax.md#️-key-findings-that-shape-the-design), [11 §3](../11-cryptotrader-crossover-review.md#3-conflicts-and-how-they-were-resolved) | Dry-run snapshot |
| R3.09 | Residency timeline (CGT event I1 modelling) + AE / EG (crypto hard-flag) / CY / GENERIC plugin stubs | [09 plugin interface](../09-journal-and-tax.md#jurisdiction-plugin-interface) | Plugin tests |
| R3.10 | Exports: Beancount/hledger + Fava, accountant CSV/PDF pack, optional Koinly/Syla CSV, CARF reconciliation against venue-provided statements when available (otherwise not applicable) | [03 M18](../03-build-spec.md#m18-trading-journal--tax--mt_journal), [09 goals](../09-journal-and-tax.md#goals) | Export diff |
| R3.11 | Daily reconciliation journal ↔ venues; mismatch = incident | [09 quality](../09-journal-and-tax.md#quality) | Recon report |
| R3.12 | Every report records rule version + FX/price source | [09 quality](../09-journal-and-tax.md#quality) | Report test |
| R3.13 | Trading-journal view per trade: strategy, signal/rationale, chart snapshot and attachments (stored content-addressed under `data/attachments/`, referenced by hash in the WORM note row), notes, tags, review prompts | [D14](../ui/dashboards/D14-journal.md), [03 M18](../03-build-spec.md#m18-trading-journal--tax--mt_journal) | Playwright |
| R3.14 | D15: FY summary, PAYG estimate, lots/matches, residency, reports, regime setting | [D15](../ui/dashboards/D15-tax.md) | Playwright |
| R3.N1 | Tax-sensitive fields encrypted at column level (`pgcrypto`) with envelope encryption (yearly data keys wrapped by a master key; rotation re-wraps keys in a non-WORM key table, never rows) and excluded from LLM prompts | [07 §8](../07-security-notes.md#8-data-protection-backups--audit), [17 §D](../17-decisions-register.md#d-other-decisions) | Prompt audit |
| R3.N2 | Tax golden tests are mandatory for merge | [04 standing rules](../04-plan-of-action.md#standing-rules) | CI |
| R3.15 | **Valuation hierarchy** for non-trade events: fill price → VWAP of our recorded trades (AUD venue, else USD × RBA) → on-chain pool price → aggregators as cross-check only; stored values are ours with method + source | [16 §4.1](../16-configuration-and-safety-model.md#41-valuing-crypto-for-the-journal) | Golden tests |
| R3.16 | **Commands and residency contract:** `tax.fy.lock` / `tax.fy.unlock` (C3), `task.answer` (C1), `journal.manual_event.add` (C2); a residency change emits `tax.residency.changed`, the venue registry recomputes, and any loosening that results is C3 | [02 §7.2](../02-v1-architecture.md#72-commands-rest-write), [17 §D](../17-decisions-register.md#d-other-decisions) | Command tests |
| R3.17 | Minimal **Accounts page** (D16 settings) to register accounts/addresses in `ops.wallets` and tag them `investment` / `trading` | [D16](../ui/dashboards/D16-system.md), [17 §D](../17-decisions-register.md#d-other-decisions) | Playwright |
| R3.18 | Minimal `curation.task` table so `TAX_QUESTION` tasks are stored from P3; P5 (M19) extends it additively | [03 M19](../03-build-spec.md#m19-user-task-queue--community-curation--mt_curation), [17 §D](../17-decisions-register.md#d-other-decisions) | Migration test |
| R3.N3 | Write path survives a Postgres outage: journal/WORM writes buffer in NATS JetStream, bounded at 1 GB or 24 h (defaults, configurable); above 80% of the buffer new entries stop, exits continue; nothing executes without a record | [16 §3.3](../16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check), [17 §C](../17-decisions-register.md#c-defaults-that-were-n-or-unspecified) | Postgres-down drill |

## 4. ToDo sets

### A. Your actions (`USER`)
- [ ] **T3.01** `USER` **Engage a tax agent.** Send the question list (09); the key one is **investor vs trader-in-business, answered before any live trade**; include the PAYG method, wash-sale window and perps treatment. → R3.07 · [09 questions](../09-journal-and-tax.md#questions-for-your-tax-agent-tracked-as-tasks)
- [ ] **T3.02** `USER` Ask the agent to confirm the **2027 CGT reform status** and the 30 June 2027 transitional mechanism. → R3.08
- [ ] **T3.03** `USER` Export historical statements you already have (IBKR Flex, OANDA, IG, exchanges) for opening balances/lots. → R3.01, R3.05
- [ ] **T3.04** `USER` Register your accounts on the Accounts page and tag each `investment` or `trading`. → R3.04, R3.17
- [ ] **T3.05** `USER` Enter the residency timeline (AU from …; any planned moves). → R3.09
- [ ] **T3.06** `USER` Diary hard date: **30 June 2027** snapshot must run (end of day AEST). → R3.08

### B. Build (`BUILD`, code)
- [ ] **T3.20** `BUILD` `mt_journal` event model + ingestion adapters (fills, ccxt ledgers, IBKR Flex, OANDA, IG, on-chain stub). → R3.01, R3.02
- [ ] **T3.21** `BUILD` FX service (RBA F11 for AUD with the last-business-day and via-USD rules; crypto values from the valuation service, R3.15; USD), three-currency storage; CoinGecko values are never persisted. → R3.03
- [ ] **T3.22** `BUILD` `ops.wallets` account/wallet registry with internal-transfer matching and tags. → R3.04
- [ ] **T3.23** `BUILD` Lot engine (rp2/ledger ideas): specific-ID, FIFO, FX-cash lots. → R3.05
- [ ] **T3.24** `BUILD` AU_2026 plugin, PAYG estimator (both methods), wash-sale flags (30-day default), myTax worksheet; regime switch with dual reporting. → R3.06, R3.07
- [ ] **T3.25** `BUILD` AU_2027_REFORM scaffold behind a flag; snapshot job (Prefect, idempotent, price source recorded). → R3.08
- [ ] **T3.26** `BUILD` Residency timeline + AE/EG/CY/GENERIC stubs; Egypt crypto hard flag wired to M11. → R3.09
- [ ] **T3.27** `BUILD` Exports: Beancount + Fava, accountant pack, Koinly/Syla CSV. → R3.10
- [ ] **T3.28** `BUILD` Reconciliation job journal ↔ venues. → R3.11
- [ ] **T3.29** `BUILD` UI: D14 Journal (incl. content-addressed attachments), D15 Tax & Reports. → R3.13, R3.14
- [ ] **T3.30** `BUILD` Tax-agent questions created as `TAX_QUESTION` tasks in the minimal `curation.task` table (queue lands fully in P5; store now). → R3.18 · T3.01
- [ ] **T3.31** `BUILD` Valuation service implementing the hierarchy; snapshot price convention per asset class. → R3.15, R3.08
- [ ] **T3.32** `BUILD` Commands `tax.fy.lock`/`unlock` (C3), `task.answer` (C1), `journal.manual_event.add` (C2); `tax.residency.changed` event → venue-registry recompute, with any resulting loosening routed to C3. → R3.16
- [ ] **T3.33** `BUILD` Minimal Accounts page in D16 settings: register, tag and list `ops.wallets` entries. → R3.17

### C. Ops & config (`OPS`)
- [ ] **T3.40** `OPS` `journal` container; Fava sidecar on the internal network. → R3.10
- [ ] **T3.41** `OPS` Envelope encryption: master key in the secrets store, yearly data keys in a non-WORM key table; insert-only role for `journal.*`. → R3.N1, R3.02
- [ ] **T3.42** `OPS` JetStream limits for the journal/WORM write path (1 GB / 24 h defaults; new entries stop at 80%) with an alert. → R3.N3

### D. Verify & test (`VERIFY`)
- [ ] **T3.60** `VERIFY` Golden-file tests from ATO worked examples (e.g. bought 2 Feb 2018 → discount from 3 Feb 2019). → R3.06, R3.N2
- [ ] **T3.61** `VERIFY` Property tests: lots conserved; matched qty = disposed qty; journal balances = venue balances. → R3.05, R3.11
- [ ] **T3.62** `VERIFY` Snapshot dry run on a test date. → R3.08
- [ ] **T3.63** `VERIFY` Beancount export balances; Fava opens it. → R3.10
- [ ] **T3.64** `VERIFY` Prompt audit: no TFN/address fields reachable by the gateway. → R3.N1
- [ ] **T3.65** `VERIFY` Command tests: a locked FY rejects new events until a C3 unlock; a residency change that would loosen the venue registry waits for C3. → R3.16
- [ ] **T3.66** `VERIFY` Key rotation re-wraps data keys only: no WORM row changes and the hash chain still verifies. → R3.N1
- [ ] **T3.67** `VERIFY` Postgres-down drill: writes buffer in JetStream; at 80% new entries stop while exits continue; on recovery every buffered record lands. → R3.N3

### E. Run / soak (`RUN`)
- [ ] **T3.80** `RUN` One month of paper trades fully journalled and reconciled daily with zero unexplained breaks.

## 5. Deliverables

Journal + lot engine · AU_2026 + PAYG + dual-regime reports · 2027 scaffold + snapshot job · residency + plugin stubs · exports · D14 + D15.

## 6. Exit criteria (demo)

1. Every paper trade, fee and funding payment appears automatically in the journal in native/USD/AUD.
2. D15 shows FY-to-date AU figures both ways (investor vs trader) and a PAYG estimate, each with rule version + FX source.
3. The tax-agent questions are logged and the agent is engaged.

## 7. Risks & open questions

| Risk | Mitigation |
|---|---|
| 2027 reform status unresolved | Flagged; reports both regimes; snapshot runs regardless (costs nothing) |
| Investor vs trader classification | Decide with the agent **before P7**; the engine reports both ways meanwhile |
| Broker statement formats change | Golden files per format; reconciliation catches drift |
