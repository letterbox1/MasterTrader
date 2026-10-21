---
id: P4-T003
kind: task
title: Provide watch keywords, cashtags and trusted feeds/sites
phase: 4
type: USER
status: backlog
priority: high
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R4.01, R4.05]
roadmap_todos: [T4.03]
modules: [M2]
dashboards: [D08]
branch: p4/P4-T003-watch-keywords-and-feeds
pr: ""
doc_sync: [docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T003 · Provide watch keywords, cashtags and trusted feeds/sites

## Goal / expected outcome

`config/intel/watchlist.yaml` and `config/intel/feeds.yaml` hold your cashtags/keywords (for Bluesky Jetstream, Mastodon, Farcaster, relevance boosting) and the RSS feeds / sites you trust (for RSS, RSS-Bridge and crawl4ai), so the news and social connectors start from your universe instead of a generic one.

## Context & references

- Roadmap: [R4.01, R4.05](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.03](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Sources: [06 §2](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) (feeds, RSS-Bridge for sites without feeds, Jetstream filtered on cashtags/keywords)
- Cross-phase: P1 T1.01 universe/watchlist (reuse it as the starting cashtag list).
- Unblocks: P4-T011 (RSS), P4-T012 (RSS-Bridge bridges), P4-T021–T023 (social keyword filters).

## Requirements

- `watchlist.yaml`: `cashtags` (e.g. `$BTC`, `$EURUSD`, `$SPY`), `keywords` (e.g. `FOMC`, `rate cut`, `ETF approval`), `exclude` (spam terms), per-market-type grouping (crypto/FX/metals/energy/equities/macro).
- `feeds.yaml`: per feed `url`, `kind` (rss/atom/site), `market_types`, `paywalled` (bool), `notes`. Sites without a feed are marked `kind: site` and become RSS-Bridge candidates.
- Only free sources; paywalled sites are headline + link only.

## ToDo

- [ ] Copy `config/intel/watchlist.example.yaml` → `watchlist.yaml`; seed it from your P1 universe; add macro keywords.
- [ ] Copy `config/intel/feeds.example.yaml` → `feeds.yaml`; list the wire/financial/crypto feeds you read, and sites without feeds you want bridged.
- [ ] Mark paywalled sources `paywalled: true`.
- [ ] Commit both files or hand them to the agent; later edits go through `intel.watchlist.update` / `intel.source.add` in D08.

## Verification

### Tests
- Agent validates both files with the `mt_data.text.config` pydantic schemas (no duplicate URLs, valid cashtags).

### Scenarios
- Given a feed URL returns 404 when first fetched, then D08 Sources shows it red and you replace it.

### Stress / failure injection
- n/a: human configuration step.

## Acceptance criteria

- [ ] Both YAML files committed and schema-valid
- [ ] ≥ 20 cashtags/keywords and ≥ 15 feeds/sites listed

## Exceptions & edge cases

- Very broad keywords (e.g. 'market') flood the relevance gate; P4-T060 tunes them using hit-rate.

## Cardinal rules (do NOT)

- Do NOT list sources whose terms forbid automated access or require a paid login.
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.

## Doc sync on completion

- `docs/roadmap/phase-4-intel.md`: tick T4.03

## Branch & PR

- Branch: `p4/P4-T003-watch-keywords-and-feeds`
- PR title: `P4-T003: Provide watch keywords, cashtags and trusted feeds/sites`
- PR checklist: no PR needed for the human step itself; the agent records the outcome (non-secret parts only) in this file and runs `./kanban done P4-T003`

## Progress log

- 2026-10-21 00:00 · planner · created
