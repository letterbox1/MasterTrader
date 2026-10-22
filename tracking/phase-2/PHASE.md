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
updated: 2026-10-22
---

# Phase 2 · Strategy framework, risk manager & research lab

## Summary

Phase 2 makes MasterTrader a trading platform: you can create **any strategy type on any timeframe**, backtest it with **measured costs**, validate it, and run it on **paper behind the risk manager**, controlled from the web UI and Telegram. The P1 paper clock starts at the end of the phase. ([roadmap](../../docs/roadmap/phase-2-strategies-risk-lab.md))

Aligned on 2026-10-22 with [16](../../docs/16-configuration-and-safety-model.md) and [17](../../docs/17-decisions-register.md) (all decisions ratified, 17 §E): layered configuration L0–L4 with strictest-wins and 16 defaults (nothing hard-coded); two-stage sleeve (10%/15%) and system (10%/25% + lock) drawdowns; three-layer dead-man; inline safety-state checks; modes `paper`/`hitl`/`autonomous` per bot (paper → HITL C2, → autonomous C3); DSR ≥ 0.95 and the per-strategy gate profile; client order ID `{bot}-{engine_epoch}-{seq}`; `stp: n/a (netting)` for netting brokers; `paper_ok`; Telegram `/kill` via NATS credentials limited to `kill.set`; `risk.sleeve.restart` C3. **Build first, keys last:** every venue integration is built and tested keyless (fixtures, emulators, sandbox venue); the one keyed check is P2-T071 (T2.72) after your keys (P2-T001).

The phase was planned in two parts that now share one board:
- **Part A (P2-T001–T099, P2-B001–B049):** M0 strategy framework, M11 risk manager (layers, ceilings, limits, sizing, sleeves, venue registry, RiskGate, safety-state checks, ladder, change control, kill, three-layer dead-man, modes, decay/health), M12 execution (engine, STP, adapters, client IDs + reconciliation, algos, TCA, shadow), bots/HITL/Telegram, D06 + D03 Bots/settings, ops, verification, USER items, runbooks.
- **Part B (P2-T101–T199, P2-B050–B099):** M7 lab + validation harness, M6 features, M21 tier A, MasterTradingBot libraries, D01/D03/D04/D05, parity and latency, the paper-clock RUN items and the phase exit demo.

Build order (roadmap risk mitigation): **M11 + M12 + one template first**, then bots/HITL and UI; lab extensions can trail by a week.

## Entry criteria

Phase gating is by dependency (17 §E): each task waits only for its own `depends_on`, including the explicit P0/P1 prerequisites listed below.
- [ ] P0 command layer (C0–C3/Kill + TOTP), WORM audit tables, `audit.integrity` and `ops.venue_registry` exist (P0-T024–T038)
- [ ] P1 DQ status, measured costs, reconciliation, egress check and the Telegram alert bot exist (P1-T030, P1-T038–T042, P1-T045, P1-T071)
- [ ] Testnet/practice **trade-only** keys (T2.03 → P2-T001) are needed only before the keyed check P2-T071, not to start the phase (see gap P2-B020)

## Exit criteria

- [ ] 1. Create a strategy from a template, from code and by "describe it"; backtest with measured costs; the validation report shows all harness sections.
- [ ] 2. Run it on paper behind M11; a HITL order is approved from Telegram.
- [ ] 3. Kill drill passes from the phone; a C3 loosening needs TOTP + cool-down.
- [ ] 4. The P1 paper clock has started.
- [ ] All Phase 2 tasks (Part A and Part B) are done or cancelled.
- [ ] No open S1/S2 bugs or gaps in Phase 2.

Evidence for every criterion is collected by the exit demo P2-T199.

## Workstreams

| Workstream | Tasks |
|---|---|
| Your actions (USER) | P2-T001 keys (keyed check only) · P2-T002 MasterTradingBot inputs · P2-T048 review defaults, set values + L0 ceilings · P2-T049 sleeves · P2-T050 first manifests · P2-T064 kill drill · P2-T065 C3 loosening + retire break-glass · P2-T066 first bots + HITL approval · P2-T067 start paper clock |
| Build · M0 strategy framework | P2-T003 base classes · P2-T004 manifest (proposals) · P2-T005 never-build · P2-T006 registry · P2-T007 lifecycle, mode ceiling, gate profile · P2-T008, P2-T009 templates · P2-T030 shadow mode |
| Build · M11 configuration & limits | P2-T010 layered policy store · P2-T011 L0 ceilings · P2-T069 layer merge + effective limits · P2-T012 defaults, two-stage drawdowns · P2-T013 sizing · P2-T014 sleeves/netting · P2-T015 portfolio · P2-T016 venue registry + 2× + `paper_ok` · P2-T019 change control · P2-T020 mt_api surface |
| Build · M11 order path & safety | P2-T017 RiskGate · P2-T070 inline safety-state checks · P2-T018 ladder · P2-T031 kill · P2-T032 dead-man layer 1 · P2-T072 `deadman` sidecar (layer 2) · P2-T073 venue timers + resting stops (layer 3) · P2-T074 restart flat, bots paused · P2-T033 modes/approvals · P2-T034 decay/health |
| Build · M12 execution (keyless) | P2-T021 engine · P2-T022 STP / netting rule · P2-T023 testnet configs + sandbox · P2-T024 Alpaca · P2-T025 OANDA · P2-T026 IG · P2-T027 client IDs + reconcile · P2-T028 maker-first/TWAP · P2-T029 TCA |
| Build · bots, HITL & Telegram | P2-T035 Telegram v1 + C3 · P2-T036 bot model (L4) · P2-T037 bot modes/downgrade · P2-T038 approvals API + `ApprovalCard` · P2-T039 Telegram approval cards · P2-T040 bot commands · P2-T041 D03 Bots tab |
| Build · UI (D06, D03 settings) | P2-T042 D06 overview · P2-T043 D06 policy/events/changes, D03 settings, Stress placeholder |
| Ops | P2-T044 containers + gVisor + `deadman` · P2-T045 secrets + key audit tool · P2-T046 MLflow · P2-T047 Grafana |
| Verify · Part A | P2-T051 golden/property · P2-T052 no-bypass · P2-T053 C3 matrix · P2-T054 kill + layer-1 drills · P2-T055 restart-duplicate · P2-T056 STP audit · P2-T057 adapter conformance · P2-T058 latency (risk, kill) · P2-T059 degraded modes · P2-T060 decay/ladder/downgrade · P2-T061 bot scenarios · P2-T062 viewport (D06, Bots, settings) · P2-T063 Part A flows · P2-T075 kill-the-engine drill · P2-T076 safety-state goldens · **P2-T071 keyed testnet end-to-end (last)** |
| Docs | P2-T068 runbooks |
| Lab core (M7) | P2-T101, P2-T102, P2-T103, P2-T104, P2-T105, P2-T106, P2-T107, P2-T117 |
| Validation harness (M7) | P2-T108, P2-T109, P2-T110, P2-T111, P2-T112 (vendored analysers), P2-T113, P2-T114 (gate profile), P2-T115 |
| Sandbox + generator | P2-T116 |
| Core features (M6) | P2-T120, P2-T121, P2-T122, P2-T123 |
| Tier A (M21) | P2-T125, P2-T126, P2-T127, P2-T128 |
| MasterTradingBot libraries | P2-T130, P2-T131, P2-T132 |
| UI (D01, D03, D04, D05) | P2-T140, P2-T141, P2-T142, P2-T143, P2-T144, P2-T145, P2-T146, P2-T147, P2-T148, P2-T149, P2-T150 |
| Verify · Part B | P2-T133, P2-T160, P2-T161, P2-T162, P2-T163, P2-T164, P2-T165, P2-T166, P2-T167, P2-T168 |
| Run | P2-T180 (paper clock; completion checked in P7 T7.80), P2-T182 |
| Phase exit demo | P2-T199 |
| Gaps | Closed 2026-10-22: P2-B001–B014, P2-B050–B060. Open (doc wording, S3/S4): P2-B015–B020 |

Totals: 128 tasks (85 BUILD, 27 VERIFY, 9 USER, 4 OPS, 2 RUN, 1 DOC); sizes 18 L, 74 M, 31 S, 5 XS; no XL.

## Critical path

Weighted by size (longest chain to the exit demo):

P2-T010 → P2-T012 → P2-T014 → P2-T015 → P2-T017 → P2-T105 → P2-T106 → P2-T107 → P2-T108 → P2-T110 → P2-T114 → P2-T117 → P2-T145 → P2-T146 → P2-T163 → P2-T199

Parallel spines:
- Paper clock: P2-T017 → P2-T021 → P2-T031 → P2-T032 → P2-T042 → P2-T043 → P2-T063 → P2-T067 → P2-T180.
- Dead-man: P2-T021 → P2-T022 → P2-T025 → P2-T073 → P2-T075; P2-T032 → P2-T072 → P2-T075; P2-T027 → P2-T074.
- Keys last: P2-T001 (you) + P2-T057/P2-T056/P2-T045/P2-T072/P2-T073 → P2-T071 → P2-T066 → P2-T067.
- C3: P2-T019 → P2-T043 → P2-T053 → P2-T065.
- Safety state: P2-T070 → P2-T017 → P2-T076.

## Traceability

### Requirements → tasks

| Requirement | Tasks |
|---|---|
| R2.01 | P2-T003, P2-T021, P2-T105, P2-T161, P2-T199 |
| R2.02 | P2-T008, P2-T009, P2-T132, P2-T144 |
| R2.03 | P2-T003, P2-T008, P2-T009, P2-T144 |
| R2.04 | P2-T004, P2-T006, P2-T050, P2-T143, P2-T144 |
| R2.05 | P2-T005, P2-T144 |
| R2.06 | P2-T006, P2-T007, P2-T114, P2-T143, P2-T166, P2-T180, P2-T199 |
| R2.07 | P2-T030, P2-T115 |
| R2.10 | P2-T017, P2-T020, P2-T021, P2-T051, P2-T052, P2-T063 |
| R2.11 | P2-T010, P2-T015, P2-T020, P2-T043, P2-T069 |
| R2.12 | P2-T013, P2-T051 |
| R2.13 | P2-T012, P2-T014, P2-T049, P2-T051, P2-T148 |
| R2.14 | P2-T012, P2-T048, P2-T051 |
| R2.15 | P2-T018, P2-T042, P2-T060 |
| R2.16 | P2-T017, P2-T020, P2-T059, P2-T070 |
| R2.17 | P2-T016 |
| R2.18 | P2-T031, P2-T032, P2-T042, P2-T054, P2-T063, P2-T064, P2-T068, P2-T072, P2-T075, P2-T199 |
| R2.19 | P2-T011, P2-T019, P2-T035, P2-T043, P2-T048, P2-T053, P2-T063, P2-T065, P2-T199 |
| R2.20 | P2-T033, P2-T037, P2-T063, P2-T067, P2-T149, P2-T199 |
| R2.21 | P2-T034, P2-T060 |
| R2.30 | P2-T021, P2-T023, P2-T024, P2-T025, P2-T026, P2-T057, P2-T071 |
| R2.31 | P2-T022, P2-T024, P2-T025, P2-T026, P2-T056, P2-T071 |
| R2.32 | P2-T024, P2-T025, P2-T026, P2-T027, P2-T055, P2-T059, P2-T074 |
| R2.33 | P2-T028 |
| R2.34 | P2-T029, P2-T047, P2-T063, P2-T147 |
| R2.40 | P2-T101, P2-T102, P2-T104, P2-T105, P2-T106, P2-T117, P2-T145, P2-T146, P2-T161, P2-T166, P2-T167, P2-T199 |
| R2.41 | P2-T102, P2-T103, P2-T104, P2-T105, P2-T164 |
| R2.42 | P2-T102, P2-T106, P2-T108, P2-T109, P2-T110, P2-T111, P2-T114, P2-T143, P2-T146, P2-T164, P2-T166, P2-T199 |
| R2.43 | P2-T112, P2-T113, P2-T114, P2-T146, P2-T160, P2-T199 |
| R2.44 | P2-T046, P2-T101, P2-T107, P2-T115, P2-T117, P2-T145, P2-T164, P2-T167 |
| R2.45 | P2-T044, P2-T116, P2-T144, P2-T146, P2-T165, P2-T166, P2-T167, P2-T199 |
| R2.46 | P2-T120, P2-T121, P2-T122, P2-T123 |
| R2.47 | P2-T046, P2-T125, P2-T126, P2-T127, P2-T128, P2-T162, P2-T199 |
| R2.48 | P2-T002, P2-T130, P2-T131, P2-T132, P2-T133, P2-T199 |
| R2.50 | P2-T041, P2-T042, P2-T043, P2-T062, P2-T117, P2-T140, P2-T141, P2-T142, P2-T143, P2-T144, P2-T145, P2-T146, P2-T147, P2-T148, P2-T163, P2-T166, P2-T168, P2-T199 |
| R2.51 | P2-T035, P2-T038, P2-T039, P2-T140, P2-T149, P2-T168, P2-T199 |
| R2.52 | P2-T035, P2-T059 |
| R2.53 | P2-T036, P2-T037, P2-T060, P2-T061, P2-T066 |
| R2.54 | P2-T038, P2-T039, P2-T040, P2-T041, P2-T061, P2-T066, P2-T149 |
| R2.55 | P2-T010, P2-T011, P2-T043, P2-T048, P2-T069 |
| R2.56 | P2-T032, P2-T072, P2-T073, P2-T074, P2-T075, P2-T199 |
| R2.57 | P2-T043 |
| R2.58 | P2-T070, P2-T076, P2-T199 |
| R2.N1 | P2-T017, P2-T031, P2-T047, P2-T054, P2-T058, P2-T128, P2-T162, P2-T199 |
| R2.N2 | P2-T051, P2-T076 |
| R2.N3 | P2-T001, P2-T023, P2-T044, P2-T045, P2-T071 |

### Roadmap ToDos → tasks

| ToDo | Tasks |
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
| T2.20 | P2-T003, P2-T004, P2-T005, P2-T006, P2-T007 |
| T2.21 | P2-T008, P2-T009 |
| T2.22 | P2-T010, P2-T012, P2-T013, P2-T014, P2-T015, P2-T016, P2-T017, P2-T018, P2-T020, P2-T034, P2-T060 |
| T2.23 | P2-T031, P2-T032 |
| T2.24 | P2-T011, P2-T019, P2-T020, P2-T053 |
| T2.25 | P2-T021, P2-T022, P2-T023, P2-T024, P2-T025, P2-T026, P2-T027, P2-T028, P2-T033, P2-T057 |
| T2.26 | P2-T029 |
| T2.27 | P2-T101, P2-T102, P2-T103, P2-T104, P2-T105, P2-T106, P2-T107, P2-T108, P2-T109, P2-T110, P2-T111, P2-T112, P2-T113, P2-T114, P2-T115, P2-T117, P2-T164, P2-T166, P2-T167 |
| T2.28 | P2-T116, P2-T165 |
| T2.29 | P2-T120, P2-T121, P2-T122, P2-T123 |
| T2.30 | P2-T125, P2-T126, P2-T127, P2-T128 |
| T2.31 | P2-T130, P2-T131, P2-T132 |
| T2.32 | P2-T038, P2-T042, P2-T043, P2-T117, P2-T140, P2-T141, P2-T142, P2-T143, P2-T144, P2-T145, P2-T146, P2-T147, P2-T148, P2-T149, P2-T166, P2-T168 |
| T2.33 | P2-T035, P2-T039, P2-T059 |
| T2.34 | P2-T036, P2-T037, P2-T038, P2-T039, P2-T040, P2-T041 |
| T2.35 | P2-T010, P2-T069 |
| T2.36 | P2-T072, P2-T073, P2-T074 |
| T2.37 | P2-T030, P2-T115 |
| T2.38 | P2-T043 |
| T2.39 | P2-T070 |
| T2.40 | P2-T044, P2-T045 |
| T2.41 | P2-T046 |
| T2.42 | P2-T047 |
| T2.60 | P2-T051, P2-T052, P2-T063 |
| T2.61 | P2-T054, P2-T063 |
| T2.62 | P2-T055 |
| T2.63 | P2-T056 |
| T2.64 | P2-T160 |
| T2.65 | P2-T161 |
| T2.66 | P2-T058, P2-T162 |
| T2.67 | P2-T133 |
| T2.68 | P2-T062, P2-T163 |
| T2.69 | P2-T061 |
| T2.70 | P2-T075 |
| T2.71 | P2-T076 |
| T2.72 | P2-T071 |
| T2.80 | P2-T180 |
| T2.81 | P2-T150, P2-T182 |
| T2.90 | P2-T068 |
| Exit criteria 1–4 | P2-T199 (with evidence from P2-T051, P2-T062–T067, P2-T075, P2-T076, P2-T166, P2-T180) |

## Planning notes & risks

- **Configurable defaults:** every number in the tasks is a default from 16 §2–§3 stored in the layered policy (P2-T010/P2-T069) and shown with its layer and link; none is hard-coded. Loosening at any layer (incl. L0 and the gate profile) is C3; tightening is immediate.
- **Build first, keys last:** adapters (P2-T023–T026), STP (P2-T022), conformance (P2-T057), STP audit (P2-T056), key audit (P2-T045), drills (P2-T054, P2-T075) and restart tests (P2-T055) run on the sandbox venue, mock venue emulators and cassettes. P2-T071 is the single keyed check; HITL bots on testnet/practice accounts (P2-T066) come after it. Paper bots and the paper clock run on the sandbox venue and need no venue keys.
- **Shared components owned by Part A:** `ApprovalCard` + approvals sheet (P2-T038), `KillSwitchButton` wiring + `LimitBar`/`LadderIndicator`/`VenueStatusChip` (P2-T042), `DiffView` + `C3Flow` and the D03 settings page (P2-T043), `/risk/preview`, `/risk/policy` (effective limits), `/approvals`, order and risk APIs (P2-T017, P2-T020, P2-T038, P2-T069). `RiskPreview` is built once in P2-T140.
- **Gate results** come from the validation harness through the `GateProvider` interface (P2-T007); thresholds come from the per-strategy gate profile (16 §2.4). Until P2-T114 lands, promotions above `backtested` are refused (safe default).
- **Biggest technical risks:** p99 < 1 ms risk check with layers + safety state (compiled tables, no I/O; benchmark early in P2-T017/P2-T058); IG/OANDA adapter effort (L each); venue cancel-after support is partly (U) and must be verified before P2-T073 enables it; the sidecar needs an external venue emulator because the in-engine sandbox venue dies with the engine (P2-T072/P2-T075).
- **Event blackouts** use manual windows in P2; calendar-driven blackouts (`cal.*`) arrive with M5 in P4.
- **Kill:** no vault sweep in P2 (logged no-op hook; P5 R5.07 adds it).
- **Break-glass C3** stays available until Telegram C3 is proven; you retire it in P2-T065.
- **AU access:** carry and token-unlock need perps; they run on paper only where the registry marks the product `paper_ok`.
- **No live money:** configs refuse mainnet/live endpoints in P2 (P2-T023).
- **Open doc gaps (S3/S4, wording):** P2-B015 (Postgres down: 02 §9.3 vs 16 §3.1), P2-B016 (02 F6 automatic kill triggers vs 03 M11/16), P2-B017 (D06 lists `risk.sleeve.restart` as P7), P2-B018 (D06 Stress replay 'R2.57' wording), P2-B019 (02 F2 'egress from P7'), P2-B020 (roadmap entry criterion requires keys up front). Tasks follow 16/17 meanwhile.

## Cross-phase prerequisites

Now explicit `depends_on` entries on existing P0/P1 tasks (only real preconditions):

| From | Task | Used by |
|---|---|---|
| P0 | P0-T002 Telegram bot + user id (USER) | P2-T064, P2-T066 |
| P0 | P0-T009 demo/paper/testnet accounts (USER) | P2-T001 |
| P0 | P0-T014 monorepo · P0-T016 `mt_core` types · P0-T018 `mt_obs` | P2-T004 · P2-T003, P2-T010 · P2-T032 |
| P0 | P0-T020 compose (NATS, MLflow) · P0-T021 networks · P0-T022 sops → tmpfs | P2-T044, P2-T046, P2-T101 · P2-T044 · P2-T001, P2-T044, P2-T045 |
| P0 | P0-T024 schemas/Alembic · P0-T025 venue registry table · P0-T027 `pit(as_of)` | P2-T006, P2-T010, P2-T101 · P2-T016 · P2-T101, P2-T103 |
| P0 | P0-T029 WORM layer · P0-T031 WORM audit tables · P0-T038 `audit.verify` + `audit.integrity` | P2-T007, P2-T010, P2-T113 · P2-T021 · P2-T070 |
| P0 | P0-T033 TOTP · P0-T034 command bus · P0-T035 confirmation levels + break-glass · P0-T036 WS hub | P2-T035 · P2-T006, P2-T020, P2-T117 · P2-T007, P2-T019, P2-T020, P2-T031, P2-T117 · P2-T020, P2-T038, P2-T117 |
| P0 | P0-T039 backups · P0-T042 LiteLLM gateway · P0-T045 Grafana provisioning | P2-T046 · P2-T113, P2-T116 · P2-T047 |
| P0 | P0-T048 API client · P0-T049 component library · P0-T050 app shell · P0-T053 viewport harness · P0-T062 your TOTP (USER) | P2-T038, P2-T140 · P2-T038, P2-T041, P2-T042, P2-T140, P2-T141 · P2-T041, P2-T042, P2-T142 · P2-T062 · P2-T048, P2-T064, P2-T065 |
| P1 | P1-T004 NATS streams · P1-T009 instrument master · P1-T012/T013 Parquet + bars | P2-T021, P2-T031 · P2-T003, P2-T103 · P2-T103 |
| P1 | P1-T016 OANDA · P1-T017 IG · P1-T021 Alpaca stream clients | P2-T025 · P2-T026 · P2-T024 |
| P1 | P1-T030 DQ monitor · P1-T071 egress check · P1-T057 DQ fault tooling | P2-T017, P2-T070 · P2-T070 · P2-T059 |
| P1 | P1-T038 fees · P1-T039 funding · P1-T040 spreads/TCA scaffold | P2-T029, P2-T102 · P2-T029, P2-T102 · P2-T017, P2-T023, P2-T029, P2-T102 |
| P1 | P1-T041/T042 reconciliation · P1-T045 alert fan-out | P2-T027 · P2-T035, P2-T047 |
| P3 (downstream) | Journal consumes `fill.*` and the `manual` sleeve tag | P2-T014, P2-T021 |
| P4 (later) | M5 calendars → `cal.*` blackouts | P2-T017 |
| P5 (later) | R5.07 kill-switch hot-wallet sweep | P2-T018, P2-T031 |
| P6 (later) | Tier-B heartbeat (ladder rung 4), LLM-signal template, teacher labels (R6.14) | P2-T018, P2-T037, P2-T125 |
| P7 (downstream) | R7.02/T7.80 paper period (clock started in P2-T067/P2-T180), R7.06/R7.07 kill criteria + live decay (extends P2-T034), R7.16 Stress tab (replaces the P2-T043 placeholder), exit-node IP (P2-T001 keys re-pointed) | P2-T034, P2-T043, P2-T067, P2-T180 |
