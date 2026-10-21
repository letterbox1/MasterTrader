---
id: P0-T028
kind: task
title: Add the pit bypass test to CI
phase: 0
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T027, P0-T015]
requirements: [R0.04]
roadmap_todos: [T0.60]
modules: [mt_store]
dashboards: []
branch: p0/P0-T028-pit-bypass-ci-test
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T028 · Add the pit bypass test to CI

## Goal / expected outcome

CI fails the build if any research-side module reads raw tables instead of `mt_store.pit(as_of)`: a static import/SQL-string check plus a runtime DB-privilege test.

## Context & references

- [Roadmap P0 R0.04](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.60](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [SPEC non-negotiables](../../../SPEC.md#non-negotiable-requirements) (NN1)
- [03 §4 data model](../../../docs/03-build-spec.md#4-data-model-overview)
- [04 standing rules](../../../docs/04-plan-of-action.md#standing-rules) (pit test mandatory)
- Depends on: P0-T027, P0-T015

## Requirements

- Research-side packages: `mt_lab`, `mt_features`, `mt_strategy`, `mt_agents`, `mt_memory`, `mt_models`, `mt_anomaly`, plus `notebooks/` and `strategies/`.
- Static check (`tools/pitcheck.py`, AST-based): in those paths, fail on imports of `sqlalchemy`, `psycopg`, `asyncpg`, `duckdb` or `mt_store.db`; fail on string literals matching `\b(FROM|JOIN)\s+(market|text|features|journal|audit|curation|strategy|risk)\.`; fail on `revisions='latest'`. Allow-list file with justification + expiry only.
- import-linter contract: research packages may import `mt_store.pit` and `mt_store.catalog` only.
- Runtime check: an integration test logs in as `mt_research_ro` and asserts `SELECT` on each fact table raises `insufficient_privilege`.
- Wired as a required CI step (`make pitcheck`).

## ToDo

- [ ] Write `tools/pitcheck.py` and the import-linter config.
- [ ] Add positive/negative fixtures under `tests/pitcheck/`.
- [ ] Add the runtime privilege test.
- [ ] Wire into CI and mark required.

## Verification

### Tests
- Negative fixtures: a module importing `psycopg`, a module with `SELECT * FROM market.bar_1m`, a `revisions='latest'` call → each fails.
- Positive fixture: a module using `pit(as_of).table('market.bar_1m')` passes.
- Runtime: `mt_research_ro` direct select denied.

### Scenarios
- Given a contributor adds a notebook with raw SQL, when CI runs, then the build fails naming the file and line.
- Given an allow-list entry is past its expiry date, then the check fails.

### Stress / failure injection
- n/a: static check; runtime < 30 s in CI.

## Acceptance criteria

- [ ] CI fails on each negative fixture and passes on the positive one
- [ ] Runtime privilege test green
- [ ] Check is a required status on `main`
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Ops code (mt_api, mt_obs, flows) may read tables directly; only research paths are constrained.

## Cardinal rules (do NOT)

- Do NOT add blanket allow-list entries or disable the check to merge.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/03-build-spec.md` §4: name the CI check (`make pitcheck`).
- `docs/roadmap/phase-0-foundations.md`: tick T0.60 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T028-pit-bypass-ci-test`
- PR title: `P0-T028: Add the pit bypass test to CI`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T028` run

## Progress log

- 2026-10-21 00:00 · planner · created
