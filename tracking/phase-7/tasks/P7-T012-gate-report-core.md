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
depends_on: [P2-T114, P2-T110, P2-T108]
requirements: [R7.01]
roadmap_todos: [T7.20]
modules: [M7, M0]
dashboards: [D03, D04]
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, mlflow, backtest-worker]
branch: p7/P7-T012-gate-report-core
pr: ""
doc_sync: [docs/03-build-spec.md, docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T012 · Gate report: evaluation core for all §8 gates and harness extensions

## Goal / expected outcome

`mt_lab.gates.evaluate(strategy_version)` produces a structured, versioned gate result covering every 03 §8 gate and every 14 §6 harness extension, with pass/fail, the measured value, the threshold and the evidence run id for each.

## Context & references

- Roadmap: [R7.01 · ToDo T7.20](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) (items 1–8) · [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) (gates 1–7) · [14 §1](../../../docs/14-strategy-evidence-and-validation.md#1-viability-verdict-set-expectations-before-building) (benchmark rule) · [D03](../../../docs/ui/dashboards/D03-strategies.md) Gates tab · [D04](../../../docs/ui/dashboards/D04-research-lab.md) (only truth results count) · [16 §2.4](../../../docs/16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile) (gate profile defaults; loosening C3) · [16 §2.4.1](../../../docs/16-configuration-and-safety-model.md#241-regime-labels-for-per-regime-results) (`regime_v1`)
- Cross-phase (`depends_on`): P2-T114 (validation orchestrator and gate evaluator this extends), P2-T110 (DSR), P2-T108 (trial counter); also uses P2-T111/T112/T113 and P2-T029 (measured costs). LLM strategies read the post-cutoff result from P6-T017 when it exists (an LLM strategy can't exist before P6, so it isn't a dependency).
- Related: P7-T013 (paper section), P7-T014 (rendering/storage), gaps P7-B001 and P7-B014 (resolved: 17 §B, 17 §D)

## Requirements

- Gates evaluated: OOS walk-forward beats benchmark after measured costs; MC permutation p < 0.05; **deflated Sharpe ratio (DSR, a probability) ≥ 0.95** with the automatic trial counter (inputs: per-period Sharpe, n obs, skew, kurtosis, variance of Sharpe across trials); look-ahead + recursive analysers clean; LLM leakage review: no item `present` (or waived with an audited waiver); walk-forward **≥ 60% of folds positive and worst fold ≥ −(sleeve halt drawdown)**; profitable **each year** and **each regime** (bull/bear/chop by `regime_v1`, 16 §2.4.1) or labelled single-regime; survives **2× and 3×** measured costs; survivorship-free universe flag; beats asset-class passive benchmark after costs; LLM strategies tested only post-cutoff (evaluation starts ≥ 30 days after the latest training cutoff of every model in the chain and needs ≥ 90 days out of sample after that embargo; unknown cutoff → fail, 16 §2.4); safety drills (kill switch, dead-man all three layers, restart, and DQ pause per 02 §13) passed on the bot's venue (from `ops.drill_log`).
- Thresholds come from the per-strategy **gate profile** in the layered policy store (defaults from 16 §2.4, shown with their layer); **loosening a gate is C3**, tightening is free (C1).
- Only truth (Nautilus replay) backtests count; screening results are shown but marked ineligible.
- Output: `GateResult{gate_id, status: pass|fail|waived|n/a, value, threshold, evidence_run_id, notes}` list + overall verdict; deterministic for the same inputs.

## ToDo

- [ ] `packages/mt_lab/gates/` with one evaluator per gate reading MLflow runs and `strategy.backtest` via `pit(as_of)`.
- [ ] Gate-profile settings in the layered policy (P2-T010) with change control via `risk.policy.update` (tighten C1 / loosen C3).
- [ ] Benchmark resolver per asset class (BTC + stablecoin yield; FX/indices buy-and-hold or carry; equities index ETF) from the manifest `benchmark` field.
- [ ] Waiver model: waiver row (WORM) with reason and approver; only leakage-review/look-ahead findings may be waived, via `lab.leakage.waive` (C2, audited).
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

- `docs/03-build-spec.md` §8: link the gate evaluator and the gate-profile settings.
- `docs/14-strategy-evidence-and-validation.md` §6: note evaluator names per gate.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.20 when this item is done.

## Branch & PR

- Branch: `p7/P7-T012-gate-report-core`
- PR title: `P7-T012: Gate report: evaluation core for all §8 gates and harness extensions`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T012` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (DSR ≥ 0.95, walk-forward ≥ 60% and worst fold, regime_v1, safety drills, gate profile in the layered policy (16 §2.4); deps on the P2 harness)
