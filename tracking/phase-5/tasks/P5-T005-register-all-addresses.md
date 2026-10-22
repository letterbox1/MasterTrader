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
depends_on: [P5-T001, P5-T021, P5-T050, P5-T067, P3-T042]
requirements: [R5.05, R5.25]
roadmap_todos: [T5.04]
modules: [M22, M18]
dashboards: [D18]
tools: []
mcp: []
env: []
services: []
branch: p5/P5-T005-register-all-addresses
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

# P5-T005 · Register every address and account you own with role and investment/trading tag

## Goal / expected outcome

Every on-chain address and exchange account you own is in `ops.wallets` with proof of control, provider label, custody role and tax tag (`investment` vs `trading`), so the unified view (D18) is complete and reconciles to the journal.

## Context & references

- Roadmap: ToDo T5.04 → [R5.05](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · [13 §3](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view)
- Tax segregation: [09 goals](../../../docs/09-journal-and-tax.md) (wallet registry and investment vs trading)
- P3 already registered exchange accounts in `ops.wallets` (P3 T3.04, P3-T042); this adds on-chain addresses and re-confirms tags
- Proof of control ([R5.25](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md), decision P5-B016, [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)): you sign a one-time challenge in **your own wallet app** (EIP-4361-style text on EVM, Solana `signMessage`) or make a tiny self-transfer; the system only verifies (P5-T067) and never signs
- Depends on: P5-T021 (`wallet.register`), P5-T067 (challenge verifier), P5-T050 (D18 form), P5-T001 (vault/warm addresses), P3-T042 (exchange accounts registered in P3)

## Requirements

- Register: vault, warm, any phone/browser wallets (MetaMask, Trust Wallet, Phantom, Rabby…), governance addresses, plus P5-T004 system wallets (auto-registered; you confirm tags).
- For each: address, chain, provider label (e.g. "Trust Wallet – phone"), role (vault/warm/hot/identity/burner/governance), tax tag.
- Proof of control per R5.25: copy the one-time challenge shown in D18, sign it in your own wallet app ("sign message" in MetaMask, Rabby, Phantom, Trust Wallet…) and paste the signature back; or make the tiny self-transfer with the displayed amount/memo. Never through a website or WalletConnect; the system never signs.
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
- The vault (Ellipal) can't sign plain messages: use the tiny self-transfer (its gas is the only cost). There is no unproven "attested" registration; an address without proof stays `pending` and is excluded from autonomous paths and sweep destinations.

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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (R5.25 proof of control: wallet-app challenge signature or self-transfer, system never signs; manual_attested removed; depends on P5-T067)
