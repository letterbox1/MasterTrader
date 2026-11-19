---
id: P7-T071
kind: task
title: Choose the go-live runtime host and cloud options (default: stay on the workstation)
phase: 7
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R7.01]
roadmap_todos: []
modules: [M17]
dashboards: [D16]
tools: []
mcp: []
env: []
services: []
branch: p7/P7-T071-choose-the-go-live-runtime-host-and-cloud-option
pr: ""
doc_sync: [docs/18-platform-and-deployment.md, docs/roadmap/phase-7-prove-and-go-live.md]
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
# P7-T071 · Choose the go-live runtime host and cloud options (default: stay on the workstation)

## Goal / expected outcome

You choose where the always-on trading services run for live money, and whether to use the paid cloud options. If you don't choose, the default applies: **stay on the workstation**, web app served locally, database self-hosted (`deploy.mode: workstation`, [16 §2.15](../../../docs/16-configuration-and-safety-model.md#215-platform-deployment-and-regions)). This is asked because the options cost money.

## Context & references

- Options and trade-offs: [18 §5](../../../docs/18-platform-and-deployment.md#5-deployment-modes) · what can't run on Vercel: [18 §6](../../../docs/18-platform-and-deployment.md#6-what-cant-run-on-vercel-and-why) · Decisions: [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19)
- The agent prepares a one-page comparison (cost per month, uptime, latency to your venues measured from the workstation) in this task's progress log before you decide.
- Unblocks: P7-T073 (the shift).

## Requirements

- Pick one runtime host: **workstation** (free; needs the UPS and 4G failover, P7-T009) · **home server** · **Sydney cloud VM** with a static IP (a few dollars to tens of dollars a month; doubles as the egress IP).
- Optional: **Vercel** for the web app (Hobby is free for personal use (U)); **Supabase cloud** in Sydney (paid plan needed; free plan is 500 MB and pauses after 7 idle days); point-in-time recovery add-on (paid).
- Account sign-ups for anything you pick are yours (Vercel, Supabase, the VM provider); the agent writes step-by-step instructions.

## ToDo

- [ ] Read the agent's comparison in the progress log
- [ ] Reply with your choice (or say "default")
- [ ] Create the accounts for the options you picked and add their tokens to the secrets file (names in P7-T073)

## Verification

### Tests
- Agent records the choice as a config change (`deploy.mode`, `db.target`, `web.host`) with source `user`.

### Scenarios
- Given no choice is made, when P7-T073 starts, then it proceeds with the workstation default.

### Stress / failure injection
- n/a: decision.

## Acceptance criteria

- [ ] Choice recorded (or the default confirmed)

## Exceptions & edge cases

- If you pick a cloud option and later drop it, P7-T073 runs again for the new target; nothing is deleted from the old one until the move verifies.

## Cardinal rules (do NOT)

- The agent never signs up for paid services or enters payment details.

## Doc sync on completion

- docs/18-platform-and-deployment.md, docs/roadmap/phase-7-prove-and-go-live.md: update to match what was built.

## Branch & PR

- Branch: `p7/P7-T071-choose-the-go-live-runtime-host-and-cloud-option`
- PR title: `P7-T071: Choose the go-live runtime host and cloud options (default: stay on the workstation)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T071` run

## Progress log

- 2026-11-19 09:16 · cloud:vm:be04b6ae61f8 · created
