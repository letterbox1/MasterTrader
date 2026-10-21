---
id: P5-T009
kind: task
title: Phase 5 schemas and Alembic migrations (curation, M4, wallets)
phase: 5
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R5.05, R5.18, R5.20, R5.11]
roadmap_todos: [T5.22, T5.25, T5.29, T5.30]
modules: [M4, M19, M22]
dashboards: []
branch: p5/P5-T009-p5-schemas-migrations
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/02-v1-architecture.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T009 · Phase 5 schemas and Alembic migrations (curation, M4, wallets)

## Goal / expected outcome

All non-WORM Phase 5 tables exist via Alembic in `mt_store` with provenance columns, `event_time`/`ingest_time`, UUIDv7 ids and Decimal money, so every other P5 task builds on a fixed data model.

## Context & references

- Roadmap: [R5.05, R5.11, R5.18, R5.20](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDos T5.22, T5.25, T5.29, T5.30
- Data model: [08 data model](../../../docs/08-airdrops-and-token-launches.md#data-model-postgres) · [03 §4](../../../docs/03-build-spec.md#4-data-model-overview) · [02 §5.2 conventions](../../../docs/02-v1-architecture.md#52-key-conventions)
- Wallet registry: [13 §3](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view) (`ops.wallets`); P3 registry (P3 R3.04/T3.22) — see gap P5-B015
- Provenance: [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms)
- WORM tables are split out to P5-T010

## Requirements

- Schema `curation`: `airdrop_opportunity`, `token_risk_report`, `opportunity_score`, `decision`, `user_task`, `discord_curation`, `community_curation`, `blocklist_domain`, `blocklist_address`, `blacklist_project`, `campaign_record`, `project_dossier`, `wallet_cluster` (+ `wallet_cluster_member` edge table), `source_observation` (per-source corroboration rows).
- Schema `ops`: extend the P3 registry into `ops.wallets` (address, chain, provider_label, role ∈ vault/hl_master/warm/hot/identity/burner/governance/legacy/exchange, tax_tag ∈ investment/trading, custody_tier, proof_method, proof_status, watch_only bool); `ops.wallet_balance_snapshot` (hypertable), `ops.wallet_transfer`, `ops.wallet_approval`, `ops.nonce_account`, `ops.costgate_quote`, `ops.gas_budget_usage`, `ops.sweep_run`, `ops.recon_wallet_result`.
- Every ingest row carries `source`, `licence`, `train_ok`, `model_input_ok`, `display_ok`, `retention_days`, `commercial_ok`; Telegram-derived rows default `model_input_ok=false`, `train_ok=false`; CoinGecko rows `retention_days=1`.
- Natural keys: opportunity unique on `(chain, contract)` else `slug`; task idempotency key; blocklist unique on normalised domain/address.
- Indexes for D12/D13 queries (stage, deadline, viability, risk) and for D18 (wallet, chain, time); migration runs < 30 s on an empty DB and is reversible (down migration) for non-WORM tables.

## ToDo

- [ ] Write Alembic revisions in `packages/mt_store/migrations/` for the `curation` tables listed.
- [ ] Extend/rename the P3 registry to `ops.wallets` (or a view with that name if P3 used another name) and add the new columns with safe defaults.
- [ ] Add `ops.*` wallet-indexer, cost-gate and sweep tables; make `ops.wallet_balance_snapshot` a Timescale hypertable.
- [ ] Add SQLAlchemy/msgspec models in `packages/mt_store/models/curation.py` and `ops_wallets.py`; Decimal for all amounts.
- [ ] Add retention jobs entries for CoinGecko-sourced columns (≤ 1 day) to the existing retention runner.
- [ ] Write migration tests (up/down on an empty DB; up on a P3-populated fixture DB).
- [ ] Update the docs listed under Doc sync.

## Verification

### Tests
- Integration: Alembic upgrade/downgrade on a disposable Postgres 16 + Timescale container.
- Unit: model round-trip (Decimal precision kept; UUIDv7 ordering).
- Integration: upgrade on a fixture DB that contains P3 registry rows keeps every row and tag.

### Scenarios
- Given a P3 database with 5 registered exchange accounts, when the P5 migration runs, then `ops.wallets` lists the 5 with tags unchanged.
- Given a Telegram-derived `source_observation` insert without flags, when it is written, then defaults make it `model_input_ok=false`.

### Stress / failure injection
- Insert 1M `wallet_balance_snapshot` rows; D18 aggregate query < 200 ms with indexes (EXPLAIN attached to PR).

## Acceptance criteria

- [ ] All listed tables exist with provenance columns and conventions
- [ ] P3 registry data preserved
- [ ] Migration tests green in CI
- [ ] `pit` CI check still green

## Exceptions & edge cases

- If P3 named the registry differently, keep a compatibility view and record the decision in P5-B015.
- Postgres down during migration: Alembic transaction rolls back; rerun is idempotent.

## Cardinal rules (do NOT)

- Do NOT put mandates, exec logs, the signer ledger or income journal here (WORM, P5-T010).
- Do NOT use floats for any amount.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order, including disposal-rule sells, goes through M11.
- Do NOT UPDATE or DELETE WORM rows (`curation.mandate`, `curation.exec_log`, the signer ledger, `journal.*`, `audit.*`); corrections are new rows with `supersedes_id` (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: data model list gains `source_observation`, `wallet_cluster_member` and schema prefixes.
- `docs/02-v1-architecture.md` §5.3: add the new core entities.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.22, T5.25, T5.29, T5.30 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T009-p5-schemas-migrations`
- PR title: `P5-T009: Phase 5 schemas and Alembic migrations (curation, M4, wallets)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T009` run

## Progress log

- 2026-10-21 00:00 · planner · created
