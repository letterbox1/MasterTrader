---
id: P5-T047
kind: task
title: Community curation: official invites, follow channel, leave-when and Discord delivery verification
phase: 5
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T029, P5-T034, P5-T031, P4-T020]
requirements: [R5.21, R5.20]
roadmap_todos: [T5.30]
modules: [M19, M2]
dashboards: [D13]
tools: [uv]
mcp: []
env: []
services: [postgres, nats]
branch: p5/P5-T047-community-curation-discord-delivery
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T047 · Community curation: official invites, follow channel, leave-when and Discord delivery verification

## Goal / expected outcome

The curation queue proposes at most 3 new servers a week (default, configurable), with invites from **official sources only** (CoinGecko `links.chat_url`, project site/docs footers, official X bio, governance forums), blocklist- and domain-verified, naming **which announcement channel to Follow**, the destination inbox channel and a "leave when" condition; after you tap Done the bot verifies posts are arriving and re-prompts if nothing arrives within 7 days (default, configurable; 16 §2.13).

## Context & references

- Roadmap: [R5.21](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.30 · delivery test P5-T061
- [08 Discord curation queue](../../../docs/08-airdrops-and-token-launches.md#discord-curation-queue) · [research Discord facts](../../../docs/research/airdrops-rugpull-discord.md) · [D13 Communities tab](../../../docs/ui/dashboards/D13-tasks-curation.md)
- P4 Discord bot ingesting `#mt-inbox` (P4-T020); defaults: 7-day re-prompt and ≤ 3 new servers per week ([16 §2.13](../../../docs/16-configuration-and-safety-model.md#213-curation); decision P5-B011)

## Requirements

- Sources and verification: invite host must be `discord.gg`/`discord.com/invite` (or `t.me` for Telegram) found on an official source; the invite's guild name/icon is checked via the public invite endpoint; cross-checked with the verified domain and blocklists.
- Ranking: ≤ 3 new servers/week by default (config), prioritised by viability/EV and deadline; Telegram channels respect the 500-channel cap (12 §4); X follows and Galxe spaces use the same queue.
- Entry fields: project, platform, verified invite, announcement channel name to Follow, destination channel (`#mt-inbox` or category), status (suggested/joined/following/verified/left), last post received, leave-when (e.g. 30 days after claim).
- Delivery verification: after Done, watch P4 Discord ingest for messages whose webhook source = the followed channel; verified on first post; if none in 7 days (default, configurable) → re-prompt task; leave-when reached → `leave` task.
- Bot never joins servers or follows channels itself (no self-bots).

## ToDo

- [ ] Implement `packages/mt_curation/community/` (invite discovery from observations, verifier, ranker, delivery watcher, leave-when scheduler), entries stored in `curation.community`.
- [ ] Map P4 Discord follow-webhook metadata to curation entries.
- [ ] Tests with recorded invite/webhook fixtures; doc sync.

## Verification

### Tests
- Unit: invite from a non-official page is discarded; lookalike guild name flagged.
- Integration: Done → first ingested post from the followed channel flips status to `verified`.
- Unit: no post in 7 days → re-prompt task created once (not daily spam).

### Scenarios
- Given CoinGecko `chat_url` and the project site footer show different invites, then the entry is held for manual review with both links (verified-via tags).
- Given the user tapped Done but followed the wrong channel, then posts from another channel don't verify it and the re-prompt names the correct channel.

### Stress / failure injection
- n/a: low volume (a few entries per week)

## Acceptance criteria

- [ ] Official-source-only invites with verification
- [ ] ≤ configured new servers per week
- [ ] Delivery verification and re-prompt working
- [ ] Leave-when tasks generated

## Exceptions & edge cases

- Discord invite endpoint rate-limited: defer verification; never mark verified without evidence.
- Message Content intent limits (< 100 servers toggle) documented; the bot only reads our own server.

## Cardinal rules (do NOT)

- Do NOT use self-bots, user tokens or automated joins/follows.
- Do NOT surface invites found only in Telegram chats or DMs.
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.
- Do NOT let Telegram text reach any model, RAG index or training set; Telegram contributes deterministic postures only (12 §4–5).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: confirm the Discord queue text matches the build (the 7-day and ≤ 3 per week defaults are already in 08 and 16 §2.13).
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.30 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T047-community-curation-discord-delivery`
- PR title: `P5-T047: Community curation: official invites, follow channel, leave-when and Discord delivery verification`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T047` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (Discord 7 days / ≤ 3 servers per week defaults per 16 §2.13/P5-B011; `curation.community`; P4 Discord dep)
