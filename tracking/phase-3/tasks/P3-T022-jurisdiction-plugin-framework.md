---
id: P3-T022
kind: task
title: Jurisdiction plugin framework with dated rule versions and report provenance
phase: 3
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T008]
requirements: [R3.06, R3.12, R3.09]
roadmap_todos: [T3.24, T3.26]
modules: [M18]
dashboards: []
tools: [git, uv]
mcp: []
env: []
services: [postgres]
branch: p3/P3-T022-jurisdiction-plugin-framework
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

# P3-T022 · Jurisdiction plugin framework with dated rule versions and report provenance

## Goal / expected outcome

The `JurisdictionRules` protocol from 09 is implemented with a registry of dated plugins selected by the residency timeline, and every computation and report records the rule version, the FX/price sources and a content hash, so the same inputs always give the same output hash.

## Context & references

- Roadmap: [R3.06, R3.09, R3.12, T3.24, T3.26](../../../docs/roadmap/phase-3-journal-and-tax.md)
- Interface: [09 jurisdiction plugin interface](../../../docs/09-journal-and-tax.md#jurisdiction-plugin-interface) · [09 quality](../../../docs/09-journal-and-tax.md#quality) (rule version + FX source on every report)
- Reproducibility: [D15 acceptance 2](../../../docs/ui/dashboards/D15-tax.md) (same inputs → same hash)
- `fx_policy`: RBA F11 for AUD (last published business day; non-F11 via USD) and the crypto valuation hierarchy ([16 §4.1](../../../docs/16-configuration-and-safety-model.md#41-valuing-crypto-for-the-journal), P3-T011)
- Related: P3-T019 (lot engine supplies `lot_policy` inputs; the framework only defines the types, so it can start once the event model exists)

## Requirements

- Protocol fields/methods exactly as 09: `code`, `valid_from`, `valid_to`, `home_currency`, `tax_year`, `is_resident`, `classify`, `lot_policy`, `fx_policy`, `compute`, `on_residency_change`, `reports`, `compliance_flags`.
- Registry: plugins discovered via entry points `mt_journal.jurisdictions`; selection by (residency period, FY, feature flags); `AU_2026` default for AU through FY2026-27.
- `TaxComputation` result (msgspec): inputs manifest (event ids + computation ids + FX rate ids), rule version (`AU_2026@<semver>+<git sha>`), FX/price sources and valuation-method summary, regime, totals, line items; canonical JSON → sha256 `result_hash`.
- Persist each computation to `journal.tax_report` (WORM) with `rule_version`, `fx_sources`, `inputs_hash`, `result_hash`, `generated_by` (command id).
- Determinism: no wall-clock in computations; `as_of` explicit; Decimal context fixed.

## ToDo

- [ ] Implement `packages/mt_journal/rules/base.py` (Protocol, TaxYear, Treatment enum, TaxComputation)
- [ ] Registry + selection in `rules/registry.py`; feature flags in `config/journal/flags.yaml` (`AU_2027_REFORM: false`, `GST_BAS_MODE: false`) and tax settings in `config/journal/au_settings.yaml` (wash-sale window default 30 days, [16 §4.4](../../../docs/16-configuration-and-safety-model.md#44-tax-flags)); every setting value used is recorded in the report provenance
- [ ] Report provenance writer in `reports/provenance.py`
- [ ] Tests; docs

## Verification

### Tests

- Unit: AU `tax_year` for 2027-06-30 = FY2026-27 and 2027-07-01 = FY2027-28 (taxpayer-local).
- Determinism: compute the same FY twice → identical `result_hash`; change one FX rate id → different hash.
- Unit: plugin selection by residency + date + flag.

### Scenarios

- Given an FY report, when you open it in D15, then the footer shows rule version, FX source (RBA F11), price sources and the hash.
- Given two identical generate commands, when run, then the second reuses the stored report (same hash) instead of writing a duplicate.

### Stress / failure injection

- n/a: framework; performance measured in P3-T023/T052

## Acceptance criteria

- [ ] Protocol + registry merged; at least a dummy plugin passes the conformance test suite
- [ ] Every stored report has rule version, sources and hashes
- [ ] Reproducibility test green
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Rule bug fix → new rule version; old reports stay (WORM) and D15 marks them `superseded_by_rule_version`.

## Cardinal rules (do NOT)

- Do NOT compute tax outside a plugin; do NOT hard-code "50% if held ≥ 12 months" anywhere outside AU_2026.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.24, T3.26 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T022-jurisdiction-plugin-framework`
- PR title: `P3-T022: Jurisdiction plugin framework with dated rule versions and report provenance`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T022` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (fx_policy = RBA rule + 16 §4.1 valuation; settings recorded in provenance; depends_on trimmed to P3-T008 for parallel start; tools/services filled)
