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
depends_on: [P0-T019, P0-T045, P0-T041, P0-T040, P0-T042, P0-T043, P0-T044, P0-T051, P0-T052, P0-T065, P0-T072]
requirements: [R0.02, R0.10, R0.N4, R0.07, R0.12]
roadmap_todos: [T0.80]
modules: [ops, M17]
dashboards: []
tools: [docker, promtool, just]
mcp: []
env: []
services: [supabase-postgres, supabase-auth, nats, minio]
branch: p0/P0-T063-72h-idle-soak
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T063 · Run the 72-hour idle soak

## Goal / expected outcome

The complete P0 stack runs untouched on the always-on **workstation** (self-hosted Supabase + the Compose stack, [18 §9](../../../docs/18-platform-and-deployment.md#9-workstation-first-build-path)) for 72 hours: no container restarts, nightly backups and WAL archiving succeed, three daily seals and verifies pass, alerts stay quiet (except the deliberate test alert), and resource usage is stable. It runs keyless against MinIO (Object Lock) and the mocked Bot API, with the seeded test account and the throwaway `worm_owner`; the real bucket and bot are checked separately in P0-T073 (build first, keys last), so the soak waits on none of your USER tasks.

## Context & references

- [Roadmap P0 T0.80](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [02 §9.2 SLOs](../../../docs/02-v1-architecture.md#92-observability--slos)
- [07 §9 monitoring & incident response](../../../docs/07-security-notes.md#9-monitoring--incident-response)
- [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19) (workstation-first; USER-blocker rule)
- Evidence feeds P0-T064; real-account checks: P0-T073 (seal target + bot), P0-T057 (backup target), P0-T068 (LLM keys)
- Depends on: P0-T019, P0-T045, P0-T041, P0-T040, P0-T042, P0-T043, P0-T044, P0-T051, P0-T052, P0-T065, P0-T072 (these bring in the rest of the stack, including P0-T070)

## Requirements

- Start only after every dependency is done and the stack is up on the workstation with all migrations applied (`just db-migrate`; throwaway `worm_owner` until the ceremony before live money, P0-T013).
- Pass criteria over 72 h: restart count 0 for every service (Supabase stack included); no OOM kills; ≥ 3 successful nightly backups and continuous WAL (lag < 2 min p99) to the MinIO Object-Lock target; 3 seals anchored to MinIO (+ witnesses received by the mocked Bot API); 3 daily full verifies and every hourly incremental check ok; KV `audit.integrity` stays `ok`; the deliberate test alert reaches the mocked Bot API; future bar partitions present (P0-T072 job ran); no firing alerts other than a scheduled synthetic test; memory growth < 10 % per service after the first hour; disk growth logged; chrony offset < 50 ms.
- Light synthetic activity allowed: a cron calling `system.settings.update` (C0) every 10 min with the seeded test account's `aal2` token (refreshed through Supabase Auth) to exercise Auth, audit and chain; nothing else.
- If any criterion fails: fix, then restart the 72 h clock.
- The workstation must not sleep or suspend during the soak (power settings logged).

## ToDo

- [ ] Record the start time and the workstation profile (P0-T005) in the progress log.
- [ ] Start the synthetic C0 cron.
- [ ] At 24 h, 48 h, 72 h: snapshot Grafana (containers, workstation, backups/WORM) and note status.
- [ ] Write the soak report (table of criteria vs observed) into the progress log and `docs/runbooks/evidence/p0-soak-<date>.md`.

## Verification

### Tests
- Criteria checks via PromQL queries listed in the report (e.g. `increase(container_restart_count[72h]) == 0`).

### Scenarios
- Given a nightly backup fails at hour 30, then the soak fails, the cause is fixed and the 72 h clock restarts.
- Given the Supabase Auth token refresh fails during the synthetic cron, then the soak fails (Auth must stay healthy for 72 h).

### Stress / failure injection
- The soak itself is the endurance test.

## Acceptance criteria

- [ ] 72 h with all pass criteria met (report attached)
- [ ] Evidence committed for the exit demo

## Exceptions & edge cases

- Planned security-update reboot inside the window: either defer unattended reboots for the soak or restart the clock (log which).
- The workstation is also your desktop: heavy personal use during the soak is allowed but logged; an OOM or sleep restarts the clock.

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
- 2026-11-19: Workstation-first: the soak runs on the workstation with the test account and the throwaway worm_owner; no longer waits on P0-T062 or P0-T013.
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (soak is keyless on the workstation (MinIO + mocked Bot API + seeded test account); USER dependencies P0-T006 and P0-T002 and their env names moved to the new live-check task P0-T073; Supabase stack in the pass criteria; P0-T072 added)
