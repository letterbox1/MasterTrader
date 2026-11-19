---
id: P0-T029
kind: task
title: Implement WORM privileges and blocking triggers
phase: 0
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T024]
requirements: [R0.07]
roadmap_todos: [T0.23]
modules: [M17, mt-store, supabase]
dashboards: []
tools: [git, cargo, supabase, psql]
mcp: []
env: []
services: [supabase-postgres]
branch: p0/P0-T029-worm-privileges-blocking-triggers
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T029 · Implement WORM privileges and blocking triggers

## Goal / expected outcome

A reusable SQL helper `create_worm_table()` (defined in `supabase/migrations/`) makes a table WORM: owned by `worm_owner`, app roles get `INSERT, SELECT` only, `UPDATE/DELETE/TRUNCATE` revoked, `BEFORE UPDATE OR DELETE` and `BEFORE TRUNCATE` triggers that raise, no `ON DELETE CASCADE` into it, and partitions protected from drops inside the 7-year retention.

## Context & references

- [Roadmap P0 R0.07](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.23](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [15 §2.1 scope](../../../docs/15-bots-hitl-and-worm-audit.md#21-scope)
- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers) (Privileges, Triggers)
- [07 §8 backups & audit](../../../docs/07-security-notes.md#8-data-protection-backups--audit)
- [03 §4 data model](../../../docs/03-build-spec.md#4-data-model-overview)
- [SPEC non-negotiables](../../../SPEC.md#non-negotiable-requirements) (NN7)
- Depends on: P0-T024. Build first, keys last: CI and dev set a throwaway `worm_owner` password in scratch DBs; the production ceremony with the offline credential is P0-T013, which runs these migrations later.

## Requirements

- `create_worm_table(schema, name, columns, chain_key=..., partition_by=None)` emits: `CREATE TABLE` owned by `worm_owner`; `REVOKE ALL ... FROM PUBLIC`; `GRANT INSERT, SELECT` to listed app roles; trigger `worm_block_mutation()` `BEFORE UPDATE OR DELETE FOR EACH ROW` and `worm_block_truncate()` `BEFORE TRUNCATE FOR EACH STATEMENT`, both `RAISE EXCEPTION 'WORM table %: % is forbidden'` with SQLSTATE `MT001`.
- Event trigger (`ddl_command_start`) `worm_guard` rejects `DROP TABLE`, `ALTER TABLE ... DISABLE TRIGGER`, `DETACH PARTITION` and `DROP` of partitions on WORM tables unless the session sets `mt.worm_maintenance = 'ceremony'` **and** the current user is `worm_owner` **and** the partition's upper bound is older than 7 years.
- Catalog table `audit.worm_registry` (itself WORM) lists every WORM table, chain key and retention (≥ 2557 days).
- FK check (pgTAP): `supabase test db` fails if any FK referencing a WORM table has `ON DELETE CASCADE`/`SET NULL`.
- Migrations touching WORM tables are SQL files tagged `-- mt:worm` on their first line. `supabase db reset` applies everything in dev/CI/paper with the throwaway `worm_owner`; against the always-on stack (and, at the shift, the cloud project) the `just db-migrate` recipe applies pending files in order, switching to the `worm_owner` connection for `mt:worm` files and refusing if it isn't connected as `worm_owner` (the ceremony credential from P0-T013 before live money); non-WORM files run as `mt_migrator` (U: confirm `supabase migration up --db-url` can be driven file by file; otherwise the recipe applies those files with `psql` and records them in the migration history table).
- 15 §2.1 scope list is recorded for later phases (`journal.*`, `risk.approval`, `risk.change`, `strategy.bot_version`, `curation.mandate`/`exec_log`, signer ledger) — they must use this helper.

## ToDo

- [ ] Implement the helper, the two trigger functions, and the `worm_guard` event trigger.
- [ ] Create `audit.worm_registry` via the helper (bootstrapping order documented).
- [ ] Add pgTAP checks (FK cascade rule; every table in `audit.*`/`journal.*` must be in `worm_registry`; RLS on).
- [ ] Add the `-- mt:worm` guard to the `just db-migrate` recipe (and a CI check that every WORM DDL file carries the tag).
- [ ] Unit/integration tests (below); the full adversarial suite is P0-T055.

## Verification

### Tests
- Integration: as `mt_api_rw`, `UPDATE`, `DELETE`, `TRUNCATE` on a WORM test table each fail (privilege error); as `worm_owner`, `UPDATE` fails with `MT001` (trigger).
- Integration: `ALTER TABLE ... DISABLE TRIGGER ALL` as `worm_owner` without the ceremony GUC fails.
- Lint: fixture FK with `ON DELETE CASCADE` to a WORM table fails.

### Scenarios
- Given a wrong migration tries `DELETE FROM audit.command`, then it fails at the trigger even though it runs as the owner.
- Given someone runs a WORM migration as `mt_migrator`, then the `db-migrate` guard aborts before any DDL.

### Stress / failure injection
- Trigger overhead: insert 100k rows into a WORM table with only the blocking triggers; overhead vs a plain table < 5 % (logged).

## Acceptance criteria

- [ ] Helper + triggers + event trigger implemented
- [ ] App roles: U/D/T fail; owner: U/D fail via trigger
- [ ] Lint rules active in CI
- [ ] `audit.worm_registry` lists the P0 WORM tables
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, `supabase test db`, gitleaks, `pit` check)

## Exceptions & edge cases

- A superuser (`supabase_admin` on the self-hosted stack; the platform operator on Supabase cloud, [18 §4.4](../../../docs/18-platform-and-deployment.md#44-point-in-time-and-worm)) can still bypass triggers; that is the 'detected, not prevented' case of 15 §2.3 — hash chain + external seals catch it.
- Retention-expired partition drops are allowed only via the ceremony and are themselves logged in a WORM `audit.worm_maintenance` row.

## Cardinal rules (do NOT)

- Do NOT add an 'admin' escape hatch that UPDATEs WORM rows.
- Do NOT store the real (ceremony) worm_owner password anywhere on the workstation or runtime host; dev/CI/paper stacks use a generated throwaway that is never the ceremony credential and never in the runtime secrets file.
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md` §2.2: document the helper name, SQLSTATE `MT001` and the ceremony GUC.
- `docs/roadmap/phase-0-foundations.md`: tick T0.23 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T029-worm-privileges-blocking-triggers`
- PR title: `P0-T029: Implement WORM privileges and blocking triggers`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T029` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keyless: no longer waits on the worm_owner ceremony P0-T013; 15 §2.1 scope list; run fields added)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (helper and guards are SQL in `supabase/migrations/` + pgTAP; Alembic `worm=True` env guard → `-- mt:worm` tag enforced by `just db-migrate`; superuser caveat per 18 §4.4)
