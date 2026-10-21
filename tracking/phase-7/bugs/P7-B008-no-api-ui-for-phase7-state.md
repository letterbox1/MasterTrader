---
id: P7-B008
kind: gap
title: No API or dashboard spec for capital steps, kill-criteria state, gate reports and weekly reviews
phase: 7
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.05, R7.03, R7.01]
roadmap_todos: []
modules: []
dashboards: []
branch: p7/P7-B008-no-api-ui-for-phase7-state
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/dashboards/D06-risk.md, docs/ui/dashboards/D14-journal.md, docs/ui/dashboards/D03-strategies.md]
doc_sync_status: n/a
found_in: docs/02-v1-architecture.md §7 (command catalogue, queries); docs/ui/dashboards/D03-strategies.md, D06-risk.md, D14-journal.md
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-B008 · No API or dashboard spec for capital steps, kill-criteria state, gate reports and weekly reviews

## Goal / expected outcome

The docs agree and are specific enough to implement: add the entries above to 02 §7.1/§7.2 and sections to D03, D06, D14, D16 (the Phase 7 tasks' Doc sync lists the exact edits).

## Context & references

- Found in: `docs/02-v1-architecture.md §7 (command catalogue, queries); docs/ui/dashboards/D03-strategies.md, D06-risk.md, D14-journal.md`
- Related: P7-T011, P7-T014, P7-T016, P7-T019, P7-T020

## Requirements

- **What:** Phase 7 introduces state that users must see and act on, but the API catalogue and dashboards do not list it.
- **Expected:** Catalogue entries: `/system/preflight`, `/strategies/{id}/gate-report`, `/risk/capital-steps`, `/risk/kill-criteria`, `/journal/reviews`; commands `lab.gate_report.generate`, `risk.capital.fund` (C3), `risk.capital_step.approve` (C3), `risk.sleeve.restart` (C3), `risk.review.close` (C3), `journal.review.signoff`, `ops.drill.record`; dashboard sections in D03/D06/D14/D16.
- **Actual:** None of these exist in 02 §7 or the dashboard specs; D06 has no capital-step or kill-criteria panel; D14 has no Reviews tab.
- **Impact:** UI and API work in P7-T011/T014/T016/T019/T020/T022 lacks a spec to validate against. (severity S3)
- **Suggested fix:** Add the entries above to 02 §7.1/§7.2 and sections to D03, D06, D14, D16 (the Phase 7 tasks' Doc sync lists the exact edits).

## ToDo

- [ ] Confirm the conflict/omission against the cited sections
- [ ] Agree the resolution (the user decides where it changes risk or money rules)
- [ ] Edit the docs listed under Doc sync in one PR
- [ ] Update any Phase 7 task text that depended on the assumption

## Verification

### Tests
- Doc review: the cited sections now state one consistent rule; affected task files reference it.

### Scenarios
- Given an implementer reads only the fixed docs, then they implement the same behaviour the Phase 7 tasks assume.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Docs updated and consistent
- [ ] Root cause noted in the progress log

## Exceptions & edge cases

- If the user picks a different resolution than suggested, update the dependent Phase 7 tasks in the same PR.

## Cardinal rules (do NOT)

- Do NOT resolve a conflict by picking the looser number.
- Do NOT edit generated files (`KANBAN.md`, boards, README marked blocks) by hand.

## Doc sync on completion

- `docs/02-v1-architecture.md`: apply the agreed fix.
- `docs/ui/dashboards/D06-risk.md`: apply the agreed fix.
- `docs/ui/dashboards/D14-journal.md`: apply the agreed fix.
- `docs/ui/dashboards/D03-strategies.md`: apply the agreed fix.

## Branch & PR

- Branch: `p7/P7-B008-no-api-ui-for-phase7-state`
- PR title: `P7-B008: fix no API or dashboard spec for capital steps, kill-criteria state, gate reports and weekly reviews`
- PR checklist: doc fix or regression test · root cause in the progress log · `./kanban done` run

## Progress log

- 2026-10-21 00:00 · planner · opened
