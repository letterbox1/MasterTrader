---
id: P7-T037
kind: task
title: cTrader Open API adapter (Linux route)
phase: 7
type: BUILD
status: backlog
priority: medium
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T004]
requirements: [R7.10]
roadmap_todos: [T7.24]
modules: [M12, M16]
dashboards: [D05]
branch: p7/P7-T037-ctrader-open-api-adapter
pr: ""
doc_sync: [docs/03-build-spec.md, docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T037 · cTrader Open API adapter (Linux route)

## Goal / expected outcome

An `mt_engine` adapter for FP Markets' cTrader Open API (protobuf over TLS) provides execution, market data and recon on Linux without the Windows VPS; cancel this task if P7-T004 chose `mt5` only.

## Context & references

- Roadmap: [R7.10 · ToDo T7.24](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §8](../../../docs/14-strategy-evidence-and-validation.md#8-mastertradingbot-integration) (cTrader Open API as the Linux route) · [03 M12](../../../docs/03-build-spec.md#m12-execution--mt_engine) (optional cTrader Open API/FIX) · [12 §6](../../../docs/12-policy-and-compliance.md#6-professional-advice-triggers-tracked-as-tasks-in-d13--d15) (cTrader Open API limits open item)
- Related: P7-T004 (route choice), P7-T030, P7-T025, P7-T051

## Requirements

- OAuth app registered by you (credentials in sops); token refresh handled; scopes trading + accounts only.
- Respect documented rate limits (record them from P7-T004); backoff on throttling.
- Same capabilities as P7-T036: orders with broker-side SL/TP, symbol mapping, fills, swaps/commissions, recon side.
- Licence-clean implementation (own protobuf client generated from the published proto files).

## ToDo

- [ ] Generate protobuf client from published `.proto` (pinned version).
- [ ] Exec/data clients in `packages/mt_engine/adapters/ctrader/`.
- [ ] Recon side adapter.
- [ ] Tests (fake server + demo).
- [ ] Docs.

## Verification

### Tests
- Unit: message encode/decode, symbol mapping, token refresh.
- Integration (cTrader demo): order lifecycle through M11 → journal → TCA → recon.

### Scenarios
- Given an access token expires mid-session, then it refreshes without dropping orders.
- Given a rate-limit error, then requests back off and no retry storm occurs.

### Stress / failure injection
- Socket drop 10× in 10 min: reconnect, resubscribe, unconfirmed → confirmed after recon, no duplicate orders.

## Acceptance criteria

- [ ] Adapter passes demo integration; or task cancelled with reason if route is MT5-only.
- [ ] CI green.

## Exceptions & edge cases

- Different symbol naming between cTrader and MT5 for the same instrument: map both to one `market.instrument`.

## Cardinal rules (do NOT)

- Do NOT use unofficial cTrader endpoints or scraped tokens.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M12: cTrader adapter.
- `docs/14-strategy-evidence-and-validation.md` §8: close the cTrader limits open item.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.24 when this item is done.

## Branch & PR

- Branch: `p7/P7-T037-ctrader-open-api-adapter`
- PR title: `P7-T037: cTrader Open API adapter (Linux route)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T037` run

## Progress log

- 2026-10-21 00:00 · planner · created
