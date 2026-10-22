---
phase: 7
title: Prove it, then go small-live
roadmap: docs/roadmap/phase-7-prove-and-go-live.md
status: in_progress
opens_after: [3]
force_open: false
hard_gate: true
started: 2026-10-22
completed: ""
doc_sync_status: n/a
updated: 2026-10-22
---

# Phase 7 · Prove it, then go small-live

## Summary

Only strategies that pass every gate on paper reach live money, in small sub-accounts with withdrawals disabled; each bot starts live at its **starting allocation** (set in its strategy settings, default A$2,000), steps up by **+25% of the current allocation after 4 consecutive clean weeks** (each step C3), steps back on warnings and halts, and stops on pre-written kill criteria ([roadmap](../../docs/roadmap/phase-7-prove-and-go-live.md), [16 §2.4–2.6](../../docs/16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot), [14 §7](../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7)). All exchange traffic leaves through one static Sydney exit-node IP ([16 §3.2](../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys)). Phase 7 is **hard-gated**: it opens after P3; items that need P5/P6 deliverables carry their own task dependencies ([17 §D P7-B011](../../docs/17-decisions-register.md#d-other-decisions)).

The work is organised in nine workstreams:

1. **Entry checks and your pre-live actions:** tax decision, advice, venue checks, accounts, keys, Travel Rule, UPS/4G, the egress VM.
2. **Evidence:** the gate report (gate profile, 16 §2.4), paper/HITL tracking, reference distributions, weekly review pack and sign-off.
3. **Money rules:** the capital-step state machine and C3 approvals; kill criteria (sleeve, memecoin, recon 24 h); two-stage system drawdown (10% no new entries, 25% flatten + 30-day lock).
4. **Live monitoring:** decay (rolling 60-trade / 26-week vs p5, CUSUM, 5 losses → HITL), daily health check (halt the bot), auto-downgrade.
5. **Reconciliation hardening:** three-way recon at the 16 §2.9 defaults, unconfirmed state, 24 h halt.
6. **Execution:** MT5 bridge/adapter and/or cTrader, MasterTradingBot port, resting venue stops, live config, Windows VPS hardening.
7. **Continuity, egress and mobile:** exit-node tunnel, three-layer dead-man with UPS, failover and pull-the-plug drills, approvals/PWA polish.
8. **Phase 7 API/UI and stress:** the Phase 7 catalogue in `mt_api`, D06 Live / D03 Go-live, the D06 Stress tab and the pre-funding stress replay.
9. **Verification and RUN windows:** drills, simulated breaches, parity, E2E scenario, micro-live windows, the exit demo.

## Entry criteria

These come from roadmap §2. They are enforced in code by the go-live preflight (P7-T011), which blocks funding, live modes and capital steps until each holds.

- [ ] Phase 3 done (`opens_after: [3]`, `hard_gate: true`); P2 done transitively; P5/P6 deliverables are task-level dependencies only (17 §D P7-B011)
- [ ] ≥ 8 weeks of paper for each P1 sleeve through the real policy/risk/execution path (started P2 T2.80, P2-T180); other bots per their gate profile (≥ 8 weeks and ≥ 50 trades by default) — checked by P7-T011 / P7-T056
- [ ] Tax agent has answered investor vs trader-in-business (P3 T3.01) — recorded by P7-T001
- [ ] Venue registry marks each target venue/product `allowed`, AUSTRAC re-check < 90 days — P7-T003, P7-T046
- [ ] Runbooks drilled at least once (kill, keys leaked, server down with open positions, bad data; wallet drained only if a hot/burner wallet exists) — P7-T044, P7-T045

## Exit criteria

- [ ] At least one strategy live in a micro sub-account with all gates passed and the audit trail complete (P7-T057, P7-T059, P7-T064)
- [ ] Kill criteria and decay monitoring proven by simulated breaches (P7-T048, P7-T049, P7-T021)
- [ ] Weekly reviews logged for every live week (P7-T060)
- [ ] Micro-live stable (first 4-week window complete, P7-T059); the 12-month review is scheduled as a recurring calendar review (P7-T042, P7-T063), not awaited
- [ ] All Phase 7 tasks done or cancelled (cancelled only with a reason, e.g. the unchosen MT5/cTrader route, the optional Mini App, P7-T062)
- [ ] No open S1/S2 bugs or gaps in `tracking/phase-7/bugs/`

## Workstreams

| Workstream | Tasks |
|---|---|
| Your actions (USER) | P7-T001 tax decision · P7-T002 lawyer items · P7-T003 venue checks · P7-T004 FP Markets terms/route · P7-T005 Windows VPS · P7-T006 live accounts/sub-accounts · P7-T065 egress exit-node VM · P7-T007 live keys (allow-listed to the exit-node IP) · P7-T008 Travel Rule addresses · P7-T009 UPS + 4G · P7-T053 pull-the-plug drill · P7-T057 fund the starting allocation · P7-T058 approve bot promotions · P7-T060 weekly reviews · P7-T061 approve capital steps · P7-T063 diary the recurring 12-month review |
| Build: entry checks & evidence | P7-T010 advice register · P7-T011 go-live preflight + drill log · P7-T012 gate core · P7-T013 paper/HITL tracking · P7-T014 report/API/D03 · P7-T015 weekly pack · P7-T016 review sign-off · P7-T017 reference distributions |
| Build: capital steps & kill criteria | P7-T018 step state machine · P7-T019 step approvals + `CapitalStepCard` · P7-T020 kill framework (shortfall, sleeve 60-trade Sharpe) · P7-T021 memecoin kills (needs P5-T036) · P7-T022 system drawdown stages live · P7-T042 recurring 12-month review schedule + report |
| Build: live monitoring & bots | P7-T023 decay (rolling, CUSUM, losses) · P7-T024 daily health check per bot · P7-T028 bot autonomous promotion (C3) · P7-T029 auto-downgrade |
| Build: reconciliation | P7-T025 three-way recon · P7-T026 unconfirmed state · P7-T027 24 h halt |
| Build: execution | P7-T030 resting venue stops · P7-T034 MT5 bridge · P7-T036 MT5 adapter · P7-T037 cTrader adapter · P7-T038 MasterTradingBot port |
| Build: Phase 7 API/UI & stress | P7-T067 Phase 7 API catalogue + D06 Live / D03 Go-live · P7-T068 D06 Stress tab + `risk.stress.run` |
| Build: approvals & mobile | P7-T039 approvals polish · P7-T040 PWA install/offline · P7-T041 Telegram Mini App (optional) |
| Ops | P7-T031 live engine config + secrets + alert routing · P7-T032 key audit job · P7-T033 dead-man fail-flat + UPS · P7-T035 VPS hardening + bridge deploy (T7.43) · P7-T066 exit-node tunnel + egress check |
| Docs | P7-T043 live-trading runbooks |
| Verify | P7-T044, P7-T045 runbook drills · P7-T046 registry re-check gate · P7-T047 live key audit (T7.65) · P7-T048 kill-criteria sims · P7-T049 decay/downgrade sims · P7-T050 recon fault injection · P7-T051 MT5/cTrader parity · P7-T052 failover drill (T7.64) · P7-T054 phone test · P7-T055 E2E scenario · P7-T069 stress replay before funding (T7.66) · P7-T064 exit demo |
| Run | P7-T056 paper/HITL period · P7-T059 micro-live 4-week windows · ~~P7-T062~~ cancelled (12-month review is a standing operation) |

## Critical path

P7-T010 → P7-T011 (preflight) ┐
P7-T012 → P7-T013 → P7-T014 (gate report) → P7-T056 (paper confirmed) ┤
P2 stress placeholder → P7-T068 → P7-T069 (stress replay) ┤
P7-T043 → P7-T044 / P7-T045 (drills) ┤
P7-T003 → P7-T046; P7-T003 → P7-T006 → P7-T065 → P7-T007 → P7-T047 (live key audit, also needs P7-T031/T032/T066) ┤
P7-T009 → P7-T066 (tunnel); P7-T009 + P7-T030 → P7-T033 → P7-T052 (failover) → P7-T053 ┤
P7-T001 ┘ → **P7-T057 fund the starting allocation** → P7-T059 (4-week window, with P7-T060 weekly reviews) → P7-T061 (first step) → **P7-T064 exit demo**

In parallel, these must be done before the exit demo:
- **Simulations:** P7-T017 → P7-T020 → P7-T048; P7-T023/T024 → P7-T029 → P7-T049; P7-T021 (memecoin, waits on P5-T036).
- **Recon:** P7-T025 → P7-T026 → P7-T050.
- **Steps, promotion and UI:** P7-T018 → P7-T019 → P7-T055; P7-T019 + P7-T020 + P7-T022 → P7-T067.

**Shortest path to the first live trade** is roughly: preflight + gate report + stress replay + drills + exit node and key audit + failover/pull-the-plug, with the paper clock already elapsed from P2. The MT5/cTrader work (P7-T005, P7-T034–T038, P7-T051) is **off** the critical path for crypto sleeves. **Build first, keys last:** every BUILD/OPS item is keyless (mocks, fixtures, testnet/sandbox, demo); only P7-T047 (live key audit), P7-T057 and P7-T059 touch live keys or money.

## Traceability

### Requirements → tasks

| Requirement | Tasks |
|---|---|
| R7.01 All §8 gates incl. harness extensions (DSR ≥ 0.95, safety drills) | P7-T011, P7-T012, P7-T013, P7-T014, P7-T017, P7-T055, P7-T057, P7-T064 |
| R7.02 Paper/HITL period (≥ 8 weeks and ≥ 50 trades; class overrides), tracking within tolerance | P7-T011, P7-T013, P7-T014, P7-T056, P7-T064 |
| R7.03 Weekly review | P7-T015, P7-T016, P7-T055, P7-T060, P7-T064 |
| R7.04 Live sub-accounts, trade-only IP-locked keys, no withdrawals, Travel Rule | P7-T003, P7-T006, P7-T007, P7-T008, P7-T011, P7-T031, P7-T032, P7-T045, P7-T047, P7-T064 |
| R7.05 Capital steps (starting allocation, +25% of current, step-down); 12-month review recurring | P7-T018, P7-T019, P7-T022, P7-T042, P7-T046, P7-T055, P7-T057, P7-T059, P7-T061, P7-T063, P7-T064 |
| R7.06 Kill criteria; two-stage system drawdown | P7-T017, P7-T020, P7-T021, P7-T022, P7-T027, P7-T043, P7-T044, P7-T048, P7-T064 |
| R7.07 Live decay monitoring, one meaning per signal | P7-T017, P7-T023, P7-T024, P7-T029, P7-T049, P7-T064 |
| R7.08 Modes per bot; HITL → autonomous is C3; every bot starts live in `hitl` | P7-T019, P7-T028, P7-T029, P7-T039, P7-T049, P7-T055, P7-T058, P7-T064 |
| R7.09 Reconciliation hardening (16 §2.9) | P7-T025, P7-T026, P7-T027, P7-T043, P7-T050, P7-T064 |
| R7.10 MT5/cTrader adapters; MasterTradingBot as M0 strategies; hardened VPS | P7-T004, P7-T005, P7-T034, P7-T035, P7-T036, P7-T037, P7-T038, P7-T051, P7-T064 |
| R7.11 Continuity: UPS + 4G, three-layer dead-man, resting stops | P7-T009, P7-T030, P7-T033, P7-T043, P7-T044, P7-T052, P7-T053, P7-T064, P7-T066 |
| R7.12 Approvals/mobile polish, ≤ 3 taps, PWA | P7-T039, P7-T040, P7-T041, P7-T054, P7-T064 |
| R7.13 Professional-advice items closed or deferred | P7-T001, P7-T002, P7-T003, P7-T004, P7-T010, P7-T011, P7-T046, P7-T064 |
| R7.14 Static AU egress via the exit node | P7-T007, P7-T009, P7-T011, P7-T032, P7-T043, P7-T047, P7-T052, P7-T064, P7-T065, P7-T066 |
| R7.15 Phase 7 state in the API and UI | P7-T014, P7-T016, P7-T019, P7-T064, P7-T067 |
| R7.16 D06 Stress tab + `risk.stress.run`, run before live capital | P7-T064, P7-T068, P7-T069 |

### Roadmap ToDos → tasks

| ToDo | Tasks |
|---|---|
| T7.01 Tax agent decision recorded | P7-T001 |
| T7.02 Live accounts + sub-accounts per mandate | P7-T006 |
| T7.03 Live keys; Travel Rule addresses | P7-T007, P7-T008 |
| T7.04 Set the starting allocation and fund after the gate report | P7-T057 |
| T7.05 Weekly review signed off | P7-T015, P7-T016, P7-T060 |
| T7.06 Approve promotions (C3) and capital steps | P7-T019, P7-T028, P7-T029, P7-T058, P7-T061 |
| T7.07 Professional advice | P7-T002, P7-T003, P7-T010 |
| T7.08 FP Markets clauses; Windows VPS | P7-T004, P7-T005 |
| T7.09 UPS + 4G; pull-the-plug drill | P7-T009, P7-T053 |
| T7.10 12-month review in your calendar as a recurring review | P7-T042, P7-T063 |
| T7.11 Egress VM; its IP allow-listed on every live key | P7-T065, P7-T007 |
| T7.20 Gate report generator | P7-T012, P7-T013, P7-T014, P7-T017 |
| T7.21 Capital-step state machine + kill-criteria evaluators | P7-T018, P7-T019, P7-T020, P7-T021, P7-T022, P7-T027, P7-T055 |
| T7.22 Live decay and health jobs | P7-T017, P7-T023, P7-T024, P7-T029, P7-T049 |
| T7.23 Reconciliation hardening | P7-T025, P7-T026, P7-T027, P7-T050 |
| T7.24 MT5 bridge / cTrader adapter; MasterTradingBot port | P7-T034, P7-T035, P7-T036, P7-T037, P7-T038 |
| T7.25 Approvals/mobile polish; PWA; Mini App | P7-T039, P7-T040, P7-T041, P7-T054 |
| T7.26 Phase 7 API and UI | P7-T067, P7-T014, P7-T016, P7-T019 |
| T7.27 D06 Stress tab + `risk.stress.run` | P7-T068 |
| T7.40 Live engine config, secrets, alert routing | P7-T031, P7-T032, P7-T047 |
| T7.41 Dead-man fail-flat with 4G | P7-T030, P7-T033, P7-T052 |
| T7.42 Exit-node tunnel; egress check on the static IP | P7-T066 |
| T7.43 Windows VPS hardening for MT5 | P7-T035 |
| T7.60 All runbooks drilled | P7-T011, P7-T043, P7-T044, P7-T045 |
| T7.61 Simulated kill-criteria breaches | P7-T048, P7-T049 |
| T7.62 MT5/cTrader paper parity | P7-T051 |
| T7.63 Venue registry re-check < 90 days before each funding | P7-T003, P7-T011, P7-T046 |
| T7.64 Failover drill (4G via tunnel; tunnel down) | P7-T052 |
| T7.65 Live key audit | P7-T047 |
| T7.66 Stress replay before the first funding | P7-T069 |
| T7.80 Paper/HITL period per bot | P7-T056 |
| T7.81 Micro-live 4-week windows | P7-T059 |
| T7.82 12 months live → review | Deferred: a recurring calendar review after P7 closes ([roadmap README §10](../../docs/roadmap/README.md#10-standing-operations-recurring-outside-the-phases)); P7-T062 cancelled, scheduling in P7-T042 |

All 16 requirements and all 33 ToDos are covered (T7.82 deliberately deferred to standing operations). The exit demo (P7-T064) re-verifies every R7.xx.

## Cross-phase prerequisites

These are now explicit `depends_on` entries (existing task IDs) in the Phase 7 task files:

| From | Tasks | Used by |
|---|---|---|
| P0 | P0-T012 (UPS/4G ordered), P0-T025 (`ops.venue_registry`), P0-T050 (app shell), P0-T052 (D16 security/keys) | P7-T009, T010, T040, T032 |
| P1 | P1-T041/T042 (venue recon), P1-T045 (alert fan-out), P1-T071 (egress check) | P7-T025, T031, T011, T066 |
| P2 | P2-T010 (layered policy), P2-T012 (system drawdown stages), P2-T015 (portfolio risk), P2-T016 (registry check), P2-T021 (engine), P2-T027 (epoch IDs + restart recon), P2-T029 (TCA), P2-T031 (kill switch), P2-T032 (dead-man layer 1), P2-T072/T073/T074 (dead-man layers 2–3, clean restart), P2-T033 (modes), P2-T034 (decay/health on paper), P2-T035 (Telegram C3), P2-T037 (bot modes + auto-downgrade), P2-T039 / P2-T149 (approval cards/queue), P2-T042 (D06 venues), P2-T043 (Stress placeholder), P2-T068 (runbooks), P2-T103 (PIT datasets), P2-T108/T110/T114 (trial counter, DSR, gate evaluator), P2-T132/T133 (MasterTradingBot template + golden files), P2-T143 (D03 Gates), P2-T150 (weekly five-worst report), P2-T180 (paper clock) | P7-T003, T010–T015, T018–T026, T028–T031, T033, T036–T039, T043, T056, T068 |
| P3 | P3-T001 (tax agent), P3-T012 (`ops.wallets`), P3-T034 (journal ↔ venue recon), P3-T038 (minimal `curation.task`) | P7-T001, T008, T015, T025, T010 |
| P5 | P5-T036 (`token_risk_report` rug labels) | P7-T021 only (memecoin sleeve) |
| P6 | none required: hold-and-earn falls back to stables on the venue + a USER task; LLM post-cutoff results (P6-T017) are read only when an LLM strategy exists | — |

P2 R2.56 is now P2-T072 (deadman sidecar), P2-T073 (venue timers + resting stops) and P2-T074 (clean restart), `depends_on` of P7-T030, P7-T033 and P7-T026.

## Planning notes & risks

- **Decisions applied (2026-10-22 alignment):** gate profile and paper/HITL period (16 §2.4), clean week and capital steps from a per-bot starting allocation (16 §2.5, default A$2,000), decay/kill meanings (16 §2.6), two-stage system drawdown (16 §2.1), reconciliation defaults (16 §2.9), three-layer dead-man (16 §3.1), static AU egress via the exit node (16 §3.2), modes `paper`/`hitl`/`autonomous` per bot (17 §B), Windows VPS baseline (07 §5.1). All gaps P7-B001–B016 are closed with doc evidence.
- **RUN items that outlast the phase:**
  - P7-T056 closes when one P1 sleeve passes paper (others keep running).
  - P7-T059 needs one full 4-week window.
  - Capital steps after exit and the 12-month review are standing operations ([roadmap README §10](../../docs/roadmap/README.md#10-standing-operations-recurring-outside-the-phases)).
- **Route choice:** P7-T004 decides MT5 vs cTrader. cTrader only → cancel P7-T005, P7-T034, P7-T035, P7-T036; MT5 only → cancel P7-T037. Cancelled items count as closed for dependencies and the exit check.
- **P2 overlap:** P2 builds decay/health signals (P2-T034), auto-downgrade (P2-T037), both system drawdown stages (P2-T012) and the dead-man layers on paper; Phase 7 tasks extend them to live venues, frozen references and the new triggers rather than rebuilding them.
- **Risks:**
  - **Live diverges from paper:** shortfall warning/kill (P7-T020), small steps, weekly review.
  - **Temptation to override:** no discretionary paths; only flatten-and-halt with a reason, and every loosening is C3.
  - **Venue status changes:** the DAF starts 9 Apr 2027 and the ASIC 2:1 order expires 23 May 2027; mitigated by the < 90-day re-check gate (P7-T046) and registry-change downgrades (P7-T029).
  - **Exit node is a single point of failure:** tunnel down → venue timers + resting stops only (P7-T066, P7-T052, runbook `egress-tunnel-down.md`).
- **Uncertain:**
  - whether venues the registry allows offer native stop orders and cancel-after timers on spot (P7-T003 records it; P7-T030 refuses live where stops are missing);
  - FP Markets' algo clauses (P7-T004);
  - a free-tier Sydney VM with a static IP (U in 16 §3.2; P7-T065 records it);
  - exact date windows for the four stress scenarios (U; P7-T068 confirms them from recorded data).
