---
id: P1-T027
kind: task
title: Ingest ABS CPI for tax indexation
phase: 1
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T024]
requirements: [R1.06]
roadmap_todos: [T1.24]
modules: [M1]
dashboards: [D02]
branch: p1/P1-T027-abs-cpi-flow
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/09-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T027 · Ingest ABS CPI for tax indexation

## Goal / expected outcome

ABS CPI series (quarterly All Groups, weighted average of eight capital cities, and the monthly CPI) load point-in-time with every release, ready for the AU_2027_REFORM indexation in P3.

## Context & references

- Roadmap: requirements [R1.06](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.24](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (ABS CPI, needed for the 2027 tax indexation) · [09 Goals](../../../docs/09-journal-and-tax.md#goals) · consumer [P3 roadmap](../../../docs/roadmap/phase-3-journal-and-tax.md)
- Gap: which CPI series the indexation uses is not specified (P1-B016)
- Depends on (this phase): P1-T024

## Requirements

- ABS Data API (SDMX) via `sdmx1` (ABS provider) or the ABS SDMX REST endpoint; dataflow for CPI
- Store each release as a vintage (`event_time` = ABS release timestamp, 11:30 am Canberra time); revisions add rows
- Load both quarterly and monthly CPI index series until P3 confirms which one indexation uses
- Provenance `source=abs`, `licence=CC BY 4.0`, `commercial_ok=true`

## ToDo

- [ ] Implement the ABS adapter and daily check for new releases
- [ ] Load full history
- [ ] Pit test; docs
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: SDMX parsing of CPI dataflow fixture
- Integration: pit query before a release returns the previous quarter

### Scenarios

- Given ABS releases a revised quarter, when ingested, then both values exist and the pit query at an earlier date returns the original

### Stress / failure injection

- n/a: tiny dataset

## Acceptance criteria

- [ ] Quarterly and monthly CPI history loaded with vintages; release check running
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Base-period rebasing by ABS: store the series ID with its base; never mix bases in one series

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.24 once every task traced to it in PHASE.md is done; note P1-T027 next to it.
- `docs/09-journal-and-tax.md`: link the CPI series loaded and the open question in P1-B016

## Branch & PR

- Branch: `p1/P1-T027-abs-cpi-flow`
- PR title: `P1-T027: Ingest ABS CPI for tax indexation`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T027` run

## Progress log

- 2026-10-21 00:00 · planner · created
