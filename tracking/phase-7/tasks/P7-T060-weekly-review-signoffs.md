---
id: P7-T060
kind: task
title: Run and sign off the weekly review every live week
phase: 7
type: USER
status: backlog
priority: critical
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P7-T016]
requirements: [R7.03]
roadmap_todos: [T7.05]
modules: [M18]
dashboards: [D14]
branch: p7/P7-T060-weekly-review-signoffs
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

# P7-T060 · Run and sign off the weekly review every live week

## Goal / expected outcome

Every week from the first paper review in this phase through phase exit, you spend 30–45 minutes on the review pack and sign it off in D14, so exit criterion 3 (weekly reviews logged for every live week) holds.

## Context & references

- Roadmap: [R7.03 · ToDo T7.05](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [04 Phase 7](../../../docs/04-plan-of-action.md#phase-7--prove-it-then-go-small-live-months-710) (weekly review) · [14 §1](../../../docs/14-strategy-evidence-and-validation.md#1-viability-verdict-set-expectations-before-building) (budget your hours) · [14 §4](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) (five worst trades) · [D14](../../../docs/ui/dashboards/D14-journal.md)
- Related: P7-T015, P7-T016, P7-T059

## Requirements

- Each week: read the five sections, tag the five worst trades (followed plan? mistake type), note actions, sign off by Sunday of the following week (7-day limit).
- Actions become tasks; any risk loosening you want still goes through C3 separately.
- Zero unsigned live weeks at phase exit.

## ToDo

- [ ] Open the Monday Telegram digest → D14 review.
- [ ] Review the five sections and tag the worst trades.
- [ ] Sign off; create follow-up actions.
- [ ] Repeat weekly; note the count of signed weeks in the progress log at phase exit.

## Verification

### Tests
- Evidence: `/journal/reviews` shows every live week signed.

### Scenarios
- Given you miss a week, then that week is dirty for capital steps and the review is still required before exit.

### Stress / failure injection
- n/a: recurring user task.

## Acceptance criteria

- [ ] Every live week in the phase has a signed review.
- [ ] Follow-up actions created or explicitly 'none'.

## Exceptions & edge cases

- Travel/illness: reviews can be done on the phone; if missed, sign late (the week stays dirty).

## Cardinal rules (do NOT)

- Do NOT approve risk loosening inside the review form; use the C3 path.
- Do NOT add discretionary overrides; the only manual action outside approve mode is flatten-and-halt with a required reason (14 §4).
- Do NOT put Telegram text into any model, RAG index or training set (12 §4–5).

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §4: none unless the review content changed.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.05 when this item is done.

## Branch & PR

- Branch: `p7/P7-T060-weekly-review-signoffs`
- PR title: `P7-T060: Run and sign off the weekly review every live week`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T060` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
