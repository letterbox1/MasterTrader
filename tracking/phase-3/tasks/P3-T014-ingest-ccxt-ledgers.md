---
id: P3-T014
kind: task
title: Ingestion adapter for ccxt ledgers (funding, fees, transfers)
phase: 3
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T008, P3-T011, P3-T012]
requirements: [R3.01]
roadmap_todos: [T3.20]
modules: [M18]
dashboards: [D14]
branch: p3/P3-T014-ingest-ccxt-ledgers
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

# P3-T014 · Ingestion adapter for ccxt ledgers (funding, fees, transfers)

## Goal / expected outcome

Funding payments, trading fees not on fills, deposits, withdrawals, transfers between sub-accounts, interest and rebates from crypto venues are pulled via ccxt `fetchLedger` (and `fetchFundingHistory`/`fetchDeposits`/`fetchWithdrawals` where needed) with read-only keys, and journalled in three currencies.

## Context & references

- Roadmap: [R3.01, T3.20](../../../docs/roadmap/phase-3-journal-and-tax.md) · exit criterion 1 (funding payments)
- [09 architecture](../../../docs/09-journal-and-tax.md#architecture) · keys policy [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys)
- Cross-phase: P1 T1.02 (read-only IP-locked keys), P1 T1.29 (ccxt reconciliation jobs), P2 T2.03 (per-mode sub-accounts)

## Requirements

- Venues: those in the venue registry with status `allowed` or `read_only` and an account in `ops.wallets` (initially Binance testnet, Bybit testnet, plus any AU spot venue used).
- Schedule: Prefect flow `journal-ccxt-ledger` every 15 min per account + EOD full sweep; cursor per account in `journal.ingest_cursor`; respects the P1 quota tracker.
- Mapping: `funding` → `funding_payment` (sign preserved), `fee` → `fee_only`, `transfer` between own sub-accounts → `internal_transfer` candidate, `deposit`/`withdrawal` → candidates for P3-T018, `rebate`/`interest` → `interest`.
- `source = ccxt_ledger`, `source_ref = venue ledger id`; dedupe against fill-fee events (a fee already on a fill is not double counted: match on trade id).
- Keys read from sops (`<VENUE>_READONLY_KEY`), never logged.

## ToDo

- [ ] Implement `packages/mt_journal/ingest/ccxt_ledger.py` with per-venue quirks map
- [ ] Fee de-duplication against nautilus fill events
- [ ] Prefect deployment + quota tracker integration
- [ ] Golden fixtures (recorded ledger responses, secrets scrubbed) for Binance and Bybit testnet
- [ ] Tests; docs

## Verification

### Tests

- Golden: recorded ledger JSON → expected events (funding sign, fee dedupe).
- Unit: venue paging/cursor edge (same timestamp, multiple entries).
- Integration (testnet, optional in CI): one real funding payment appears.

### Scenarios

- Given an 8-hourly funding on a perp, when the flow runs, then a `funding_payment` event appears with AUD value and links to the position's instrument.
- Given a fee already journalled from the fill, when the ledger shows it, then no second fee event is written.
- Given the venue returns 429, when the flow runs, then it backs off per the quota tracker and resumes from the cursor.

### Stress / failure injection

- Backfill 12 months of ledger entries (synthetic 200k rows) within quota limits; resumable after a kill mid-run.

## Acceptance criteria

- [ ] Funding, fees, deposits and withdrawals journalled for every configured venue
- [ ] No double-counted fees (test)
- [ ] Cursor resume proven
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Venue changes ledger types → unknown type quarantined + alert (format drift).
- Testnet resets wipe history → registry marks the account epoch; old events stay (WORM).

## Cardinal rules (do NOT)

- Do NOT use keys with trade or withdrawal permission for ledger reads.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Keys stay read-only/trade-only, IP-locked, withdrawals disabled; no live money before the P7 gates.
- Do NOT use paid data/APIs or scraping that breaks terms; free tiers only (03 §1).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.20 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T014-ingest-ccxt-ledgers`
- PR title: `P3-T014: Ingestion adapter for ccxt ledgers (funding, fees, transfers)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T014` run

## Progress log

- 2026-10-21 00:00 · planner · created
