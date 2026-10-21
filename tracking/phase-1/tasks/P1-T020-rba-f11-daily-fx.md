---
id: P1-T020
kind: task
title: Ingest RBA F11 daily exchange rates
phase: 1
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T005, P1-T007]
requirements: [R1.04]
roadmap_todos: [T1.23]
modules: [M1]
dashboards: [D02]
branch: p1/P1-T020-rba-f11-daily-fx
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

# P1-T020 · Ingest RBA F11 daily exchange rates

## Goal / expected outcome

The RBA F11 daily AUD exchange rates are loaded in full history and updated each business day into `market.fx_reference`, ready for the P3 FX service and tax conversions.

## Context & references

- Roadmap: requirements [R1.04](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.23](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (RBA F11 daily FX, needed for tax) · [09 Goals](../../../docs/09-journal-and-tax.md#goals) (three currencies on every event; RBA daily rate with source and timestamp)
- Consumer: [P3 roadmap](../../../docs/roadmap/phase-3-journal-and-tax.md) T3.21 FX service (R3.03)
- Depends on (this phase): P1-T005, P1-T007

## Requirements

- Download the RBA F11.1 CSV (current) and historical F11 files; parse all published currencies vs AUD
- Store (date, base AUD, quote, rate) with `source=rba_f11`, `licence=public`, `event_time` = publication date at the RBA's stated reference time (4.00 pm Sydney, verify on the table notes), `ingest_time` = now
- Keep every published revision (new row on change); never forward-fill in storage (P3 decides the fallback rule for non-business days)
- Data checks: rates > 0, no duplicate dates per currency, day-over-day move > 5% flagged to DQ as `bad_reference` (not dropped)

## ToDo

- [ ] Implement downloader + parser for current and historical files (column headers change across files)
- [ ] Implement the daily flow and the one-off history load
- [ ] Add `pit` query helper `fx_reference.rate(base, quote, as_of)` for P3
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: parser against fixtures of the current and two historical file layouts; header metadata rows skipped
- Integration: history load then daily increment; pit query returns the value known at `as_of`

### Scenarios

- Given an Australian public holiday, when the flow runs, then no row is written and no incident raised
- Given RBA corrects a past value, when re-ingested, then both rows exist and `pit(as_of)` before the correction returns the old value

### Stress / failure injection

- n/a: one small file per day

## Acceptance criteria

- [ ] Full RBA F11 history loaded; daily update running; pit helper tested
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- RBA changes the CSV layout: parser fails loudly (alert) rather than loading misaligned columns

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.23 once every task traced to it in PHASE.md is done; note P1-T020 next to it.
- `docs/09-journal-and-tax.md`: link the `fx_reference` table and pit helper as the RBA source

## Branch & PR

- Branch: `p1/P1-T020-rba-f11-daily-fx`
- PR title: `P1-T020: Ingest RBA F11 daily exchange rates`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T020` run

## Progress log

- 2026-10-21 00:00 · planner · created
