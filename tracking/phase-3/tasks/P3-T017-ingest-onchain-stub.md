---
id: P3-T017
kind: task
title: On-chain event adapter stub and wallet-transfer contract
phase: 3
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T008, P3-T011, P3-T012, P0-T016]
requirements: [R3.01]
roadmap_todos: [T3.20]
modules: [M18, M22]
dashboards: []
tools: [git, uv]
mcp: []
env: []
services: [postgres, nats]
branch: p3/P3-T017-ingest-onchain-stub
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T017 · On-chain event adapter stub and wallet-transfer contract

## Goal / expected outcome

The journal consumes on-chain transfers via a defined `wallet.{chain}.{address}.transfer` message contract and accepts a Rotki CSV import, so P5's wallet-indexer can plug in without journal changes; decoding at scale stays out of scope.

## Context & references

- Roadmap: [R3.01, T3.20](../../../docs/roadmap/phase-3-journal-and-tax.md) · scope note: on-chain decoding at scale is P5 (wallet-indexer)
- Subjects in [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) · [13 §3](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view) · Rotki sidecar in [09 tools vetted](../../../docs/09-journal-and-tax.md#tools-vetted)
- Boundary: P5 T5.22 (wallet-indexer publishes transfers and extends `ops.wallets` additively, [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)), P5 T5.29 (airdrop income linking)
- Cross-phase prerequisite (depends_on): P0-T016 (`mt_core` versioned message schemas)
- Values: non-trade transfers and airdrops are valued by P3-T011 per [16 §4.1](../../../docs/16-configuration-and-safety-model.md#41-valuing-crypto-for-the-journal) (long-tail tokens via pool price)

## Requirements

- Message schema `mt_core.schemas.WalletTransfer` v1: chain, tx_hash, log_index, block_time, from, to, asset (contract/mint), amount (string decimal), fee_native, classification hint (`transfer|swap|airdrop|staking|approval`), campaign_id (optional).
- `source = chain`, `source_ref = chain:tx_hash:log_index`; gas → `fee_only` with `fee_type = gas`.
- Rotki CSV import (manual, inbox `rotki/`) mapping decoded events; Rotki P&L ignored (09).
- Airdrop/staking classification left as `airdrop_initial` vs `airdrop_established` **pending** evidence (P5 campaign records); default `needs_classification` flag, never silently income or zero.

## ToDo

- [ ] Define the schema in `packages/mt_core/schemas/wallet.py` (shared with P5)
- [ ] Implement `packages/mt_journal/ingest/onchain.py` consumer + Rotki CSV importer
- [ ] Fixture-based tests; docs (contract described in 13 §3)

## Verification

### Tests

- Unit: schema validation rejects float amounts.
- Golden: Rotki CSV sample → events.
- Integration: publish a test `wallet.eth.0xabc.transfer` → event written.

### Scenarios

- Given a transfer between two registered own addresses, when consumed, then it's an `internal_transfer` candidate for P3-T018 (not a disposal).
- Given an airdrop transfer without campaign evidence, when consumed, then it's journalled with `needs_classification` and appears in D15 Income as unclassified.

### Stress / failure injection

- n/a: stub; volume arrives with P5 (P5 adds its own load tests)

## Acceptance criteria

- [ ] Schema published and versioned
- [ ] Consumer + Rotki import pass tests
- [ ] Unclassified airdrops visibly flagged
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Chain reorg: a later message with the same `source_ref` and `removed = true` → correction row voiding the event.

## Cardinal rules (do NOT)

- Do NOT decode contracts or index chains from the journal (P5 owns that); the only RPC read in the journal is P3-T011's pool-price valuation.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT use paid data/APIs or scraping that breaks terms; free tiers only (03 §1).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §3: reference the `WalletTransfer` v1 contract consumed by the journal.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.20 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T017-ingest-onchain-stub`
- PR title: `P3-T017: On-chain event adapter stub and wallet-transfer contract`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T017` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (valuation via 16 §4.1 service; `ops.wallets` boundary per 17 §B; RPC rule aligned with pool-price tier; explicit P0-T016 depends_on; tools/services filled)
