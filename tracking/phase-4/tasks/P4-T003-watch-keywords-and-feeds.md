---
id: P4-T003
kind: task
title: Seed the watch keywords, cashtags and trusted feeds from the 06/12 defaults
phase: 4
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010, P4-T043, P1-T001]
requirements: [R4.01, R4.05]
roadmap_todos: [T4.03]
modules: [M2]
dashboards: [D08]
tools: [git, uv]
mcp: []
env: []
services: [supabase-postgres, mt-api]
branch: p4/P4-T003-watch-keywords-and-feeds
pr: ""
doc_sync: [docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P4-T003 · Seed the watch keywords, cashtags and trusted feeds from the 06/12 defaults

## Goal / expected outcome

`config/intel/watchlist.yaml` and `config/intel/feeds.yaml` exist, drafted by the agent from the docs' defaults, and are seeded into `text.source` and the watchlist through `mt-api` with source `seed`. The news and social connectors start from the P1 universe and the [06 §2](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) source stack instead of an empty list. Nothing is asked of you during the build: you review the lists once in the go-live pack (P7-T070) and can edit them in D08 any time.

## Context & references

- Roadmap: [R4.01, R4.05](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.03](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Sources: [06 §2](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) (wire/financial/crypto RSS; central banks Fed, ECB, BoE, BoJ, SNB, RBA, BoC, RBNZ; sites without feeds via RSS-Bridge: AP, Reuters, Economist WIB, Substack, Bundesbank, Binance blog; CryptoPanic; Jetstream filtered on cashtags and keywords) · [06 §3 Calendars & central banks](../../../docs/06-aggregators-and-market-providers.md#calendars--central-banks-m5--m3)
- Terms: [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (what each platform allows) · [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) (provenance flags per source)
- Keywords: the high-importance event kinds of [16 §2.8](../../../docs/16-configuration-and-safety-model.md#28-calendar-blackouts) (central-bank decisions, CPI, NFP, …) and the M3/M4 event words in [03 M2](../../../docs/03-build-spec.md#m2-news--social--mt_datatext).
- Decision: [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19): configurable values are seeded from the doc defaults and approved once in the go-live pack (P7-T070), never asked during the build.
- Cross-phase (`depends_on`): P1-T001 (seeded universe/watchlist: the cashtag list), P4-T010 (source registry, `source_terms.yaml`), P4-T043 (`intel.source.add` / `intel.watchlist.update` commands).
- Used by: P4-T060 (brief run) and P4-T066 (YouTube channels). The connectors (P4-T011, P4-T012, P4-T021–T023) are built on fixtures and the example files, so they don't wait for this.

## Requirements

- `watchlist.yaml`: `cashtags` from the P1 universe (e.g. `$BTC`, `$EURUSD`, `$SPY`), grouped by market type (crypto/FX/metals/energy/equities/macro); `keywords` from the 16 §2.8 high-importance event kinds and the M2/M3 event words (e.g. `FOMC`, `rate decision`, `CPI`, `NFP`, `ETF approval`, `exploit`, `token unlock`); a short `exclude` list of spam terms.
- `feeds.yaml`: per feed `url`, `kind` (rss/atom/site), `market_types`, `paywalled` (bool), `notes`, `seed_source` (the doc section it came from). The 06 §2 central banks and wire/financial/crypto feeds as `rss`/`atom`; the 06 §2 sites without feeds as `kind: site` (RSS-Bridge candidates, P4-T012).
- Only free sources. Every entry needs a `source_terms.yaml` entry with 12 §5 provenance flags; an entry whose terms forbid automated access or need a paid login is left out. Paywalled sites are headline + link only.
- Optional `youtube_channels` list in `feeds.yaml` (empty by default): used only by the YouTube check (P4-T066) and, if it passes, the YouTube connector (P4-T024).
- Seeded through `mt-api` (`intel.source.add`, `intel.watchlist.update`) with source `seed`; idempotent; never overwrites your edits (a row you changed keeps your value).

## ToDo

- [ ] Draft `config/intel/watchlist.yaml` from the P1 universe and the 16 §2.8 / 03 M2 keywords; draft `config/intel/feeds.yaml` from 06 §2
- [ ] Add a doc-parse test that checks every 06 §2 central bank and feed-less site appears (or is listed as excluded with the reason)
- [ ] `mt intel seed` command: validate both files with the `mt_data.text.config` schemas and seed them through `mt-api` with source `seed`
- [ ] Run it; D08 Sources lists the seeded sources with their provenance flags
- [ ] Tests; progress log; `./kanban done P4-T003`

## Verification

### Tests
- Both files validate with the `mt_data.text.config` schemas (no duplicate URLs, valid cashtags, every entry has a terms entry): `uv run pytest`.
- Re-running the seed changes nothing; a source you edited in D08 keeps your value after a re-seed.

### Scenarios
- Given a seeded feed URL returns 404 when first fetched, then D08 Sources shows it red and the agent replaces or drops it (logged).
- Given a fresh stack, when the seed runs, then D08 Sources lists ≥ 15 feeds/sites and the watchlist ≥ 20 cashtags/keywords.

### Stress / failure injection
- n/a: seed data.

## Acceptance criteria

- [ ] Both YAML files committed, schema-valid and seeded with source `seed`
- [ ] ≥ 20 cashtags/keywords and ≥ 15 feeds/sites listed

## Exceptions & edge cases

- Very broad keywords (e.g. 'market') flood the relevance gate; P4-T060 tunes them using hit-rate.
- If P1-T001's universe is not seeded yet, the cashtag group starts from the 06 §2 defaults and is re-seeded when it lands (idempotent).

## Cardinal rules (do NOT)

- Do NOT list sources whose terms forbid automated access or require a paid login.
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT overwrite a value you edited; numbers and lists come from the defaults files, never hard-coded.

## Doc sync on completion

- `docs/roadmap/phase-4-intel.md`: tick T4.03

## Branch & PR

- Branch: `p4/P4-T003-watch-keywords-and-feeds`
- PR title: `P4-T003: Seed the watch keywords, cashtags and trusted feeds from the 06/12 defaults`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T003` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (connectors no longer wait for this list (build on fixtures); optional YouTube channel list for P4-T066)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (converted from a USER task to an agent seed task per 17 §G: the lists are drafted from 06 §2 / 12 §4–5 / 16 §2.8 defaults and seeded through `mt-api` with source `seed`; you review them in the go-live pack P7-T070; services `supabase-postgres`, `mt-api`; depends on P4-T010, P4-T043, P1-T001)
