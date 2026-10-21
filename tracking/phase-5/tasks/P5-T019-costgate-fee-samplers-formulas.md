---
id: P5-T019
kind: task
title: On-chain cost gate: fee samplers and cost formulas
phase: 5
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T016, P5-T018]
requirements: [R5.04]
roadmap_todos: [T5.21]
modules: [M22, M16, M12]
dashboards: [D18]
branch: p5/P5-T019-costgate-fee-samplers-formulas
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T019 · On-chain cost gate: fee samplers and cost formulas

## Goal / expected outcome

`mt_treasury.costgate` computes the all-in cost of any on-chain action from live samples: Solana `C = 5000·n_sig + μ·CU_limit + tip_jito`, EVM `C = gas_used·(baseFee + priorityFee) + L1_data`, constant-product AMM impact, pump.fun bonding-curve impact and the all-in round trip, in native, USD and AUD.

## Context & references

- Roadmap: [R5.04](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.21
- Formulas: [13 §7](../../../docs/13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16)
- Placement gap (cost gate listed under the P6 `treasury` container in 02 §3.2) → P5-B002: built here as a library used by airdrop-exec, signer and mt-api
- Simulation `gas_used` from P5-T016; RPC pools P5-T018; FX from P3 (R3.03)

## Requirements

- Solana μ sampled from `getRecentPrioritizationFees` and Helius `getPriorityFeeEstimate`; Jito tip-floor feed p25–p99; min tip 1,000 lamports; bundles ≤ 5 transactions.
- EVM: `eth_feeHistory` (baseFee, priority percentiles); `gas_used` from the Anvil simulation; L1 data fee from the chain's fee oracle contract (OP-stack `GasPriceOracle` etc.), **never hard-coded**.
- AMM: `Δx = x·Δy(1−φ) / (y + Δy(1−φ))` from pool reserves; pump.fun pre-graduation bonding curve; CEX legs walk the L2 book (P1 data).
- Round trip = entry tx + exit tx + entry/exit impact at size + venue fees + withdrawal fees.
- Samples cached ≤ 15 s; every quote persisted to `ops.costgate_quote` with inputs; Decimal maths.

## ToDo

- [ ] Implement samplers in `packages/mt_treasury/costgate/samplers/` (solana.py, evm.py, jito.py) using the RPC pool.
- [ ] Implement formula module with unit-tested pure functions.
- [ ] Implement quote object + persistence; FX conversion via the P3 FX service.
- [ ] Golden tests from worked examples; property tests (monotonic in size, non-negative).

## Verification

### Tests
- Unit: golden values for each formula (hand-computed examples checked into `tests/golden/costgate/`).
- Property: impact increases monotonically with Δy; cost ≥ 0; tip ≥ 1,000 lamports when Jito used.
- Integration: L1 data fee read from an OP-stack oracle on a fork equals the oracle's `getL1Fee` result.

### Scenarios
- Given Base mainnet after an oracle upgrade, when L1 fee is quoted, then it uses the oracle call, not a constant.
- Given Jito tip-floor feed is down, when a Solana quote is needed, then it uses the last sample ≤ 15 s old or returns `wait`.

### Stress / failure injection
- 1,000 quotes/min from mocks: p95 < 100 ms excluding RPC; cache hit ratio reported.

## Acceptance criteria

- [ ] All 13 §7 formulas implemented with golden tests
- [ ] Quotes persisted with inputs in three currencies
- [ ] No hard-coded L1 fee constants

## Exceptions & edge cases

- RPC fee history unavailable: return `wait` (never guess low).
- Pool reserves stale > 1 block for impact: re-read or `wait`.

## Cardinal rules (do NOT)

- Do NOT use the wallet's gas estimate instead of the simulation `gas_used`.
- Do NOT tip in a separate transaction (12 §4 Jito).
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §7: link the implementation and golden examples.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.21 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T019-costgate-fee-samplers-formulas`
- PR title: `P5-T019: On-chain cost gate: fee samplers and cost formulas`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T019` run

## Progress log

- 2026-10-21 00:00 · planner · created
