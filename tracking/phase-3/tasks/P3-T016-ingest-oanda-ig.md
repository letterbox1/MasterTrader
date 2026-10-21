---
id: P3-T016
kind: task
title: Ingestion adapters for OANDA transactions and IG statements
phase: 3
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T008, P3-T011, P3-T012]
requirements: [R3.01]
roadmap_todos: [T3.20]
modules: [M18]
dashboards: []
branch: p3/P3-T016-ingest-oanda-ig
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

# P3-T016 · Ingestion adapters for OANDA transactions and IG statements

## Goal / expected outcome

OANDA v20 transaction stream/history and IG transaction/trade history become journal events (CFD/FX trades, financing, commission, spread costs, deposits/withdrawals), so CFD and FX activity has the revenue-account inputs AU_2026 needs.

## Context & references

- Roadmap: [R3.01, T3.20](../../../docs/roadmap/phase-3-journal-and-tax.md)
- CFD treatment: revenue account ([09 AU_2026](../../../docs/09-journal-and-tax.md#jurisdiction-plugin-interface)); financing as `cfd_financing`
- Cross-phase: P2 T2.25 (OANDA/IG adapters; practice/demo accounts), P1 T1.02 (read-only keys)

## Requirements

- OANDA: v20 `GET /v3/accounts/{id}/transactions/sinceid` (read-only token in sops), types ORDER_FILL, DAILY_FINANCING, TRANSFER_FUNDS, DIVIDEND_ADJUSTMENT; `source_ref = transaction id`.
- IG: REST `/history/transactions` + `/history/activity` (demo) and CSV statement import from the inbox; `source_ref = reference`.
- Map: fills → `trade_open/close` (CFD asset class), financing → `cfd_financing`, transfers → deposit/withdrawal candidates, guaranteed-stop premiums → `fee_only` (commission).
- De-duplicate against nautilus fill events for the same trade (match on venue trade id) — statement data can enrich, never duplicate.
- Schedule: every 30 min + EOD.

## ToDo

- [ ] Implement `packages/mt_journal/ingest/oanda.py` and `ig.py`
- [ ] Dedupe/enrich logic against fill events
- [ ] Golden fixtures from practice/demo accounts (scrubbed); tests; docs

## Verification

### Tests

- Golden: OANDA DAILY_FINANCING → `cfd_financing` with sign and AUD value.
- Golden: IG CSV → events; dedupe vs fill events.
- Unit: hedged positions on IG produce correct open/close pairing.

### Scenarios

- Given a CFD position held over a weekend, when financing posts, then three financing events (or one triple) are journalled as the venue reports them.
- Given IG changes CSV column order, when imported, then the header-driven parser still works; an unknown column is ignored with a warning; a missing required column quarantines the file.

### Stress / failure injection

- Replay 6 months of practice-account transactions; zero duplicates against fills.

## Acceptance criteria

- [ ] Both adapters pass golden tests
- [ ] Financing and commission present for every CFD position day in the fixture
- [ ] No fill duplicated
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- OANDA account currency AUD vs USD: native amounts in account currency; FX stamping per P3-T010.
- IG demo resets → account epoch noted.

## Cardinal rules (do NOT)

- Do NOT use trading-enabled tokens for reads where a read-only token exists.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Keys stay read-only/trade-only, IP-locked, withdrawals disabled; no live money before the P7 gates.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.20 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T016-ingest-oanda-ig`
- PR title: `P3-T016: Ingestion adapters for OANDA transactions and IG statements`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T016` run

## Progress log

- 2026-10-21 00:00 · planner · created
