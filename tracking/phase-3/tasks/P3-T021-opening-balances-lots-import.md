---
id: P3-T021
kind: task
title: Opening balances and opening lots import from historical statements
phase: 3
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T015, P3-T016, P3-T019, P3-T055]
requirements: [R3.01, R3.05]
roadmap_todos: [T3.20, T3.23]
modules: [M18]
dashboards: []
tools: [git, uv]
mcp: []
env: []
services: [postgres, mt-api]
branch: p3/P3-T021-opening-balances-lots-import
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

# P3-T021 · Opening balances and opening lots import from historical statements

## Goal / expected outcome

The historical import (built and tested on scrubbed sample statements; your real P3-T003 exports are run in P3-T061) and a manual CSV template for anything without a parser produce opening lots with original acquisition dates and cost bases plus opening cash balances per account, reconciled against each statement's closing positions.

## Context & references

- Roadmap: [R3.01, R3.05, T3.20, T3.23](../../../docs/roadmap/phase-3-journal-and-tax.md)
- Inputs: sample statements in `tests/journal/fixtures/statements/` for the build; P3-T003 (USER exports) only in the late check P3-T061 · adapters P3-T014/T015/T016 · command `journal.manual_event.add` (C2) from P3-T055
- 12-month rule depends on true acquisition dates: [09 AU_2026](../../../docs/09-journal-and-tax.md#jurisdiction-plugin-interface)

## Requirements

- Import mode `historical` runs all statement adapters over the inbox in chronological order, producing full history where available (preferred) rather than synthetic opening lots.
- Where history is incomplete, a manual template `config/journal/opening_lots.csv` (asset, account, acquired_date, qty, cost_base_aud, cost_base_ccy, evidence_ref) creates `source = manual` opening lots via `journal.manual_event.add` (C2, reason required, [17 §D P3-B006](../../../docs/17-decisions-register.md#d-other-decisions)), flagged `cost_base_estimated` if evidence is missing.
- Reconcile: per account, computed holdings at statement end = statement closing positions (qty exact; cash within 0.01 of the currency).
- Import report saved to `journal.tax_report` (type `import_report`) with file hashes.

## ToDo

- [ ] Implement `packages/mt_journal/ingest/historical.py` orchestrator + manual CSV loader (one `journal.manual_event.add` C2 command per row, with the CSV row as the reason reference)
- [ ] Reconciliation against statement closing positions
- [ ] Import report generator; tests with scrubbed fixtures; docs

## Verification

### Tests

- Integration: fixture of 2 years IBKR + 1 year OANDA → lots and balances match closing positions.
- Unit: manual CSV with a missing evidence ref → `cost_base_estimated` flag.

### Scenarios

- Given a lot bought 2 Feb 2018 imported from IBKR, when D15 Lots opens, then `acquired` = 2018-02-02 and discount eligibility shows as already met.
- Given an imported closing position differs from computed holdings, when the report runs, then the account is marked `opening_mismatch` and blocks FY reports until resolved or acknowledged.

### Stress / failure injection

- Import 10 years × 5 accounts synthetic history < 15 min; idempotent on re-run.

## Acceptance criteria

- [ ] Every account in the sample fixture set reconciles or has a documented acknowledged mismatch (your real accounts are checked in P3-T061)
- [ ] Import report stored with file hashes
- [ ] Manual events audited in `audit.command`
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Overlapping statements (two exports covering the same period) → dedupe by source_ref.
- Accounts in other currencies → FX via RBA for the historical dates (P1 backfill must cover them; else `pending_fx`).

## Cardinal rules (do NOT)

- Do NOT insert manual events by SQL; use the audited command.
- Do NOT invent cost bases; missing evidence stays flagged.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT expose tax-sensitive fields (TFN, addresses, raw statements) to any LLM prompt, RAG index or the LiteLLM gateway ([07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7.2: none (`journal.manual_event.add` C2 already listed).
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.20, T3.23 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T021-opening-balances-lots-import`
- PR title: `P3-T021: Opening balances and opening lots import from historical statements`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T021` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (manual events are C2 via P3-T055 (was C1, P3-B006); built on sample statements, real exports moved to P3-T061; tools/services filled)
