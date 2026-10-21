---
id: P3-T024
kind: task
title: AU_2026 revenue, income and Div 775 forex computations
phase: 3
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T020, P3-T022]
requirements: [R3.06]
roadmap_todos: [T3.24]
modules: [M18]
dashboards: [D15]
branch: p3/P3-T024-au2026-revenue-income-div775
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

# P3-T024 · AU_2026 revenue, income and Div 775 forex computations

## Goal / expected outcome

`AU_2026` computes revenue-account results (CFDs per TR 2005/15, futures by default with per-instrument override (U)), Div 775 forex gains/losses from FX-cash lots, ordinary income (staking, established airdrops, interest, dividends with franking and foreign withholding, funding/financing), and foreign income + foreign tax paid, as D15 Income and Summary items.

## Context & references

- Roadmap: [R3.06, T3.24](../../../docs/roadmap/phase-3-journal-and-tax.md)
- [09 AU_2026 row](../../../docs/09-journal-and-tax.md#jurisdiction-plugin-interface) · D15 Summary/Income tabs [D15](../../../docs/ui/dashboards/D15-tax.md) · agent questions 2 and 4 ([09](../../../docs/09-journal-and-tax.md#questions-for-your-tax-agent-tracked-as-tasks))

## Requirements

- Treatment map in `classify(event, regime)`: CFD → REVENUE; futures → REVENUE (override table `config/journal/instrument_overrides.yaml`, (U)); perps → REVENUE by default (U, agent question added); funding/financing/borrow → REVENUE (deductible or assessable by sign); staking/established airdrop/interest → INCOME; dividends → INCOME with franking credits and withholding; FX-cash realisations → Div 775 REVENUE.
- Foreign income: income with a foreign source (US dividends, offshore exchange interest) aggregated with foreign tax paid (withholding) for item 20 mapping.
- Outputs: revenue P&L by instrument class, Div 775 net, income by type, foreign income + tax paid — each with event drill-down ids.

## ToDo

- [ ] Implement `rules/au_2026/revenue.py`, `income.py`, `forex.py`
- [ ] Override config + validation
- [ ] Golden tests; docs

## Verification

### Tests

- Golden: CFD round trips + financing → revenue result equals venue realised P&L ± financing.
- Golden: US dividend USD 100 with 15% withholding → AUD income and AUD foreign tax paid at RBA rate.
- Golden: Div 775 example from P3-T020 flows into Summary.

### Scenarios

- Given a futures instrument overridden to CAPITAL, when computed, then it moves to the CGT schedule and the override + (U) label appears on the report.
- Given perp funding received and paid, when computed, then net funding is a revenue item, not CGT.

### Stress / failure injection

- n/a: computation volume covered in P3-T023/P3-T052

## Acceptance criteria

- [ ] Revenue, income, forex and foreign income totals produced with drill-down
- [ ] All (U) treatments labelled on outputs
- [ ] Golden tests pass
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Franked dividends from AU ETFs (if held) → franking credit grossed up; data from statement fields only.
- Negative interest → deductible expense item (flag).

## Cardinal rules (do NOT)

- Do NOT net revenue losses against capital gains.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.24 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T024-au2026-revenue-income-div775`
- PR title: `P3-T024: AU_2026 revenue, income and Div 775 forex computations`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T024` run

## Progress log

- 2026-10-21 00:00 · planner · created
