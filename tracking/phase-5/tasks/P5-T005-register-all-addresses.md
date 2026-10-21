---
id: P5-T005
kind: task
title: Register every address and account you own with role and investment/trading tag
phase: 5
type: USER
status: backlog
priority: high
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P5-T021, P5-T050, P5-T001]
requirements: [R5.05]
roadmap_todos: [T5.04]
modules: [M22, M18]
dashboards: [D18]
branch: p5/P5-T005-register-all-addresses
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

# P5-T005 · Register every address and account you own with role and investment/trading tag

## Goal / expected outcome

Every on-chain address and exchange account you own is in `ops.wallets` with proof of control, provider label, custody role and tax tag (`investment` vs `trading`), so the unified view (D18) is complete and reconciles to the journal.

## Context & references

- Roadmap: ToDo T5.04 → [R5.05](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · [13 §3](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view)
- Tax segregation: [09 goals](../../../docs/09-journal-and-tax.md) (wallet registry and investment vs trading)
- P3 already registered exchange accounts (P3 T3.04); this adds on-chain addresses and re-confirms tags
- Proof-of-control method: P5-B016 / P5-T021
- Depends on: P5-T021 (`wallet.register`), P5-T050 (D18 form), P5-T001 (vault/warm addresses)

## Requirements

- Register: vault, warm, any phone/browser wallets (MetaMask, Trust Wallet, Phantom, Rabby…), governance addresses, plus P5-T004 system wallets (auto-registered; you confirm tags).
- For each: address, chain, provider label (e.g. "Trust Wallet – phone"), role (vault/warm/hot/identity/burner/governance), tax tag.
- Proof of control per P5-T021: a micro self-transfer with the displayed memo/amount, or a message signature you produce **on your own device** (never via a site).
- `wallet.register` and `wallet.tag` are C1 (in-app confirm).

## ToDo

- [ ] Open D18 `/wallets` → Register; add each address with label, role and tag.
- [ ] Complete the proof-of-control step shown for each address; wait for "verified".
- [ ] Re-check exchange accounts imported in P3 and confirm their tags.
- [ ] Review the wallet table: every wallet you own is listed; nothing unknown is listed.
- [ ] Report "done" so T5.04 can be ticked.

## Verification

### Tests
- Manual: D18 shows every registered address as verified with a balance.
- After the next daily recon (P5-T024): no "unregistered counterparty owned by you" warnings.

### Scenarios
- Given you register a phone wallet, when you complete the self-transfer proof, then it shows "verified" and its transfers to your exchange are tagged internal.

### Stress / failure injection
- n/a: human data entry

## Acceptance criteria

- [ ] All owned addresses/accounts registered and verified
- [ ] Every row has role and investment/trading tag
- [ ] Daily recon shows no unknown own-wallet transfers

## Exceptions & edge cases

- Old wallets you no longer use: register them as `legacy` (read-only) so historical transfers classify correctly.
- If a proof needs gas you don't want to spend (vault), use the message-signature option on the device or mark `proof: manual_attested` with a note (weaker; shown in D18).

## Cardinal rules (do NOT)

- Do NOT type, photograph, paste or upload a seed phrase, Shamir share or private key anywhere (chat, issue, git, cloud notes, the MasterTrader UI). The system only ever receives **public** addresses.
- Do NOT connect any wallet to a website to "prove" ownership.
- Do NOT commit secrets or paste them into chats, issues or logs; secrets live only in the sops/age file or OpenBao (07 §2).

## Doc sync on completion

- No repo doc change; the agent ticks T5.04 once you confirm.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.04 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T005-register-all-addresses`
- PR title: `P5-T005: Register every address and account you own with role and investment/trading tag`
- PR checklist: no PR (USER item); confirm in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
