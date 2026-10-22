---
id: P0-T008
kind: task
title: Create the private Discord feeds server and bot application
phase: 0
type: USER
status: ready
priority: medium
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: []
roadmap_todos: [T0.07]
modules: [M2, M19]
dashboards: []
tools: []
mcp: []
env: []
services: [discord]
branch: p0/P0-T008-discord-server-and-bot
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md]
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

# P0-T008 · Create the private Discord feeds server and bot application

## Goal / expected outcome

A private Discord server "MasterTrader Feeds" with `#mt-inbox` and category channels, a bot application with the Message Content intent added to it, and the first announcement-channel follows in place, so P4 ingest has data waiting.

## Context & references

- [Roadmap P0 T0.07](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [06 §2 social stack](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack)
- [07 §10 social accounts](../../../docs/07-security-notes.md#10-social--scraping-accounts)
- [12 §4 platform rules](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)
- [04 do-this-week](../../../docs/04-plan-of-action.md#️-do-this-week-regardless-of-phase)
- [P4 roadmap](../../../docs/roadmap/phase-4-intel.md)
- Unblocks: P4 Discord ingest

## Requirements

- Server: private; channels `#mt-inbox` + categories (e.g. `crypto-projects`, `exchanges`, `macro`, `airdrops`), ≤ ~10–15 follower webhooks per receiving channel.
- Bot app at the Discord developer portal: name `MasterTrader Reader`, **Message Content intent** on (self-serve under 10k servers), permissions View Channels + Read Message History only; added only to your server.
- Follows: use Discord's **Follow** button on public announcement channels you already know; spread across category channels.
- Outputs: `bot_token`, `application_id`, `guild_id`, channel ids → the sops secrets file `~/.config/mastertrader/secrets.sops.yaml` (created by the secrets task, P0-T022) under `discord:`. Until the secrets file exists, keep values **only** in your password manager; never in chat, email, git, issues or notes apps.

## ToDo

- [ ] Create the server and the channels above.
- [ ] Create the bot application, enable Message Content intent, generate the token, invite it with minimal permissions via an OAuth2 URL.
- [ ] Follow the announcement channels you already know (log how many).
- [ ] Record ids and token; move them to the secrets file once P0-T022 lands.

## Verification

### Tests
- Confirmation: the bot shows as a member (offline) in the server; follows deliver at least one cross-post within a week.

### Scenarios
- Given a project posts an announcement, when you follow its channel, then it appears in your category channel and P4's bot can read it.

### Stress / failure injection
- n/a: account action.

## Acceptance criteria

- [ ] Server and channels exist
- [ ] Bot app created with Message Content intent and read-only permissions in your server only
- [ ] ≥ 1 follow active
- [ ] Token stored only in password manager / secrets file

## Exceptions & edge cases

- A project has no announcement channel: it can't be followed; never use a user token or self-bot to read it.

## Cardinal rules (do NOT)

- Do NOT use self-bots or user tokens (Discord ToS; 12 §4).
- Do NOT give the bot admin or send-message permissions.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, ToS-breaking scraping, self-bots or user tokens; free tiers only ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- None beyond this task's log.
- `docs/roadmap/phase-0-foundations.md`: tick T0.07 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T008-discord-server-and-bot`
- PR title: `P0-T008: Create the private Discord feeds server and bot application`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T008` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (secrets file path → `~/.config/mastertrader/`, outside the repo (17 §D P0-B018); run fields added)
