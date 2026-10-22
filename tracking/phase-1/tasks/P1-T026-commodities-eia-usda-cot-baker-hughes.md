---
id: P1-T026
kind: task
title: Ingest EIA, USDA, CFTC COT and Baker Hughes data
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
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, prefect-server]
branch: p1/P1-T026-commodities-eia-usda-cot-baker-hughes
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
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

# P1-T026 · Ingest EIA, USDA, CFTC COT and Baker Hughes data

## Goal / expected outcome

Commodity fundamentals and positioning (EIA energy series and STEO, USDA WASDE/QuickStats, CFTC COT, Baker Hughes rig count) load point-in-time on their release schedules for D02 and P2 features.

## Context & references

- Roadmap: requirements [R1.06](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.24](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (Futures/commodities: EIA, USDA, CFTC COT, Baker Hughes) · [06 §3 Reports, nowcasts & forecasts](../../../docs/06-aggregators-and-market-providers.md#reports-nowcasts--forecasts-m6-features-m5-release-events)
- Build first, keys last ([17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)): EIA is built keyless against fixtures (live with your EIA key from P0-T010 in P1-T073); CFTC COT, Baker Hughes and USDA WASDE files are keyless and run live here. USDA QuickStats needs a free key that no USER task provides yet (gap P1-B019): it ships disabled with the reason until decided
- Depends on (this phase): P1-T024

## Requirements

- EIA API v2 series (crude stocks, production) with release timestamps as `event_time`
- USDA WASDE report tables (monthly, keyless); QuickStats API behind `USDA_QUICKSTATS_API_KEY`, disabled until P1-B019 is decided
- CFTC COT (legacy + disaggregated futures-only) weekly files; `event_time` = Friday 15:30 ET release, not the Tuesday as-of date (store both)
- Baker Hughes weekly rig count file (official download)
- Same macro table schema; provenance from 06

## ToDo

- [ ] Implement four adapters and their schedules hooks (P1-T053)
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: COT as-of vs release date mapping; WASDE table parser
- Integration: fixtures → macro tables; pit query before release returns the previous week

### Scenarios

- Given a US federal holiday delays COT, when the flow runs on Friday, then it retries Monday and `event_time` is the actual release time

### Stress / failure injection

- n/a: weekly/monthly batches

## Acceptance criteria

- [ ] COT, Baker Hughes and WASDE loaded live with history and on schedule; EIA proven on fixtures (live in P1-T073); QuickStats enabled or disabled-with-reason per P1-B019; COT pit test passes
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Baker Hughes changes its file format/URL often: fail loudly and alert; manual URL override in config

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.24 once every task traced to it in PHASE.md is done; note P1-T026 next to it.
- `docs/03-build-spec.md` §M1: note release-time handling for COT

## Branch & PR

- Branch: `p1/P1-T026-commodities-eia-usda-cot-baker-hughes`
- PR title: `P1-T026: Ingest EIA, USDA, CFTC COT and Baker Hughes data`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T026` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keyless build, EIA live in P1-T073; USDA QuickStats key gap P1-B019)
