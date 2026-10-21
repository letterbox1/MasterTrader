---
phase: 7
title: Prove it, then go small-live
roadmap: docs/roadmap/phase-7-prove-and-go-live.md
status: not_started
opens_after: [3]
force_open: false
started: ""
completed: ""
doc_sync_status: n/a
updated: 2026-10-21
---

# Phase 7 · Prove it, then go small-live

## Summary

Only strategies that pass every gate on paper reach live money, in small sub-accounts with withdrawals disabled; capital steps up only on evidence (25% after 4 clean weeks) and stops on pre-written kill criteria ([roadmap](../../docs/roadmap/phase-7-prove-and-go-live.md), [14 §7](../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7)).

The work is organised in eight workstreams:

1. **Entry checks and your pre-live actions:** tax decision, advice, venue checks, accounts, keys, Travel Rule, UPS/4G.
2. **Evidence:** the gate report, paper tracking, reference distributions, weekly review pack and sign-off.
3. **Money rules:** the capital-step state machine and C3 approvals; kill criteria (sleeve, memecoin, recon 24 h, portfolio DD 25%).
4. **Live monitoring:** decay (rolling 60-trade vs p5, CUSUM), daily health check, auto-downgrade of autonomous bots.
5. **Reconciliation hardening:** three-way recon, unconfirmed state, 24 h halt.
6. **Execution:** MT5 bridge/adapter and/or cTrader, MasterTradingBot port, resting broker-side stops, live config.
7. **Continuity and mobile:** fail-flat, UPS/4G, pull-the-plug drill, approvals/PWA polish.
8. **Verification and RUN windows:** drills, simulated breaches, parity, E2E scenario, micro-live windows, the 12-month clock, the exit demo.

## Entry criteria

These come from roadmap §2. They are enforced in code by the go-live preflight (P7-T011), which blocks funding, live modes and capital steps until each holds.

- [ ] ≥ 8 weeks of paper for each P1 sleeve through the real policy/risk/execution path (started P2 T2.80) — checked by P7-T011 / P7-T056
- [ ] Tax agent has answered investor vs trader-in-business (P3 T3.01) — recorded by P7-T001
- [ ] Venue registry marks each target venue/product `allowed`, AUSTRAC re-check < 90 days — P7-T003, P7-T046
- [ ] Runbooks drilled at least once (kill, keys leaked, server down with open positions, bad data, wallet drained) — P7-T044, P7-T045
- [ ] Phase 3 done (`opens_after: [3]`); P2 (gates, risk, engine, bots) done transitively

## Exit criteria

- [ ] At least one strategy live in a micro sub-account with all gates passed and the audit trail complete (P7-T057, P7-T059, P7-T064)
- [ ] Kill criteria and decay monitoring proven by simulated breaches (P7-T048, P7-T049)
- [ ] Weekly reviews logged for every live week (P7-T060)
- [ ] All Phase 7 tasks done or cancelled (cancelled only with a reason, e.g. the unchosen MT5/cTrader adapter, the optional Mini App)
- [ ] No open S1/S2 bugs or gaps in `tracking/phase-7/bugs/`

## Workstreams

| Workstream | Tasks |
|---|---|
| Your actions (USER) | P7-T001 tax decision · P7-T002 lawyer items · P7-T003 venue checks · P7-T004 FP Markets terms/route · P7-T005 Windows VPS · P7-T006 live accounts/sub-accounts · P7-T007 live keys · P7-T008 Travel Rule addresses · P7-T009 UPS + 4G · P7-T053 pull-the-plug drill · P7-T057 fund micro-live · P7-T058 approve bot promotions · P7-T060 weekly reviews · P7-T061 approve capital steps · P7-T063 12-month criteria |
| Build: entry checks & evidence | P7-T010 advice register · P7-T011 go-live preflight + drill log · P7-T012 gate core · P7-T013 paper tracking · P7-T014 report/API/D03 · P7-T015 weekly pack · P7-T016 review sign-off · P7-T017 reference distributions |
| Build: capital steps & kill criteria | P7-T018 step state machine · P7-T019 step approvals + UI · P7-T020 kill framework (shortfall, 60-trade Sharpe) · P7-T021 memecoin kills · P7-T022 portfolio DD 25% flatten · P7-T042 12-month report |
| Build: live monitoring & bots | P7-T023 decay (rolling + CUSUM) · P7-T024 daily health check · P7-T028 bot autonomous promotion (C3) · P7-T029 auto-downgrade |
| Build: reconciliation | P7-T025 three-way recon · P7-T026 unconfirmed state · P7-T027 24 h halt |
| Build: execution & continuity | P7-T030 resting broker-side stops · P7-T034 MT5 bridge · P7-T036 MT5 adapter · P7-T037 cTrader adapter · P7-T038 MasterTradingBot port |
| Build: approvals & mobile | P7-T039 approvals polish · P7-T040 PWA install/offline · P7-T041 Telegram Mini App (optional) |
| Ops | P7-T031 live engine config + secrets + alert routing · P7-T032 key audit job · P7-T033 dead-man fail-flat + UPS/4G · P7-T035 VPS deploy + hardening |
| Docs | P7-T043 live-trading runbooks |
| Verify | P7-T044, P7-T045 runbook drills · P7-T046 registry re-check gate · P7-T047 key/sub-account audit · P7-T048 kill-criteria sims · P7-T049 decay/downgrade sims · P7-T050 recon fault injection · P7-T051 MT5/cTrader parity · P7-T052 fail-flat/failover test · P7-T054 phone test · P7-T055 E2E scenario · P7-T064 exit demo |
| Run | P7-T056 paper/approve period · P7-T059 micro-live 4-week windows · P7-T062 start the 12-month clock |

## Critical path

P7-T010 → P7-T011 (preflight) ┐
P7-T012 → P7-T013 → P7-T014 (gate report) → P7-T056 (paper confirmed) ┤
P7-T043 → P7-T044 / P7-T045 (drills) ┤
P7-T003 → P7-T046; P7-T006 → P7-T007 → P7-T031 → P7-T047 ┤
P7-T009 + P7-T030 → P7-T033 → P7-T052 → P7-T053 ┤
P7-T001 ┘ → **P7-T057 fund micro-live** → P7-T059 (4-week window, with P7-T060 weekly reviews) → P7-T061 (first step) → **P7-T064 exit demo**

In parallel, these must be done before the exit demo:
- **Simulations:** P7-T017 → P7-T020 → P7-T048; P7-T023/T024 → P7-T029 → P7-T049.
- **Recon:** P7-T025 → P7-T026 → P7-T050.
- **Steps and promotion:** P7-T018 → P7-T019 → P7-T055.

**Shortest path to the first live trade** is roughly: preflight + gate report + drills + key audit + pull-the-plug, with the paper clock already elapsed from P2. The MT5/cTrader work (P7-T034–T038, T051) is **off** the critical path for crypto sleeves.

## Traceability

### Requirements → tasks

| Requirement | Tasks |
|---|---|
| R7.01 All §8 gates incl. harness extensions | P7-T012, P7-T013, P7-T014, P7-T017, P7-T055, P7-T057 |
| R7.02 Paper/approve period, tracking within tolerance | P7-T011, P7-T013, P7-T014, P7-T056 |
| R7.03 Weekly review | P7-T015, P7-T016, P7-T055, P7-T060 |
| R7.04 Live sub-accounts, trade-only IP-locked keys, no withdrawals, Travel Rule | P7-T003, P7-T006, P7-T007, P7-T008, P7-T011, P7-T031, P7-T032, P7-T045, P7-T047 |
| R7.05 Capital steps → 12-month review | P7-T018, P7-T019, P7-T022, P7-T042, P7-T046, P7-T055, P7-T057, P7-T059, P7-T061, P7-T062, P7-T063 |
| R7.06 Kill criteria | P7-T017, P7-T020, P7-T021, P7-T022, P7-T027, P7-T043, P7-T044, P7-T048 |
| R7.07 Live decay monitoring | P7-T017, P7-T023, P7-T024, P7-T029, P7-T049 |
| R7.08 Autonomous mode is C3 (per bot); approve mode first | P7-T019, P7-T028, P7-T029, P7-T039, P7-T049, P7-T055, P7-T058 |
| R7.09 Reconciliation hardening | P7-T025, P7-T026, P7-T027, P7-T043, P7-T050 |
| R7.10 MT5/cTrader adapters; MasterTradingBot as M0 strategies | P7-T004, P7-T005, P7-T034, P7-T035, P7-T036, P7-T037, P7-T038, P7-T051 |
| R7.11 Continuity: UPS + 4G, fail flat, resting stops | P7-T009, P7-T030, P7-T033, P7-T043, P7-T044, P7-T052, P7-T053 |
| R7.12 Approvals/mobile polish, ≤ 3 taps, PWA | P7-T039, P7-T040, P7-T041, P7-T054 |
| R7.13 Professional-advice items closed or deferred | P7-T001, P7-T002, P7-T003, P7-T004, P7-T010, P7-T011, P7-T046 |

### Roadmap ToDos → tasks

| ToDo | Tasks |
|---|---|
| T7.01 Tax agent decision recorded | P7-T001 |
| T7.02 Live accounts + sub-accounts per mandate | P7-T006 |
| T7.03 Live keys; Travel Rule addresses | P7-T007, P7-T008, P7-T047 |
| T7.04 Fund micro-live after the gate report | P7-T057 |
| T7.05 Weekly review signed off | P7-T015, P7-T016, P7-T060 |
| T7.06 Approve promotions (C3) and capital steps | P7-T019, P7-T028, P7-T029, P7-T058, P7-T061 |
| T7.07 Professional advice | P7-T002, P7-T003, P7-T010 |
| T7.08 FP Markets clauses; Windows VPS | P7-T004, P7-T005, P7-T035 |
| T7.09 UPS + 4G; pull-the-plug drill | P7-T009, P7-T053 |
| T7.10 12-month review | P7-T042, P7-T063 |
| T7.20 Gate report generator | P7-T012, P7-T013, P7-T014, P7-T017 |
| T7.21 Capital-step state machine + kill-criteria evaluators | P7-T018, P7-T019, P7-T020, P7-T021, P7-T022, P7-T027, P7-T055 |
| T7.22 Live decay monitoring jobs | P7-T017, P7-T023, P7-T024, P7-T029, P7-T049 |
| T7.23 Reconciliation hardening | P7-T025, P7-T026, P7-T027, P7-T050 |
| T7.24 MT5 bridge / cTrader adapter; MasterTradingBot port | P7-T034, P7-T035, P7-T036, P7-T037, P7-T038 |
| T7.25 Approvals/mobile polish; PWA; Mini App | P7-T039, P7-T040, P7-T041, P7-T054 |
| T7.40 Live engine config, secrets, alert routing | P7-T031, P7-T032, P7-T047 |
| T7.41 Dead-man fail-flat with 4G | P7-T030, P7-T033, P7-T052 |
| T7.60 All runbooks drilled | P7-T011, P7-T043, P7-T044, P7-T045 |
| T7.61 Simulated kill-criteria breaches | P7-T048, P7-T049 |
| T7.62 MT5/cTrader paper parity | P7-T051 |
| T7.63 Venue registry re-check < 90 days before each funding | P7-T003, P7-T011, P7-T046 |
| T7.80 Paper/approve period per strategy | P7-T056 |
| T7.81 Micro-live 4-week windows | P7-T059 |
| T7.82 12 months live → review | P7-T042, P7-T062 |

All 13 requirements and all 25 ToDos are covered. The exit demo (P7-T064) re-verifies every R7.xx.

## Cross-phase prerequisites

Other phases' roadmap IDs these tasks rely on (named in each task's *Context & references*; not in `depends_on`):

| From | IDs | Used by |
|---|---|---|
| P0 | T0.02 (UPS/4G ordered), T0.22 (`ops.venue_registry`), T0.23/R0.07 (WORM layer), T0.24/R0.08 (`mt_api`, C0–C3), T0.26 (PWA shell), T0.90 (first runbooks) | P7-T009, T010, T011, T014, T040, T043 |
| P1 | T1.29/R1.12 (recon jobs), T1.30/R1.13 (venue health + quarterly AUSTRAC task), T1.31 (alert channels) | P7-T003, T025, T031 |
| P2 | T2.80 (paper clock), T2.81 (weekly five-worst), T2.22/R2.21 (health check + decay baseline), T2.23 (kill/dead-man), T2.25/R2.32 (engine, restart epoch), T2.26 (TCA), T2.27 (validation harness), T2.31/T2.67/R2.48 (MasterTradingBot libraries + golden files), T2.32–T2.34/R2.53–R2.54 (UI, Telegram, bots), T2.90 (runbooks) | P7-T011–T029, T034–T039, T043–T044 |
| P3 | T3.01/R3.07 (tax agent engaged), T3.02 (2027 reform), T3.28/R3.11 (journal ↔ venue recon), T3.80 | P7-T001, T015, T025 |
| P5 | T5.01/T5.04 (vault/warm wallets registered), T5.90 (wallet-drained runbook), `curation.task` (PRO_ADVICE type) | P7-T008, T010, T045 (see P7-B011) |
| P6 | T6.28/R6.20–R6.22 (`mt_treasury` hold-and-earn, for capital after DD/12-month retirement), T6.23 (post-cutoff eval for LLM strategies) | P7-T012, T022 (see P7-B011) |

## Planning notes & risks

- **RUN items that outlast the phase:**
  - P7-T056 closes when one P1 sleeve passes paper (others keep running).
  - P7-T059 needs one full 4-week window.
  - P7-T062 only starts the 12-month clock. Completing the actual 12-month review isn't owned by any phase yet (P7-B012).
  - Capital steps after exit continue as standing operations.
- **Route choice:** P7-T004 decides MT5 vs cTrader. Cancel the unchosen adapter task (P7-T036 or P7-T037; with P7-T005/T034/T035 if not MT5). Cancelled items count as closed for dependencies and the exit check.
- **P2 overlap:** R2.21 already builds the health check and decay alerts on paper, and R2.53 builds auto-downgrade. Phase 7 tasks deliberately extend these to live fills, frozen reference distributions and the new triggers rather than rebuilding them.
- **Open S2 gaps block exit until resolved:**
  - **P7-B003:** capital-step semantics.
  - **P7-B004:** 4G failover vs IP-locked keys.
  - Both need your decision because they change money and key rules. The tasks carry proposed defaults.
- **Risks:**
  - **Live diverges from paper:** shortfall kill (P7-T020), small steps, weekly review.
  - **Temptation to override:** no discretionary paths; only flatten-and-halt with a reason, and every loosening is C3.
  - **Venue status changes:** the DAF starts 9 Apr 2027 and the ASIC 2:1 order expires 23 May 2027. Mitigations are the < 90-day re-check gate (P7-T046) and registry-change downgrades (P7-T029).
  - **Low-frequency sleeves:** these may never reach 60 trades during micro-live (P7-B016).
- **Uncertain:**
  - whether venues the registry allows actually offer native stop orders on spot. P7-T030 refuses live on venues without them, which could narrow the venue list;
  - FP Markets' algo clauses (P7-T004).
