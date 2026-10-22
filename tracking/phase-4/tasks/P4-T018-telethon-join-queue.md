---
id: P4-T018
kind: task
title: Telethon client and FLOOD_WAIT-aware join queue (≤ 500 channels)
phase: 4
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010]
requirements: [R4.02]
roadmap_todos: [T4.21]
modules: [M2]
dashboards: [D07, D08]
tools: [uv, git]
mcp: []
env: []
services: [nats]
branch: p4/P4-T018-telethon-join-queue
pr: ""
doc_sync: [docs/03-build-spec.md, docs/runbooks/social-accounts.md, docs/roadmap/phase-4-intel.md]
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

# P4-T018 · Telethon client and FLOOD_WAIT-aware join queue (≤ 500 channels)

## Goal / expected outcome

`mt_data.text.telegram` runs a pinned Telethon client on the dedicated account, joins channels from `telegram_channels.yaml` through a persistent, rate-limited join queue that honours `FLOOD_WAIT` exactly, never exceeds 500 joined channels, and streams new messages **in memory only** to the posture extractor (P4-T019). Built and tested against a fake Telethon client and a fixture channel list; joining real channels on your account is the live check P4-T068 (keys last).

## Context & references

- Roadmap: [R4.02](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.21](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Policy: [12 §4 Telegram](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (honour FLOOD_WAIT, rate-limited queue, cap 500; no mass-join, member lists, auto-DM/forward, read-receipt tricks)
- Spec: [03 M2](../../../docs/03-build-spec.md#m2-news--social--mt_datatext) · Accounts: [07 §10](../../../docs/07-security-notes.md#10-social--scraping-accounts)
- Time-sensitive: [06 §0](../../../docs/06-aggregators-and-market-providers.md#0-️-time-sensitive-actions) (Telethon archived on GitHub, moved to Codeberg → pin)
- Related: P4-T006 (session mechanism), P4-T019 (postures), P4-T068 (live check). Decision: [17 §A](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (P4-B001): Telegram → regex extractor → postures → code/policy only ([02 F3b](../../../docs/02-v1-architecture.md#8-end-to-end-flows)).

## Requirements

- Join queue persisted in a local SQLite state file on the `ingest-text` volume (`/data/ingest-text/telegram_join_queue.db`: handle, priority, state, attempts, next_attempt_at, last_error), because the scrape network has no route to Postgres ([02 §3.1](../../../docs/02-v1-architecture.md#31-networks)); queue state (joined count, paused-until) is published in the Telegram `feed_status` entry for D08 Sources.
- Join pacing (configurable defaults in `config/intel/telegram.yaml`): at most 1 join per 10–20 min (jittered) and ≤ 20 per day; on `FloodWaitError(seconds)` sleep **exactly** `seconds` + jitter and pause the whole queue.
- Hard cap: refuse to join when joined count ≥ 500; leaving a channel is manual (or on ban/private).
- Read-only: no sending, forwarding, reacting, read-receipt manipulation or member-list calls; client wrapper exposes only the allowed methods.
- Messages are handed to the extractor in memory; **message text is never persisted** and never published to NATS.
- Reconnect with backoff; session from tmpfs (P4-T006).

## ToDo

- [ ] Pin Telethon version (Codeberg) in `uv.lock`; vendor notes in `third_party/LICENSES.md` if vendored.
- [ ] `TelegramClientWrapper` exposing only `join_channel`, `iter_new_messages`, `get_entity` (allow-list); everything else raises.
- [ ] Join queue worker + local SQLite state file + state metrics.
- [ ] Validator for `telegram_channels.yaml` (cap, public handles).
- [ ] Health/heartbeat + `feed_status` for Telegram.
- [ ] Tests below.

## Verification

### Tests
- Unit: fake Telethon raising `FloodWaitError(347)` → queue sleeps 347 s + jitter (fake clock) and no other join is attempted meanwhile.
- Unit: 501st join refused; state `cap_reached`.
- Unit: wrapper raises on any non-allow-listed method (send_message, get_participants, …).
- Integration: messages flow to the extractor callback; nothing with `.text` is written to DB/NATS (spy on writers).

### Scenarios
- Given the account gets a 24-h FLOOD_WAIT, then joins pause 24 h, ingestion of already-joined channels continues, D08 Sources shows 'join paused until …'.
- Given a channel goes private, then it is marked `lost` and not retried.
- Given the process restarts mid-queue, then it resumes from the local queue state file without double-joining.

### Stress / failure injection
- Inject random FLOOD_WAITs (1 s–24 h) over 500 queued joins in simulation: cap never exceeded, total joins/day ≤ limit, no tight retry loops.

## Acceptance criteria

- [ ] Join queue honours FLOOD_WAIT exactly and never exceeds 500 (tests)
- [ ] Allow-list wrapper prevents any write action (tests)
- [ ] No Telegram text persisted anywhere (spy test)
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Account restriction/ban: stop all Telegram activity, alert critical, require a manual review; never create a new account automatically.
- Telethon breaking change: pinned; upgrades go through a dedicated PR.

## Cardinal rules (do NOT)

- Do NOT mass-join, scrape member lists, auto-DM, forward or react.
- Do NOT persist or publish Telegram message text.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT use unpinned images (`:latest`) or vendored code with telemetry/referral IDs; pin by digest.

## Doc sync on completion

- `docs/03-build-spec.md`: M2 Telegram: document join pacing defaults
- `docs/runbooks/social-accounts.md`: FLOOD_WAIT / ban handling
- `docs/roadmap/phase-4-intel.md`: tick T4.21 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T018-telethon-join-queue`
- PR title: `P4-T018: Telethon client and FLOOD_WAIT-aware join queue (≤ 500 channels)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T018` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (F3b postures-only per 17 §A P4-B001; built on a fake client, live joins moved to P4-T068; dropped P4-T006/P4-T001 dependencies)
- 2026-10-22 00:00 · aligner · join-queue state moved from `ops.tg_join_queue` to a local state file (scrape side has no DB route, 02 §3.1)
