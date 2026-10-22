---
id: P3-T008
kind: task
title: Journal event model, normaliser and idempotent append-only writer
phase: 3
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T005, P0-T016]
requirements: [R3.01, R3.02]
roadmap_todos: [T3.20]
modules: [M18]
dashboards: []
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, nats]
branch: p3/P3-T008-journal-event-model-writer
pr: ""
doc_sync: [docs/09-journal-and-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T008 · Journal event model, normaliser and idempotent append-only writer

## Goal / expected outcome

`mt_journal` has one typed `JournalEvent` model, a normaliser interface every ingestion adapter implements, and a writer that appends events idempotently (same `source`+`source_ref` never twice), handles corrections as superseding rows, stores the raw payload hash, and publishes `journal.event.new`.

## Context & references

- Roadmap: [R3.01, R3.02, T3.20](../../../docs/roadmap/phase-3-journal-and-tax.md)
- [09 architecture](../../../docs/09-journal-and-tax.md#architecture) · [09 journal event](../../../docs/09-journal-and-tax.md#journal-event-captured-per-transaction) · [02 §6 NATS](../../../docs/02-v1-architecture.md#6-messaging-nats) (`journal.event.new`) · [02 F9](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Cross-phase prerequisite (depends_on): P0-T016 (`mt_core` domain types and versioned message schemas)
- Write path when Postgres is down: [16 §3.3](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check) (buffer in JetStream; bounds and M11 hook in P3-T057)
- Used by: P3-T013…P3-T017 adapters, P3-T019 lot engine

## Requirements

- `JournalEvent` (msgspec, Decimal fields) with all 09 fields; `event_type` enum covering: trade_open, trade_close, swap_crypto, deposit, withdrawal, internal_transfer, staking_reward, airdrop_established, airdrop_initial, mining, interest, dividend, funding_payment, borrow_fee, cfd_financing, futures_variation_margin, expiry_settlement, fork, gift, loss_theft, fee_only, corporate_action, fx_conversion.
- `Adapter` protocol: `fetch(cursor) -> Iterable[RawRecord]`, `normalise(raw) -> list[JournalEvent]`, `cursor_after(raw)`; cursors persisted in `journal.ingest_cursor`.
- Writer: single transaction per batch; dedupe on `(source, source_ref)`; `raw_payload_hash = sha256(canonical raw)`; same ref with a different hash → **correction** row with `supersedes_event_id` + reason `source_restated` (never an edit).
- `taxpayer_local_date` computed from `ts_utc` in the residency timezone (default Australia/Sydney) — drives FY and the day-count.
- Publishes `journal.event.new` {event_id, event_type, account_id, instrument, amt_aud, mode} after commit; WS topic `journal` via mt-api.
- Manual events: `source = manual` only through `journal.manual_event.add` (C2, reason required; handler in P3-T055); never direct SQL.
- Values: trades carry the fill price; non-trade crypto values come from the valuation service (P3-T011, [16 §4.1](../../../docs/16-configuration-and-safety-model.md#41-valuing-crypto-for-the-journal)) before insert.
- Locked FY: an event whose taxpayer-local date is in a locked FY is appended to `journal.ingest_held`, not `journal.event` (rule owned by P3-T055).
- Postgres unreachable: the writer leaves NATS messages un-acked and uses the `mt_store.worm.buffer` path (P3-T057) for anything it has already accepted; nothing is lost and nothing executes without a record.

## ToDo

- [ ] Implement `packages/mt_journal/model.py`, `normalise.py` (Adapter protocol), `writer.py`, `cursor.py`
- [ ] Implement correction logic + `current_event` usage in readers
- [ ] NATS publisher for `journal.event.new` (schema in `mt_core.schemas`)
- [ ] Unit/property tests; adapter test harness (`tests/journal/harness.py`) that every adapter reuses with golden files
- [ ] Docs: event type list in 09

## Verification

### Tests

- Unit: every event type round-trips msgspec ↔ DB row; Decimal precision kept (no rounding below instrument precision).
- Property (Hypothesis): writing the same batch N times yields exactly one row per `source_ref`; random restatements produce a correction chain whose `current_event` equals the last version.
- Unit: `taxpayer_local_date` for 2027-06-30T14:30Z is 2027-07-01 in Australia/Sydney (FY boundary).

### Scenarios

- Given a fill already journalled, when the adapter replays it after a restart, then no new row is written.
- Given a broker restates a fee, when re-ingested, then a superseding row appears and D14 shows the correction chain.
- Given Postgres is unavailable, when the writer fails, then the batch is not acked on NATS (re-delivered later), the WORM buffer path takes over within its bounds (default 1 GB / 24 h, 16 §3.3) and an alert fires (02 §9.3).

### Stress / failure injection

- Replay 50k events with 10% duplicates and 1% restatements; zero duplicate rows; throughput logged for P3-T052.

## Acceptance criteria

- [ ] Model + writer merged with ≥ 95% branch coverage on `writer.py`
- [ ] Idempotency and correction property tests pass
- [ ] `journal.event.new` published only after commit
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Clock: `ts_utc` comes from the source; `ingested_at` from `clock_timestamp()` (chrony-synced). Source timestamps in the future by > 5 min → flagged `clock_suspect`.
- Partial batch failure → whole batch rolls back; cursor not advanced.
- Unknown event type from an adapter → never guessed; the record goes to a quarantine table `journal.ingest_quarantine` (append-only) and alerted.

## Cardinal rules (do NOT)

- Do NOT write journal rows outside the writer; do NOT let adapters open their own DB sessions.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/09-journal-and-tax.md`: list the final `event_type` enum and the correction rule.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.20 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T008-journal-event-model-writer`
- PR title: `P3-T008: Journal event model, normaliser and idempotent append-only writer`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T008` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (manual events only via `journal.manual_event.add` C2 (P3-B006); valuation hierarchy 16 §4.1; locked-FY holding; Postgres-down buffer 16 §3.3; explicit P0 depends_on; tools/services filled)
