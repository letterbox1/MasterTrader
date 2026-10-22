---
id: P7-T063
kind: task
title: Diary the recurring 12-month review and pre-commit its keep criteria
phase: 7
type: USER
status: backlog
priority: medium
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P7-T042, P7-T057]
requirements: [R7.05]
roadmap_todos: [T7.10]
modules: [M11]
dashboards: [D03]
tools: []
mcp: []
env: []
services: [your calendar]
branch: p7/P7-T063-precommit-12-month-review
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T063 · Diary the recurring 12-month review and pre-commit its keep criteria

## Goal / expected outcome

Before live results accumulate, you confirm in writing (WORM) the 12-month keep criteria (positive live net P&L, live Sharpe > 0.5, beats the benchmark) and put the 12-month review in your calendar as a **recurring yearly review** from the first live funding (T7.10). The reviews themselves are standing operations after P7 closes, not phase work ([roadmap README §10](../../../docs/roadmap/README.md#10-standing-operations-recurring-outside-the-phases), [17 §D P7-B012](../../../docs/17-decisions-register.md#d-other-decisions)).

## Context & references

- Roadmap: [R7.05 · ToDo T7.10](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) · [14 §1](../../../docs/14-strategy-evidence-and-validation.md#1-viability-verdict-set-expectations-before-building) (benchmark rule; failing capital to hold-and-earn M22)
- Related: P7-T042 (yearly `REVIEW_12M` task + report), P7-T057 (first funding date), P7-T062 (cancelled)

## Requirements

- Criteria recorded as sleeve settings in the layered policy via `risk.policy.update` (a WORM version row; defaults from 14 §7); later changes can only tighten without C3.
- A recurring calendar entry (yearly from each sleeve's first live funding) in your own calendar, matching the `REVIEW_12M` tasks P7-T042 schedules; the review uses that report.
- Phase scope: this item is done when the criteria are committed and the review is diaried; the review outcome is recorded later on the `REVIEW_12M` task.

## ToDo

- [ ] Read the interim report format (P7-T042).
- [ ] Commit the criteria as sleeve settings (D06 policy editor; loosening later would be C3).
- [ ] Add the 12-month review to your calendar as a yearly recurring event from the first funding date.
- [ ] Record in the progress log.

## Verification

### Tests
- n/a (user action).

### Scenarios
- Given month 12 arrives, then the `REVIEW_12M` task opens with the report attached and keep/retire proposals.

### Stress / failure injection
- n/a.

## Acceptance criteria

- [ ] Criteria committed (WORM settings version) and the recurring review in your calendar.

## Exceptions & edge cases

- Programme ended earlier by two DD events: the review is moot; record it.

## Cardinal rules (do NOT)

- Do NOT loosen keep criteria after live trading starts (any loosening is C3).
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §7: none unless criteria were tightened.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.10 when this item is done.

## Branch & PR

- Branch: `p7/P7-T063-precommit-12-month-review`
- PR title: `P7-T063: Diary the recurring 12-month review and pre-commit its keep criteria`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T063` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (T7.10 re-scoped to a recurring calendar review per 17 §D P7-B012 and README §10; criteria as settings (no new command); dep on cancelled P7-T062 replaced by P7-T057)
