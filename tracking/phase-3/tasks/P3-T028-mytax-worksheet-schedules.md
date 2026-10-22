---
id: P3-T028
kind: task
title: myTax worksheet, CGT and income schedules with GST/BAS mode dormant
phase: 3
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T025, P3-T026]
requirements: [R3.06, R3.12]
roadmap_todos: [T3.24]
modules: [M18]
dashboards: [D15]
tools: [git, uv]
mcp: []
env: []
services: [postgres]
branch: p3/P3-T028-mytax-worksheet-schedules
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

# P3-T028 · myTax worksheet, CGT and income schedules with GST/BAS mode dormant

## Goal / expected outcome

For any FY, the system generates a myTax worksheet (item mapping 18 capital gains, 20 foreign income, 24 other income, 10/11 interest/dividends, business schedule if trading, labels (U)), a CGT schedule and an income schedule, as reproducible reports carrying rule version, FX/price sources and hash, with a dormant GST/BAS mode behind a flag.

## Context & references

- Roadmap: [R3.06, R3.12, T3.24](../../../docs/roadmap/phase-3-journal-and-tax.md)
- [09 AU_2026 myTax mapping](../../../docs/09-journal-and-tax.md#jurisdiction-plugin-interface) · [09 quality](../../../docs/09-journal-and-tax.md#quality) · D15 Reports tab [D15](../../../docs/ui/dashboards/D15-tax.md) · command `tax.report.generate` (C1)

## Requirements

- Report types: `mytax_worksheet`, `cgt_schedule`, `income_schedule`, each per FY and regime (both when undecided).
- Each line: myTax item/label (U-labelled), amount AUD, drill-down event ids, notes (e.g. `needs_classification` exclusions).
- Outputs: JSON (canonical, hashed) + CSV + PDF (WeasyPrint, local fonts, no network); footer "Not tax advice. Confirm with a registered tax agent." + rule version + FX source + valuation methods + hash.
- Stored in `journal.tax_report` + file under `/srv/mastertrader/journal/exports/<fy>/`; same inputs → same hash (no timestamps in the hashed body).
- `GST_BAS_MODE` flag (default false): when false, no GST computation code path runs; a stub returns `dormant`.

## ToDo

- [ ] Implement `packages/mt_journal/reports/mytax.py`, `cgt_schedule.py`, `income_schedule.py`, PDF templates
- [ ] `tax.report.generate` command handler (C1) + idempotency on inputs hash
- [ ] GST/BAS dormant stub + flag test
- [ ] Tests; docs

## Verification

### Tests

- Golden: fixture FY → worksheet JSON byte-identical to the golden file; PDF text extraction contains rule version and hash.
- Unit: regenerate → same hash, no duplicate row.
- Unit: GST/BAS flag off → no GST lines.

### Scenarios

- Given an FY with unclassified airdrops, when the worksheet is generated, then they're excluded and listed as blocking notes.
- Given a rule version bump, when regenerated, then a new report row with a new hash; the old one shows `superseded_by_rule_version`.

### Stress / failure injection

- Generate all reports for an FY with 50k events < 2 min; PDF < 10 MB.

## Acceptance criteria

- [ ] All three reports reproducible (hash test)
- [ ] Every report footer has rule version, FX source, hash and the not-advice line
- [ ] GST/BAS stays dormant
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Locked FY (`tax.fy.lock`, P3-T055) → generation allowed (read-only) but no regime/lot changes.
- Item label uncertainty → shown with (U) until the agent confirms.

## Cardinal rules (do NOT)

- Do NOT include TFN in generated files unless the accountant pack explicitly needs it (decrypted only at generation, P3-T036).
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."
- Do NOT expose tax-sensitive fields (TFN, addresses, raw statements) to any LLM prompt, RAG index or the LiteLLM gateway ([07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.24 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T028-mytax-worksheet-schedules`
- PR title: `P3-T028: myTax worksheet, CGT and income schedules with GST/BAS mode dormant`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T028` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (locked FY via P3-T055; valuation methods in footer (R3.12); tools/services filled)
