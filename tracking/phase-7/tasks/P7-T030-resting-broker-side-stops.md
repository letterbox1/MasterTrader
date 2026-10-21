---
id: P7-T030
kind: task
title: Resting broker-side stops on every live position
phase: 7
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.11]
roadmap_todos: [T7.41]
modules: [M12, M11]
dashboards: [D05]
branch: p7/P7-T030-resting-broker-side-stops
pr: ""
doc_sync: [docs/07-security-notes.md, docs/03-build-spec.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T030 · Resting broker-side stops on every live position

## Goal / expected outcome

Every live position has a resting stop order held **at the venue/broker** (native stop or OCO), so a host, power or link failure never leaves a position unprotected; positions on venues without native stops are refused for live trading.

## Context & references

- Roadmap: [R7.11 · ToDo T7.41](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [07 §5](../../../docs/07-security-notes.md#5-network--host) (resting broker-side stops cover the gap) · [14 §4](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) (ATR-scaled stops, exit plan fixed at entry) · [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) (broker-side limits as a second line) · [03 M12](../../../docs/03-build-spec.md#m12-execution--mt_engine)
- Related: P7-T033 (fail-flat), P7-T052, P7-T053

## Requirements

- On every live entry fill: place a venue-native stop (stop-market or stop-limit with a protective limit offset) at the exit-plan stop; re-place on partial fills; trail by amending the resting order (rate-limit aware).
- If the stop cannot be placed within 5 s: flatten the position (protective, no approval) and alert.
- Venue capability flag in `ops.venue_registry` (`native_stops: yes/no`); M11 rejects live entries where `no`.
- Recon (P7-T025) checks that each live position has a matching resting stop; missing stop = unexplained break.
- STP mode sent explicitly on stop orders too.

## ToDo

- [ ] Stop manager in `packages/mt_engine/protection/` per adapter (ccxt AU spot venues, OANDA/IG, MT5/cTrader).
- [ ] Registry capability flag + M11 check.
- [ ] Recon rule `missing_resting_stop`.
- [ ] Tests; docs.

## Verification

### Tests
- Integration (testnet/practice): entry → resting stop visible via venue REST; partial fill → stop quantity matches position.
- Integration: simulated stop placement failure → position flattened within 5 s + alert.
- Unit: trailing amend respects venue rate limits.

### Scenarios
- Given the host loses power with an open BTC position, then the venue still holds the stop and the position is protected.
- Given a venue without native stops, then live entries there are rejected with `no_native_stops`.

### Stress / failure injection
- Amend storm during volatile moves: amendments throttled to venue limits; never cancel-then-replace leaving a gap (use amend or place-new-then-cancel-old).

## Acceptance criteria

- [ ] 100% of live positions in recon have a resting stop.
- [ ] Failure to place → flatten + alert within 5 s.
- [ ] CI green.

## Exceptions & edge cases

- Spot venues without stop orders (some AU spot venues): mark `native_stops: no` → not eligible for live.
- Weekend FX: broker-side stop persists; gap risk noted in the runbook.

## Cardinal rules (do NOT)

- Do NOT hold stops only in the engine for live positions.
- Do NOT cancel a resting stop before its replacement is acknowledged.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.

## Doc sync on completion

- `docs/07-security-notes.md` §5: resting-stop rule.
- `docs/03-build-spec.md` M12: stop manager.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.41 when this item is done.

## Branch & PR

- Branch: `p7/P7-T030-resting-broker-side-stops`
- PR title: `P7-T030: Resting broker-side stops on every live position`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T030` run

## Progress log

- 2026-10-21 00:00 · planner · created
