---
id: P5-T014
kind: task
title: Signer EVM plug-in: builders, decoders and hard blocks
phase: 5
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T013]
requirements: [R5.02, R5.03, R5.16]
roadmap_todos: [T5.20]
modules: [M22]
dashboards: []
branch: p5/P5-T014-signer-evm-builders-hard-blocks
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

# P5-T014 · Signer EVM plug-in: builders, decoders and hard blocks

## Goal / expected outcome

The EVM chain plug-in builds every allowed transaction itself from the intent (Merkle `claim`, sized `approve` + revoke, ERC-20 transfer for sweeps, protocol calls on the allow-list), decodes it back, and enforces the hard blocks so drainer patterns are refused in code.

## Context & references

- Roadmap: [R5.02, R5.03](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.20 · drainer suite P5-T052
- [13 §2 hard blocks](../../../docs/13-wallets-treasury-and-onchain.md#2-signer-service-the-only-process-that-sees-hot-keys) · [08 never automated](../../../docs/08-airdrops-and-token-launches.md#never-automated) · [07 §4](../../../docs/07-security-notes.md#4-crypto-wallets-airdrops-on-chain-claims)
- Simulation hook: P5-T016 (Anvil fork)

## Requirements

- Builders: `claim` from ABI + selector on the mandate allow-list; `approve(spender, amount)` only with amount = exact trade size and a paired revoke intent queued; `transfer`/native send only for `sweep` to the vault destination; EIP-1559 fees from the cost-gate quote; chain-id bound.
- Decoder: re-decode the built calldata with the verified ABI (Blockscout) and assert it equals the intent (to, selector, args, value).
- Hard blocks (refuse, never downgrade to warning): EIP-2612 `permit`, Permit2 (`permit`, `permitTransferFrom`, `permitBatch`, signature transfers), `setApprovalForAll`, `approve`/`increaseAllowance` with amount ≥ 2^255 or > trade size, any EIP-712 / `personal_sign` / `eth_sign` request, unknown contract or router address, `msg.value > 0` on claims, `delegatecall`-style multicall into unknown targets, any transfer to an EOA that is not the vault ("claim fee" pattern).
- Allow-list is per wallet and per chain; addresses checksummed and compared case-insensitively.
- Library choices: `eth-abi`/`eth-account` (MIT) — pinned; no third-party bot code.

## ToDo

- [ ] Implement `packages/mt_signer/chains/evm/` builder, decoder, hard-block rules (one rule per module with an ID used in refusal codes).
- [ ] ABI resolver from Blockscout verified source (cached; unverified → refuse for autonomous paths).
- [ ] Approval lifecycle: sized approve → action → revoke intent scheduled; unrevoked after 10 min → alert + `REVOKE_APPROVAL` task.
- [ ] Table-driven tests with real calldata fixtures for each blocked pattern.
- [ ] Property tests: random calldata never yields a signature unless it decodes to an allow-listed selector.

## Verification

### Tests
- Unit: one fixture per hard block (permit, Permit2 x3, setApprovalForAll, unlimited approve, increaseAllowance, unknown router, value>0 claim, EOA "claim fee", typed-data request) → refused with its rule ID.
- Property (Hypothesis): fuzzed calldata/targets are refused unless they match the allow-list exactly.
- Unit: build→decode round-trip equality for every allowed intent type.

### Scenarios
- Given a mandate allowing `claim(uint256,address,uint256,bytes32[])` on contract C, when the intent targets C with that selector, then it builds and decodes equal.
- Given the same intent pointing at a proxy whose implementation changed since the mandate, then it refuses `implementation_changed` and raises a task.

### Stress / failure injection
- 10k fuzzed intents: zero false allows; run time < 60 s in CI.

## Acceptance criteria

- [ ] All 13 §2 EVM hard blocks enforced with rule IDs
- [ ] Approvals sized and auto-revoked
- [ ] Round-trip and property tests green

## Exceptions & edge cases

- Proxy contracts: allow-list pins the implementation address/codehash; a change refuses until re-vetted.
- L2s with custom tx types: unsupported type → refuse (fail closed).

## Cardinal rules (do NOT)

- Do NOT accept raw or pre-built transactions, raw messages or typed-data payloads from any caller — intents only; the signer re-builds and re-decodes everything itself (13 §2).
- Do NOT log, print, serialise to NATS or persist private keys anywhere except OpenBao/sops; keys are never in `.env`.
- Do NOT add an override to sign a blocked pattern "just once"; blocked means refused.
- Do NOT commit secrets or paste them into chats, issues or logs; secrets live only in the sops/age file or OpenBao (07 §2).
- Do NOT give any LLM, agent or MCP path a route to keys, the signer socket or the `signer` network (R5.N1).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §2: list the EVM rule IDs.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.20 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T014-signer-evm-builders-hard-blocks`
- PR title: `P5-T014: Signer EVM plug-in: builders, decoders and hard blocks`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T014` run

## Progress log

- 2026-10-21 00:00 · planner · created
