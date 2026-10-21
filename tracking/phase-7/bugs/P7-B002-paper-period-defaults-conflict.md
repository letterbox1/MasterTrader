---
id: P7-B002
kind: gap
title: Paper/approve period defaults conflict across docs
phase: 7
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.02]
roadmap_todos: []
modules: []
dashboards: []
branch: p7/P7-B002-paper-period-defaults-conflict
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/02-v1-architecture.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: docs/03-build-spec.md §8 item 5; docs/14-strategy-evidence-and-validation.md §6 item 7; docs/02-v1-architecture.md §12 (Phase 7 row) and §13 item 5
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-B002 · Paper/approve period defaults conflict across docs

## Goal / expected outcome

The docs agree and are specific enough to implement: replace '≥ 2–4 weeks' in 14 §6 with the R7.02 table and change 02 §12's Phase 7 exit to 'gates passed per strategy; paper per R7.02'.

## Context & references

- Found in: `docs/03-build-spec.md §8 item 5; docs/14-strategy-evidence-and-validation.md §6 item 7; docs/02-v1-architecture.md §12 (Phase 7 row) and §13 item 5`
- Related: P7-T013, P7-T056

## Requirements

- **What:** Paper-period minimums are inconsistent.
- **Expected:** One table: P1 sleeves ≥ 8 weeks; memecoin ≥ 300 trades; all other strategies default ≥ 3 months — as R7.02 states.
- **Actual:** 03 §8 says default 3 months; 14 §6 says '≥ 2–4 weeks' as the general minimum; 02 §12 sets the Phase 7 exit as '≥ 3 months paper/approve' for all, contradicting the 8-week P1 rule.
- **Impact:** Ambiguous gate thresholds; the roadmap's critical path (8-week P1 clock) conflicts with the architecture's phase exit. (severity S3)
- **Suggested fix:** Replace '≥ 2–4 weeks' in 14 §6 with the R7.02 table and change 02 §12's Phase 7 exit to 'gates passed per strategy; paper per R7.02'.

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
- `docs/02-v1-architecture.md`: apply the agreed fix.
- `docs/03-build-spec.md`: apply the agreed fix.

## Branch & PR

- Branch: `p7/P7-B002-paper-period-defaults-conflict`
- PR title: `P7-B002: fix paper/approve period defaults conflict across docs`
- PR checklist: doc fix or regression test · root cause in the progress log · `./kanban done` run

## Progress log

- 2026-10-21 00:00 · planner · opened
