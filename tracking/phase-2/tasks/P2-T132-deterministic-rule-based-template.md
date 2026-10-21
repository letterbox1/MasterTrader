---
id: P2-T132
kind: task
title: Deterministic rule-based template on the shared libraries
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T130, P2-T131]
requirements: [R2.48, R2.02]
roadmap_todos: [T2.31]
modules: [M0]
dashboards: [D03]
branch: p2/P2-T132-deterministic-rule-based-template
pr: ""
doc_sync: [docs/03-build-spec.md, docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T132 · Deterministic rule-based template on the shared libraries

## Goal / expected outcome

The 'deterministic rule-based' M0 template: a Nautilus strategy whose entries/exits are declarative rules over the shared signal library and whose sizing proposals use the shared sizing library, with a first MasterTradingBot rule set ported as an example manifest.

## Context & references

- Roadmap: [R2.48, R2.02](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.31
- [03 M0 templates](../../../docs/03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe) · [14 §8 merging](../../../docs/14-strategy-evidence-and-validation.md#8-mastertradingbot-integration) (MTB strategies appear as M0 strategies with template 'deterministic rule-based')
- Part-A prerequisites: M0 base classes, manifest schema, registry and template parameter-schema conventions (T2.20/T2.21 in part A (P2-T001–T099)); part A registers the `deterministic_rule_based` template slot (currently P2-T009) that this task fills

## Requirements

- Rule DSL (YAML in the manifest): conditions over library signals with AND/OR, entry/exit/stop/target, ATR-scaled stops, time stops; validated by JSON schema → drives `ParamForm`.
- Exit plan fixed and logged at entry (14 §4).
- Runs unchanged in screener (vectorised rules), truth backtest and paper.
- Example manifest `strategies/mtb_ema_cross/manifest.yaml` with counterparty, sleeve, kill criteria and benchmark fields filled (from T2.04/T2.05 inputs).
- Execution adapter for MT5/cTrader is P7; in P2 the template trades only on paper/testnet venues available via part A.

## ToDo

- [ ] Implement `packages/mt_strategy/templates/rule_based.py` + rule DSL schema
- [ ] Port the first MTB rule set as an example strategy
- [ ] Template tests (screener, truth, paper smoke via part A engine)
- [ ] Docs

## Verification

### Tests
- Template test: example manifest validates, backtests on screener and truth, results equal on a fixture where both apply.
- Unit: DSL schema rejects unknown signals and missing stops.

### Scenarios
- Given the MTB EMA-cross rule set, when backtested on the golden period, then trades match MTB's historical trade list (verified fully in P2-T133).

### Stress / failure injection
- n/a: covered by truth runner and engine benchmarks.

## Acceptance criteria

- [ ] Template registered with evidence/priority display fields
- [ ] Example MTB strategy runs in all three modes available in P2
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Rules needing tick data on instruments with only 1m data: refused at manifest validation (resolution check).

## Cardinal rules (do NOT)

- Do NOT add an MT5/cTrader live adapter here (P7).
- Do NOT bypass M11 for template orders.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT touch live money; keys are trade-only, IP-locked, withdrawals disabled; live waits for the P7 gates.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M0: rule DSL reference.
- `docs/14-strategy-evidence-and-validation.md` §8: example strategy path.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.31 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T132-deterministic-rule-based-template`
- PR title: `P2-T132: Deterministic rule-based template on the shared libraries`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T132` run

## Progress log

- 2026-10-21 00:00 · planner · created
