---
id: P2-T008
kind: task
title: Strategy templates batch 1: core trading styles
phase: 2
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T003, P2-T004]
requirements: [R2.02, R2.03]
roadmap_todos: [T2.21]
modules: [M0]
dashboards: [D03]
branch: p2/P2-T008-templates-core-styles
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

# P2-T008 · Strategy templates batch 1: core trading styles

## Goal / expected outcome

Templates for scalping (tick/L2), intraday, EMA/MA crossover, trend on majors (vol-targeted), mean reversion, breakout and swing/position exist under `packages/mt_strategy/templates/`, each with a parameter schema that drives the UI `ParamForm` and Optuna.

## Context & references

- Roadmap: [R2.02, R2.03](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.21
- Spec: [03 M0 template list](../../../docs/03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe) · [14 §3 evidence + priority](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) · [14 §4 regime filters, sizing, stops](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06)
- UI: [D03 builder Template tab](../../../docs/ui/dashboards/D03-strategies.md)
- Related: P2-T003 base classes, P2-T013 sizing models, P2-T028 execution algos; Part B's lab runs the template backtests.

## Requirements

- Each template: `strategy.py` (MTStrategy subclass), `manifest.template.yaml` (params with types/ranges/defaults, `priority`, `evidence`, default `counterparty`/`benchmark` suggestions), README with evidence summary.
- Trend on majors: daily/4h, long only above slow MA or positive 30–90d momentum, shorts capped, vol target 15–20% annualised from 30–60d realised vol, ATR trailing stop 2–4× daily ATR, P1.
- Scalping: tick/L2 driven, flagged 'deep books only'; intraday: session-aware; breakout + mean reversion: P3 per 14 §3.
- Every template fixes the exit plan at entry (stop, target, time stop) in the `OrderIntent`.
- Params flagged `risk_increasing` where they raise size/leverage.

## ToDo

- [ ] Implement the 7 templates
- [ ] Parameter schemas + JSON Schema export via P2-T004
- [ ] Register templates in `/strategies/templates` with evidence/priority
- [ ] Smoke backtest each template on 1 month of recorded data (Nautilus BacktestEngine) in CI with a tiny fixture dataset
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Template tests: each creates a valid manifest and runs a backtest to completion on fixture data (D03 acceptance 1).
- Unit: regime filter (trend long only above slow MA) blocks entries below it.
- Unit: exit plan present on every emitted intent.

### Scenarios
- Given the trend template on BTCUSDT 4h, when price is below the slow MA, then no long entries are emitted.
- Given the scalping template on an instrument without L2, when saved, then validation fails with `TimeframeUnavailable`.

### Stress / failure injection
- Run all 7 templates over 1 year of 1m bars in CI nightly; no exceptions; runtime recorded.

## Acceptance criteria

- [ ] 7 templates with schemas and READMEs
- [ ] Each passes the template test
- [ ] Evidence and priority visible via `/strategies/templates`
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Weekend/thin-hours on 24/7 crypto: daily bars use a fixed UTC cut (14 §4 porting pitfalls).
- Instrument precision: sizes rounded down to venue lot size; never up.

## Cardinal rules (do NOT)

- Do NOT hard-code sizes or venue fees in templates; sizing comes from M11 models and costs from M16.
- Do NOT add a template for any X/Never pattern.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/ui/dashboards/D03-strategies.md`: template list matches the shipped catalogue (see P2-B054).
- `docs/03-build-spec.md` M0: link templates folder.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.21 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T008-templates-core-styles`
- PR title: `P2-T008: Strategy templates batch 1: core trading styles`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T008` run

## Progress log

- 2026-10-21 00:00 · planner · created
