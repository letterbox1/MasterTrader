---
id: P1-B016
kind: gap
title: Which ABS CPI series drives tax indexation is not specified
phase: 1
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.06]
roadmap_todos: []
modules: []
dashboards: []
branch: p1/P1-B016-abs-cpi-series-unspecified
pr: ""
doc_sync: [docs/09-journal-and-tax.md]
doc_sync_status: n/a
found_in: docs/09-journal-and-tax.md (AU_2027_REFORM); docs/03-build-spec.md M1
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-B016 · Which ABS CPI series drives tax indexation is not specified

## Goal / expected outcome

09 names the exact series (e.g. quarterly All Groups CPI, weighted average of eight capital cities) and the as-of rule for indexation

## Context & references

- Found in: [09 Goals](../../../docs/09-journal-and-tax.md#goals) and 03 M1 say "ABS CPI" for 2027 indexation; ABS publishes quarterly and monthly CPI (and several indexes); revisions and rebasing rules are not stated
- Related items: P1-T027

## Requirements

- **Where:** [09 Goals](../../../docs/09-journal-and-tax.md#goals) and 03 M1 say "ABS CPI" for 2027 indexation; ABS publishes quarterly and monthly CPI (and several indexes); revisions and rebasing rules are not stated
- **Expected:** 09 names the exact series (e.g. quarterly All Groups CPI, weighted average of eight capital cities) and the as-of rule for indexation
- **Actual:** Unspecified; P1-T027 loads both quarterly and monthly meanwhile
- **Suggested fix:** Ask the tax agent (12 §6 trigger) and record the answer in 09
- **Impact:** P3 indexation could use the wrong series (severity S3)

## ToDo

- [ ] Raise with the tax agent via the user
- [ ] Edit 09
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

- `docs/09-journal-and-tax.md`: apply the fix above

## Branch & PR

- Branch: `p1/P1-B016-abs-cpi-series-unspecified`
- PR title: `P1-B016: Which ABS CPI series drives tax indexation is not specified`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-B016` run

## Progress log

- 2026-10-21 00:00 · planner · opened
