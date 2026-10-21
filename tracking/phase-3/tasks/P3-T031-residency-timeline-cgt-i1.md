---
id: P3-T031
kind: task
title: Residency timeline and CGT event I1 modelling
phase: 3
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T022, P3-T030]
requirements: [R3.09]
roadmap_todos: [T3.26]
modules: [M18]
dashboards: [D15]
branch: p3/P3-T031-residency-timeline-cgt-i1
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

# P3-T031 · Residency timeline and CGT event I1 modelling

## Goal / expected outcome

A residency timeline (country, from/to, domicile, permanent home, employment and centre-of-interests evidence) drives which jurisdiction plugin applies per period; on leaving Australia, AU_2026 `on_residency_change` produces CGT event I1 deemed disposals of non-TAP assets at market value, modelled **both** with and without the s104-165 election.

## Context & references

- Roadmap: [R3.09, T3.26](../../../docs/roadmap/phase-3-journal-and-tax.md)
- [09 residency timeline + cross-border events](../../../docs/09-journal-and-tax.md#jurisdiction-plugin-interface) · D15 Residency tab [D15](../../../docs/ui/dashboards/D15-tax.md) · command `tax.residency.add` (C1, re-computation preview first)
- Gap: P3-B007 (residency → M11 contract; C-level when loosening)

## Requirements

- `journal.residency_period` (WORM): country, from, to (nullable), residency basis notes, domicile, evidence notes (encrypted, P3-T007), source (manual / passport-stamp report).
- `tax.residency.add` (C1): validates no overlaps/gaps (gap = `unknown` period warning), shows a recomputation preview (which FYs and plugins change) before applying.
- Each plugin's `is_resident(timeline, tax_year)` evaluates its own tests (AU default: resident while an AU period is active; CY 183/60-day; AE 183 or 90 + conditions; EG 183) — dual-residency → tie-breaker note (DTA status (U)).
- I1: at the AU exit date, snapshot (`kind = residency_I1`) of all non-TAP lots via P3-T030's API; two computations stored: `elect_s104_165 = false` (deemed disposal now) and `= true` (deferral; lots remain with TAP status tracking).
- Lots carry `tap` flag (default false for crypto/foreign shares; true only for Australian real property interests — not expected).

## ToDo

- [ ] Implement `packages/mt_journal/residency/` (model, validation, preview, I1 hook in AU_2026)
- [ ] `tax.residency.add` command handler + preview endpoint
- [ ] Tests; docs

## Verification

### Tests

- Unit: overlapping periods rejected; gap flagged.
- Golden: exit AU on 2028-03-01 → I1 deemed disposal of fixture lots at snapshot values; elected variant has no disposal.
- Unit: plugin selection per FY follows the timeline.

### Scenarios

- Given you enter a move to the UAE from 2028-03-01, when previewed, then D15 shows FY2027-28 split AU/AE, the I1 snapshot to be taken and both s104-165 outcomes.
- Given residency `EG` is entered, when applied, then P3-T033's hard flag activates.

### Stress / failure injection

- n/a: low-volume config path

## Acceptance criteria

- [ ] Timeline drives plugin selection
- [ ] I1 modelled both ways and shown
- [ ] Changes audited and previewed before apply
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Retroactive entry (past move) → recomputation writes superseding reports; locked FYs require unlock first.
- Timezone of the move date → taxpayer-local date in the departure country.

## Cardinal rules (do NOT)

- Do NOT decide residency for the user; the timeline is user-entered evidence for the agent.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."
- Do NOT expose tax-sensitive fields (TFN, addresses, raw statements) to any LLM prompt, RAG index or the LiteLLM gateway ([07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.26 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T031-residency-timeline-cgt-i1`
- PR title: `P3-T031: Residency timeline and CGT event I1 modelling`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T031` run

## Progress log

- 2026-10-21 00:00 · planner · created
