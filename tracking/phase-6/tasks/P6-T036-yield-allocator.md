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
depends_on: [P6-T033, P6-T035, P5-T020, P5-T022]
requirements: [R6.21, R6.24]
roadmap_todos: [T6.28]
modules: [M22]
dashboards: [D18]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [postgres]
branch: p6/P6-T036-yield-allocator
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/16-configuration-and-safety-model.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T036 · Yield allocator: net apyBase minus amortised gas and risk haircut, within caps

## Goal / expected outcome

The allocator ranks allow-listed pools by **net yield = apyBase − amortised entry/exit gas − risk haircut** and proposes moves for idle stables/LST-eligible assets that respect every cap and the reserve; each proposal carries a cost-gate quote.

## Context & references

- Roadmap: [R6.21](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.24](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.28
- Spec: [13 §4](../../../docs/13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) (net yield formula, ≤ 20% per protocol, per-chain/per-stablecoin caps) · [13 §7](../../../docs/13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16) (cost gate) · [13 §5](../../../docs/13-wallets-treasury-and-onchain.md#5-treasury) (reserve)
- Cross-phase: P5-T020 (`mt_onchain.costgate` verdicts), P5-T022 (wallet-indexer balances); M11 via P6-T033/P2-T017
- Defaults: [16 §2.7](../../../docs/16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13) (per-protocol ≤ 20%, HLP cap, cost-gate margin 2×)
- Depends on (this phase): P6-T033, P6-T035

## Requirements

- Idle capital = balances above floats + reserve target, from the unified wallet view (P5).
- Gas amortisation: entry + exit cost from the P5 cost gate quote, divided over the expected hold (default 90 days; PT to maturity).
- Constraints (policy values from P6-T033; defaults 16 §2.7 / 13 §5): per protocol ≤ 20% of treasury, per chain, per stablecoin, HLP cap (≤ 10% of stables and ≤ 5% of portfolio, whichever is smaller), reserve band 20–40% after the move; integer-feasible solution via greedy with cap checks (documented) or small LP.
- Output: `treasury.proposal` rows (from → to, amount, net yield, gate quote, rationale); `auto_ok` only for stablecoin lending within allow-list and caps; everything else becomes an approval task.
- Rebalance only if net improvement ≥ hurdle (default 1.0% APY, a setting proposed for 16 §2.7) **and** the cost gate allows it (expected benefit ≥ 2× all-in cost, 16 §2.7).

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
- `docs/16-configuration-and-safety-model.md` §2.7: add the rebalance hurdle as a default.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.28 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T036-yield-allocator`
- PR title: `P6-T036: Yield allocator: net apyBase minus amortised gas and risk haircut, within caps`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T036` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (caps/HLP/cost-gate margin from 16 §2.7 (hurdle as a setting, gate 2× instead of an extra 3×); cross-phase deps P5-T020/P5-T022; run fields)
