---
id: P0-T024
kind: task
title: Create the schemas, DB roles and RLS deny-all as Supabase SQL migrations with pgTAP
phase: 0
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T016, P0-T017, P0-T070]
requirements: [R0.03]
roadmap_todos: [T0.22]
modules: [mt-store, supabase]
dashboards: []
tools: [git, cargo, supabase, psql, just]
mcp: []
env: []
services: [supabase-postgres]
branch: p0/P0-T024-mt-store-schemas-roles-alembic
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T024 · Create the schemas, DB roles and RLS deny-all as Supabase SQL migrations with pgTAP

## Goal / expected outcome

Plain SQL migrations in `supabase/migrations/` create all 13 canonical schemas `market`, `text`, `features`, `strategy`, `risk`, `audit`, `journal`, `curation`, `ops`, `rag`, `models`, `treasury`, `hindsight` (later phases only add tables with new migration files), the role model (owner/migrator/app/read-only roles, `worm_owner` placeholder), **row-level security on every table with no policies for `anon`/`authenticated`**, and the shared conventions (UUIDv7, `timestamptz` UTC, `event_time` + `ingest_time`). pgTAP tests (`supabase test db`) prove the invariants, and `supabase db reset` rebuilds the database from scratch on every run. The same files deploy to the self-hosted stack (`supabase migration up`) and, at the shift, to Supabase cloud (`supabase db push`).

## Context & references

- [Roadmap P0 R0.03](../../../docs/roadmap/phase-0-foundations.md#3-requirements) · [T0.22](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [18 §3 migrations](../../../docs/18-platform-and-deployment.md#3-repository-layout) · [18 §4.4 point-in-time and WORM](../../../docs/18-platform-and-deployment.md#44-point-in-time-and-worm) · [18 §4.5 access rules](../../../docs/18-platform-and-deployment.md#45-access-rules)
- [03 §4 data model](../../../docs/03-build-spec.md#4-data-model-overview)
- [02 §5.1 stores](../../../docs/02-v1-architecture.md#51-stores) · [02 §5.2 key conventions](../../../docs/02-v1-architecture.md#52-key-conventions)
- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers)
- Schema list decided in [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (P0-B005, closed): the 13 schemas of 03 §4 / 02 §5.1 are all created in P0; later phases add tables only.
- Depends on: P0-T016, P0-T017, P0-T070 (Supabase stack, extensions)
- Unblocks: P0-T025, P0-T027, P0-T029, P0-T072, P0-T032

## Requirements

- Roles: `mt_owner` (NOLOGIN, owns non-WORM schemas), `mt_migrator` (member of `mt_owner`, runs non-WORM migrations), `worm_owner` (LOGIN, password set offline via P0-T013; throwaway in dev/CI/paper; owns WORM tables), app roles per service (`mt_api_rw`, `mt_obs_rw`, `mt_flows_rw`, `mt_research_ro`), `mt_monitor_ro` (exporters).
- Default privileges: app roles get `SELECT, INSERT, UPDATE, DELETE` only on **non-WORM** tables of the schemas they need; `mt_research_ro` gets **no** direct `SELECT` on fact tables (only on the `pit` functions/views from P0-T027).
- **Supabase roles** (`anon`, `authenticated`, `service_role`): no privileges on any MasterTrader schema; **RLS enabled on every table** with no policies for `anon`/`authenticated` (deny all), enforced by an event trigger or a migration helper so new tables can't miss it ([18 §4.5](../../../docs/18-platform-and-deployment.md#45-access-rules)).
- Conventions enforced by pgTAP tests over `information_schema`/`pg_catalog`: every fact table has `event_time timestamptz NOT NULL`, `ingest_time timestamptz NOT NULL DEFAULT clock_timestamp()`; PKs are `uuid` (UUIDv7 generated app-side; a `uuid_generate_v7()` SQL function as fallback); money columns are `numeric`, never `real/double`; RLS on.
- Migrations are **forward-only** (Supabase has no down migrations): a fix is a new migration; WORM tables are never dropped by a migration. `supabase db reset` from zero must always succeed (CI).
- SQL helpers (in migrations): `mt_create_fact_table(...)`, `mt_grant_app(...)`, `mt_enable_rls(...)`.
- `mt-store` crate: `sqlx` connection pools per role (statement timeout 5 s default, from settings), compile-time-checked queries (`sqlx prepare` offline data committed).
- `ops` starter tables: `ops.user_pref`, `ops.setting`, `ops.command_session` (short-lived Telegram/break-glass command sessions at `aal2`, [18 §4.6](../../../docs/18-platform-and-deployment.md#46-auth)), `ops.idempotency_key`, `ops.pending_confirmation` (used by P0-T033, P0-T034, P0-T035); `ops.backup_run`, `ops.restore_test` (used by P0-T041). Login sessions themselves live in Supabase Auth.

## ToDo

- [ ] Migration `<ts>_schemas_roles.sql`: schemas + roles + default privileges + `uuid_generate_v7()` + revokes for `anon`/`authenticated`/`service_role`.
- [ ] Migration `<ts>_helpers.sql`: `mt_create_fact_table`, `mt_grant_app`, `mt_enable_rls` and the RLS event trigger.
- [ ] Migration `<ts>_ops_starter.sql`: the `ops` starter tables.
- [ ] pgTAP tests in `supabase/tests/`: schemas, roles, privileges, RLS on every table, conventions.
- [ ] `mt-store` DB pools per role with sqlx offline data.
- [ ] Fill the CI `db` job: `supabase start` → `supabase db reset` → `supabase test db`.

## Verification

### Tests
- `supabase db reset && supabase test db`: all 13 schemas and roles exist; RLS on for every table; `anon`/`authenticated` have no privilege on any MasterTrader schema; conventions hold.
- Privilege tests (pgTAP): `mt_api_rw` cannot `CREATE` in any schema; `mt_research_ro` cannot `SELECT` from `market.*` directly.
- `cargo test -p mt-store db`: pools connect per role; `uuid_generate_v7()` output is time-ordered.

### Scenarios
- Given a developer adds a fact table without `ingest_time`, when CI runs `supabase test db`, then it fails with the table name.
- Given a developer adds a table without RLS, then the event trigger enables it and the pgTAP check passes; disabling RLS by hand fails the test.
- Given the anon key, when a client queries any MasterTrader table through the Data API, then it is refused.

### Stress / failure injection
- n/a: DDL; performance is covered by later table-specific tests.

## Acceptance criteria

- [ ] All 13 schemas + roles exist after `supabase db reset`
- [ ] RLS deny-all on every table; Supabase roles have no access (pgTAP)
- [ ] Conventions (event_time/ingest_time/numeric/uuid) enforced by pgTAP
- [ ] Privilege tests pass; `supabase test db` green in CI
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, `supabase test db`, gitleaks, `pit` check)

## Exceptions & edge cases

- Bars: the partitioned `market.bar_*` parents and the partition job are P0-T072 (no TimescaleDB).
- `worm_owner` has no real password until the ceremony (P0-T013, before live money); dev/CI/paper use a throwaway password.
- Supabase's own schemas (`auth`, `storage`, `extensions`, …) are not touched except by the Supabase stack.

## Cardinal rules (do NOT)

- Do NOT grant `UPDATE/DELETE/TRUNCATE` on any WORM table to any app role.
- Do NOT give research roles direct reads on fact tables (pit only).
- Do NOT add RLS policies for `anon` or `authenticated`, and do NOT expose MasterTrader schemas to the Data API.
- Do NOT edit an applied migration; add a new one.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/03-build-spec.md` §4: list the role model and the RLS rule; `docs/02-v1-architecture.md` §5.1: note which schemas exist as of P0.
- `docs/roadmap/phase-0-foundations.md`: tick T0.22 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T024-mt-store-schemas-roles-alembic`
- PR title: `P0-T024: Create the schemas, DB roles and RLS deny-all as Supabase migrations`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T024` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (all 13 canonical schemas in P0 (17 §B P0-B005); run fields added)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (Alembic → forward-only SQL in `supabase/migrations/` with pgTAP (`supabase test db`); RLS deny-all + no access for Supabase roles; sqlx pools in `mt-store`; `ops.session` → `ops.command_session` (logins live in Supabase Auth); depends on P0-T070 instead of P0-T020; bars moved to P0-T072)
