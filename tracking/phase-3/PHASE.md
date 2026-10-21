---
phase: 3
title: Journal & tax
roadmap: docs/roadmap/phase-3-journal-and-tax.md
status: not_started
opens_after: [2]
force_open: false
started: ""
completed: ""
doc_sync_status: n/a
updated: 2026-10-21
---

# Phase 3 · Journal & tax

## Summary

Every economic event (fills, fees, funding, transfers, statements, on-chain events) is journalled automatically into WORM `journal.*` tables in **native, USD and AUD** with rate provenance (RBA F11 for AUD). A lot engine (specific-ID → FIFO, FX-cash lots for Div 775, Decimal everywhere) feeds a dated jurisdiction-plugin engine: **AU_2026** (CGT discount, revenue CFDs/futures, Div 775, crypto income, wash-sale flags, myTax worksheet, **PAYG-instalment estimator**), reported **both ways** (investor vs trader-in-business) until the tax agent decides; **AU_2027_REFORM** behind a flag plus the **30 June 2027 snapshot job** (hard date); a residency timeline with CGT event I1 and AE / EG (crypto hard flag → M11) / CY / GENERIC stubs. Exports (Beancount + Fava, accountant pack, Koinly/Syla CSV, CARF), a daily journal↔venue reconciliation, D14 Journal and D15 Tax & Reports, and column encryption with prompt exclusion complete the phase. You engage a tax agent now: the investor-vs-trader answer gates P7.

Work is organised into eight workstreams (below): USER actions, storage & security, ingestion, FX & registry, lots & rules, reform/residency, exports & reconciliation, UI/API, and verification/run.

## Entry criteria

- [ ] Phase 2 done (paper fills flowing through M11 on testnet/practice accounts; `audit.fill` populated; paper clock T2.80 running)
- [ ] RBA F11 daily FX and ABS CPI series loaded and readable via `pit(as_of)` (P1 T1.23, T1.24)
- [ ] P0 WORM layer (`worm_owner`, triggers, hash chain, daily seal, `audit.verify`) and `journal` schema exist (P0 T0.22, T0.23)
- [ ] `mt_api` command bus with C0–C3 levels, WebSocket hub and web shell available (P0 T0.24, T0.26)
- [ ] Read-only, IP-locked venue keys in the sops file for ledger reads and reconciliation (P1 T1.02)

## Exit criteria

- [ ] Every paper trade, fee and funding payment appears automatically in the journal in native/USD/AUD (P3-T054 EC1)
- [ ] D15 shows FY-to-date AU figures both ways (investor vs trader) and a PAYG estimate, each with rule version + FX source (P3-T054 EC2)
- [ ] The tax-agent questions are logged and the agent is engaged (P3-T001, P3-T038; P3-T054 EC3)
- [ ] All phase-3 tasks are done or cancelled
- [ ] No open S1/S2 bugs or gaps in phase 3

## Workstreams

| Workstream | Tasks |
|---|---|
| Your actions (USER) | P3-T001 engage tax agent · P3-T002 2027 reform status · P3-T003 export statements · P3-T004 diary 30 Jun 2027 · P3-T042 register + tag accounts · P3-T043 residency timeline |
| Storage & security (BUILD/OPS) | P3-T005 journal schema + WORM · P3-T006 roles + column keys (OPS) · P3-T007 column encryption + prompt exclusion · P3-T009 `journal` container + Fava (OPS) |
| Event model & ingestion (BUILD) | P3-T008 event model + writer · P3-T013 Nautilus fills · P3-T014 ccxt ledgers · P3-T015 IBKR Flex · P3-T016 OANDA + IG · P3-T017 on-chain stub · P3-T021 opening lots |
| FX & registry (BUILD) | P3-T010 FX core (RBA F11) · P3-T011 crypto rates + 3-currency stamping · P3-T012 account/wallet registry + tags · P3-T018 internal-transfer matcher |
| Lots & AU rules (BUILD) | P3-T019 lot engine · P3-T020 FX-cash lots + derivatives · P3-T022 plugin framework · P3-T023 AU_2026 CGT · P3-T024 revenue/income/Div 775 · P3-T025 regime + dual reporting · P3-T026 wash-sale · P3-T027 PAYG · P3-T028 myTax + schedules |
| 2027 reform & residency (BUILD/DOC) | P3-T029 AU_2027_REFORM flag · P3-T030 30 Jun 2027 snapshot job · P3-T031 residency + I1 · P3-T032 AE/EG/CY/GENERIC · P3-T033 Egypt flag → M11 · P3-T044 runbooks (DOC) |
| Exports & reconciliation (BUILD) | P3-T034 daily recon · P3-T035 Beancount · P3-T036 accountant pack + Koinly/Syla · P3-T037 CARF scaffold · P3-T038 TAX_QUESTION store |
| API & UI (BUILD) | P3-T039 journal/tax API · P3-T040 D14 Journal · P3-T041 D15 Tax & Reports |
| Verify | P3-T045 ATO golden + CI gate · P3-T046 property tests · P3-T047 WORM suite · P3-T048 snapshot dry run · P3-T049 Beancount + Fava · P3-T050 prompt audit · P3-T051 E2E scenarios · P3-T052 stress/failure injection · P3-T054 phase exit demo |
| Run | P3-T053 start the 1-month journalled paper run |

## Critical path

P3-T005 → P3-T008 → P3-T010 → P3-T011 → P3-T019 → P3-T020 → P3-T022 → P3-T023 → P3-T025 → P3-T027 → P3-T039 → P3-T041 → P3-T051 → P3-T054

In parallel: P3-T012 → P3-T013/T014 → P3-T018 → P3-T034 → P3-T053 (the 1-month run should start as early as possible); P3-T030 → P3-T048 (snapshot dry run well before 2027-06-30); P3-T001 (tax agent) starts on day one because the answer gates P7.

## Traceability

| Requirement | Tasks |
|---|---|
| R3.01 | P3-T003, P3-T005, P3-T008, P3-T009, P3-T013, P3-T014, P3-T015, P3-T016, P3-T017, P3-T021, P3-T051, P3-T052, P3-T053, P3-T054 |
| R3.02 | P3-T005, P3-T006, P3-T008, P3-T047, P3-T052 |
| R3.03 | P3-T010, P3-T011, P3-T051, P3-T054 |
| R3.04 | P3-T012, P3-T018, P3-T042, P3-T051 |
| R3.05 | P3-T003, P3-T019, P3-T020, P3-T021, P3-T046 |
| R3.06 | P3-T022, P3-T023, P3-T024, P3-T026, P3-T027, P3-T028, P3-T045, P3-T054 |
| R3.07 | P3-T001, P3-T025, P3-T038, P3-T054 |
| R3.08 | P3-T002, P3-T004, P3-T029, P3-T030, P3-T044, P3-T048 |
| R3.09 | P3-T022, P3-T031, P3-T032, P3-T033, P3-T043 |
| R3.10 | P3-T009, P3-T035, P3-T036, P3-T037, P3-T049 |
| R3.11 | P3-T034, P3-T037, P3-T044, P3-T046, P3-T052, P3-T053 |
| R3.12 | P3-T022, P3-T028, P3-T036, P3-T054 |
| R3.13 | P3-T039, P3-T040, P3-T051 |
| R3.14 | P3-T038, P3-T039, P3-T041, P3-T051, P3-T054 |
| R3.N1 | P3-T006, P3-T007, P3-T050 |
| R3.N2 | P3-T045 |

| Roadmap ToDo | Tasks |
|---|---|
| T3.01 | P3-T001 |
| T3.02 | P3-T002 |
| T3.03 | P3-T003 |
| T3.04 | P3-T042 |
| T3.05 | P3-T043 |
| T3.06 | P3-T004 |
| T3.20 | P3-T005, P3-T008, P3-T013, P3-T014, P3-T015, P3-T016, P3-T017, P3-T021, P3-T051, P3-T052 |
| T3.21 | P3-T010, P3-T011 |
| T3.22 | P3-T012, P3-T018 |
| T3.23 | P3-T019, P3-T020, P3-T021 |
| T3.24 | P3-T022, P3-T023, P3-T024, P3-T025, P3-T026, P3-T027, P3-T028 |
| T3.25 | P3-T029, P3-T030, P3-T044 |
| T3.26 | P3-T022, P3-T031, P3-T032, P3-T033 |
| T3.27 | P3-T035, P3-T036, P3-T037 |
| T3.28 | P3-T034, P3-T037, P3-T044, P3-T052 |
| T3.29 | P3-T039, P3-T040, P3-T041, P3-T051 |
| T3.30 | P3-T038 |
| T3.40 | P3-T009 |
| T3.41 | P3-T006, P3-T007, P3-T047 |
| T3.60 | P3-T045 |
| T3.61 | P3-T046 |
| T3.62 | P3-T048 |
| T3.63 | P3-T049 |
| T3.64 | P3-T050 |
| T3.80 | P3-T053 |

## Planning notes & risks

- **Tax agent answer gates P7.** P3-T001 starts on day one; the engine reports both regimes (P3-T025) until a written answer is recorded against the Q1 `TAX_QUESTION` (P3-T038). P7 T7.01 records the decision.
- **Hard date 2027-06-30.** The snapshot job (P3-T030) is built and dry-run (P3-T048) in this phase (~Jan–Feb 2027); the real run happens months after the phase closes. It is idempotent and uses recorded prices only, so a late run gives identical values. The diary item (P3-T004) and runbook (P3-T044) cover the day itself. Price convention is open (P3-B002, S2).
- **2027 reform status is contested** (09 vs 11 §3): `AU_2027_REFORM` defaults off and can only be enabled with an agent answer reference (P3-T029).
- **Crypto price provenance** (P3-B001, S2): tax values must come from our own recorded exchange bars, not CoinGecko (≤ 24 h retention). P3-T011 implements this default; the doc fix is open.
- **1-month RUN outlasts the build window.** P3-T053 starts the run and closes in-phase after 7 clean days; completion of the full month (and the T3.80 roadmap box) is checked by the P7 weekly review if needed.
- **Registry boundary with P5.** P3 creates `ops.wallets` + effective-dated tax tags (P3-T012); P5 wallet-indexer extends it additively (P3-B003). There is no P3 registry screen, so registration goes through a seed file loaded via `mt_api` commands (P3-B011).
- **TAX_QUESTION storage before M19.** P3-T038 creates a minimal additive `curation.task`; P5 T5.30 must extend, not recreate it (P3-B012).
- **Default treatments marked (U)** (futures, perps, stablecoins as foreign currency, fee-in-crypto disposals, Div 775 elections, myTax labels) are config flags surfaced on every report and raised as agent questions; they are never silently treated as settled.
- **Command catalogue additions** proposed by this plan: `tax.fy.lock`/`tax.fy.unlock`, `task.answer`, `journal.manual_event.add` (P3-B006); KV `compliance_state` for the Egypt flag, with C3 when a residency change loosens risk (P3-B007).
- **Not tax advice:** every D15 surface and report carries the footer; the engine produces inputs for the agent.

## Cross-phase prerequisites

| Phase | Roadmap IDs this phase relies on | Used by |
|---|---|---|
| P0 | R0.03/T0.22 (`journal` schema, Alembic), R0.05 (provenance columns), R0.07/T0.23/T0.61 (WORM layer + suite), R0.08/T0.24 (`mt_api`, C-levels, WS), R0.11/T0.26 (web shell, components), R0.N1/T0.43 (sops → tmpfs), R0.N4/T0.44 (immutable backups), T0.41/T0.42 (compose, networks, Prefect), T0.45 (LiteLLM config) | P3-T005–T009, T039–T041, T047, T050 |
| P1 | R1.04/T1.23 (RBA F11), R1.06/T1.24 (ABS CPI), R1.01–R1.03/T1.20–T1.22 (recorded crypto trades/bars), R1.08 (quota tracker), R1.12/T1.29 (read-only reconciliation clients), R1.14 (alerts), T1.02 (read-only keys) | P3-T010, T011, T014, T029, T030, T034 |
| P2 | R2.30/T2.25 (paper engine, `audit.fill`, OANDA/IG adapters), R2.31 (STP non-fills), R2.17/T2.22 (M11 venue/residency checks), R2.53/T2.34 (bots: `bot_id`, `strategy_id`), T2.26 (TCA costs vs modelled), T2.80 (paper clock) | P3-T013, T016, T033, T039, T040, T053 |
| P5 (downstream) | R5.05/T5.22 (wallet-indexer publishes `wallet.*.transfer`, extends `ops.wallets`), R5.18/T5.29 (airdrop classification evidence), R5.20/T5.30 (full task queue on `curation.task`) | consumes P3-T012, T017, T038 |
| P7 (downstream) | T7.01 (tax agent decision set in D15), R7.03/T7.05 (weekly review incl. journal recon; completes T3.80 if handed off), R7.09/T7.23 (three-way recon hardening) | consumes P3-T001, T025, T034, T053 |
