---
id: P2-T016
kind: task
title: Venue registry check and 2x crypto-derivatives cap
phase: 2
type: BUILD
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T010]
requirements: [R2.17]
roadmap_todos: [T2.22]
modules: [M11]
dashboards: [D06]
branch: p2/P2-T016-venue-registry-check-2x-cap
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T016 · Venue registry check and 2x crypto-derivatives cap

## Goal / expected outcome

Every order is checked against `ops.venue_registry` (venue × product × residency status) and crypto-derivative leverage is capped at 2× whatever the venue allows; registry changes propagate live via `venue.registry.changed`, and `venue.registry.update` tightens at C1 and allows at C3.

## Context & references

- Roadmap: [R2.17](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.22
- Policy: [12 §2 venue access registry](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) · [12 §1 2× cap](../../../docs/12-policy-and-compliance.md#1-australian-boundary-the-load-bearing-assumption) · [SPEC NN11](../../../SPEC.md#non-negotiable-requirements)
- UI: [D06 Venue registry widget](../../../docs/ui/dashboards/D06-risk.md) · NATS: [02 §6 `venue.registry.changed`](../../../docs/02-v1-architecture.md#6-messaging-nats)
- Cross-phase: table seeded in P0 (R0.06), health fields from P1 (R1.13).
- Related: P2-B008 (paper/testnet semantics).

## Requirements

- Check: `status == allowed` for (venue, entity, product ∈ spot/margin/perps/CFD) under current residency; `read_only`/`blocked` → reject with the registry reason.
- Leverage: `min(policy, registry.max_leverage, ceiling, 2× if crypto derivative)`.
- Concentration cap per venue (default ≤ 25–30% of equity) evaluated with P2-T012.
- Mode semantics: paper/testnet orders follow the rule decided in P2-B008 (default until decided: paper allowed for `read_only`/`blocked` products, flagged `paper_only_venue`).
- `venue.registry.update` command: status tighten (allowed → read_only/blocked) C1; any loosening C3; AUSTRAC check date stale > 90 days → warning in D06.
- Registry cached in-engine; `venue.registry.changed` reload < 1 s; bots on a changed venue get an auto-downgrade signal (P2-T037).

## ToDo

- [ ] `packages/mt_risk/venue.py` check + cache
- [ ] Command handler with classification
- [ ] NATS subscriber for reload
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Rejection tests: Bybit perps (blocked) live order rejected; OKX AU derivatives (unresolved → paper only) rejected live; Binance AU spot allowed.
- Unit: 3× leverage on a crypto perp clamps/rejects to 2× even if registry says 5×.
- Unit: loosening `venue.registry.update` requires C3.

### Scenarios
- Given Kraken AU derivatives `blocked`, when a strategy submits a Kraken futures order, then reject `venue_blocked` with the reason text.
- Given you change a venue to `blocked` mid-session, when the next order arrives (< 1 s later), then it is rejected and bots on that venue downgrade.

### Stress / failure injection
- Publish 100 registry changes/s for 10 s; checks stay < 1 ms p99 and use the latest version.

## Acceptance criteria

- [ ] Every order passes the registry check (bypass test in P2-T052)
- [ ] 2× cap enforced independent of venue settings
- [ ] Live reload < 1 s
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Registry unreachable at start: default-deny.
- Residency change (P3 timeline): registry rows switch with the residency period; until then current residency only.

## Cardinal rules (do NOT)

- Do NOT allow VPN/proxy routing to reach a blocked venue.
- Do NOT trade Polymarket; read-only only.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.

## Doc sync on completion

- `docs/12-policy-and-compliance.md` §2: note the enforced fields and paper semantics.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.22 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T016-venue-registry-check-2x-cap`
- PR title: `P2-T016: Venue registry check and 2x crypto-derivatives cap`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T016` run

## Progress log

- 2026-10-21 00:00 · planner · created
