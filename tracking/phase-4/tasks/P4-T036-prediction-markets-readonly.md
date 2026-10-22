---
id: P4-T036
kind: task
title: Polymarket and Kalshi read-only probability clients (lawful reach only)
phase: 4
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010, P2-T120]
requirements: [R4.09, R4.11]
roadmap_todos: [T4.25, T4.32]
modules: [M3, M6]
dashboards: [D08]
tools: [uv, git]
mcp: []
env: []
services: [postgres, nats]
branch: p4/P4-T036-prediction-markets-readonly
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/06-aggregators-and-market-providers.md, docs/roadmap/phase-4-intel.md]
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

# P4-T036 · Polymarket and Kalshi read-only probability clients (lawful reach only)

## Goal / expected outcome

Read-only httpx clients pull public market probabilities from Kalshi (`api.elections.kalshi.com/trade-api/v2`, no auth) and, **only if lawfully reachable without VPN/proxy**, Polymarket (Gamma + CLOB public reads), for macro/event markets (Fed decision, CPI, NFP, GDP, recession), storing probability series for M3 events and M6 features. There is no trading code path at all.

## Context & references

- Roadmap: [R4.09, R4.11](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.25](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Policy: [12 §1 Polymarket](../../../docs/12-policy-and-compliance.md#1-australian-boundary-the-load-bearing-assumption) (ACMA warning 2 Jul 2025, ISP block 13 Aug 2025; never via VPN/proxy; Kalshi read-only)
- Providers: [06 §3 prediction markets](../../../docs/06-aggregators-and-market-providers.md#3-additional-forex--multi-asset-providers) (official Kalshi library has a proprietary licence → httpx)
- Verified by P4-T056 (config review). Also feeds the D02 positioning widget (P4-T065, roadmap T4.32).
- Cross-phase: P2-T120 (feature registry) is a `depends_on` entry; the venue registry rows (`read_only`) come from P0-T025/P0-T026.

## Requirements

- Config `config/intel/prediction_markets.yaml`: `polymarket.enabled` default **false** while residency = AU; reachability check is a direct request from the host's normal route; any proxy/VPN env var present → refuse to start.
- No order, wallet, signing or auth code; CI grep check forbids `order`, `sign`, `private_key` symbols in the module.
- Markets list per series (ticker/slug), poll every 5 min; store mid/last probability, volume, open interest as `features.value` `pm.{market}`.
- Large moves (> 10 pp in 1 h) create `geo_event` kind `pm_move`.
- Venue registry (`ops.venue_registry`) marks Polymarket/Kalshi as `read_only`; M11 rejects any intent to them (already by registry).

## ToDo

- [ ] Kalshi client + market mapping.
- [ ] Polymarket client behind the lawful-reach guard.
- [ ] Proxy/VPN env guard + CI symbol check.
- [ ] Feature writer + `pm_move` events.
- [ ] Tests.

## Verification

### Tests
- Unit: proxy env set → client refuses to start.
- CI: forbidden-symbol grep passes.
- Unit: fixture → probability series; 12 pp move → `pm_move` event.

### Scenarios
- Given residency AU and Polymarket returns a block page, then the source is disabled with reason 'not lawfully reachable'.
- Given residency changes (12 §1), then the flag must be re-reviewed (task created, not auto-enabled).

### Stress / failure injection
- n/a: low volume.

## Acceptance criteria

- [ ] Kalshi probabilities flowing; Polymarket disabled for AU unless lawfully reachable
- [ ] No trading code path (CI check)
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Kalshi market tickers roll (new contracts per meeting): mapping resolves the next-dated contract automatically.

## Cardinal rules (do NOT)

- Do NOT use a VPN, proxy or alternate DNS to reach Polymarket.
- Do NOT add any order/wallet code for prediction markets.
- Do NOT touch live money (P7 gates); keys stay trade-only, IP-locked, withdrawals disabled.
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/12-policy-and-compliance.md`: §1: note the implemented guard
- `docs/06-aggregators-and-market-providers.md`: §3 prediction markets: markets tracked
- `docs/roadmap/phase-4-intel.md`: tick T4.25 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T036-prediction-markets-readonly`
- PR title: `P4-T036: Polymarket and Kalshi read-only probability clients (lawful reach only)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T036` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (also mapped to new roadmap ToDo T4.32 (prediction-market probabilities for D02); explicit depends_on P2-T120)
