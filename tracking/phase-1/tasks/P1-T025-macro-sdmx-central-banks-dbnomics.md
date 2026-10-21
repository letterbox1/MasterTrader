---
id: P1-T025
kind: task
title: Ingest sdmx1, central-bank and DBnomics series
phase: 1
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T024]
requirements: [R1.06]
roadmap_todos: [T1.24]
modules: [M1]
dashboards: [D02]
branch: p1/P1-T025-macro-sdmx-central-banks-dbnomics
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md, docs/06-aggregators-and-market-providers.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T025 · Ingest sdmx1, central-bank and DBnomics series

## Goal / expected outcome

One `sdmx1` client loads ECB/IMF/OECD/BIS/Eurostat series, direct fetchers load BoE IADB, BoC Valet, RBA, SNB and BoJ series, and DBnomics fills the rest, all into the same point-in-time macro tables.

## Context & references

- Roadmap: requirements [R1.06](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.24](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (Rates & macro) · [06 §3 Calendars & central banks](../../../docs/06-aggregators-and-market-providers.md#calendars--central-banks-m5--m3) (one SDMX client `sdmx1`, Apache-2.0; direct fetchers; DBnomics, AGPL lib fine for personal use)
- Open checks feeding this task: IMF SDMX 3.0 base URL, BoC/BoJ keyless (P1-T056)
- Depends on (this phase): P1-T024

## Requirements

- `sdmx1` providers: ECB, IMF (SDMX 3.0 URL from P1-T056), OECD, BIS, Eurostat
- Direct fetchers: BoE IADB CSV, BoC Valet JSON, RBA statistical tables (cash rate F1, yields F2), SNB data portal, BoJ time-series
- DBnomics as catch-all for anything else in the universe list
- Same table schema and pit rules as P1-T024; `source` per provider; licence tags from 06
- Each provider has a quota entry (most are keyless; conservative defaults)

## ToDo

- [ ] Implement provider adapters behind one `MacroSource` interface
- [ ] Map each universe series to provider + key in `config/universe.yaml`
- [ ] Tests with recorded fixtures per provider
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: parsers per provider (fixtures)
- Integration: each adapter loads its fixture into macro tables; pit query works

### Scenarios

- Given BoJ requires a key after all (open check fails), when the flow runs, then BoJ is disabled with a reason and DBnomics is used if it mirrors the series

### Stress / failure injection

- n/a: small batch volumes

## Acceptance criteria

- [ ] Every universe macro series from these providers loaded with history and a daily/weekly update
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- SDMX structure changes: adapter fails loudly; other providers continue

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.24 once every task traced to it in PHASE.md is done; note P1-T025 next to it.
- `docs/03-build-spec.md` §M1: list providers implemented
- `docs/06-aggregators-and-market-providers.md` §3: confirm the IMF/BoC/BoJ endpoints used

## Branch & PR

- Branch: `p1/P1-T025-macro-sdmx-central-banks-dbnomics`
- PR title: `P1-T025: Ingest sdmx1, central-bank and DBnomics series`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T025` run

## Progress log

- 2026-10-21 00:00 · planner · created
