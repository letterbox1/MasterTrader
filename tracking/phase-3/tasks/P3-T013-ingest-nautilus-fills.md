---
id: P3-T013
kind: task
title: Ingestion adapter for Nautilus fills and positions
phase: 3
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T008, P3-T011, P3-T012, P3-T009]
requirements: [R3.01]
roadmap_todos: [T3.20]
modules: [M18, M12]
dashboards: [D14]
branch: p3/P3-T013-ingest-nautilus-fills
pr: ""
doc_sync: [docs/ui/dashboards/D14-journal.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-T013 · Ingestion adapter for Nautilus fills and positions

## Goal / expected outcome

Every paper (and later live) fill published by the engine on `fill.{venue}` becomes a journal event within **5 s**, with fees split by type, `strategy_id`, `bot_id`, signal provenance link and paper/live mode, satisfying exit criterion 1 for trades and fees.

## Context & references

- Roadmap: [R3.01, T3.20](../../../docs/roadmap/phase-3-journal-and-tax.md) · exit criterion 1
- [02 F2 step 7 and F9](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · subjects `fill.{venue}` / `pos.{account}` in [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) · [D14 acceptance 1](../../../docs/ui/dashboards/D14-journal.md) (≤ 5 s)
- Cross-phase: P2 T2.25 (`mt_engine`, `audit.fill`), P2 T2.34 (bots), P2 R2.31 (STP cancels recorded as non-fills)

## Requirements

- Durable consumer `journal-fills` on `fill.>`; map each Nautilus `OrderFilled` → `trade_open`/`trade_close` (position-aware) with `source = nautilus`, `source_ref = venue exec id` (fallback `trade_id + client_order_id`).
- Fees: commission, exchange, regulatory split when the venue provides it; otherwise `commission` with `fee_split = venue_total`; spread markup for CFDs from `audit.fill` if present.
- Link `strategy_id`, `bot_id`, `signal_id`, `decision_run_id`, `client_order_id` so D14 can show the provenance chain.
- Paper vs live: `mode` from the account registry; paper events are journalled and reported separately (D14 toggle; tax reports exclude `mode = paper` by default with an explicit include switch for demos).
- Latency: p95 fill-published → row committed + `journal.event.new` < 5 s.
- STP cancels and rejected orders never create events (non-fills).

## ToDo

- [ ] Implement `packages/mt_journal/ingest/nautilus_fills.py` (Adapter protocol)
- [ ] Position-aware open/close classification (per account × instrument, netting vs hedging accounts)
- [ ] Prometheus histogram `journal_fill_ingest_seconds`; alert if p95 > 5 s for 10 min
- [ ] Golden fixtures from P2 paper runs (Binance testnet, OANDA practice, IG demo, Alpaca paper)
- [ ] Tests; docs

## Verification

### Tests

- Golden: fixture fills for 4 venues → expected journal rows (byte-identical canonical JSON).
- Integration: publish 100 fills to a test NATS; all journalled once; p95 latency < 5 s.
- Unit: partial fills of one order → separate events summing to order qty.

### Scenarios

- Given a paper fill on Binance testnet, when published, then D14 shows it within 5 s with fee and AUD value.
- Given an STP cancel, when processed, then no event is written.
- Given the engine republishes fills after a restart, when consumed, then no duplicates (writer idempotency).

### Stress / failure injection

- Burst 2,000 fills in 10 s (grid strategy); p95 still < 5 s; no consumer redelivery storm.

## Acceptance criteria

- [ ] Every `audit.fill` row of the test day has exactly one matching journal event
- [ ] p95 ingest < 5 s measured
- [ ] Provenance ids present on 100% of strategy fills
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Venue disconnect → fills arrive late after reconcile; `ts_utc` is the venue time, not arrival.
- Hedging-mode accounts (OANDA/IG) can hold long and short simultaneously → classification per position id.

## Cardinal rules (do NOT)

- Do NOT read fills directly from venue APIs here (that's reconciliation, P3-T034).
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/ui/dashboards/D14-journal.md`: confirm the provenance fields shown match those journalled.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.20 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T013-ingest-nautilus-fills`
- PR title: `P3-T013: Ingestion adapter for Nautilus fills and positions`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T013` run

## Progress log

- 2026-10-21 00:00 · planner · created
