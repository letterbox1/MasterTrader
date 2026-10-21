---
id: P3-T005
kind: task
title: Journal schema migrations registered as WORM tables
phase: 3
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R3.02, R3.01]
roadmap_todos: [T3.20]
modules: [M18]
dashboards: []
branch: p3/P3-T005-journal-schema-worm
pr: ""
doc_sync: [docs/09-journal-and-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-T005 · Journal schema migrations registered as WORM tables

## Goal / expected outcome

Alembic migrations create every `journal.*` table (event, raw payload, lot, lot_match, fx_rate, account registry link, transfer_link, residency_period, regime_setting, tax_report, lot_snapshot, note, tag) and register each with the P0 WORM layer (owner `worm_owner`, INSERT/SELECT grants, blocking triggers, per-row hash chain, daily seal), so nothing downstream can ever edit a journal row.

## Context & references

- Roadmap: [R3.02, R3.01, T3.20](../../../docs/roadmap/phase-3-journal-and-tax.md)
- WORM design: [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) · [SPEC NN7](../../../SPEC.md#non-negotiable-requirements) · [03 §4](../../../docs/03-build-spec.md#4-data-model-overview)
- Event fields: [09 journal event](../../../docs/09-journal-and-tax.md#journal-event-captured-per-transaction) · entities `journal_event`, `lot`, `lot_match`, `fx_rate`, `residency_period`, `tax_report` in [02 §5.3](../../../docs/02-v1-architecture.md#53-core-entities-abbreviated-full-ddl-in-migrations)
- Cross-phase prerequisites (text only): P0 T0.22 (`journal` schema + Alembic), P0 T0.23 (WORM layer: `worm_owner`, triggers, hash chain, seal, `audit.verify`)
- Next: P3-T006 (roles/keys), P3-T008 (writer)

## Requirements

- Tables (all `numeric` for money/qty/rates, `timestamptz` UTC, UUIDv7 PKs): `journal.event`, `journal.raw_payload` (encrypted blob + `raw_payload_hash`), `journal.lot`, `journal.lot_match`, `journal.fx_rate`, `journal.transfer_link`, `journal.residency_period`, `journal.regime_setting`, `journal.lot_snapshot`, `journal.tax_report`, `journal.note`, `journal.tag`, `journal.ingest_cursor` (adapter cursors; append-only, latest row wins).
- `journal.event` columns per 09: identity (`event_id`, `source`, `source_ref`, `ingested_at`, `supersedes_event_id`, `raw_payload_hash`), time (`ts_utc` + `ts_ns`, venue tz, local time, `taxpayer_local_date`), venue/account (`account_id`, wallet address, chain, counterparty, custodial flag, counterparty residency), instrument (id, ISIN/ticker, asset class, multiplier, expiry, settlement ccy), economics (side, qty, price, gross, fee columns by type), three-currency amounts (`amt_native`, `ccy_native`, `amt_usd`, `amt_aud`, `fx_rate_usd`, `fx_rate_aud`, `fx_source`, `fx_ts`), `event_type` enum (all 09 types), tax context (`residency_code`, `regime`, `wash_sale_flag`, `strategy_id`, `bot_id`, `mode` paper/live), provenance columns (`source`, `licence`, `model_input_ok=false`, `train_ok=false`, `retention_days` ≥ 2557).
- Unique `(source, source_ref, supersedes_event_id IS NULL)` partial index for idempotency; `current_event` view = latest row per correction chain.
- Every table: `chain_id`, `seq`, `prev_hash`, `row_hash` via the P0 trigger; partitions never dropped inside 7 years; no `ON DELETE CASCADE` into `journal.*`.
- Migration is reversible only in test DBs (downgrade guarded by env flag).

## ToDo

- [ ] Write Alembic revision `journal_0001_core` under `migrations/versions/` with the tables, enums and indexes above
- [ ] Register each table with the WORM helper from P0 (`mt_store.worm.register(table, chain_key=...)`) so triggers + hash chain apply
- [ ] Create `journal.current_event`, `journal.current_lot` views (latest per supersede chain)
- [ ] Add SQLAlchemy/msgspec models in `packages/mt_store/journal/` and the `JournalEvent` type extension in `packages/mt_core/schemas/journal.py`
- [ ] Write migration tests (upgrade on empty DB, schema snapshot test)
- [ ] Document the table list in `docs/09-journal-and-tax.md` (new "Storage" subsection)

## Verification

### Tests

- Unit: model ↔ DDL parity test (every msgspec field has a column of the right type; no `float`/`double precision` anywhere in `journal.*`).
- Integration: migrate a scratch Postgres 16 + Timescale; `INSERT` as `journal_app` works, `UPDATE`/`DELETE`/`TRUNCATE` raise (full suite in P3-T047).
- Integration: hash chain populated (`row_hash` non-null, `seq` contiguous per chain).

### Scenarios

- Given a fresh DB, when migrations run, then all journal tables exist with WORM triggers and the `audit.verify` run passes.
- Given an app role, when it tries `DELETE FROM journal.event`, then it fails with the WORM exception and nothing changes.

### Stress / failure injection

- Insert 100k synthetic events in a test DB; hash-chain insert throughput recorded as a baseline for P3-T052 (target: no measurable delay on the fill path; fills never wait on seals).

## Acceptance criteria

- [ ] All tables created by one Alembic head; schema snapshot committed
- [ ] No float columns in `journal.*` (CI grep test)
- [ ] WORM triggers + hash chain active on every `journal.*` table
- [ ] CI green (lint, types, tests, `pit` check)
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Correction chains: a superseding row must reference an existing `event_id`; FK enforced without cascade.
- Timescale: `journal.event` is a regular table (not a hypertable) so partitions are never auto-dropped by retention policies.
- Downgrade in production is refused.

## Cardinal rules (do NOT)

- Do NOT add `ON DELETE CASCADE` or any retention policy that could drop journal partitions inside 7 years.
- Do NOT store raw statements unencrypted (P3-T007 provides the helper).
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/09-journal-and-tax.md`: add a Storage subsection listing the `journal.*` tables and the current-row views.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.20 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T005-journal-schema-worm`
- PR title: `P3-T005: Journal schema migrations registered as WORM tables`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T005` run

## Progress log

- 2026-10-21 00:00 · planner · created
