# Phase 2 · Part B plan (lab, features, tier A, MasterTradingBot libraries, D01/D03/D04/D05)

For the main agent to merge into `tracking/phase-2/PHASE.md`. Part B owns task IDs P2-T101–T199 and gap IDs P2-B050–B099. Part A (P2-T001–T099) owns M0, M11, M12, bots/HITL/Telegram, D06, the USER/OPS items and the runbooks.

## Workstreams

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

## Critical path

Weighted by size (part B only):

P2-T101 → P2-T102 → P2-T105 → P2-T106 → P2-T107 → P2-T108 → P2-T110 → P2-T114 → P2-T117 → P2-T145 → P2-T146 → P2-T163 → P2-T199

The paper-clock branch (which unlocks P7) is: … → P2-T114 → P2-T117 → P2-T143 → P2-T180 → P2-T199, plus P2-T161 (backtest ↔ paper parity) → P2-T180.

Part-A items on the same path: M0 base classes/manifest/templates (T2.20/T2.21) before P2-T104/T105; the M11 pre-trade layer (T2.22) and paper engine (T2.25) before P2-T105 parity, P2-T161 and P2-T180; the sandbox container + gVisor (T2.40) before P2-T116/T165; MLflow artefact storage (T2.41) before P2-T107/T127; the `ApprovalCard`/approvals API (currently P2-T038) before P2-T149. Ship order suggested by roadmap §7: one template through truth backtest + validation first; the D04 polish and the generator can trail by a week.

## Traceability

### Requirements → tasks (part B)

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

### Roadmap ToDos → tasks (part B)

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

## Planning notes & risks (part B)

- **Overlap resolved with part A:** `ApprovalCard`, approvals API and top-bar sheet (part A, currently P2-T038), `KillSwitchButton` wiring (P2-T042) and `DiffView`/`C3Flow` (P2-T043) are built once by part A and reused by P2-T140/T141/T143/T149. Flatten-and-halt uses part A's `position.close {halt, reason}` (P2-T020). `RiskPreview` is built in P2-T140 and must be the one part A's `ApprovalCard` embeds; agree props early.
- **S2 gaps to settle before P2-T110/T112 start:** P2-B050 (DSR threshold) and P2-B051 (freqtrade GPL route; default clean-room re-implementation).
- **Defaults chosen where docs are silent** (configurable, documented in the gaps): `regime_v1` price-based regimes (P2-B055), outcome labels for tier A (P2-B057), walk-forward 24m/3m folds, K = 5 purged folds with 1% embargo, 2,000 permutations, 5,000 block-bootstrap resamples, complexity penalty λ = 0.05 Sharpe per free parameter.
- **Risk:** truth backtests over L2 are slow; the 2 h job cap and worker caps keep the engine's cores free (P2-T167 verifies engine SLOs under lab load).
- **Risk:** MasterTradingBot golden files depend on the USER item T2.04 (part A, currently P2-T002); P2-T130 skips goldens with an explicit 'awaiting T2.04' marker that P2-T133 must clear.

## Cross-phase prerequisites (part B)

- P0: T0.22 (`mt_store`, `pit(as_of)`, Parquet helpers), T0.23 (WORM), T0.24 (`mt_api` command bus, confirmation levels, WS), T0.26 (web app, component library v0), T0.41 (NATS, MLflow, LiteLLM), T0.45 (gateway role keys/budgets), T0.64 (Playwright matrix in CI).
- P1: T1.21/T1.22 (bars, Parquet recording, backfills), T1.27 (DQ status), T1.28 (cost service → measured costs), T1.29 (reconciliation), T1.32 (D02/D07 and instrument finest-resolution metadata).
- Downstream: P6 (R6.14 distillation reuses P2-T125–T128; T6.23 LLM-signal post-cutoff evaluation plugs into P2-T114), P7 (T7.80 checks the paper clock started by P2-T180).
