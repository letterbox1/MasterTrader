---
id: P1-T022
kind: task
title: Backfill Alpaca IEX history for stocks and ETFs
phase: 1
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T021, P1-T012, P1-T013]
requirements: [R1.05]
roadmap_todos: [T1.22]
modules: [M1]
dashboards: [D07]
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, prefect-server]
branch: p1/P1-T022-backfill-alpaca-history
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

# P1-T022 · Backfill Alpaca IEX history for stocks and ETFs

## Goal / expected outcome

A resumable flow loads Alpaca IEX historical trades and minute bars for universe stocks/ETFs into the catalog and `market.bar_1m`, tagged IEX.

## Context & references

- Roadmap: requirements [R1.05](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.22](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Roadmap T1.22 (Alpaca history) · [03 §6](../../../docs/03-build-spec.md#6-smallest-free-timeframe-by-asset-class) (Alpaca IEX history; daily via yfinance)
- Depends on (this phase): P1-T021, P1-T012, P1-T013
- Build first, keys last ([17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)): built keyless against fixture pages; the full history load runs with your Alpaca paper keys in P1-T073

## Requirements

- Historical endpoints with `feed=iex`; page through with the quota tracker
- Trades → catalog (`source=alpaca_iex`); 1m bars → `market.bar_1m_vendor` (`bar_source=vendor_bar`), never into the live aggregates
- Manifest in `ops.backfill_job`; report like P1-T015

## ToDo

- [ ] Implement the backfill flow with paging and manifest
- [ ] Report generation
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: pagination token handling; IEX flag carried
- Integration: fixture pages → catalog + bars; idempotent re-run

### Scenarios

- Given a 429, when received, then the flow waits per `Retry-After` and resumes

### Stress / failure injection

- Load: 2 years of 1m bars for 30 symbols within free limits; time and bytes recorded

## Acceptance criteria

- [ ] Fixture backfill, paging and resume tests pass keyless; the full load with a backfill report runs with your paper keys in P1-T073
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Splits/dividends: store raw (unadjusted) and record the adjustment flag; adjusted series are derived later

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.
- Do NOT use keys with withdrawal rights, or without an IP allow-list where the venue supports one; practice/testnet/paper only, no live money before the P7 gates.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.22 once every task traced to it in PHASE.md is done; note P1-T022 next to it.
- `docs/03-build-spec.md` §M1: note history depth obtained

## Branch & PR

- Branch: `p1/P1-T022-backfill-alpaca-history`
- PR title: `P1-T022: Backfill Alpaca IEX history for stocks and ETFs`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T022` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (vendor 1m bars in market.bar_1m_vendor; keyless build, full keyed load in P1-T073)
