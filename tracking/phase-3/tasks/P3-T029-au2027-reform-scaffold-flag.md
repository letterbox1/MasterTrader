---
id: P3-T029
kind: task
title: AU_2027_REFORM plugin scaffold behind a feature flag
phase: 3
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T023, P1-T027]
requirements: [R3.08]
roadmap_todos: [T3.25]
modules: [M18]
dashboards: [D15]
tools: [git, uv]
mcp: []
env: []
services: [postgres]
branch: p3/P3-T029-au2027-reform-scaffold-flag
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

# P3-T029 · AU_2027_REFORM plugin scaffold behind a feature flag

## Goal / expected outcome

An `AU_2027_REFORM` plugin (valid from FY2027-28) exists behind the `AU_2027_REFORM` flag (default **off**): it splits each lot into pre- and post-reform portions using the 30 June 2027 snapshot, indexes the post-reform cost base by ABS CPI, applies the 30% minimum tax mechanism (U), and when the flag is off D15 still shows its figures side by side as an informational comparison.

## Context & references

- Roadmap: [R3.08, T3.25](../../../docs/roadmap/phase-3-journal-and-tax.md)
- [09 key findings: 2027 reform](../../../docs/09-journal-and-tax.md#️-key-findings-that-shape-the-design) · [11 §3 conflict](../../../docs/11-cryptotrader-crossover-review.md#3-conflicts-and-how-they-were-resolved) · [02 F9 step 4](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Cross-phase prerequisite (depends_on): P1-T027 (ABS CPI via `pit`; series All groups, weighted average of eight capital cities, A2325846C (U), [17 §D P1-B016](../../../docs/17-decisions-register.md#d-other-decisions); tax-agent question 9)
- Snapshot convention: [16 §4.2](../../../docs/16-configuration-and-safety-model.md#42-market-value-snapshot-30-june-2027-and-any-residency-change)
- Related: P3-T002 (agent confirmation), P3-T030 (snapshot), P3-T048 (dry run)

## Requirements

- Pre-reform portion: snapshot value − cost base, eligible for the 50% discount under AU_2026 rules (held ≥ 12 months at 30 June 2027 by the same both-days-excluded test).
- Post-reform portion: proceeds − snapshot value, cost base indexed by ABS CPI (All groups, weighted average of eight capital cities; quarterly) from the quarter of 30 June 2027 to the quarter of disposal; mechanism (U).
- 30% minimum tax on post-reform real gains: computed as an informational figure only (needs marginal-rate inputs) — (U), labelled.
- Lots acquired after 30 June 2027: indexation from acquisition quarter.
- Flag off (default): AU_2026 rules stay primary for FY2027-28; reform figures shown as a comparison column. Flag on: requires P3-T002 answer reference in `config/journal/flags.yaml` (`AU_2027_REFORM: {enabled: true, answer_ref: ...}`); validated at startup.
- Rule version string `AU_2027_REFORM@0.x (U)` on every output.

## ToDo

- [ ] Implement `packages/mt_journal/rules/au_2027_reform/` (plugin + CPI indexer reading ABS CPI via `pit`)
- [ ] Flag validation + comparison-column wiring in reports
- [ ] Synthetic golden tests (clearly marked as mechanism (U)); docs

## Verification

### Tests

- Golden (synthetic): lot cost 10,000, snapshot 15,000, sold 18,000 two years later with CPI +6% → pre-reform gain 5,000 (discount eligible), post-reform real gain 18,000 − 15,900 = 2,100.
- Unit: flag on without `answer_ref` → startup error.
- Unit: CPI quarter lookup uses the release available `as_of` the computation (no look-ahead).

### Scenarios

- Given the flag is off, when D15 Summary for FY2027-28 opens, then AU_2026 is primary and AU_2027_REFORM appears as a labelled comparison.
- Given a lot without a snapshot row (job missed), when computed, then the plugin refuses with `snapshot_missing` and D15 shows a red banner linking the runbook.

### Stress / failure injection

- n/a: same volume as P3-T023

## Acceptance criteria

- [ ] Plugin computes pre/post split and CPI indexation on fixtures
- [ ] Flag default off; enabling needs an answer reference
- [ ] Every output labelled (U) with rule version
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- ABS CPI release lag: disposal quarter CPI not yet published → use latest available with `cpi_provisional` flag; recomputation later writes a superseding report.
- Crypto included per agent answer (P3-T002 question c).

## Cardinal rules (do NOT)

- Do NOT enable the flag in code defaults.
- Do NOT read CPI outside `pit(as_of)`.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.25 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T029-au2027-reform-scaffold-flag`
- PR title: `P3-T029: AU_2027_REFORM plugin scaffold behind a feature flag`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T029` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (CPI series A2325846C (U) and 16 §4.2 snapshot linked; explicit P1-T027 depends_on; tools/services filled)
