---
id: P4-T020
kind: task
title: Discord bot ingesting followed announcement channels
phase: 4
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010, P4-T006, P4-T002]
requirements: [R4.04]
roadmap_todos: [T4.22]
modules: [M2]
dashboards: [D07, D08]
branch: p4/P4-T020-discord-bot-ingest
pr: ""
doc_sync: [docs/06-aggregators-and-market-providers.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T020 · Discord bot ingesting followed announcement channels

## Goal / expected outcome

A discord.py bot (your bot application, added by you as admin to your own feeds server) with the Message Content intent ingests cross-posted announcements from the receiving channels in `discord_follows.yaml`, maps each post back to its source server/channel, and publishes `raw.text.discord` items.

## Context & references

- Roadmap: [R4.04](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.22](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Sources: [06 §2 Discord row](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) · Policy: [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)
- Cross-phase: P5 R5.21 (bot verifies delivery after a follow task) reuses this bot.
- Related: P4-T002 (follows), P4-T006 (token).

## Requirements

- Intents: guilds, guild_messages, message_content; bot only in servers you administer (startup check: leave any other guild and alert).
- Ingest only channels listed as receiving channels; capture `webhook_id`/crosspost reference → original server/channel name.
- Store message content as text (attachments as links only), embeds flattened, `untrusted=true`.
- Flag receiving channels with no posts for 14 days ('follow broken?').
- Backfill the last 100 messages per channel on first start (rate-limit aware).

## ToDo

- [ ] Bot service in `ingest-text` (discord.py pinned).
- [ ] Follow-map loader + crosspost source resolver.
- [ ] Guild allow-list guard.
- [ ] Backfill + live listener; heartbeat; `feed_status`.
- [ ] Tests with discord.py test doubles.

## Verification

### Tests
- Unit: crosspost message fixture → original source resolved.
- Unit: bot in an unexpected guild → leaves + alert.
- Integration: mocked gateway events → `raw.text.discord`.

### Scenarios
- Given Discord gateway disconnects, then the bot resumes with session resume and backfills missed messages from the last seen id.
- Given a followed project deletes its channel, then the receiving channel goes quiet and is flagged after 14 days.

### Stress / failure injection
- Burst of 1,000 messages in 1 min across channels: no drops, respects Discord rate limits on backfill.

## Acceptance criteria

- [ ] Receiving channels ingest live for 48 h
- [ ] Guild allow-list guard proven by test
- [ ] No user token anywhere in the code path
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Message Content intent policy can change (U as of Jun 2026): if revoked, alert and fall back to embeds/titles only.
- Postgres down (02 §9.3): raw items stay in `RAW_TEXT` and are processed on recovery; the connector itself never needs the DB.

## Cardinal rules (do NOT)

- Do NOT use self-bots, user tokens or browser automation.
- Do NOT post, react or DM from the bot in P4.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT use unpinned images (`:latest`) or vendored code with telemetry/referral IDs; pin by digest.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: §2 Discord row: confirm intent status and follow limits observed
- `docs/roadmap/phase-4-intel.md`: tick T4.22 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T020-discord-bot-ingest`
- PR title: `P4-T020: Discord bot ingesting followed announcement channels`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T020` run

## Progress log

- 2026-10-21 00:00 · planner · created
