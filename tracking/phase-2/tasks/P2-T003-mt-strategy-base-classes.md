---
id: P2-T003
kind: task
title: Strategy base traits (Rust) and multi-timeframe helpers
phase: 2
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T016, P1-T009, P0-T071]
requirements: [R2.01, R2.03]
roadmap_todos: [T2.20]
modules: [M0]
dashboards: []
tools: [cargo, uv]
mcp: []
env: []
services: []
branch: p2/P2-T003-mt-strategy-base-classes
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-T003 · Strategy base traits (Rust) and multi-timeframe helpers

## Goal / expected outcome

Strategies are **Rust by default** ([18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates), [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20)): the `MtStrategy`/`MtActor` traits in `crates/mt-engine/src/strategy/` sit on Nautilus's Rust `Strategy`/`Actor` API so one strategy runs unchanged in backtest, sandbox/paper and live, subscribes to any data granularity (ticks, quotes, trades, book deltas, time/tick/volume/value bars, several timeframes at once) and can only emit orders through the M11 gate (`submit_intent`). A thin Python research base (`packages/mt_research/strategy/`, Nautilus Python API) gives ML-research strategies the same hooks and the same single gated path through the `mt-risk` binding (P2-T202); Python strategies are paper-only and are ported to Rust (ONNX via `ort`) before live.

## Context & references

- Roadmap: [R2.01, R2.03](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.20
- Spec: [03 M0](../../../docs/03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe) · [03 §6 smallest free timeframe](../../../docs/03-build-spec.md#6-smallest-free-timeframe-by-asset-class) · [02 §4 components](../../../docs/02-v1-architecture.md#4-logical-components)
- Flow: [02 F2](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Cross-phase (`depends_on`): `mt-core` types `BarSpec`, `Signal`, `OrderIntent` (P0-T016, T0.21), reached from Python through the `mt_store` PyO3 module (P0-T071); instrument master with finest resolution (P1-T009, T1.22/T1.32). Bars + Parquet catalog (P1 R1.02) are only needed for replay data; tests use recorded fixtures.
- Related: P2-T004 (manifest), P2-T017 (RiskGate), P2-T021 (engine), P2-T203 (`mt_research` package + lab binding, where the Python research base lives). Backtest↔paper parity is verified by Part B (T2.65).

## Requirements

- `MtStrategy` trait (Rust; the Python research base mirrors it as `MTStrategy(Strategy)`): lifecycle hooks (`on_start`, `on_bar`, `on_quote_tick`, `on_trade_tick`, `on_order_book_deltas`), access to params from the manifest, `emit_signal()` publishing `sig.{source}.{strategy}`, `submit_intent(OrderIntent)` as the **only** order path (calls the injected `RiskGate`; direct `submit_order` is wrapped and refused).
- `MtActor` trait (Python `MTActor(Actor)`) for non-trading components (feature taps, shadow comparators).
- Multi-timeframe helper: parse `BarSpec` strings (`1s`, `5s`, `1m`, `3m`, `7m`, `1h`, `4h`, `1D`, `1W`, `tick:500`, `volume:1000`, `value:1e6`); subscribe several specs; align on bar close; expose `latest(spec)` without look-ahead (next-bar action).
- Native resolution check: `min_resolution(instrument)` from instrument metadata; subscribing finer than available raises `TimeframeUnavailable` with a clear message (D03 acceptance 3).
- Clock: use Nautilus clock only (never the wall clock: no `SystemTime::now()` / `datetime.now()`), UTC, one bar-close convention.
- Python research strategies: `mode` capped at `paper` by the lifecycle (P2-T007); the base refuses to start on a non-paper node.
- Non-functional: per-event overhead of the base class ≤ 20 µs p99 (keeps signal → order p99 < 5 ms budget, 02 §9.2).

## ToDo

- [ ] Create `crates/mt-engine/src/strategy/base.rs` (`MtStrategy`, `MtActor`, `StrategyContext` with bot mode `paper|hitl|autonomous`, sleeve, bot_id, version, signal timestamp for the decision deadline) on Nautilus's Rust strategy API
- [ ] Create `crates/mt-engine/src/strategy/mtf.rs` (BarSpec parser → Nautilus `BarType`, aggregation from finest data, alignment helpers); the parser lives in `mt-core` so Python gets it through the `mt_store` module
- [ ] Create `crates/mt-engine/src/strategy/gate.rs`: `RiskGate` trait (implemented by the linked `mt-risk` crate, P2-T017) and a `NullGate` that rejects everything (default-deny) for tests
- [ ] The trait exposes no direct `submit_order`; orders leave only via `submit_intent` → `RiskGate`
- [ ] Python research base `packages/mt_research/strategy/base.py` (`MTStrategy`, `MTActor`) with the same hooks, `submit_intent` via the `mt-risk` binding (P2-T202), direct `submit_order`/`submit_order_list` wrapped to raise `BypassError`, an import-linter contract (only `mt_research.strategy.base` may call Nautilus `submit_order`) and a paper-only start guard
- [ ] Example strategy `strategies/examples/ema_cross_min/` (Rust crate + manifest) used by tests, plus the same logic as a Python research example for the parity case
- [ ] Write tests (see Verification)
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Commands: `cargo test -p mt-engine strategy`, `cargo clippy -p mt-engine`; Python research base: `uv run pytest packages/mt_research/tests/strategy`.
- Unit: BarSpec parser round-trips all spec kinds; invalid specs rejected.
- Unit: `TimeframeUnavailable` for a 1s spec on a daily-only instrument.
- Integration: the same Rust example strategy runs in a Nautilus `BacktestEngine` and a sandbox node (paper venue) without code changes; produces identical intents for the same replayed data. The Python research example produces the same intents as the Rust one on the same data.
- Unit: Rust: the trait exposes no direct submit; a `cargo test` compile-fail (trybuild) case proves it. Python research base: a direct `submit_order` call raises `BypassError`; the import-linter contract fails CI when violated.
- Unit: the Python research base refuses to start on a node whose mode is not `paper`.

### Scenarios
- Given a strategy with 1D trend filter + 5m entries + tick execution, when replaying a day, then entries only fire on 5m closes after the 1D bar that closed before them (no look-ahead).
- Given a strategy calls `submit_order` directly, when compiled (Rust) or run (Python research), then it fails to compile / raises and no order reaches the venue.

### Stress / failure injection
- Replay 1 day of BTCUSDT trades (~1M events) through the example strategy; record per-event overhead histogram; p99 ≤ 20 µs.

## Acceptance criteria

- [ ] Rust example strategy runs unchanged in backtest and sandbox/paper; the Python research example matches its intents
- [ ] All bar kinds and multi-timeframe subscriptions supported and tested
- [ ] Bypass attempts fail: Rust compile-fail test, Python `BypassError` test and the import-linter CI contract
- [ ] CI green: `cargo clippy -- -D warnings`, `cargo test`, and for the research-only Python path ruff, mypy, `uv run pytest packages/mt_research` (and the `mt-risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Venue lacks native ticks (daily-only FX/ETF sources): helper aggregates from finest available and reports it.
- Restart mid-bar: partial bars are discarded, never emitted.
- Clock: backtest uses simulated clock; live uses Nautilus live clock; never mix.
- A Python research strategy promoted towards `hitl`/`autonomous` is refused until it has been ported to Rust (P2-T007 mode ceiling).

## Cardinal rules (do NOT)

- Do NOT give strategies any path to the venue other than `submit_intent` → M11.
- Do NOT read wall-clock time or raw tables inside strategies (use Nautilus clock and `pit(as_of)` for research).
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/03-build-spec.md` M0: document the `MtStrategy` trait API, the Python research base and the BarSpec grammar.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.20 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T003-mt-strategy-base-classes`
- PR title: `P2-T003: Strategy base traits (Rust) and multi-timeframe helpers`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T003` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (bot modes paper/hitl/autonomous in context, signal time for decision deadline; cross-phase deps)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (Rust/Python split per 18 §2; `cargo` + `uv run pytest` commands; Rust `MtStrategy` trait counterpart for deterministic strategies; dep P0-T071 (`mt_store` binding); depends_on + P0-T071; tools [uv] → [cargo, uv])
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (Rust `MtStrategy` trait is primary in `crates/mt-engine/src/strategy/`; the Python base moves to `packages/mt_research/strategy/` as a paper-only research path; `cargo` commands first; title updated; tools unchanged [cargo, uv])
