---
id: P7-T003
kind: task
title: Venue checks: AUSTRAC re-check, OKX AU derivatives and venue terms
phase: 7
type: USER
status: backlog
priority: critical
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R7.13, R7.04]
roadmap_todos: [T7.07, T7.63]
modules: [M11]
dashboards: [D06]
branch: p7/P7-T003-venue-checks-before-live
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T003 · Venue checks: AUSTRAC re-check, OKX AU derivatives and venue terms

## Goal / expected outcome

Every venue/product you intend to trade live has a fresh (< 90 days) AUSTRAC register check by ABN, its conduct/STP/rate-limit terms read, and OKX AU derivatives either reconciled or kept paper-only, all recorded in `ops.venue_registry`.

## Context & references

- Roadmap: [R7.13, R7.04 · ToDo T7.07, T7.63](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) (registry fields, starting classification) · [12 §3](../../../docs/12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention) (STP) · [12 §6](../../../docs/12-policy-and-compliance.md#6-professional-advice-triggers-tracked-as-tasks-in-d13--d15) (venue checks)
- Cross-phase: P0 T0.11/T0.22 (registry seed and table), P1 T1.30 (venue-health collector + quarterly re-check task).
- Related: P7-T046 (VERIFY re-check < 90 days before each funding), P7-T006 (accounts only at `allowed` venues)

## Requirements

- For each target venue: AUSTRAC VASP register status and `checked_at` date (must be < 90 days old at funding time), entity/ABN, products allowed for a retail client, max leverage (crypto derivatives ≤ 2× regardless, 12 §1).
- Read and summarise each venue's conduct, STP and rate-limit terms; record the STP parameter/mode to send on every order (12 §3 table).
- **OKX AU derivatives:** status stays `unresolved → paper only` unless reconciled in writing; do **not** attempt the derivatives test (five failed attempts lock derivatives permanently).
- Offshore derivatives (Bybit, Bitget, MEXC, Gate, KuCoin) stay data-only; Polymarket trading stays blocked; Binance AU and Kraken AU derivatives stay blocked for retail.

## ToDo

- [ ] List target venues for the first live sleeves (expected: one AU spot venue for trend on majors, e.g. Independent Reserve or BTC Markets; FP Markets if MasterTradingBot goes live).
- [ ] Search the AUSTRAC register by ABN for each; note status and date.
- [ ] Read each venue's client terms (conduct, algo/API use, STP, rate limits); note anything that changes the registry row.
- [ ] OKX AU: ask support in writing whether retail derivatives are available to you; record the answer or leave as paper-only.
- [ ] Enter results in D06 → Venues (tightening is immediate; marking a venue `allowed` is C3: Telegram approve + TOTP + cool-down).
- [ ] Confirm P7-T046's check shows every target venue `allowed` with `checked_at` < 90 days.

## Verification

### Tests
- n/a (user action); P7-T046 verifies the registry state programmatically.

### Scenarios
- Given a venue's `checked_at` is 91 days old, when you try to fund or step capital, then preflight blocks with 'registry re-check overdue'.
- Given OKX AU derivatives are unresolved, when a strategy targets OKX perps, then M11 rejects (product not `allowed`).

### Stress / failure injection
- n/a: one-off user check (repeats quarterly via the P1 re-check task).

## Acceptance criteria

- [ ] Each target venue row has status, `checked_at` < 90 days, products, max leverage, STP mode and a terms summary.
- [ ] OKX AU derivatives remain `read_only`/paper unless reconciled in writing.
- [ ] No offshore derivative venue is `allowed`.

## Exceptions & edge cases

- Register status changes between check and funding (e.g. cancellation like GetCoins, Sep 2026): the P1 venue-health monitor alerts, `venue.registry.changed` fires, and live bots auto-downgrade (P7-T029).
- DAF commencement (9 Apr 2027) and ASIC 2:1 order expiry (23 May 2027): re-check the affected rows on those dates.

## Cardinal rules (do NOT)

- Do NOT attempt the OKX AU derivatives test.
- Do NOT mark a venue `allowed` on unverified (U) information.
- Do NOT open multiple KYC accounts, use VPNs/proxies, or self-match across sub-accounts (12 §3).
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).

## Doc sync on completion

- `docs/12-policy-and-compliance.md` §2: update the starting-classification table with verified status and dates.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.07, T7.63 when this item is done.

## Branch & PR

- Branch: `p7/P7-T003-venue-checks-before-live`
- PR title: `P7-T003: Venue checks: AUSTRAC re-check, OKX AU derivatives and venue terms`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T003` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
