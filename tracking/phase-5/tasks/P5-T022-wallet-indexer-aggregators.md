---
id: P5-T022
kind: task
title: wallet-indexer: read-only balance and position aggregators
phase: 5
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T021, P5-T018]
requirements: [R5.05]
roadmap_todos: [T5.22]
modules: [M22]
dashboards: [D18]
branch: p5/P5-T022-wallet-indexer-aggregators
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

# P5-T022 · wallet-indexer: read-only balance and position aggregators

## Goal / expected outcome

The `wallet-indexer` service (`mt_treasury.indexer`) reads every registered wallet with read-only sources — Helius DAS `getAssetsByOwner` (Solana), Blockscout/own RPC (EVM tokens and DefiLlama-adapter-style positions), Hyperliquid `/info` (if approved), ccxt read-only for exchanges — values them from our own prices (CoinGecko cached ≤ 24 h) and publishes snapshots and `wallet.*` events.

## Context & references

- Roadmap: [R5.05](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.22
- [13 §3 steps 2 and 4](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view) · containers [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) (`wallet-indexer`)
- Provider terms: [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (CoinGecko ≤ 24 h cache, DefiLlama `api.llama.fi` only, Etherscan not a decision input)

## Requirements

- Poll cadence: hot/burner/identity every 60 s; others every 15 min; exchanges every 5 min; respecting P5-T018 quotas.
- Snapshot rows to `ops.wallet_balance_snapshot` (native, USD, AUD, price source, timestamp); total → chain → provider → protocol → position rollup.
- Publish `wallet.{chain}.{address}.balance` on change > 0.1% or new asset.
- Spam/airdropped-dust tokens tagged `unpriced/spam` (not counted in net worth) using blocklists and liquidity checks.
- Hyperliquid reader enabled only if the venue registry allows Hyperliquid.
- Exchange keys used are read-only, IP-locked (07 §3).

## ToDo

- [ ] Create service `packages/mt_treasury/indexer/` with adapters: helius_das.py, evm_blockscout.py, evm_positions.py (adapter pattern inspired by DefiLlama logic for core Aave/Spark/Kamino/LST reads), hyperliquid_info.py, ccxt_readonly.py.
- [ ] Pricing: reuse M1/CoinGecko cached prices; fallback to DexScreener pair price for long-tail tokens (display only).
- [ ] Rollup query endpoints `/wallets?group=` and `/wallets/{id}`.
- [ ] Compose service `wallet-indexer` on `core` with digest; heartbeat.
- [ ] Tests with recorded fixtures (VCR-style) per adapter.

## Verification

### Tests
- Unit: each adapter parses recorded fixtures into normalised holdings.
- Integration: rollup totals equal the sum of snapshots (property).
- Integration: a spam token with no liquidity is excluded from net worth.

### Scenarios
- Given Helius is rate-limited, when polling, then fallback provider is used and the snapshot is marked with the actual source.
- Given a CoinGecko price older than 24 h, then the row shows `price_stale` and D18 renders amber.

### Stress / failure injection
- 200 registered addresses: one full cycle within quotas and < 5 min; memory stable over 24 h soak.

## Acceptance criteria

- [ ] All four source families implemented
- [ ] Snapshots and events flowing for every registered wallet
- [ ] Rollups available for D18
- [ ] Quotas respected

## Exceptions & edge cases

- Address on an unsupported chain: listed with `unsupported_chain` and no balance (not silently dropped).
- Postgres down: buffer snapshots in NATS (bounded) per 02 §9.3; resume.

## Cardinal rules (do NOT)

- Do NOT use Etherscan or Birdeye as a data source; do NOT store CoinGecko data beyond 24 h.
- Do NOT use exchange keys with trade or withdrawal scope here.
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.
- Do NOT move value outside the configured caps/floats; exchange keys stay read-only or trade-only, IP-locked, withdrawals disabled; no live trading before the P7 gates.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §3: list adapters and cadences.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.22 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T022-wallet-indexer-aggregators`
- PR title: `P5-T022: wallet-indexer: read-only balance and position aggregators`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T022` run

## Progress log

- 2026-10-21 00:00 · planner · created
