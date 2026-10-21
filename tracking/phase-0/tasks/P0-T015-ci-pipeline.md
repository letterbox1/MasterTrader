---
id: P0-T015
kind: task
title: Set up the CI pipeline (lint, types, tests, audit, secrets)
phase: 0
type: OPS
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T014]
requirements: [R0.01, R0.N5, R0.N1]
roadmap_todos: [T0.20, T0.65]
modules: [ops]
dashboards: []
branch: p0/P0-T015-ci-pipeline
pr: ""
doc_sync: [README.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T015 · Set up the CI pipeline (lint, types, tests, audit, secrets)

## Goal / expected outcome

GitHub Actions runs on every PR and on `main`: `uv sync --locked`, ruff, mypy, pytest (with a Postgres+Timescale service container), `pip-audit`, gitleaks, and wired jobs that later items fill (`pit` bypass check, migration test, Playwright matrix, trivy/grype). Branch protection requires these checks.

## Context & references

- [Roadmap P0 R0.01, R0.N5](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [07 §7 supply chain](../../../docs/07-security-notes.md#7-supply-chain)
- [07 §2 secrets](../../../docs/07-security-notes.md#2-secrets)
- [03 §9 hygiene](../../../docs/03-build-spec.md#9-future-proof-hygiene)
- Related: P0-T004 (branch protection), P0-T028, P0-T053, P0-T056
- Depends on: P0-T014

## Requirements

- Workflow `.github/workflows/ci.yml` with jobs `python` (lint/type/test), `security` (gitleaks full history, pip-audit), `migrations` (filled by P0-T024), `web` (filled by P0-T047), `images` (filled by P0-T056).
- All third-party actions pinned by **commit SHA**, not tag; `permissions: contents: read` by default; `actionlint` runs.
- Postgres service container uses the **same digest** as compose (single source: `infra/images.lock`).
- Runtime budget: pipeline ≤ 15 min p95 so free private-repo minutes (2,000/month on GitHub Free) last; the Playwright matrix runs on `apps/web/**` changes and nightly.
- No real secrets in CI for P0 (tests use throwaway credentials).

## ToDo

- [ ] Write `ci.yml` with the jobs above; pin actions by SHA.
- [ ] Add path filters and concurrency groups (cancel superseded runs).
- [ ] Add `pip-audit --strict` against `uv export --format requirements-txt`.
- [ ] Add the gitleaks job scanning full history (`fetch-depth: 0`).
- [ ] Add the wired jobs later tasks fill; each fails closed once enabled if its script is missing.
- [ ] Ask the user (via P0-T004) to mark the jobs as required checks.

## Verification

### Tests
- Self-test: a PR with a ruff error fails `python`; a PR with a fake secret fails `security`; a test branch pinning a known-vulnerable dependency fails `pip-audit`.

### Scenarios
- Given a contributor references an action by tag instead of SHA, when CI runs the SHA-pin check, then it fails.
- Given CI minutes run low, then the nightly matrix is the first thing to throttle (documented in README).

### Stress / failure injection
- n/a: pipeline config; duration measured over the first 10 runs (log p95).

## Acceptance criteria

- [ ] All jobs run on PRs; the failing examples fail
- [ ] Actions pinned by SHA; default permissions read-only
- [ ] p95 duration ≤ 15 min over 10 runs (logged)
- [ ] Required checks configured on `main`
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- GitHub outage: merges wait; never merge without checks.
- pip-audit false positive: ignore by ID with expiry date and reason, never globally.

## Cardinal rules (do NOT)

- Do NOT store real secrets in GitHub Actions secrets for P0.
- Do NOT use `pull_request_target` with checkout of PR code.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get CI green.
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `README.md`: CI section (jobs, how to run locally with `make check`).
- `docs/roadmap/phase-0-foundations.md`: tick T0.20, T0.65 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T015-ci-pipeline`
- PR title: `P0-T015: Set up the CI pipeline (lint, types, tests, audit, secrets)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T015` run

## Progress log

- 2026-10-21 00:00 · planner · created
