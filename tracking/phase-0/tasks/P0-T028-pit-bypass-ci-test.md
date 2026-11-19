---
id: P0-T028
kind: task
title: Add the pit bypass guard to CI (Rust and Python)
phase: 0
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T027, P0-T071, P0-T015]
requirements: [R0.04]
roadmap_todos: [T0.60]
modules: [mt_store]
dashboards: []
tools: [git, cargo, uv, python>=3.12, supabase, just]
mcp: []
env: []
services: [supabase-postgres]
branch: p0/P0-T028-pit-bypass-ci-test
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md]
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

# P0-T028 · Add the pit bypass guard to CI (Rust and Python)

## Goal / expected outcome

CI fails the build if any research-side code, **Rust or Python**, reads raw tables instead of `pit(as_of)` ([18 §4.4](../../../docs/18-platform-and-deployment.md#44-point-in-time-and-worm)): a static check per language plus a runtime DB-privilege test.

## Context & references

- [Roadmap P0 R0.04](../../../docs/roadmap/phase-0-foundations.md#3-requirements) · [T0.60](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [SPEC non-negotiables](../../../SPEC.md#non-negotiable-requirements) (NN1)
- [03 §4 data model](../../../docs/03-build-spec.md#4-data-model-overview) · [18 §4.4](../../../docs/18-platform-and-deployment.md#44-point-in-time-and-worm)
- [04 standing rules](../../../docs/04-plan-of-action.md#standing-rules) (pit test mandatory)
- Depends on: P0-T027 (Rust `pit`), P0-T071 (Python binding), P0-T015 (CI)

## Requirements

- Research-side code: Python packages `mt_lab`, `mt_features`, `mt_strategy`, `mt_agents`, `mt_memory`, `mt_models`, `mt_anomaly`, plus `notebooks/` and `strategies/` (Python and Rust strategies); Rust strategy crates and any crate marked `research` in its `Cargo.toml` metadata.
- **Python static check** (`tools/pitcheck`, AST-based): in those paths, fail on imports of `sqlalchemy`, `psycopg`, `asyncpg`, `duckdb`, `supabase` or `polars.read_database`; fail on string literals matching `\b(FROM|JOIN)\s+(market|text|features|journal|audit|curation|strategy|risk)\.`; fail on `revisions='latest'`. import-linter contract: research packages may import `mt_store.pit` and `mt_store.catalog` only.
- **Rust static check**: research crates may depend on `mt-store` (`pit`, `catalog` modules) but not on `sqlx`, `tokio-postgres`, `postgres` or `duckdb` (`cargo deny` bans per crate + a `cargo metadata` script); a source scan for the same SQL pattern and `As::Latest`.
- Allow-list file with justification + expiry only.
- Runtime check: an integration test (pgTAP + a Rust test) logs in as `mt_research_ro` and asserts `SELECT` on each fact table raises `insufficient_privilege`, while pit functions work.
- Wired as a required CI step (`just pitcheck`).

## ToDo

- [ ] Write `tools/pitcheck` (Python AST + import-linter config) and the Rust dependency/source check.
- [ ] Add positive/negative fixtures under `tests/pitcheck/` for both languages.
- [ ] Add the runtime privilege test (pgTAP in `supabase/tests/`, Rust integration test).
- [ ] Wire into CI (`just pitcheck`) and mark required.

## Verification

### Tests
- Negative fixtures: a Python module importing `psycopg`, a Python module with `SELECT * FROM market.bar`, a `revisions='latest'` call, a Rust research crate depending on `sqlx`, a Rust file with raw `FROM market.` SQL → each fails.
- Positive fixtures: Python `mt_store.pit(as_of).bars(...)` and Rust `mt_store::pit(as_of, &clock).bars(...)` pass.
- Runtime: `supabase test db` and `cargo test -p mt-store --test research_role`: `mt_research_ro` direct select denied.

### Scenarios
- Given a contributor adds a notebook or a Rust strategy with raw SQL, when CI runs, then the build fails naming the file and line.
- Given an allow-list entry is past its expiry date, then the check fails.

### Stress / failure injection
- n/a: static checks; runtime < 30 s in CI.

## Acceptance criteria

- [ ] CI fails on each negative fixture (both languages) and passes on the positive ones
- [ ] Runtime privilege test green
- [ ] Check is a required status on `main`
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, `supabase test db`, gitleaks, `pit` check)

## Exceptions & edge cases

- Ops code (`mt-api`, `mt-obs`, `mt-store` itself, flows) may read tables directly; only research paths are constrained.

## Cardinal rules (do NOT)

- Do NOT add blanket allow-list entries or disable the check to merge.
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/03-build-spec.md` §4: name the CI check (`just pitcheck`) and that it covers Rust and Python.
- `docs/roadmap/phase-0-foundations.md`: tick T0.60 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T028-pit-bypass-ci-test`
- PR title: `P0-T028: Add the pit bypass guard to CI (Rust and Python)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T028` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (no decision changes (note: roadmap T0.28 is the LiteLLM callback, not this task); run fields added)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (guard covers Rust research crates (cargo deny bans + source scan) and Python (AST + import-linter); runtime test via pgTAP; depends on P0-T071; make → just)
