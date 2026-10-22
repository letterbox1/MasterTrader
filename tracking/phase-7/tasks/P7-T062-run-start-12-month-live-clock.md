---
id: P7-T062
kind: task
title: Start the 12-month live clock
phase: 7
type: RUN
status: cancelled
priority: medium
size: XS
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T057]
requirements: [R7.05]
roadmap_todos: [T7.82]
modules: [M11]
dashboards: [D03]
tools: []
mcp: []
env: []
services: []
branch: p7/P7-T062-run-start-12-month-live-clock
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P7-T062 · Start the 12-month live clock

## Goal / expected outcome

The 12-month live review clock is started per sleeve at its first live funding, a reminder is scheduled for day 365, and the monthly interim report (P7-T042) is scheduled — the review itself happens long after this phase closes.

## Context & references

- Roadmap: [R7.05 · ToDo T7.82](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) (12-month review) · Roadmap T7.82
- Related: P7-T042, P7-T063, gap P7-B012 (no phase owns the actual review)

## Requirements

- `risk.capital_step` row with `live_started_at` per sleeve (already written at funding) is the clock start.
- Prefect schedules: monthly interim 12-month report; day-365 reminder task (`curation.task` type `REVIEW_12M`) with Telegram notification.
- This item is done when the clock and schedules exist; completion of the review is out of phase scope (see P7-B012).

## ToDo

- [ ] Verify `live_started_at` is set for the first sleeve.
- [ ] Create the monthly report schedule and the day-365 task.
- [ ] Record dates in the progress log.

## Verification

### Tests
- Integration: schedule exists; a test-clock run creates the reminder task on day 365.

### Scenarios
- Given a second sleeve goes live later, then its own clock starts at its funding date.

### Stress / failure injection
- n/a: scheduling.

## Acceptance criteria

- [ ] Clock start recorded; monthly interim report and day-365 reminder scheduled.

## Exceptions & edge cases

- Sleeve retired before 12 months: the reminder is cancelled with a reason.

## Cardinal rules (do NOT)

- Do NOT backdate the clock.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §7: clock start date.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.82 when this item is done.

## Branch & PR

- Branch: `p7/P7-T062-run-start-12-month-live-clock`
- PR title: `P7-T062: Start the 12-month live clock`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T062` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (cancelled: T7.82 is deferred to the recurring 12-month review outside the phases (17 §D P7-B012, roadmap README §10); scheduling moved into P7-T042)
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · cancelled: T7.82 deferred: the 12-month review is a recurring calendar review outside the phases (docs/17 §D P7-B012, docs/roadmap/README.md §10); the yearly schedule is built in P7-T042 and diaried in P7-T063
