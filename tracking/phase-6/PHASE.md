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
updated: 2026-10-21
---

# Phase 6 · AI decision layer, memory, models, anomalies & treasury

## Summary

From the [roadmap](../../docs/roadmap/phase-6-ai-models-treasury.md): ask for an analysis of any instrument and get a sourced `Signal`; agents learn from settled outcomes; our own tier-B decision models are trained, benchmarked and promoted only through gates; anomalies are explained on Telegram; idle capital earns under the on-chain cost gate.

The 66 tasks are organised in eight workstreams:
1. **Agents & LLM plumbing:** Signal v2, the LLM-call audit and prompt registry, the tool belt, the debate graph, the scheduler and triggers, budgets with local fallback.
2. **Memory:** Hindsight slim, point-in-time recall, settlement and reflection.
3. **Anomalies:** detectors and the explain agent.
4. **LLM-signal strategies:** the template and the post-cutoff gate.
5. **Tier B stage 2:** question registry v2, the label store and labelling queue, the dataset builder, trainer, calibration, serving, the shadow sampler and threshold tuner, the bake-off, promotion gates, and the nightly and monthly flows.
6. **Treasury & hold-and-earn:** policy and allow-list, yields, the allocator, sweeps and reserve, the execution path, the node model, the DAO monitor.
7. **UI:** D09, D10 (two parts), D18 earn.
8. **Optional modules (low priority):** Hummingbot, social drafts, credibility, crowd-sim, LightRAG.

VERIFY, RUN and the exit demo close the phase.

## Entry criteria

- [ ] Phase 5 done (signer, cost gate and wallet view passing their test suites; D18 view live)
- [ ] P4 text + RAG + SemIf running ≥ 4 weeks (teacher/label data accumulating)
- [ ] P2 lab, tier-A pipeline, MLflow registry and promotion gates available
- [ ] P0 gateway (LiteLLM ≥ 1.83, pinned) with per-role virtual keys, TEI, WORM audit machinery and `mt_api` C0–C3 in place
- [ ] GPU decision taken (T0.01); if no GPU, accept that the tier-B SLO can't be met and SemIf may stay in production

## Exit criteria

- [ ] 1. Ask for an analysis of any instrument → a sourced `Signal` with provenance, visible in D09 (P6-T062, P6-T066)
- [ ] 2. An anomaly is explained on Telegram (P6-T061, P6-T066)
- [ ] 3. The bake-off report names a production tier-B model (or keeps SemIf) with calibration evidence (P6-T059, P6-T066)
- [ ] 4. Idle stables are allocated within the allow-list after the cost gate; the treasury reserve holds (P6-T060, P6-T066)
- [ ] All phase-6 tasks are done or cancelled (optional items cancelled per P6-T003 decisions)
- [ ] No open S1/S2 bugs in phase 6

## Workstreams

| Workstream | Tasks |
|---|---|
| Your actions (USER) | P6-T001 budgets · P6-T002 Tally/FinMMEval/licences · P6-T003 optional modules · P6-T034 treasury policy (C3) · P6-T044 labelling queue · P6-T049 social drafts (optional) |
| Build: agents & LLM plumbing | P6-T004 Signal v2 · P6-T005 LLM-call audit + prompt registry · P6-T006 tool belt · P6-T007 debate graph · P6-T008 scheduler/triggers/API · P6-T009 budgets + fallback |
| Build: memory | P6-T012 Hindsight client + PIT recall · P6-T013 settlement + reflection |
| Build: anomalies | P6-T014 detectors · P6-T015 explain agent |
| Build: LLM-signal strategies | P6-T016 template · P6-T017 post-cutoff gate |
| Build: tier B stage 2 | P6-T018 question registry v2 · P6-T019 label store + queue API · P6-T020 dataset builder · P6-T021 trainer · P6-T022 calibration · P6-T024 export + serving · P6-T025 shadow sampler · P6-T026 threshold tuner · P6-T028 Laya-ft · P6-T029 bake-off harness · P6-T030 promotion gates · P6-T031 nightly distillation · P6-T032 monthly fine-tune |
| Build: treasury | P6-T033 policy + allow-list · P6-T035 DefiLlama yields · P6-T036 allocator · P6-T037 sweeps + reserve · P6-T038 earn execution · P6-T039 node/validator model · P6-T040 DAO monitor |
| Build: UI | P6-T041 D09 · P6-T042 D10 registry/questions/bake-off/gateway · P6-T043 D10 memory/RAG/labelling/shadow · P6-T045 D18 earn |
| Build: optional (low) | P6-T046 Hummingbot + D11 · P6-T047 social drafts · P6-T048 credibility + shill-burst · P6-T050 crowd-sim · P6-T051 LightRAG |
| Ops | P6-T010 spend panel + alerts · P6-T011 Hindsight container · P6-T023 GPU serving · P6-T027 bake-off containers |
| Verify | P6-T052 audit + scheduler · P6-T053 budgets · P6-T054 prompt injection · P6-T055 PIT memory · P6-T056 label provenance · P6-T057 determinism · P6-T058 latency SLO · P6-T059 bake-off review · P6-T060 treasury · P6-T061 seeded anomaly · P6-T062 E2E F4 · P6-T063 LLM-signal gate · P6-T064 degraded modes · **P6-T066 exit demo** |
| Run | P6-T065 start the 4-week distillation + LLM-signal paper soak (completion checked at P7 entry) |
| Gaps | P6-B001 … P6-B016 |

## Critical path

P6-T004 → P6-T005 → P6-T006 → P6-T007 → (P6-T011 → P6-T012) → P6-T013 → (P6-T018 → P6-T019) → P6-T020 → P6-T021 → P6-T022 → (P6-T023) → P6-T024 → (P6-T027 → P6-T028) → P6-T029 → P6-T030 → P6-T031 → P6-T059 → P6-T065 → P6-T066

Parallel track (treasury): P6-T033 → P6-T034 (USER, C3) → P6-T035 → P6-T036 → P6-T037 → P6-T038 → P6-T060 → P6-T066.

The settlement step (P6-T013) needs elapsed time: a Signal must reach its horizon before it yields a label. So start P6-T007/P6-T008 early and let short-horizon scheduled runs accumulate teacher data while the tier-B pipeline is built.

## Traceability

| Requirement | Tasks |
|---|---|
| R6.01 | P6-T004, P6-T006, P6-T007, P6-T008, P6-T041, P6-T054, P6-T062, P6-T066 |
| R6.02 | P6-T006, P6-T008, P6-T052 |
| R6.03 | P6-T005, P6-T052 |
| R6.04 | P6-T011, P6-T012, P6-T013, P6-T043, P6-T055, P6-T062, P6-T064 |
| R6.05 | P6-T014, P6-T015, P6-T054, P6-T061, P6-T066 |
| R6.06 | P6-T016, P6-T017, P6-T063, P6-T065 |
| R6.07 | P6-T001, P6-T009, P6-T010, P6-T042, P6-T053, P6-T064 |
| R6.10 | P6-T020, P6-T021, P6-T022, P6-T024, P6-T059, P6-T066 |
| R6.11 | P6-T023, P6-T024, P6-T057, P6-T058, P6-T064 |
| R6.12 | P6-T002, P6-T027, P6-T028, P6-T029, P6-T030, P6-T042, P6-T059, P6-T066 |
| R6.13 | P6-T018, P6-T019, P6-T020, P6-T025, P6-T026, P6-T032, P6-T043, P6-T044, P6-T056 |
| R6.14 | P6-T013, P6-T020, P6-T030, P6-T031, P6-T042, P6-T059, P6-T062, P6-T065 |
| R6.20 | P6-T033, P6-T034, P6-T038, P6-T045, P6-T060, P6-T066 |
| R6.21 | P6-T034, P6-T035, P6-T036, P6-T060, P6-T066 |
| R6.22 | P6-T033, P6-T034, P6-T037, P6-T060, P6-T066 |
| R6.23 | P6-T002, P6-T039, P6-T040, P6-T060 |
| R6.24 | P6-T033, P6-T036, P6-T037, P6-T038, P6-T045, P6-T060, P6-T064, P6-T066 |
| R6.30 | P6-T003, P6-T046 |
| R6.31 | P6-T003, P6-T047, P6-T048, P6-T049 |
| R6.32 | P6-T003, P6-T050, P6-T051 |
| R6.40 | P6-T041, P6-T042, P6-T043, P6-T045, P6-T062, P6-T066 |

| Roadmap ToDo | Tasks |
|---|---|
| T6.01 | P6-T001 |
| T6.02 | P6-T044 |
| T6.03 | P6-T034 |
| T6.04 | P6-T003 |
| T6.05 | P6-T049 |
| T6.20 | P6-T004, P6-T005, P6-T006, P6-T007, P6-T008 |
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
| T6.40 | P6-T011, P6-T023, P6-T027 |
| T6.41 | P6-T009, P6-T010, P6-T053 |
| T6.60 | P6-T059 |
| T6.61 | P6-T057, P6-T058 |
| T6.62 | P6-T056 |
| T6.63 | P6-T055 |
| T6.64 | P6-T060 |
| T6.65 | P6-T054 |
| T6.80 | P6-T065 |

Supporting items without a roadmap ToDo:
- P6-T002 (external access, USER).
- P6-T052, P6-T061, P6-T062 and P6-T063 (the "Verified by" checks for R6.01–R6.03, R6.05 and R6.06).
- P6-T064 (degraded modes, 02 §9.3).
- P6-T066 (exit demo).

See P6-B001.

## Planning notes & risks

- **Optional items (P6-T046–P6-T051)** are low priority. P6-T003 records your decision. Cancel each item you decline so it doesn't hold the phase open.
- **Elapsed time:**
  - Tier-B training needs settled teacher decisions (P6-T013). Run short-horizon scheduled analyses as early as possible.
  - The 4-week soak (P6-T065) is only **started** here. "Four clean weeks" is checked at P7 entry, so the phase can close.
- **GPU dependency:** without a 16–24 GB GPU, P6-T021 training is impractical and the p95 < 50 ms SLO (P6-T058) can't be met. In that case the valid outcome of exit criterion 3 is "keep SemIf". Record it in P6-T059.
- **Distillation copying teacher bias** (roadmap risk). Mitigations:
  - outcome-corrected labels (P6-T020);
  - worst-fold promotion against a frozen baseline (P6-T030);
  - shadow outputs never used as labels (P6-T019, P6-T056).
- **LLM spend creep:** event-triggered runs only (P6-T008), per-role and monthly limits with local fallback (P6-T009), alerts (P6-T010).
- **DeFi protocol risk:**
  - allow-list and C3 (P6-T033, P6-T034);
  - ≤ 20% per protocol and the reserve band (P6-T036, P6-T037);
  - depeg/exploit auto-exits (P6-T038);
  - verification on forks only (P6-T060).
- **Point-in-time risk in memory:** Hindsight consolidation could leak the future into backtests. P6-B016 (S2) must be closed by P6-T012 and proven by P6-T055.
- **Assumed defaults until the docs decide:**
  - gate thresholds (P6-B015): target precision 0.75, veto precision 0.90, ECE ≤ 0.05, flip rate ≤ 0.1%, shadow ≥ 14 days;
  - HLP cap (P6-B013);
  - venue cap 25% (P6-B008).
- **Kev-4B/9B:** no source or licence is documented (P6-B003). It's excluded from the bake-off unless P6-T002 finds a free, self-hostable release.
- **`audit.llm_call` ownership:** may move earlier (P6-B010). If P0/P2 build the writer, re-scope P6-T005 to the prompt registry and `training_cutoff` only.

## Cross-phase prerequisites

| Phase | Roadmap IDs relied on | Used by |
|---|---|---|
| P0 | R0.02 (Compose, digests), R0.04 (`pit`), R0.05 (provenance columns), R0.07 (WORM), R0.08 (`mt_api` C0–C3, `audit.command`), R0.09 / T0.45 (LiteLLM per-role keys, TEI), R0.10 (Grafana/Loki), T0.21 (`mt_core.Signal` v1), T0.01 (GPU) | Almost every P6 task |
| P1 | R1.02 (bars), R1.08 (quota tracker), R1.09 (provenance), R1.14 (Telegram/ntfy alerts) | P6-T010, P6-T014, P6-T035 |
| P2 | R2.01/R2.02/R2.04 (templates, manifest), R2.06 (lifecycle gates), R2.10 (M11), R2.19 (C3 change control, hard ceilings), R2.20 (modes), R2.42/R2.43 (validation harness), R2.44 (MLflow), R2.47 (tier-A pipeline), R2.52 (Telegram bot) | P6-T016, P6-T017, P6-T030, P6-T031, P6-T033, P6-T038 |
| P3 | Journal (internal-transfer tagging, income events) | P6-T037, P6-T038 |
| P4 | R4.03 (Telegram gate), R4.06 (text chain), R4.07 (RAG), R4.08 (events), R4.10 (calendars), R4.11 (sentiment/regime), R4.12 (SemIf, question registry v1, decision-svc), R4.N1 (untrusted text) | P6-T006, P6-T014, P6-T018, P6-T024, P6-T029 |
| P5 | R5.02/R5.03 (signer, hard blocks), R5.04 (cost gate), R5.05 (wallet view), R5.06 (depeg/exploit monitors), R5.07 (sweeps), R5.20 (task queue), R5.23 (D18 view), R5.N2 (kill freezes treasury) | P6-T033–P6-T040, P6-T045 |
| P7 (downstream) | Consumes P6-T065 soak results and LLM-signal strategies on paper | P6-T065 hand-over note |
| P8 (downstream) | Agents and memory callable from MCP; prompt-injection suite reused | P6-T054 |
