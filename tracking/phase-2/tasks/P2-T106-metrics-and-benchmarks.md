---
id: P2-T106
kind: task
title: Backtest metrics, cost breakdown and asset-class benchmarks
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T104, P2-T105]
requirements: [R2.40, R2.42]
roadmap_todos: [T2.27]
modules: [M7]
dashboards: [D04, D03]
branch: p2/P2-T106-metrics-and-benchmarks
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T106 · Backtest metrics, cost breakdown and asset-class benchmarks

## Goal / expected outcome

A single `mt_lab.metrics` module that turns any result into the D04 Summary metrics plus a benchmark series for the strategy's asset class, so 'beats the passive alternative after costs' is computed the same way everywhere.

## Context & references

- Roadmap: [R2.42](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) (benchmark) · ToDo T2.27
- [14 §1 benchmark rule](../../../docs/14-strategy-evidence-and-validation.md#1-viability-verdict-set-expectations-before-building): crypto = hold BTC + stablecoin yield; FX/indices = buy-and-hold or carry; equities = index ETF
- [D04 Summary tab](../../../docs/ui/dashboards/D04-research-lab.md) · [D03 Performance tab](../../../docs/ui/dashboards/D03-strategies.md)

## Requirements

- Metrics: total return, CAGR, Sharpe (per-period and annualised, stating periods/year), Sortino, Calmar, max DD + duration, hit rate, avg win/loss, profit factor, turnover, exposure, trade count; costs breakdown fees/spread/slippage/funding-swap.
- Per-period return series stored for the validation suite (P2-T109–T111).
- Benchmarks: `btc_hold_plus_stable_yield`, `buy_and_hold`, `carry`, `index_etf`, `equal_weight`, `custom`; default from the manifest `benchmark` field (part A M0 manifest).
- Stablecoin yield series is a configurable constant or a recorded free series (no paid data); documented assumption.
- Excess return vs benchmark after costs and its own Sharpe/IR.
- Monthly returns matrix for the heatmap; drawdown series.

## ToDo

- [ ] Implement `mt_lab/metrics.py` with the metric set and stated annualisation
- [ ] Implement `mt_lab/benchmarks.py` with the six benchmark builders using P2-T103 datasets
- [ ] Persist metrics JSON + series artefacts (Parquet) linked to the backtest row and MLflow (P2-T107)
- [ ] Golden tests vs hand-computed values
- [ ] Doc benchmark definitions in 14 §1

## Verification

### Tests
- Golden: metrics on a fixture equity curve equal hand-computed values to 1e-9.
- Unit: Sharpe of a zero-variance series returns NaN with a reason, not inf.
- Unit: benchmark series for BTC hold matches the dataset close series.

### Scenarios
- Given a strategy that earns less than BTC hold after costs, when the report is built, then excess return < 0 and the benchmark gate (P2-T114) will fail.
- Given a strategy with zero trades, then metrics show 0 trades and Sharpe NaN with an explanatory note.

### Stress / failure injection
- Metrics on 5M-trade tick strategy result in < 30 s using columnar ops.

## Acceptance criteria

- [ ] All D04 Summary metrics produced for screener and truth results
- [ ] Benchmarks selectable and defaulting from the manifest
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Multi-currency P&L converted to base currency (AUD) at the bar's FX rate via pit; source recorded.
- Benchmark data missing for part of the range: benchmark gate is 'unknown', never 'pass'.

## Cardinal rules (do NOT)

- Do NOT annualise Sharpe before passing it to deflated Sharpe (it needs per-period values).
- Do NOT read research/backtest data except through `mt_store.pit(as_of=…)`; the `pit` CI bypass test must stay green.
- Do NOT add paid data/APIs or services; free tiers and self-hosted components only (03 §1).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §1: concrete benchmark definitions used.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.27 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T106-metrics-and-benchmarks`
- PR title: `P2-T106: Backtest metrics, cost breakdown and asset-class benchmarks`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T106` run

## Progress log

- 2026-10-21 00:00 · planner · created
