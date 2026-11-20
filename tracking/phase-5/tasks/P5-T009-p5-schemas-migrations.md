---
id: P5-T009
kind: task
title: Phase 5 schemas and Supabase SQL migrations (curation, M4, wallets)
phase: 5
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T024, P0-T025, P3-T012, P3-T038]
requirements: [R5.05, R5.18, R5.20, R5.11, R5.25]
roadmap_todos: [T5.22, T5.25, T5.29, T5.30]
modules: [M4, M19, M22]
dashboards: []
tools: [supabase, docker, cargo, git]
mcp: []
env: []
services: [supabase-postgres]
branch: p5/P5-T009-p5-schemas-migrations
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/02-v1-architecture.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P5-T009 · Phase 5 schemas and Supabase SQL migrations (curation, M4, wallets)

## Goal / expected outcome

All non-WORM Phase 5 tables exist via SQL migrations in `supabase/migrations/` ([18 §3](../../../docs/18-platform-and-deployment.md#3-repository-layout)) with provenance columns, `event_time`/`ingest_time`, UUIDv7 ids and Decimal money, so every other P5 task builds on a fixed data model.

## Context & references

- Roadmap: [R5.05, R5.11, R5.18, R5.20](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDos T5.22, T5.25, T5.29, T5.30
- Data model: [08 data model](../../../docs/08-airdrops-and-token-launches.md#data-model-postgres) · [03 §4](../../../docs/03-build-spec.md#4-data-model-overview) · [02 §5.2 conventions](../../../docs/02-v1-architecture.md#52-key-conventions)
- Wallet registry: [13 §3](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view): one registry, `ops.wallets`, created in P3 (P3-T012) and extended additively here; there is no `treasury.wallet` (decision P5-B015, [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer))
- Task table: `curation.task`, created minimally in P3 (P3-T038, `TAX_QUESTION`) and extended additively here ([03 M19](../../../docs/03-build-spec.md#m19-user-task-queue--community-curation--mt_curation)); community entries in `curation.community` ([08 data model](../../../docs/08-airdrops-and-token-launches.md#data-model-postgres))
- Provenance: [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms)
- WORM tables are split out to P5-T010

## Requirements

- Schema `curation`: `airdrop_opportunity`, `token_risk_report`, `opportunity_score`, `decision`, `community` (Discord, Telegram, X and Galxe curation entries), `blocklist_domain`, `blocklist_address`, `blacklist_project`, `campaign_record`, `project_dossier`, `wallet_cluster` (+ `wallet_cluster_member` edge table), `source_observation` (per-source corroboration rows).
- `curation.task` (from P3): additive columns only: `type` checked against the canonical 03 M19 list (JOIN_DISCORD, FOLLOW_ANNOUNCEMENTS, JOIN_TELEGRAM, FOLLOW_X, QUEST, ONCHAIN_ACTION_MANUAL, CLAIM_MANUAL, ICO_REVIEW, REVOKE_APPROVAL, TAX_QUESTION, GENUINE_USE, PRO_ADVICE, VENUE_CHECK, APPROVE_ORDER, REG_CHANGE), numbered steps, links with `verified_via`, deadline, estimated minutes, scores, opportunity/community refs, ranking weights, idempotency key, expiry; existing P3 rows keep their ids and content.
- Schema `ops`: extend the P3 `ops.wallets` table additively (new columns: address, chain, provider_label, role ∈ vault/hl_master/warm/hot/identity/burner/governance/legacy/exchange, tax_tag ∈ investment/trading, custody_tier, proof_method, proof_status, watch_only bool); `ops.wallet_balance_snapshot` (native monthly range partitions, [18 §4.3](../../../docs/18-platform-and-deployment.md#43-bars-without-timescaledb)), `ops.wallet_transfer`, `ops.wallet_approval`, `ops.nonce_account`, `ops.costgate_quote`, `ops.gas_budget_usage`, `ops.sweep_run`, `ops.recon_wallet_result`.
- Every ingest row carries `source`, `licence`, `train_ok`, `model_input_ok`, `display_ok`, `retention_days`, `commercial_ok`; Telegram-derived rows default `model_input_ok=false`, `train_ok=false`; CoinGecko rows `retention_days=1`.
- Natural keys: opportunity unique on `(chain, contract)` else `slug`; task idempotency key; blocklist unique on normalised domain/address.
- Indexes for D12/D13 queries (stage, deadline, viability, risk) and for D18 (wallet, chain, time); migration runs < 30 s on an empty DB (`supabase db reset`); RLS on with no policies for `anon`/`authenticated` ([18 §4.5](../../../docs/18-platform-and-deployment.md#45-access-rules)); changes after release are new forward migrations (Supabase has no down migrations).

## ToDo

- [ ] Write SQL migrations in `supabase/migrations/` ([18 §3](../../../docs/18-platform-and-deployment.md#3-repository-layout)) for the new `curation` tables listed.
- [ ] Extend the P3 `curation.task` table additively (new columns and the canonical type check constraint).
- [ ] Extend the P3 `ops.wallets` table additively (new nullable columns or safe defaults; no rename, no drop).
- [ ] Add `ops.*` wallet-indexer, cost-gate and sweep tables; partition `ops.wallet_balance_snapshot` by month (pg_partman where available, else the `mt-store` partition job; no TimescaleDB).
- [ ] Add Rust row types (sqlx, `rust_decimal`) in `crates/mt-store` for the `ops.*` wallet tables used by the Rust crates, and for the `curation` tables used by the Rust `mt-airdrop`/`mt-curation` crates (no Python models: both are Rust, 18 §2.1); `rust_decimal` for all amounts.
- [ ] Add retention jobs entries for CoinGecko-sourced columns (≤ 1 day) to the existing retention runner.
- [ ] Write pgTAP tests (`supabase test db`): `supabase db reset` on an empty DB; migrate up on a P3-populated fixture DB.
- [ ] Update the docs listed under Doc sync.

## Verification

### Tests
- Integration: `supabase db reset` + `supabase test db` (pgTAP) on the local Supabase CLI stack.
- Unit: model round-trip (Decimal precision kept; UUIDv7 ordering).
- Integration: upgrade on a fixture DB that contains P3 registry rows keeps every row and tag.

### Scenarios
- Given a P3 database with 5 registered exchange accounts, when the P5 migration runs, then `ops.wallets` lists the 5 with tags unchanged.
- Given P3 `TAX_QUESTION` rows in `curation.task`, when the migration runs, then they keep ids and content and pass the new type constraint.
- Given a Telegram-derived `source_observation` insert without flags, when it is written, then defaults make it `model_input_ok=false`.

### Stress / failure injection
- Insert 1M `wallet_balance_snapshot` rows; D18 aggregate query < 200 ms with indexes (EXPLAIN attached to PR).

## Acceptance criteria

- [ ] All listed tables exist with provenance columns and conventions
- [ ] P3 registry data preserved
- [ ] Migration tests green in CI
- [ ] `pit` CI check still green

## Exceptions & edge cases

- The registry is already `ops.wallets` in P3 (17 §B); if a P3 column conflicts with a P5 need, add a new column instead of altering the old one and note it in the PR.
- Postgres down during migration: the migration transaction rolls back; `supabase migration up` rerun is idempotent.

## Cardinal rules (do NOT)

- Do NOT put mandates, exec logs, the signer ledger or income journal here (WORM, P5-T010).
- Do NOT create a second task table (`user_task`), separate community tables (`discord_curation` / `community_curation`) or a second wallet registry; extend `curation.task` and `ops.wallets`.
- Do NOT use floats for any amount.
- Do NOT bypass `mt-api`, the risk manager (M11, `mt-risk`) or `pit(as_of)` (`mt-store`); every order goes through M11, and until the P7 live gates pass, disposal sales are manual USER tasks (never automated).
- Do NOT UPDATE or DELETE WORM rows (`curation.mandate`, `curation.exec_log`, the signer ledger, `journal.*`, `audit.*`); corrections are new rows with `supersedes_id` (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: data model list gains `source_observation` and `wallet_cluster_member`.
- `docs/02-v1-architecture.md` §5.3: add the new core entities.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.22, T5.25, T5.29, T5.30 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T009-p5-schemas-migrations`
- PR title: `P5-T009: Phase 5 schemas and Supabase SQL migrations (curation, M4, wallets)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T009` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (extend P3 `curation.task` and `ops.wallets` additively; `curation.community` replaces discord/community_curation; canonical 03 M19 task types; P0/P3 deps added)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (Alembic → `supabase/migrations/` + pgTAP; hypertable → monthly partitions; Rust row types; services postgres → supabase-postgres; tools +cargo +git +supabase)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (curation row types in Rust for `mt-airdrop`/`mt-curation`, no Python models; tools −uv)
