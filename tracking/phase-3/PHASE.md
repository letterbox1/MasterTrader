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
updated: 2026-10-22
---

# Phase 3 · Journal & tax

## Summary

Every economic event (fills, fees, funding, transfers, statements, on-chain events) is journalled automatically into WORM `journal.*` tables in **native, USD and AUD** with rate provenance: RBA F11 for AUD (last published business day on gaps; non-F11 currencies via USD) and crypto values from the **valuation hierarchy** of 16 §4.1 (fill price → VWAP of our recorded trades → on-chain pool price; aggregators cross-check only). A lot engine (specific-ID → FIFO, FX-cash lots for Div 775, Decimal everywhere) feeds a dated jurisdiction-plugin engine: **AU_2026** (CGT discount, revenue CFDs/futures/perps (U), Div 775, crypto income, wash-sale flags at 30 days either side (16 §4.4, flag only), myTax worksheet, **PAYG estimator computing both ATO methods**), reported **both ways** (investor vs trader-in-business) until the tax agent decides; **AU_2027_REFORM** behind a flag plus the **30 June 2027 snapshot job** using the 16 §4.2 per-asset-class price convention; a residency timeline with CGT event I1 whose changes emit `tax.residency.changed` (venue registry recomputes; loosening is C3; Egypt blocks crypto via the registry); and AE / EG / CY / GENERIC stubs. The phase also delivers `ops.wallets` with a minimal D16 **Accounts page**, a minimal `curation.task` table for `TAX_QUESTION`s, the commands `tax.fy.lock`/`unlock` (C3), `task.answer` (C1) and `journal.manual_event.add` (C2), envelope encryption (master key in sops, yearly data keys re-wrapped on rotation in a non-WORM key table), a bounded JetStream buffer for the Postgres-down write path (1 GB / 24 h; new entries stop at 80%), exports (Beancount + Fava, accountant pack, Koinly/Syla CSV, CARF from venue statements when available), daily journal↔venue reconciliation, and D14 / D15. You engage a tax agent now: the investor-vs-trader answer gates P7.

**Build first, keys last:** every importer and statement parser is built and tested against recorded responses and sample files. Your real statements and the read-only practice/testnet keys are used only by the late check P3-T061 and the RUN item P3-T053. Cross-phase prerequisites are explicit `depends_on` entries (replacing the old phase gate).

## Entry criteria

- [ ] Phase 2 paper fills flowing through M11 on testnet/practice accounts; `audit.fill` populated (P2-T021; paper clock P2-T180) — needed by P3-T013/T053 only
- [ ] RBA F11 daily FX and ABS CPI series loaded and readable via `pit(as_of)` (P1-T020, P1-T027) — needed by P3-T010/T029/T030 only
- [ ] P0 WORM layer and `journal`/`ops`/`curation` schemas exist (P0-T024, P0-T029, P0-T030, P0-T038)
- [ ] `mt_api` command bus with C0–C3 levels, WebSocket hub and web shell available (P0-T034, P0-T035, P0-T036, P0-T048–T050)
- [ ] Read-only practice/testnet keys in the sops file (P1-T002) — needed by P3-T053/T061 only

## Exit criteria

- [ ] Every paper trade, fee and funding payment appears automatically in the journal in native/USD/AUD (P3-T054 EC1)
- [ ] D15 shows FY-to-date AU figures both ways (investor vs trader) and a PAYG estimate, each with rule version + FX source (P3-T054 EC2)
- [ ] The tax-agent questions are logged and the agent is engaged (P3-T001, P3-T038; P3-T054 EC3)
- [ ] All phase-3 tasks are done or cancelled
- [ ] No open S1/S2 bugs or gaps in phase 3

## Workstreams

| Workstream | Tasks |
|---|---|
| Your actions (USER) | P3-T001 engage tax agent (12 questions) · P3-T002 2027 reform status · P3-T003 export statements · P3-T004 diary 30 Jun 2027 · P3-T042 register + tag accounts (Accounts page) · P3-T043 residency timeline |
| Storage & security (BUILD/OPS) | P3-T005 journal schema + WORM · P3-T006 roles + envelope-encryption keys (OPS) · P3-T007 column encryption + prompt exclusion · P3-T009 `journal` container + Fava (OPS) · P3-T057 JetStream write-path buffer (OPS) |
| Event model & ingestion (BUILD, keyless) | P3-T008 event model + writer · P3-T013 Nautilus fills · P3-T014 ccxt ledgers · P3-T015 IBKR Flex · P3-T016 OANDA + IG · P3-T017 on-chain stub · P3-T021 opening lots |
| FX, valuation & registry (BUILD) | P3-T010 FX (RBA F11) · P3-T011 valuation service (16 §4.1/§4.2) + 3-currency stamping · P3-T012 `ops.wallets` + tags · P3-T018 internal-transfer matcher · P3-T056 Accounts page (D16) |
| Lots & AU rules (BUILD) | P3-T019 lot engine · P3-T020 FX-cash lots + derivatives · P3-T022 plugin framework · P3-T023 AU_2026 CGT · P3-T024 revenue/income/Div 775 · P3-T025 regime + dual reporting · P3-T026 wash-sale (30 d) · P3-T027 PAYG (both methods) · P3-T028 myTax + schedules |
| 2027 reform, residency & commands (BUILD/DOC) | P3-T029 AU_2027_REFORM flag · P3-T030 30 Jun 2027 snapshot job · P3-T031 residency + I1 · P3-T032 AE/EG/CY/GENERIC · P3-T033 Egypt block via registry · P3-T055 FY lock/unlock, manual events, residency contract · P3-T044 runbooks (DOC) |
| Exports & reconciliation (BUILD) | P3-T034 daily recon · P3-T035 Beancount · P3-T036 accountant pack + Koinly/Syla · P3-T037 CARF (venue statements) · P3-T038 minimal `curation.task` + `TAX_QUESTION` + `task.answer` |
| API & UI (BUILD) | P3-T039 journal/tax API · P3-T040 D14 Journal · P3-T041 D15 Tax & Reports |
| Verify | P3-T045 ATO golden + CI gate · P3-T046 property tests · P3-T047 WORM suite · P3-T048 snapshot dry run · P3-T049 Beancount + Fava · P3-T050 prompt audit · P3-T051 E2E scenarios · P3-T052 stress/failure injection · P3-T058 command tests · P3-T059 key-rotation drill · P3-T060 Postgres-down drill · P3-T061 live importer check (keys last) · P3-T054 phase exit demo |
| Run | P3-T053 start the 1-month journalled paper run |

## Critical path

P3-T005 → P3-T008 → P3-T010 → P3-T011 → P3-T019 → P3-T023 → P3-T025 → P3-T027 → P3-T039 → P3-T041 → P3-T051 → P3-T054

In parallel (each starts as soon as its own dependencies are done):
- P3-T022 (framework) and P3-T038 (`curation.task`) start right after the event model / P0 schemas; P3-T018 needs only the writer + registry.
- P3-T055 (commands + residency contract) → P3-T031 → P3-T033 → P3-T058.
- P3-T012 → P3-T056 (Accounts page) → P3-T042 (your registration) → P3-T053 (1-month run; start as early as possible).
- P3-T013/T014 → P3-T034 → P3-T053; P3-T057 → P3-T060.
- P3-T030 → P3-T048 (snapshot dry run well before 2027-06-30).
- P3-T001 (tax agent) starts on day one because the answer gates P7; P3-T003 → P3-T061 whenever your exports are ready.

## Traceability

| Requirement | Tasks |
|---|---|
| R3.01 | P3-T003, P3-T005, P3-T008, P3-T009, P3-T013, P3-T014, P3-T015, P3-T016, P3-T017, P3-T021, P3-T051, P3-T052, P3-T053, P3-T054, P3-T060, P3-T061 |
| R3.02 | P3-T005, P3-T006, P3-T008, P3-T047, P3-T052, P3-T055, P3-T057, P3-T059, P3-T060 |
| R3.03 | P3-T010, P3-T011, P3-T051, P3-T054 |
| R3.04 | P3-T012, P3-T018, P3-T042, P3-T051, P3-T056 |
| R3.05 | P3-T003, P3-T019, P3-T020, P3-T021, P3-T046, P3-T061 |
| R3.06 | P3-T022, P3-T023, P3-T024, P3-T026, P3-T027, P3-T028, P3-T045, P3-T054 |
| R3.07 | P3-T001, P3-T025, P3-T038, P3-T054 |
| R3.08 | P3-T002, P3-T004, P3-T029, P3-T030, P3-T044, P3-T048 |
| R3.09 | P3-T022, P3-T031, P3-T032, P3-T033, P3-T043, P3-T055 |
| R3.10 | P3-T009, P3-T035, P3-T036, P3-T037, P3-T049 |
| R3.11 | P3-T034, P3-T037, P3-T044, P3-T046, P3-T052, P3-T053 |
| R3.12 | P3-T022, P3-T028, P3-T036, P3-T054 |
| R3.13 | P3-T039, P3-T040, P3-T051 |
| R3.14 | P3-T038, P3-T039, P3-T041, P3-T051, P3-T054 |
| R3.N1 | P3-T006, P3-T007, P3-T050, P3-T059 |
| R3.N2 | P3-T045 |
| R3.15 | P3-T011, P3-T030, P3-T045, P3-T051, P3-T054 |
| R3.16 | P3-T031, P3-T033, P3-T038, P3-T051, P3-T054, P3-T055, P3-T058 |
| R3.17 | P3-T042, P3-T051, P3-T056 |
| R3.18 | P3-T038 |
| R3.N3 | P3-T054, P3-T057, P3-T060 |

| Roadmap ToDo | Tasks |
|---|---|
| T3.01 | P3-T001 |
| T3.02 | P3-T002 |
| T3.03 | P3-T003 |
| T3.04 | P3-T042 |
| T3.05 | P3-T043 |
| T3.06 | P3-T004 |
| T3.20 | P3-T005, P3-T008, P3-T013, P3-T014, P3-T015, P3-T016, P3-T017, P3-T021, P3-T051, P3-T052, P3-T061 |
| T3.21 | P3-T010, P3-T011 |
| T3.22 | P3-T012, P3-T018 |
| T3.23 | P3-T019, P3-T020, P3-T021, P3-T061 |
| T3.24 | P3-T022, P3-T023, P3-T024, P3-T025, P3-T026, P3-T027, P3-T028 |
| T3.25 | P3-T029, P3-T030, P3-T044 |
| T3.26 | P3-T022, P3-T031, P3-T032, P3-T033 |
| T3.27 | P3-T035, P3-T036, P3-T037 |
| T3.28 | P3-T034, P3-T037, P3-T044, P3-T052 |
| T3.29 | P3-T039, P3-T040, P3-T041, P3-T051 |
| T3.30 | P3-T038 |
| T3.31 | P3-T011, P3-T030 |
| T3.32 | P3-T038, P3-T055 |
| T3.33 | P3-T056 |
| T3.40 | P3-T009 |
| T3.41 | P3-T006, P3-T007, P3-T047 |
| T3.42 | P3-T057 |
| T3.60 | P3-T045 |
| T3.61 | P3-T046 |
| T3.62 | P3-T048 |
| T3.63 | P3-T049 |
| T3.64 | P3-T050 |
| T3.65 | P3-T058 |
| T3.66 | P3-T059 |
| T3.67 | P3-T060 |
| T3.80 | P3-T053 |

## Planning notes & risks

- **Tax agent answer gates P7.** P3-T001 starts on day one with the 12 questions in 09 (incl. perps Q8, snapshot convention/VWAP Q10, PAYG method Q11, wash-sale window Q12); the engine reports both regimes (P3-T025) until a written answer is recorded with `task.answer` against the Q1 `TAX_QUESTION` (P3-T038). P7 T7.01 records the decision.
- **Hard date 2027-06-30.** The snapshot job (P3-T030) is built and dry-run (P3-T048) in this phase; the real run happens months after the phase closes. It is idempotent and uses recorded prices only (16 §4.2: crypto VWAP 23:55:00–23:59:59 AEST, so the recorders must be up through midnight), so a late run gives identical values. The diary item (P3-T004) and runbook (P3-T044) cover the day itself.
- **2027 reform status is contested** (09 vs 11 §3): `AU_2027_REFORM` defaults off and can only be enabled with an agent answer reference (P3-T029).
- **Valuation provenance** (decided, 16 §4.1): stored values are always ours (fill price, recorded-trade VWAP, pool price) with method and source; CoinGecko is a cross-check only (P3-T011). The pool-price tier needs an RPC endpoint; until the P5 RPC set-up exists, long-tail tokens go to `pending_price` rather than being valued at zero.
- **Build first, keys last.** Importers (P3-T013–T017, T021) are built on recorded responses and sample files with no secrets; your real statements and read-only practice keys are used only by P3-T061 and the RUN item P3-T053.
- **1-month RUN outlasts the build window.** P3-T053 starts the run and closes in-phase after 7 clean days; completion of the full month (and the T3.80 roadmap box) is checked by the P7 weekly review if needed.
- **Registry boundary with P5.** P3 creates `ops.wallets` + effective-dated tax tags (P3-T012) and the minimal D16 Accounts page (P3-T056); the P5 wallet-indexer and D18 extend both additively (17 §B).
- **`curation.task` before M19.** P3-T038 creates the minimal table with the canonical 03 M19 type list; P5 T5.30 must extend, not recreate it.
- **Residency contract.** `tax.residency.changed` → venue-registry recompute; tightening immediate, loosening C3; M11 fails closed while a recompute is pending (P3-T055, P3-T033). The earlier KV `compliance_state` proposal is dropped.
- **Postgres-down write path.** Bounded `WORM_BUFFER` stream (default 1 GB / 24 h); M11 stops new entries at 80%, exits continue (P3-T057, drilled in P3-T060). It also covers P0 `audit.*` writers, so the P0 owners should review the buffer library when it lands.
- **Default treatments marked (U)** (futures, perps, stablecoins as foreign currency, fee-in-crypto disposals, Div 775 elections, myTax labels, PAYG due dates) are settings surfaced on every report and raised as agent questions; they are never silently treated as settled.
- **New settings without a 16 entry yet:** `fx.max_prior_business_days` (default 5, P3-T010), the transfer-match windows (P3-T018), the CARF difference threshold (P3-T037) and the PAYG reminder lead time (P3-T027) are configurable in `config/journal/*` but not yet listed in docs/16; flagged for the doc owner.
- **Not tax advice:** every D15 surface and report carries the footer; the engine produces inputs for the agent.

## Cross-phase prerequisites

Explicit `depends_on` entries (they replace the old `opens_after` phase gate once `phase_gating: "dependencies"` is on):

| Prerequisite | Used by |
|---|---|
| P0-T015 CI pipeline | P3-T045 |
| P0-T016 `mt_core` schemas | P3-T008, P3-T017 |
| P0-T018 `mt_obs` logging | P3-T007 |
| P0-T020 compose stack · P0-T021 networks · P0-T023 observability | P3-T009, P3-T057 |
| P0-T022 sops + age → tmpfs | P3-T006 |
| P0-T024 schemas/roles/Alembic | P3-T005, P3-T006, P3-T012, P3-T038 |
| P0-T025 provenance columns | P3-T007 |
| P0-T027 `pit(as_of)` | P3-T010, P3-T011 |
| P0-T029 WORM triggers · P0-T030 hash chain · P0-T031 WORM audit tables | P3-T005, P3-T057 |
| P0-T032/T034/T035/T036 `mt_api`, command bus, C-levels, WS | P3-T012, P3-T038, P3-T039, P3-T055 |
| P0-T038 `audit.verify` + incident path · P0-T055 WORM suite | P3-T047, P3-T059 |
| P0-T042 LiteLLM gateway | P3-T050 |
| P0-T048/T049/T050/T052 web client, components, shell, D16 settings | P3-T040, P3-T041, P3-T056 |
| P1-T002 read-only practice/testnet keys (USER) | P3-T053, P3-T061 |
| P1-T004 JetStream streams | P3-T057 |
| P1-T006 quota tracker | P3-T014 |
| P1-T012 recorded trades (Parquet) | P3-T011, P3-T030 |
| P1-T019 ECB/Frankfurter · P1-T020 RBA F11 | P3-T010, P3-T030 |
| P1-T021 recorded US trades · P1-T023 daily closes | P3-T030 |
| P1-T027 ABS CPI | P3-T029 |
| P1-T041/T042 reconciliation clients | P3-T034 |
| P2-T001 testnet keys (USER) | P3-T051 |
| P2-T016 M11 venue-registry check · P2-T017 RiskGate | P3-T033, P3-T055, P3-T057 |
| P2-T019 change-control service (C3) | P3-T055 |
| P2-T021 engine fills / `audit.fill` | P3-T013 |
| P2-T180 paper clock started | P3-T053 |
| Downstream: P5 R5.05/T5.22 (wallet-indexer extends `ops.wallets`), R5.18/T5.29 (airdrop evidence), R5.20/T5.30 (full queue on `curation.task`); P7 T7.01 (tax decision), R7.03/T7.05 (weekly review incl. journal recon), R7.09/T7.23 (three-way recon) | consume P3-T012, T017, T038, T001, T025, T034, T053 |
