---
id: P3-T026
kind: task
title: Wash-sale flags on loss disposals reacquired within the window
phase: 3
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T023]
requirements: [R3.06]
roadmap_todos: [T3.24]
modules: [M18]
dashboards: [D15]
tools: [git, uv]
mcp: []
env: []
services: [postgres]
branch: p3/P3-T026-wash-sale-flags
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

# P3-T026 · Wash-sale flags on loss disposals reacquired within the window

## Goal / expected outcome

Every loss disposal followed by reacquisition of the same (or substantially identical) asset within N days is flagged (with extra weight for May–July), shown inline in D15, published as a compliance flag, and nothing in the system ever suggests tax-loss harvesting with reacquisition.

## Context & references

- Roadmap: [R3.06, T3.24](../../../docs/roadmap/phase-3-journal-and-tax.md)
- [09 key findings: wash sales (TR 2008/1, Part IVA)](../../../docs/09-journal-and-tax.md#️-key-findings-that-shape-the-design) · D15 rules (wash-sale warnings inline) [D15](../../../docs/ui/dashboards/D15-tax.md)
- Default: [16 §4.4](../../../docs/16-configuration-and-safety-model.md#44-tax-flags) (30 days either side, flag only) · decision [17 §C P3-B004](../../../docs/17-decisions-register.md#c-defaults-that-were-n-or-unspecified) · tax-agent question 12 (window and near-identical assets)

## Requirements

- Window = re-acquisition within **30 days either side** of a loss disposal (default from 16 §4.4, a setting in `config/journal/au_settings.yaml`, never a constant; the agent confirms via 09 question 12); marker `eofy_window` when the disposal is between 1 May and 31 July (extra attention, 09).
- Same asset = the same instrument (the same asset on two venues counts, e.g. BTC on two exchanges). Near-identical assets (e.g. BTC spot vs a BTC ETF) are a tax-agent question; the mapping table ships **empty** and any entry you add is labelled (U).
- Output: `wash_sale_flag` on CGT line items + a `compliance_flags()` entry; **flag only**: nothing is blocked or adjusted automatically and the computed loss is unchanged (16 §4.4).
- Publish `alert.info.wash_sale` once per flagged disposal; M8/M21 guard rule (documented for P6) that agents must not propose sell-and-rebuy for tax reasons.

## ToDo

- [ ] Implement `rules/au_2026/wash_sale.py` + config
- [ ] Identical-asset mapping file
- [ ] Tests; docs

## Verification

### Tests

- Unit: loss on 10 June, rebuy 25 June → flagged `eofy_window`; rebuy 15 July (35 days) → not flagged at N=30.
- Unit: gain disposals never flagged.
- Unit: cross-venue same asset flagged.

### Scenarios

- Given a loss sale and rebuy within 30 days, when D15 Capital gains opens, then the row shows a wash-sale warning with the reacquisition event link.

### Stress / failure injection

- n/a: O(n log n) scan, covered by FY compute benchmark

## Acceptance criteria

- [ ] Flags appear on fixture cases
- [ ] Window configurable and shown on the report
- [ ] No code path recommends tax-loss harvesting
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Reacquisition through an airdrop/staking reward of the same asset → flagged (informational).

## Cardinal rules (do NOT)

- Do NOT implement or suggest tax-loss harvesting with reacquisition anywhere (09).
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.24 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T026-wash-sale-flags`
- PR title: `P3-T026: Wash-sale flags on loss disposals reacquired within the window`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T026` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (30-day window and flag-only from 16 §4.4 (P3-B004 closed); same asset = same instrument, near-identical is agent Q12; tools/services filled)
