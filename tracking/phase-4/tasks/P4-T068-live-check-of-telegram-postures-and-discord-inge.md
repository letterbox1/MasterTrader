---
id: P4-T068
kind: task
title: Live check of Telegram postures and Discord ingest on your accounts
phase: 4
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T001, P4-T002, P4-T006, P4-T018, P4-T019, P4-T020]
requirements: [R4.02, R4.03, R4.04]
roadmap_todos: [T4.21, T4.22]
modules: [M2]
dashboards: [D08, D07]
tools: [uv, sops, git]
mcp: []
env: [TELEGRAM_API_ID, TELEGRAM_API_HASH, DISCORD_BOT_TOKEN]
services: [telegram-account, discord-feeds-server, nats, postgres]
branch: p4/P4-T068-live-check-of-telegram-postures-and-discord-inge
pr: ""
doc_sync: [docs/runbooks/social-accounts.md, docs/roadmap/phase-4-intel.md]
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

# P4-T068 · Live check of Telegram postures and Discord ingest on your accounts

## Goal / expected outcome

On your dedicated Telegram account and your Discord feeds server, the account-bound sources work live: the join queue starts joining your channel list slowly within `FLOOD_WAIT` rules and postures appear in `text.telegram_posture` / `posture.telegram.*` (numbers only), and the Discord bot ingests your followed announcement channels for 48 h. The Telegram-text gate probes (P4-T050) run against the live stack with zero leaks.

## Context & references

- Roadmap: [R4.02, R4.03, R4.04](../../../docs/roadmap/phase-4-intel.md#3-requirements) · completes ToDos [T4.21, T4.22](../../../docs/roadmap/phase-4-intel.md#4-todo-sets) on real accounts
- Decisions: [17 §A](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (P4-B001: F3b postures only) · [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P4-B002/B003: `text.telegram_posture`, `posture.telegram.*`, consumers M4/M11 rules only) · [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22) (keys last) · [16 §2.13](../../../docs/16-configuration-and-safety-model.md#213-curation) (7-day Discord delivery check)
- Your inputs (`depends_on`): P4-T001 (channel list + your Telethon login), P4-T002 (Discord follows); account setup came from P0-T002/P0-T008
- Built on fixtures in: P4-T018 (join queue), P4-T019 (postures), P4-T020 (Discord bot); secrets mechanism P4-T006
- Policy: [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (joined channels only; honour FLOOD_WAIT; no self-bots).

## Requirements

- Telegram: the queue joins from `telegram_channels.yaml` at its configured pace (default ≤ 20/day), honours any `FLOOD_WAIT` exactly, never exceeds 500; postures for joined channels appear within one window; no message text or usernames in any table, log or NATS payload (spy + grep).
- Discord: the bot is only in your feeds server (guild allow-list), ingests each receiving channel for 48 h, resolves crosspost sources; channels quiet for 7 days are flagged (16 §2.13).
- Re-run the P4-T050 probes (DB scan, NATS tap, Loki, API crawl) against the live stack for 24 h: zero Telegram text outside the in-memory extractor.
- Credentials stay in the sops file outside the repo; the env names above are only for this session's `sops exec-env` and are never printed.

## ToDo

- [ ] Confirm the encrypted Telethon session exists and decrypts into `ingest-text` tmpfs only
- [ ] Enable Telegram ingest; watch the first joins and the first postures in D08
- [ ] Enable the Discord bot; confirm each receiving channel shows items/day > 0 within 48 h
- [ ] Run the P4-T050 probes on the live stack for 24 h and save the report
- [ ] Record results (counts, no text) in this file and the social-accounts runbook

## Verification

### Tests
- Live probe report (P4-T050 probes against the live stack).
- Join-queue metrics: joins/day, FLOOD_WAIT events honoured, joined count ≤ 500.

### Scenarios
- Given Telegram returns a 24-h FLOOD_WAIT, then joins pause, already-joined channels keep producing postures, and D08 Sources shows 'join paused until …'.
- Given the bot is invited to a server you don't administer, then it leaves and alerts.
- Given a followed channel delivers nothing for 7 days, then you're re-prompted (16 §2.13).

### Stress / failure injection
- n/a: real-account pacing must stay slow; load is covered on fixtures in P4-T058.

## Acceptance criteria

- [ ] Telegram joins follow the queue rules; postures live; zero text leaks in the 24-h live probe
- [ ] Discord receiving channels ingest live for 48 h
- [ ] Results recorded without any message text, usernames or secrets

## Exceptions & edge cases

- Account restricted or banned: stop all Telegram activity, alert critical, manual review; never create a new account.
- Message Content intent revoked: Discord falls back to embeds/titles only and alerts.

## Cardinal rules (do NOT)

- Do NOT mass-join, scrape member lists, DM, forward or react.
- Do NOT use self-bots or user tokens.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file outside the repo ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/runbooks/social-accounts.md`: live-check results and what to watch
- `docs/roadmap/phase-4-intel.md`: tick T4.21/T4.22 when all their items are done

## Branch & PR

- Branch: `p4/P4-T068-live-check-of-telegram-postures-and-discord-inge`
- PR title: `P4-T068: Live check of Telegram postures and Discord ingest on your accounts`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T068` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (keys-last live check for account-bound Telegram/Discord sources (17 §E); postures per 17 §A/§D)
