---
id: P5-T003
kind: task
title: Add the fallback RPC provider accounts and restrict the RPC keys in sops
phase: 5
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P0-T010]
requirements: [R5.05, R5.04, R5.12]
roadmap_todos: [T5.41]
modules: [M22, M4]
dashboards: []
tools: [sops, gitleaks]
mcp: []
env: []
services: [helius, alchemy, chainstack]
branch: p5/P5-T003-rpc-provider-accounts
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

# P5-T003 · Add the fallback RPC provider accounts and restrict the RPC keys in sops

## Goal / expected outcome

Helius Free (Solana) and Alchemy Free (EVM) keys already exist from P0-T010. This task adds one free fallback account per chain family (Chainstack or QuickNode for Solana; optionally Infura for EVM), restricts every RPC key where the provider allows it, and keeps all keys only in the sops/age secrets file. The keys are first used by the late live check P5-T068; every build task runs keyless.

## Context & references

- Roadmap: ToDo T5.41 · [13 §7 RPC](../../../docs/13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16)
- Policy: [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) RPC providers row (one account each; no second accounts/multiplexing)
- Secrets: [07 §2](../../../docs/07-security-notes.md#2-secrets)
- Helius and Alchemy keys: registered in P0-T010 (T0.10); this task only adds fallbacks and restrictions
- Build first, keys last ([17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)): P5-T018 and every build task run against Anvil, devnets, PublicNode and recorded fixtures without secrets; these keys are used by the live check P5-T068 and then in production
- Unblocks: P5-T068 (live read-only check)

## Requirements

- Accounts: Helius Free (1M credits/month, 10 rps) and Alchemy Free (30M CU/month) exist from P0-T010; add one Solana fallback (Chainstack or QuickNode free) and, if you want it, one EVM fallback (Infura free); PublicNode needs no account (low-volume fallback only).
- Optional: a Blockscout API key if the instance requires one; The Graph key (100k queries/month) only if P5 tasks need subgraphs.
- Exactly **one** account per provider, registered to you; no referral links.
- Keys live in the sops secrets file outside the repo (path from P0-T022, [07 §2](../../../docs/07-security-notes.md#2-secrets)) and reach services by name only: `HELIUS_API_KEY`, `ALCHEMY_API_KEY` (from P0-T010), plus `CHAINSTACK_API_KEY` / `QUICKNODE_API_KEY` / `INFURA_API_KEY` for the fallbacks you create, each with a `created` date (key-age alert, 07 §2).

## ToDo

- [ ] Sign up at each provider with your normal email and MFA on the provider account.
- [ ] Restrict each key where the provider allows it (allowed origins/IP to your host's egress IP; read methods only).
- [ ] Open the sops secrets file (outside the repo; path from P0-T022) and add the fallback keys + creation dates; save (re-encrypts).
- [ ] Run the P0 secret check (`gitleaks` pre-commit) to confirm nothing leaked into the working tree.
- [ ] Tell the agent which providers exist (names only) so the RPC pool config (P5-T018) lists them for production and the live check (P5-T068).

## Verification

### Tests
- Manual: `sops -d` shows the new keys locally (never paste the output); `git status` in the repo shows no change (the secrets file lives outside the repo).
- In P5-T068: a live health probe per provider returns a block height.

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
- PR title: `P5-T003: Add the fallback RPC provider accounts and restrict the RPC keys in sops`
- PR checklist: no PR (USER item); confirm in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (Helius/Alchemy keys come from P0-T010; fallbacks + restrictions only; keys-last: unblocks P5-T068, not the builds; sops file outside the repo)
