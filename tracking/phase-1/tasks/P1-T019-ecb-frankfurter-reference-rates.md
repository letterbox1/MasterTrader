---
id: P1-T019
kind: task
title: Self-host Frankfurter and ingest ECB reference rates
phase: 1
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T005, P1-T007]
requirements: [R1.04]
roadmap_todos: [T1.23]
modules: [M1]
dashboards: [D02]
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, prefect-server]
branch: p1/P1-T019-ecb-frankfurter-reference-rates
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/02-v1-architecture.md]
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

# P1-T019 · Self-host Frankfurter and ingest ECB reference rates

## Goal / expected outcome

A self-hosted Frankfurter container serves ECB euro reference rates internally, and a daily flow stores them in `market.fx_reference` for cross-checks and UI conversions.

## Context & references

- Roadmap: requirements [R1.04](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.23](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (ECB reference rates + self-hosted Frankfurter) · [06 §3 Market data](../../../docs/06-aggregators-and-market-providers.md#market-data-m1) (Frankfurter, MIT)
- Depends on (this phase): P1-T005, P1-T007

## Requirements

- `frankfurter` service in Compose (image pinned by digest, internal `core` network only), its own DB volume
- Daily flow after ECB publication (~16:00 CET; schedule in P1-T053) stores (date, base EUR, quote, rate) with `source=ecb`, `licence=public`, `event_time` = ECB reference date 16:00 CET, `ingest_time` = now
- Backfill full ECB history once (from 1999)

## ToDo

- [ ] Add the container and health check
- [ ] Implement the flow and the backfill
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: parse Frankfurter JSON; weekend/holiday dates carry no rows (no forward-fill in storage)
- Integration: container up in CI and the flow loads a fixture date range

### Scenarios

- Given a TARGET holiday, when the flow runs, then nothing is written and no DQ incident is raised

### Stress / failure injection

- n/a: one call per day

## Acceptance criteria

- [ ] ECB rates from 1999 to today in `market.fx_reference`; daily update running
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- ECB revises rarely; a changed value is stored as a new row with later `ingest_time` (pit keeps both)

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.
- Do NOT add an image without pinning it by digest, or vendored code that carries telemetry or referral IDs.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.23 once every task traced to it in PHASE.md is done; note P1-T019 next to it.
- `docs/02-v1-architecture.md` §3.2: add the `frankfurter` container

## Branch & PR

- Branch: `p1/P1-T019-ecb-frankfurter-reference-rates`
- PR title: `P1-T019: Self-host Frankfurter and ingest ECB reference rates`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T019` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields; keyless public source)
