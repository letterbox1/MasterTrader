---
id: P1-T056
kind: task
title: Run the open provider checks and record them in 06
phase: 1
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.04, R1.05, R1.06]
roadmap_todos: [T1.60]
modules: [M1]
dashboards: []
branch: p1/P1-T056-verify-open-provider-checks
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/06-aggregators-and-market-providers.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T056 · Run the open provider checks and record them in 06

## Goal / expected outcome

Each open check from 06 §3 is tested against the live provider with a small script and recorded in 06 as pass/fail with the date and evidence, satisfying exit criterion 4 and unblocking P4's StockTwits decision.

## Context & references

- Roadmap: requirements [R1.04](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.05](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.06](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.60](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Checks: [06 §3 Open checks](../../../docs/06-aggregators-and-market-providers.md#open-checks-do-these-in-phase-1) · exit criterion 4 ([phase 1 §6 exit criteria](../../../docs/roadmap/phase-1-data-and-monitoring.md#6-exit-criteria-demo)) · P4 depends on the StockTwits result ([P4 roadmap](../../../docs/roadmap/phase-4-intel.md) R4.05)

## Requirements

- OANDA order book / position book endpoints (`/v3/instruments/{instrument}/orderBook` and `positionBook`) on the practice host return data
- TrueFX downloads still work (free registration, monthly files)
- Live IMF SDMX 3.0 base URL (record the exact URL `sdmx1` should use)
- IG client-sentiment endpoint path (demo) returns data
- StockTwits API reachability (`streams/symbol/{SYM}`), without auth and within terms
- Tardis.dev free monthly samples (which exchanges/data types, licence)
- BoC Valet and BoJ time-series work without a key
- Scripts in `tools/provider_checks/` (no secrets in output); results table appended to 06 §3 "Open checks"

## ToDo

- [ ] Write one check script per item using quota-aware clients
- [ ] Run each, capture status code, sample size and date
- [ ] Update 06 §3 with a pass/fail table and consequences (e.g. disable source in `config/sources.yaml` on fail)
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Each script exits 0 on pass, 1 on fail, and prints a one-line summary (no payload dumps)

### Scenarios

- Given StockTwits is unreachable, when recorded, then 06 marks it fail and P4 keeps it out of scope (R4.05)
- Given IMF moved its SDMX 3.0 URL, when found, then P1-T025 config uses the new URL

### Stress / failure injection

- n/a: one-off checks

## Acceptance criteria

- [ ] All seven checks have a pass/fail line with date in 06 §3
- [ ] Sources that failed are disabled in `config/sources.yaml` with the reason
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Inconclusive results (rate limited, temporary outage) are re-run once on another day before recording

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.60 once every task traced to it in PHASE.md is done; note P1-T056 next to it.
- `docs/06-aggregators-and-market-providers.md` §3 Open checks: pass/fail table with dates

## Branch & PR

- Branch: `p1/P1-T056-verify-open-provider-checks`
- PR title: `P1-T056: Run the open provider checks and record them in 06`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T056` run

## Progress log

- 2026-10-21 00:00 · planner · created
