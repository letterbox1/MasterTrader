---
id: P2-T130
kind: task
title: MasterTradingBot pure indicator/signal library with golden-file harness
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T014]
requirements: [R2.48]
roadmap_todos: [T2.31]
modules: [M0]
dashboards: []
tools: [uv]
mcp: []
env: []
services: []
branch: p2/P2-T130-mtb-indicator-signal-library
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T130 · MasterTradingBot pure indicator/signal library with golden-file harness

## Goal / expected outcome

A pure-function, I/O-free indicator/signal library (EMA, ATR, scalper triggers and the MasterTradingBot rule primitives) in `mt_strategy.lib.signals`, plus a golden-file harness that replays MasterTradingBot's historical inputs and compares outputs exactly.

## Context & references

- Roadmap: [R2.48](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.31 · golden match verified in P2-T133
- [14 §8 MasterTradingBot integration](../../../docs/14-strategy-evidence-and-validation.md#8-mastertradingbot-integration) (shared libraries, not merged engines; our own licence-clean code)
- [14 §4 porting pitfalls](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) (fixed UTC daily cut; ATR/vol scaling instead of fixed pips)
- User input: MasterTradingBot rule descriptions + historical signal/trade outputs come from USER item T2.04 in part A (P2-T001–T099) (currently P2-T002)

## Requirements

- Pure functions only (no I/O, no globals, no clock reads): `ema`, `sma`, `atr` (Wilder), `true_range`, crossovers, scalper triggers as described by T2.04, session filters taking an explicit calendar argument.
- Both batch (array) and streaming (state object) forms; streaming equals batch exactly (parity harness from P2-T120 reused where features overlap).
- Golden-file format: `tests/golden/mtb/<rule>/<instrument>_<period>.{inputs,expected}.parquet` with MT5 bar timestamps converted to UTC and the MT5 server timezone recorded.
- Numeric conventions documented (EMA seeding, ATR smoothing, rounding to instrument digits) to match MT5 behaviour exactly.
- Licence-clean: written from the rule descriptions, not copied from third-party EA code.

## ToDo

- [ ] Create `packages/mt_strategy/lib/signals.py` and streaming state classes
- [ ] Golden-file loader + comparator (`mt_strategy.testing.golden`) with tolerance 0 for signals and ≤ 1e-8 for indicator values
- [ ] Implement primitives from the T2.04 rule descriptions
- [ ] Unit tests vs TA-Lib for overlapping indicators while golden files are pending
- [ ] Doc conventions

## Verification

### Tests
- Unit: EMA/ATR equal TA-Lib on fixtures (where conventions match).
- Golden: harness runs whatever golden sets exist; CI fails on any mismatch.
- Property: streaming == batch for random inputs (hypothesis).

### Scenarios
- Given MT5 broker-time bars (UTC+2/+3), when converted, then daily boundaries match the fixed UTC cut documented for porting.
- Given golden files not yet provided by the user, then golden tests are skipped with an explicit 'awaiting T2.04' marker that P2-T133 must clear (not silently passing).

### Stress / failure injection
- n/a: pure functions; performance covered by template benchmarks.

## Acceptance criteria

- [ ] Library is pure (import-linter rule forbids I/O modules)
- [ ] Golden harness in CI
- [ ] Conventions documented
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- MT5 symbol suffixes (e.g. `XAUUSD.r`) map to instrument ids via a mapping table.
- Weekend/holiday gaps: indicators continue on bar count, not wall-clock.

## Cardinal rules (do NOT)

- Do NOT copy MetaQuotes/EA or GPL code; write from the rule descriptions.
- Do NOT add I/O, clock or network access to the library.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §8: library location and conventions.
- `docs/03-build-spec.md` M0: shared library note.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.31 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T130-mtb-indicator-signal-library`
- PR title: `P2-T130: MasterTradingBot pure indicator/signal library with golden-file harness`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T130` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields; golden inputs from P2-T002 are checked in P2-T133)
- 2026-10-22 00:00 · coordinator · depends on P0-T014 (code lives in the uv monorepo; dependency gating)
