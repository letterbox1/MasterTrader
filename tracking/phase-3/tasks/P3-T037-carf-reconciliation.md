---
id: P3-T037
kind: task
title: CARF reconciliation scaffold (venue-reported vs journal)
phase: 3
type: BUILD
status: backlog
priority: low
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T019, P3-T022]
requirements: [R3.10, R3.11]
roadmap_todos: [T3.27, T3.28]
modules: [M18]
dashboards: [D15]
tools: [git, uv]
mcp: []
env: []
services: [postgres]
branch: p3/P3-T037-carf-reconciliation
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

# P3-T037 · CARF reconciliation scaffold (venue-reported vs journal)

## Goal / expected outcome

The journal can import **venue-provided** annual crypto statements (CARF/CRS 2.0 style statements or venue tax reports, CSV) when a venue provides one, store each venue's tax-residency declaration, and produce a reconciliation report of venue-reported vs journal totals per venue and year; where a venue provides no statement the check is marked **not applicable** ([17 §D P3-B010](../../../docs/17-decisions-register.md#d-other-decisions)).

## Context & references

- Roadmap: [R3.10, T3.27](../../../docs/roadmap/phase-3-journal-and-tax.md) (R3.10 lists CARF reconciliation)
- [09 cross-border events: CARF / CRS 2.0](../../../docs/09-journal-and-tax.md#jurisdiction-plugin-interface) · agent question 7 (AU CARF start) ([09](../../../docs/09-journal-and-tax.md#questions-for-your-tax-agent-tracked-as-tasks))
- Decision: [17 §D P3-B010](../../../docs/17-decisions-register.md#d-other-decisions) (use venue-provided statements when available; otherwise not applicable) · [09 CARF / CRS 2.0](../../../docs/09-journal-and-tax.md#jurisdiction-plugin-interface)
- Related: P3-T019 (journal disposal totals), P3-T022 (report provenance); no dependency on the daily recon

## Requirements

- Table `journal.venue_reported_total` (WORM): venue, account, period, metric (gross proceeds, gross acquisitions, transfers out, count), value, currency, source file hash.
- Table `journal.venue_residency_declaration` (WORM): venue, declared country, date, evidence ref.
- Generic CSV importer with a column map per venue in `config/journal/carf_maps/<venue>.yaml`.
- Report `carf_recon` (type in `journal.tax_report`): per venue/year status `reconciled | differences | not_applicable` (no venue statement); per metric diff; the flag threshold is a setting (default 1% or AUD 100) in `config/journal/carf.yaml`.
- Australia's CARF start is (U) (2027/28 reported); the scaffold is ready, no data expected yet.

## ToDo

- [ ] Migrations + importer + report
- [ ] Sample map for one venue from its annual statement CSV
- [ ] Tests; docs

## Verification

### Tests

- Unit: sample venue totals vs fixture journal → diff report.
- Unit: residency declaration stored and shown.
- Unit: a venue/year with no statement → `not_applicable`, never `reconciled`.

### Scenarios

- Given a venue annual statement showing proceeds 12,000 AUD, when the journal shows 11,500, then the report flags a 500 difference with event drill-down.

### Stress / failure injection

- n/a: low volume, annual

## Acceptance criteria

- [ ] Import + report work on a sample
- [ ] Report listed in D15 Reports
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Venue reports in USD → converted with RBA for the period's end per the venue's own convention (documented in the map).

## Cardinal rules (do NOT)

- Do NOT change journal data to match venue totals; differences are explained or corrected via events.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.27, T3.28 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T037-carf-reconciliation`
- PR title: `P3-T037: CARF reconciliation scaffold (venue-reported vs journal)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T037` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (CARF uses venue-provided statements, else not applicable (P3-B010 closed); threshold a setting; depends_on trimmed (no daily-recon dependency); tools/services filled)
