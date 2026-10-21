---
id: P3-T035
kind: task
title: Beancount v3 ledger export with lots for Fava
phase: 3
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T019, P3-T020, P3-T022]
requirements: [R3.10]
roadmap_todos: [T3.27]
modules: [M18]
dashboards: [D14, D15]
branch: p3/P3-T035-beancount-export
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

# P3-T035 · Beancount v3 ledger export with lots for Fava

## Goal / expected outcome

A yearly (and full-history) Beancount v3 ledger is exported from the journal with accounts per registered venue/wallet, commodities per asset, lots with cost `{}` and acquisition dates, prices from the FX/price service and balance assertions from reconciliation, so `bean-check` passes and Fava gives an independent second opinion and accountant hand-off.

## Context & references

- Roadmap: [R3.10, T3.27](../../../docs/roadmap/phase-3-journal-and-tax.md) · verified by P3-T049
- [09 goals §4](../../../docs/09-journal-and-tax.md#goals) · [09 tools vetted (hledger/Beancount + Fava, adopt)](../../../docs/09-journal-and-tax.md#tools-vetted) · [03 M18 exports](../../../docs/03-build-spec.md#m18-trading-journal--tax--mt_journal)
- Related: P3-T009 (Fava sidecar), P3-T034 (balance assertions)

## Requirements

- Account naming: `Assets:<Venue>:<Account>:<Asset>`, `Income:Trading:<Class>`, `Income:Staking`, `Expenses:Fees:<Type>`, `Equity:Opening`; operating currency AUD.
- Each journal event → one transaction with metadata `event_id`, `source_ref`, `fx_source`; acquisitions carry `{cost, date}` lots; disposals reference the lot cost per `lot_match` (so Beancount's booking = our matching, booking method `NONE` with explicit lots).
- `price` directives for every rate used (from `journal.fx_rate` and crypto price sources).
- `balance` assertions per account/asset at each daily recon date with status ok.
- Output `/srv/mastertrader/journal/exports/<fy>/ledger.beancount` + `current.beancount` symlink for Fava; deterministic ordering; hash recorded in `journal.tax_report` (type `beancount`).
- Command `tax.export` (C0) with `format = beancount`, scope FY or journal.

## ToDo

- [ ] Implement `packages/mt_journal/exports/beancount.py` (beancount v3 library for validation only)
- [ ] Wire `tax.export` handler
- [ ] Tests; docs

## Verification

### Tests

- Integration: fixture FY → export → `bean-check` exit 0.
- Unit: deterministic output (same inputs → identical bytes).
- Unit: disposal lots match `journal.lot_match` exactly.

### Scenarios

- Given an internal transfer, when exported, then it's a transfer between asset accounts with the same lot cost/date (no income/expense except the fee).

### Stress / failure injection

- Export 1M events < 5 min; file loads in Fava within 60 s.

## Acceptance criteria

- [ ] `bean-check` passes on fixture and on the paper-trading month (P3-T049)
- [ ] Export hash stored
- [ ] Fava shows the ledger via the sidecar
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Assets with symbols illegal in Beancount → mapped commodity names with metadata of the original id.

## Cardinal rules (do NOT)

- Do NOT let Beancount re-book lots differently from our engine (explicit lots only).
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.27 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T035-beancount-export`
- PR title: `P3-T035: Beancount v3 ledger export with lots for Fava`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T035` run

## Progress log

- 2026-10-21 00:00 · planner · created
