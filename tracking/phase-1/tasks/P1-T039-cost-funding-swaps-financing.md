---
id: P1-T039
kind: task
title: Measure funding rates and swap/financing costs
phase: 1
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T038, P1-T016, P1-T017]
requirements: [R1.11]
roadmap_todos: [T1.28]
modules: [M16]
dashboards: [D07, D02]
branch: p1/P1-T039-cost-funding-swaps-financing
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

# P1-T039 · Measure funding rates and swap/financing costs

## Goal / expected outcome

Perp funding (predicted and realised) and FX/CFD financing (OANDA `InstrumentFinancing`, IG funding) are stored and published, so the Costs panels populate (exit criterion 2) and P2 backtests can use measured carry.

## Context & references

- Roadmap: requirements [R1.11](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.28](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (Funding and swaps) · [phase 1 §6 exit criteria](../../../docs/roadmap/phase-1-data-and-monitoring.md#6-exit-criteria-demo) item 2
- Depends on (this phase): P1-T038, P1-T016, P1-T017

## Requirements

- Funding: predicted (next funding rate from public mark-price/premium-index streams) and realised (settled rates history) for perps on Binance, Bybit, OKX; table `market.funding_rate` (venue, symbol, kind predicted|realised, rate, interval, `event_time`)
- Financing: OANDA instrument financing rates (long/short) daily and realised financing transactions from the practice account; IG funding from demo transactions; table `market.financing_rate`
- Publish on `cost.{venue}.{symbol}` with funding/swap fields

## ToDo

- [ ] Implement funding collectors (public) and financing collectors (practice/demo, GET-only)
- [ ] Backfill realised funding history for universe perps
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: rate normalisation to per-interval and annualised
- Integration: fixtures → tables; snapshot message contains predicted + last realised

### Scenarios

- Given a funding interval change by the venue (e.g. 8 h → 4 h), when detected, then the interval is stored per row and annualisation uses it

### Stress / failure injection

- n/a: low-frequency polling; streams already covered by P1-T010

## Acceptance criteria

- [ ] Funding and financing series populate D07 Costs and D02 Costs for universe instruments
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Practice accounts with no positions have no realised financing: show rates only and label realised as "none yet"

## Cardinal rules (do NOT)

- Do NOT use keys with withdrawal rights or without an IP allow-list; practice/testnet/paper only, no live money before the P7 gates.
- Do NOT place, modify or cancel orders from this code; P1 is read-only toward venues (orders arrive in P2 through M11).
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.28 once every task traced to it in PHASE.md is done; note P1-T039 next to it.
- `docs/03-build-spec.md` §M16: tables for funding/financing

## Branch & PR

- Branch: `p1/P1-T039-cost-funding-swaps-financing`
- PR title: `P1-T039: Measure funding rates and swap/financing costs`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T039` run

## Progress log

- 2026-10-21 00:00 · planner · created
