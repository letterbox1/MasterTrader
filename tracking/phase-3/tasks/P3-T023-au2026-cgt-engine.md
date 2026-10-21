---
id: P3-T023
kind: task
title: AU_2026 capital gains with 12-month discount and loss ordering
phase: 3
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T020, P3-T022]
requirements: [R3.06]
roadmap_todos: [T3.24]
modules: [M18]
dashboards: [D15]
branch: p3/P3-T023-au2026-cgt-engine
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

# P3-T023 · AU_2026 capital gains with 12-month discount and loss ordering

## Goal / expected outcome

The `AU_2026` plugin computes investor-regime CGT per FY: per-parcel 50% discount for lots held at least 12 months **excluding both the acquisition and disposal days**, capital losses applied before the discount and to non-discount gains first, net capital losses carried forward, crypto↔crypto disposals as CGT events, and income-asset cost bases (staking/established airdrops at AUD value; initial-allocation airdrops at $0).

## Context & references

- Roadmap: [R3.06, T3.24](../../../docs/roadmap/phase-3-journal-and-tax.md) · golden suite P3-T045
- Rules: [09 AU_2026 row](../../../docs/09-journal-and-tax.md#jurisdiction-plugin-interface) · [09 key findings](../../../docs/09-journal-and-tax.md#️-key-findings-that-shape-the-design) · correct ATO details from isaacrowntree/ledger ([09 tools vetted](../../../docs/09-journal-and-tax.md#tools-vetted))
- D15 Capital gains tab fields: [D15](../../../docs/ui/dashboards/D15-tax.md)

## Requirements

- Discount eligibility: disposal local date ≥ acquisition local date + 1 year + 1 day (bought 2 Feb 2018 → eligible on disposals from 3 Feb 2019); leap years handled by calendar arithmetic, not 365 days.
- Cost base = purchase price + incidental costs (brokerage, fees on acquisition) in AUD at acquisition FX; proceeds = gross − disposal costs.
- Loss ordering per FY: current-year capital losses + carried-forward losses applied first to non-discount gains, then to discount gains; then 50% discount on the remaining discount gains; net capital loss carried forward to the next FY (`journal.tax_report` stores the carry-forward).
- Crypto: every disposal incl. crypto↔crypto is a CGT event (proceeds = AUD market value of what's received); fee-in-crypto disposals per P3-T018 default.
- Income-linked lots: staking rewards and `airdrop_established` → ordinary income at AUD value and that value is the cost base; `airdrop_initial` → $0 cost base; `needs_classification` → excluded from totals with a blocking D15 warning.
- Personal-use asset and other exemptions are out of scope (flag only).
- Lines carry: asset, acquired, disposed, holding days (both excluded), discount eligible, cost base, proceeds, gain/loss, method (specific ID / FIFO), wash-sale flag.

## ToDo

- [ ] Implement `packages/mt_journal/rules/au_2026/cgt.py` (+ `classify` for capital events)
- [ ] Loss-ordering + carry-forward across FYs (reads prior FY report carry-forward)
- [ ] Line-item model for D15 Capital gains
- [ ] Golden tests from ATO worked examples (data in `tests/golden/au_2026/cgt/*.yaml`); docs

## Verification

### Tests

- Golden (ATO-style): discount boundary 2 Feb 2018 → 3 Feb 2019 eligible, 2 Feb 2019 not.
- Golden: loss ordering example (non-discount gain 1,000; discount gain 4,000; loss 2,000 → net = (4,000 − 1,000) × 50% = 1,500).
- Golden: crypto↔crypto swap BTC→ETH produces a BTC disposal at ETH market value and an ETH lot at that value.
- Golden: staking reward income → cost base equals income value.

### Scenarios

- Given a lot held 366 days including a 29 Feb, when disposed, then eligibility uses calendar dates (eligible) — test both sides of the boundary.
- Given a net capital loss in FY2026-27, when FY2027-28 is computed, then the carry-forward is applied first to non-discount gains.

### Stress / failure injection

- Compute an FY with 50k disposals < 60 s; deterministic hash across 3 runs.

## Acceptance criteria

- [ ] All AU_2026 CGT golden tests pass
- [ ] Discount boundary case surfaced for D15 rule-check panel
- [ ] Carry-forward persisted and reused
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Disposal on the same local day as acquisition → 0 holding days, never discount.
- Events crossing midnight UTC vs Sydney → local date rules.
- Trader-in-business regime ignores the discount (P3-T025 handles the alternate computation).

## Cardinal rules (do NOT)

- Do NOT use a 365-day test (the miladtm94 bug noted in 09).
- Do NOT apply the discount before losses.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.24 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T023-au2026-cgt-engine`
- PR title: `P3-T023: AU_2026 capital gains with 12-month discount and loss ordering`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T023` run

## Progress log

- 2026-10-21 00:00 · planner · created
