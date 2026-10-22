---
id: P4-T021
kind: task
title: Bluesky Jetstream client filtered on cashtags and keywords
phase: 4
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010]
requirements: [R4.05]
roadmap_todos: [T4.22]
modules: [M2]
dashboards: [D07, D08]
tools: [uv, git]
mcp: []
env: []
services: [nats]
branch: p4/P4-T021-bluesky-jetstream
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

# P4-T021 · Bluesky Jetstream client filtered on cashtags and keywords

## Goal / expected outcome

`mt_data.text.bluesky` consumes the Bluesky **Jetstream** WebSocket (`app.bsky.feed.post` collection), filters posts locally on `watchlist.yaml` cashtags/keywords, resolves author handles via the atproto SDK only when needed, and publishes matches as `raw.text.bluesky`.

## Context & references

- Roadmap: [R4.05](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.22](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Sources: [06 §2 Bluesky row](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) (free and explicitly permitted)
- Research: [social-aggregators](../../../docs/research/social-aggregators.md)

## Requirements

- Jetstream with `wantedCollections=app.bsky.feed.post`, zstd compression on, cursor persisted for resume in a local state file on the `ingest-text` volume (scrape side has no DB route, 02 §3.1).
- Local filter: case-insensitive keyword/cashtag match + language filter; drop replies/reposts by default (config).
- Store post URI as canonical id; author DID; text; `untrusted=true`.
- Throughput: handle full-firehose rate on one core (filter before decode where possible).

## ToDo

- [ ] Jetstream client with cursor resume and reconnect.
- [ ] Compiled keyword matcher (Aho-Corasick).
- [ ] Publisher + tests + fixtures.

## Verification

### Tests
- Unit: matcher hits/misses on fixture posts.
- Integration: recorded Jetstream segment replay → expected matches.
- Unit: cursor resume after disconnect produces no gaps/duplicates.

### Scenarios
- Given the Jetstream instance is down, then fail over to the next public Jetstream host in config.
- Given a keyword list update via `intel.watchlist.update`, then the matcher reloads without restart.

### Stress / failure injection
- Replay 1 h of recorded firehose at 5× speed: CPU < 1 core, lag < 5 s.

## Acceptance criteria

- [ ] Matching posts ingested for 24 h from the public Jetstream (keyless) using the example watchlist; lag metric < 5 s p95
- [ ] Cursor resume proven
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Firehose spikes: drop non-matching posts early; never buffer the unfiltered stream to disk.
- Postgres down (02 §9.3): raw items stay in `RAW_TEXT` and are processed on recovery; the connector itself never needs the DB.

## Cardinal rules (do NOT)

- Do NOT post, like or follow from any account.
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT use unpinned images (`:latest`) or vendored code with telemetry/referral IDs; pin by digest.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: §2 Bluesky row: Jetstream hosts used
- `docs/roadmap/phase-4-intel.md`: tick T4.22 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T021-bluesky-jetstream`
- PR title: `P4-T021: Bluesky Jetstream client filtered on cashtags and keywords`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T021` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (no longer waits for your keyword list (P4-T003): example watchlist, your list runs in P4-T060)
- 2026-10-22 00:00 · aligner · cursor moved from `ops.cursor` to a local state file (scrape side has no DB route, 02 §3.1)
