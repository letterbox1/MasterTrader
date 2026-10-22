---
id: P0-T024
kind: task
title: Create the Postgres schemas, DB roles and Alembic baseline
phase: 0
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T016, P0-T017, P0-T020]
requirements: [R0.03]
roadmap_todos: [T0.22]
modules: [mt_store]
dashboards: []
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [postgres]
branch: p0/P0-T024-mt-store-schemas-roles-alembic
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T024 · Create the Postgres schemas, DB roles and Alembic baseline

## Goal / expected outcome

Alembic (in `migrations/`, helpers in `mt_store.migrate`) creates all 13 canonical schemas `market`, `text`, `features`, `strategy`, `risk`, `audit`, `journal`, `curation`, `ops`, `rag`, `models`, `treasury`, `hindsight` (later phases only add tables), the role model (owner/migrator/app/read-only roles, `worm_owner` placeholder) and the shared conventions (UUIDv7, `timestamptz` UTC, `event_time` + `ingest_time`). A migration test proves upgrade → downgrade → upgrade on a clean DB.

## Context & references

- [Roadmap P0 R0.03](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.22](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [03 §4 data model](../../../docs/03-build-spec.md#4-data-model-overview)
- [02 §5.1 stores](../../../docs/02-v1-architecture.md#51-stores)
- [02 §5.2 key conventions](../../../docs/02-v1-architecture.md#52-key-conventions)
- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers)
- Schema list decided in [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (P0-B005, closed): the 13 schemas of 03 §4 / 02 §5.1 are all created in P0; later phases add tables only.
- Depends on: P0-T016, P0-T017, P0-T020

## Requirements

- Roles: `mt_owner` (NOLOGIN, owns non-WORM schemas), `mt_migrator` (LOGIN, member of `mt_owner`, used by Alembic for non-WORM changes), `worm_owner` (LOGIN, password set offline via P0-T013; owns WORM tables), app roles per service (`mt_api_rw`, `mt_obs_rw`, `mt_flows_rw`, `mt_research_ro`), `mt_monitor_ro` (exporters).
- Default privileges: app roles get `SELECT, INSERT, UPDATE, DELETE` only on **non-WORM** tables of the schemas they need; `mt_research_ro` gets **no** direct `SELECT` on fact tables (only on `pit` functions/views from P0-T027).
- Conventions enforced by a migration lint (`mt_store.lint`): every fact table has `event_time timestamptz NOT NULL`, `ingest_time timestamptz NOT NULL DEFAULT clock_timestamp()`; PKs are `uuid` (UUIDv7 generated app-side; a `uuid_generate_v7()` SQL function as fallback); money columns are `numeric`, never `real/double`.
- Alembic env reads the DSN from tmpfs secrets; `alembic upgrade head` is idempotent; every migration has a working `downgrade` (except WORM tables, whose downgrade refuses unless `MT_ALLOW_WORM_DROP=test` in CI).
- `ops` starter tables: `ops.user_pref`, `ops.setting`, `ops.session`, `ops.idempotency_key`, `ops.pending_confirmation` (used by P0-T033, P0-T034, P0-T035); `ops.backup_run`, `ops.restore_test` (used by P0-T041).

## ToDo

- [ ] Initialise Alembic in `migrations/` with `mt_store.migrate` helpers (`create_fact_table`, `grant_app`).
- [ ] Migration 0001: schemas + roles + default privileges + `uuid_generate_v7()`.
- [ ] Migration 0002: `ops` starter tables.
- [ ] Implement `mt_store.lint` (inspects `information_schema`) and run it in the migration test.
- [ ] Implement `mt_store.db` (async SQLAlchemy 2 engine/session factory per role, statement timeout 5 s default).
- [ ] Fill the CI `migrations` job: upgrade → lint → downgrade → upgrade on a fresh container.

## Verification

### Tests
- Migration test (CI): upgrade/downgrade/upgrade clean; `mt_store.lint` passes.
- Privilege tests: `mt_api_rw` cannot `CREATE` in any schema; `mt_research_ro` cannot `SELECT` from `market.*` directly.
- Unit: `uuid_generate_v7()` output is time-ordered.

### Scenarios
- Given a developer adds a fact table without `ingest_time`, when CI runs the lint, then it fails with the table name.
- Given a migration is applied twice, then the second run is a no-op.

### Stress / failure injection
- n/a: DDL; performance is covered by later table-specific tests.

## Acceptance criteria

- [ ] All 13 schemas + roles exist after `alembic upgrade head`
- [ ] Migration test green in CI
- [ ] Lint enforces event_time/ingest_time/numeric/uuid conventions
- [ ] Privilege tests pass
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- TimescaleDB hypertables arrive in P1 (bars); P0 only ensures the extension is present.
- `worm_owner` has no password until the ceremony; CI sets a throwaway password in its scratch DB only.

## Cardinal rules (do NOT)

- Do NOT grant `UPDATE/DELETE/TRUNCATE` on any WORM table to any app role.
- Do NOT give research roles direct reads on fact tables (pit only).
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/03-build-spec.md` §4: list the role model; `docs/02-v1-architecture.md` §5.1: note which schemas exist as of P0.
- `docs/roadmap/phase-0-foundations.md`: tick T0.22 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T024-mt-store-schemas-roles-alembic`
- PR title: `P0-T024: Create the Postgres schemas, DB roles and Alembic baseline`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T024` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (all 13 canonical schemas in P0 (17 §B P0-B005); run fields added)
