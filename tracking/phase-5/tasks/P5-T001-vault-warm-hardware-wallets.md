---
id: P5-T001
kind: task
title: Set up the vault and warm hardware wallets (public addresses only)
phase: 5
type: USER
status: backlog
priority: critical
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R5.01]
roadmap_todos: [T5.01]
modules: [M22]
dashboards: [D18]
tools: []
mcp: []
env: []
services: []
branch: p5/P5-T001-vault-warm-hardware-wallets
pr: ""
doc_sync: [docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T001 · Set up the vault and warm hardware wallets (public addresses only)

## Goal / expected outcome

You own an air-gapped **vault** (cold) wallet and a **warm** hardware wallet, initialised offline by you, and their **public** addresses per chain are written down ready for registration (P5-T005). The system never sees a key. This is the anchor of the custody tiers (R5.01) and the sweep destination (R5.07).

## Context & references

- Roadmap: [R5.01](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.01 · entry criterion "Wallets created by you"
- Custody tiers: [13 §1](../../../docs/13-wallets-treasury-and-onchain.md#1-custody-tiers) (vault = air-gapped, e.g. Ellipal Titan, MetaMask-QR signing only; warm = hardware wallet you approve on-device)
- Seed rules: [07 §4](../../../docs/07-security-notes.md#4-crypto-wallets-airdrops-on-chain-claims)
- Watch-only rule (decision P5-B008, [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)): the system never holds vault or warm keys; it may only *prepare* unsigned transactions (QR / WalletConnect) for you to sign in your own wallet ([13 §1](../../../docs/13-wallets-treasury-and-onchain.md#1-custody-tiers))
- Unblocks: P5-T002 (seed backup), P5-T005 (register addresses), P5-T028 (sweeps to the vault address)

## Requirements

- Vault: an air-gapped device (e.g. Ellipal Titan) never connected to the host or the internet; signs only via QR.
- Warm: a hardware wallet with on-device confirmation (Ledger Flex/Nano X or Trezor Safe 5); used manually for staking/governance later (P6).
- Both initialised by you from a fresh seed generated **on the device**; no pre-seeded or second-hand devices.
- Output: one public address per chain you will use (EVM and Solana at minimum) per wallet, kept in a plain note (public data only) for P5-T005.
- If Hyperliquid has been approved (12 §1), the HL master hardware signer is a separate device; otherwise record "HL master: not applicable".

## ToDo

- [ ] Buy or confirm the devices from the manufacturer's official store (never a marketplace reseller); check tamper seals.
- [ ] Initialise the vault device offline, generate a new seed on-device, set a strong PIN; do **not** write the seed yet in its final form (P5-T002 handles backup).
- [ ] Initialise the warm hardware wallet the same way; update firmware from the vendor app only.
- [ ] Derive the first EVM and Solana receive addresses on each device; verify each address on the device screen.
- [ ] Send a test receive of a trivial amount to each vault/warm address from an exchange you own; confirm arrival on a block explorer.
- [ ] Record the public addresses (wallet, chain, address, device label such as "Ellipal – vault") in a note you will paste into the registration form in P5-T005.
- [ ] Tick T5.01 by reporting "done" to the agent (no addresses or secrets in chat needed).

## Verification

### Tests
- Manual: each address shown on the device screen equals the address recorded in your note (character-by-character on the first/last 6).
- Manual: the test receive is visible on a block explorer for every vault/warm address.

### Scenarios
- Given a new vault device, when you derive the EVM address, then the device screen and your note match exactly.
- Given a device that arrives with a pre-printed recovery card, when you open it, then you stop and return it (supply-chain attack).

### Stress / failure injection
- n/a: one-off human setup

## Acceptance criteria

- [ ] Vault and warm devices initialised on-device by you, firmware current
- [ ] Public EVM + Solana addresses recorded for each (public data only)
- [ ] Test receive confirmed on-chain for each address
- [ ] No secret material exists anywhere digital

## Exceptions & edge cases

- Ellipal has no EIP-712 and no xpub export: register individual addresses, not xpubs.
- If you already hold funds on an older device, treat it as "legacy" and move funds to the new vault later; do not reuse its seed.
- Device loss before P5-T002 is done = recreate from scratch (no funds yet beyond the test amounts).

## Cardinal rules (do NOT)

- Do NOT type, photograph, paste or upload a seed phrase, Shamir share or private key anywhere (chat, issue, git, cloud notes, the MasterTrader UI). The system only ever receives **public** addresses.
- Do NOT connect the vault to any computer, phone app or WalletConnect session.
- Do NOT let any MasterTrader process generate or hold vault/warm keys; vault and warm are watch-only in the system (R5.01). The system may only prepare unsigned transactions that you review and sign in your own wallet.
- Do NOT commit secrets or paste them into chats, issues or logs; secrets live only in the sops/age file or OpenBao (07 §2).

## Doc sync on completion

- No repo doc change; the agent ticks T5.01 in the roadmap once you confirm.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.01 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T001-vault-warm-hardware-wallets`
- PR title: `P5-T001: Set up the vault and warm hardware wallets (public addresses only)`
- PR checklist: no PR (USER item); confirm in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (watch-only wording per P5-B008: system may prepare unsigned transactions only; run fields)
