---
id: P1-T024
kind: task
title: Ingest FRED/ALFRED vintages and US Treasury rates
phase: 1
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T005, P1-T006, P1-T007]
requirements: [R1.06]
roadmap_todos: [T1.24]
modules: [M1]
dashboards: [D02]
branch: p1/P1-T024-macro-fred-alfred-treasury
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

# P1-T024 · Ingest FRED/ALFRED vintages and US Treasury rates

## Goal / expected outcome

Macro series land point-in-time in `market.macro_series` / `market.macro_obs`: FRED values with ALFRED vintages (so backtests see what was known then) and US Treasury yield curves, all queryable via `pit(as_of)`.

## Context & references

- Roadmap: requirements [R1.06](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.24](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (US Treasury, FRED/ALFRED vintages) · point-in-time rule [03 §4](../../../docs/03-build-spec.md#4-data-model-overview) · [SPEC non-negotiables](../../../SPEC.md#non-negotiable-requirements) NN1
- FRED key from sops (P0 T0.10)
- Depends on (this phase): P1-T005, P1-T006, P1-T007

## Requirements

- `market.macro_series` (id, source, title, units, frequency, seasonal adj., release) and `market.macro_obs` (series, period, value, `realtime_start`, `realtime_end`, `event_time`, `ingest_time`, provenance)
- ALFRED vintages: `event_time` = `realtime_start` (the date the value became known); a revision adds a row, never overwrites
- Treasury daily par yield curve (and real yields) from the Treasury's official feed with `event_time` = publication date
- Quota: FRED API limits via the quota tracker (budget in `config/quotas.yaml`, verify number)
- Universe macro list from `config/universe.yaml` (`macro:` section)

## ToDo

- [ ] Migration for macro tables (if not in P0) with pit-friendly indexes
- [ ] FRED/ALFRED client (fredapi or thin httpx) with vintage paging
- [ ] Treasury curve loader
- [ ] `pit` query tests proving no look-ahead
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: vintage mapping; revision creates a new row
- Integration: CPIAUCSL vintages fixture → `pit(as_of=2024-01-15)` returns the value published before that date, not the revised one

### Scenarios

- Given a series is revised, when the daily flow runs, then a new row appears and older `as_of` queries are unchanged
- Given FRED is down, when the flow runs, then it retries with backoff and marks the feed degraded in D07

### Stress / failure injection

- n/a: batch; the pit look-ahead test is the critical check

## Acceptance criteria

- [ ] Universe macro series and the Treasury curve loaded with vintages; pit look-ahead test passes in CI
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Discontinued FRED series: keep history, mark inactive
- Time zone: FRED dates are calendar dates (US); store as UTC midnight of that date and document it

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.24 once every task traced to it in PHASE.md is done; note P1-T024 next to it.
- `docs/03-build-spec.md` §M1: link the macro tables and vintage rule

## Branch & PR

- Branch: `p1/P1-T024-macro-fred-alfred-treasury`
- PR title: `P1-T024: Ingest FRED/ALFRED vintages and US Treasury rates`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T024` run

## Progress log

- 2026-10-21 00:00 · planner · created
