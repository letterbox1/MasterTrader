---
id: P4-T054
kind: task
title: Feature IC report for the new sentiment, regime, positioning and macro features
phase: 4
type: VERIFY
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T040, P4-T041, P4-T042]
requirements: [R4.11]
roadmap_todos: [T4.64]
modules: [M6]
dashboards: [D04]
branch: p4/P4-T054-verify-feature-ic-report
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T054 · Feature IC report for the new sentiment, regime, positioning and macro features

## Goal / expected outcome

The P2 IC evaluator produces an IC / rank-IC / decay report for every new P4 feature (sentiment per market type, regime labels, event scores, positioning, Fed-path, VIX regime, nowcasts, PM probabilities, vol forecasts) against forward returns/vol at multiple horizons, PIT-correct, with a keep/watch/drop recommendation per feature.

## Context & references

- Roadmap: [R4.11](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.64](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Spec: [03 M6 evaluator](../../../docs/03-build-spec.md#m6-features--mt_features)
- Cross-phase: P2 R2.46 (IC evaluator).

## Requirements

- Horizons: 1 h, 1 d, 5 d (returns) and realised vol for forecasts.
- Purged/embargoed splits; minimum history noted (P4 features have short live history → use backfilled PIT history and flag it).
- Report stored in MLflow + `docs/` summary; Telegram postures are not evaluated (not features).

## ToDo

- [ ] Configure evaluator runs.
- [ ] Generate report.
- [ ] Recommendations per feature.
- [ ] Publish summary.

## Verification

### Tests
- Evaluator sanity: a shuffled-target control gives IC ≈ 0.

### Scenarios
- Given a feature has < 60 days of history, then it is marked 'insufficient' not 'drop'.

### Stress / failure injection
- n/a: offline report.

## Acceptance criteria

- [ ] IC report covers every new feature with a recommendation
- [ ] Shuffled-target control passes
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Backfilled sentiment may suffer source-coverage bias; flag it.

## Cardinal rules (do NOT)

- Do NOT bypass `pit(as_of)` when building the evaluation set.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md`: M6: link the IC report and feature status
- `docs/roadmap/phase-4-intel.md`: tick T4.64 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T054-verify-feature-ic-report`
- PR title: `P4-T054: Feature IC report for the new sentiment, regime, positioning and macro features`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T054` run

## Progress log

- 2026-10-21 00:00 · planner · created
