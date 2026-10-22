---
id: P3-T018
kind: task
title: Internal-transfer matcher across own accounts and wallets
phase: 3
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T008, P3-T012]
requirements: [R3.04]
roadmap_todos: [T3.22]
modules: [M18, M22]
dashboards: []
tools: [git, uv]
mcp: []
env: []
services: [postgres]
branch: p3/P3-T018-internal-transfer-matcher
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

# P3-T018 · Internal-transfer matcher across own accounts and wallets

## Goal / expected outcome

Every withdrawal from one registered account that lands as a deposit in another registered account is linked as an `internal_transfer` (never a disposal), the lots move with their original acquisition dates and cost base, and the network/withdrawal fee is recorded; unmatched legs go to a review list.

## Context & references

- Roadmap: [R3.04, T3.22](../../../docs/roadmap/phase-3-journal-and-tax.md)
- [09 goals §6](../../../docs/09-journal-and-tax.md#goals) (internal transfers never disposals) · [13 §3](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view)
- Related: P3-T012 registry (`ops.wallets`), P3-T019 lot engine (lot relocation), P3-T014/T017 (transfer legs; tests use synthetic events so this can be built in parallel), P3-T046 property tests

## Requirements

- Match keys in order: (1) same tx hash / venue transfer id on both legs; (2) same asset, amount_out − fee = amount_in within 0.1% or the venue's fee, time window ≤ 6 h (setting, default; ≤ 72 h for fiat bank rails) in `config/journal/transfers.yaml`, destination address = registered address.
- Writes `journal.transfer_link` (WORM) with both event ids, method, confidence; legs re-labelled via superseding events `internal_transfer` (never edits).
- Lot relocation: lots move `account_id` with unchanged `acquired_at`/cost base; the fee is a separate `fee_only` (gas/withdrawal) event — whether the fee is a disposal of a small amount of the asset is an AU_2026 classification (default: CGT disposal of the fee quantity, flagged (U)).
- Unmatched after the window → `transfer_unmatched` review item in D14 and a reconciliation note; never auto-classified as a disposal.

## ToDo

- [ ] Implement `packages/mt_journal/transfers/matcher.py` (scheduled + on-event)
- [ ] Lot relocation hook used by P3-T019
- [ ] Review list query for D14
- [ ] Tests (unit + property); docs

## Verification

### Tests

- Unit: tx-hash match; amount-minus-fee match; window boundary; multi-leg (one withdrawal split into two deposits).
- Property: for any generated set of own-account transfers, total quantity per asset across accounts is conserved and no disposal is created.

### Scenarios

- Given BTC withdrawn from Binance to your Ledger address with a 0.0002 BTC fee, when matched, then lots relocate, a fee event exists and no capital gain appears.
- Given a deposit from an unregistered address, when processed, then it's an external deposit (acquisition needs a cost base → review), not internal.

### Stress / failure injection

- 10k random transfer pairs with noise; precision ≥ 99.9% on synthetic ground truth; runtime < 2 min.

## Acceptance criteria

- [ ] Zero disposals generated from own-account transfers in tests
- [ ] Unmatched legs visible in D14 review list
- [ ] Fee treatment flagged (U) and listed as an agent question
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Exchange deposits credited later than 72 h → late match supersedes the unmatched flag.
- Same amount, two candidates → lowest time gap wins; tie → review.

## Cardinal rules (do NOT)

- Do NOT classify an unmatched transfer as a disposal automatically.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.22 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T018-internal-transfer-matcher`
- PR title: `P3-T018: Internal-transfer matcher across own accounts and wallets`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T018` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (depends_on trimmed to true preconditions (writer + registry) for parallel work; windows are settings; tools/services filled)
