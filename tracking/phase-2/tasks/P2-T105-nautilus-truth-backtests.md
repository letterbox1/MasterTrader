---
id: P2-T105
kind: task
title: Nautilus truth backtest runner with L1/L2 replay and measured fills
phase: 2
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T102, P2-T103]
requirements: [R2.40, R2.41, R2.01]
roadmap_todos: [T2.27]
modules: [M7, M0]
dashboards: [D04]
branch: p2/P2-T105-nautilus-truth-backtests
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T105 · Nautilus truth backtest runner with L1/L2 replay and measured fills

## Goal / expected outcome

`mt_lab.truth` runs the unchanged M0 Nautilus strategy class in a `BacktestEngine` over L1/L2/tick replay from the Parquet catalog, with fill, fee, latency and funding/swap models built from measured M16 costs, deterministic seeds and a stored reproduction record; these are the only results that count for gates.

## Context & references

- Roadmap: [R2.40, R2.41, R2.01](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.27
- Spec: [03 M7 truth path](../../../docs/03-build-spec.md#m7-research-lab--mt_lab) · [03 M0](../../../docs/03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe) (one class: backtest, sandbox/paper, live) · [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8)
- Part-A prerequisite: M0 base classes, manifest and templates (T2.20/T2.21 in part A (P2-T001–T099)); the M11 pre-trade checks (T2.22) run in-process in the engine so backtests see the same rejections as paper
- D04 fields 'Fill model (Nautilus): L1/L2 replay, queue position, latency': [D04](../../../docs/ui/dashboards/D04-research-lab.md)

## Requirements

- Load the strategy by id/version from the registry and run it with zero code changes in `BacktestEngine` (same class used by `engine` for paper).
- Data: Nautilus catalog replay of ticks/quotes/trades/book deltas or bars from P2-T103 datasets; L2 replay where recorded.
- Fill model: fills only at prices/sizes that existed (book walk on L2; L1 with size cap otherwise), optional queue-position model, latency from the cost snapshot; venue fees and funding/swap applied at their timestamps.
- Risk: route orders through the M11 pre-trade layer in backtest mode (part A API) so limits, collars, DQ blocks and the 2× cap apply identically.
- Determinism: fixed seed + data_hash + code_sha + Nautilus version ⇒ identical trades (D04 acceptance 4).
- Result row: `engine=truth`, `gate_eligible=true` unless costs are custom/zero; trades, fills, positions, equity, cost breakdown (fees, spread, slippage, funding/swap).
- Runtime target: 1 month of 1-s L1 for one crypto symbol in < 10 min on 1 core.

## ToDo

- [ ] Implement `mt_lab/truth/runner.py` building `BacktestEngine` venues, instruments and data from a `Dataset`
- [ ] Implement `FillModel`/`FeeModel`/latency adapters from P2-T102 and funding/swap event injection
- [ ] Wire the M11 pre-trade layer in backtest mode (integration with part A's `mt_risk` API) and record rejections
- [ ] Register `truth` `JobRunner`; store the reproduction record (code SHA, manifest hash, data snapshot ids, seed, engine version)
- [ ] Determinism test, parity hook for P2-T161
- [ ] Docs

## Verification

### Tests
- Unit: fill model never fills beyond displayed L2 size at that timestamp; funding applied every interval for perps.
- Integration: EMA template on a 1-week BTC fixture produces a stored golden trade list; second run identical.
- Integration: an order breaching the max-position limit is rejected by M11 in backtest exactly as in paper.

### Scenarios
- Given a market order larger than the visible book, when filled, then it walks levels and the residual is unfilled/partially filled — never at a non-existent price.
- Given a DQ-bad period in the data, when the strategy signals, then M11 blocks the order (no trading on bad data).
- Given custom zero costs, when the run finishes, then `gate_eligible=false` and the 'Unrealistic costs' flag is set.

### Stress / failure injection
- Replay 1 week of L2 deltas for 3 symbols concurrently on 3 workers: no cross-run state leakage.
- Kill the worker mid-run: job re-queued (P2-T101) and the re-run result equals a clean run.

## Acceptance criteria

- [ ] Same strategy class runs unchanged here and in part A's paper engine
- [ ] Determinism test passes (identical trade hashes)
- [ ] M11 rejections visible in the result
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Instruments lacking L2: fall back to L1 with a size cap and label the fill model used.
- Strategy subscribes to a resolution the instrument cannot provide: refuse (D03 acceptance 3).
- Nautilus version bump changes results: the reproduction record pins the version; re-runs on a new version are new results.

## Cardinal rules (do NOT)

- Do NOT fork or patch Nautilus (LGPL) in-tree; wrap it.
- Do NOT bypass the M11 layer in backtests to 'speed up' runs.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT read research/backtest data except through `mt_store.pit(as_of=…)`; the `pit` CI bypass test must stay green.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M7: truth runner fill/latency model and reproduction record.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.27 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T105-nautilus-truth-backtests`
- PR title: `P2-T105: Nautilus truth backtest runner with L1/L2 replay and measured fills`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T105` run

## Progress log

- 2026-10-21 00:00 · planner · created
