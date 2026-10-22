---
id: P4-T066
kind: task
title: YouTube check: channel RSS, Data API v3 quota and yt-dlp subtitles
phase: 4
type: VERIFY
status: backlog
priority: low
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T024, P4-T003, P4-T005]
requirements: [R4.05]
roadmap_todos: [T4.65]
modules: [M2]
dashboards: [D08]
tools: [uv, yt-dlp, git]
mcp: []
env: [YOUTUBE_API_KEY]
services: [youtube-data-api]
branch: p4/P4-T066-youtube-check-channel-rss-data-api-v3-quota-and-
pr: ""
doc_sync: [docs/06-aggregators-and-market-providers.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P4-T066 · YouTube check: channel RSS, Data API v3 quota and yt-dlp subtitles

## Goal / expected outcome

A recorded pass/fail decides whether YouTube joins as a source: channel RSS reachable for your chosen channels, the Data API v3 free quota (10,000 units/day) covers the planned polling with headroom, and yt-dlp subtitle fetches work for those channels within YouTube's terms. The result is written to `ops.source_check`, flips `sources.youtube.enabled` (P4-T024) only on a pass, and is recorded in 06.

## Context & references

- Roadmap: [R4.05](../../../docs/roadmap/phase-4-intel.md#3-requirements) (YouTube only if its P4 check passes) · ToDo [T4.65](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P4-B005): the YouTube check moves to P4 · [06 §2 Conditional row + Phase 4 check](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack)
- Keys last: this is the late live check; the connector was built on fixtures in P4-T024. Your inputs: channels (P4-T003), optional free Data API key (P4-T005)
- Related: P4-T024 (flagged connector), P4-T056 (terms review).

## Requirements

- `ops/checks/youtube_check.py`: (1) channel RSS (`/feeds/videos.xml?channel_id=`) returns entries for each chosen channel; (2) Data API v3 key works and the planned call budget (videos.list/channels.list per day) is ≤ 50% of the 10,000-unit free quota (configurable); (3) yt-dlp fetches subtitles for one recent video per channel without login/cookies.
- The key is read only for this check session (`sops exec-env`), never printed or logged.
- Result row in `ops.source_check` (source `youtube`, per-check result, reason, checked_at); the flag flips on only when all three pass; pass/fail with date recorded in 06.
- Terms: no downloading of video/audio, subtitles only; no circumvention of age/region gates.

## ToDo

- [ ] Write `ops/checks/youtube_check.py` (+ unit tests on recorded responses)
- [ ] Run it on your channel list with your key
- [ ] Record the result in `ops.source_check` and 06; set the flag accordingly
- [ ] If it passed, confirm the connector schedules and stays within quota for 24 h

## Verification

### Tests
- Unit: each sub-check on recorded fixtures (pass, 404 channel, quota error, yt-dlp failure).
- Integration: a recorded pass row enables the flag; a fail row keeps it off with the reason in D08 Sources.

### Scenarios
- Given one channel has no subtitles, then that channel is excluded and the rest can pass.
- Given the quota estimate exceeds 50% of the free units, then the check fails with 'quota' and suggests fewer channels.
- Given you declined YouTube in P4-T005, then the check records 'declined' (start with `--force`; no key needed) and the flag stays off.

### Stress / failure injection
- n/a: one-off check; quota-bound.

## Acceptance criteria

- [ ] Check result recorded in `ops.source_check` and in 06 with the date
- [ ] Flag on only if all sub-checks passed; disabled reason visible in D08 Sources otherwise
- [ ] No key value in logs, output or the repo

## Exceptions & edge cases

- yt-dlp breakage after YouTube changes: record fail; metadata via RSS can still pass separately if you want a metadata-only source (new decision, not automatic).

## Cardinal rules (do NOT)

- Do NOT download video or audio; subtitles/metadata only.
- Do NOT use cookies, logins or region/age-gate circumvention.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file outside the repo ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: Phase 4 check: record pass/fail and date (the row there currently names P4-T024; point it to this task)
- `docs/roadmap/phase-4-intel.md`: tick T4.65

## Branch & PR

- Branch: `p4/P4-T066-youtube-check-channel-rss-data-api-v3-quota-and-`
- PR title: `P4-T066: YouTube check: channel RSS, Data API v3 quota and yt-dlp subtitles`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T066` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (T4.65 YouTube check moved to P4 (17 §D P4-B005); keys last)
