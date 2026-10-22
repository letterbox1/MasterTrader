---
id: P3-T011
kind: task
title: Valuation service (16 §4.1 hierarchy) and three-currency stamping on every event
phase: 3
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T008, P3-T010, P1-T012, P0-T027]
requirements: [R3.03, R3.15]
roadmap_todos: [T3.21, T3.31]
modules: [M18]
dashboards: []
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres]
branch: p3/P3-T011-crypto-rates-three-currency-stamping
pr: ""
doc_sync: [docs/09-journal-and-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T011 · Valuation service (16 §4.1 hierarchy) and three-currency stamping on every event

## Goal / expected outcome

Every journal event is stored with native, USD and AUD amounts plus rate source and timestamp, and every crypto value follows the **valuation hierarchy** of [16 §4.1](../../../docs/16-configuration-and-safety-model.md#41-valuing-crypto-for-the-journal): trades at their fill price; non-trade events at the VWAP of our own recorded trades (primary AUD venue, else USD venue × RBA AUD/USD); long-tail tokens at the on-chain DEX pool price at the event block; aggregators such as CoinGecko as a cross-check only. The stored value is always ours, with method and source references, so 7-year retention is free of third-party data terms and a later base-currency or residency change never needs a re-price. The same service supplies the per-asset-class snapshot prices (16 §4.2) used by P3-T030.

## Context & references

- Roadmap: [R3.03, R3.15, T3.21, T3.31](../../../docs/roadmap/phase-3-journal-and-tax.md) · exit criterion 1 (native/USD/AUD)
- Rules: [16 §4.1](../../../docs/16-configuration-and-safety-model.md#41-valuing-crypto-for-the-journal) · [16 §4.2](../../../docs/16-configuration-and-safety-model.md#42-market-value-snapshot-30-june-2027-and-any-residency-change) · [09 FX and valuation rules](../../../docs/09-journal-and-tax.md#fx-and-valuation-rules) · decisions [17 §A P3-B001, P3-B002](../../../docs/17-decisions-register.md#a-s2-items-all-resolved)
- CoinGecko terms (cache ≤ 24 h, display and cross-check only): [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) · wallet view uses the same hierarchy [13 §3](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view)
- Cross-phase prerequisites (depends_on): P1-T012 (Parquet recorder of public trades), P0-T027 (`pit(as_of)`); recorded trades come from P1-T010/T011 streams
- Related: P3-T010 (RBA FX), P3-T030 (snapshot job uses `snapshot_price`), P3-T017 (on-chain events), P3-T045 (valuation golden cases)

## Requirements

- **Tier 1 · trades:** the actual fill price and fees (`method = fill`, source `TRADE:<venue exec id>`); the other currency leg via FX (P3-T010).
- **Tier 2 · non-trade events** (airdrops, staking rewards, income, transfers needing a value): VWAP of our recorded public trades of X/AUD on the **primary AUD venue** for the event minute (`method = vwap_aud`); otherwise the USD venue VWAP for that minute × RBA AUD/USD (`method = vwap_usd_x_rba`). Venues come from `config/journal/valuation.yaml` (primary AUD venue, USD venue order); defaults are the venues P1 records, editable in settings.
- **Tier 3 · long-tail tokens** with no recorded venue: the on-chain DEX pool price at the event block read via our RPC (`method = pool_price`, source = chain, pool address, block). Built and tested against recorded pool-state fixtures; the RPC endpoint is a setting (empty until the P5 RPC set-up) and when empty the event goes to `pending_price`.
- **Tier 4 · aggregators** (CoinGecko etc.): cross-check only via the P1 24 h cache; the aggregator value is **never** persisted to `journal.*`; a large divergence adds a review note on the event.
- Each value is a `journal.valuation` row (method, price, window, source refs, venue, block) referenced by the event; reports carry the method summary (R3.12).
- Stamping happens in the writer pipeline before insert; events without a value go to `pending_price` (never inserted with null `amt_aud`, never valued at zero).
- `snapshot_price(asset, asset_class, valuation_ts)` implements the 16 §4.2 convention per asset class (crypto: VWAP of recorded trades 23:55:00–23:59:59 AEST on the primary venue; ASX official close; US/EU last trade at or before 23:59:59 AEST, else previous official close; FX RBA rate for the day) for P3-T030; conventions are per-asset-class settings.
- Home-currency columns for future homes (AED/EGP/EUR) computed on demand by plugins, not stored now.
- All rates `numeric` with ≥ 18 decimal places for crypto; reads through `pit(as_of)` only.

## ToDo

- [ ] Implement `packages/mt_journal/valuation/service.py` with tiers 1–4 and `snapshot_price`
- [ ] VWAP reader over recorded trades (`pit`), pool-price reader (RPC client behind an interface, fixture-backed in tests)
- [ ] `journal.valuation` writes + `config/journal/valuation.yaml` (venues, snapshot conventions)
- [ ] Stamp step `mt_journal/stamp.py` used by the writer: native → USD → AUD with sources and valuation id
- [ ] Pending-price queue + retry flow (Prefect `journal-valuation-retry`)
- [ ] Golden tests with recorded trade and pool fixtures; docs

## Verification

### Tests
- Golden: BTC fill on an AUD venue keeps its fill price (`method = fill`); USD value via F11.
- Golden: staking reward of ETH at 10:31 → VWAP of recorded ETH/AUD trades 10:31:00–10:31:59 on the primary AUD venue; with no AUD trades that minute → ETH/USD VWAP × RBA AUD/USD.
- Golden: long-tail token → pool price at the event block from a recorded pool fixture.
- Unit: a `COINGECKO*` source can never be persisted (validator rejects it).
- Property: `amt_aud = amt_native × rate_aud` exactly (Decimal) for random inputs.

### Scenarios
- Given an airdrop of a token with no recorded venue and no RPC configured, when stamped, then it goes to `pending_price` and a review note is raised (zero is never assumed).
- Given CoinGecko differs widely from our VWAP, when stamped, then our VWAP is stored and the divergence is noted; nothing from CoinGecko is stored.
- Given the snapshot job asks for BTC at 2027-06-30 23:59:59 AEST, when called, then the VWAP of recorded trades 23:55:00–23:59:59 AEST on the primary venue is returned with method and window.

### Stress / failure injection
- Stamp 1M historical events from fixtures with caching; throughput reported; memory < 1 GB.
- Recorded-trade store unavailable → events queue as `pending_price`, nothing inserted with partial values.

## Acceptance criteria

- [ ] 100% of inserted events have non-null `amt_native`, `amt_usd`, `amt_aud`, `fx_source`, `fx_ts` and, for non-trade crypto, a `journal.valuation` row with method + sources
- [ ] No stored value from an aggregator or any ≤ 24 h-retention source
- [ ] Valuation hierarchy and snapshot conventions configurable and documented in 09
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Stablecoin depeg: USDT/USD taken from recorded trades, not assumed 1, when a USD pair exists.
- Illiquid token: a VWAP built from very few trades is flagged `thin_market` (threshold is a setting) and shown in D15 notes.

## Cardinal rules (do NOT)

- Do NOT persist CoinGecko or other aggregator prices into `journal.*`; they are a cross-check only.
- Do NOT insert an event without all three currency amounts.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT use paid data/APIs or scraping that breaks terms; free tiers only (03 §1).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/09-journal-and-tax.md` FX and valuation rules: document the configured venues, `journal.valuation` and the `pending_price` state.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.21 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T011-crypto-rates-three-currency-stamping`
- PR title: `P3-T011: Crypto rate source and three-currency stamping on every event`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T011` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (rewritten as the 16 §4.1 valuation service (R3.15/T3.31) + 16 §4.2 snapshot prices; replaces bar-close/venue-preference default (P3-B001/P3-B002 closed); explicit P1/P0 depends_on; tools/services filled)
