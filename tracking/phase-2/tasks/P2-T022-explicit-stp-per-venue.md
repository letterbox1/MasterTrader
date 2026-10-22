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
tools: [uv]
mcp: []
env: []
services: []
branch: p2/P2-T022-explicit-stp-per-venue
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T022 · Explicit self-trade prevention on every order

## Goal / expected outcome

Every order to a venue with an STP field leaves the engine with an explicit, venue-correct STP parameter (never the venue default), chosen by rule (cancel-both for strategies sharing an account, cancel-taker for market-making legs); netting brokers (OANDA, IG, Alpaca, IBKR) are marked `stp: n/a (netting)` in the venue registry and run one strategy per account/sub-account where netting would merge bots; STP cancels are recorded as non-fills for reconciliation.

## Context & references

- Roadmap: [R2.31](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.25
- Policy: [12 §3 STP table](../../../docs/12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention) · [12 §2 registry STP field](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) · [14 §4 explicit STP when sharing an account](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06)
- Decision: [17 §D P2-B006](../../../docs/17-decisions-register.md#d-other-decisions) (netting brokers have no STP field → `stp: n/a (netting)`; one strategy per account/sub-account where netting would merge bots) · [12 §3 netting row](../../../docs/12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention)
- Related: P2-T056 STP audit, P2-T036 (bot creation validates the netting-account rule), P2-T071 (live STP behaviour on testnet with your keys).

## Requirements

- STP map from `ops.venue_registry` (`stp_param`, allowed modes): OKX `stpMode` (cancel_maker/cancel_taker/cancel_both, not with FOK), Binance `selfTradePreventionMode` (EXPIRE_TAKER/MAKER/BOTH, read per symbol from exchangeInfo), Kraken `stptype`/`stp_type`, BTC Markets `selfTrade: P`.
- Mode rule: default cancel-both; MM legs cancel-taker; per-account override in policy.
- Netting brokers (OANDA, IG, Alpaca, IBKR): registry `stp: n/a (netting)`; no STP field is sent and `audit.order.stp_mode = n/a_netting` is recorded. The engine refuses to start (and bot creation rejects) a configuration where two bots of different strategies share one netting account/sub-account on overlapping instruments (`netting_account_shared`).
- If a venue/symbol doesn't support the chosen mode (e.g. OKX + FOK): reject before submit, never fall back to default.
- Venue STP cancel events → `audit.order` status `stp_cancelled`, `fill_qty=0`, tagged for recon (`recon_tag=stp`).

## ToDo

- [ ] `packages/mt_engine/stp.py` (resolver from the registry `stp` column + netting-account rule check)
- [ ] Adapter hook so every venue client sets the param (Nautilus `params`/tags)
- [ ] Status mapping for STP cancels per venue
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: resolver returns the right param/value per venue × order type; FOK + OKX cancel_both rejected.
- Unit: Alpaca/OANDA/IG/IBKR orders carry no STP field and record `stp_mode=n/a_netting`; a second strategy's bot on the same OANDA practice account with an overlapping instrument → `netting_account_shared`.
- Integration (recorded Binance testnet fixtures / mock venue, no keys): order payload contains `selfTradePreventionMode`.

### Scenarios
- Given two strategies on one Binance account (mock venue replaying recorded EXPIRE_BOTH responses), when their orders would match, then both are recorded as non-fills (`stp_cancelled`, `recon_tag=stp`).
- Given a second strategy's bot is configured on the IG demo account already used by another strategy for the same instrument, when the engine loads the config, then it refuses with `netting_account_shared` (one strategy per account/sub-account).

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

- `docs/12-policy-and-compliance.md` §3: confirm the netting-broker row (`stp: n/a (netting)`) and the one-strategy-per-account check as built.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.25 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T022-explicit-stp-per-venue`
- PR title: `P2-T022: Explicit self-trade prevention on every order`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T022` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (netting brokers stp: n/a (netting) + one strategy per account (17 §D P2-B006) replaces the engine guard; keyless fixtures)
