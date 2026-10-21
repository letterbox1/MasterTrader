---
id: P4-T002
kind: task
title: Follow Discord announcement channels into the feeds server
phase: 4
type: USER
status: backlog
priority: high
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R4.04]
roadmap_todos: [T4.02]
modules: [M2]
dashboards: [D08]
branch: p4/P4-T002-discord-follows
pr: ""
doc_sync: [docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T002 · Follow Discord announcement channels into the feeds server

## Goal / expected outcome

Your private "MasterTrader Feeds" Discord server receives cross-posts from the public announcement channels you care about, spread over `#mt-inbox` and category channels at ≈10–15 follows per receiving channel, so the Discord bot (P4-T020) can ingest them.

## Context & references

- Roadmap: [R4.04](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.02](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Source stack: [06 §2 Discord row](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) (Follow works only for Community-server announcement channels)
- Policy: [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (own bot, added by an admin; no self-bots/user tokens)
- Cross-phase: P0 T0.07 (feeds server + bot app with Message Content intent).
- Unblocks: P4-T020 ingest test; P5 discovery (Discord inbox).

## Requirements

- Follow only **announcement channels the project actually publishes** (the 'Follow' button), from your normal Discord account.
- Spread follows: ≤ 15 per receiving channel; create category channels such as `#crypto-projects`, `#exchanges`, `#macro-news`, `#defi` when one fills up.
- Record each follow in `config/intel/discord_follows.yaml`: `source_server`, `source_channel`, `receiving_channel`, `topic`, `date`.

## ToDo

- [ ] In each project's server, open its announcement channel → **Follow** → choose `MasterTrader Feeds` → the receiving channel.
- [ ] When a receiving channel reaches ~12 follows, create the next category channel and continue there.
- [ ] Fill `config/intel/discord_follows.yaml` (no secrets) and commit it, or hand it to the agent.
- [ ] After P4-T020 is deployed, check D08 Sources shows each receiving channel with items/day > 0 within 48 h.

## Verification

### Tests
- Agent runs `python -m mt_data.text.discord.validate_follows` (schema, ≤ 15 per receiving channel).

### Scenarios
- Given a receiving channel has 16 follows, when validated, then it warns and suggests a new category channel.
- Given a project has no announcement channel, then skip it (no self-bot alternative).

### Stress / failure injection
- n/a: human configuration step.

## Acceptance criteria

- [ ] ≥ 1 receiving channel populated; `discord_follows.yaml` committed and valid
- [ ] No receiving channel above 15 follows

## Exceptions & edge cases

- Projects that delete or rename the announcement channel break the webhook silently; P4-T020 flags channels with no posts in 14 days.

## Cardinal rules (do NOT)

- Do NOT use a self-bot, user token or browser automation to read Discord.
- Do NOT add the bot to servers you don't administer.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.

## Doc sync on completion

- `docs/roadmap/phase-4-intel.md`: tick T4.02

## Branch & PR

- Branch: `p4/P4-T002-discord-follows`
- PR title: `P4-T002: Follow Discord announcement channels into the feeds server`
- PR checklist: no PR needed for the human step itself; the agent records the outcome (non-secret parts only) in this file and runs `./kanban done P4-T002`

## Progress log

- 2026-10-21 00:00 · planner · created
