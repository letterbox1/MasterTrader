---
id: P2-T161
kind: task
title: Verify backtest ↔ paper parity on a simple template over the same week
phase: 2
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T105, P2-T106, P2-T021, P2-T023, P2-T008]
requirements: [R2.01, R2.40]
roadmap_todos: [T2.65]
modules: [M7, M0, M12]
dashboards: [D04, D03]
tools: [uv]
mcp: []
env: []
services: [postgres, mlflow]
branch: p2/P2-T161-verify-backtest-paper-parity
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T161 · Verify backtest ↔ paper parity on a simple template over the same week

## Goal / expected outcome

Evidence that the same strategy class, run in a Nautilus truth backtest over a recorded week and on paper in the engine over that same week, produces the same signals and near-identical fills/P&L, with any difference explained.

## Context & references

- Roadmap: [R2.01, R2.40](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.65
- [03 M0](../../../docs/03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe) · [03 M7 truth](../../../docs/03-build-spec.md#m7-research-lab--mt_lab) · [02 F2](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Prerequisites (`depends_on`): paper engine (P2-T021) on the sandbox venue (P2-T023; simulated fills on live P1 data, no venue keys needed) running the EMA template (P2-T008) for one week, recorded by the P1 Parquet recorder

## Requirements

- Strategy: EMA-cross template on BTC-USDT (Binance public market data recorded in P1) 1m bars, paper bot on the sandbox venue, plus one FX pair from the P1 OANDA price stream if available.
- Signals: identical timestamps and directions (100%).
- Orders: identical intents and M11 decisions.
- Fills: per-fill price diff within the modelled slippage band; total P&L difference ≤ 10% of gross P&L or ≤ 5 bps of notional, whichever is larger; cost totals within 20% (feeds realised-vs-modelled ratio).
- Differences categorised (latency, queue position, partial fills, venue rejects) in a parity report stored as an MLflow artefact.

## ToDo

- [ ] Pick the week; confirm recording completeness (no gaps) via D07
- [ ] Replay the recorded week in truth backtest with the measured cost snapshot
- [ ] Export paper fills/orders for the week
- [ ] Write `mt_lab/parity.py` comparison + report
- [ ] Record result and categorised differences

## Verification

### Tests
- Integration: parity comparator unit-tested on synthetic identical/divergent runs.
- The parity run itself (evidence).

### Scenarios
- Given a data gap in the recorded week, then parity is not computed for that window (excluded and reported) rather than counted as divergence.
- Given a venue reject on paper that the backtest did not model, then it is listed with its reason and the cost model/fill model gets a follow-up item.

### Stress / failure injection
- n/a: one-week comparison; engine load covered by part A benchmarks.

## Acceptance criteria

- [ ] Signals 100% identical
- [ ] P&L/cost differences within the stated tolerances or explained with follow-up items
- [ ] Parity report stored and linked from D04

## Exceptions & edge cases

- Testnet liquidity is unrealistic: compare against testnet book data recorded by P1, not mainnet.

## Cardinal rules (do NOT)

- Do NOT 'fix' parity by tuning the backtest to the paper week (overfitting the fill model); changes go through the cost snapshot process.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M7: parity tolerance and result.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.65 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T161-verify-backtest-paper-parity`
- PR title: `P2-T161: Verify backtest ↔ paper parity on a simple template over the same week`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T161` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (paper parity on the sandbox venue (no keys), engine/template deps explicit)
