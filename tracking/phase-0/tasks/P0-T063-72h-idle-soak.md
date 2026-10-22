---
id: P0-T063
kind: task
title: Run the 72-hour idle soak
phase: 0
type: RUN
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T019, P0-T045, P0-T041, P0-T040, P0-T042, P0-T043, P0-T044, P0-T051, P0-T052, P0-T062, P0-T065, P0-T013, P0-T006, P0-T002]
requirements: [R0.02, R0.10, R0.N4, R0.07, R0.12]
roadmap_todos: [T0.80]
modules: [ops, M17]
dashboards: []
tools: [docker, promtool]
mcp: []
env: [TELEGRAM_BOT_TOKEN, TELEGRAM_OWNER_CHAT_ID, MT_WORM_SEAL_S3_KEY_ID, MT_WORM_SEAL_S3_SECRET]
services: [telegram, backblaze-b2, tailscale]
branch: p0/P0-T063-72h-idle-soak
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

# P0-T063 · Run the 72-hour idle soak

## Goal / expected outcome

The complete P0 stack runs untouched on the real host for 72 hours: no container restarts, nightly backups and WAL archiving succeed, three daily seals and verifies pass, alerts stay quiet (except the deliberate test alert), and resource usage is stable. It is also the late live check for the real accounts (build first, keys last): seals and the monthly export anchored to the real Object-Locked target (P0-T006), and the Telegram witness and test alert delivered by the real bot (P0-T002).

## Context & references

- [Roadmap P0 T0.80](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [02 §9.2 SLOs](../../../docs/02-v1-architecture.md#92-observability--slos)
- [07 §9 monitoring & incident response](../../../docs/07-security-notes.md#9-monitoring--incident-response)
- Evidence feeds P0-T064
- Depends on: P0-T019, P0-T045, P0-T041, P0-T040, P0-T042, P0-T043, P0-T044, P0-T051, P0-T052, P0-T062, P0-T065 (these bring in the rest of the stack), P0-T013 (production WORM migrations via the ceremony), P0-T006 (real backup/seal target), P0-T002 (real bot)

## Requirements

- Start only after every dependency is done and the stack is on the production host, with WORM migrations applied through the `worm_owner` ceremony (P0-T013).
- Pass criteria over 72 h: restart count 0 for every service; no OOM kills; ≥ 3 successful nightly backups and continuous WAL (lag < 2 min p99); 3 seals anchored to the real Object-Locked target (+ Telegram witnesses received from the real bot); 3 daily full verifies and every hourly incremental check ok; KV `audit.integrity` stays `ok`; the deliberate test alert arrives in your Telegram; no firing alerts other than a scheduled synthetic test; memory growth < 10 % per service after the first hour; disk growth logged; chrony offset < 50 ms.
- Light synthetic activity allowed: a cron calling `system.settings.update` (C0) every 10 min to exercise audit/chain; nothing else.
- If any criterion fails: fix, then restart the 72 h clock.

## ToDo

- [ ] Record the start time in the progress log.
- [ ] Start the synthetic C0 cron.
- [ ] At 24 h, 48 h, 72 h: snapshot Grafana (containers, host, backups/WORM) and note status.
- [ ] Write the soak report (table of criteria vs observed) into the progress log and `docs/runbooks/evidence/p0-soak-<date>.md`.

## Verification

### Tests
- Criteria checks via PromQL queries listed in the report (e.g. `increase(container_restart_count[72h]) == 0`).

### Scenarios
- Given a nightly backup fails at hour 30, then the soak fails, the cause is fixed and the 72 h clock restarts.

### Stress / failure injection
- The soak itself is the endurance test.

## Acceptance criteria

- [ ] 72 h with all pass criteria met (report attached)
- [ ] Evidence committed for the exit demo

## Exceptions & edge cases

- Planned host security-update reboot inside the window: either defer unattended reboots for the soak or restart the clock (log which).

## Cardinal rules (do NOT)

- Do NOT restart, redeploy or tweak services during the soak without restarting the clock.
- Do NOT silence alerts to pass the soak.
- Do NOT skip, weaken or delete a test to get CI green.
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).

## Doc sync on completion

- `docs/runbooks/evidence/`: add the soak report.
- `docs/roadmap/phase-0-foundations.md`: tick T0.80 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T063-72h-idle-soak`
- PR title: `P0-T063: Run the 72-hour idle soak`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T063` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (late live check for real bucket/bot (keys last) with env names; integrity status + hourly/daily verify (16 §2.11); deps trimmed and ceremony P0-T013 added; run fields added)
