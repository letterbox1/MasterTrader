---
id: P5-T032
kind: task
title: mt_airdrop discovery connectors (DefiLlama, CryptoRank, CoinGecko, DexScreener, Galxe, Snapshot, forums)
phase: 5
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T009, P5-T011, P5-T018, P1-T006]
requirements: [R5.10]
roadmap_todos: [T5.25]
modules: [M4]
dashboards: [D12]
tools: [uv, docker]
mcp: []
env: []
services: [postgres, nats]
branch: p5/P5-T032-discovery-api-connectors
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T032 · mt_airdrop discovery connectors (DefiLlama, CryptoRank, CoinGecko, DexScreener, Galxe, Snapshot, forums)

## Goal / expected outcome

The `airdrop` service discovers candidates from free APIs within quotas — DefiLlama tokenless protocols with rising TVL, CryptoRank Sandbox (ICO/IDO calendars, launchpads, funding), CoinGecko Demo (new listings, categories, `links`), DexScreener (new pairs/profiles by address), Galxe GraphQL (read-only), Snapshot GraphQL and Discourse `/latest.json` — writing raw `source_observation` rows with provenance.

## Context & references

- Roadmap: [R5.10](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.25
- [08 pipeline: Discover](../../../docs/08-airdrops-and-token-launches.md#pipeline) · [research discovery sources](../../../docs/research/airdrops-rugpull-discord.md) · [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)
- Quota tracker (P1-T006), RPC pool P5-T018
- Build first, keys last ([17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)): adapters are built and tested on recorded fixtures; keyed sources (CoinGecko Demo, CryptoRank) read keys by name only and are proven live in P5-T068 (keys from P0-T010)

## Requirements

- Quotas: CoinGecko Demo ~30/min and 10K/month, cache ≤ 24 h, attribution on display; CryptoRank 10/min, 10K credits/month; DexScreener ~300/min pairs, 60/min profiles, address-driven (no search-driven discovery); DefiLlama `api.llama.fi` only; Galxe read-only campaign/eligibility queries; Snapshot GraphQL public.
- Cadence: DefiLlama /protocols daily; CryptoRank calendars every 6 h; CoinGecko new listings every 2 h; DexScreener profiles every 10 min; Galxe/Snapshot/forums every 6 h.
- Each observation: source, licence, use flags, raw payload hash, `event_time` (source time) and `ingest_time`.
- Tokenless-protocol signal: no token, TVL up ≥ X% over 30 days (config), age ≥ 30 days.
- No headless browsers or internal endpoints for quest platforms; no airdrops.io scraping.

## ToDo

- [ ] Implement adapters in `packages/mt_airdrop/discover/` (one module per source) with httpx, retries, quota registration.
- [ ] Prefect deployments with cadences; `airdrop` container on `core` (digest-pinned).
- [ ] Recorded-fixture tests per adapter; quota tests.
- [ ] Doc sync.

## Verification

### Tests
- Unit: each adapter parses recorded fixtures into observations with correct provenance.
- Unit: quota tracker throttles CryptoRank at 10/min.
- Integration: end-to-end discovery run against fixtures produces deduplicated candidate list for P5-T034.

### Scenarios
- Given CoinGecko returns a new listing with `links.chat_url`, then the observation keeps the invite URL for community curation (P5-T047).
- Given DexScreener 429s, then backoff and resume without losing the cursor.

### Stress / failure injection
- Run all adapters at 2× cadence for 1 h against mocks: no quota overrun; priority sources first.

## Acceptance criteria

- [ ] All listed sources ingest with provenance
- [ ] Quotas never exceeded
- [ ] Retention for CoinGecko-derived fields ≤ 24 h

## Exceptions & edge cases

- A source changes schema: adapter fails closed for that source, alerts, others continue.

## Cardinal rules (do NOT)

- Do NOT scrape sites behind Cloudflare or use unofficial endpoints (DefiLlama airdrops page, Galxe internals).
- Do NOT automate any quest completion.
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: discovery cadences and thresholds.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.25 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T032-discovery-api-connectors`
- PR title: `P5-T032: mt_airdrop discovery connectors (DefiLlama, CryptoRank, CoinGecko, DexScreener, Galxe, Snapshot, forums)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T032` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keyless fixtures, live keys in P5-T068; P1 quota tracker dep)
