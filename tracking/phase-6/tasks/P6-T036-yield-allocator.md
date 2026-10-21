---
id: P6-T036
kind: task
title: Yield allocator: net apyBase minus amortised gas and risk haircut, within caps
phase: 6
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T033, P6-T035]
requirements: [R6.21, R6.24]
roadmap_todos: [T6.28]
modules: [M22]
dashboards: [D18]
branch: p6/P6-T036-yield-allocator
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T036 · Yield allocator: net apyBase minus amortised gas and risk haircut, within caps

## Goal / expected outcome

The allocator ranks allow-listed pools by **net yield = apyBase − amortised entry/exit gas − risk haircut** and proposes moves for idle stables/LST-eligible assets that respect every cap and the reserve; each proposal carries a cost-gate quote.

## Context & references

- Roadmap: [R6.21](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.24](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.28
- Spec: [13 §4](../../../docs/13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) (net yield formula, ≤ 20% per protocol, per-chain/per-stablecoin caps) · [13 §7](../../../docs/13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16) (cost gate) · [13 §5](../../../docs/13-wallets-treasury-and-onchain.md#5-treasury) (reserve)
- Cross-phase: P5 R5.02 signer, R5.04 cost gate, R5.05 wallet view, R5.06 monitors, R5.07 sweeps, R5.N2 kill freeze; P2 R2.10 M11, R2.19 C3
- Depends on (this phase): P6-T033, P6-T035

## Requirements

- Idle capital = balances above floats + reserve target, from the unified wallet view (P5).
- Gas amortisation: entry + exit cost from the P5 cost gate quote, divided over the expected hold (default 90 days; PT to maturity).
- Constraints: per protocol ≤ 20% of treasury, per chain, per stablecoin, HLP cap, reserve band 20–40% after the move; integer-feasible solution via greedy with cap checks (documented) or small LP.
- Output: `treasury.proposal` rows (from → to, amount, net yield, gate quote, rationale); `auto_ok` only for stablecoin lending within allow-list and caps; everything else becomes an approval task.
- Rebalance only if net improvement ≥ hurdle (default 1.0% APY and ≥ 3× round-trip cost).

## ToDo

- [ ] `mt_treasury.allocator` + proposal table.
- [ ] Gas amortisation using P5 cost gate API.
- [ ] Hurdle logic.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: net yield calc; caps never exceeded (property test over random portfolios); reserve preserved.
- Golden: three fixture portfolios → fixed proposals.

### Scenarios
- Given $10k idle USDC and Aave 4.1% vs Kamino 5.0% with Kamino at its 20% cap, then the proposal fills Aave and respects the cap.
- Given a move whose amortised gas exceeds the yield gain, then no proposal (reason logged).

### Stress / failure injection
- Property test: 10k random portfolios; zero cap/reserve violations.

## Acceptance criteria

- [ ] Proposals respect all caps and reserve.
- [ ] Every proposal has a cost-gate quote.

## Exceptions & edge cases

- Stale yields or stale balances → no proposals.
- Kill switch ON → allocator runs in report-only mode.

## Cardinal rules (do NOT)

- Do NOT use `apyReward` emissions in net yield.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §4: hurdle defaults and solver choice.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.28 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T036-yield-allocator`
- PR title: `P6-T036: Yield allocator: net apyBase minus amortised gas and risk haircut, within caps`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T036` run

## Progress log

- 2026-10-21 00:00 · planner · created
