---
id: P1-T069
kind: task
title: Re-check your venues on the AUSTRAC register each quarter
phase: 1
type: USER
status: backlog
priority: medium
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P1-T043, P0-T026]
requirements: [R1.13]
roadmap_todos: [T1.06]
modules: [M16]
dashboards: [D07]
tools: []
mcp: []
env: []
services: [austrac-register]
branch: p1/P1-T069-quarterly-austrac-register-check
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/12-policy-and-compliance.md]
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

# P1-T069 · Re-check your venues on the AUSTRAC register each quarter

## Goal / expected outcome

When the quarterly reminder arrives, you look up every venue you use on the AUSTRAC digital currency exchange register and record the result in the venue registry, so `ops.venue_registry` health shows a current AUSTRAC check date. This item covers the **first** reminder cycle; later quarters recur through the same reminder and are not tracked as Phase 1 work.

## Context & references

- Roadmap: requirement [R1.13](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.06](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B014 (venue health = our measured withdrawal times + venue status feeds via the venue watch + a quarterly AUSTRAC register check as a USER task)
- Policy: [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) (AUSTRAC status re-checked quarterly; the register has no API; `VENUE_CHECK` task, a Telegram/notification reminder until the P5 task queue exists) · [13 §6](../../../docs/13-wallets-treasury-and-onchain.md#6-monitors-feed-m16-and-m11)
- Reminder: P1-T043 raises `alert.info.austrac_recheck` when a venue's `austrac_checked_at` is older than 90 days (default, configurable)
- Cross-phase prerequisite: P0-T026 (registry seeded from your first check, P0-T011)

## Requirements

- Trigger: the reminder (Telegram + notification centre) listing the venues due, or `uv run mt-monitor venue-health remind --now` to force the first cycle
- For each venue you use: search the AUSTRAC register by ABN or name (https://www.austrac.gov.au, "Digital currency exchange register"), note status (registered / cancelled / suspended / not found) and the date checked
- Record each result yourself with `venue.registry.update` (D07 venue health panel or `/venues/registry`); a result that tightens access (e.g. registration cancelled → `blocked`) is C1 and immediate; anything that would loosen access is C3 (break-glass CLI `mtctl approve` + TOTP until Telegram C3 lands in P2)
- No scraping: the system never fetches the register for you

## ToDo

- [ ] Wait for (or force) the first quarterly reminder
- [ ] Check every venue in the reminder on the AUSTRAC register
- [ ] Record status + date per venue via `venue.registry.update`
- [ ] If any venue lost its registration, block it (C1) and tell the agent so dependent feeds/recon are reviewed
- [ ] Confirm in the progress log that the next reminder date shows ~90 days ahead in D07

## Verification

### Tests

- Agent check: `/venues/registry` shows `austrac_checked_at` = today for every venue you use, and each update is an `audit.command` row with source `web`

### Scenarios

- Given a venue's registration was cancelled, when you record it, then the venue becomes `blocked` immediately (C1), `venue.registry.changed` is emitted and an alert fires
- Given you record "registered" for all venues, when the daily reminder job runs the next day, then no reminder is raised until the next 90-day mark

### Stress / failure injection

- n/a: a manual check

## Acceptance criteria

- [ ] Every venue you use has an AUSTRAC check date within the last 90 days in `ops.venue_registry`
- [ ] Any change in status is recorded through `venue.registry.update` (never by editing the DB)

## Exceptions & edge cases

- Offshore venues used only as public data sources (e.g. Bybit market data) need no AUSTRAC check; mark them `data_only` so the reminder skips them
- If the AUSTRAC site is down, snooze the reminder a day; do not record a guess

## Cardinal rules (do NOT)

- Do NOT scrape the AUSTRAC register or automate the lookup ([12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry))
- Do NOT loosen a venue's access without C3; tightening is C1
- Do NOT paste account numbers or credentials into the progress log

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.06 (the recurring check continues via the reminder); note P1-T069 next to it.
- `docs/12-policy-and-compliance.md` §2: update the AUSTRAC status column if any venue's status changed.

## Branch & PR

- Branch: `p1/P1-T069-quarterly-austrac-register-check` (no code; only if a doc changes)
- PR title: `P1-T069: Re-check your venues on the AUSTRAC register each quarter`
- PR checklist: registry updated via commands · task file ticked · `./kanban done P1-T069` run

## Progress log

- 2026-10-22 00:00 · aligner · created for T1.06 (docs/16–17 alignment)
