---
id: P2-T114
kind: task
title: Validation suite orchestrator, report and gate evaluator
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T109, P2-T110, P2-T111, P2-T112, P2-T113]
requirements: [R2.42, R2.43, R2.06]
roadmap_todos: [T2.27]
modules: [M7, M0]
dashboards: [D03, D04]
branch: p2/P2-T114-validation-suite-and-gates
pr: ""
doc_sync: [docs/03-build-spec.md, docs/ui/dashboards/D03-strategies.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T114 · Validation suite orchestrator, report and gate evaluator

## Goal / expected outcome

`lab.validate.run` runs every harness section on truth results and produces one `ValidationReport` plus a per-gate pass/fail list that the lifecycle (part A) and D03 Gates tab consume, so 'validated' means the same thing everywhere.

## Context & references

- Roadmap: [R2.42, R2.43, R2.06](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.27 · exit criterion 1 ('the validation report shows all harness sections')
- [03 §8 gates](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) · [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [02 F7 lifecycle](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Part-A prerequisite: lifecycle state machine + `strategy.promote` gate checks (T2.20 in part A (P2-T001–T099)) call this evaluator
- [D03 Gates tab](../../../docs/ui/dashboards/D03-strategies.md) · [D04 Gates tab](../../../docs/ui/dashboards/D04-research-lab.md)

## Requirements

- Sections: summary metrics, walk-forward (worst fold, positive share), purged K-fold, MC permutation, bootstrap CI, deflated Sharpe + trial count, per-year, per-regime, cost stress 2×/3×, benchmark, look-ahead/recursive/repaint analysers, LLM leakage review, PIT audit, reproduction record.
- Gate evaluator (configurable per strategy, defaults from 03 §8/14 §6): OOS beats benchmark after measured costs; MC p < 0.05; DSR > threshold (P2-B050); analysers clean; leakage review clean or waived; each year and regime profitable (or regime-only label); survives 2× and 3× costs; worst fold rule; truth-only.
- Gates 4 (LLM post-cutoff), 5 (paper period) and 6 (live/capital steps) are reported as `n/a` or `pending` with the reason; paper-period tracking is fed from part A's paper runs.
- Output `ValidationReport` JSON (versioned) + HTML/PDF export for D04 'Export report'; stored on `strategy.experiment` and MLflow.
- API: `/strategies/{id}?gates=1` returns the latest evaluated gates per version (via P2-T117).

## ToDo

- [ ] Implement `mt_lab/validation/suite.py` orchestrating sections as sub-jobs with a dependency graph
- [ ] Implement `mt_lab/gates.py` evaluator with per-strategy thresholds (from manifest/policy) and reasons
- [ ] Implement report rendering (JSON + HTML via Jinja; PDF via WeasyPrint)
- [ ] Expose evaluator to part A's lifecycle (`can_promote(strategy_version, target_stage)`)
- [ ] Tests + docs

## Verification

### Tests
- Unit: gate evaluator on synthetic section results covers every pass/fail branch and reason text.
- Integration: full suite on the EMA template fixture produces a report with every section present.
- Contract test: lifecycle (part A) refuses `validated` when any required gate fails.

### Scenarios
- Given a screener-only result, when gates are evaluated, then every performance gate is 'not eligible: screener'.
- Given one section failed to run (crash), then the report shows it as 'error' and the overall verdict is fail.
- Given a waived leakage item, then the gate shows 'waived by user (reason, time)' with an audit link.

### Stress / failure injection
- Run the full suite for 3 strategies concurrently on 4 workers; total wall-clock recorded; no section starved beyond the 2 h cap.

## Acceptance criteria

- [ ] Report contains all harness sections listed above
- [ ] Gate evaluator used by lifecycle and D03
- [ ] Exportable HTML/PDF
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Thresholds tightened later: old reports keep their evaluated thresholds; re-evaluation creates a new gate record.
- LLM-signal strategies (P6) need post-cutoff evaluation; for P2 that gate is `n/a` unless the manifest declares an LLM component.

## Cardinal rules (do NOT)

- Do NOT let any gate default to pass when its section is missing or errored.
- Do NOT count screener results for gates.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` §8: link to the gate evaluator defaults.
- `docs/ui/dashboards/D03-strategies.md`: Gates tab fields match the evaluator output.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.27 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T114-validation-suite-and-gates`
- PR title: `P2-T114: Validation suite orchestrator, report and gate evaluator`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T114` run

## Progress log

- 2026-10-21 00:00 · planner · created
