---
id: P5-T002
kind: task
title: Back up the vault seed with Shamir (SLIP-39) and write the sealed estate letter
phase: 5
type: USER
status: backlog
priority: high
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P5-T001]
requirements: [R5.01]
roadmap_todos: [T5.02]
modules: [M22]
dashboards: []
branch: p5/P5-T002-shamir-seed-backup-estate-letter
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

# P5-T002 · Back up the vault seed with Shamir (SLIP-39) and write the sealed estate letter

## Goal / expected outcome

The vault seed is recoverable but never stored whole: split into **Shamir (SLIP-39)** shares (or a multisig) kept in separate physical places, and a sealed **estate letter** explains where shares are and how to unwind positions, without any secrets.

## Context & references

- Roadmap: ToDo T5.02 → [07 §4](../../../docs/07-security-notes.md#4-crypto-wallets-airdrops-on-chain-claims) (seed backup bullet)
- Custody tiers: [13 §1](../../../docs/13-wallets-treasury-and-onchain.md#1-custody-tiers)
- Depends on: P5-T001 (devices initialised)

## Requirements

- Scheme: SLIP-39 with a threshold such as 2-of-3 or 3-of-5 (your choice; record only the scheme, not the shares), or a 2-of-3 multisig if your devices support it.
- Shares on durable media (metal plates preferred), each in a different physical location (e.g. home safe, bank box, trusted relative).
- Estate letter: lists wallet roles, where each share is, the threshold, which devices exist, how to reach your tax agent, and the order to unwind (stablecoins → AUD; staking exits; exchange accounts) — **no seed words, PINs or passwords**.
- Warm wallet seed backed up with the same discipline (Shamir or separate metal backups in separate locations).

## ToDo

- [ ] Choose SLIP-39 (device-native if supported, e.g. Trezor) or multisig; write the scheme choice in your private notes.
- [ ] Generate the shares on the device, stamp/write each onto metal, verify each share with the device's recovery-check function.
- [ ] Place shares in separate locations; note the locations only in the estate letter.
- [ ] Write the estate letter (template: wallet roles from 13 §1, share locations, threshold, unwind steps, contacts) and seal it with a trusted person or your solicitor.
- [ ] Do a recovery dry run on a spare/reset device with the threshold number of shares, then wipe the spare.
- [ ] Report "done" to the agent so T5.02 can be ticked.

## Verification

### Tests
- Manual recovery dry run: threshold shares restore the same first EVM/Solana addresses as P5-T001.
- Manual: below-threshold shares fail to restore (if the device supports the check).

### Scenarios
- Given one share location is lost (fire), when you recover with the remaining shares, then the vault is restored.
- Given your executor opens the estate letter, when they follow it, then they can locate shares and unwind without ever having been given a secret by email.

### Stress / failure injection
- n/a: one-off human setup

## Acceptance criteria

- [ ] Shares created, verified and stored in ≥ 2 separate physical locations (meeting the threshold design)
- [ ] Recovery dry run succeeded and the spare device was wiped
- [ ] Sealed estate letter lodged, containing no secrets

## Exceptions & edge cases

- Ellipal may not support SLIP-39 natively: use a multisig with the warm device, or generate SLIP-39 on a trusted offline device and import; record which.
- If a share is ever photographed or exposed, rotate: create a new vault and move funds (treat as compromised).

## Cardinal rules (do NOT)

- Do NOT type, photograph, paste or upload a seed phrase, Shamir share or private key anywhere (chat, issue, git, cloud notes, the MasterTrader UI). The system only ever receives **public** addresses.
- Do NOT store shares in one place or in a cloud/password manager.
- Do NOT put any secret into the estate letter.
- Do NOT commit secrets or paste them into chats, issues or logs; secrets live only in the sops/age file or OpenBao (07 §2).

## Doc sync on completion

- No repo doc change; the agent ticks T5.02 once you confirm.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.02 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T002-shamir-seed-backup-estate-letter`
- PR title: `P5-T002: Back up the vault seed with Shamir (SLIP-39) and write the sealed estate letter`
- PR checklist: no PR (USER item); confirm in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
