---
id: P3-T011
kind: task
title: Crypto rate source and three-currency stamping on every event
phase: 3
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T008, P3-T010]
requirements: [R3.03]
roadmap_todos: [T3.21]
modules: [M18]
dashboards: []
branch: p3/P3-T011-crypto-rates-three-currency-stamping
pr: ""
doc_sync: [docs/09-journal-and-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-T011 · Crypto rate source and three-currency stamping on every event

## Goal / expected outcome

Every journal event is stored with native, USD and AUD amounts plus rate source and timestamp; crypto assets are priced from our own recorded exchange data (not CoinGecko), with a deterministic venue preference, so a later base-currency or residency change never needs a re-price.

## Context & references

- Roadmap: [R3.03, T3.21](../../../docs/roadmap/phase-3-journal-and-tax.md) · exit criterion 1 (native/USD/AUD)
- [09 goals §5](../../../docs/09-journal-and-tax.md#goals) · [09 architecture: FX & price service](../../../docs/09-journal-and-tax.md#architecture) · CoinGecko terms in [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)
- Cross-phase: P1 T1.20/T1.21/T1.22 (recorded trades + bars in Timescale/Parquet)
- Gap: P3-B001 ("reputable exchange rate" undefined; CoinGecko retention ≤ 24 h)

## Requirements

- Crypto price rule (default): for asset X at time t, use the 1-minute bar close (from `market.bar_1m` via `pit`) of X/AUD on the preferred AU venue (Independent Reserve → BTC Markets → Kraken AU); else X/USDT or X/USD on Binance/Kraken/Coinbase × USDT/USD (≈1, from the same venue) × USD→AUD (P3-T010). Source string e.g. `BAR1M:BTCAUD.INDEPENDENTRESERVE`.
- Trade events with an explicit price in AUD or USD use the **trade's own price** for that leg (source `TRADE`), and the other currency via FX.
- Stamping happens in the writer pipeline before insert; events without a price go to `pending_price` (never inserted with nulls in `amt_aud`).
- Home-currency columns for future homes (AED/EGP/EUR) computed on demand by plugins, not stored now (09: ECB / CBE / CBUAE later).
- All rates stored with `numeric` precision ≥ 18 decimal places for crypto.

## ToDo

- [ ] Implement `packages/mt_journal/fx/crypto.py` (venue preference table in `config/journal/price_sources.yaml`)
- [ ] Stamp step `mt_journal/stamp.py` used by the writer: native → USD → AUD with sources
- [ ] Pending-price queue + retry flow
- [ ] Golden tests with recorded bar fixtures; docs

## Verification

### Tests

- Golden: BTC trade on IR (AUD) keeps its AUD price; USD value via F11. ETH transfer (no price) uses the bar close at that minute.
- Unit: no CoinGecko source string can be persisted (validator rejects `COINGECKO*`).
- Property: amt_aud = amt_native × rate_aud exactly (Decimal), for random inputs.

### Scenarios

- Given an airdrop of a token with no AU or major-venue market, when stamped, then it goes to `pending_price` and a `TAX_QUESTION`-style review task notes the valuation gap (zero is never assumed).
- Given the preferred venue's bar is missing for that minute, when stamped, then the next venue in the preference list is used and recorded.

### Stress / failure injection

- Stamp 1M historical events from fixtures with caching; throughput reported; memory < 1 GB.

## Acceptance criteria

- [ ] 100% of inserted events have non-null `amt_native`, `amt_usd`, `amt_aud`, `fx_source`, `fx_ts`
- [ ] No stored rate from a ≤ 24 h-retention source
- [ ] Venue preference documented in 09
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Stablecoin depeg: USDT/USD taken from the venue, not assumed 1, when a USD pair exists.
- Illiquid token: minute bar from < 3 trades flagged `thin_market` (reported in D15 notes).

## Cardinal rules (do NOT)

- Do NOT persist CoinGecko-derived prices into `journal.*`.
- Do NOT insert an event without all three currency amounts.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT use paid data/APIs or scraping that breaks terms; free tiers only (03 §1).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/09-journal-and-tax.md`: document the crypto price source preference and `pending_price` state.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.21 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T011-crypto-rates-three-currency-stamping`
- PR title: `P3-T011: Crypto rate source and three-currency stamping on every event`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T011` run

## Progress log

- 2026-10-21 00:00 · planner · created
