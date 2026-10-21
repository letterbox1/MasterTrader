---
id: P5-T004
kind: task
title: Approve creation of hot, identity and burner keys in the signer and fund minimal floats
phase: 5
type: USER
status: backlog
priority: critical
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P5-T012, P5-T013, P5-T014, P5-T015, P5-T017, P5-T021]
requirements: [R5.01, R5.07]
roadmap_todos: [T5.03]
modules: [M22]
dashboards: [D18, D12]
branch: p5/P5-T004-approve-hot-identity-burner-keys
pr: ""
doc_sync: [docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T004 · Approve creation of hot, identity and burner keys in the signer and fund minimal floats

## Goal / expected outcome

The signer holds exactly the keys you approved: one **hot** key per chain in use, one **airdrop identity** wallet per chain (EVM, Solana), and a **burner** per chain; each has the caps and float you confirmed and is funded with only that float. This is the precondition for any claim, sweep or test in P5.

## Context & references

- Roadmap: ToDo T5.03 → R5.01, R5.07
- Custody tiers and limits: [13 §1](../../../docs/13-wallets-treasury-and-onchain.md#1-custody-tiers); signer: [13 §2](../../../docs/13-wallets-treasury-and-onchain.md#2-signer-service-the-only-process-that-sees-hot-keys)
- Numeric defaults gap: P5-B001 (floats/caps not specified in the docs; you decide here)
- Depends on: P5-T012 custody config, P5-T013/T014/T015 signer, P5-T017 signer container, P5-T021 registry

## Requirements

- Key creation runs inside the signer (`mt-signer keys create --tier hot|identity|burner --chain evm|solana`), triggered by a C3 command from you; private keys never leave the signer and are written only to OpenBao/sops.
- You confirm per tier: float (e.g. burner = gas for a few txs), per-tx cap, rolling-24h cap, daily gas budget; values stored in the custody config (P5-T012) via a C3 change.
- Identity wallets: exactly one per chain; if you already have a wallet with organic history you want as identity, it stays **warm** (hardware) and is registered as `identity` with signing manual — record the choice.
- Fund each wallet from an exchange you own with **only** the float; the vault address is set as the sweep destination.

## ToDo

- [ ] Review the proposed defaults in D18/`custody.yaml` (from P5-T012 and P5-B001) and set your numbers.
- [ ] Approve the C3 change for the custody config in Telegram (approve + TOTP), wait for the cool-down.
- [ ] Approve the key-creation command(s) for hot, identity (EVM, Solana) and burner (EVM, Solana) in Telegram (C3).
- [ ] Copy each new public address from D18 and fund it with exactly the float from an exchange you own (whitelisted withdrawal).
- [ ] Confirm D18 shows each wallet with tier, caps and a balance at or under the float.
- [ ] Report "done" so T5.03 can be ticked.

## Verification

### Tests
- Manual: D18 wallet table lists each new wallet with the right tier and cap usage 0%.
- Manual: the signer ledger shows a key-creation entry per key (no key material).

### Scenarios
- Given you approve key creation, when the cool-down passes, then the signer creates keys and only public addresses appear in `ops.wallets`.
- Given you fund a burner above its float, when the next sweep runs, then the excess goes to the vault address (P5-T028).

### Stress / failure injection
- n/a: human approval step (the sweep path is tested in P5-T058)

## Acceptance criteria

- [ ] Hot, identity (per chain) and burner keys exist in the signer; public addresses registered
- [ ] Caps/floats/gas budgets set by you via C3 and visible in D18
- [ ] Each wallet funded with at most its float

## Exceptions & edge cases

- If OpenBao is not yet deployed, keys live in the sops file (07 §2 upgrade path: move to OpenBao once the signer holds more than one hot key).
- If you decline an identity wallet on a chain, claims on that chain stay manual (`CLAIM_MANUAL` tasks).

## Cardinal rules (do NOT)

- Do NOT type, photograph, paste or upload a seed phrase, Shamir share or private key anywhere (chat, issue, git, cloud notes, the MasterTrader UI). The system only ever receives **public** addresses.
- Do NOT fund any system wallet beyond its float; do NOT send from the vault (outflows from the vault are manual, offline-signed, and not part of P5).
- Do NOT commit secrets or paste them into chats, issues or logs; secrets live only in the sops/age file or OpenBao (07 §2).
- Do NOT apply loosening (new mandate, higher caps, autonomous claims) without C3 (Telegram approve + TOTP + cool-down); protective actions (revoke, sweep, kill) never wait for approval.
- Do NOT move value outside the configured caps/floats; exchange keys stay read-only or trade-only, IP-locked, withdrawals disabled; no live trading before the P7 gates.

## Doc sync on completion

- No repo doc change; the agent ticks T5.03 once you confirm.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.03 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T004-approve-hot-identity-burner-keys`
- PR title: `P5-T004: Approve creation of hot, identity and burner keys in the signer and fund minimal floats`
- PR checklist: no PR (USER item); confirm in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
