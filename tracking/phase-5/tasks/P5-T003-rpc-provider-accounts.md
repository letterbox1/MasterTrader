---
id: P5-T003
kind: task
title: Create the free RPC provider accounts (Helius, Alchemy, fallbacks) and store keys in sops
phase: 5
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R5.05, R5.04, R5.12]
roadmap_todos: [T5.41]
modules: [M22, M4]
dashboards: []
branch: p5/P5-T003-rpc-provider-accounts
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

# P5-T003 · Create the free RPC provider accounts (Helius, Alchemy, fallbacks) and store keys in sops

## Goal / expected outcome

One free account per RPC provider exists (Helius Free for Solana; Alchemy Free for EVM; Chainstack/QuickNode free as fallback), each API key is stored only in the sops/age secrets file, so P5-T018 can wire RPC pools with quotas.

## Context & references

- Roadmap: ToDo T5.41 · [13 §7 RPC](../../../docs/13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16)
- Policy: [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) RPC providers row (one account each; no second accounts/multiplexing)
- Secrets: [07 §2](../../../docs/07-security-notes.md#2-secrets)
- Unblocks: P5-T018 (RPC config), then the indexer, enrichment, cost gate and signer simulation

## Requirements

- Accounts: Helius Free (1M credits/month, 10 rps), Alchemy Free (30M CU/month), one Solana fallback (Chainstack or QuickNode free), PublicNode needs no account (low-volume fallback only).
- Optional: a Blockscout API key if the instance requires one; The Graph key (100k queries/month) only if P5 tasks need subgraphs.
- Exactly **one** account per provider, registered to you; no referral links.
- Keys go into the sops file under `rpc.helius.api_key`, `rpc.alchemy.api_key`, `rpc.<fallback>.api_key`, with a `created` date (for the 90-day age alert, 07 §2).

## ToDo

- [ ] Sign up at each provider with your normal email and MFA on the provider account.
- [ ] Restrict each key where the provider allows it (allowed origins/IP to your host's egress IP; read methods only).
- [ ] Open the secrets file with `sops secrets/secrets.enc.yaml` (path from P0-T043 / R0.N1) and add the keys + creation dates; save (re-encrypts).
- [ ] Run the P0 secret check (`gitleaks` pre-commit) to confirm nothing leaked into the working tree.
- [ ] Tell the agent which providers exist (names only) so P5-T018 can configure pools.

## Verification

### Tests
- Manual: `sops -d` shows the new keys locally; `git status` shows only the encrypted file changed.
- After P5-T018: a health probe per provider returns a block height.

### Scenarios
- Given the keys are in sops, when the `wallet-indexer` container starts, then it reads them from tmpfs and never logs them.

### Stress / failure injection
- n/a: one-off human setup

## Acceptance criteria

- [ ] One account per provider created with MFA
- [ ] Keys present only in the sops file, with creation dates
- [ ] Provider names reported to the agent

## Exceptions & edge cases

- If a provider demands a card for the free tier, skip it and use the next fallback (free only).
- Rotate a key immediately if it is ever pasted somewhere it should not be.

## Cardinal rules (do NOT)

- Do NOT paste API keys into chat, issues or `.env`.
- Do NOT create second accounts to stretch a free tier (12 §4).
- Do NOT commit secrets or paste them into chats, issues or logs; secrets live only in the sops/age file or OpenBao (07 §2).
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.

## Doc sync on completion

- No repo doc change; the agent ticks T5.41 when P5-T018 also lands.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.41 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T003-rpc-provider-accounts`
- PR title: `P5-T003: Create the free RPC provider accounts (Helius, Alchemy, fallbacks) and store keys in sops`
- PR checklist: no PR (USER item); confirm in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
