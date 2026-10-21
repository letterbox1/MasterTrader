---
id: P3-T020
kind: task
title: FX-cash lots for Div 775 and realised P&L for derivatives
phase: 3
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T019]
requirements: [R3.05]
roadmap_todos: [T3.23]
modules: [M18]
dashboards: [D15]
branch: p3/P3-T020-fx-cash-lots-div775-derivatives
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-T020 · FX-cash lots for Div 775 and realised P&L for derivatives

## Goal / expected outcome

Every non-AUD cash balance (USD at IBKR, USDT on an exchange, EUR at OANDA) is tracked as FX lots so Div 775 forex gains/losses can be computed on each conversion or spend, and perps/futures/CFDs produce realised P&L events (incl. funding, financing, variation margin) rather than CGT lots.

## Context & references

- Roadmap: [R3.05, T3.23](../../../docs/roadmap/phase-3-journal-and-tax.md) · [09 AU_2026 Forex / CFDs / Futures](../../../docs/09-journal-and-tax.md#jurisdiction-plugin-interface) · [03 M18](../../../docs/03-build-spec.md#m18-trading-journal--tax--mt_journal)
- Agent question 4 (Div 775 thresholds/elections) in [09 questions](../../../docs/09-journal-and-tax.md#questions-for-your-tax-agent-tracked-as-tasks)
- Related: P3-T024 (AU_2026 revenue/forex rules), P3-T046 (property tests)

## Requirements

- Cash inflows in a foreign currency (sale proceeds, deposits, interest, funding received) open FX lots at the RBA AUD rate of that day; outflows match FX lots FIFO (default; configurable) and produce `fx_realisation` derived rows with AUD gain/loss.
- Stablecoins (USDT/USDC) are **crypto assets for CGT** by default, not foreign currency (setting per asset; agent question) — flagged (U).
- Derivatives: per position, realised P&L on close + funding/financing/variation margin as revenue items; no CGT discount; position lots tracked for P&L attribution only.
- Div 775 elections/thresholds (e.g. limited balance election) are config flags defaulting to **off** with (U) labels; computations show the flag state.

## ToDo

- [ ] Implement `packages/mt_journal/lots/fx_cash.py` and `lots/derivatives.py`
- [ ] Derived rows table `journal.fx_realisation` and `journal.derivative_pnl` (WORM, computation-scoped)
- [ ] Config `config/journal/au_settings.yaml`: stablecoin treatment, Div 775 election flags
- [ ] Golden tests; docs

## Verification

### Tests

- Golden: buy USD 10,000 at 0.65, spend USD 4,000 at 0.62 → AUD forex gain computed per FX lot.
- Golden: perp position with 3 funding payments and a close → realised P&L + funding revenue items, no lots.
- Unit: stablecoin setting toggles treatment.

### Scenarios

- Given USD proceeds from selling US shares at IBKR, when later converted to AUD, then an FX realisation row shows the forex gain/loss separately from the CGT gain.
- Given a CFD position closed at a loss, when computed, then a revenue loss appears (not a capital loss).

### Stress / failure injection

- n/a: covered by P3-T019 rebuild benchmark (same engine)

## Acceptance criteria

- [ ] FX lots exist for every non-AUD cash balance in fixtures
- [ ] Derivative P&L items reconcile to venue realised P&L in fixtures
- [ ] Settings flagged (U) visible in reports
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Negative cash balance (margin loan) → borrow lots with interest as `borrow_fee`; no FX gain until repaid.
- Tiny balances (< AUD 1) still tracked exactly.

## Cardinal rules (do NOT)

- Do NOT turn on a Div 775 election without the agent's answer.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.23 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T020-fx-cash-lots-div775-derivatives`
- PR title: `P3-T020: FX-cash lots for Div 775 and realised P&L for derivatives`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T020` run

## Progress log

- 2026-10-21 00:00 · planner · created
