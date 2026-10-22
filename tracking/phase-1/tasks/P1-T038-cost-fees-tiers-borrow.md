---
id: P1-T038
kind: task
title: Measure fees, fee tiers and borrow rates
phase: 1
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T004, P1-T005, P0-T029, P0-T030]
requirements: [R1.11]
roadmap_todos: [T1.28]
modules: [M16]
dashboards: [D07, D02]
tools: [git, uv, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p1/P1-T038-cost-fees-tiers-borrow
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

# P1-T038 · Measure fees, fee tiers and borrow rates

## Goal / expected outcome

`mt_monitor.cost` reads current fee tiers and borrow rates from free APIs for every practice/testnet venue, stores them as time series, and publishes snapshots on `cost.{venue}.{symbol}`.

## Context & references

- Roadmap: requirements [R1.11](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.28](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (Fees: commissions per fill and current fee tiers via ccxt `fetchTradingFees`, Binance commission endpoint, IBKR `commissionAndFeesReport`, Alpaca; borrow rates)
- Build first, keys last ([17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)): built keyless against ccxt/venue fixtures and public fee schedules (`source=public_schedule`); reading your testnet fee tiers with the read-only keys from P1-T002 is checked in P1-T073
- Cross-phase prerequisites (depends_on): P0-T029, P0-T030 (WORM layer for `audit.cost_event`)
- Depends on (this phase): P1-T004, P1-T005

## Requirements

- Tables `market.fee_tier` (venue, account, symbol, maker, taker, tier, `event_time`, `ingest_time`, source) and `market.borrow_rate`
- Collectors: ccxt `fetchTradingFees` (Binance/Bybit testnet), Binance commission endpoint, Alpaca fee schedule (commission-free + regulatory fees), IBKR via its report once fills exist (P2)
- Refresh every 6 h (default, configurable) and on demand; changes emit `cost.*` snapshot and `audit.cost_event` (WORM)
- GET-only HTTP client allow-list; credentials never logged

## ToDo

- [ ] Implement collectors and tables
- [ ] Cost snapshot payload and publisher
- [ ] WORM tests for `audit.cost_event`
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: fee parsing per venue fixture; tier change detection
- WORM: app-role UPDATE/DELETE on `audit.cost_event` fails
- Integration: ccxt mock → rows + `cost.*` message

### Scenarios

- Given read-only keys are missing for a venue, when the collector runs, then it uses the public schedule and marks the fee `unverified` in D07

### Stress / failure injection

- n/a: low-frequency polling

## Acceptance criteria

- [ ] Fee tiers from public schedules and fixtures visible in D07 Costs, labelled `unverified` until P1-T073 reads them live
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Testnet fee tiers may differ from live; label `testnet` so P2 cost models do not mistake them

## Cardinal rules (do NOT)

- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use keys with withdrawal rights, or without an IP allow-list where the venue supports one; practice/testnet/paper only, no live money before the P7 gates.
- Do NOT place, modify or cancel orders from this code; P1 is read-only toward venues (orders arrive in P2 through M11).
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.28 once every task traced to it in PHASE.md is done; note P1-T038 next to it.
- `docs/03-build-spec.md` §M16: note testnet vs live fee labelling

## Branch & PR

- Branch: `p1/P1-T038-cost-fees-tiers-borrow`
- PR title: `P1-T038: Measure fees, fee tiers and borrow rates`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T038` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keyless build, live fee tiers in P1-T073; deps trimmed (no WS needed); P0 WORM deps)
