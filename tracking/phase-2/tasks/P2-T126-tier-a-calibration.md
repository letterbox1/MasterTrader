---
id: P2-T126
kind: task
title: Tier A calibration (isotonic/Platt) with Brier and ECE
phase: 2
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T125]
requirements: [R2.47]
roadmap_todos: [T2.30]
modules: [M21]
dashboards: [D04]
tools: [uv]
mcp: []
env: []
services: []
branch: p2/P2-T126-tier-a-calibration
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T126 · Tier A calibration (isotonic/Platt) with Brier and ECE

## Goal / expected outcome

Every tier-A model is calibrated on a time-ordered holdout with isotonic or Platt scaling, and its Brier score, ECE and reliability curve are recorded, so the probability/edge it hands to M11 sizing means what it says.

## Context & references

- Roadmap: [R2.47](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.30
- [10 §4.3 calibration](../../../docs/10-memory-rag-and-models.md#43-design) · [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models) (output is a calibrated probability/edge, which M11 sizes)

## Requirements

- Fit isotonic (default when ≥ 1,000 holdout samples) or Platt on the calibration holdout only; choose by lower holdout Brier.
- Report Brier, ECE (15 equal-mass bins), reliability curve data, per-regime ECE (regime_v1 from P2-T111) on the test split.
- Calibrator is part of the exported model graph (compiled with the model in P2-T127) or a lookup table applied in-process (≤ 1 µs).
- Acceptance thresholds configurable; default: ECE ≤ 0.05 on test, else model not promotable.

## ToDo

- [ ] Implement `mt_models/tier_a/calibrate.py`
- [ ] Log metrics + reliability data to MLflow
- [ ] Tests
- [ ] Doc thresholds

## Verification

### Tests
- Unit: isotonic on a miscalibrated synthetic model reduces ECE; Platt on a sigmoid-shaped one.
- Unit: calibrator never sees test-split data (asserted by index).

### Scenarios
- Given a holdout with < 200 samples, then calibration is refused with 'insufficient holdout'.

### Stress / failure injection
- n/a: offline step on small holdouts; runtime negligible.

## Acceptance criteria

- [ ] Brier, ECE and reliability recorded for every model
- [ ] Calibrator exported with the model
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Regime with too few samples for ECE: reported as 'insufficient' not 0.

## Cardinal rules (do NOT)

- Do NOT calibrate on the test split.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: calibration defaults and ECE threshold.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.30 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T126-tier-a-calibration`
- PR title: `P2-T126: Tier A calibration (isotonic/Platt) with Brier and ECE`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T126` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields (no decision change))
