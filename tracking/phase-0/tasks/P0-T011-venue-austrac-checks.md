---
id: P0-T011
kind: task
title: Check AU venues on the AUSTRAC register and send results for the registry seed
phase: 0
type: USER
status: ready
priority: medium
size: M
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R0.06]
roadmap_todos: [T0.11]
modules: [M11, ops]
dashboards: []
tools: []
mcp: []
env: []
services: [austrac-register]
branch: p0/P0-T011-venue-austrac-checks
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T011 · Check AU venues on the AUSTRAC register and send results for the registry seed

## Goal / expected outcome

For every venue you may use, you've looked up the AUSTRAC register entry by ABN, noted the products available to you as a **retail** client and the key model, and written the results into `infra/seed/venue_registry.yaml` (non-secret) so P0-T026 can seed `ops.venue_registry`.

## Context & references

- [Roadmap P0 T0.11](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [12 §2 venue registry](../../../docs/12-policy-and-compliance.md#2-venue-access-registry)
- [12 §1 AU boundary](../../../docs/12-policy-and-compliance.md#1-australian-boundary-the-load-bearing-assumption)
- [12 §6 advice triggers](../../../docs/12-policy-and-compliance.md#6-professional-advice-triggers-tracked-as-tasks-in-d13--d15)
- Related: P0-T025 table + loader, P0-T026 seed
- Unblocks: P0-T026 registry seed (R0.06); P2 registry check in M11

## Requirements

- Venues (12 §2 starting list): Independent Reserve, BTC Markets, Kraken AU (Bit Trade), Binance AU, OKX AU, CoinSpot, Swyftx, CoinJar; brokers IBKR, OANDA, IG, Alpaca, FP Markets; data-only Bybit, Bitget, MEXC, Gate, KuCoin, Hyperliquid.
- Per venue: legal entity, ABN/AFSL ids, AUSTRAC status + **date checked**, products allowed to you (spot/margin/perps/CFDs) + max leverage (crypto derivatives ≤ 2×, the L0 ceiling default in [16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)), key model (scopes, IP allow-list, withdrawal whitelist), proposed status `allowed` / `read_only` / `blocked` + reason.
- Netting brokers (OANDA, IG, Alpaca, IBKR) have no STP field: record `stp: n/a (netting)` ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P2-B006). Products blocked for live may be marked `paper_ok` (P2-B008).
- Mark unverified items `(U)`; OKX AU derivatives stay **unresolved → paper only**; Hyperliquid read-only until professional advice; Polymarket blocked.
- Output file: `infra/seed/venue_registry.yaml` (no secrets) using the field names from 12 §2 and the template from P0-T025.

## ToDo

- [ ] Search the AUSTRAC register by ABN for each venue; log status and date.
- [ ] Read each venue's AU retail product page and client agreement; note products, leverage, STP parameter, rate limits if visible.
- [ ] Fill `venue_registry.yaml` and hand it to P0-T026.
- [ ] Create a reminder for the quarterly re-check (P1 T1.30 automates it).

## Verification

### Tests
- Confirmation: P0-T026's loader validates the YAML and the registry query lists every venue with a `checked_at` date.

### Scenarios
- Given a venue's AUSTRAC registration is cancelled (e.g. GetCoins, Sep 2026), then it is seeded `blocked` with the reason and date.
- Given OKX AU derivatives are unresolved, then the seed sets derivatives `blocked` and you do **not** attempt a derivatives test (five failures lock it permanently).

### Stress / failure injection
- n/a: research action.

## Acceptance criteria

- [ ] Every listed venue has an AUSTRAC/status row with a checked date
- [ ] Products and leverage per venue recorded, (U) where unverified
- [ ] YAML handed to P0-T026

## Exceptions & edge cases

- Register search unavailable: log and retry; never guess a registration as 'allowed'.

## Cardinal rules (do NOT)

- Do NOT misstate retail/wholesale status to unlock products (12 §1).
- Do NOT use a VPN to reach venues not available in AU.
- Do NOT add paid data/APIs, ToS-breaking scraping, self-bots or user tokens; free tiers only ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/12-policy-and-compliance.md` §2: update the starting classification table with your verified results and dates.
- `docs/roadmap/phase-0-foundations.md`: tick T0.11 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T011-venue-austrac-checks`
- PR title: `P0-T011: Check AU venues on the AUSTRAC register and send results for the registry seed`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T011` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (L0 leverage ceiling as a 16 §2.1 default; netting STP n/a and paper_ok per 17 §D; run fields added)
