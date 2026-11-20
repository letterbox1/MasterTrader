---
id: P0-T073
kind: task
title: Live check of the real seal target and Telegram bot (keys last)
phase: 0
type: VERIFY
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T006, P0-T002, P0-T037, P0-T040, P0-T045, P0-T022]
requirements: [R0.07, R0.N4, R0.10]
roadmap_todos: [T0.80]
modules: [mt-obs, ops]
dashboards: [D16]
tools: [docker, cargo, sops, curl]
mcp: []
env: [TELEGRAM_BOT_TOKEN, TELEGRAM_OWNER_CHAT_ID, B2_WORM_SEAL_KEY_ID, B2_WORM_SEAL_APPLICATION_KEY]
services: [telegram, backblaze-b2, supabase-postgres]
branch: p0/P0-T073-live-check-of-the-real-seal-target-and-telegram-
pr: ""
doc_sync: [docs/runbooks/, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-19
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T073 · Live check of the real seal target and Telegram bot (keys last)

## Goal / expected outcome

The seal, monthly WORM export and alert paths, built and soaked against MinIO and a mocked Bot API, are proven once against your **real accounts**: a daily seal and a test WORM export land in the real Object-Locked bucket (P0-T006) and can't be deleted, and the Telegram witness and a test alert arrive from the real bot (P0-T002). This is the "keys last" live check split out of the soak (P0-T063), so the soak doesn't wait on your accounts.

## Context & references

- [Roadmap P0 R0.07, R0.N4, R0.10](../../../docs/roadmap/phase-0-foundations.md#3-requirements) · [T0.80](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [15 §2 WORM](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) (seal, anchoring, Telegram witness)
- [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19) (build first, keys last)
- Depends on: P0-T006 (real bucket, USER), P0-T002 (real bot, USER), P0-T037 (seal), P0-T040 (WORM export), P0-T045 (alert route), P0-T022 (secrets)
- Feeds: P0-T064 exit demo

## Requirements

- Credentials come only from the sops file (env names in the front matter); nothing in the repo or logs.
- Seal: run the daily seal once against the real bucket with Object Lock; `audit.seal` row records the object key, version id and retention-until; a delete attempt with the app credential is refused.
- Export: run the monthly WORM export once to the real bucket (small test month); retention matches 16 / P0-T006 (7 years for seals/exports).
- Telegram: the seal witness message and a deliberate test alert arrive in your owner chat from the real bot; the bot token is never logged.
- Results recorded in `docs/runbooks/evidence/p0-live-accounts-<date>.md` (no secrets, no account IDs).

## ToDo

- [ ] Load the real credentials via the sops file (P0-T022 layout) on the workstation.
- [ ] Run one seal and one test export against the real bucket; try a delete (expect refusal).
- [ ] Trigger the Telegram witness and a test alert; confirm receipt.
- [ ] Write the evidence file and log here.

## Verification

### Tests
- `cargo test -p mt-obs --features live -- seal_live` (ignored by default; run manually with the real env names) passes; delete attempt returns `AccessDenied`/Object Lock error.

### Scenarios
- Given the real bucket, when the seal runs, then `audit.seal` has the object version id and the object can't be deleted before retention ends.
- Given an alert fires, then you receive it in Telegram within 1 minute.

### Stress / failure injection
- Wrong bucket credential: the seal fails closed, an incident/alert is raised, and nothing is retried in a tight loop.

## Acceptance criteria

- [ ] Seal and export landed in the real Object-Locked bucket; delete refused
- [ ] Witness and test alert received from the real bot
- [ ] Evidence file committed (no secrets)

## Exceptions & edge cases

- You chose the restic `rest-server --append-only` box instead of B2 (P0-T006): run the same checks against it.
- Telegram rate limit: retry once after the advertised delay.

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT shorten Object Lock retention to make a test pass.
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).

## Doc sync on completion

- `docs/runbooks/evidence/`: add the live-accounts evidence file.
- `docs/roadmap/phase-0-foundations.md`: tick T0.80 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T073-live-check-of-the-real-seal-target-and-telegram-`
- PR title: `P0-T073: Live check of the real seal target and Telegram bot (keys last)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T073` run

## Progress log

- 2026-11-19 00:00 · aligner · created
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (new task: the real-bucket and real-bot checks split out of the soak P0-T063, so only this late VERIFY task depends on USER P0-T006 and P0-T002)
