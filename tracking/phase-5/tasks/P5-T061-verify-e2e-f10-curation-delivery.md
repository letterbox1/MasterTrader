---
id: P5-T061
kind: task
title: End-to-end F10 curation loop and Discord delivery test
phase: 5
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T030, P5-T047, P5-T049]
requirements: [R5.20, R5.21, R5.22]
roadmap_todos: []
modules: [M19, M2]
dashboards: [D13]
branch: p5/P5-T061-verify-e2e-f10-curation-delivery
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

# P5-T061 · End-to-end F10 curation loop and Discord delivery test

## Goal / expected outcome

The F10 loop is proven: sources create tasks → instant/daily/weekly delivery (Telegram + UI) → Done/Skip/Snooze/Never → ranking changes → for a Discord follow task, the bot verifies posts arrive ("verified") or re-prompts after N days.

## Context & references

- Roadmap: R5.20 ("Flow tests"), R5.21 ("Delivery test"), R5.22 ("Digest preview")
- [02 F10](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [08 Discord queue](../../../docs/08-airdrops-and-token-launches.md#discord-curation-queue)

## Requirements

- Automated part: mocked Telegram + Discord webhook events; assert task states, ranking deltas, digest composition and timing in Australia/Sydney.
- Live part: one real follow into `#mt-inbox` from a test/announcement channel you control (your own second server) → verified within minutes; one follow never completed → re-prompt after the configured N days (time-travel in test).
- Digest preview matches the sent digest.

## ToDo

- [ ] Write `tests/scenarios/f10/` automated flow.
- [ ] Set up a second private Discord server with an announcement channel to act as the "project"; follow it into `#mt-inbox`.
- [ ] Run and record.

## Verification

### Tests
- Automated flow suite + live delivery check.

### Scenarios
- Given you Snooze 1w a task due in 3 days, then it reappears at its due-time alert, not after the full week (deadline wins).

### Stress / failure injection
- n/a: functional loop (load covered in P5-T029/T030)

## Acceptance criteria

- [ ] Automated loop passes
- [ ] Live Discord delivery verified
- [ ] Re-prompt behaviour verified
- [ ] Digest preview equals sent digest

## Exceptions & edge cases

- Discord outage: verification pending, no false re-prompt during the outage window.

## Cardinal rules (do NOT)

- Do NOT use a self-bot to simulate following.
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.
- Do NOT let Telegram text reach any model, RAG index or training set; Telegram contributes deterministic postures only (12 §4–5).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- No doc change beyond ticking verification of R5.20–R5.22.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick the related exit criterion when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T061-verify-e2e-f10-curation-delivery`
- PR title: `P5-T061: End-to-end F10 curation loop and Discord delivery test`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T061` run

## Progress log

- 2026-10-21 00:00 · planner · created
