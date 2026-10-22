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
depends_on: [P2-T132, P2-T133]
requirements: [R7.10]
roadmap_todos: [T7.24]
modules: [M0, M7, M11, M18]
dashboards: [D03]
tools: [git, uv]
mcp: []
env: []
services: [postgres, mlflow, backtest-worker]
branch: p7/P7-T038-mastertradingbot-strategy-port
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T038 · Port MasterTradingBot strategies as M0 deterministic rule-based strategies

## Goal / expected outcome

Each permitted MasterTradingBot strategy exists as an M0 strategy (template 'deterministic rule-based') with a full manifest, built on the P2 shared indicator/sizing libraries, backtested with measured costs, and ready to run on paper through the MT5/cTrader adapter (started in P7-T051).

## Context & references

- Roadmap: [R7.10 · ToDo T7.24](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §8](../../../docs/14-strategy-evidence-and-validation.md#8-mastertradingbot-integration) (shared libraries, merging as M0 strategies sharing risk, journal, tax and UI) · [14 §4](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) (porting pitfalls: fixed UTC daily cut, ATR/vol sizing instead of fixed pips, scalpers only on deep books, explicit STP) · [14 §3](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) (counterparty rule)
- Cross-phase (`depends_on`): P2-T132 (deterministic rule-based template on the shared libraries P2-T130/T131), P2-T133 (golden files match).
- Related: P7-T004 (strategies excluded by FP terms), P7-T036/T037, P7-T051

## Requirements

- One manifest per strategy: counterparty sentence, sleeve, benchmark (FX/indices buy-and-hold or carry; gold buy-and-hold), kill criteria, venue `fp_markets_mt5|ctrader`, timeframe, sessions.
- Sizing via the shared sizing library (vol-targeting / stop-distance), not fixed lots; per-trade risk ≤ the bot's setting (default 1% of sleeve equity, [16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)).
- Indicator/signal code only from `mt_core`/`mt_strategy` shared libraries (golden-tested); no copied MasterTradingBot source.
- Each strategy passes through `lab.validate.run` and gets a gate report (P7-T014) before paper on the new adapter.

## ToDo

- [ ] `strategies/mastertradingbot/<name>/` manifests + strategy classes.
- [ ] Backtests with measured FP costs (spreads/swaps from M16).
- [ ] Prepare a paper bot definition per strategy (started on the demo account in P7-T051 once the chosen adapter is ready).
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

- [ ] Every permitted strategy has a manifest, backtest, gate report and a paper bot definition.
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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (per-trade risk default per 16 §2.1; paper start moved to P7-T051; deps P2-T132/T133)
