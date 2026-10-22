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
depends_on: [P5-T018, P3-T010]
requirements: [R5.04]
roadmap_todos: [T5.21]
modules: [M22, M16, M12]
dashboards: [D18]
tools: [uv, anvil]
mcp: []
env: []
services: [anvil]
branch: p5/P5-T019-costgate-fee-samplers-formulas
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T019 · On-chain cost gate: fee samplers and cost formulas

## Goal / expected outcome

`mt_onchain.costgate` (the one cost-gate library, [13 §7](../../../docs/13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16)) computes the all-in cost of any on-chain action from live samples: Solana `C = 5000·n_sig + μ·CU_limit + tip_jito`, EVM `C = gas_used·(baseFee + priorityFee) + L1_data`, constant-product AMM impact, pump.fun bonding-curve impact and the all-in round trip, in native, USD and AUD.

## Context & references

- Roadmap: [R5.04](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.21
- Formulas: [13 §7](../../../docs/13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16)
- Placement (decision P5-B002, [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)): one library, `mt_onchain.costgate` ([02 §3.2](../../../docs/02-v1-architecture.md#32-containers) library row; [03 §3](../../../docs/03-build-spec.md#3-repository-layout) layout), used by the signer path from P5 and by the P6 treasury
- Live inputs, never constants ([16 §4.3](../../../docs/16-configuration-and-safety-model.md#43-live-inputs-instead-of-constants)): `eth_feeHistory`, `getRecentPrioritizationFees`, Helius fee estimate, Jito tip floor
- Simulation `gas_used` from P5-T016; RPC pools P5-T018; FX from P3 (R3.03)

## Requirements

- Solana μ sampled from `getRecentPrioritizationFees` and Helius `getPriorityFeeEstimate`; Jito tip-floor feed p25–p99; min tip 1,000 lamports; bundles ≤ 5 transactions.
- EVM: `eth_feeHistory` (baseFee, priority percentiles); `gas_used` from the Anvil simulation; L1 data fee from the chain's fee oracle contract (OP-stack `GasPriceOracle` etc.), **never hard-coded**.
- AMM: `Δx = x·Δy(1−φ) / (y + Δy(1−φ))` from pool reserves; pump.fun pre-graduation bonding curve; CEX legs walk the L2 book (P1 data).
- Round trip = entry tx + exit tx + entry/exit impact at size + venue fees + withdrawal fees.
- Samples cached ≤ 15 s; every quote persisted to `ops.costgate_quote` with inputs; Decimal maths.

## ToDo

- [ ] Implement samplers in `packages/mt_onchain/costgate/samplers/` (solana.py, evm.py, jito.py) using the RPC pool.
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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (library renamed `mt_onchain.costgate` per P5-B002; live inputs per 16 §4.3; deps trimmed to RPC pool + P3 FX)
