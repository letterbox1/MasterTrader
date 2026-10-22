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
updated: 2026-10-22
---

# Phase 5 · Airdrops, launches, wallets & curation

## Summary

Phase 5 makes on-chain activity safe and visible. Vetted airdrops and launches reach you as a weekly digest with step-by-step tasks. Safe, eligible claims execute automatically from capped identity wallets under signed, expiring mandates, with simulation proof and the on-chain cost gate. Scams are rejected with reasons, and every wallet you own is visible and reconciled in one place (D18).

The 69 tasks are organised in these workstreams (aligned 2026-10-22 with the decisions in docs/16–17; build first, keys last):
- **Custody & signer (M22 part 1):** custody tiers; wallet/signer/gas limits as configurable 16 §2.7 defaults with signing disabled until you confirm them; the intents-only `mt_signer` (callers: the policy service only) with EVM and Solana builders/decoders, allow-lists, caps, hard blocks and durable-nonce rules; Anvil / `simulateTransaction` simulation; isolated containers.
- **Cost gate:** the `mt_onchain.costgate` library: fee samplers, formulas, gas windows and budgets.
- **Wallet view:** the P3 `ops.wallets` registry extended additively, proof of control (you sign a one-time challenge in your own wallet app or self-transfer; the system only verifies), aggregators, transfer classifier into M18, daily journal and monthly rotki reconciliation.
- **Monitors & sweeps:** approvals, nonce authority, depeg (alert + task until P6), exploit/TVL, venue health, bridge policy and concentration; scheduled sweeps plus the kill-switch freeze and the hot-wallet sweep to the vault (default on).
- **M4 pipeline:** discovery, normalisation + corroboration, enrichment, risk (providers, heuristics, wallet clusters, blacklist, calibration), viability + EV + AU geo/KYC, decision engine, the never-automated guard, mandates, claim executor (identity wallet only), burner-first/identity, disposal rule (manual-sale USER task until the P7 gates), records and the income journal.
- **M19 curation:** task queue on the P3 `curation.task` table with the canonical 03 M19 types, Telegram buttons (incl. Details) and digests, community curation with Discord delivery verification.
- **UI:** D12, D13 and the P5 scope of D18.
- **Verification:** drainer suite, policy matrix, network isolation, SoK report, testnet claim, monitor simulations, kill drill, recon week, F8/F10 end-to-end, chaos, proof-of-control test, the late live-key check (P5-T068), and the exit demo.

## Entry criteria

- [ ] Phase 3 done: journal (M18) live with FX service and account/wallet registry (P3 R3.01–R3.04, R3.11)
- [ ] Phase 4 done: Discord inbox (R4.04) and Telegram postures (R4.02, R4.03) flowing; text pipeline (R4.06) available
- [ ] P0 foundations in place: WORM layer (R0.07), `mt_api` confirmation levels C0–C3 (R0.08), networks incl. the isolated `signer` network (R0.N3), sops secrets (R0.N1)
- [ ] P2 kill switch/dead-man (R2.18), M11 pre-trade layer (R2.10) and Telegram C3 approvals (R2.51) working
- [ ] Vault and warm wallets created by you (P5-T001; roadmap T5.01–T5.03 are tracked as P5 USER items)
- [ ] With `phase_gating: "dependencies"`, each task waits only for its own `depends_on`, including the explicit P0–P4 task IDs listed under Cross-phase prerequisites

## Exit criteria

- [ ] A weekly digest of vetted airdrops/launches with EV, steps and verified links (roadmap §6.1; P5-T063, P5-T064)
- [ ] A testnet auto-claim with simulation proof, mandate and journal links; a scam rejected with reasons (roadmap §6.2; P5-T056, P5-T060)
- [ ] The drainer test suite passes; D18 shows every registered wallet reconciled to the journal (roadmap §6.3; P5-T052, P5-T059)
- [ ] All Phase 5 tasks done or cancelled
- [ ] No open S1/S2 bugs in Phase 5

## Workstreams

| Workstream | Tasks |
|---|---|
| Your actions (USER) | P5-T001, P5-T002, P5-T003, P5-T004, P5-T005, P5-T006, P5-T007, P5-T008, P5-T065, P5-T066 |
| Data model & contracts | P5-T009, P5-T010, P5-T011, P5-T012 |
| Signer & simulation | P5-T013, P5-T014, P5-T015, P5-T016 |
| Cost gate (`mt_onchain.costgate`) | P5-T019, P5-T020 |
| Wallet registry, proof of control, indexer & recon | P5-T021, P5-T067, P5-T022, P5-T023, P5-T024 |
| Monitors & sweeps | P5-T025, P5-T026, P5-T027, P5-T028 |
| M19 curation | P5-T029, P5-T030, P5-T047 |
| M4 discovery & enrichment | P5-T032, P5-T033, P5-T034, P5-T035 |
| M4 risk | P5-T036, P5-T037, P5-T038, P5-T039 |
| M4 decide & execute | P5-T040, P5-T041, P5-T042, P5-T043, P5-T044, P5-T045, P5-T046 |
| UI | P5-T048, P5-T049, P5-T050 |
| Ops | P5-T017, P5-T018, P5-T031 |
| Docs | P5-T051 |
| Verify (keyless: Anvil, devnets, fixtures) | P5-T052, P5-T053, P5-T054, P5-T055, P5-T056, P5-T057, P5-T058, P5-T060, P5-T061, P5-T062, P5-T069 |
| Verify (live keys, last) | P5-T068 → P5-T059, P5-T063 (and the live part of P5-T060) |
| Run | P5-T063 |
| Exit | P5-T064 |

## Critical path

P5-T009 → P5-T010 → P5-T013 → P5-T014 / P5-T015 → P5-T016 → P5-T044 → P5-T046 → P5-T056 → P5-T064, with P5-T012 → P5-T050 → P5-T065 (you confirm the limits; signing stays off until then) gating every signing VERIFY item (P5-T056, P5-T058).

Parallel tracks that need no keys: cost gate (P5-T018 → P5-T019 → P5-T020), M4 (P5-T032 → P5-T034 → P5-T035 → P5-T036 → P5-T037 → P5-T040 → P5-T041, meeting the executor at P5-T044), curation (P5-T029 → P5-T030 / P5-T047 → P5-T049), and the wallet track (P5-T067 → P5-T021 → P5-T022 → P5-T023 → P5-T024).

Keys last: P0-T010 + P5-T003 (keys) and P5-T005 (your registered addresses) → P5-T068 (live read-only check) → P5-T059 (7-day recon window) and P5-T063 (two weekly digests). Start P5-T068 as soon as P5-T005 is done, because the two observation windows need elapsed time.

## Traceability

The exit demo P5-T064 covers every requirement and is omitted from the table below.

| Requirement | Tasks |
|---|---|
| R5.01 | P5-T001, P5-T002, P5-T004, P5-T012, P5-T021, P5-T050, P5-T065 |
| R5.02 | P5-T010, P5-T013, P5-T014, P5-T015, P5-T016, P5-T017, P5-T052, P5-T056, P5-T062 |
| R5.03 | P5-T014, P5-T015, P5-T025, P5-T051, P5-T052 |
| R5.04 | P5-T003, P5-T018, P5-T019, P5-T020, P5-T062, P5-T065 |
| R5.05 | P5-T003, P5-T005, P5-T009, P5-T011, P5-T018, P5-T021, P5-T022, P5-T023, P5-T024, P5-T050, P5-T059, P5-T062, P5-T067, P5-T068, P5-T069 |
| R5.06 | P5-T025, P5-T026, P5-T027, P5-T057 |
| R5.07 | P5-T004, P5-T012, P5-T028, P5-T051, P5-T058 |
| R5.10 | P5-T032, P5-T033, P5-T060 |
| R5.11 | P5-T009, P5-T034, P5-T060 |
| R5.12 | P5-T003, P5-T018, P5-T035, P5-T060, P5-T068 |
| R5.13 | P5-T031, P5-T036, P5-T037, P5-T038, P5-T039, P5-T055, P5-T060, P5-T063, P5-T068 |
| R5.14 | P5-T007, P5-T040, P5-T041, P5-T060 |
| R5.15 | P5-T006, P5-T010, P5-T011, P5-T016, P5-T041, P5-T042, P5-T043, P5-T044, P5-T045, P5-T053, P5-T056 |
| R5.16 | P5-T014, P5-T016, P5-T042, P5-T052, P5-T053 |
| R5.17 | P5-T007, P5-T041, P5-T045, P5-T060, P5-T066 |
| R5.18 | P5-T009, P5-T023, P5-T038, P5-T044, P5-T046, P5-T056, P5-T066 |
| R5.20 | P5-T008, P5-T009, P5-T011, P5-T029, P5-T030, P5-T047, P5-T049, P5-T061 |
| R5.21 | P5-T008, P5-T047, P5-T049, P5-T061 |
| R5.22 | P5-T030, P5-T049, P5-T061, P5-T063 |
| R5.23 | P5-T011, P5-T048, P5-T049, P5-T050 |
| R5.24 | P5-T004, P5-T012, P5-T050, P5-T065 |
| R5.25 | P5-T005, P5-T009, P5-T021, P5-T050, P5-T067, P5-T069 |
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
| T5.08 | P5-T065 |
| T5.09 | P5-T066 |
| T5.20 | P5-T010, P5-T012, P5-T013, P5-T014, P5-T015, P5-T016 |
| T5.21 | P5-T019, P5-T020 |
| T5.22 | P5-T009, P5-T021, P5-T022, P5-T023, P5-T024 |
| T5.23 | P5-T025, P5-T026, P5-T027 |
| T5.24 | P5-T012, P5-T028 |
| T5.25 | P5-T009, P5-T032, P5-T033, P5-T034, P5-T035 |
| T5.26 | P5-T036, P5-T037, P5-T038, P5-T039 |
| T5.27 | P5-T040, P5-T041, P5-T042 |
| T5.28 | P5-T010, P5-T011, P5-T042, P5-T043, P5-T044, P5-T045 |
| T5.29 | P5-T009, P5-T046 |
| T5.30 | P5-T009, P5-T011, P5-T029, P5-T030, P5-T047 |
| T5.31 | P5-T011, P5-T048, P5-T049, P5-T050 |
| T5.32 | P5-T067 |
| T5.40 | P5-T017, P5-T054 |
| T5.41 | P5-T003, P5-T018 |
| T5.42 | P5-T031 |
| T5.60 | P5-T052 |
| T5.61 | P5-T056 |
| T5.62 | P5-T055 |
| T5.63 | P5-T057 |
| T5.64 | P5-T058 |
| T5.65 | P5-T059 |
| T5.66 | P5-T068 |
| T5.67 | P5-T069 |
| T5.80 | P5-T063 |
| T5.90 | P5-T051 |

## Planning notes & risks

- **Decisions applied (docs/16–17, 2026-10-22):**
  - Wallet floats, signer caps, gas budgets, cost-gate margin, gas window and EV hurdle are configuration with 16 §2.7 defaults; signing stays disabled until you confirm them (P5-T012, P5-T065; P5-B001).
  - The cost gate is the library `mt_onchain.costgate`, used by the signer path from P5 and by the treasury in P6 (P5-B002).
  - The signer accepts intents only from the policy service (`airdrop-exec` in P5; treasury and DEX execution later go through it) (P5-B003).
  - Vault and warm are watch-only; the system may only prepare unsigned transactions for you to sign in your own wallet (P5-B008).
  - Autonomous claims use the chain's airdrop identity wallet, never the hot trading wallet (P5-B017).
  - One wallet registry, `ops.wallets` (created in P3, extended here); one task table, `curation.task` (created in P3, extended here), with the canonical 03 M19 task types; communities in `curation.community` (P5-B004, P5-B015).
  - Proof of control: you sign a one-time challenge in your own wallet app or make a tiny self-transfer; the system never signs (P5-T067; P5-B016).
  - Depeg before P6: alert + task only, no automated reduce (P5-T026; P5-B009).
  - Kill switch: freezes claims and treasury moves and, from P5 (default on), sweeps hot trading balances to the vault; protective sweeps/revokes are exempt (P5-T028; P5-B007).
  - Disposal: a manual-sale USER task until the P7 gates; automated via M11 only after them (P5-T045, P5-T066; P5-B010).
  - Simulation: Anvil and `simulateTransaction` only; Tenderly is not used (P5-T016; P5-B013).
  - Curation defaults: Discord re-prompt after 7 days, ≤ 3 new servers per week (16 §2.13); Telegram buttons include Details (P5-B011, P5-B014).
  - Airdrop income is a `journal.event` row linked to the campaign record (no separate income table; P5-T046).
- **Build first, keys last:** every BUILD/OPS task runs keyless against Anvil, `solana-test-validator`, Sepolia/devnet faucets and recorded fixtures. Live keys (P0-T010, P5-T003) are first used by P5-T068, then by the live windows P5-T059/P5-T063 and the live run of P5-T060. Testnet keys for P5-T056/P5-T058 are created in those tasks' setup (faucet funds, C3 approved by you), so they don't wait on real-funds steps (P5-T004, P5-T006).
- **Simulation is only a sanity check:** adversarial tokens can behave differently on execution. The backstops are caps, burner-first, hard blocks and the drainer suite (P5-T052), which is a required CI check.
- **Free RPC limits:** use one account per provider with fallbacks (P5-T018); wallet-cluster tracing has a per-token credit budget (P5-T038). Upgrade only when logs prove losses.
- **Airdrop tax classification** is marked (U). Campaign records attach the "activity done to earn it", and uncertain cases become `TAX_QUESTION` tasks for your tax agent (P5-T046).
- **Telegram:** only postures enter M4, and never as model features (P5-T033/T037). The P4 provenance gate is reused.
- **WORM:** mandates, the exec log and the signer ledger (`audit.signer_ledger`) are append-only (P5-T010); income rows are WORM `journal.event` rows. Revocations, expiries and corrections are new rows.
- **Long-running items:** P5-T059 (7 clean days) and P5-T063 (2 weeks) need elapsed time. Start them as soon as P5-T068 passes.
- **Open gaps:** P5-B013 (research note still cites Tenderly) and P5-B017 (02 §2 diagram label "hot-wallet claims only") wait for a doc fix; both S3/S4, implementation already aligned.
- **Out of scope:** hold-and-earn and treasury allocation (P6), the automated depeg reduce (P6), social drafts (P6), DEX trading strategies, the memecoin template and automated disposal sales (P7). The wallet-drained runbook drill is P7 (T7.60).

## Cross-phase prerequisites

These are explicit `depends_on` entries on the tasks that need them (they replace the old phase gate):
- **P0:** P0-T002 (Telegram bot) and P0-T008 (Discord bot) → P5-T061; P0-T010 (free API keys) → P5-T003, P5-T068; P0-T020/T021/T022 (Compose, networks, sops) → P5-T017, P5-T054; P0-T024/T025 (schemas, provenance columns) → P5-T009; P0-T029/T030/T037 (WORM triggers, hash chain, seal) → P5-T010; P0-T034/T035/T036 (command bus, confirmation levels, WS hub) → P5-T011; P0-T050 (app shell) → P5-T048, P5-T049, P5-T050.
- **P1:** P1-T004 (NATS streams) → P5-T011; P1-T006 (quota tracker) → P5-T018, P5-T032; P1-T043 (venue health) → P5-T027; P1-T045 (alert fan-out) → P5-T025, P5-T026, P5-T030.
- **P2:** P2-T010/T019 (policy store, change control C3) → P5-T012; P2-T015 (portfolio concentration) → P5-T027; P2-T031 (kill switch) → P5-T013, P5-T028; P2-T035 (Telegram C3 + TOTP) → P5-T030, P5-T043, P5-T065; P2-T046 (MLflow) → P5-T039; P2-T068 (runbook format) → P5-T051.
- **P3:** P3-T008 (journal writer) → P5-T046; P3-T010 (FX) → P5-T019; P3-T011 (crypto rates) → P5-T022, P5-T046; P3-T012 (`ops.wallets`) → P5-T009, P5-T021; P3-T017/T018 (on-chain adapter, internal-transfer matcher) → P5-T023; P3-T034 (recon) → P5-T024; P3-T038 (`curation.task`) → P5-T009; P3-T042 (your P3 account registration) → P5-T005.
- **P4:** P4-T019 (Telegram postures), P4-T020 (Discord ingest), P4-T025 (provenance gate), P4-T028 (tier B registry) → P5-T033; P4-T020 → P5-T047.
