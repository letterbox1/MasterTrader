---
id: P5-T008
kind: task
title: Work the task queue: follow communities, do social tasks yourself, review ICOs
phase: 5
type: USER
status: backlog
priority: medium
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P5-T029, P5-T030, P5-T047, P5-T049]
requirements: [R5.20, R5.21]
roadmap_todos: [T5.07]
modules: [M19]
dashboards: [D13]
branch: p5/P5-T008-work-task-queue
pr: ""
doc_sync: [docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T008 · Work the task queue: follow communities, do social tasks yourself, review ICOs

## Goal / expected outcome

For at least two weeks you work the D13/Telegram queue: join and **Follow** the suggested announcement channels into your `#mt-inbox`, do social/quest tasks yourself, review ICO items — tapping Done/Skip/Snooze/Never so ranking learns and Discord delivery verification is exercised.

## Context & references

- Roadmap: ToDo T5.07 → R5.20, R5.21 · [08 Discord curation queue](../../../docs/08-airdrops-and-token-launches.md#discord-curation-queue)
- UI: [D13](../../../docs/ui/dashboards/D13-tasks-curation.md), Telegram buttons ([mobile §3](../../../docs/ui/mobile-and-telegram.md))
- Runs alongside P5-T063 (two weekly digests)
- Depends on: P5-T029, P5-T030, P5-T047, P5-T049

## Requirements

- Follow tasks: join the server from the **verified invite only**, click Follow on the named announcement channel, target `#mt-inbox` (≈10–15 follows per receiving channel, P4 T4.02).
- Social tasks (follow on X, quests on Galxe/Zealy/Layer3): you do them by hand; nothing is automated.
- Tap Done only after doing the task; use Never for projects you never want to see again.

## ToDo

- [ ] Each day: open the Telegram digest or D13 Inbox; do the top tasks; tap Done/Skip/Snooze/Never.
- [ ] For each Discord follow: after Done, check D13 Communities flips to "verified" within the verification window.
- [ ] Note any task whose link looked wrong and report it (feeds P5-T063 false-positive review).
- [ ] After two weeks report "done" so T5.07 can be ticked.

## Verification

### Tests
- Manual: D13 History shows ≥ 10 closed tasks with outcomes.
- Manual: ≥ 3 Discord follows reached "verified".

### Scenarios
- Given a follow task, when you tap Done but forgot to click Follow, then the bot re-prompts you after N days (P5-T047).

### Stress / failure injection
- n/a: human activity

## Acceptance criteria

- [ ] ≥ 2 weeks of queue use
- [ ] ≥ 3 verified Discord follows
- [ ] Feedback (skip/never) visible in ranking changes

## Exceptions & edge cases

- If a link in a task fails the blocklist at render time it shows as plain text — do not copy it into a browser; report it.

## Cardinal rules (do NOT)

- Do NOT use self-bots, browser automation or captcha solvers for any task.
- Do NOT connect your main or vault wallet to any site from a task.
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.

## Doc sync on completion

- No repo doc change; the agent ticks T5.07 once you confirm.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.07 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T008-work-task-queue`
- PR title: `P5-T008: Work the task queue: follow communities, do social tasks yourself, review ICOs`
- PR checklist: no PR (USER item); confirm in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
