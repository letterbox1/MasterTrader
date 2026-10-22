---
id: P6-T029
kind: task
title: Bake-off harness, FinMMEval check and report
phase: 6
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T022, P6-T024, P6-T027, P6-T028, P6-T068]
requirements: [R6.12]
roadmap_todos: [T6.25]
modules: [M21, M7]
dashboards: [D10]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [mlflow, gpu, postgres]
branch: p6/P6-T029-bakeoff-harness-report
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

# P6-T029 · Bake-off harness, FinMMEval check and report

## Goal / expected outcome

One command (`models.bakeoff.run`, C1) evaluates every contender — own Qwen-LoRA head (0.6B/1.7B), fine-tuned Laya, Clef-flash, Kev-4B/9B (only if P6-T068 cleared it), SemIf zero-shot, JSON generation — on our walk-forward test folds and the CLEF-2026 FinMMEval Buy/Hold/Sell task, and produces a report with Brier/ECE per regime, coverage at target precision, latency p50/p95 and flip rate.

## Context & references

- Roadmap: [R6.12](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.25
- Spec: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (contenders, data, metrics, promotion only via gates) · [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models)
- UI: [D10](../../../docs/ui/dashboards/D10-models-memory.md) Bake-off tab (`/models/benchmarks`)
- Exit: [roadmap §6 exit criteria](../../../docs/roadmap/phase-6-ai-models-treasury.md#6-exit-criteria-demo) item 3
- Kev: included only if P6-T068 cleared it ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P6-B003)
- Defaults the report checks against: [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets)
- Depends on (this phase): P6-T022, P6-T024, P6-T027, P6-T028, P6-T068. FinMMEval data from P6-T002 is used when provided; the loader is tested on a format fixture, so the harness doesn't wait for it.

## Requirements

- Common contender interface: `predict(state, question) → probs, latency`; contenders started/stopped via P6-T027 profile.
- Data: our final walk-forward test folds (never used for tuning) + FinMMEval Buy/Hold/Sell (if access from P6-T002).
- Metrics: accuracy, log-loss, Brier, ECE per regime (trend/range/crisis), coverage at target precision, latency p50/p95 (same hardware, batch 1), flip rate (repeat each input 5× incl. across restarts).
- Report: HTML + JSON in MLflow; each contender flagged against the 16 §2.10 defaults (coverage at ≥ 0.75 precision, ECE ≤ 0.05, flip rate ≤ 0.1%); `/models/benchmarks` API; a recommendation per question (production model or keep SemIf) with evidence; JSON-generation parse-failure rate.
- Runs reproducibly from a config (seed, folds, contenders) and records hardware/driver versions.

## ToDo

- [ ] Harness `mt_models.bakeoff` + contender adapters.
- [ ] FinMMEval loader (licence-respecting, local files only).
- [ ] Metrics + report generator.
- [ ] `models.bakeoff.run` command + `/models/benchmarks` query.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: metric functions vs references; flip-rate computation.
- Integration: harness on two toy contenders produces a report with all metrics.
- API: command level C1, job visible on WS `lab.job`.

### Scenarios
- Given all contenders available, then the report ranks them per question with CIs and names a recommended production model or SemIf.
- Given a contender container fails mid-run, then the report marks it `incomplete` and the run still finishes for others.

### Stress / failure injection
- Full bake-off on 5 questions completes within one overnight window (< 8 h) with GPU lock respected.

## Acceptance criteria

- [ ] Bake-off report generated for ≥ 3 questions incl. FinMMEval (or documented absence).
- [ ] Report reviewed in P6-T059.

## Exceptions & edge cases

- Different context limits per contender: state ≤ 320 tokens fits all; record any truncation.

## Cardinal rules (do NOT)

- Do NOT promote anything from the harness directly; promotion only via P6-T030 gates.
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots, user tokens, sybil/multi-wallet or fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: bake-off results summary.
- `docs/02-v1-architecture.md` §7.1: `/models/benchmarks` payload.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.25 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T029-bakeoff-harness-report`
- PR title: `P6-T029: Bake-off harness, FinMMEval check and report`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T029` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (Kev via P6-T068; FinMMEval optional input (keys/data last); report flags 16 §2.10 thresholds; run fields)
