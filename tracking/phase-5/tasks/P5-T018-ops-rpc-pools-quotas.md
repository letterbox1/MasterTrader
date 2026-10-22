---
id: P5-T018
kind: task
title: RPC provider pools, fallbacks and per-provider quota trackers
phase: 5
type: OPS
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T006]
requirements: [R5.05, R5.04, R5.12]
roadmap_todos: [T5.41]
modules: [M22, M4, M16]
dashboards: [D07]
tools: [uv, docker]
mcp: []
env: []
services: []
branch: p5/P5-T018-ops-rpc-pools-quotas
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

# P5-T018 · RPC provider pools, fallbacks and per-provider quota trackers

## Goal / expected outcome

`mt_core.rpc` exposes per-chain RPC pools (Solana: Helius → Chainstack/QuickNode → PublicNode; EVM: Alchemy → Infura/PublicNode; own Blockscout API) with per-provider quota tracking that throttles before free limits, health probes and failover, used by indexer, enrichment, cost gate and simulation.

## Context & references

- Roadmap: ToDo T5.41 → R5.05 · [13 §7 RPC](../../../docs/13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16)
- Quota tracker framework from P1 (T1.25 / R1.08); [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) RPC rules
- Build first, keys last ([17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)): built and tested against mocked providers, Anvil, `solana-test-validator` and keyless public endpoints (PublicNode) with recorded fixtures; real keys (P0-T010, P5-T003) are read by name only at runtime (`HELIUS_API_KEY`, `ALCHEMY_API_KEY`, fallbacks) and first exercised in P5-T068

## Requirements

- Budgets: Helius 1M credits/month and 10 rps; Alchemy 30M CU/month; The Graph 100k queries/month (if used); PublicNode low-volume fallback only (no production traffic, no IP rotation).
- Throttle at 80% of each daily-prorated budget; alert at 90%; never exceed (thresholds configurable).
- Spread load across **different** providers; never multiple accounts on one provider.
- Failover on 5xx/timeouts with circuit breaker (default 5 errors in 60 s → provider paused 10 min, configurable; [16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)).
- Quota usage visible in D07 quota panel.

## ToDo

- [ ] Implement `packages/mt_core/rpc/pool.py` with provider adapters, credit-cost tables per method, circuit breaker.
- [ ] Register budgets in the P1 quota tracker; Grafana panel + alerts.
- [ ] Health probe Prefect flow every 5 min (block height freshness).
- [ ] Tests with mocked providers; doc sync.

## Verification

### Tests
- Unit: credit accounting per method (e.g. Helius DAS costs) matches the table.
- Unit: circuit breaker opens after 5 errors/min and closes after 10 min.
- Integration: probes against keyless public endpoints and local nodes; the live keyed probe is P5-T068.

### Scenarios
- Given Helius returns 429, when the indexer asks for balances, then the pool fails over to the fallback and records the event.
- Given 80% of the Alchemy daily share is used, when enrichment requests more, then low-priority jobs are deferred.

### Stress / failure injection
- Simulated 3× normal load for 1 h against mocks: no budget overrun; priority order claims/simulation > indexer > enrichment.

## Acceptance criteria

- [ ] Pools configured for EVM and Solana with fallbacks
- [ ] Quotas throttle before limits and show in D07
- [ ] Circuit breaker tested

## Exceptions & edge cases

- All providers down: signer/executor fail closed; indexer marks balances `stale` (D18 amber).

## Cardinal rules (do NOT)

- Do NOT create second accounts or rotate IPs to beat limits (12 §4).
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.
- Do NOT commit secrets or paste them into chats, issues or logs; secrets live only in the sops/age file or OpenBao (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §7: record the chosen fallbacks and priorities.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.41 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T018-ops-rpc-pools-quotas`
- PR title: `P5-T018: RPC provider pools, fallbacks and per-provider quota trackers`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T018` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keyless build: no dependency on P5-T003 keys, live probe moved to P5-T068; RPC error pause per 16 §2.1; P1 quota tracker dep)
