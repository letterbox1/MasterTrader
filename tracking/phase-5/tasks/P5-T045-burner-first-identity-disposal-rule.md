---
id: P5-T045
kind: task
title: Burner-first and identity flow, genuine-use tasks and disposal-rule orders via M11
phase: 5
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T044, P5-T029]
requirements: [R5.17, R5.15]
roadmap_todos: [T5.28]
modules: [M4, M11, M19, M22]
dashboards: [D12, D13]
branch: p5/P5-T045-burner-first-identity-disposal-rule
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T045 · Burner-first and identity flow, genuine-use tasks and disposal-rule orders via M11

## Goal / expected outcome

New or untrusted dApp interactions always run first from a **burner** with minimal float; only after a clean burner run does a task move to the chain's **identity** wallet (one per chain), optionally as a `GENUINE_USE` task under a mandate with caps; on any claim the **disposal rule** (default sell 50%) creates an order through M11, or a manual sell task when no allowed venue path exists.

## Context & references

- Roadmap: [R5.17](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md), R5.15 · ToDo T5.28 · USER P5-T007
- [08 wallet discipline](../../../docs/08-airdrops-and-token-launches.md#wallet-discipline) · [13 §1 rules](../../../docs/13-wallets-treasury-and-onchain.md#1-custody-tiers) · [03 M4 genuine-use](../../../docs/03-build-spec.md#m4-airdrops-token-launches--icos--mt_airdrop)
- Disposal execution path gap (no DEX path until P7) → P5-B010

## Requirements

- Burner run: a burner-scoped mandate (tiny caps) for the specific contract/function; record `burner_run` result (simulation + on-chain effects, approvals created/revoked); clean = no unexpected outflows, approvals revoked, contract unchanged.
- Promotion: only after a clean burner run may the opportunity propose identity-wallet tasks; the identity wallet is never used for memecoin churn or unvetted contracts.
- `GENUINE_USE`: real, modest usage sized to genuine use (swap/stake/LP/vote) — no dust loops, volume farming or wash trading; every step is the user's click unless it is a plain claim.
- Disposal rule: after a claim finalises, compute sell qty = disposal% × received; create an `OrderIntent` (sleeve `airdrop`) through M11 on an allowed venue if the token is listed there; else create `ONCHAIN_ACTION_MANUAL` "sell X% via …" task with cost-gate estimate; remainder held under M22 rules.
- Per-campaign single-wallet constraint (NA-09).

## ToDo

- [ ] Implement `packages/mt_airdrop/flows/burner.py`, `identity.py`, `disposal.py`.
- [ ] M11 integration: `airdrop` sleeve with its own limits; order via `mt_api` `order.place` internal path.
- [ ] Task templates for GENUINE_USE and manual sell; tests; doc sync.

## Verification

### Tests
- Integration: burner run with a mock dApp that leaves an approval → not clean → no identity task; approval revoked.
- Integration: claim of a token listed on an allowed CEX → M11 receives an OrderIntent for 50% (paper/testnet venue).
- Unit: token not on any allowed venue → manual sell task with numbers.

### Scenarios
- Given a clean burner run on protocol P, then a GENUINE_USE task appears for the identity wallet with caps and steps.
- Given M11 rejects the disposal order (venue blocked), then a manual task is created and the reason shown in D12.

### Stress / failure injection
- n/a: per-claim flow (load covered by P5-T062)

## Acceptance criteria

- [ ] Burner-first enforced before identity tasks
- [ ] Disposal orders go through M11 or become manual tasks
- [ ] No identity-wallet use for unvetted contracts

## Exceptions & edge cases

- Burner float insufficient for the run: refill via sweeps module (to float only), else task.

## Cardinal rules (do NOT)

- Do NOT place disposal orders outside M11 or before P7 gates on live venues (paper/testnet or manual only in P5).
- Do NOT propose dust loops or volume farming as genuine use.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order, including disposal-rule sells, goes through M11.
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.
- Do NOT move value outside the configured caps/floats; exchange keys stay read-only or trade-only, IP-locked, withdrawals disabled; no live trading before the P7 gates.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: burner-clean criteria and disposal fallbacks.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.28 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T045-burner-first-identity-disposal-rule`
- PR title: `P5-T045: Burner-first and identity flow, genuine-use tasks and disposal-rule orders via M11`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T045` run

## Progress log

- 2026-10-21 00:00 · planner · created
