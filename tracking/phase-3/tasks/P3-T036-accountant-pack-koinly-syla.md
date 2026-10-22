---
id: P3-T036
kind: task
title: Accountant pack (CSV and PDF) and optional Koinly/Syla CSV
phase: 3
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T028]
requirements: [R3.10, R3.12]
roadmap_todos: [T3.27]
modules: [M18]
dashboards: [D15]
tools: [git, uv]
mcp: []
env: []
services: [postgres]
branch: p3/P3-T036-accountant-pack-koinly-syla
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

# P3-T036 · Accountant pack (CSV and PDF) and optional Koinly/Syla CSV

## Goal / expected outcome

One command produces the accountant pack for an FY — a zip with the myTax worksheet, CGT and income schedules, PAYG workings, lots register, event register, FX source register, reconciliation summary, Beancount ledger, and a manifest of hashes — plus an optional Koinly-universal / Syla-style CSV so the agent can cross-check in their own tool; our engine stays primary.

## Context & references

- Roadmap: [R3.10, R3.12, T3.27](../../../docs/roadmap/phase-3-journal-and-tax.md)
- [09 goals §8](../../../docs/09-journal-and-tax.md#goals) · [11 §3 tax software](../../../docs/11-cryptotrader-crossover-review.md#3-conflicts-and-how-they-were-resolved) (Syla/Koinly optional, paid tools not required) · D15 Reports [D15](../../../docs/ui/dashboards/D15-tax.md)

## Requirements

- Pack contents (CSV + PDF where noted): `00_manifest.json` (file → sha256, rule version, FX sources, generated_at), `01_mytax_worksheet.pdf/csv`, `02_cgt_schedule.csv`, `03_income_schedule.csv`, `04_payg.csv`, `05_lots_register.csv`, `06_events.csv`, `07_fx_rates.csv` (with the valuation-method register: method, source refs, per 16 §4.1), `08_recon_summary.csv`, `09_ledger.beancount`, `10_open_questions.csv` (TAX_QUESTION tasks), `README.pdf` (method notes, (U) list, not-advice line).
- Taxpayer details (name/TFN) included only if `include_identity = true` (decrypts from `journal.taxpayer_profile` inside `journal`), default false.
- Koinly: "universal" CSV columns (Date, Sent Amount, Sent Currency, Received Amount, Received Currency, Fee Amount, Fee Currency, Net Worth Amount, Net Worth Currency, Label, Description, TxHash); Syla: format (U) — generic CSV with the same fields until confirmed.
- `tax.export` (C0) with formats `accountant_pack`, `koinly_csv`, `syla_csv`; packs written to `/srv/mastertrader/journal/exports/<fy>/` and listed in D15 Reports with hashes.

## ToDo

- [ ] Implement `packages/mt_journal/exports/accountant_pack.py`, `koinly.py`, `syla.py`
- [ ] PDF templates (local fonts, no network)
- [ ] Tests; docs

## Verification

### Tests

- Golden: fixture FY pack manifest hashes stable across runs.
- Unit: Koinly CSV row for a crypto swap and a staking reward.
- Unit: identity excluded by default (grep pack for TFN pattern → none).

### Scenarios

- Given the agent asks for the FY pack, when you click Export in D15, then a zip appears in Reports with its manifest hash.

### Stress / failure injection

- n/a: batch export (size bound ~50 MB for 50k events)

## Acceptance criteria

- [ ] Pack generated with all listed files + manifest
- [ ] TFN excluded by default
- [ ] Koinly CSV imports into Koinly's validator format (column check)
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Open `needs_classification` items → included in `10_open_questions.csv` and listed on page 1 of README.pdf.

## Cardinal rules (do NOT)

- Do NOT upload packs anywhere automatically; you hand them to the agent.
- Do NOT add Koinly/Syla API integrations (paid).
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."
- Do NOT use paid data/APIs or scraping that breaks terms; free tiers only (03 §1).
- Do NOT expose tax-sensitive fields (TFN, addresses, raw statements) to any LLM prompt, RAG index or the LiteLLM gateway ([07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.27 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T036-accountant-pack-koinly-syla`
- PR title: `P3-T036: Accountant pack (CSV and PDF) and optional Koinly/Syla CSV`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T036` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (pack includes valuation methods (16 §4.1); tools/services filled)
