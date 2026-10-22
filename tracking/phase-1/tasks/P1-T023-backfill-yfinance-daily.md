---
id: P1-T023
kind: task
title: Load yfinance daily history for stocks, ETFs and futures
phase: 1
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T013, P1-T006, P1-T009]
requirements: [R1.05, R1.06]
roadmap_todos: [T1.22]
modules: [M1]
dashboards: [D02]
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, prefect-server]
branch: p1/P1-T023-backfill-yfinance-daily
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

# P1-T023 · Load yfinance daily history for stocks, ETFs and futures

## Goal / expected outcome

A daily flow loads yfinance daily bars for universe stocks/ETFs, daily futures (e.g. `GC=F`, `CL=F`) and macro proxies (`^VIX`), giving every asset class a 1D series for D02 and exit criterion 1.

## Context & references

- Roadmap: requirements [R1.05](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.06](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.22](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (yfinance/OpenBB daily history; futures daily only: `GC=F`, `CL=F`; akshare for Asia) · [03 §6](../../../docs/03-build-spec.md#6-smallest-free-timeframe-by-asset-class) (futures: daily only)
- Licence: personal use only ([06 §3](../../../docs/06-aggregators-and-market-providers.md#3-additional-forex--multi-asset-providers) SaaS note)
- Depends on (this phase): P1-T013, P1-T006, P1-T009

## Requirements

- Daily bars into `market.bar_daily_vendor` (separate from built bars) with `source=yfinance`, `licence=personal`, `commercial_ok=false`
- Polite request rate via the quota tracker (yfinance has no published limit: conservative default, back off on errors)
- Store unadjusted OHLC plus adjusted close; record the yfinance version
- Futures continuous contracts flagged `continuous=true` (roll gaps are not data errors)

## ToDo

- [ ] Implement the flow (history once, then daily after US close in P1-T053)
- [ ] Optional akshare adapter for Asian futures behind a flag
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: dataframe → rows mapping; NaN rows dropped and counted
- Integration: fixture responses → rows; re-run idempotent

### Scenarios

- Given Yahoo returns an empty frame, when the flow runs, then it retries later and marks the source degraded after 3 failures

### Stress / failure injection

- n/a: one daily batch; quota tracker covers rate

## Acceptance criteria

- [ ] Daily history for all universe stocks/ETFs and listed futures; daily update running
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- yfinance breakage is common: failures alert and the flow falls back to the last good data with a stale flag, never silent

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.22 once every task traced to it in PHASE.md is done; note P1-T023 next to it.
- `docs/03-build-spec.md` §M1: note which futures tickers are loaded

## Branch & PR

- Branch: `p1/P1-T023-backfill-yfinance-daily`
- PR title: `P1-T023: Load yfinance daily history for stocks, ETFs and futures`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T023` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields; keyless source)
