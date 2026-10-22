---
id: P4-T011
kind: task
title: RSS/Atom ingestion with trafilatura and crawl4ai extraction
phase: 4
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010, P4-T008]
requirements: [R4.01]
roadmap_todos: [T4.20]
modules: [M2]
dashboards: [D07, D08]
tools: [uv, git, docker]
mcp: []
env: []
services: [nats, crawl4ai]
branch: p4/P4-T011-rss-trafilatura-crawl4ai
pr: ""
doc_sync: [docs/06-aggregators-and-market-providers.md, docs/roadmap/phase-4-intel.md]
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

# P4-T011 · RSS/Atom ingestion with trafilatura and crawl4ai extraction

## Goal / expected outcome

`mt_data.text.rss` polls every feed in `feeds.yaml` (feedparser), fetches article pages and extracts main text with **trafilatura**, falling back to **crawl4ai** only for JS-rendered pages; it respects robots.txt and paywalls and publishes `RawTextItem`s on `raw.text.rss`.

## Context & references

- Roadmap: [R4.01](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.20](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Sources: [06 §2](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) · Spec: [03 M2](../../../docs/03-build-spec.md#m2-news--social--mt_datatext)
- Related: P4-T010 (framework), P4-T015 (central banks reuse this fetcher), P4-T012 (RSS-Bridge feeds use the same parser).

## Requirements

- Poll interval per feed (default 5 min, min 2 min) with ETag/Last-Modified; jittered schedule.
- Extraction order: feed `content:encoded` → trafilatura on the page → crawl4ai (headless, no cookies, 20 s timeout) only for `js: true` feeds.
- Paywalled feeds (`paywalled: true`): store title + summary + link only, `display_ok` full text false.
- robots.txt checked and cached 24 h; disallowed paths are not fetched (headline only).
- Max page size 2 MB; non-HTML content types skipped.

## ToDo

- [ ] Implement `RssConnector` on the P4-T010 base (feedparser + httpx).
- [ ] Implement `extract.py` (trafilatura with `favor_precision`, crawl4ai client over the `scrape` network).
- [ ] Approx-timestamp handling via the shared normaliser.
- [ ] Record fixtures (10 real feeds, saved responses) for offline tests.
- [ ] Feed-level metrics: items/day, extraction failures, bytes.

## Verification

### Tests
- Unit: fixtures → expected title/body/published/approx flags.
- Unit: robots.txt disallow → no page fetch.
- Integration: local HTTP fixture server + crawl4ai container extracts a JS-only page.

### Scenarios
- Given a feed repeats the same item with a new guid, then dedupe (P4-T026) collapses it via content hash.
- Given a page returns 403 for our User-Agent, then the item is stored headline-only and the source is flagged, not retried with a spoofed UA.

### Stress / failure injection
- 300 feeds polled concurrently with 10% timeouts injected: no task starvation, p95 cycle < 2 min, memory < 1 GB.

## Acceptance criteria

- [ ] Every RSS source in `feeds.example.yaml` (and in your `feeds.yaml` if P4-T003 is done) ingests in a 24-h run; your full list is exercised in P4-T060
- [ ] Paywall + robots rules covered by tests
- [ ] D07 shows each feed's status
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Feeds with no dates: `published_at = ingested_at`, `published_approx = true`.
- Postgres down (02 §9.3): raw items stay in `RAW_TEXT` and are processed on recovery; the connector itself never needs the DB.

## Cardinal rules (do NOT)

- Do NOT spoof User-Agents or bypass paywalls.
- Do NOT persist crawl4ai cookies or browser profiles.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT use unpinned images (`:latest`) or vendored code with telemetry/referral IDs; pin by digest.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: §2: note poll defaults and extraction order
- `docs/roadmap/phase-4-intel.md`: tick T4.20 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T011-rss-trafilatura-crawl4ai`
- PR title: `P4-T011: RSS/Atom ingestion with trafilatura and crawl4ai extraction`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T011` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (no longer waits for your feed list (P4-T003): built on fixtures + example feeds, your list runs in P4-T060)
