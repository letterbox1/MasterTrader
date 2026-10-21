---
id: P5-T027
kind: task
title: Monitors: venue health, bridge policy and concentration
phase: 5
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T022]
requirements: [R5.06]
roadmap_todos: [T5.23]
modules: [M22, M16, M11]
dashboards: [D18]
branch: p5/P5-T027-monitors-venue-bridge-concentration
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T027 · Monitors: venue health, bridge policy and concentration

## Goal / expected outcome

Venue health (withdrawal delays, proof-of-reserve changes, AUSTRAC registration status from `ops.venue_registry`), bridge policy (native USDC via CCTP or canonical bridges only, per-bridge caps, no bridging inside a live strategy leg) and concentration limits (per protocol, chain, stablecoin and venue; ≤ 25% equity per exchange) are evaluated continuously against the unified wallet view and fed to M11 and D18.

## Context & references

- Roadmap: [R5.06](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.23
- [13 §6](../../../docs/13-wallets-treasury-and-onchain.md#6-monitors-feed-m16-and-m11) · [12 §2 venue registry](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) · P1 venue-health collector (T1.30 / R1.13)
- Concentration number conflict (25% vs 25–30%) → P5-B006

## Requirements

- Venue health: reuse P1 collector output; add D18 venue-health rows; stale AUSTRAC check (> 90 days) → `VENUE_CHECK` task.
- Bridge policy: bridge allow-list (CCTP, canonical L2 bridges) in config; any intent or detected transfer via a non-allow-listed bridge → alert; signer refuses bridge intents in P5 (bridging is never automated per 07 §4/08).
- Concentration: compute shares from D18 rollups; breach of the venue cap (25% default, stricter of the conflicting docs) → M11 blocks deposits/new exposure there; protocol/chain/stablecoin caps configurable.
- Outputs to `monitor.event`, `risk.event`, Grafana.

## ToDo

- [ ] Implement `monitors/venue_health.py`, `bridge_policy.py`, `concentration.py`.
- [ ] M11 integration for concentration blocks (via risk events/limit state).
- [ ] D18 data endpoints; tests; doc sync.

## Verification

### Tests
- Unit: concentration calc with fixtures (exchange at 26% → breach).
- Unit: transfer via an unknown bridge contract → alert.
- Integration: M11 rejects a deposit-increasing order to a venue above cap.

### Scenarios
- Given an exchange's withdrawal delays exceed 24 h, then D18 shows red venue health and an urgent task to review exposure.
- Given AUSTRAC re-check is older than 90 days, then a `VENUE_CHECK` task appears in D13.

### Stress / failure injection
- n/a: low-frequency evaluations (≤ every 5 min)

## Acceptance criteria

- [ ] Three monitors live with M11/D18 integration
- [ ] Bridge intents refused in P5
- [ ] Venue cap enforced at the stricter value

## Exceptions & edge cases

- Wallet view stale: concentration uses last good snapshot and marks `stale` (no new blocks lifted).

## Cardinal rules (do NOT)

- Do NOT automate any bridging in P5.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order, including disposal-rule sells, goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §6: bridge allow-list and concentration defaults.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.23 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T027-monitors-venue-bridge-concentration`
- PR title: `P5-T027: Monitors: venue health, bridge policy and concentration`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T027` run

## Progress log

- 2026-10-21 00:00 · planner · created
