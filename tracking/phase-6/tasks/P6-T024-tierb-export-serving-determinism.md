---
id: P6-T024
kind: task
title: Export own heads and serve them in decision-svc with determinism controls
phase: 6
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T022, P6-T023, P6-T018, P2-T128]
requirements: [R6.11, R6.10, R6.N3]
roadmap_todos: [T6.24]
modules: [M21]
dashboards: [D10, D09]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [decision-svc, nats, postgres, gpu]
branch: p6/P6-T024-tierb-export-serving-determinism
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/02-v1-architecture.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-T024 · Export own heads and serve them in decision-svc with determinism controls

## Goal / expected outcome

Calibrated heads export to ONNX (FP32) and vLLM adapters; `decision-svc` stage 2 serves them next to SemIf per question, applies calibration and abstention, enforces determinism controls, logs every decision to `audit.tierb_decision`, publishes `dec.tierb.*` and NATS KV `tierb_scores`, and allows a veto only above the calibrated high-precision threshold.

## Context & references

- Roadmap: [R6.11](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.10](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.24
- Spec: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (serving, determinism controls, outputs) · [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models) · [02 F3](../../../docs/02-v1-architecture.md#8-end-to-end-flows) steps 5–7 · [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) (`dec.tierb.*`, KV `tierb_scores`) · [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos) (p95 < 50 ms)
- Cross-phase: P4-T029 (decision-svc stage 1), P2-T128 (tier-A runtime reads KV scores)
- Defaults: [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets) (veto ≥ 0.90 precision, flip rate ≤ 0.1%) · prefix caching off on the decision path (17 §A, P4-B010)
- Depends on (this phase): P6-T022, P6-T023, P6-T018

## Requirements

- Export: `optimum`/`torch.onnx` FP32 graph incl. head; parity test vs PyTorch (max abs diff < 1e-4); artefact hash in `models.registry`.
- Routing: per question → serving model (SemIf or own head) from the registry; candidates/shadow models run alongside without affecting outputs.
- Determinism: FP32 head, pinned revision, batch size 1 or fixed padded batch, prefix caching off, logged `prompt_hash` (state hash), `model_revision`, `question_version` on every decision.
- Output: option probabilities (calibrated), `abstain` flag, latency; `audit.tierb_decision` row; `dec.tierb.{question}.{subject}`; KV `tierb_scores` for tier A.
- Veto: `risk.event` only when the question is a veto question, the model is production, and p ≥ `veto_threshold` (calibrated; default precision ≥ 0.90, 16 §2.10).
- Backtest mode: CPU ONNX FP32 path selected automatically when called from the lab (reproducible).
- SLO (R6.N3, 17 §B P6-B002): ~2–12 ms typical, p95 < 50 ms per decision on GPU for the 0.6B head; CPU 100–400 ms; decision-svc is never on the order path (tier A reads cached KV scores).
- Shared-prefix scoring is never used here; any score from an offline shared-prefix run is marked non-deterministic and refused by the router.

## ToDo

- [ ] Exporter + parity tests.
- [ ] decision-svc model router + calibration/abstention layer.
- [ ] Audit writer and NATS/KV publishing (extend P4).
- [ ] Veto gate wiring to `risk.event`.
- [ ] Lab client forcing CPU ONNX FP32.
- [ ] Tests; docs.

## Verification

### Tests
- Parity: ONNX vs PyTorch probabilities on 1,000 states (< 1e-4).
- Unit: abstention and veto threshold logic.
- Integration: `text.doc.new` → own head decision → KV updated → tier A reads feature.
- Determinism smoke (full test in P6-T057).

### Scenarios
- Given a production `veto` head with p=0.93 ≥ 0.9 threshold, then a `risk.event` is published; with p=0.85 nothing is published.
- Given a candidate model in shadow, then its outputs are logged but never reach KV.
- Given a lab backtest, then decisions come from CPU ONNX FP32 regardless of GPU availability.

### Stress / failure injection
- Covered by P6-T058 (load, SLO) and P6-T064 (GPU loss).

## Acceptance criteria

- [ ] Own heads served for ≥ 1 question in production-candidate state.
- [ ] Every decision audited with hashes/revisions.
- [ ] Veto impossible below threshold (test).

## Exceptions & edge cases

- Model file missing/corrupt: router falls back to SemIf for that question and alerts.
- Restart: KV scores retained; stale scores carry `as_of` so tier A can ignore stale ones.

## Cardinal rules (do NOT)

- Do NOT let tier B place orders; veto goes through `risk.event` → M11.
- Do NOT call any remote API from the decision path.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `journal.*`, policy changes); corrections are new rows referencing the original (15 §2).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: export/parity numbers.
- `docs/02-v1-architecture.md` F3: stage-2 routing.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.24 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T024-tierb-export-serving-determinism`
- PR title: `P6-T024: Export own heads and serve them in decision-svc with determinism controls`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T024` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (latency per 17 §B (R6.N3), veto default 0.90 and prefix caching off (16 §2.10, 17 §A); cross-phase deps P4-T029/P2-T128; run fields)
