---
id: P3-T015
kind: task
title: Ingestion adapter for IBKR Flex statements
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
branch: p3/P3-T015-ingest-ibkr-flex
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

# P3-T015 · Ingestion adapter for IBKR Flex statements

## Goal / expected outcome

IBKR Flex Activity statements (XML), from the inbox or the Flex Web Service, are parsed into journal events (trades, commissions, dividends with withholding, interest, FX conversions, transfers, corporate actions) with golden-file tests per format version.

## Context & references

- Roadmap: [R3.01, T3.20](../../../docs/roadmap/phase-3-journal-and-tax.md)
- Importer references: LibreFolio / Investment-Portfolio-Tracker IBKR Flex importers in [09 tools vetted](../../../docs/09-journal-and-tax.md#tools-vetted)
- Related: P3-T003 (your exports), P3-T021 (opening lots), P3-T007 (raw payload encryption)

## Requirements

- Inputs: `/srv/mastertrader/journal/inbox/ibkr/<account>/*.xml` and, if `IBKR_FLEX_TOKEN` exists in sops, a daily Flex Web Service pull (read-only token).
- Sections: Trades (incl. `ibCommission`, `openCloseIndicator`), CashTransactions (dividends, withholding tax, broker interest), Transfers, CorporateActions, ConversionRates (stored for reference only; tax AUD uses RBA).
- `source = broker_stmt`, `source_ref = tradeID / transactionID`; each file's raw XML stored encrypted with `raw_payload_hash`.
- Dividends: gross, withholding (→ foreign tax paid), franking (n/a for IBKR US stocks → 0).
- Format drift: unknown element/attribute → file quarantined, alert, no partial import.

## ToDo

- [ ] Implement `packages/mt_journal/ingest/ibkr_flex.py` (lxml, secure parser: no external entities)
- [ ] Inbox watcher (Prefect flow `journal-inbox`, every 30 min) shared by statement adapters
- [ ] Flex Web Service client (optional) with token from sops
- [ ] Golden files (scrubbed) per Flex version; tests; docs

## Verification

### Tests

- Golden: sample Flex XML (paper account) → expected events.
- Security: XXE payload file is rejected.
- Unit: dividend with withholding produces dividend + foreign tax paid fields.

### Scenarios

- Given the same Flex file dropped twice, when ingested, then no duplicates.
- Given a restated trade (IBKR correction), when re-ingested, then a superseding event is written.

### Stress / failure injection

- Ingest a 5-year Flex file (~50k rows) in < 5 min; memory bounded (streaming parse).

## Acceptance criteria

- [ ] Golden tests pass for trades, cash, transfers, corporate actions
- [ ] Quarantine on unknown format proven
- [ ] Raw XML encrypted at rest
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Corporate actions (splits) → `corporate_action` events that adjust lots in P3-T019, never edit old lots.
- Multi-currency cash → feeds Div 775 FX-cash lots (P3-T020).

## Cardinal rules (do NOT)

- Do NOT parse XML with external entity resolution enabled.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT expose tax-sensitive fields (TFN, addresses, raw statements) to any LLM prompt, RAG index or the LiteLLM gateway ([07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.20 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T015-ingest-ibkr-flex`
- PR title: `P3-T015: Ingestion adapter for IBKR Flex statements`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T015` run

## Progress log

- 2026-10-21 00:00 · planner · created
