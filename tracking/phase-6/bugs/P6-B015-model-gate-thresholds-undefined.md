---
id: P6-B015
kind: gap
title: Tier-B promotion/abstention/veto thresholds have no numbers (target precision, ECE max, flip-rate max, veto precision)
phase: 6
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.10, R6.14]
roadmap_todos: []
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p6/P6-B015-model-gate-thresholds-undefined
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md]
doc_sync_status: done
found_in: docs/10-memory-rag-and-models.md §4.3; docs/03-build-spec.md M21
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-B015 · Tier-B promotion/abstention/veto thresholds have no numbers (target precision, ECE max, flip-rate max, veto precision)

## Goal / expected outcome

The docs agree and are specific enough to build from: documented defaults (user-editable) for each threshold.

## Context & references

- Found in: docs/10-memory-rag-and-models.md §4.3; docs/03-build-spec.md M21
- [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) ('target precision', 'calibrated high-precision threshold') · [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models)
- Affects: P6-T022, P6-T026, P6-T030, P6-T057

## Requirements

- **Steps to reproduce:** read docs/10-memory-rag-and-models.md §4.3; docs/03-build-spec.md M21 and compare it with the cross-referenced sections listed under Context.
- **Expected:** documented defaults (user-editable) for each threshold.
- **Actual:** Docs require abstention 'at a target precision', veto 'above a calibrated high-precision threshold' and promotion 'via gates', but give no default numbers for precision targets, ECE/Brier limits, flip-rate limit or shadow duration.
- **Suggested fix:** Proposed defaults (used by P6 tasks until decided): target precision 0.75, veto precision 0.90, ECE ≤ 0.05, flip rate ≤ 0.1%, shadow ≥ 14 days, worst fold ≥ frozen baseline.
- **Impact:** Gates could be set arbitrarily per implementer (severity S3)

## ToDo

- [x] Decision recorded in docs/17 (17 §C P6-B015): tier-B threshold defaults
- [x] Owning docs carry it: 16 §2.10 (auto-decide coverage at ≥ 0.75 precision, veto ≥ 0.90, ECE ≤ 0.05, flip rate ≤ 0.1%, ≥ 14 days in shadow); 10 §4.3 (abstention, promotion, veto, determinism); roadmap R6.13/R6.14; 02 §7.2 (`models.question.update` below the default bar is C3)
- [x] Affected tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P6-T018 (registry), P6-T022 (calibration), P6-T026 (tuner), P6-T030 (promotion gates), P6-T057/P6-T059 (verification)
- [x] Decision and source noted in the progress log

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (16 §2.10 (auto-decide coverage at ≥ 0.75 precision, veto ≥ 0.90, ECE ≤ 0.05, flip rate ≤ 0.1%, ≥ 14 days in shadow); 10 §4.3 (abstention, promotion, veto, determinism); roadmap R6.13/R6.14; 02 §7.2 (`models.question.update` below the default bar is C3))
- [x] Affected tasks consistent with it (P6-T018 (registry), P6-T022 (calibration), P6-T026 (tuner), P6-T030 (promotion gates), P6-T057/P6-T059 (verification))
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- Until resolved, dependent tasks use the conservative interpretation stated under Suggested fix and note it in their progress log.

## Cardinal rules (do NOT)

- Do NOT silently pick a number in code; record the decision in the doc first.
- Do NOT edit docs owned by another phase's planner from a P6 branch without the owner's agreement; propose the change in the PR description.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md`: resolve the inconsistency.

## Branch & PR

- Branch: `p6/P6-B015-model-gate-thresholds-undefined`
- PR title: `P6-B015: Tier-B promotion/abstention/veto thresholds have no numbers (target precision, ECE max, flip-rate max, veto precision)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-B015` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · resolved by docs/17 §C P6-B015: tier-B threshold defaults. Docs now carry it: 16 §2.10 (auto-decide coverage at ≥ 0.75 precision, veto ≥ 0.90, ECE ≤ 0.05, flip rate ≤ 0.1%, ≥ 14 days in shadow); 10 §4.3 (abstention, promotion, veto, determinism); roadmap R6.13/R6.14; 02 §7.2 (`models.question.update` below the default bar is C3). Implementation owned by P6-T018 (registry), P6-T022 (calibration), P6-T026 (tuner), P6-T030 (promotion gates), P6-T057/P6-T059 (verification). Root cause: the docs required thresholds without numbers.
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §C P6-B015); docs updated: 16 §2.10 tier-B thresholds, 10 §4.3, roadmap R6.13/R6.14, 02 §7.2 models.question.update; implementation owned by P6-T018, P6-T022, P6-T026, P6-T030, P6-T057, P6-T059
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · doc sync done: docs already updated in this wave
