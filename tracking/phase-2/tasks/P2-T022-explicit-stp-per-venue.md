---
id: P2-T022
kind: task
title: Explicit self-trade prevention on every order
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T021, P2-T016]
requirements: [R2.31]
roadmap_todos: [T2.25]
modules: [M12]
dashboards: []
branch: p2/P2-T022-explicit-stp-per-venue
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

# P2-T022 · Explicit self-trade prevention on every order

## Goal / expected outcome

Every order leaves the engine with an explicit, venue-correct STP parameter (never the venue default), chosen by rule (cancel-both for strategies sharing an account, cancel-taker for market-making legs), and STP cancels are recorded as non-fills for reconciliation.

## Context & references

- Roadmap: [R2.31](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.25
- Policy: [12 §3 STP table](../../../docs/12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention) · [12 §2 registry STP field](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) · [14 §4 explicit STP when sharing an account](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06)
- Related: P2-B006 (venues without STP), P2-T056 STP audit.

## Requirements

- STP map from `ops.venue_registry` (`stp_param`, allowed modes): OKX `stpMode` (cancel_maker/cancel_taker/cancel_both, not with FOK), Binance `selfTradePreventionMode` (EXPIRE_TAKER/MAKER/BOTH, read per symbol from exchangeInfo), Kraken `stptype`/`stp_type`, BTC Markets `selfTrade: P`.
- Mode rule: default cancel-both; MM legs cancel-taker; per-account override in policy.
- Engine-side self-cross guard for venues without a native STP parameter (Alpaca, OANDA, IG, IBKR): block an order that would cross a resting own order on the same account; record `stp_mode=engine_guard`.
- If a venue/symbol doesn't support the chosen mode (e.g. OKX + FOK): reject before submit, never fall back to default.
- Venue STP cancel events → `audit.order` status `stp_cancelled`, `fill_qty=0`, tagged for recon (`recon_tag=stp`).

## ToDo

- [ ] `packages/mt_engine/stp.py` (resolver + guard)
- [ ] Adapter hook so every venue client sets the param (Nautilus `params`/tags)
- [ ] Status mapping for STP cancels per venue
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: resolver returns the right param/value per venue × order type; FOK + OKX cancel_both rejected.
- Unit: engine guard blocks a crossing order on Alpaca paper.
- Integration (Binance testnet): order payload contains `selfTradePreventionMode`.

### Scenarios
- Given two strategies on one Binance testnet account, when their orders would match, then the venue expires both per EXPIRE_BOTH and both are recorded as non-fills.
- Given an IG order that would cross own resting order, when submitted, then the engine guard rejects it with `self_cross_guard`.

### Stress / failure injection
- n/a: deterministic mapping; covered by the STP audit (P2-T056).

## Acceptance criteria

- [ ] No order path without an explicit STP decision (unit test enumerates all venues)
- [ ] STP cancels recorded as non-fills
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- exchangeInfo unavailable: use last cached symbol STP modes; none cached → reject.
- Venue changes allowed modes: registry update + alert.

## Cardinal rules (do NOT)

- Do NOT leave STP to the venue default.
- Do NOT self-match across sub-accounts (12 §3).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.

## Doc sync on completion

- `docs/12-policy-and-compliance.md` §3: add Alpaca/OANDA/IG/IBKR engine-guard rows (with P2-B006).
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.25 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T022-explicit-stp-per-venue`
- PR title: `P2-T022: Explicit self-trade prevention on every order`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T022` run

## Progress log

- 2026-10-21 00:00 · planner · created
