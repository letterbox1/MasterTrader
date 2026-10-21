---
id: P4-T013
kind: task
title: GDELT news volume, tone and event feed connector
phase: 4
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010]
requirements: [R4.01, R4.08]
roadmap_todos: [T4.20, T4.25]
modules: [M2, M3]
dashboards: [D07, D08]
branch: p4/P4-T013-gdelt-connector
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T013 · GDELT news volume, tone and event feed connector

## Goal / expected outcome

`mt_data.text.gdelt` pulls GDELT 2.0 15-minute updates (DOC/GKG for article volume and tone per keyword/country/theme; Events export for M3) and stores per-query volume/tone series plus article links, feeding both the news feed (M2) and global events (M3).

## Context & references

- Roadmap: [R4.01, R4.08](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDos [T4.20, T4.25](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Sources: [06 §2](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) · Spec: [03 M2](../../../docs/03-build-spec.md#m2-news--social--mt_datatext)
- Events: [03 M3](../../../docs/03-build-spec.md#m3-global-events--mt_dataevents)
- Related: P4-T034 (conflict events consume the GDELT events stream), P4-T040 (tone into sentiment).

## Requirements

- Poll the 15-min `lastupdate.txt` manifest; download only new files; verify MD5 from the manifest.
- Queries driven by `watchlist.yaml` keywords and the country list of the exposure map.
- Store tone/volume as `features`-ready series (`text.gdelt_tone`: query, bucket_15m, n_articles, avg_tone) and article URLs as headline-only documents (`display_ok` link only).
- Events export rows go to `raw.evt.gdelt` for P4-T034.

## ToDo

- [ ] Manifest poller + downloader + MD5 check.
- [ ] GKG/DOC parsers (CSV, tab-separated, zip).
- [ ] Tone/volume aggregator.
- [ ] Events export → `raw.evt.gdelt`.
- [ ] Fixtures + tests.

## Verification

### Tests
- Unit: parse a saved 15-min GKG file → expected tone/volume.
- Unit: MD5 mismatch → file rejected and retried.
- Integration: two consecutive manifests → only new file processed (idempotent).

### Scenarios
- Given GDELT skips a 15-min interval, then the gap is recorded (no interpolation) and DQ shows it.
- Given a backlog after downtime, then files are processed in order with original timestamps as `event_time`.

### Stress / failure injection
- Process 96 files (one day) in a backlog burst: completes < 10 min, memory < 1.5 GB.

## Acceptance criteria

- [ ] 15-min updates ingested continuously for 24 h with zero missed available files
- [ ] Tone/volume series queryable via `pit(as_of)`
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- GDELT URLs often point to paywalled pages: store link + GDELT metadata only.
- Postgres down (02 §9.3): raw items stay in `RAW_TEXT` and are processed on recovery; the connector itself never needs the DB.

## Cardinal rules (do NOT)

- Do NOT crawl every GDELT article URL; only fetch pages for watchlist-relevant items via P4-T011 rules.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT use unpinned images (`:latest`) or vendored code with telemetry/referral IDs; pin by digest.

## Doc sync on completion

- `docs/03-build-spec.md`: M2/M3: note GDELT dual use and tables
- `docs/roadmap/phase-4-intel.md`: tick T4.20, T4.25 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T013-gdelt-connector`
- PR title: `P4-T013: GDELT news volume, tone and event feed connector`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T013` run

## Progress log

- 2026-10-21 00:00 · planner · created
