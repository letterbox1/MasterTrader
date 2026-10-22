---
id: P5-T067
kind: task
title: "Proof-of-control challenge: issue one-time challenges and verify wallet-app signatures or self-transfers"
phase: 5
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T009, P5-T011]
requirements: [R5.25, R5.05]
roadmap_todos: [T5.32]
modules: [M22]
dashboards: [D18]
tools: [uv, docker]
mcp: []
env: []
services: [postgres, nats]
branch: p5/P5-T067-proof-of-control-challenge-issue-one-time-challe
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/02-v1-architecture.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T067 · Proof-of-control challenge: issue one-time challenges and verify wallet-app signatures or self-transfers

## Goal / expected outcome

`mt_treasury.registry.proof` issues a one-time, expiring challenge for an address being registered and verifies the proof you produce **in your own wallet app**: an EIP-4361-style text signature (EVM `personal_sign`), a Solana `signMessage` signature, or a tiny self-transfer carrying the challenge amount/memo. The system only verifies; it never signs or requests a signature through a website. Valid proof sets `proof_status = verified` on the `ops.wallets` row; forged, replayed or expired proofs are rejected.

## Context & references

- Roadmap: [R5.25](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.32 · test P5-T069
- Decision P5-B016 ([17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)): you sign a one-time challenge in your own wallet app (EIP-4361-style text / Solana `signMessage`) or make a tiny self-transfer; the system never signs it
- [13 §3 step 1](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view) (proof of control; signer-created wallets are registered by the signer itself) · [D18 actions](../../../docs/ui/dashboards/D18-wallets-treasury.md) (register = C1) · [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) (`wallet.register` C1; C1 = confirm token from the preview call)
- Never-automated: the system never asks for `personal_sign` of arbitrary payloads ([08 never automated](../../../docs/08-airdrops-and-token-launches.md#never-automated)); the challenge is fixed, human-readable text you sign yourself
- Used by P5-T021 (`wallet.register`), P5-T050 (D18 registration wizard) and P5-T005 (USER registration)

## Requirements

- **Challenge issue:** the `wallet.register` preview step returns a challenge bound to (address, chain, registry nonce, issued_at, expires_at, host id). Default expiry 30 min, configurable. EVM text follows the EIP-4361 layout (domain = the MasterTrader host name, statement "Prove control of this address for MasterTrader registration. No transaction, no approval.", nonce, issued-at, expiration). Solana uses the same text for `signMessage`.
- **Signature verify:** EVM via EIP-191 `personal_sign` recovery (`eth-account`, pinned) with EIP-55 address match; EIP-1271 contract wallets are rejected with `contract_wallet_unsupported` (use self-transfer). Solana via ed25519 verify (`solders`/`PyNaCl`, pinned) against the base58 public key.
- **Self-transfer verify:** the challenge also carries a unique dust amount (EVM native, Solana lamports) or memo; a transfer from the address to itself (or to a registered address of yours) matching it within 24 h, seen by the indexer at finality, verifies. Input is the `wallet.{chain}.{address}.transfer` contract (P5-T011); tests use fixtures.
- **One-time:** each challenge verifies at most once; a reused nonce, an expired challenge, a different address/chain or a modified text is rejected (`proof_replayed`, `proof_expired`, `proof_mismatch`, `proof_bad_signature`).
- **Records:** challenge issued/verified/rejected rows (append-only) with method and reason; `ops.wallets.proof_method` ∈ {`wallet_signature`, `self_transfer`, `signer_owned`, `exchange_api`}, `proof_status` ∈ {`pending`, `verified`, `rejected`, `expired`}.
- No private key, seed or signing library that holds keys runs in this code path: verify-only.

## ToDo

- [ ] Implement `packages/mt_treasury/registry/proof/` (`challenge.py`, `verify_evm.py`, `verify_solana.py`, `verify_self_transfer.py`).
- [ ] Add challenge rows (`ops.wallet_proof_challenge`, append-only) via an additive migration on top of P5-T009.
- [ ] Wire the preview step of `wallet.register` to return the challenge text and expiry (handler shared with P5-T021).
- [ ] Unit tests with published EIP-191/ed25519 test vectors and generated test keys; replay/expiry/mismatch cases.
- [ ] Update the docs listed under Doc sync.

## Verification

### Tests
- Unit: EIP-191 recovery against known vectors; Solana ed25519 verify against known vectors.
- Unit: a signature over a modified challenge text (one character changed) is rejected `proof_bad_signature`.
- Unit: the same valid signature submitted twice → second rejected `proof_replayed`; after expiry → `proof_expired`.
- Integration (fixtures): a self-transfer event with the challenge amount verifies; a transfer from a different address does not.
- Static check: the proof package imports no key-holding or signing APIs (`Account.sign_*`, `Keypair.sign_message`) outside test code.

### Scenarios
- Given you sign the challenge in MetaMask and paste the signature back, when it verifies, then the address shows `verified` with method `wallet_signature`.
- Given the vault (Ellipal) cannot sign messages, when you make the tiny self-transfer instead, then the indexer event verifies it within one poll after finality.
- Given an attacker submits a signature for a different address, then it is rejected `proof_mismatch` and the attempt is recorded.

### Stress / failure injection
- 1,000 verification attempts/min with 90% invalid: no crash, p95 verify < 20 ms (signature path), all invalid rejected with reason codes.

## Acceptance criteria

- [ ] Challenges are one-time, expiring and bound to address + chain
- [ ] EVM and Solana signature verification and self-transfer verification implemented
- [ ] Replayed, expired, mismatched and forged proofs rejected with reason codes
- [ ] No signing code path in the system for proofs (static check)

## Exceptions & edge cases

- Chain reorg removes the self-transfer: proof returns to `pending` until a final transfer is seen.
- Hardware wallets that sign only typed data or nothing (e.g. Ellipal vault): use self-transfer.
- Exchange accounts: proof is a working read-only API key (`exchange_api`), handled in P5-T021.

## Cardinal rules (do NOT)

- Do NOT sign the challenge, or anything else, on the user's behalf; the system only verifies.
- Do NOT ask the user to connect a wallet to a website or use WalletConnect to "prove" ownership; the user pastes a signature produced in their own app.
- Do NOT accept arbitrary payloads to verify; only the issued challenge text counts.
- Do NOT commit secrets or paste them into chats, issues or logs; secrets live only in the sops/age file or OpenBao (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §3: challenge format, expiry default and reason codes.
- `docs/02-v1-architecture.md` §7.2: note that the `wallet.register` preview returns the proof challenge.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.32 when this lands.

## Branch & PR

- Branch: `p5/P5-T067-proof-of-control-challenge-issue-one-time-challe`
- PR title: `P5-T067: Proof-of-control challenge: issue one-time challenges and verify wallet-app signatures or self-transfers`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T067` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (R5.25 / T5.32: proof of control, system verifies only, P5-B016)
