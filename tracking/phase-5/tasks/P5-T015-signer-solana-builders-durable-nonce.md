---
id: P5-T015
kind: task
title: Signer Solana plug-in: builders, decoders, hard blocks and durable-nonce rules
phase: 5
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T013]
requirements: [R5.02, R5.03]
roadmap_todos: [T5.20]
modules: [M22]
dashboards: []
branch: p5/P5-T015-signer-solana-builders-durable-nonce
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

# P5-T015 · Signer Solana plug-in: builders, decoders, hard blocks and durable-nonce rules

## Goal / expected outcome

The Solana plug-in builds claim, revoke, sweep and nonce-housekeeping transactions itself, decodes every instruction, refuses foreign `SetAuthority`/SPL `Approve`, unknown program IDs and any durable-nonce transaction it did not build, and manages nonce accounts (advance/close).

## Context & references

- Roadmap: [R5.03](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) (durable-nonce block) · ToDo T5.20
- [13 §2 durable nonces](../../../docs/13-wallets-treasury-and-onchain.md#2-signer-service-the-only-process-that-sees-hot-keys) (Drift, Apr 2026, ~US$270M) · [07 §4](../../../docs/07-security-notes.md#4-crypto-wallets-airdrops-on-chain-claims)
- Simulation hook: P5-T016 (`simulateTransaction`); nonce-authority monitor: P5-T025

## Requirements

- Builders: claim instructions from the allow-listed program IDL (Anchor IDL from the official repo), SPL token transfer for sweeps to the vault ATA, SPL `Revoke`, compute-budget instructions from the cost-gate quote, Jito tip **inside** the transaction when used (min 1,000 lamports).
- Decoder: every instruction's program ID must be in {System, SPL Token, Token-2022, ATA, ComputeBudget, Memo} ∪ wallet allow-list; else refuse `unknown_program`.
- Hard blocks: `SetAuthority` on any account (unless a self-built nonce/ATA housekeeping intent), SPL `Approve`/`ApproveChecked` (except sized + revoked flows built here), `AdvanceNonceAccount` not built by us, `AuthorizeNonceAccount`, Token-2022 permanent-delegate/transfer-hook interactions on unvetted mints, any partially-signed transaction from outside.
- Durable nonces: only nonce accounts created by the signer are used; after each use they are advanced; unused ones are closed at the end of a session; nonce authority must equal our key (checked before use).
- Recent blockhash path by default; durable nonce only for intents that explicitly require it.

## ToDo

- [ ] Implement `packages/mt_signer/chains/solana/` with `solders`/`solana-py` (pinned).
- [ ] Program allow-list + IDL loader; instruction decoder producing a normalised call summary for the ledger.
- [ ] Hard-block rules with IDs; Token-2022 extension inspection on the mint.
- [ ] Nonce manager: create/advance/close, authority check, record in `ops.nonce_account`.
- [ ] Fixture-based tests (real mainnet transactions captured as JSON) + property tests.

## Verification

### Tests
- Unit: fixtures for foreign SetAuthority, SPL Approve, foreign AdvanceNonceAccount, AuthorizeNonceAccount, unknown program, partially-signed external tx → refused with rule IDs.
- Unit: nonce lifecycle (create → use → advance → close) on `solana-test-validator`.
- Property: random instruction lists refused unless all program IDs are allow-listed and decode cleanly.

### Scenarios
- Given a nonce account whose authority changed (attack), when an intent would use it, then the signer refuses `nonce_authority_changed` and the monitor raises a critical alert.
- Given a claim on a Token-2022 mint with a transfer hook, then it refuses unless the mint is explicitly vetted.

### Stress / failure injection
- 5k fuzzed transactions in CI: zero false allows.

## Acceptance criteria

- [ ] All Solana hard blocks enforced
- [ ] Durable-nonce rules implemented and tested on a local validator
- [ ] Nonce accounts tracked in `ops.nonce_account`

## Exceptions & edge cases

- RPC returns a stale blockhash: rebuild once, then refuse; never re-sign a stale tx from cache.
- Token-2022 mint with default-frozen extension: claim builds but sweep fails → task, not retry loop.

## Cardinal rules (do NOT)

- Do NOT accept raw or pre-built transactions, raw messages or typed-data payloads from any caller — intents only; the signer re-builds and re-decodes everything itself (13 §2).
- Do NOT log, print, serialise to NATS or persist private keys anywhere except OpenBao/sops; keys are never in `.env`.
- Do NOT sign any durable-nonce transaction the system did not build and decode itself (13 §2).
- Do NOT commit secrets or paste them into chats, issues or logs; secrets live only in the sops/age file or OpenBao (07 §2).
- Do NOT give any LLM, agent or MCP path a route to keys, the signer socket or the `signer` network (R5.N1).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §2: list Solana rule IDs and the nonce lifecycle.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.20 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T015-signer-solana-builders-durable-nonce`
- PR title: `P5-T015: Signer Solana plug-in: builders, decoders, hard blocks and durable-nonce rules`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T015` run

## Progress log

- 2026-10-21 00:00 · planner · created
