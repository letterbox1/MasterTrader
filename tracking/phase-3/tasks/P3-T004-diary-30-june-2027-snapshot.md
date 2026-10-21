---
id: P3-T004
kind: task
title: Diary the 30 June 2027 snapshot hard date
phase: 3
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R3.08]
roadmap_todos: [T3.06]
modules: [M18]
dashboards: [D15]
branch: p3/P3-T004-diary-30-june-2027-snapshot
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-T004 · Diary the 30 June 2027 snapshot hard date

## Goal / expected outcome

The 30 June 2027 end-of-day AEST market-value snapshot of every open lot is in your calendar with reminders, so you can confirm it ran (P3-T030) and react if it didn't.

## Context & references

- Roadmap: [R3.08, T3.06](../../../docs/roadmap/phase-3-journal-and-tax.md) · [roadmap README §4 fixed dates](../../../docs/roadmap/README.md#4-fixed-external-dates)
- Design: [09 key findings](../../../docs/09-journal-and-tax.md#️-key-findings-that-shape-the-design) (snapshot of every open lot, price source recorded)
- Related: P3-T030 (job), P3-T044 (runbook), P3-B002 (price convention)

## Requirements

- Calendar entries (your own calendar, not the repo): **2027-06-01** check host/backups/price feeds and P3-T002 answer; **2027-06-29** confirm the Prefect deployment `journal-snapshot-2027-06-30` is scheduled; **2027-06-30 23:59 AEST** snapshot runs; **2027-07-01 09:00 AEST** verify in D15 Lots that the snapshot status is `complete` for every open lot.
- If the host is down on the date, the job is idempotent and back-dated to the 30 June valuation time using recorded prices (P3-T030); you still must confirm.

## ToDo

- [ ] Add the four calendar entries with alerts
- [ ] Add the runbook link (P3-T044) to the 1 July entry
- [ ] Record in the progress log that the reminders exist

## Verification

### Tests

- n/a (USER action)

### Scenarios

- Given 2027-07-01 09:00 AEST, when you open D15 Lots, then every lot open at 30 June shows a snapshot value with price source and timestamp; otherwise follow the runbook.

### Stress / failure injection

- n/a

## Acceptance criteria

- [ ] Four reminders exist in your calendar
- [ ] Progress log notes it

## Exceptions & edge cases

- Daylight saving: 30 June is AEST (UTC+10) in Sydney; no DST ambiguity.

## Cardinal rules (do NOT)

- Do NOT rely on memory alone; this date cannot be re-run with live prices later.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.06 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T004-diary-30-june-2027-snapshot` (only if this action changes a config/seed file; otherwise no PR)
- PR title: `P3-T004: Diary the 30 June 2027 snapshot hard date`
- Checklist: steps done · outputs stored where stated (secrets only in the sops file) · confirmation recorded in the progress log · `./kanban done P3-T004` run

## Progress log

- 2026-10-21 00:00 · planner · created
