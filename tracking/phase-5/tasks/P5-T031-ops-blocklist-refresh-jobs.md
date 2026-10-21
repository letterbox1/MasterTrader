---
id: P5-T031
kind: task
title: Blocklist refresh jobs (MetaMask, ScamSniffer, polkadot-js, Chainabuse)
phase: 5
type: OPS
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T009]
requirements: [R5.13]
roadmap_todos: [T5.42]
modules: [M4, M19]
dashboards: [D12]
branch: p5/P5-T031-ops-blocklist-refresh-jobs
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T031 · Blocklist refresh jobs (MetaMask, ScamSniffer, polkadot-js, Chainabuse)

## Goal / expected outcome

Scheduled Prefect flows refresh `curation.blocklist_domain` and `curation.blocklist_address` from MetaMask eth-phishing-detect, ScamSniffer scam-database, polkadot-js/phishing and the Chainabuse API, with provenance and licence tags, so risk scoring, link rendering and the signer all check the same fresh lists.

## Context & references

- Roadmap: ToDo T5.42 → R5.13 · [08 risk-score blocklists](../../../docs/08-airdrops-and-token-launches.md#risk-score-0100-any-hard-fail--100--reject)
- Research: [blocklists and licences](../../../docs/research/airdrops-rugpull-discord.md) (DBAD (U), GPL-3.0 (U), Chainabuse 5,000 calls/hour)

## Requirements

- Cadence: git-based lists every 6 h (shallow fetch of pinned repos), Chainabuse incremental hourly within 5,000 calls/hour.
- Normalise domains (punycode, lowercase, eTLD+1 plus full host) and addresses (checksum/base58).
- Each row: `source`, `licence`, `first_seen`, `last_seen`; removal from a source sets `delisted_at` (keep history).
- Lookup API `mt_curation.blocklist.check(domain|address)` with in-memory bloom/set cache, p99 < 1 ms.
- Failure: last good list kept; staleness > 24 h alerts and marks link rendering as "verification degraded".

## ToDo

- [ ] Write Prefect flows in `packages/mt_curation/blocklists/` with source adapters.
- [ ] Add cache + lookup API; publish refresh metrics to Prometheus.
- [ ] Record licences in `third_party/LICENSES.md` notes (data use only, no redistribution).
- [ ] Tests; doc sync.

## Verification

### Tests
- Unit: normalisation (punycode lookalike `xn--` domains, mixed-case addresses).
- Integration: refresh from fixture repos twice → idempotent; a delisted entry gets `delisted_at`.
- Benchmark: lookup p99 < 1 ms with 500k entries.

### Scenarios
- Given ScamSniffer adds a drainer domain, when the next refresh runs, then a task link to it renders as plain text and risk scoring hard-fails the project.

### Stress / failure injection
- Source repo unavailable for 48 h: alerts fire, last good list used, no empty-list window.

## Acceptance criteria

- [ ] Four sources refreshed on schedule with provenance
- [ ] Lookup API fast and shared
- [ ] Staleness alerting works

## Exceptions & edge cases

- Licence of eth-phishing-detect/ScamSniffer unverified (U): private use only, no redistribution.

## Cardinal rules (do NOT)

- Do NOT redistribute blocklist data; do NOT exceed the Chainabuse rate limit.
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: refresh cadences.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.42 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T031-ops-blocklist-refresh-jobs`
- PR title: `P5-T031: Blocklist refresh jobs (MetaMask, ScamSniffer, polkadot-js, Chainabuse)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T031` run

## Progress log

- 2026-10-21 00:00 · planner · created
