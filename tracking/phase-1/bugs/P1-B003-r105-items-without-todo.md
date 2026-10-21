---
id: P1-B003
kind: gap
title: Alpaca real-time, FinanceDatabase and exchange_calendars have no roadmap ToDo
phase: 1
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.05]
roadmap_todos: []
modules: []
dashboards: []
branch: p1/P1-B003-r105-items-without-todo
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md]
doc_sync_status: n/a
found_in: docs/roadmap/phase-1-data-and-monitoring.md §4 (T1.20–T1.24) vs R1.05
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-B003 · Alpaca real-time, FinanceDatabase and exchange_calendars have no roadmap ToDo

## Goal / expected outcome

Every requirement maps to at least one ToDo

## Context & references

- Found in: R1.05 requires Alpaca IEX real-time (30 symbols), FinanceDatabase symbol master and `exchange_calendars`; T1.22 covers only Alpaca history and yfinance
- Related items: P1-T009, P1-T021

## Requirements

- **Where:** R1.05 requires Alpaca IEX real-time (30 symbols), FinanceDatabase symbol master and `exchange_calendars`; T1.22 covers only Alpaca history and yfinance
- **Expected:** Every requirement maps to at least one ToDo
- **Actual:** No ToDo names the Alpaca real-time stream, the symbol master or session calendars
- **Suggested fix:** Add a ToDo (e.g. T1.33 `BUILD` Alpaca IEX stream + instrument master + session calendars → R1.05) or extend T1.22's wording; tasks P1-T009 and P1-T021 already cover the work and trace to T1.22 meanwhile
- **Impact:** Traceability gap; risk of the stream being forgotten (severity S3)

## ToDo

- [ ] Edit the roadmap §4 ToDo list
- [ ] Update the affected P1 task files if the decision changes their requirements

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [ ] Docs updated and consistent
- [ ] Root cause and decision noted in the progress log

## Exceptions & edge cases

- Until fixed, related tasks follow the interim rule stated in their own files

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a number in code; the decision lands in the docs first
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: apply the fix above

## Branch & PR

- Branch: `p1/P1-B003-r105-items-without-todo`
- PR title: `P1-B003: Alpaca real-time, FinanceDatabase and exchange_calendars have no roadmap ToDo`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-B003` run

## Progress log

- 2026-10-21 00:00 · planner · opened
