---
id: P4-T022
kind: task
title: Mastodon/fediverse client (hashtags and followed accounts)
phase: 4
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010, P4-T012]
requirements: [R4.05]
roadmap_todos: [T4.22]
modules: [M2]
dashboards: [D07, D08]
tools: [uv, git]
mcp: []
env: []
services: [nats, rss-bridge]
branch: p4/P4-T022-mastodon-client
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

# P4-T022 · Mastodon/fediverse client (hashtags and followed accounts)

## Goal / expected outcome

`mt_data.text.mastodon` uses Mastodon.py against public hashtag timelines and followed accounts on configured instances (or RSS-Bridge's MastodonBridge where signed fetch blocks API access), publishing `raw.text.mastodon` items.

## Context & references

- Roadmap: [R4.05](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.22](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Sources: [06 §2 Mastodon row](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) · research: MastodonBridge works, some instances need signed fetch

## Requirements

- Config `config/intel/mastodon.yaml`: instances, hashtags, accounts.
- Poll every 5 min with `since_id`; respect instance rate-limit headers.
- Fallback to MastodonBridge for instances that require signed fetch.

## ToDo

- [ ] Client + since_id persistence.
- [ ] Bridge fallback via P4-T012.
- [ ] Tests + fixtures.

## Verification

### Tests
- Unit: fixture timeline → items; since_id honoured.
- Unit: rate-limit header parsing → throttle.

### Scenarios
- Given an instance blocks unauthenticated reads, then fallback to the bridge and flag the source.

### Stress / failure injection
- n/a: low volume.

## Acceptance criteria

- [ ] Configured hashtags/accounts ingest for 24 h
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Postgres down (02 §9.3): raw items stay in `RAW_TEXT` and are processed on recovery; the connector itself never needs the DB.

## Cardinal rules (do NOT)

- Do NOT post or boost.
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: §2 Mastodon row: instances used
- `docs/roadmap/phase-4-intel.md`: tick T4.22 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T022-mastodon-client`
- PR title: `P4-T022: Mastodon/fediverse client (hashtags and followed accounts)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T022` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (added P4-T012 dependency (bridge fallback is a true precondition))
