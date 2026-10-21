---
id: P7-B003
kind: gap
title: Capital-step rules undefined: 'clean week', 25% base, step-down
phase: 7
type: DOC
status: backlog
priority: high
size: S
severity: S2
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.05]
roadmap_todos: []
modules: []
dashboards: []
branch: p7/P7-B003-capital-step-semantics-undefined
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: docs/14-strategy-evidence-and-validation.md §7; docs/03-build-spec.md §8 item 6
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-B003 · Capital-step rules undefined: 'clean week', 25% base, step-down

## Goal / expected outcome

The docs agree and are specific enough to implement: adopt the P7-T018 defaults in 14 §7: clean = no kill breach, no unexplained recon break > 24 h, no decay/health alert, DQ-paused < 10% of hours, review signed, P&L within the 5th–95th band, no limit breach; step = +25% of current sleeve capital; after any halt, restart at the previous step's capital minus one step (min micro) with the streak at 0.

## Context & references

- Found in: `docs/14-strategy-evidence-and-validation.md §7; docs/03-build-spec.md §8 item 6`
- Related: P7-T018, P7-T019, P7-T061

## Requirements

- **What:** The capital-step rule is load-bearing for live money but its terms are not defined.
- **Expected:** Written definitions of (a) a clean week, (b) what the 25% is a percentage of, (c) what happens to capital after a kill/halt and restart (step back, reset to micro, or keep).
- **Actual:** Docs only say '25% steps after 4 clean weeks each' and 'up to A$10–25k'. No definition of clean; unclear whether 25% is of the current sleeve capital, of the initial micro amount, or of the A$10–25k target.
- **Impact:** P7-T018/T019 must invent the rule; a looser reading would scale capital faster than intended. (severity S2)
- **Suggested fix:** Adopt the P7-T018 defaults in 14 §7: clean = no kill breach, no unexplained recon break > 24 h, no decay/health alert, DQ-paused < 10% of hours, review signed, P&L within the 5th–95th band, no limit breach; step = +25% of current sleeve capital; after any halt, restart at the previous step's capital minus one step (min micro) with the streak at 0.

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

- `docs/14-strategy-evidence-and-validation.md`: apply the agreed fix.
- `docs/03-build-spec.md`: apply the agreed fix.

## Branch & PR

- Branch: `p7/P7-B003-capital-step-semantics-undefined`
- PR title: `P7-B003: fix capital-step rules undefined: 'clean week', 25% base, step-down`
- PR checklist: doc fix or regression test · root cause in the progress log · `./kanban done` run

## Progress log

- 2026-10-21 00:00 · planner · opened
