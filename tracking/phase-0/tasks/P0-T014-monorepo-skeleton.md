---
id: P0-T014
kind: task
title: Create the uv workspace monorepo skeleton with quality tooling
phase: 0
type: BUILD
status: ready
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.01, R0.N5]
roadmap_todos: [T0.20]
modules: [mt_core, mt_store, mt_api, mt_obs]
dashboards: []
branch: p0/P0-T014-monorepo-skeleton
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, README.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T014 · Create the uv workspace monorepo skeleton with quality tooling

## Goal / expected outcome

A `uv` workspace monorepo with every package from 03 §3 as an importable stub, the 02 §11 top-level layout, ruff/mypy/pytest configured, pre-commit with gitleaks, and `third_party/LICENSES.md`. `uv sync --locked && uv run pytest` passes on a clean clone.

## Context & references

- [Roadmap P0 R0.01, R0.N5](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.20](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [03 §3 repo layout](../../../docs/03-build-spec.md#3-repository-layout)
- [02 §11 repo layout](../../../docs/02-v1-architecture.md#11-repository-layout)
- [03 §9 hygiene](../../../docs/03-build-spec.md#9-future-proof-hygiene)
- [07 §7 supply chain](../../../docs/07-security-notes.md#7-supply-chain)
- Layout conflict between 02 §11 and 03 §3 is filed as P0-B006; this task follows **02 §11** (`infra/`, `migrations/`, `apps/web/`) and notes it in the PR.

## Requirements

- Python **3.12**, `uv` workspace: root `pyproject.toml` with `[tool.uv.workspace] members = ["packages/*"]`; `uv.lock` committed **with hashes**.
- Packages (stubs with `__init__.py`, `py.typed`, one smoke test each): `mt_core, mt_store, mt_data, mt_features, mt_strategy, mt_lab, mt_agents, mt_memory, mt_models, mt_anomaly, mt_risk, mt_engine, mt_monitor, mt_obs, mt_journal, mt_airdrop, mt_curation, mt_treasury, mt_social, mt_api, mt_ui, mt_mcp`.
- Top level per 02 §11: `apps/web/`, `services/`, `strategies/`, `infra/`, `migrations/`, `third_party/` (+ `LICENSES.md` table: name, upstream URL, pinned commit, licence, telemetry check date), `tests/`, `notebooks/`, `docs/runbooks/`.
- ruff (lint + format, line length 110, rules E,F,I,B,UP,S,ASYNC), mypy `--strict` on `mt_core, mt_store, mt_api, mt_obs` (others `--check-untyped-defs`), pytest + `pytest-asyncio`, coverage ≥ 80 % on P0 packages.
- pre-commit: ruff, ruff-format, mypy (changed files), **gitleaks** (pinned rev), check-yaml, end-of-file, `no-commit-to-branch main`.
- `.gitignore` covers `.env*`, `*.sops.dec*`, `secrets*.yaml` except `*.example.yaml`, `/data`, `node_modules`.

## ToDo

- [ ] Create root `pyproject.toml`, workspace members and the shared dev-dependency group; run `uv lock`.
- [ ] Generate the 22 package stubs with `pyproject.toml` each (hatchling), `py.typed` and `tests/test_import.py`.
- [ ] Create top-level folders with one-line READMEs; add `third_party/LICENSES.md` with the table header and vendoring rules (07 §7).
- [ ] Configure ruff, mypy, pytest, coverage in root `pyproject.toml`.
- [ ] Add `.pre-commit-config.yaml` with pinned revs incl. gitleaks; `.gitleaks.toml` allow-lists only `tests/fixtures/fake_secrets/`.
- [ ] Add a `Makefile` with `lint`, `type`, `test`, `check` targets used by CI.
- [ ] Update docs listed under Doc sync.

## Verification

### Tests
- Unit: each package's `test_import.py` imports it.
- Tooling: `pre-commit run --all-files` clean; `uv sync --locked` succeeds on a fresh clone (CI job).

### Scenarios
- Given a developer adds `AWS_SECRET_ACCESS_KEY=...` to a file, when committing, then gitleaks blocks the commit.
- Given `uv.lock` is out of date, when CI runs `uv sync --locked`, then it fails.

### Stress / failure injection
- n/a: scaffolding.

## Acceptance criteria

- [ ] `uv sync --locked && uv run pytest` passes on a clean clone
- [ ] All 22 packages importable; mypy strict passes on the four core packages
- [ ] `pre-commit run --all-files` clean; gitleaks blocks a planted secret
- [ ] `third_party/LICENSES.md` exists with the table and rules
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Package list changes later (e.g. `mt_signer` in P5): add then; stubs here are placeholders, not designs.

## Cardinal rules (do NOT)

- Do NOT install anything with `curl | sh`; use pinned packages only (07 §7).
- Do NOT add runtime dependencies to stub packages beyond what P0 needs.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get CI green.
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` §3 and `docs/02-v1-architecture.md` §11: align the layout to what was built (see P0-B006).
- `README.md`: add 'Getting started' (uv sync, pre-commit install).
- `docs/roadmap/phase-0-foundations.md`: tick T0.20 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T014-monorepo-skeleton`
- PR title: `P0-T014: Create the uv workspace monorepo skeleton with quality tooling`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T014` run

## Progress log

- 2026-10-21 00:00 · planner · created
