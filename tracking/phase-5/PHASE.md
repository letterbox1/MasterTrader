---
phase: 5
title: Airdrops, launches, wallets & curation
roadmap: docs/roadmap/phase-5-airdrops-wallets-curation.md
status: not_started
opens_after: [3, 4]
force_open: false
started: ""
completed: ""
doc_sync_status: n/a
updated: 2026-10-21
---

# Phase 5 · Airdrops, launches, wallets & curation

## Summary

Phase 5 makes on-chain activity safe and visible. Vetted airdrops and launches reach you as a weekly digest with step-by-step tasks. Safe, eligible claims execute automatically from capped identity wallets under signed, expiring mandates, with simulation proof and the on-chain cost gate. Scams are rejected with reasons, and every wallet you own is visible and reconciled in one place (D18).

The 64 tasks are organised in these workstreams:
- **Custody & signer (M22 part 1):** custody tiers; the intents-only `mt_signer` with EVM and Solana builders/decoders, allow-lists, caps, hard blocks and durable-nonce rules; Anvil / `simulateTransaction` simulation; isolated containers.
- **Cost gate:** fee samplers, formulas, gas windows and budgets.
- **Wallet view:** registry with proof of control, aggregators, transfer classifier into M18, daily journal and monthly rotki reconciliation.
- **Monitors & sweeps:** approvals, nonce authority, depeg, exploit/TVL, venue health, bridge policy and concentration; scheduled sweeps plus the kill-switch freeze and sweep.
- **M4 pipeline:** discovery, normalisation + corroboration, enrichment, risk (providers, heuristics, wallet clusters, blacklist, calibration), viability + EV + AU geo/KYC, decision engine, the never-automated guard, mandates, claim executor, burner-first/identity, disposal rule, records and the income journal.
- **M19 curation:** task queue, Telegram buttons and digests, community curation with Discord delivery verification.
- **UI:** D12, D13 and the P5 scope of D18.
- **Verification:** drainer suite, policy matrix, network isolation, SoK report, testnet claim, monitor simulations, kill drill, recon week, F8/F10 end-to-end, chaos, and the exit demo.

## Entry criteria

- [ ] Phase 3 done: journal (M18) live with FX service and account/wallet registry (P3 R3.01–R3.04, R3.11)
- [ ] Phase 4 done: Discord inbox (R4.04) and Telegram postures (R4.02, R4.03) flowing; text pipeline (R4.06) available
- [ ] P0 foundations in place: WORM layer (R0.07), `mt_api` confirmation levels C0–C3 (R0.08), networks incl. the isolated `signer` network (R0.N3), sops secrets (R0.N1)
- [ ] P2 kill switch/dead-man (R2.18), M11 pre-trade layer (R2.10) and Telegram C3 approvals (R2.51) working
- [ ] Vault and warm wallets created by you (P5-T001; roadmap T5.01–T5.03 are tracked as P5 USER items)

## Exit criteria

- [ ] A weekly digest of vetted airdrops/launches with EV, steps and verified links (roadmap §6.1; P5-T063, P5-T064)
- [ ] A testnet auto-claim with simulation proof, mandate and journal links; a scam rejected with reasons (roadmap §6.2; P5-T056, P5-T060)
- [ ] The drainer test suite passes; D18 shows every registered wallet reconciled to the journal (roadmap §6.3; P5-T052, P5-T059)
- [ ] All Phase 5 tasks done or cancelled
- [ ] No open S1/S2 bugs in Phase 5

## Workstreams

| Workstream | Tasks |
|---|---|
| Your actions (USER) | P5-T001, P5-T002, P5-T003, P5-T004, P5-T005, P5-T006, P5-T007, P5-T008 |
| Data model & contracts | P5-T009, P5-T010, P5-T011, P5-T012 |
| Signer & simulation | P5-T013, P5-T014, P5-T015, P5-T016 |
| Cost gate | P5-T019, P5-T020 |
| Wallet indexer & recon | P5-T021, P5-T022, P5-T023, P5-T024 |
| Monitors & sweeps | P5-T025, P5-T026, P5-T027, P5-T028 |
| M19 curation | P5-T029, P5-T030, P5-T047 |
| M4 discovery & enrichment | P5-T032, P5-T033, P5-T034, P5-T035 |
| M4 risk | P5-T036, P5-T037, P5-T038, P5-T039 |
| M4 decide & execute | P5-T040, P5-T041, P5-T042, P5-T043, P5-T044, P5-T045, P5-T046 |
| UI | P5-T048, P5-T049, P5-T050 |
| Ops | P5-T017, P5-T018, P5-T031 |
| Docs | P5-T051 |
| Verify | P5-T052, P5-T053, P5-T054, P5-T055, P5-T056, P5-T057, P5-T058, P5-T059, P5-T060, P5-T061, P5-T062, P5-T064 |
| Run | P5-T063 |

## Critical path

P5-T009 → P5-T010 → P5-T013 → P5-T014 / P5-T015 → P5-T016 → P5-T019 → P5-T020 → P5-T043 → P5-T044 → P5-T046 → P5-T056 → P5-T064

The parallel M4 track (P5-T032 → P5-T034 → P5-T035 → P5-T036 → P5-T037 → P5-T040 → P5-T041) must meet the executor at P5-T044. The wallet track (P5-T021 → P5-T022 → P5-T023 → P5-T024 → P5-T059) needs P5-T005 to start the 7-day recon window. The RUN window (P5-T063, two weeks) should start as soon as P5-T030/T041/T047 land.

## Traceability

The exit demo P5-T064 covers every requirement and is omitted from the table below.

| Requirement | Tasks |
|---|---|
| R5.01 | P5-T001, P5-T002, P5-T004, P5-T012, P5-T021, P5-T050 |
| R5.02 | P5-T010, P5-T013, P5-T014, P5-T015, P5-T016, P5-T017, P5-T052, P5-T056, P5-T062 |
| R5.03 | P5-T014, P5-T015, P5-T025, P5-T051, P5-T052 |
| R5.04 | P5-T003, P5-T018, P5-T019, P5-T020, P5-T062 |
| R5.05 | P5-T003, P5-T005, P5-T009, P5-T011, P5-T018, P5-T021, P5-T022, P5-T023, P5-T024, P5-T050, P5-T059, P5-T062 |
| R5.06 | P5-T025, P5-T026, P5-T027, P5-T057 |
| R5.07 | P5-T004, P5-T012, P5-T028, P5-T051, P5-T058 |
| R5.10 | P5-T032, P5-T033, P5-T060 |
| R5.11 | P5-T009, P5-T034, P5-T060 |
| R5.12 | P5-T003, P5-T018, P5-T035, P5-T060 |
| R5.13 | P5-T031, P5-T036, P5-T037, P5-T038, P5-T039, P5-T055, P5-T060, P5-T063 |
| R5.14 | P5-T007, P5-T040, P5-T041, P5-T060 |
| R5.15 | P5-T006, P5-T010, P5-T011, P5-T016, P5-T041, P5-T042, P5-T043, P5-T044, P5-T045, P5-T053, P5-T056 |
| R5.16 | P5-T014, P5-T016, P5-T042, P5-T052, P5-T053 |
| R5.17 | P5-T007, P5-T041, P5-T045, P5-T060 |
| R5.18 | P5-T009, P5-T010, P5-T023, P5-T038, P5-T044, P5-T046, P5-T056 |
| R5.20 | P5-T008, P5-T009, P5-T011, P5-T029, P5-T030, P5-T047, P5-T049, P5-T061 |
| R5.21 | P5-T008, P5-T047, P5-T049, P5-T061 |
| R5.22 | P5-T030, P5-T049, P5-T061, P5-T063 |
| R5.23 | P5-T011, P5-T048, P5-T049, P5-T050 |
| R5.N1 | P5-T017, P5-T054 |
| R5.N2 | P5-T013, P5-T028, P5-T044, P5-T058, P5-T062 |

| Roadmap ToDo | Tasks |
|---|---|
| T5.01 | P5-T001 |
| T5.02 | P5-T002 |
| T5.03 | P5-T004 |
| T5.04 | P5-T005 |
| T5.05 | P5-T006 |
| T5.06 | P5-T007 |
| T5.07 | P5-T008 |
| T5.20 | P5-T010, P5-T012, P5-T013, P5-T014, P5-T015, P5-T016 |
| T5.21 | P5-T019, P5-T020 |
| T5.22 | P5-T009, P5-T021, P5-T022, P5-T023, P5-T024 |
| T5.23 | P5-T025, P5-T026, P5-T027 |
| T5.24 | P5-T012, P5-T028 |
| T5.25 | P5-T009, P5-T032, P5-T033, P5-T034, P5-T035 |
| T5.26 | P5-T036, P5-T037, P5-T038, P5-T039 |
| T5.27 | P5-T040, P5-T041, P5-T042 |
| T5.28 | P5-T010, P5-T011, P5-T042, P5-T043, P5-T044, P5-T045 |
| T5.29 | P5-T009, P5-T010, P5-T046 |
| T5.30 | P5-T009, P5-T011, P5-T029, P5-T030, P5-T047 |
| T5.31 | P5-T011, P5-T048, P5-T049, P5-T050 |
| T5.40 | P5-T017, P5-T054 |
| T5.41 | P5-T003, P5-T018 |
| T5.42 | P5-T031 |
| T5.60 | P5-T052 |
| T5.61 | P5-T056 |
| T5.62 | P5-T055 |
| T5.63 | P5-T057 |
| T5.64 | P5-T058 |
| T5.65 | P5-T059 |
| T5.80 | P5-T063 |
| T5.90 | P5-T051 |

## Planning notes & risks

- **Decisions taken in planning:**
  - The on-chain cost gate is built in P5 as the library `mt_treasury.costgate` (P5-B002).
  - Auto-claims run from the per-chain **identity** wallet, not the trading hot wallet (P5-B017).
  - In P5, sweeps run inside `airdrop-exec` as the signer's only caller (P5-B003).
  - Disposal sells with no allowed venue become manual tasks until the P7 DEX path (P5-B010).
- **Numeric defaults are missing** for custody caps, floats and gas budgets (P5-B001, S2). Signing stays disabled (`UNSET_REQUIRES_USER`) until you set them in P5-T004. This S2 gap must close before the phase can finish.
- **Simulation is only a sanity check:** adversarial tokens can behave differently on execution. The backstops are caps, burner-first, hard blocks and the drainer suite (P5-T052), which is a required CI check.
- **Free RPC limits:** use one account per provider with fallbacks (P5-T018); wallet-cluster tracing has a per-token credit budget (P5-T038). Upgrade only when logs prove losses.
- **Airdrop tax classification** is marked (U). Campaign records attach the "activity done to earn it", and uncertain cases become `TAX_QUESTION` tasks for your tax agent (P5-T046).
- **Telegram:** only postures enter M4, and never as model features (P5-T033/T037). The P4 provenance gate is reused.
- **WORM:** mandates, the exec log, the signer ledger and the income journal are append-only (P5-T010). Revocations, expiries and corrections are new rows.
- **Long-running items:** P5-T059 (7 clean days) and P5-T063 (2 weeks) need elapsed time inside the 4-week phase. Start them early.
- **Out of scope:** hold-and-earn and treasury allocation (P6), social drafts (P6), DEX trading strategies and the memecoin template (P7). The wallet-drained runbook drill is P7 (T7.60).

## Cross-phase prerequisites

- **P0:**
  - R0.03 schemas;
  - R0.05 provenance columns;
  - R0.07 WORM layer (T0.23, tests T0.61);
  - R0.08 `mt_api` C0–C3 (T0.24, T0.62);
  - R0.N1 sops secrets (T0.43);
  - R0.N3 network segmentation (T0.42);
  - R0.N6 Playwright viewport matrix (T0.64).
- **P1:**
  - R1.08 quota tracker (T1.25);
  - R1.13 venue-health collector (T1.30);
  - R1.14 alerts (Telegram, email, ntfy) (T1.31);
  - R1.12 reconciliation framework (T1.29).
- **P2:**
  - R2.10 M11 default-deny pre-trade layer;
  - R2.13 sleeves (the `airdrop` sleeve);
  - R2.18 kill switch and dead-man (T2.23);
  - R2.19 change control;
  - R2.51/R2.52 Telegram approvals and `/kill` (T2.33);
  - T2.90 runbook format.
- **P3:**
  - R3.01 journal ingestion;
  - R3.02 append-only;
  - R3.03 FX (three currencies);
  - R3.04 account/wallet registry (T3.22);
  - R3.06 AU_2026 crypto income;
  - R3.11 recon;
  - T3.30 stored `TAX_QUESTION` tasks.
- **P4:**
  - R4.02/R4.03 Telegram postures and gate;
  - R4.04 Discord bot and `#mt-inbox`;
  - R4.06 text chain;
  - R4.12 tier B question registry (Discord classification).
