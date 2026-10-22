---
id: P6-T022
kind: task
title: Tier B calibration, abstention thresholds and calibration report
phase: 6
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T021]
requirements: [R6.10]
roadmap_todos: [T6.24]
modules: [M21, M7]
dashboards: [D10]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [mlflow]
branch: p6/P6-T022-tierb-calibration-abstention
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T022 · Tier B calibration, abstention thresholds and calibration report

## Goal / expected outcome

Each trained head is post-hoc calibrated (temperature or isotonic) on a walk-forward holdout, gets abstention thresholds at a target precision (abstain is the default), and ships a calibration report (reliability diagram, Brier/ECE per regime, coverage at target precision).

## Context & references

- Roadmap: [R6.10](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.24
- Spec: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (calibration, abstention, coverage) · [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models)
- UI: [D10](../../../docs/ui/dashboards/D10-models-memory.md) Registry detail (reliability diagram)
- Defaults: [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets) ([17 §C](../../../docs/17-decisions-register.md#c-defaults-that-were-n-or-unspecified) P6-B015): auto-decide at ≥ 0.75 precision, veto ≥ 0.90, ECE ≤ 0.05, flip rate ≤ 0.1%
- Depends on (this phase): P6-T021

## Requirements

- Calibrators: temperature scaling (multi-class) and isotonic (one-vs-rest); pick by holdout log-loss; store as part of the model artefact.
- Regimes: `trend|range|crisis` from the P4 regime feature; metrics per regime and overall: accuracy, log-loss, Brier, ECE (15 bins), coverage at target precision.
- Abstention: per question/option thresholds chosen so precision ≥ `target_precision` (from the registry; default 0.75, 16 §2.10) on holdout; below threshold → `abstain`.
- Veto questions: separate high-precision threshold (default precision ≥ 0.90, 16 §2.10) required before any direct veto is enabled.
- Report artefact (HTML + JSON) in MLflow; summary fields written to `models.registry`.

## ToDo

- [ ] `mt_models.tierb.calibrate` + report generator.
- [ ] Threshold search with bootstrap CI.
- [ ] Write thresholds as a proposed question version (applied via C1 in P6-T026/T042).
- [ ] Tests; docs.

## Verification

### Tests
- Unit: ECE computation vs reference; isotonic monotonicity; threshold search returns precision ≥ target on synthetic data.
- Golden: report JSON for a fixed toy model.

### Scenarios
- Given an over-confident head (ECE 0.18), after temperature scaling ECE drops below the gate threshold or the model is marked `not_calibrated`.
- Given a regime with < 50 holdout samples, then its metrics are shown as insufficient, not hidden.

### Stress / failure injection
- n/a: offline batch job; runtime bounded by holdout size (< 5 min per question).

## Acceptance criteria

- [ ] Every candidate head has a calibration report in MLflow and summary in `models.registry`.
- [ ] Abstention thresholds recorded per question.

## Exceptions & edge cases

- Holdout overlaps training horizon (purge failure) → job aborts.
- Regime label missing for a period → bucket `unknown`, reported.

## Cardinal rules (do NOT)

- Do NOT tune thresholds on the final test fold used for promotion.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: calibrator choice and default targets.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.24 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T022-tierb-calibration-abstention`
- PR title: `P6-T022: Tier B calibration, abstention thresholds and calibration report`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T022` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (thresholds = 16 §2.10 defaults (17 §C P6-B015); run fields)
