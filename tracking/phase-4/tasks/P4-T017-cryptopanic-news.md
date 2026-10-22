---
id: P4-T017
kind: task
title: CryptoPanic free-tier news connector with attribution
phase: 4
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010]
requirements: [R4.01]
roadmap_todos: [T4.20]
modules: [M2]
dashboards: [D07, D08]
tools: [uv, git]
mcp: []
env: []
services: [nats]
branch: p4/P4-T017-cryptopanic-news
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

# P4-T017 · CryptoPanic free-tier news connector with attribution

## Goal / expected outcome

`mt_data.text.cryptopanic` pulls CryptoPanic's free-tier posts (with votes) for watchlist currencies, stores headlines + links with required attribution, and exposes the vote counts as a crypto sentiment input. Built and tested on recorded fixtures without a key; the live run with your key is P4-T067.

## Context & references

- Roadmap: [R4.01](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.20](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Sources: [06 §2](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) · Spec: [03 M2](../../../docs/03-build-spec.md#m2-news--social--mt_datatext)
- D08: [Additions](../../../docs/ui/dashboards/D08-intel.md) (new sources: Farcaster, CryptoPanic)
- Related: P4-T040 (crypto sentiment).

## Requirements

- Poll within free-tier limits (configurable, default every 5 min) using the key from secrets.
- Store `votes` (positive/negative/important/…) in `entities`/metadata; attribution string displayed in D08 for every item.
- Provenance per `source_terms.yaml`.

## ToDo

- [ ] Connector + quota budget.
- [ ] Attribution field rendered by D08 (contract field `attribution`).
- [ ] Fixtures + tests.

## Verification

### Tests
- Unit: fixture parsing incl. votes.
- Unit: attribution present on every stored item.

### Scenarios
- Given the free tier is withdrawn (terms change), then the source is disabled with a reason in D08 Sources.

### Stress / failure injection
- n/a: low volume.

## Acceptance criteria

- [ ] Fixture replay ingests items + votes with attribution on every item (the live 24-h run is P4-T067)
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Postgres down (02 §9.3): raw items stay in `RAW_TEXT` and are processed on recovery; the connector itself never needs the DB.

## Cardinal rules (do NOT)

- Do NOT strip attribution or republish items.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT use unpinned images (`:latest`) or vendored code with telemetry/referral IDs; pin by digest.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: §2 CryptoPanic row: attribution handling
- `docs/roadmap/phase-4-intel.md`: tick T4.20 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T017-cryptopanic-news`
- PR title: `P4-T017: CryptoPanic free-tier news connector with attribution`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T017` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (build first, keys last: fixtures only, live run moved to P4-T067; dropped P4-T005 dependency)
