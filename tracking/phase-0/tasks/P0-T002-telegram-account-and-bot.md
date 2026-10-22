---
id: P0-T002
kind: task
title: Set up the dedicated Telegram identity, api_id/api_hash and alert bot
phase: 0
type: USER
status: ready
priority: high
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: []
roadmap_todos: [T0.06]
modules: [M2, M15]
dashboards: []
tools: []
mcp: []
env: []
services: [telegram]
branch: p0/P0-T002-telegram-account-and-bot
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

# P0-T002 · Set up the dedicated Telegram identity, api_id/api_hash and alert bot

## Goal / expected outcome

A dedicated Telegram identity (landline voice code or prepaid SIM) with a 2-step password, an `api_id`/`api_hash` from my.telegram.org, and a bot created via @BotFather whose chat with you is known. This gates the P0 seal witness and alert route, P1 alerts and P4 ingest.

## Context & references

- [Roadmap P0 T0.06](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [04 do-this-week](../../../docs/04-plan-of-action.md#️-do-this-week-regardless-of-phase)
- [07 §10 social accounts](../../../docs/07-security-notes.md#10-social--scraping-accounts)
- [12 §4 platform rules](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)
- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers) (Telegram witness of the daily seal)
- [P1 roadmap](../../../docs/roadmap/phase-1-data-and-monitoring.md) (T1.31 alerts bot)
- Unblocks: the live seal witness and real alert receipt checked in the soak (P0-T063); P0-T037 and P0-T045 are built against a mocked Bot API, so they don't wait for this task; P1 alerts (T1.31); P4 Telethon ingest

## Requirements

- Dedicated number: try a landline that can receive the voice-call code first; otherwise a prepaid SIM kept in a drawer (needed for re-login).
- Account hardening: 2-step verification password (unique, ≥ 16 chars), recovery email set, phone number visible to nobody.
- `api_id` / `api_hash` from my.telegram.org → *API development tools* (app title `MasterTrader`, platform Desktop).
- Bot via @BotFather: name `MasterTrader Alerts`, username ending `_bot`; `/setjoingroups` → Disable; `/setprivacy` → Enable. Store the bot token.
- Find your personal chat id with the bot (send `/start`, then call `getUpdates` from the host) and record it as `telegram.owner_chat_id`.
- Outputs → the sops secrets file `~/.config/mastertrader/secrets.sops.yaml` (created by the secrets task, P0-T022) under `telegram:` (`api_id`, `api_hash`, `bot_token`, `owner_chat_id`). The late live checks (P0-T063) use the env names `TELEGRAM_BOT_TOKEN` and `TELEGRAM_OWNER_CHAT_ID` (names only; values stay in the secrets file). Until the secrets file exists, keep values **only** in your password manager; never in chat, email, git, issues or notes apps.

## ToDo

- [ ] Get the dedicated number working (landline voice code or prepaid SIM); log which kind you used (not the number).
- [ ] Install Telegram on a spare device or Telegram Desktop; register the account; set the 2-step password and recovery email.
- [ ] Create the app at my.telegram.org and note `api_id`/`api_hash` in your password manager.
- [ ] Create the bot with @BotFather and apply `/setjoingroups` Disable and `/setprivacy` Enable.
- [ ] From your **personal** Telegram account, open the bot and send `/start`; read your chat id via `getUpdates`.
- [ ] Once P0-T022 lands, run `sops ~/.config/mastertrader/secrets.sops.yaml` and add the `telegram:` block.
- [ ] Log completion date and 'stored in secrets file' in the progress log.

## Verification

### Tests
- Confirmation: `getMe` against the Bot API (run on the host via `sops exec-env`, so the token never hits shell history) returns `ok: true`.

### Scenarios
- Given the bot token is in the secrets file, when the seal flow (P0-T037) sends the daily witness, then it arrives in your personal chat.
- Given the dedicated SIM is lost, when Telegram asks for a code, then the 2-step password plus recovery email still allow login (test once).

### Stress / failure injection
- n/a: account action.

## Acceptance criteria

- [ ] Dedicated account exists with 2-step password and recovery email
- [ ] `api_id`, `api_hash`, `bot_token`, `owner_chat_id` stored in the secrets file (or password manager until P0-T022)
- [ ] `getMe` returns ok from the host
- [ ] No value pasted into chat, git or an issue

## Exceptions & edge cases

- Landline voice code not offered: use a prepaid SIM; keep it topped up so the number is not recycled.
- my.telegram.org refuses app creation (common on new accounts): wait 24–48 h and retry from the same device/IP; do not use a VPN.

## Cardinal rules (do NOT)

- Do NOT use your personal Telegram account as the ingest identity.
- Do NOT use a VPN/proxy to register or log in.
- Do NOT mass-join channels now (P4 uses a rate-limited join queue; cap 500).
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT put Telegram text into any model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT add paid data/APIs, ToS-breaking scraping, self-bots or user tokens; free tiers only ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/07-security-notes.md` §10: note that the dedicated identity exists (no values).
- `docs/roadmap/phase-0-foundations.md`: tick T0.06 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T002-telegram-account-and-bot`
- PR title: `P0-T002: Set up the dedicated Telegram identity, api_id/api_hash and alert bot`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T002` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (secrets file path → `~/.config/mastertrader/`, outside the repo (17 §D P0-B018); keys-last: P0-T037/P0-T045 no longer wait for this, live check in P0-T063; env names named; run fields added)
