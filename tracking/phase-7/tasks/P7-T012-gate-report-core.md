---
id: P7-T012
kind: task
title: Gate report: evaluation core for all §8 gates and harness extensions
phase: 7
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.01]
roadmap_todos: [T7.20]
modules: [M7, M0]
dashboards: [D03, D04]
branch: p7/P7-T012-gate-report-core
pr: ""
doc_sync: [docs/03-build-spec.md, docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T012 · Gate report: evaluation core for all §8 gates and harness extensions

## Goal / expected outcome

`mt_lab.gates.evaluate(strategy_version)` produces a structured, versioned gate result covering every 03 §8 gate and every 14 §6 harness extension, with pass/fail, the measured value, the threshold and the evidence run id for each.

## Context & references

- Roadmap: [R7.01 · ToDo T7.20](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) (items 1–8) · [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) (gates 1–7) · [14 §1](../../../docs/14-strategy-evidence-and-validation.md#1-viability-verdict-set-expectations-before-building) (benchmark rule) · [D03](../../../docs/ui/dashboards/D03-strategies.md) Gates tab · [D04](../../../docs/ui/dashboards/D04-research-lab.md) (only truth results count)
- Cross-phase: P2 T2.27 (validation harness, trial counter, leakage review, analysers), P2 T2.26 (measured costs), P6 T6.23 (post-cutoff eval for LLM strategies).
- Related: P7-T013 (paper section), P7-T014 (rendering/storage), gaps P7-B001 (deflated Sharpe threshold), P7-B014 (safety drills gate)

## Requirements

- Gates evaluated: OOS walk-forward beats benchmark after measured costs; MC permutation p < 0.05; **deflated Sharpe probability > 0.95** with the automatic trial counter (inputs: per-period Sharpe, n obs, skew, kurtosis, variance of Sharpe across trials); look-ahead + recursive analysers clean; LLM leakage review: no item `present` (or waived with an audited waiver); walk-forward share of positive folds and **worst fold** reported; profitable **each year** and **each regime** (bull/bear/chop) or labelled single-regime; survives **2× and 3×** measured costs; survivorship-free universe flag; beats asset-class passive benchmark after costs; LLM strategies tested only post-cutoff; safety drills (kill, dead-man, DQ pause) passed (from `ops.drill_log`).
- Thresholds come from a versioned `gates.yaml` policy (defaults above); **loosening a threshold is C3**, tightening C1.
- Only truth (Nautilus replay) backtests count; screening results are shown but marked ineligible.
- Output: `GateResult{gate_id, status: pass|fail|waived|n/a, value, threshold, evidence_run_id, notes}` list + overall verdict; deterministic for the same inputs.

## ToDo

- [ ] `packages/mt_lab/gates/` with one evaluator per gate reading MLflow runs and `strategy.backtest` via `pit(as_of)`.
- [ ] `gates.yaml` policy model + change control via `risk.policy.update`-style diff (tighten C1 / loosen C3).
- [ ] Benchmark resolver per asset class (BTC + stablecoin yield; FX/indices buy-and-hold or carry; equities index ETF) from the manifest `benchmark` field.
- [ ] Waiver model: waiver row (WORM) with reason and approver; only leakage-review items may be waived.
- [ ] Golden tests with a fixture strategy that passes and variants that fail exactly one gate each.
- [ ] Docs.

## Verification

### Tests
- Golden: fixture 'trend_fixture' passes all gates; 12 mutants each fail exactly the intended gate.
- Property: verdict is `pass` only if every non-`n/a` gate is `pass`/`waived`; adding trials never increases deflated Sharpe probability.
- Unit: deflated Sharpe matches a reference implementation within 1e-6 on published examples.

### Scenarios
- Given a strategy profitable overall but losing in 2022 bear, then 'per-regime' fails unless the manifest labels it single-regime (bull) and the bot scope restricts it.
- Given the trial counter is 400, when deflated Sharpe probability drops to 0.93, then the gate fails with value 0.93 / threshold 0.95.
- Given only a screening backtest exists, then gates show 'ineligible: screening result'.

### Stress / failure injection
- Evaluate 100 strategy versions in parallel on the backtest-worker: completes < 10 min; MLflow unavailable → evaluation fails closed (verdict `incomplete`).

## Acceptance criteria

- [ ] Every gate in 03 §8 and 14 §6 has an evaluator with value, threshold and evidence.
- [ ] Verdict is deterministic and covered by golden tests.
- [ ] Threshold loosening requires C3.
- [ ] CI green.

## Exceptions & edge cases

- Missing cost data for a venue: cost-stress gate fails ('no measured costs'), never falls back to fixed bps for illiquid assets.
- Strategy with < 1 year history: per-year gate `fail` (not `n/a`) unless it is explicitly marked research-only.

## Cardinal rules (do NOT)

- Do NOT compute gates on non-PIT data or screening results.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/03-build-spec.md` §8: link the gate evaluator and `gates.yaml`.
- `docs/14-strategy-evidence-and-validation.md` §6: note evaluator names per gate.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.20 when this item is done.

## Branch & PR

- Branch: `p7/P7-T012-gate-report-core`
- PR title: `P7-T012: Gate report: evaluation core for all §8 gates and harness extensions`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T012` run

## Progress log

- 2026-10-21 00:00 · planner · created
