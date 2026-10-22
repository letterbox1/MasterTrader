---
id: P7-B008
kind: gap
title: No API or dashboard spec for capital steps, kill-criteria state, gate reports and weekly reviews
phase: 7
type: DOC
status: done
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
doc_sync_status: done
found_in: docs/02-v1-architecture.md §7 (command catalogue, queries); docs/ui/dashboards/D03-strategies.md, D06-risk.md, D14-journal.md
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
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

- [x] Decision recorded in docs/17 (17 §D P7-B008): Phase 7 API and dashboard spec: /system/preflight, /strategies/{id}/gate-report, /risk/capital-steps, /risk/kill-criteria, /journal/reviews; lab.gate_report.generate (C1), risk.capital.fund, risk.capital_step.approve, risk.sleeve.restart, risk.review.close (C3), journal.review.signoff, ops.drill.record (C1); D06 Live tab, D03 Go-live, D14 Weekly reviews
- [x] Owning docs carry it: 02 §7 queries and §7.2 command catalogue; D06 Live tab; D03 Go-live and Gates; D14 Weekly reviews; roadmap R7.15/T7.26
- [x] Affected Phase 7 tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P7-T067, P7-T011, P7-T014, P7-T016, P7-T019, P7-T020, P7-T022
- [x] Decision and root cause noted in the progress log

## Verification

### Tests
- Doc review: the cited sections now state one consistent rule; affected task files reference it.

### Scenarios
- Given an implementer reads only the fixed docs, then they implement the same behaviour the Phase 7 tasks assume.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (02 §7 queries and §7.2 command catalogue; D06 Live tab; D03 Go-live and Gates; D14 Weekly reviews; roadmap R7.15/T7.26)
- [x] Affected tasks consistent with it (P7-T067, P7-T011, P7-T014, P7-T016, P7-T019, P7-T020, P7-T022)
- [x] Root cause noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by docs/17 17 §D P7-B008: Phase 7 API and dashboard spec: /system/preflight, /strategies/{id}/gate-report, /risk/capital-steps, /risk/kill-criteria, /journal/reviews; lab.gate_report.generate (C1), risk.capital.fund, risk.capital_step.approve, risk.sleeve.restart, risk.review.close (C3), journal.review.signoff, ops.drill.record (C1); D06 Live tab, D03 Go-live, D14 Weekly reviews. Docs now carry it: 02 §7 queries and §7.2 command catalogue; D06 Live tab; D03 Go-live and Gates; D14 Weekly reviews; roadmap R7.15/T7.26. Implementation owned by P7-T067, P7-T011, P7-T014, P7-T016, P7-T019, P7-T020, P7-T022. Root cause: Phase 7 state existed only in task files, not in the API catalogue or dashboard specs.
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P7-B008); docs updated: 02 §7 queries and §7.2 command catalogue; D06 Live tab; D03 Go-live and Gates; D14 Weekly reviews; roadmap R7.15/T7.26; implementation owned by P7-T067, P7-T011, P7-T014, P7-T016, P7-T019, P7-T020, P7-T022
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
