---
id: P1-B016
kind: gap
title: Which ABS CPI series drives tax indexation is not specified
phase: 1
type: DOC
status: ready
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
tools: []
mcp: []
env: []
services: []
branch: p1/P1-B016-abs-cpi-series-unspecified
pr: ""
doc_sync: [docs/09-journal-and-tax.md]
doc_sync_status: n/a
found_in: docs/09-journal-and-tax.md (AU_2027_REFORM); docs/03-build-spec.md M1
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Decision recorded in docs/17 (17 §D P1-B016): All groups CPI, weighted average of eight capital cities, quarterly, series A2325846C (U)
- [x] Aligned docs carry it: 03 M1 (ABS CPI), 06 §3 (ABS CPI tax input; open checks), 09 (key findings; AU_2027_REFORM; tax-agent question 9); roadmap R1.06, T1.60
- [x] P1-T027 loads the configured series ID (`macro.abs_cpi_series`); P1-T056 owns the ID check
- [ ] Verify the series ID A2325846C and its release calendar via the ABS Data API (P1-T056, T1.60) and record the result in 06 §3
- [ ] The as-of rule for indexation is confirmed by your tax agent (09 question 9; a P3 tax-agent USER item)

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [x] Docs name the series and mark the ID (U)
- [ ] Series ID verified (or corrected in `config/universe.yaml` and the docs) with evidence from P1-T056
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
- 2026-10-22 00:00 · aligner · decision in 17 §D P1-B016 and carried by 03 M1, 06 §3, 09; left open because the series ID is (U) until verified: owned by P1-T056 (T1.60), loaded by P1-T027 from config; severity stays S3; the indexation as-of rule goes to the tax agent in P3
