---
id: P4-T024
kind: task
title: Conditional StockTwits and YouTube connectors (behind reachability checks)
phase: 4
type: BUILD
status: backlog
priority: low
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010, P1-T056]
requirements: [R4.05]
roadmap_todos: [T4.22]
modules: [M2]
dashboards: [D08]
tools: [uv, git]
mcp: []
env: []
services: [nats, postgres]
branch: p4/P4-T024-stocktwits-youtube-conditional
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

# P4-T024 · Conditional StockTwits and YouTube connectors (behind reachability checks)

## Goal / expected outcome

StockTwits (`streams/symbol/{SYM}`) and YouTube (channel RSS + Data API v3 metadata; yt-dlp subtitles for earnings calls) connectors exist **behind feature flags** that are switched on only when their reachability/terms checks pass: StockTwits from P1-T056 (T1.60), YouTube from the Phase 4 check P4-T066 (T4.65), which runs after this build and flips the flag. If a check fails, the source shows as disabled with the reason in D08.

## Context & references

- Roadmap: [R4.05](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.22](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Sources: [06 §2 conditional rows](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) · [06 §3 open checks](../../../docs/06-aggregators-and-market-providers.md#3-additional-forex--multi-asset-providers)
- Cross-phase: P1-T056 (T1.60 StockTwits reachability) is a `depends_on` entry.
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P4-B005): the YouTube check moved to Phase 4 as its own VERIFY task, P4-T066 ([R4.05](../../../docs/roadmap/phase-4-intel.md#3-requirements), [06 §2](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack)).

## Requirements

- Feature flags `sources.stocktwits.enabled`, `sources.youtube.enabled` default false.
- `ops.source_check` table (source, check, result, reason, checked_at) that P4-T066 writes; the YouTube flag reads it.
- StockTwits: per-symbol polling within published limits; skip silently if T1.60 failed.
- YouTube transcripts stored as documents (`doc_type=transcript`), linked to tickers via the channel config.

## ToDo

- [ ] `ops.source_check` migration + flag resolver (the YouTube check script itself is P4-T066).
- [ ] StockTwits connector (flagged).
- [ ] YouTube RSS + metadata + subtitle connector (flagged).
- [ ] D08 Sources disabled-reason field.
- [ ] Tests with fixtures.

## Verification

### Tests
- Unit: both connectors on fixtures.
- Unit: flag off → connector never schedules.
- Integration: a seeded `ops.source_check` pass/fail row switches the YouTube flag on/off.

### Scenarios
- Given T1.60 recorded StockTwits as unreachable, then the StockTwits source is disabled with that reason.
- Given the YouTube quota is exhausted, then pause until the daily reset.

### Stress / failure injection
- n/a: low volume; quota-bound.

## Acceptance criteria

- [ ] StockTwits flag set from the P1-T056 result; YouTube stays off until P4-T066 records a pass; connectors enabled only if checks pass
- [ ] Disabled reasons visible in D08 Sources
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- yt-dlp breakage on YouTube changes: pin; failures are non-fatal (metadata still ingests).

## Cardinal rules (do NOT)

- Do NOT scrape StockTwits HTML if the API is unavailable.
- Do NOT download video; subtitles/metadata only.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: §3 open checks: add the YouTube check and its result
- `docs/roadmap/phase-4-intel.md`: tick T4.22 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T024-stocktwits-youtube-conditional`
- PR title: `P4-T024: Conditional StockTwits and YouTube connectors (behind reachability checks)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T024` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (YouTube check moved to new VERIFY P4-T066 (17 §D P4-B005, T4.65); depends on P1-T056 for StockTwits)
