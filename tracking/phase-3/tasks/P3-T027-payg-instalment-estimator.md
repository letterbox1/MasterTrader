---
id: P3-T027
kind: task
title: PAYG instalment estimator (quarterly)
phase: 3
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T025]
requirements: [R3.06]
roadmap_todos: [T3.24]
modules: [M18]
dashboards: [D15]
branch: p3/P3-T027-payg-instalment-estimator
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

# P3-T027 · PAYG instalment estimator (quarterly)

## Goal / expected outcome

D15 PAYG shows, for each quarter of the FY, the estimated instalment income (excluding capital gains) and the estimated instalment under both regimes, using the instalment rate or amount from your ATO notice, with due dates, history and rule version — part of exit criterion 2.

## Context & references

- Roadmap: [R3.06, T3.24](../../../docs/roadmap/phase-3-journal-and-tax.md) · exit criterion 2 (PAYG estimate)
- [09 BAS finding](../../../docs/09-journal-and-tax.md#️-key-findings-that-shape-the-design) ("BAS module" = PAYG-instalment estimator; GST/BAS dormant) · [02 F9 step 5](../../../docs/02-v1-architecture.md#8-end-to-end-flows) (quarterly output) · D15 PAYG tab [D15](../../../docs/ui/dashboards/D15-tax.md)
- Gap: P3-B005 (method details unspecified)

## Requirements

- Inputs: instalment method from your ATO notice (`rate` with instalment rate %, or `amount`) entered in `config/journal/payg.yaml` (no TFN); FY quarters Q1 Jul–Sep, Q2 Oct–Dec, Q3 Jan–Mar, Q4 Apr–Jun; default due dates 28 Oct, 28 Feb, 28 Apr, 28 Jul (configurable; (U) until confirmed on your notice).
- Instalment income = gross ordinary income in the quarter (revenue trading gains, interest, dividends incl. franking gross-up, staking/airdrop income, net Div 775 gains) **excluding capital gains**; under the trader regime, trading gains are included.
- Estimate = instalment income × rate (rate method) or notice amount (amount method); both regimes shown; negative instalment income → 0 with a note (variation is your call with the agent).
- Quarterly Prefect flow `journal-payg-quarterly` runs on the 1st day after each quarter end and stores the estimate as a `journal.tax_report` (type `payg`) + a `task.new` reminder 14 days before each due date.

## ToDo

- [ ] Implement `rules/au_2026/payg.py`
- [ ] Config schema + validation
- [ ] Prefect deployment + reminder task
- [ ] Tests; docs

## Verification

### Tests

- Golden: fixture quarter with revenue 10,000, interest 500, capital gain 20,000, rate 8% → estimate 840 (capital gain excluded).
- Unit: amount method returns the notice amount.
- Unit: quarter boundaries use taxpayer-local dates.

### Scenarios

- Given no notice entered, when D15 PAYG opens, then it shows instalment income per quarter and "enter your instalment rate" instead of an estimate.
- Given the quarter ends 30 Sep, when 1 Oct arrives, then the flow stores the Q1 estimate and a reminder for 28 Oct is queued.

### Stress / failure injection

- n/a: quarterly batch

## Acceptance criteria

- [ ] PAYG estimates per quarter under both regimes, with rule version and FX source
- [ ] Reminder tasks created
- [ ] Capital gains excluded (test)
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Mid-year notice change → new config effective from the next quarter (history kept).
- GST/BAS mode flag stays off; turning it on is out of scope (dormant).

## Cardinal rules (do NOT)

- Do NOT store TFN or ATO notice PDFs in the repo.
- Do NOT lodge anything; this is an estimator.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.24 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T027-payg-instalment-estimator`
- PR title: `P3-T027: PAYG instalment estimator (quarterly)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T027` run

## Progress log

- 2026-10-21 00:00 · planner · created
