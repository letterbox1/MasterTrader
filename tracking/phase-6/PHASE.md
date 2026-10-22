---
phase: 6
title: AI decision layer, memory, models, anomalies & treasury
roadmap: docs/roadmap/phase-6-ai-models-treasury.md
status: not_started
opens_after: [5]
force_open: false
started: ""
completed: ""
doc_sync_status: n/a
updated: 2026-10-22
---

# Phase 6 · AI decision layer, memory, models, anomalies & treasury

## Summary

From the [roadmap](../../docs/roadmap/phase-6-ai-models-treasury.md): ask for an analysis of any instrument and get a sourced `Signal`; agents learn from settled outcomes; our own tier-B decision models are trained, benchmarked and promoted only through gates; anomalies are explained on Telegram; idle capital earns under the on-chain cost gate.

Aligned on 2026-10-22 with [16](../../docs/16-configuration-and-safety-model.md) and [17](../../docs/17-decisions-register.md) (ratified): every number is a configurable default (LLM budgets and tier-B thresholds in 16 §2.10, wallet/treasury caps in 16 §2.7, venue cap in 16 §2.1); `audit.llm_call` exists from P0; `Signal` fields per 03 M8; PIT memory with `observed_at`/`ingested_at`; build first, keys last.

The 70 tasks are organised in eight workstreams:
1. **Agents & LLM plumbing:** Signal (03 M8), prompt/model versioning on the P0 audit, the tool belt, the debate graph, the scheduler and triggers, budget enforcement with local fallback.
2. **Memory:** Hindsight slim, point-in-time recall (filtered / frozen snapshot / off), settlement and reflection.
3. **Anomalies:** detectors and the explain agent.
4. **LLM-signal strategies:** the template and the post-cutoff gate.
5. **Tier B stage 2:** question registry v2, the label store and labelling queue, the dataset builder, trainer, calibration, serving, the shadow sampler and threshold tuner, the bake-off (Kev only if cleared), promotion gates, and the nightly and monthly flows.
6. **Treasury & hold-and-earn:** policy and allow-list, yields, the allocator, sweeps and reserve, the execution path, the node model, the DAO monitor.
7. **UI:** D09, D10 (two parts), D18 earn.
8. **Optional modules (low priority):** Hummingbot, social drafts, credibility, crowd-sim, LightRAG.

VERIFY, RUN and the exit demo close the phase; live checks with your keys come last (P6-T070).

## Entry criteria

- [ ] Cross-phase prerequisites are explicit `depends_on` entries on each task (parallel by dependency, 17 §E); the list below is the summary
- [ ] P5 signer, cost gate and wallet view passing their test suites (P5-T013, P5-T016, P5-T020, P5-T022, P5-T050) for the treasury track
- [ ] P4 text + RAG + SemIf running (P4-T029, P4-T032, P4-T062); ≥ 4 weeks of teacher/label data helps tier-B training (P6-T020 refuses below its minimum rows)
- [ ] P2 lab, tier-A pipeline, MLflow registry and promotion gates available (P2-T046, P2-T107, P2-T114, P2-T125, P2-T128)
- [ ] P0 gateway (LiteLLM ≥ 1.83, pinned) with per-role keys, `audit.llm_call` writer, `llm-local`, TEI, WORM machinery and `mt_api` C0–C3 in place (P0-T031, P0-T042, P0-T043, P0-T044, P0-T034)
- [ ] GPU decision taken (P0-T005); without a GPU the tier-B SLO can't be met and keeping SemIf is a valid outcome

## Exit criteria

- [ ] 1. Ask for an analysis of any instrument → a sourced `Signal` with provenance, visible in D09 (P6-T067, P6-T062, P6-T070, P6-T066)
- [ ] 2. An anomaly is explained on Telegram (P6-T061, P6-T066)
- [ ] 3. The bake-off report names a production tier-B model (or keeps SemIf) with calibration evidence (P6-T059, P6-T066)
- [ ] 4. Idle stables are allocated within the allow-list after the cost gate; the treasury reserve holds (P6-T060, P6-T034, P6-T066)
- [ ] All phase-6 tasks are done or cancelled (optional items cancelled per P6-T003 decisions)
- [ ] No open S1/S2 bugs in phase 6

## Workstreams

| Workstream | Tasks |
|---|---|
| Your actions (USER) | P6-T001 review budget defaults · P6-T002 Tally key + FinMMEval · P6-T003 optional modules · P6-T034 treasury policy (C3) · P6-T044 labelling queue · P6-T049 social drafts (optional) |
| Build: agents & LLM plumbing | P6-T004 Signal (03 M8) · P6-T005 prompt/model versioning on the P0 audit · P6-T006 tool belt · P6-T007 debate graph · P6-T008 scheduler/triggers/API · P6-T009 budget enforcement |
| Build: memory | P6-T012 Hindsight client + PIT recall · P6-T013 settlement + reflection |
| Build: anomalies | P6-T014 detectors · P6-T015 explain agent + `anomaly.explain` |
| Build: LLM-signal strategies | P6-T016 template · P6-T017 post-cutoff gate |
| Build: tier B stage 2 | P6-T018 question registry v2 · P6-T019 label queue (extends P4 labels) · P6-T020 dataset builder · P6-T021 trainer · P6-T022 calibration · P6-T024 export + serving · P6-T025 shadow sampler · P6-T026 threshold tuner · P6-T028 Laya-ft · P6-T029 bake-off harness · P6-T030 promotion gates · P6-T031 nightly distillation · P6-T032 monthly fine-tune |
| Build: treasury | P6-T033 policy + allow-list · P6-T035 DefiLlama yields · P6-T036 allocator · P6-T037 sweeps + reserve · P6-T038 earn execution · P6-T039 node/validator model · P6-T040 DAO monitor |
| Build: UI | P6-T041 D09 · P6-T042 D10 registry/questions/bake-off/gateway · P6-T043 D10 memory/RAG/labelling/shadow · P6-T045 D18 earn |
| Build: optional (low) | P6-T046 Hummingbot + D11 · P6-T047 social drafts · P6-T048 credibility + shill-burst · P6-T050 crowd-sim · P6-T051 LightRAG |
| Ops | P6-T010 spend panel + alerts · P6-T011 Hindsight container · P6-T023 GPU serving · P6-T027 bake-off containers |
| Verify (keyless) | P6-T052 scheduler + audit (T6.67) · P6-T053 budgets (T6.70) · P6-T054 prompt injection · P6-T055 PIT memory · P6-T056 label provenance · P6-T057 determinism · P6-T058 latency (T6.71) · P6-T059 bake-off review · P6-T060 treasury · P6-T061 seeded anomaly (T6.68) · P6-T062 E2E F4 · P6-T063 LLM-signal gate (T6.69) · P6-T064 degraded modes · P6-T067 sample runs (T6.66) · P6-T068 Kev licence check (T6.72) · P6-T069 port check (T6.73) |
| Verify (your keys, last) | P6-T070 live gateway roles + Tally |
| Run | P6-T065 start the 4-week distillation + LLM-signal paper soak (completion checked at P7 entry) |
| Exit | P6-T066 exit demo |
| Gaps | P6-B003 open (Kev (U), owned by P6-T068); P6-B001, P6-B002, P6-B004–P6-B016 closed |

## Critical path

P6-T004 → P6-T006 → P6-T007 → P6-T012 → P6-T013 → P6-T020 → P6-T021 → P6-T022 → P6-T024 → P6-T029 → P6-T030 → P6-T031 → P6-T059 → P6-T065 → P6-T066

Feeding in from the side (start early, they don't wait for the chain): P6-T005, P6-T009 (keyless, on P0 only) → P6-T007/P6-T008; P6-T011 → P6-T012; P6-T018 → P6-T019 → P6-T020; P6-T023 → P6-T024; P6-T068 → P6-T027 → P6-T028 → P6-T029.

Parallel track (treasury): P6-T033 → P6-T035/P6-T036/P6-T037 → P6-T038 → P6-T060 → P6-T066, with P6-T034 (USER, C3) needed only for the exit demo.

Keys last: P6-T070 (your Anthropic/custom endpoint and Tally keys) runs after the keyless VERIFY items and before the exit demo.

The settlement step (P6-T013) needs elapsed time: a Signal must reach its horizon before it yields a label. So start P6-T007/P6-T008 early and let short-horizon scheduled runs accumulate teacher data while the tier-B pipeline is built.

## Traceability

| Requirement | Tasks |
|---|---|
| R6.01 | P6-T004, P6-T006, P6-T007, P6-T008, P6-T041, P6-T054, P6-T062, P6-T066, P6-T067, P6-T070 |
| R6.02 | P6-T006, P6-T008, P6-T052 |
| R6.03 | P6-T005, P6-T052, P6-T053, P6-T070 |
| R6.04 | P6-T011, P6-T012, P6-T013, P6-T043, P6-T055, P6-T062, P6-T064 |
| R6.05 | P6-T014, P6-T015, P6-T054, P6-T061, P6-T066 |
| R6.06 | P6-T016, P6-T017, P6-T063, P6-T065 |
| R6.07 | P6-T001, P6-T009, P6-T010, P6-T042, P6-T053, P6-T064, P6-T070 |
| R6.10 | P6-T020, P6-T021, P6-T022, P6-T024, P6-T059, P6-T066 |
| R6.11 | P6-T023, P6-T024, P6-T057, P6-T058, P6-T064 |
| R6.12 | P6-T002, P6-T027, P6-T028, P6-T029, P6-T030, P6-T042, P6-T059, P6-T066, P6-T068 |
| R6.13 | P6-T018, P6-T019, P6-T020, P6-T025, P6-T026, P6-T032, P6-T043, P6-T044, P6-T056 |
| R6.14 | P6-T013, P6-T020, P6-T030, P6-T031, P6-T042, P6-T059, P6-T062, P6-T065 |
| R6.20 | P6-T033, P6-T034, P6-T038, P6-T045, P6-T060, P6-T066 |
| R6.21 | P6-T034, P6-T035, P6-T036, P6-T060, P6-T066 |
| R6.22 | P6-T033, P6-T034, P6-T037, P6-T060, P6-T066 |
| R6.23 | P6-T002, P6-T039, P6-T040, P6-T060, P6-T070 |
| R6.24 | P6-T033, P6-T036, P6-T037, P6-T038, P6-T045, P6-T060, P6-T064, P6-T066 |
| R6.30 | P6-T003, P6-T046 |
| R6.31 | P6-T003, P6-T047, P6-T048, P6-T049 |
| R6.32 | P6-T003, P6-T050, P6-T051 |
| R6.40 | P6-T041, P6-T042, P6-T043, P6-T045, P6-T062, P6-T066 |
| R6.N1 | P6-T006, P6-T054 |
| R6.N2 | P6-T011, P6-T023, P6-T027, P6-T069 |
| R6.N3 | P6-T023, P6-T024, P6-T058 |

| Roadmap ToDo | Tasks |
|---|---|
| T6.01 | P6-T001 |
| T6.02 | P6-T044 |
| T6.03 | P6-T034 |
| T6.04 | P6-T003 |
| T6.05 | P6-T049 |
| T6.20 | P6-T004, P6-T006, P6-T007, P6-T008 |
| T6.21 | P6-T012, P6-T013 |
| T6.22 | P6-T014, P6-T015 |
| T6.23 | P6-T016, P6-T017 |
| T6.24 | P6-T020, P6-T021, P6-T022, P6-T024 |
| T6.25 | P6-T028, P6-T029 |
| T6.26 | P6-T018, P6-T019, P6-T025, P6-T026, P6-T032 |
| T6.27 | P6-T030, P6-T031 |
| T6.28 | P6-T033, P6-T035, P6-T036, P6-T037, P6-T038, P6-T039, P6-T040 |
| T6.29 | P6-T041, P6-T042, P6-T043, P6-T045 |
| T6.30 | P6-T046, P6-T047, P6-T048, P6-T050, P6-T051 |
| T6.31 | P6-T005 |
| T6.32 | P6-T009 |
| T6.40 | P6-T011, P6-T023, P6-T027 |
| T6.41 | P6-T010 |
| T6.60 | P6-T059 |
| T6.61 | P6-T057 |
| T6.62 | P6-T056 |
| T6.63 | P6-T055 |
| T6.64 | P6-T060 |
| T6.65 | P6-T054 |
| T6.66 | P6-T067 |
| T6.67 | P6-T052 |
| T6.68 | P6-T061 |
| T6.69 | P6-T063 |
| T6.70 | P6-T053 |
| T6.71 | P6-T058 |
| T6.72 | P6-T068 |
| T6.73 | P6-T069 |
| T6.80 | P6-T065 |

Supporting items without a roadmap ToDo:
- P6-T002 (USER: Tally key and FinMMEval data, feeds P6-T059 and P6-T070).
- P6-T062 (full F4 flow), P6-T064 (degraded modes, 02 §9.3).
- P6-T070 (live check with your keys: gateway roles and Tally; build first, keys last).
- P6-T066 (exit demo).

Gaps: P6-B001, P6-B002 and P6-B004–P6-B016 closed on 2026-10-22 (decided in 17, docs aligned). P6-B003 stays open until the Kev (U) check P6-T068 is done.

## Planning notes & risks

- **Optional items (P6-T046–P6-T051)** are low priority. P6-T003 records your decision. Cancel each item you decline so it doesn't hold the phase open. Crowd-sim is possible only with a local memory backend and a hardened config (17 §D P6-B009); otherwise cancel P6-T050.
- **Elapsed time:**
  - Tier-B training needs settled teacher decisions (P6-T013). Run short-horizon scheduled analyses as early as possible.
  - The 4-week soak (P6-T065) is only **started** here. "Four clean weeks" is checked at P7 entry, so the phase can close.
- **GPU dependency:** without a 16–24 GB GPU (P0-T005), P6-T021 training is impractical and the p95 < 50 ms SLO (P6-T058) can't be met. In that case the valid outcome of exit criterion 3 is "keep SemIf". Record it in P6-T059.
- **Distillation copying teacher bias** (roadmap risk). Mitigations:
  - outcome-corrected labels (P6-T020);
  - worst-fold promotion against a frozen baseline and ≥ 14 days in shadow (P6-T030, 16 §2.10);
  - shadow outputs never used as labels (P6-T019, P6-T056).
- **LLM spend creep:** event-triggered runs only (P6-T008), per-role and monthly limits with local fallback (P6-T009, 16 §2.10 defaults incl. `shadow` $0.30), alerts (P6-T010).
- **DeFi protocol risk:**
  - allow-list and C3 (P6-T033, P6-T034);
  - ≤ 20% per protocol, HLP ≤ 10% of stables and ≤ 5% of portfolio, venue ≤ 25% (L1), and the reserve band (P6-T036, P6-T037; 16 §2.1/§2.7);
  - depeg/exploit auto-exits, which start only with this treasury (P6-T038; before P6 it's alert + task);
  - verification on forks only (P6-T060).
- **Point-in-time risk in memory:** decided (17 §A P6-B016): `observed_at`/`ingested_at`, derived memories carry the latest source time, `frozen`/`off` backtest modes (P6-T012); the mandatory PIT test is P6-T055.
- **Build first, keys last:** everything builds and verifies against `llm-local`, recorded responses, fake providers, forks and fixtures. Your keys are needed only by P6-T070 (Anthropic/custom endpoint from P0-T007, Tally from P6-T002).
- **Kev-4B/9B:** in the bake-off only if a public, licence-compatible release exists (17 §D P6-B003); the agent check is P6-T068 (T6.72), and P6-B003 stays open until it's done.
- **Doc follow-ups raised by tasks' doc sync:** 16 §2.4 gets the post-cutoff embargo/minimum OOS defaults (P6-T017); 16 §2.7 gets the rebalance hurdle and stablecoin-issuer cap defaults (P6-T036, P6-T037).

## Cross-phase prerequisites

With `phase_gating: "dependencies"` (17 §E), these are explicit `depends_on` entries on the tasks below; this table is the summary.

| Phase | Tasks relied on | Used by |
|---|---|---|
| P0 | P0-T005 (GPU), P0-T007 (USER: LLM keys), P0-T016 (`Signal` v1), P0-T020 (Compose), P0-T022 (secrets), P0-T024 (13 schemas incl. `treasury`, `hindsight`), P0-T027 (`pit`), P0-T030/P0-T031 (WORM, `audit.llm_call`), P0-T034 (command bus), P0-T036 (WS hub), P0-T042 (LiteLLM + audit callback), P0-T043 (TEI), P0-T044 (`llm-local`), P0-T045 (Grafana), P0-T048/P0-T049 (web client, components), P0-T056 (exposure scan), P0-T068 (live gateway smoke) | P6-T001, T004–T012, T015, T023, T027, T041–T043, T047, T058, T069, T070 |
| P1 | P1-T006 (quota tracker), P1-T007 (provenance), P1-T013 (bars), P1-T029 (DefiLlama client), P1-T045 (alert fan-out), P1-T060 (alert path verified) | P6-T010, T014, T015, T035, T061 |
| P2 | P2-T003/P2-T004 (strategy base, manifest), P2-T010/P2-T011 (risk policy, L0 ceilings), P2-T017 (M11 RiskGate), P2-T019 (tighten/loosen + C3), P2-T031 (kill switch), P2-T033 (modes), P2-T035 (Telegram C3), P2-T046/P2-T107 (MLflow), P2-T114 (gate evaluator), P2-T125/P2-T128 (tier A) | P6-T009, T016, T017, T020, T021, T024, T031, T033, T034, T038, T046 |
| P3 | P3-T018 (internal-transfer matcher) | P6-T037 |
| P4 | P4-T025 (provenance gate), P4-T028 (registry v1, `models.registry`), P4-T029 (decision-svc stage 1), P4-T031/P4-T032 (RAG), P4-T040 (sentiment/regime), P4-T062 (`models.label` + `models.label.add`) | P6-T005, T006, T014, T018, T019, T023, T024, T043, T051 |
| P5 | P5-T013 (signer), P5-T016 (simulation), P5-T020 (cost gate), P5-T022 (wallet view), P5-T026 (depeg/exploit monitors), P5-T028 (sweeps, kill freeze), P5-T029 (task queue), P5-T050 (D18 view) | P6-T036–P6-T038, T040, T045, T047 |
| P7 (downstream) | Consumes P6-T065 soak results and LLM-signal strategies on paper | P6-T065 hand-over note |
| P8 (downstream) | Agents and memory callable from MCP; prompt-injection suite reused | P6-T054 |

