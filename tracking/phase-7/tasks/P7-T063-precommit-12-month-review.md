---
id: P7-T063
kind: task
title: Pre-commit the 12-month keep criteria and diary the review
phase: 7
type: USER
status: backlog
priority: medium
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P7-T042, P7-T062]
requirements: [R7.05]
roadmap_todos: [T7.10]
modules: [M11]
dashboards: [D03]
branch: p7/P7-T063-precommit-12-month-review
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T063 · Pre-commit the 12-month keep criteria and diary the review

## Goal / expected outcome

Before live results accumulate, you confirm in writing (WORM) the 12-month keep criteria — positive live net P&L, live Sharpe > 0.5, beats the benchmark — and diary the review date; at the review you keep only sleeves that pass and move the rest to hold-and-earn.

## Context & references

- Roadmap: [R7.05 · ToDo T7.10](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) · [14 §1](../../../docs/14-strategy-evidence-and-validation.md#1-viability-verdict-set-expectations-before-building) (benchmark rule; failing capital to hold-and-earn M22)
- Related: P7-T042 (report), P7-T062 (clock), gap P7-B012

## Requirements

- Criteria confirmed via `strategy.review_12m.commit` (C1, WORM) — they can later only be tightened.
- Calendar entry for day 365 per sleeve; the review uses the P7-T042 report.
- Phase scope: this item is done when the criteria are committed and the review is diaried; the review outcome is recorded later on the `REVIEW_12M` task.

## ToDo

- [ ] Read the interim report format (P7-T042).
- [ ] Commit the criteria in D03 (no loosening possible later).
- [ ] Add the review date to your calendar.
- [ ] Record in the progress log.

## Verification

### Tests
- n/a (user action).

### Scenarios
- Given month 12 arrives, then the `REVIEW_12M` task opens with the report attached and keep/retire proposals.

### Stress / failure injection
- n/a.

## Acceptance criteria

- [ ] Criteria committed (WORM) and review diaried.

## Exceptions & edge cases

- Programme ended earlier by two DD events: the review is moot; record it.

## Cardinal rules (do NOT)

- Do NOT loosen keep criteria after live trading starts.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §7: none unless criteria were tightened.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.10 when this item is done.

## Branch & PR

- Branch: `p7/P7-T063-precommit-12-month-review`
- PR title: `P7-T063: Pre-commit the 12-month keep criteria and diary the review`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T063` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
