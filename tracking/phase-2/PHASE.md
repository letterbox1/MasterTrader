---
phase: 2
title: Strategy framework, risk manager & research lab
roadmap: docs/roadmap/phase-2-strategies-risk-lab.md
status: not_started
opens_after: [1]
force_open: false
started: ""
completed: ""
doc_sync_status: n/a
updated: 2026-10-21
---

# Phase 2 · Strategy framework, risk manager & research lab

## Summary

Phase 2 makes MasterTrader a trading platform: you can create **any strategy type on any timeframe**, backtest it with **measured costs**, validate it, and run it on **paper behind the risk manager**, controlled from the web UI and Telegram. The P1 paper clock starts at the end of the phase. ([roadmap](../../docs/roadmap/phase-2-strategies-risk-lab.md))

The phase is planned in two parts:
- **Part A (this file, P2-T001–T099, P2-B001–B049):** M0 strategy framework (base classes, manifest + never-build validator, registry, lifecycle, templates), M11 risk manager (policy, ceilings, limits, sizing, sleeves/netting, portfolio, venue registry + 2×, RiskGate, ladder, change control, kill, dead-man, modes, health/decay), M12 execution (engine, STP, testnet + Alpaca/OANDA/IG adapters, epoch IDs + reconciliation, maker-first/TWAP, TCA, shadow), trading bots + HITL/autonomous + Telegram approval cards, Telegram v1, D06 Risk + D03 Bots tab + shared `ApprovalCard`/`DiffView`/`C3Flow`, ops, the related verification, all USER items and the runbooks.
- **Part B (P2-T101+, P2-B050+):** M7 lab + validation harness, M6 features, M21 tier A, MasterTradingBot shared libraries, D01/D03 (non-bot)/D04/D05, parity and tier-A/signal→order latency, the paper-clock RUN items and the phase exit demo. See the Part B section below.

Build order (roadmap risk mitigation): **M11 + M12 + one template first**, then bots/HITL and UI; lab extensions can trail by a week.

## Entry criteria

- [ ] Phase 1 exit criteria met; `dq.status.*` and measured costs (`cost.*`) are flowing (P1 R1.10, R1.11)
- [ ] Testnet/practice **trade-only** keys exist (T2.03 → P2-T001)
- [ ] P0 command layer with C0–C3/Kill + TOTP, WORM audit tables and `ops.venue_registry` seed are live (P0 R0.06–R0.08)
- [ ] Telegram bot (alerts) and ntfy from P1 are working (P1 R1.14)

## Exit criteria

- [ ] 1. Create a strategy from a template, from code and by "describe it"; backtest with measured costs; the validation report shows all harness sections.
- [ ] 2. Run it on paper behind M11; an approve-mode (HITL) order is approved from Telegram.
- [ ] 3. Kill drill passes from the phone; a C3 loosening needs TOTP + cool-down.
- [ ] 4. The P1 paper clock has started.
- [ ] All Phase 2 tasks (Part A and Part B) are done or cancelled.
- [ ] No open S1/S2 bugs or gaps in Phase 2.

## Workstreams

| Workstream | Tasks |
|---|---|
| Your actions (USER) | P2-T001 keys · P2-T002 MasterTradingBot inputs · P2-T048 policy + ceilings · P2-T049 sleeves · P2-T050 first manifests · P2-T064 kill drill · P2-T065 C3 loosening · P2-T066 first bots + HITL approval · P2-T067 start paper clock |
| Build · M0 strategy framework | P2-T003 base classes · P2-T004 manifest · P2-T005 never-build · P2-T006 registry · P2-T007 lifecycle · P2-T008, P2-T009 templates · P2-T030 shadow mode |
| Build · M11 risk manager | P2-T010 policy · P2-T011 ceilings file · P2-T012 limits · P2-T013 sizing · P2-T014 sleeves/netting · P2-T015 portfolio · P2-T016 venue registry + 2× · P2-T017 RiskGate · P2-T018 ladder · P2-T019 change control · P2-T020 mt_api surface · P2-T031 kill · P2-T032 dead-man · P2-T033 modes/approvals · P2-T034 health/decay |
| Build · M12 execution | P2-T021 engine · P2-T022 STP · P2-T023 testnet venues · P2-T024 Alpaca · P2-T025 OANDA · P2-T026 IG · P2-T027 epoch IDs + reconcile · P2-T028 maker-first/TWAP · P2-T029 TCA |
| Build · bots, HITL & Telegram | P2-T035 Telegram v1 + C3 · P2-T036 bot model · P2-T037 bot modes/downgrade · P2-T038 approvals API + `ApprovalCard` · P2-T039 Telegram approval cards · P2-T040 bot commands · P2-T041 D03 Bots tab |
| Build · UI (D06) | P2-T042 D06 overview · P2-T043 D06 policy/events/changes |
| Ops | P2-T044 containers + gVisor · P2-T045 secrets + key audit · P2-T046 MLflow · P2-T047 Grafana |
| Verify | P2-T051 golden/property · P2-T052 no-bypass · P2-T053 C3 · P2-T054 kill/dead-man drills · P2-T055 restart-duplicate · P2-T056 STP audit · P2-T057 adapter conformance · P2-T058 latency (risk, kill) · P2-T059 degraded modes · P2-T060 decay/ladder/downgrade · P2-T061 bot scenarios · P2-T062 viewport (D06, Bots) · P2-T063 Part A end-to-end flows |
| Docs | P2-T068 runbooks |
| Gaps | P2-B001 … P2-B014 |

## Part B (lab, features, tier A, UI)

_Merged from the Part B planner (P2-T101+, P2-B050+)._

For the main agent to merge into `tracking/phase-2/PHASE.md`. Part B owns task IDs P2-T101–T199 and gap IDs P2-B050–B099. Part A (P2-T001–T099) owns M0, M11, M12, bots/HITL/Telegram, D06, the USER/OPS items and the runbooks.

### Workstreams

| Workstream | Tasks |
|---|---|
| Lab core (M7): jobs, costs, data, engines, tracking | P2-T101, P2-T102, P2-T103, P2-T104, P2-T105, P2-T106, P2-T107, P2-T117 |
| Validation harness (M7) | P2-T108, P2-T109, P2-T110, P2-T111, P2-T112, P2-T113, P2-T114, P2-T115 |
| Sandbox + LLM strategy generator (M7) | P2-T116 |
| Core features (M6) | P2-T120, P2-T121, P2-T122, P2-T123 |
| Tier A (M21) | P2-T125, P2-T126, P2-T127, P2-T128 |
| MasterTradingBot shared libraries | P2-T130, P2-T131, P2-T132 |
| UI: shared components | P2-T140, P2-T141 |
| UI: D01 Cockpit | P2-T142 |
| UI: D03 Strategies (registry, detail, builder; not Bots) | P2-T143, P2-T144 |
| UI: D04 Research Lab | P2-T145, P2-T146 |
| UI: D05 Execution + web approvals queue | P2-T147, P2-T148, P2-T149 |
| Reports | P2-T150 |
| Verify | P2-T133, P2-T160, P2-T161, P2-T162, P2-T163, P2-T164, P2-T165, P2-T166, P2-T167, P2-T168 |
| Run | P2-T180 (start the P1-sleeve paper clock; completion checked in P7 T7.80), P2-T182 |
| Phase exit demo | P2-T199 |
| Gaps (docs) | P2-B050 (S2), P2-B051 (S2), P2-B052, P2-B053, P2-B054, P2-B055, P2-B056, P2-B057, P2-B058 (S3), P2-B059, P2-B060 (S4) |

Totals: 52 tasks (39 BUILD, 11 VERIFY, 2 RUN) and 11 gap items. Sizes: 8 L, 33 M, 10 S, 1 XS. No XL.

### Critical path

Weighted by size (part B only):

P2-T101 → P2-T102 → P2-T105 → P2-T106 → P2-T107 → P2-T108 → P2-T110 → P2-T114 → P2-T117 → P2-T145 → P2-T146 → P2-T163 → P2-T199

The paper-clock branch (which unlocks P7) is: … → P2-T114 → P2-T117 → P2-T143 → P2-T180 → P2-T199, plus P2-T161 (backtest ↔ paper parity) → P2-T180.

Part-A items on the same path: M0 base classes/manifest/templates (T2.20/T2.21) before P2-T104/T105; the M11 pre-trade layer (T2.22) and paper engine (T2.25) before P2-T105 parity, P2-T161 and P2-T180; the sandbox container + gVisor (T2.40) before P2-T116/T165; MLflow artefact storage (T2.41) before P2-T107/T127; the `ApprovalCard`/approvals API (currently P2-T038) before P2-T149. Ship order suggested by roadmap §7: one template through truth backtest + validation first; the D04 polish and the generator can trail by a week.

### Traceability

#### Requirements → tasks (part B)

| Requirement | Tasks |
|---|---|
| R2.01 | P2-T105, P2-T161, P2-T199 (part A owns the base class) |
| R2.02 | P2-T132 (deterministic rule-based template), P2-T144 (builder) — other templates are part A |
| R2.03 | P2-T144 (builder resolution checks) — framework is part A |
| R2.04 | P2-T143, P2-T144 (manifest fields shown/enforced in UI) — schema is part A |
| R2.05 | P2-T144 (builder refusal display) — validator is part A |
| R2.06 | P2-T114 (gate evaluator), P2-T143, P2-T166, P2-T180, P2-T199 — state machine is part A |
| R2.07 | P2-T115 (sweeps, A/B on identical data) — shadow mode is part A |
| R2.13 | P2-T148 (manual sleeve ticket UI) — sleeves are part A |
| R2.20 | P2-T149 (web approvals) — mode routing is part A |
| R2.34 | P2-T147 (TCA tab) — TCA computation is part A |
| R2.40 | P2-T101, P2-T102, P2-T104, P2-T105, P2-T106, P2-T117, P2-T145, P2-T146, P2-T161, P2-T166, P2-T167, P2-T199 |
| R2.41 | P2-T102, P2-T103, P2-T104, P2-T105, P2-T164 |
| R2.42 | P2-T102, P2-T106, P2-T108, P2-T109, P2-T110, P2-T111, P2-T114, P2-T143, P2-T146, P2-T164, P2-T166, P2-T199 |
| R2.43 | P2-T112, P2-T113, P2-T114, P2-T146, P2-T160, P2-T199 |
| R2.44 | P2-T101, P2-T107, P2-T115, P2-T117, P2-T145, P2-T164, P2-T167 |
| R2.45 | P2-T116, P2-T144, P2-T146, P2-T165, P2-T166, P2-T167, P2-T199 |
| R2.46 | P2-T120, P2-T121, P2-T122, P2-T123 |
| R2.47 | P2-T125, P2-T126, P2-T127, P2-T128, P2-T162, P2-T199 |
| R2.48 | P2-T130, P2-T131, P2-T132, P2-T133, P2-T199 |
| R2.50 | P2-T117, P2-T140, P2-T141, P2-T142, P2-T143, P2-T144, P2-T145, P2-T146, P2-T147, P2-T148, P2-T163, P2-T166, P2-T168, P2-T199 (D06 is part A) |
| R2.51 | P2-T140, P2-T149, P2-T168, P2-T199 (Telegram side is part A) |
| R2.54 | P2-T149 (web side only) — bots/HITL are part A |
| R2.N1 | P2-T128, P2-T162 (tier A p99 < 50 µs; signal → order p99 < 5 ms), P2-T199 — risk p99 < 1 ms and kill < 1 s are part A |

#### Roadmap ToDos → tasks (part B)

| ToDo | Tasks |
|---|---|
| T2.27 | P2-T101, P2-T102, P2-T103, P2-T104, P2-T105, P2-T106, P2-T107, P2-T108, P2-T109, P2-T110, P2-T111, P2-T112, P2-T113, P2-T114, P2-T115, P2-T117, P2-T164, P2-T166, P2-T167 |
| T2.28 | P2-T116, P2-T165 |
| T2.29 | P2-T120, P2-T121, P2-T122, P2-T123 |
| T2.30 | P2-T125, P2-T126, P2-T127, P2-T128 |
| T2.31 | P2-T130, P2-T131, P2-T132 |
| T2.32 | P2-T117, P2-T140, P2-T141, P2-T142, P2-T143, P2-T144, P2-T145, P2-T146, P2-T147, P2-T148, P2-T149, P2-T166, P2-T168 (D06 + ApprovalCard/approvals sheet are part A) |
| T2.64 | P2-T160 |
| T2.65 | P2-T161 |
| T2.66 | P2-T162 (tier A + signal → order; risk-check benchmark is part A) |
| T2.67 | P2-T133 |
| T2.68 | P2-T163 (D01, D03, D04, D05; D06 is part A) |
| T2.80 | P2-T180 (start only; ≥ 8-week completion checked in P7 T7.80) |
| T2.81 | P2-T150, P2-T182 |
| Exit criteria 1–4 | P2-T199 (with part A evidence for criteria 2–3) |

### Planning notes & risks (part B)

- **Overlap resolved with part A:** `ApprovalCard`, approvals API and top-bar sheet (part A, currently P2-T038), `KillSwitchButton` wiring (P2-T042) and `DiffView`/`C3Flow` (P2-T043) are built once by part A and reused by P2-T140/T141/T143/T149. Flatten-and-halt uses part A's `position.close {halt, reason}` (P2-T020). `RiskPreview` is built in P2-T140 and must be the one part A's `ApprovalCard` embeds; agree props early.
- **S2 gaps to settle before P2-T110/T112 start:** P2-B050 (DSR threshold) and P2-B051 (freqtrade GPL route; default clean-room re-implementation).
- **Defaults chosen where docs are silent** (configurable, documented in the gaps): `regime_v1` price-based regimes (P2-B055), outcome labels for tier A (P2-B057), walk-forward 24m/3m folds, K = 5 purged folds with 1% embargo, 2,000 permutations, 5,000 block-bootstrap resamples, complexity penalty λ = 0.05 Sharpe per free parameter.
- **Risk:** truth backtests over L2 are slow; the 2 h job cap and worker caps keep the engine's cores free (P2-T167 verifies engine SLOs under lab load).
- **Risk:** MasterTradingBot golden files depend on the USER item T2.04 (part A, currently P2-T002); P2-T130 skips goldens with an explicit 'awaiting T2.04' marker that P2-T133 must clear.

### Cross-phase prerequisites (part B)

- P0: T0.22 (`mt_store`, `pit(as_of)`, Parquet helpers), T0.23 (WORM), T0.24 (`mt_api` command bus, confirmation levels, WS), T0.26 (web app, component library v0), T0.41 (NATS, MLflow, LiteLLM), T0.45 (gateway role keys/budgets), T0.64 (Playwright matrix in CI).
- P1: T1.21/T1.22 (bars, Parquet recording, backfills), T1.27 (DQ status), T1.28 (cost service → measured costs), T1.29 (reconciliation), T1.32 (D02/D07 and instrument finest-resolution metadata).
- Downstream: P6 (R6.14 distillation reuses P2-T125–T128; T6.23 LLM-signal post-cutoff evaluation plugs into P2-T114), P7 (T7.80 checks the paper clock started by P2-T180).

## Critical path

P2-T010 → P2-T012 → P2-T014 → P2-T015 → P2-T017 → P2-T021 → P2-T033 → P2-T037 → P2-T039 → P2-T061 → P2-T066 → P2-T067 (paper clock).

Parallel spines: P2-T004 → P2-T008 → P2-T050 (manifests, feeds Part B validation); P2-T017 → P2-T031 → P2-T032 → P2-T054 → P2-T064 (kill/dead-man); P2-T019 → P2-T043 → P2-T053 → P2-T065 (C3); P2-T021 → P2-T022 → P2-T023…T026 → P2-T057 (venues).

## Traceability

| Requirement | Tasks |
|---|---|
| R2.01 | P2-T003, P2-T021 · parity test: Part B |
| R2.02 | P2-T008, P2-T009 · deterministic rule-based template: Part B |
| R2.03 | P2-T003, P2-T008, P2-T009 |
| R2.04 | P2-T004, P2-T006, P2-T050 |
| R2.05 | P2-T005 |
| R2.06 | P2-T006, P2-T007 |
| R2.07 | P2-T030 (shadow mode) · sweeps + A/B: Part B · see P2-B014 |
| R2.10 | P2-T017, P2-T020, P2-T021, P2-T051, P2-T052, P2-T063 |
| R2.11 | P2-T010, P2-T015, P2-T020, P2-T043 |
| R2.12 | P2-T013, P2-T051 |
| R2.13 | P2-T014, P2-T049, P2-T051 |
| R2.14 | P2-T012, P2-T048, P2-T051 |
| R2.15 | P2-T018, P2-T042, P2-T060 |
| R2.16 | P2-T017, P2-T020, P2-T059 |
| R2.17 | P2-T016 |
| R2.18 | P2-T031, P2-T032, P2-T042, P2-T054, P2-T063, P2-T064, P2-T068 |
| R2.19 | P2-T011, P2-T019, P2-T035, P2-T043, P2-T048, P2-T053, P2-T063, P2-T065 |
| R2.20 | P2-T033, P2-T037, P2-T063, P2-T067 |
| R2.21 | P2-T034, P2-T060 |
| R2.30 | P2-T021, P2-T023, P2-T024, P2-T025, P2-T026, P2-T057 |
| R2.31 | P2-T022, P2-T024, P2-T025, P2-T026, P2-T056 |
| R2.32 | P2-T024, P2-T025, P2-T026, P2-T027, P2-T055, P2-T059 |
| R2.33 | P2-T028 |
| R2.34 | P2-T029, P2-T047, P2-T063 |
| R2.40–R2.43, R2.46 | Part B |
| R2.44 | Part B · MLflow ops: P2-T046 |
| R2.45 | Part B · containers/gVisor: P2-T044 |
| R2.47 | Part B · MLflow registry stages: P2-T046 |
| R2.48 | Part B · your inputs: P2-T002 |
| R2.50 | P2-T041, P2-T042, P2-T043, P2-T062 · D01, D03 (non-bot), D04, D05: Part B |
| R2.51 | P2-T035, P2-T038, P2-T039 · web queue in D01/D05: Part B |
| R2.52 | P2-T035, P2-T059 |
| R2.53 | P2-T036, P2-T037, P2-T060, P2-T061, P2-T066 |
| R2.54 | P2-T038, P2-T039, P2-T040, P2-T041, P2-T061, P2-T066 |
| R2.N1 | P2-T017, P2-T031, P2-T047, P2-T058 · tier A and signal → order: Part B |
| R2.N2 | P2-T051 |
| R2.N3 | P2-T001, P2-T023, P2-T044, P2-T045 |

| Roadmap ToDo | Tasks |
|---|---|
| T2.01 | P2-T048 |
| T2.02 | P2-T049 |
| T2.03 | P2-T001, P2-T045 |
| T2.04 | P2-T002 |
| T2.05 | P2-T050 |
| T2.06 | P2-T064 |
| T2.07 | P2-T065 |
| T2.08 | P2-T067 |
| T2.09 | P2-T066 |
| T2.20 | P2-T003, P2-T004, P2-T005, P2-T006, P2-T007, P2-T030 |
| T2.21 | P2-T008, P2-T009 |
| T2.22 | P2-T010, P2-T012, P2-T013, P2-T014, P2-T015, P2-T016, P2-T017, P2-T018, P2-T020, P2-T034, P2-T060 |
| T2.23 | P2-T031, P2-T032 |
| T2.24 | P2-T011, P2-T019, P2-T020, P2-T053 |
| T2.25 | P2-T021, P2-T022, P2-T023, P2-T024, P2-T025, P2-T026, P2-T027, P2-T028, P2-T030, P2-T033, P2-T057 |
| T2.26 | P2-T029 |
| T2.27–T2.31 | Part B |
| T2.32 | P2-T038, P2-T042, P2-T043 · D01, D03, D04, D05, manual ticket: Part B |
| T2.33 | P2-T035, P2-T039, P2-T059 |
| T2.34 | P2-T036, P2-T037, P2-T038, P2-T039, P2-T040, P2-T041 |
| T2.40 | P2-T044, P2-T045 |
| T2.41 | P2-T046 |
| T2.42 | P2-T047 |
| T2.60 | P2-T051, P2-T052, P2-T063 |
| T2.61 | P2-T054, P2-T063 |
| T2.62 | P2-T055 |
| T2.63 | P2-T056 |
| T2.64, T2.65, T2.67 | Part B |
| T2.66 | P2-T058 (risk check, kill) · tier A and signal → order: Part B |
| T2.68 | P2-T062 (D06, Bots tab) · D01, D03, D04, D05: Part B |
| T2.69 | P2-T061 |
| T2.80, T2.81 | Part B |
| T2.90 | P2-T068 |

## Planning notes & risks

- **Shared components owned by Part A:** `ApprovalCard` + approvals sheet (P2-T038), `KillSwitchButton` wiring + `LimitBar`/`LadderIndicator`/`VenueStatusChip` (P2-T042), `DiffView` + `C3Flow` (P2-T043), and the `/risk/preview`, `/approvals`, order and risk APIs (P2-T017, P2-T020, P2-T038). Part B's D01/D05/D03 tasks embed them; agree `RiskPreview` props once (Part B builds `RiskPreview`).
- **Gate results** come from Part B's validation harness through the `GateProvider` interface defined in P2-T007; until it lands, promotions above `backtested` are refused (safe default). Health/decay (P2-T034) also needs Part B's stored validation baselines.
- **Open numbers** (dead-man N, collar %, decision deadlines, downgrade N losses, cost-blowout kill) are proposed in P2-B003 and decided by you in P2-T048; code ships them only as policy defaults.
- **Biggest technical risks:** p99 < 1 ms risk check with a full policy (keep the hot path in-memory, compiled policy; benchmark early in P2-T017); IG/OANDA adapter effort (L each; Binance testnet + sandbox are enough to unblock bots/HITL first); engine-death dead-man (P2-B002, sidecar in P2-T032).
- **Event blackouts** use manual windows in P2; calendar-driven blackouts (`cal.*`) arrive with M5 in P4.
- **Kill rung 6 vault sweep** is a logged hook until P5 (P2-B010).
- **Mode vocabulary** (`paper|hitl|autonomous` canonical, `approve|auto` aliases) follows Part B's gap P2-B053; D03 template list follows P2-B054; web approval card spec follows P2-B058.
- **AU access:** carry and token-unlock need perps, which are blocked/unresolved for AU retail; they stay paper-only under the rule proposed in P2-B008.
- **No live money:** all configs refuse mainnet/live endpoints in P2 (P2-T023).

## Cross-phase prerequisites

| From | Roadmap IDs | Used by |
|---|---|---|
| P0 | R0.03 schemas + Alembic, R0.06 `ops.venue_registry`, R0.07 WORM layer, R0.08 `mt_api` (TOTP, C0–C3/Kill, `audit.command`, WS), R0.10 obs, R0.11 web shell + kill placeholder, R0.N1 sops secrets, R0.02 compose (MLflow, NATS) · T0.21 `mt_core` types, T0.23, T0.24, T0.26, T0.41–T0.43, T0.64 viewport harness | P2-T004, T006, T010, T016, T019, T020, T021, T035, T042, T044, T046, T062 |
| P1 | R1.01/R1.04/R1.05 live feeds, R1.02 bars + Parquet catalog, R1.10 DQ status, R1.11 costs + TCA scaffolding (T1.28), R1.12 reconciliation, R1.13 venue health, R1.14 alerts + Telegram bot (T1.31), T1.02 read-only keys, T1.61 DQ fault tooling | P2-T003, T017, T023–T027, T029, T035, T059 |
| P3 (downstream) | Journal consumes `fill.*` and the `manual` sleeve tag | P2-T014, P2-T021 |
| P4 (later) | M5 calendars → `cal.*` blackouts | P2-T017 |
| P5 (later) | R5.07 kill-switch hot-wallet sweep | P2-T018, P2-T031 |
| P6 (later) | Tier-B model service heartbeat (ladder rung 4, bot downgrade), LLM-signal template, Hummingbot venue behind M11 | P2-T018, P2-T037 |
| P7 (downstream) | R7.02 paper period (clock started in P2-T067), R7.06/R7.07 kill criteria + live decay (extends P2-T034), R7.10 MT5/cTrader adapters | P2-T034, P2-T067 |
