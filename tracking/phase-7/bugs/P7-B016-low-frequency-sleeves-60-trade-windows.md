---
id: P7-B016
kind: gap
title: Daily trend sleeves may not reach 60 trades for months, starving decay and kill checks
phase: 7
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.06, R7.07]
roadmap_todos: []
modules: []
dashboards: []
branch: p7/P7-B016-low-frequency-sleeves-60-trade-windows
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md]
doc_sync_status: n/a
found_in: docs/14-strategy-evidence-and-validation.md §6 (rolling 60-trade decay) and §7 (live Sharpe after 60 trades)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-B016 · Daily trend sleeves may not reach 60 trades for months, starving decay and kill checks

## Goal / expected outcome

The docs agree and are specific enough to implement: add a horizon-based criterion to 14 §6–§7 and let P7-T017 store horizon distributions.

## Context & references

- Found in: `docs/14-strategy-evidence-and-validation.md §6 (rolling 60-trade decay) and §7 (live Sharpe after 60 trades)`
- Related: P7-T017, P7-T020, P7-T023

## Requirements

- **What:** A daily/4h trend sleeve on a few majors may trade only a few times a month, so 60-trade windows take a year or more.
- **Expected:** A time-based companion check for low-frequency sleeves (e.g. 90-day return vs bootstrap p5 for the same horizon) so the micro-live kill/decay protection is active early.
- **Actual:** Only trade-count windows are specified; the 30-day health check helps but only on Sharpe/DD.
- **Impact:** The first live sleeve (trend on majors) could run micro-live without its Sharpe kill criterion ever becoming active. (severity S3)
- **Suggested fix:** Add a horizon-based criterion to 14 §6–§7 and let P7-T017 store horizon distributions.

## ToDo

- [x] Decision recorded in docs/17 (17 §C P7-B016): low-frequency bots that can't reach the trade counts use time windows: ≥ 26 weeks for the paper/HITL period and a 26-week rolling window for decay
- [x] Owning docs carry it: 16 §2.4 and §2.6; 14 §6 item 7 and the decay table; roadmap R7.02/R7.07
- [x] Affected Phase 7 tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P7-T017, P7-T013, P7-T023
- [x] Decision and root cause noted in the progress log

## Verification

### Tests
- Doc review: the cited sections now state one consistent rule; affected task files reference it.

### Scenarios
- Given an implementer reads only the fixed docs, then they implement the same behaviour the Phase 7 tasks assume.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (16 §2.4 and §2.6; 14 §6 item 7 and the decay table; roadmap R7.02/R7.07)
- [x] Affected tasks consistent with it (P7-T017, P7-T013, P7-T023)
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- If the user picks a different resolution than suggested, update the dependent Phase 7 tasks in the same PR.

## Cardinal rules (do NOT)

- Do NOT resolve a conflict by picking the looser number.
- Do NOT edit generated files (`KANBAN.md`, boards, README marked blocks) by hand.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md`: apply the agreed fix.

## Branch & PR

- Branch: `p7/P7-B016-low-frequency-sleeves-60-trade-windows`
- PR title: `P7-B016: fix daily trend sleeves may not reach 60 trades for months, starving decay and kill checks`
- PR checklist: doc fix or regression test · root cause in the progress log · `./kanban done` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by docs/17 17 §C P7-B016: low-frequency bots that can't reach the trade counts use time windows: ≥ 26 weeks for the paper/HITL period and a 26-week rolling window for decay. Docs now carry it: 16 §2.4 and §2.6; 14 §6 item 7 and the decay table; roadmap R7.02/R7.07. Implementation owned by P7-T017, P7-T013, P7-T023. Root cause: only trade-count windows were specified, which starve daily trend sleeves.
