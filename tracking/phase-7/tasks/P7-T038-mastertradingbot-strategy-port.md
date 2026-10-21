---
id: P7-T038
kind: task
title: Port MasterTradingBot strategies as M0 deterministic rule-based strategies
phase: 7
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.10]
roadmap_todos: [T7.24]
modules: [M0, M7, M11, M18]
dashboards: [D03]
branch: p7/P7-T038-mastertradingbot-strategy-port
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T038 · Port MasterTradingBot strategies as M0 deterministic rule-based strategies

## Goal / expected outcome

Each permitted MasterTradingBot strategy exists as an M0 strategy (template 'deterministic rule-based') with a full manifest, built on the P2 shared indicator/sizing libraries, backtested with measured costs, and running on paper through the MT5/cTrader adapter.

## Context & references

- Roadmap: [R7.10 · ToDo T7.24](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §8](../../../docs/14-strategy-evidence-and-validation.md#8-mastertradingbot-integration) (shared libraries, merging as M0 strategies sharing risk, journal, tax and UI) · [14 §4](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) (porting pitfalls: fixed UTC daily cut, ATR/vol sizing instead of fixed pips, scalpers only on deep books, explicit STP) · [14 §3](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) (counterparty rule)
- Cross-phase: P2 T2.31 (shared libraries + template), P2 T2.67 (golden files), P2 T2.04 (your rule descriptions and outputs).
- Related: P7-T004 (strategies excluded by FP terms), P7-T036/T037, P7-T051

## Requirements

- One manifest per strategy: counterparty sentence, sleeve, benchmark (FX/indices buy-and-hold or carry; gold buy-and-hold), kill criteria, venue `fp_markets_mt5|ctrader`, timeframe, sessions.
- Sizing via the shared sizing library (vol-targeting / stop-distance), not fixed lots; per-trade risk ≤ 1% of sleeve.
- Indicator/signal code only from `mt_core`/`mt_strategy` shared libraries (golden-tested); no copied MasterTradingBot source.
- Each strategy passes through `lab.validate.run` and gets a gate report (P7-T014) before paper on the new adapter.

## ToDo

- [ ] `strategies/mastertradingbot/<name>/` manifests + strategy classes.
- [ ] Backtests with measured FP costs (spreads/swaps from M16).
- [ ] Start paper bots on the demo account via the chosen adapter.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: each strategy's signal function matches golden outputs on fixture bars.
- Integration: backtest → validation → gate report produced (pass or fail is fine).

### Scenarios
- Given a scalper that only worked with fixed pips, when ported with ATR sizing, then its validation result is recorded honestly (may fail gates).

### Stress / failure injection
- n/a: strategy port; load covered by adapter stress tests.

## Acceptance criteria

- [ ] Every permitted strategy has a manifest, backtest, gate report and a paper bot.
- [ ] CI green.

## Exceptions & edge cases

- Strategy forbidden by FP terms (P7-T004): not ported; noted in the manifest registry as excluded.

## Cardinal rules (do NOT)

- Do NOT skip gates for strategies that 'already worked' in MasterTradingBot.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §8: list of ported strategies.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.24 when this item is done.

## Branch & PR

- Branch: `p7/P7-T038-mastertradingbot-strategy-port`
- PR title: `P7-T038: Port MasterTradingBot strategies as M0 deterministic rule-based strategies`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T038` run

## Progress log

- 2026-10-21 00:00 · planner · created
