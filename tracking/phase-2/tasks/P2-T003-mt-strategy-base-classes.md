---
id: P2-T003
kind: task
title: mt_strategy base classes and multi-timeframe helpers
phase: 2
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.01, R2.03]
roadmap_todos: [T2.20]
modules: [M0]
dashboards: []
branch: p2/P2-T003-mt-strategy-base-classes
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

# P2-T003 · mt_strategy base classes and multi-timeframe helpers

## Goal / expected outcome

`packages/mt_strategy` provides `MTStrategy`/`MTActor` on top of Nautilus `Strategy`/`Actor` so one strategy class runs unchanged in backtest, sandbox/paper and live, subscribes to any data granularity (ticks, quotes, trades, book deltas, time/tick/volume/value bars, several timeframes at once) and can only emit orders through the M11 gate.

## Context & references

- Roadmap: [R2.01, R2.03](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.20
- Spec: [03 M0](../../../docs/03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe) · [03 §6 smallest free timeframe](../../../docs/03-build-spec.md#6-smallest-free-timeframe-by-asset-class) · [02 §4 components](../../../docs/02-v1-architecture.md#4-logical-components)
- Flow: [02 F2](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Cross-phase: `mt_core` types `BarSpec`, `Signal`, `OrderIntent` (P0 T0.21); bars + Parquet catalog (P1 R1.02).
- Related: P2-T004 (manifest), P2-T017 (RiskGate), P2-T021 (engine). Backtest↔paper parity is verified by Part B (T2.65).

## Requirements

- `MTStrategy(Strategy)`: lifecycle hooks (`on_start`, `on_bar`, `on_quote_tick`, `on_trade_tick`, `on_order_book_deltas`), access to params from the manifest, `emit_signal()` publishing `sig.{source}.{strategy}`, `submit_intent(OrderIntent)` as the **only** order path (calls the injected `RiskGate`; direct `submit_order` is wrapped and refused).
- `MTActor(Actor)` for non-trading components (feature taps, shadow comparators).
- Multi-timeframe helper: parse `BarSpec` strings (`1s`, `5s`, `1m`, `3m`, `7m`, `1h`, `4h`, `1D`, `1W`, `tick:500`, `volume:1000`, `value:1e6`); subscribe several specs; align on bar close; expose `latest(spec)` without look-ahead (next-bar action).
- Native resolution check: `min_resolution(instrument)` from instrument metadata; subscribing finer than available raises `TimeframeUnavailable` with a clear message (D03 acceptance 3).
- Clock: use Nautilus clock only (never `datetime.now()`), UTC, one bar-close convention.
- Non-functional: per-event overhead of the base class ≤ 20 µs p99 (keeps signal → order p99 < 5 ms budget, 02 §9.2).

## ToDo

- [ ] Create `packages/mt_strategy/base.py` (`MTStrategy`, `MTActor`, `StrategyContext` with mode, sleeve, bot_id, version)
- [ ] Create `packages/mt_strategy/mtf.py` (BarSpec parser → Nautilus `BarType`, aggregation from finest data, alignment helpers)
- [ ] Create `packages/mt_strategy/gate.py` protocol `RiskGateProtocol` (implemented by P2-T017) and a `NullGate` that rejects everything (default-deny) for tests
- [ ] Wrap `submit_order`/`submit_order_list` so calling them outside `submit_intent` raises `BypassError`
- [ ] Add an import-linter contract: only `mt_strategy.base` may call Nautilus `submit_order`
- [ ] Example strategy `strategies/examples/ema_cross_min/` used by tests
- [ ] Write tests (see Verification)
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: BarSpec parser round-trips all spec kinds; invalid specs rejected.
- Unit: `TimeframeUnavailable` for a 1s spec on a daily-only instrument.
- Integration: the same example strategy class runs in a Nautilus `BacktestEngine` and a sandbox `TradingNode` (paper venue) without code changes; produces identical intents for the same replayed data.
- Unit: direct `submit_order` call raises `BypassError`; import-linter contract fails CI when violated.

### Scenarios
- Given a strategy with 1D trend filter + 5m entries + tick execution, when replaying a day, then entries only fire on 5m closes after the 1D bar that closed before them (no look-ahead).
- Given a strategy calls `submit_order` directly, when run, then it raises and no order reaches the venue.

### Stress / failure injection
- Replay 1 day of BTCUSDT trades (~1M events) through the example strategy; record per-event overhead histogram; p99 ≤ 20 µs.

## Acceptance criteria

- [ ] Example strategy runs unchanged in backtest and sandbox/paper
- [ ] All bar kinds and multi-timeframe subscriptions supported and tested
- [ ] Bypass attempts fail in unit tests and in the import-linter CI contract
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Venue lacks native ticks (daily-only FX/ETF sources): helper aggregates from finest available and reports it.
- Restart mid-bar: partial bars are discarded, never emitted.
- Clock: backtest uses simulated clock; live uses Nautilus live clock; never mix.

## Cardinal rules (do NOT)

- Do NOT give strategies any path to the venue other than `submit_intent` → M11.
- Do NOT read wall-clock time or raw tables inside strategies (use Nautilus clock and `pit(as_of)` for research).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/03-build-spec.md` M0: document the base-class API and BarSpec grammar.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.20 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T003-mt-strategy-base-classes`
- PR title: `P2-T003: mt_strategy base classes and multi-timeframe helpers`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T003` run

## Progress log

- 2026-10-21 00:00 · planner · created
