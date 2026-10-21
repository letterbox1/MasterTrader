---
id: P2-T006
kind: task
title: Strategy registry, versions and strategy commands
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T004]
requirements: [R2.04, R2.06]
roadmap_todos: [T2.20]
modules: [M0]
dashboards: [D03]
branch: p2/P2-T006-strategy-registry-versions
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T006 · Strategy registry, versions and strategy commands

## Goal / expected outcome

Strategies and their immutable versions live in `strategy.registry` / `strategy.versions` / `strategy.runs`, exposed through `mt_api` queries and the `strategy.create|update_params|clone|archive` commands, so bots, the lab and the engine all reference a pinned version.

## Context & references

- Roadmap: [R2.04, R2.06](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.20
- Architecture: [02 §4 M0 tables](../../../docs/02-v1-architecture.md#4-logical-components) · [02 §7 API](../../../docs/02-v1-architecture.md#7-api-contract-mt_api) · [02 §7.2 command catalogue](../../../docs/02-v1-architecture.md#72-commands-rest-write)
- UI: [D03 registry + versions tab](../../../docs/ui/dashboards/D03-strategies.md)
- Cross-phase: Alembic migrations + `strategy` schema (P0 R0.03); `audit.command` (P0 R0.08).

## Requirements

- Tables (Alembic): `strategy.registry(id uuid7, name unique, template, created_at, archived_at)`, `strategy.versions(id, strategy_id, version int, manifest jsonb, manifest_hash, code_hash, git_sha, created_at, created_by)` (insert-only), `strategy.runs(id, version_id, kind backtest|paper|shadow|live, started_at, ended_at, metrics jsonb)`.
- A new version is created on any manifest or code change; versions are never mutated.
- Queries: `/strategies`, `/strategies/{id}` (+`?versions=1`), `/strategies/{id}/runs`, `/strategies/templates` (template catalogue with evidence + priority).
- Commands: `strategy.create` (C1), `strategy.update_params` (C1 paper / C2 live mode / C3 when a `risk_increasing` param increases, classified by P2-T019), `strategy.clone` (C1), `strategy.archive` (C1).
- Every command written to `audit.command`; problem+json errors.

## ToDo

- [ ] Migrations for the three tables + insert-only grants on `strategy.versions`
- [ ] `packages/mt_strategy/registry.py` service (create, new_version, get_pinned)
- [ ] `mt_api` routers for the queries and commands; OpenAPI updated
- [ ] Hash code by module file contents + git SHA
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: new version on param change; identical manifest → no new version (hash).
- Integration: `strategy.create` with invalid manifest → 422 problem+json; with valid → draft row + `audit.command` row.
- DB: UPDATE on `strategy.versions` by app role fails.

### Scenarios
- Given a strategy with 3 versions, when a bot pins v2, then later edits create v4 and the bot still runs v2.
- Given `strategy.update_params` raises position size on a live-mode strategy, when submitted, then it is routed to C3.

### Stress / failure injection
- n/a: CRUD; check `/strategies` p95 < 100 ms with 500 strategies × 20 versions.

## Acceptance criteria

- [ ] Tables, queries and commands live and documented in OpenAPI
- [ ] Versions immutable (grant + test)
- [ ] Audit rows for every command
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Archive of a strategy with running bots is refused until bots are stopped.
- Postgres down: commands fail fast with 503; the engine keeps running pinned versions from memory.

## Cardinal rules (do NOT)

- Do NOT mutate a version row; create a new one.
- Do NOT let a client choose its own confirmation level; the server classifies.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows with `supersedes_id` (15 §2).

## Doc sync on completion

- `docs/02-v1-architecture.md` §4/§7: confirm table names and endpoints as built.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.20 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T006-strategy-registry-versions`
- PR title: `P2-T006: Strategy registry, versions and strategy commands`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T006` run

## Progress log

- 2026-10-21 00:00 · planner · created
