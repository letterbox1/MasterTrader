---
id: P5-T035
kind: task
title: Enrichment: Blockscout/own RPC, Helius, DexScreener/GeckoTerminal, CryptoRank
phase: 5
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T034, P5-T018]
requirements: [R5.12]
roadmap_todos: [T5.25]
modules: [M4]
dashboards: [D12]
branch: p5/P5-T035-enrichment-blockscout-helius-dex
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/12-policy-and-compliance.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T035 · Enrichment: Blockscout/own RPC, Helius, DexScreener/GeckoTerminal, CryptoRank

## Goal / expected outcome

Each opportunity is enriched with contract facts from **Blockscout/own RPC** (verified source, proxy/implementation, creator, holders), Solana facts from **Helius** (`getAsset`, mint/freeze authority, holders), market facts from DexScreener/GeckoTerminal (liquidity, pair age, volume) and funding from CryptoRank — with a source audit proving Etherscan is never a decision input.

## Context & references

- Roadmap: [R5.12](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.25
- [08 pipeline: Enrich](../../../docs/08-airdrops-and-token-launches.md#pipeline) · [12 §4 Etherscan row](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) · [06 on-chain providers](../../../docs/06-aggregators-and-market-providers.md)

## Requirements

- EVM: Blockscout API (or own RPC + verified-source lookups) for source verification, proxy admin/implementation (EIP-1967 slots), creator tx and deployer address, top holders.
- Solana: Helius `getAsset`, mint/freeze authority, metadata mutability, Token-2022 extensions, top holders (excluding pools/lockers/burn).
- Market: DexScreener/GeckoTerminal pairs by address (liquidity USD, FDV, pair age, 24 h volume, LP lock info where exposed).
- Funding: CryptoRank rounds/investors.
- All enrichment rows carry provenance; Etherscan URLs may appear only as manual links in D12 (display), never stored as inputs; a CI source-audit test greps for Etherscan API hosts in decision code.
- Cache per token 1 h (market) / 24 h (contract facts) within quotas.

## ToDo

- [ ] Implement `packages/mt_airdrop/enrich/` adapters and the `EnrichmentReport` model.
- [ ] Add CI source-audit check (no `api.etherscan.io` or Birdeye in `mt_airdrop`/`mt_treasury`).
- [ ] Fixture tests; doc sync.

## Verification

### Tests
- Unit: proxy detection from EIP-1967 storage slots on fixture data.
- Unit: Helius `getAsset` parse incl. Token-2022 extension list.
- CI: source audit fails when an Etherscan API host is introduced.

### Scenarios
- Given an unverified EVM contract, then enrichment marks `verified=false` (hard fail for autonomous paths later).
- Given DexScreener has no pair, then liquidity = 0 and pair age = n/a (scored as risk).

### Stress / failure injection
- Enrich 500 new tokens in a burst within quotas (queue + priority by corroboration score).

## Acceptance criteria

- [ ] All four enrichment families populated with provenance
- [ ] Source audit test in CI
- [ ] Quotas respected

## Exceptions & edge cases

- Blockscout instance down: fall back to own RPC for slots/bytecode; source verification `unknown` → treated as unverified.

## Cardinal rules (do NOT)

- Do NOT use Etherscan or Birdeye as a decision input (12 §4).
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: enrichment fields.
- `docs/12-policy-and-compliance.md`: note the CI source-audit enforcing the Etherscan rule.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.25 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T035-enrichment-blockscout-helius-dex`
- PR title: `P5-T035: Enrichment: Blockscout/own RPC, Helius, DexScreener/GeckoTerminal, CryptoRank`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T035` run

## Progress log

- 2026-10-21 00:00 · planner · created
