---
id: P5-T034
kind: task
title: Normalise and dedupe, verify official domain, corroboration score
phase: 5
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T032, P5-T031]
requirements: [R5.11]
roadmap_todos: [T5.25]
modules: [M4]
dashboards: [D12]
tools: [uv]
mcp: []
env: []
services: [postgres]
branch: p5/P5-T034-normalise-official-domain-corroboration
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

# P5-T034 · Normalise and dedupe, verify official domain, corroboration score

## Goal / expected outcome

Observations collapse into `airdrop_opportunity` keyed by (chain, contract) else project slug; the **official domain** is resolved from CoinGecko/DefiLlama and cross-checked with WHOIS age and blocklists; a **corroboration score** counts independent sources agreeing on domain, contract and dates, and anything with < 2 independent sources is `watch` only.

## Context & references

- Roadmap: [R5.11](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.25
- [08 pipeline: Normalise](../../../docs/08-airdrops-and-token-launches.md#pipeline) · [08 hard fails](../../../docs/08-airdrops-and-token-launches.md#risk-score-0100-any-hard-fail--100--reject) (claim domain ≠ official domain)

## Requirements

- Dedupe: exact (chain, contract); fuzzy slug match (normalised name, ticker, domain) with manual merge/split in D12.
- Official domain: majority of CoinGecko `links.homepage` and DefiLlama `url`, plus official X bio/docs when available; WHOIS/RDAP age recorded; blocklisted → hard-fail flag.
- Independence: sources sharing an upstream (e.g. two aggregators copying CoinGecko) count once; independent sources = DefiLlama, CryptoRank, CoinGecko, official X, official Discord, official docs/forum.
- Corroboration score 0–N with fields agreeing (domain, contract, dates); < 2 → stage `watch` regardless of other scores.
- Lookalike detection: punycode/homoglyph and Levenshtein ≤ 2 vs the official domain → phishing flag.

## ToDo

- [ ] Implement `packages/mt_airdrop/normalise/` (keys, dedupe, merge), `domain.py` (RDAP client, lookalike), `corroboration.py`.
- [ ] Merge/split commands surfaced to D12 (C1).
- [ ] Tests with fixture observations; doc sync.

## Verification

### Tests
- Unit: dedupe merges the same contract seen on 4 sources into one opportunity.
- Unit: homoglyph domain `unіswap.org` (Cyrillic і) flagged.
- Unit: two sources copying CoinGecko count as one independent source.

### Scenarios
- Given a project seen only in Telegram postures and DexScreener, then corroboration = 1 → `watch`, no task created.
- Given DefiLlama and CoinGecko disagree on the domain, then `domain_conflict` is surfaced and autonomous paths are blocked.

### Stress / failure injection
- 50k observations/day normalised within 10 min of arrival.

## Acceptance criteria

- [ ] Opportunities deduplicated with stable keys
- [ ] Official domain verified with WHOIS age and blocklists
- [ ] Corroboration score computed; < 2 → watch only

## Exceptions & edge cases

- RDAP rate-limited/unavailable: domain age `unknown` (scored as risk), never assumed old.

## Cardinal rules (do NOT)

- Do NOT treat Telegram-only signals as corroboration from an official source.
- Do NOT let Telegram text reach any model, RAG index or training set; Telegram contributes deterministic postures only (12 §4–5).
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: independence rules for corroboration.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.25 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T034-normalise-official-domain-corroboration`
- PR title: `P5-T034: Normalise and dedupe, verify official domain, corroboration score`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T034` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields; content already matches 08 normalise/corroboration)
