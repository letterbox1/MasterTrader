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
| R3.01 | Journal ingestion: Nautilus fills, ccxt ledgers (funding, fees, transfers), broker statements (IBKR Flex, OANDA, IG), on-chain events | [09 architecture](../09-journal-and-tax.md#architecture), [02 F9](../02-v1-architecture.md#8-end-to-end-flows) | Ingest tests |
| R3.02 | Append-only journal; corrections supersede, never edit; ≥ 7-year retention | [09 quality](../09-journal-and-tax.md#quality), [SPEC NN7](../../SPEC.md#non-negotiable-requirements) | Audit tests |
| R3.03 | Every event stored in **native, USD and AUD** with rate source + timestamp (RBA for AUD) | [09 goals](../09-journal-and-tax.md#goals) | Unit tests |
| R3.04 | **Account/wallet registry:** internal transfers tagged and never disposals; `investment` vs `trading` tags | [09 goals](../09-journal-and-tax.md#goals), [13 §3](../13-wallets-treasury-and-onchain.md#3-unified-wallet-view) | Unit tests |
| R3.05 | Lot engine: specific-ID → FIFO fallback; FX-cash lots (Div 775); Decimal everywhere | [03 M18](../03-build-spec.md#m18-trading-journal--tax--mt_journal) | Property tests |
| R3.06 | **AU_2026** plugin: 50% discount, revenue-account CFD/FX/futures, Div 775, crypto income, wash-sale flags, myTax mapping, **PAYG-instalment estimator**; GST/BAS mode dormant | [09 plugin interface](../09-journal-and-tax.md#jurisdiction-plugin-interface), [09 key findings](../09-journal-and-tax.md#️-key-findings-that-shape-the-design) | Golden tests |
| R3.07 | Tax regime is a per-FY, per-activity setting (investor / trader-in-business / revenue); reports **both ways** until your tax agent decides | [09 key findings](../09-journal-and-tax.md#️-key-findings-that-shape-the-design) | Report test |
| R3.08 | **AU_2027_REFORM behind a flag** (status conflicts between sources) + the **30 June 2027 market-value snapshot job** of every open lot | [09 key findings](../09-journal-and-tax.md#️-key-findings-that-shape-the-design), [11 §3](../11-cryptotrader-crossover-review.md#3-conflicts-and-how-they-were-resolved) | Dry-run snapshot |
| R3.09 | Residency timeline (CGT event I1 modelling) + AE / EG (crypto hard-flag) / CY / GENERIC plugin stubs | [09 plugin interface](../09-journal-and-tax.md#jurisdiction-plugin-interface) | Plugin tests |
| R3.10 | Exports: Beancount/hledger + Fava, accountant CSV/PDF pack, optional Koinly/Syla CSV, CARF reconciliation | [03 M18](../03-build-spec.md#m18-trading-journal--tax--mt_journal), [09 goals](../09-journal-and-tax.md#goals) | Export diff |
| R3.11 | Daily reconciliation journal ↔ venues; mismatch = incident | [09 quality](../09-journal-and-tax.md#quality) | Recon report |
| R3.12 | Every report records rule version + FX/price source | [09 quality](../09-journal-and-tax.md#quality) | Report test |
| R3.13 | Trading-journal view per trade: strategy, signal/rationale, chart snapshot, notes, tags, review prompts | [D14](../ui/dashboards/D14-journal.md), [03 M18](../03-build-spec.md#m18-trading-journal--tax--mt_journal) | Playwright |
| R3.14 | D15: FY summary, PAYG estimate, lots/matches, residency, reports, regime setting | [D15](../ui/dashboards/D15-tax.md) | Playwright |
| R3.N1 | Tax-sensitive fields encrypted at column level (`pgcrypto`) and excluded from LLM prompts | [07 §8](../07-security-notes.md#8-data-protection-backups--audit) | Prompt audit |
| R3.N2 | Tax golden tests are mandatory for merge | [04 standing rules](../04-plan-of-action.md#standing-rules) | CI |

## 4. ToDo sets

### A. Your actions (`USER`)
- [ ] **T3.01** `USER` **Engage a tax agent.** Send the question list (09); the key one is **investor vs trader-in-business, answered before any live trade**. → R3.07 · [09 questions](../09-journal-and-tax.md#questions-for-your-tax-agent-tracked-as-tasks)
- [ ] **T3.02** `USER` Ask the agent to confirm the **2027 CGT reform status** and the 30 June 2027 transitional mechanism. → R3.08
- [ ] **T3.03** `USER` Export historical statements you already have (IBKR Flex, OANDA, IG, exchanges) for opening balances/lots. → R3.01, R3.05
- [ ] **T3.04** `USER` Register your accounts and tag each `investment` or `trading`. → R3.04
- [ ] **T3.05** `USER` Enter the residency timeline (AU from …; any planned moves). → R3.09
- [ ] **T3.06** `USER` Diary hard date: **30 June 2027** snapshot must run (end of day AEST). → R3.08

### B. Build (`BUILD`, code)
- [ ] **T3.20** `BUILD` `mt_journal` event model + ingestion adapters (fills, ccxt ledgers, IBKR Flex, OANDA, IG, on-chain stub). → R3.01, R3.02
- [ ] **T3.21** `BUILD` FX service (RBA F11 for AUD, reputable crypto rate, USD), three-currency storage. → R3.03
- [ ] **T3.22** `BUILD` Account/wallet registry with internal-transfer matching and tags. → R3.04
- [ ] **T3.23** `BUILD` Lot engine (rp2/ledger ideas): specific-ID, FIFO, FX-cash lots. → R3.05
- [ ] **T3.24** `BUILD` AU_2026 plugin, PAYG estimator, wash-sale flags, myTax worksheet; regime switch with dual reporting. → R3.06, R3.07
- [ ] **T3.25** `BUILD` AU_2027_REFORM scaffold behind a flag; snapshot job (Prefect, idempotent, price source recorded). → R3.08
- [ ] **T3.26** `BUILD` Residency timeline + AE/EG/CY/GENERIC stubs; Egypt crypto hard flag wired to M11. → R3.09
- [ ] **T3.27** `BUILD` Exports: Beancount + Fava, accountant pack, Koinly/Syla CSV. → R3.10
- [ ] **T3.28** `BUILD` Reconciliation job journal ↔ venues. → R3.11
- [ ] **T3.29** `BUILD` UI: D14 Journal, D15 Tax & Reports. → R3.13, R3.14
- [ ] **T3.30** `BUILD` Tax-agent questions created as `TAX_QUESTION` tasks (queue lands fully in P5; store now). → T3.01

### C. Ops & config (`OPS`)
- [ ] **T3.40** `OPS` `journal` container; Fava sidecar on the internal network. → R3.10
- [ ] **T3.41** `OPS` Column encryption keys in the secrets store; insert-only role for `journal.*`. → R3.N1, R3.02

### D. Verify & test (`VERIFY`)
- [ ] **T3.60** `VERIFY` Golden-file tests from ATO worked examples (e.g. bought 2 Feb 2018 → discount from 3 Feb 2019). → R3.06, R3.N2
- [ ] **T3.61** `VERIFY` Property tests: lots conserved; matched qty = disposed qty; journal balances = venue balances. → R3.05, R3.11
- [ ] **T3.62** `VERIFY` Snapshot dry run on a test date. → R3.08
- [ ] **T3.63** `VERIFY` Beancount export balances; Fava opens it. → R3.10
- [ ] **T3.64** `VERIFY` Prompt audit: no TFN/address fields reachable by the gateway. → R3.N1

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
