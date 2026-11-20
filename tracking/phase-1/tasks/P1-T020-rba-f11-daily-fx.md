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
depends_on: [P1-T005, P1-T007, P0-T027, P1-T078]
requirements: [R1.04]
roadmap_todos: [T1.23]
modules: [M1]
dashboards: [D02]
tools: [git, cargo, docker]
mcp: []
env: []
services: [supabase-postgres]
branch: p1/P1-T020-rba-f11-daily-fx
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/09-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-T020 · Ingest RBA F11 daily exchange rates

## Goal / expected outcome

The RBA F11 daily AUD exchange rates are loaded in full history and updated each business day into `market.fx_reference`, ready for the P3 FX service and tax conversions.

## Context & references

- Roadmap: requirements [R1.04](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.23](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (RBA F11 daily FX, needed for tax) · [09 Goals](../../../docs/09-journal-and-tax.md#goals) (three currencies on every event; RBA daily rate with source and timestamp)
- Consumer: [P3 roadmap](../../../docs/roadmap/phase-3-journal-and-tax.md) T3.21 FX service (R3.03)
- Depends on (this phase): P1-T005, P1-T007, P1-T078 (`mt-connectors` base)
- Cross-phase prerequisites (depends_on): P0-T027 (`pit(as_of)` and Parquet catalog helpers)

## Requirements

- Download the RBA F11.1 CSV (current) and historical F11 files; parse all published currencies vs AUD
- Store (date, base AUD, quote, rate) with `source=rba_f11`, `licence=public`, `event_time` = publication date at the RBA's stated reference time (4.00 pm Sydney, verify on the table notes), `ingest_time` = now
- Keep every published revision (new row on change); never forward-fill in storage (the P3 FX service applies the decided fallback: last published business day; non-F11 currencies via USD with RBA AUD/USD × ECB/Frankfurter, [16 §4.3](../../../docs/16-configuration-and-safety-model.md#43-live-inputs-instead-of-constants), [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P3-B008)
- Data checks: rates > 0, no duplicate dates per currency, day-over-day move > 5% (default, configurable) flagged to DQ as `bad_reference` (not dropped)

## ToDo

- [ ] Implement the `rba_f11` provider in `mt-connectors`: downloader + parser for current and historical files (column headers change across files)
- [ ] Implement the daily job (scheduled in P1-T053) and the one-off history load
- [ ] Add the `pit` query helper `fx_reference::rate(base, quote, as_of)` in `mt-store` (Rust, one implementation) for P3 (`mt-journal`)
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- `cargo test -p mt-connectors rba_f11`: parser against fixtures of the current and two historical file layouts; header metadata rows skipped
- Integration: history load then daily increment; pit query returns the value known at `as_of`

### Scenarios

- Given an Australian public holiday, when the job runs, then no row is written and no incident raised
- Given RBA corrects a past value, when re-ingested, then both rows exist and `pit(as_of)` before the correction returns the old value

### Stress / failure injection

- n/a: one small file per day

## Acceptance criteria

- [ ] Full RBA F11 history loaded; daily update running; pit helper tested
- [ ] CI green (`cargo clippy`, `cargo test -p mt-connectors`, `cargo test -p mt-store`, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- RBA changes the CSV layout: parser fails loudly (alert) rather than loading misaligned columns

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)` (`mt-store`, also through its Python binding); research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.23 once every task traced to it in PHASE.md is done; note P1-T020 next to it.
- `docs/09-journal-and-tax.md`: link the `fx_reference` table and pit helper as the RBA source

## Branch & PR

- Branch: `p1/P1-T020-rba-f11-daily-fx`
- PR title: `P1-T020: Ingest RBA F11 daily exchange rates`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T020` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (RBA gap rule from 17 §D P3-B008 cited; 5% as default; P0 dep on pit)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (stays a Python Prefect flow; the `pit` FX helper lives in Rust `mt-store` with a Python binding; services supabase-postgres)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (Python Prefect flow → `mt-connectors` `rba_f11` provider (Rust) on `mt-scheduler`; FX `pit` helper serves the Rust `mt-journal` (binding not needed here); deps +P1-T078; tools cargo; services drop prefect-server)
