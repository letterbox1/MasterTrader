---
id: P2-T025
kind: task
title: OANDA v20 practice adapter
phase: 2
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T022, P2-T001]
requirements: [R2.30, R2.31, R2.32]
roadmap_todos: [T2.25]
modules: [M12]
dashboards: []
branch: p2/P2-T025-oanda-v20-adapter
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T025 · OANDA v20 practice adapter

## Goal / expected outcome

A Nautilus live data + execution client for **OANDA v20** in `packages/mt_engine/adapters/` lets strategies trade the OANDA v20 practice/paper account through the same engine path (M11 gate, explicit STP decision, epoch client IDs, reconciliation).

## Context & references

- Roadmap: [R2.30](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.25
- Spec: [03 M12 custom adapters](../../../docs/03-build-spec.md#m12-execution--mt_engine) · [12 §2 registry row](../../../docs/12-policy-and-compliance.md#2-venue-access-registry)
- Cross-phase: P1 data streams for this venue (R1.04/R1.05) and read-only recon (R1.12) — reuse their clients/parsers.
- Related: P2-T001 keys, P2-T022 STP, P2-T027 IDs/reconcile, P2-T057 conformance tests.

## Requirements

- OANDA v20 practice REST (`/v3/accounts/{id}/orders`, `/trades`, `/positions`, `/transactions`) + transaction stream; pricing stream stays with P1.
- Units-based sizing (FX), `clientExtensions.id` = client order id; stop-loss/take-profit on fill; financing transactions forwarded to M16.
- No native STP: engine self-cross guard; `stp_mode=engine_guard`.
- Hedging vs netting account mode read at start and recorded.
- Implements Nautilus `LiveExecutionClient`: submit/modify/cancel, order status reports, fill reports, position reports (`generate_order_status_reports`, `generate_fill_reports`, `generate_position_status_reports`) for restart reconciliation.
- Maps `client_order_id` to the venue's client reference field; maps venue errors to Nautilus rejects with reason text.
- Rate limits read from response headers where available; backoff with jitter; never retry a submit without checking status by client id first.
- Secrets read from tmpfs (sops) via `mt_core.config`; keys never logged.

## ToDo

- [ ] Implement client + config + instrument provider
- [ ] Order/fill/position report mapping
- [ ] Recorded HTTP/WS cassettes for CI (no live keys in CI)
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: payload mapping per order type (market, limit, stop, stop-limit, brackets where supported).
- Integration (CI, cassettes): submit → ack → fill → report round-trip; cancel; reject mapping.
- Manual/nightly: live practice-account smoke via P2-T057.

### Scenarios
- Given a limit order on OANDA v20 practice, when filled partially then cancelled, then audit shows one order, one partial fill, cancel status, all with the same client id.
- Given the stream disconnects, when reconnected, then missed fills are fetched via reports before new orders are allowed.

### Stress / failure injection
- Disconnect the network for 30 s mid-order: orders marked `unknown`, then reconciled; no duplicate submit.

## Acceptance criteria

- [ ] Adapter passes cassette tests in CI
- [ ] Reports support restart reconciliation
- [ ] No secret appears in logs (log scrubber test)
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Venue maintenance windows: adapter reports `venue_unavailable`; gate holds orders.
- Practice account resets balance: recon flags an incident, not an auto-fix.

## Cardinal rules (do NOT)

- Do NOT hard-code keys or account ids.
- Do NOT add broker/referral IDs to requests.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.
- Pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M12: mark the OANDA v20 adapter as implemented (paper/practice) with known limits.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.25 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T025-oanda-v20-adapter`
- PR title: `P2-T025: OANDA v20 practice adapter`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T025` run

## Progress log

- 2026-10-21 00:00 · planner · created
