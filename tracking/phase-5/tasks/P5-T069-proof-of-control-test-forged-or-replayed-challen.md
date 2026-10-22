---
id: P5-T069
kind: task
title: "Proof-of-control test: forged or replayed challenges rejected, valid proofs register the address"
phase: 5
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T067, P5-T021, P5-T023, P5-T050]
requirements: [R5.25, R5.05]
roadmap_todos: [T5.67]
modules: [M22]
dashboards: [D18]
tools: [uv, docker, anvil, solana-test-validator, pnpm]
mcp: []
env: []
services: [postgres, nats, anvil]
branch: p5/P5-T069-proof-of-control-test-forged-or-replayed-challen
pr: ""
doc_sync: [docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P5-T069 · Proof-of-control test: forged or replayed challenges rejected, valid proofs register the address

## Goal / expected outcome

An end-to-end suite (`tests/registry/test_proof_of_control.py` plus a Playwright flow) proves R5.25 through `mt_api` → `wallet.register` → proof verifier → `ops.wallets`: a valid wallet-app signature (EVM and Solana) or a valid self-transfer registers the address as `verified`; a forged, replayed, expired, mismatched or modified-text proof is rejected with its reason code and leaves the address unverified; and the system never produces a signature itself.

## Context & references

- Roadmap: ToDo T5.67 → [R5.25](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) ("Unit tests")
- Decision P5-B016 ([17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)) · [13 §3](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view) · [D18 register action](../../../docs/ui/dashboards/D18-wallets-treasury.md)
- Under test: P5-T067 (challenge + verifiers), P5-T021 (`wallet.register`), P5-T023 (self-transfer seen by the classifier), P5-T050 (D18 registration wizard)

## Requirements

- Test wallets stand in for "your own wallet app": generated throwaway keys inside the test process sign the challenge text (EVM `personal_sign`, Solana `signMessage`); they never touch the signer service or real funds.
- Self-transfer on Anvil (EVM) and `solana-test-validator`: send the challenge amount from the address to itself; the indexer/classifier picks it up at finality.
- Negative cases (each must be rejected and audited): signature by a different key; signature over modified text; replay of an already-used challenge; expired challenge; challenge for another chain; self-transfer with the wrong amount or from another address; EIP-1271 contract wallet signature.
- Assert no signer intent, no signer ledger row and no key-holding call happens during registration.
- Playwright: the D18 wizard shows the challenge, accepts a pasted signature and flips the row to `verified`; a bad signature shows the reason.

## ToDo

- [ ] Write the API-level suite with positive and negative cases (≥ 12 cases).
- [ ] Write the Anvil/local-validator self-transfer cases.
- [ ] Write the Playwright registration-wizard flow (phone and desktop profiles).
- [ ] Add the suite to CI as a required check for `mt_treasury.registry`; record results in the progress log.

## Verification

### Tests
- The suite itself, plus a meta-test that fails if any case is skipped or xfail'd.

### Scenarios
- Given a valid MetaMask-style signature of the issued challenge, when you paste it in D18, then the address shows `verified` (method `wallet_signature`).
- Given an attacker replays yesterday's valid signature, when submitted against a new challenge, then it is rejected `proof_replayed` and the address stays unverified.
- Given a vault address proved by self-transfer on the local chain, when the transfer finalises, then the address is `verified` (method `self_transfer`).

### Stress / failure injection
- Run the suite 10× in a loop: 0 flaky failures; inject an indexer restart during the self-transfer case: verification completes after restart without duplicates.

## Acceptance criteria

- [ ] All positive cases register the address as verified
- [ ] All negative cases rejected with the expected reason codes and audited
- [ ] No signer intent or ledger row produced by registration
- [ ] Required CI check added; results logged

## Exceptions & edge cases

- Local validator flakiness: retry the setup, never relax an assertion.
- If a chain's wallet apps can't sign messages, self-transfer is the documented path (covered here).

## Cardinal rules (do NOT)

- Do NOT use the signer service or any real key/funds in this test.
- Do NOT add a "skip proof" or "trust me" registration path to make tests pass.
- Do NOT commit secrets or paste them into chats, issues or logs; test keys are generated per run and never persisted.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.67 when this lands.

## Branch & PR

- Branch: `p5/P5-T069-proof-of-control-test-forged-or-replayed-challen`
- PR title: `P5-T069: Proof-of-control test: forged or replayed challenges rejected, valid proofs register the address`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T069` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (T5.67: proof-of-control test, P5-B016)
