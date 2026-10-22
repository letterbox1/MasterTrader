---
id: P5-T016
kind: task
title: Simulation hooks: Anvil fork and simulateTransaction with balance-diff analysis
phase: 5
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T014, P5-T015]
requirements: [R5.02, R5.15, R5.16]
roadmap_todos: [T5.20]
modules: [M22, M4]
dashboards: [D12]
tools: [uv, docker, anvil, solana-test-validator]
mcp: []
env: []
services: [anvil]
branch: p5/P5-T016-signer-simulation-hooks
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

# P5-T016 · Simulation hooks: Anvil fork and simulateTransaction with balance-diff analysis

## Goal / expected outcome

Before every signature the signer simulates the exact transaction (EVM: local **Anvil** mainnet fork at the latest block; Solana: `simulateTransaction` with account snapshots) and a diff analyser asserts the only effects are "+expected tokens to me, −gas" (or the intent's declared effect). The diff is stored with the exec log and shown in D12.

## Context & references

- Roadmap: R5.02 (mandatory simulation) · ToDo T5.20 · testnet proof P5-T056
- [13 §2](../../../docs/13-wallets-treasury-and-onchain.md#2-signer-service-the-only-process-that-sees-hot-keys) (Anvil fork and `simulateTransaction` are the only simulators; simulation is a sanity check only)
- [08 autonomous claim conditions](../../../docs/08-airdrops-and-token-launches.md#what-may-run-autonomously) · Tenderly is not used (decision P5-B013, [17 §D](../../../docs/17-decisions-register.md#d-other-decisions))

## Requirements

- EVM: `anvil --fork-url <pool RPC> --fork-block-number <latest>` (CI: a keyless public endpoint or a pinned `anvil --load-state` dump; no API key); run tx via `eth_call` + `debug_traceCall`/state diff; collect ERC-20/721/1155 Transfer and Approval logs, native balance deltas, storage writes to token contracts.
- Solana: `simulateTransaction` with `accounts` config for all writable accounts; diff pre/post token balances and owners/authorities/delegates.
- Pass rule per intent: `claim` → only inflows of the expected token(s) to the wallet and a gas/fee outflow; **any** other outflow, new approval/delegate, authority change or call to an unexpected contract fails.
- `gas_used` from the simulation is returned to the cost gate (not the wallet estimate).
- Simulation digest (diff JSON + sha256) attached to the ledger and exec log; D12 renders "+X tokens, −gas, no other state change".
- Timeout 10 s; failure or timeout = refuse (fail closed).

## ToDo

- [ ] Implement `mt_signer/simulate/evm_anvil.py` (Anvil process manager talking to the `anvil` container) and `solana_sim.py`.
- [ ] Implement `diff.py` normaliser and per-intent pass rules.
- [ ] Add golden fixtures: clean Merkle claim; claim that also transfers another token out; claim that sets approval; Solana claim that changes delegate.
- [ ] Expose digest to exec log and D12.

## Verification

### Tests
- Integration: Anvil fork of a public testnet/mainnet block with a known Merkle distributor → pass; with a malicious mock distributor that pulls USDC → fail.
- Integration: `solana-test-validator` program that changes a token delegate on claim → fail.
- Unit: diff normaliser golden tests.

### Scenarios
- Given a token that behaves differently when `tx.origin` is a fork, when simulation passes but caps limit loss, then caps + burner-first remain the backstop (documented).
- Given Anvil is down, when a claim is requested, then it is refused `simulation_unavailable` and becomes a `CLAIM_MANUAL` task.

### Stress / failure injection
- 20 parallel simulations: p95 < 5 s on the target host; Anvil memory bounded (restart if > 2 GB).

## Acceptance criteria

- [ ] Every signature path calls simulation; fail-closed on error
- [ ] Diff rules reject any non-gas outflow or approval change
- [ ] Digest visible in exec log/D12

## Exceptions & edge cases

- Fork RPC rate-limited: use the pool fallback (P5-T018); never skip simulation.
- Block reorg between simulation and broadcast: resimulate if > 2 blocks old.

## Cardinal rules (do NOT)

- Do NOT accept raw or pre-built transactions, raw messages or typed-data payloads from any caller — intents only; the signer re-builds and re-decodes everything itself (13 §2).
- Do NOT log, print, serialise to NATS or persist private keys anywhere except OpenBao/sops; keys are never in `.env`.
- Do NOT treat a passing simulation as proof of safety; caps and hard blocks still apply.
- Do NOT commit secrets or paste them into chats, issues or logs; secrets live only in the sops/age file or OpenBao (07 §2).
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §2: document the diff pass rules.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.20 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T016-signer-simulation-hooks`
- PR title: `P5-T016: Simulation hooks: Anvil fork and simulateTransaction with balance-diff analysis`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T016` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (Anvil/simulateTransaction only, Tenderly not used per P5-B013; keyless CI fork)
