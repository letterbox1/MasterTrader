---
id: P1-T053
kind: task
title: Schedule batch flows by source update time in AEST/AEDT
phase: 1
type: OPS
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T015, P1-T018, P1-T019, P1-T020, P1-T022, P1-T023, P1-T024, P1-T025, P1-T026, P1-T027, P1-T028, P1-T029, P1-T008, P1-T037]
requirements: [R1.06, R1.08]
roadmap_todos: [T1.41]
modules: [M1]
dashboards: [D07]
branch: p1/P1-T053-prefect-batch-schedules
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T053 · Schedule batch flows by source update time in AEST/AEDT

## Goal / expected outcome

Every P1 batch flow has a Prefect deployment with a schedule aligned to its source's publication time, timezone-aware (Australia/Sydney for display, source timezone for triggers), within quota, with retries and alerts on failure.

## Context & references

- Roadmap: requirements [R1.06](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.08](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.41](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Roadmap T1.41 (respect quotas and source update times, AEST/AEDT aware) · [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) · UI [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) Feeds shows batch sources too
- Depends on (this phase): P1-T015, P1-T018, P1-T019, P1-T020, P1-T022, P1-T023, P1-T024, P1-T025, P1-T026, P1-T027, P1-T028, P1-T029, P1-T008, P1-T037

## Requirements

- Deployments in `infra/prefect/deployments.yaml` with cron + timezone per source, e.g. RBA F11 after 16:00 Australia/Sydney on business days, ABS CPI on release days 11:30 Australia/Canberra, ECB after 16:00 Europe/Berlin, FRED daily 08:00 America/New_York, COT Friday 15:30 America/New_York, EDGAR polling every 10 min US business hours, yfinance after 17:00 America/New_York, retention hourly, compaction 00:30 UTC, nightly DQ after compaction, tiering daily
- Each run checks the quota tracker before starting; retries with backoff (3×); failure → `alert.warning.batch_failed`; success updates the feed's last-message age in D07
- Concurrency limits per source (1) and a work-pool for heavy backfills off-peak

## ToDo

- [ ] Write deployments and a validation test that every batch source in `config/sources.yaml` has exactly one schedule
- [ ] DST tests for AU and US transitions
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: cron + timezone next-run calculations across DST changes (first Sunday of April/October in Sydney, March/November in New York)
- Integration: deployments register in a test Prefect server

### Scenarios

- Given a flow fails three times, when retries are exhausted, then an alert fires and D07 shows the source as degraded with the error

### Stress / failure injection

- n/a: schedules; quota behaviour is tested in P1-T006

## Acceptance criteria

- [ ] Every batch source scheduled; DST tests pass; failures alert
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Source publishes late: flow re-checks every 30 min for up to 6 h before failing

## Cardinal rules (do NOT)

- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.41 once every task traced to it in PHASE.md is done; note P1-T053 next to it.
- `docs/03-build-spec.md` §M1: link the schedule file

## Branch & PR

- Branch: `p1/P1-T053-prefect-batch-schedules`
- PR title: `P1-T053: Schedule batch flows by source update time in AEST/AEDT`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T053` run

## Progress log

- 2026-10-21 00:00 · planner · created
