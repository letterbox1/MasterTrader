---
id: P3-T032
kind: task
title: AE, EG, CY and GENERIC jurisdiction plugin stubs
phase: 3
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T031]
requirements: [R3.09]
roadmap_todos: [T3.26]
modules: [M18]
dashboards: [D15]
tools: [git, uv]
mcp: []
env: []
services: []
branch: p3/P3-T032-plugins-ae-eg-cy-generic
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T032 · AE, EG, CY and GENERIC jurisdiction plugin stubs

## Goal / expected outcome

Stub plugins for the UAE, Egypt, Cyprus and a GENERIC fallback implement the full protocol with the 09 summary rules, home currency, tax-year definition and compliance flags, and pass the shared plugin conformance suite, so a residency change produces a sensible (U-labelled) report rather than nothing.

## Context & references

- Roadmap: [R3.09, T3.26](../../../docs/roadmap/phase-3-journal-and-tax.md) · [09 plugin table](../../../docs/09-journal-and-tax.md#jurisdiction-plugin-interface) · agent questions 5–6 ([09](../../../docs/09-journal-and-tax.md#questions-for-your-tax-agent-tracked-as-tasks))

## Requirements

- AE: home AED, calendar tax year; no personal income tax or CGT, so reports show nil personal tax; corporate-tax monitor flag when trading turnover > AED 1m in a calendar year (natural-person threshold); VA transfers VAT-exempt note; residency 183 days or 90 + conditions.
- EG: home EGP, calendar tax year; listed-securities gains exempt; stamp duty per trade 0.05% per side (U) report; other income progressive up to 27.5% (informational); **crypto hard flag** in `compliance_flags`; residency 183 days.
- CY: home EUR, calendar year; securities gains exempt; **8% flat on net crypto gains** (losses offset same-year crypto gains only; Art. 20E from 1 Jan 2026, enactment (U)); SDC/GeSY 2.65% notes; residency 183 days or 60-day rule.
- GENERIC: home currency parameter + FIFO/HIFO capital report.
- FX for non-AUD homes: ECB (EUR), CBE (EGP), CBUAE (AED) sources declared in `fx_policy` but **not fetched** until a residency period needs them (then a P1-style flow is added; noted as follow-up).
- Every output labelled `(U) stub — confirm with a local adviser`.

## ToDo

- [ ] Implement `rules/ae.py`, `rules/eg.py`, `rules/cy.py`, `rules/generic.py`
- [ ] Shared conformance test suite `tests/journal/rules/test_conformance.py` run against every plugin
- [ ] Docs

## Verification

### Tests

- Conformance: all 5 protocol methods return typed results for every plugin.
- Unit: CY 8% on net crypto gains with same-year loss offset; EG stamp duty on a listed trade fixture; AE turnover threshold flag.
- Unit: tax_year for EG/CY is the calendar year.

### Scenarios

- Given a CY residency period, when D15 opens for 2029, then the CY crypto ledger shows the 8% computation labelled (U).

### Stress / failure injection

- n/a: stubs

## Acceptance criteria

- [ ] 4 plugins registered and conformant
- [ ] Each output (U)-labelled
- [ ] EG crypto hard flag emitted
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Missing FX source for a home currency → plugin returns `fx_unavailable` and reports in USD with a warning.

## Cardinal rules (do NOT)

- Do NOT fetch CBE/CBUAE data or add paid sources now.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."
- Do NOT use paid data/APIs or scraping that breaks terms; free tiers only (03 §1).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.26 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T032-plugins-ae-eg-cy-generic`
- PR title: `P3-T032: AE, EG, CY and GENERIC jurisdiction plugin stubs`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T032` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (no decision changes; tools/services filled)
