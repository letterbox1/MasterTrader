---
id: P7-B007
kind: gap
title: Reconciliation interval N, tolerances and 'explained' rules unspecified
phase: 7
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.09]
roadmap_todos: []
modules: []
dashboards: []
branch: p7/P7-B007-recon-interval-and-tolerances-unspecified
pr: ""
doc_sync: [docs/03-build-spec.md, docs/ui/dashboards/D07-data-quality.md]
doc_sync_status: n/a
found_in: docs/03-build-spec.md M16 (Reconciliation: 'every N minutes'); roadmap R7.09; docs/14-strategy-evidence-and-validation.md §7 ('unexplained within 24h')
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-B007 · Reconciliation interval N, tolerances and 'explained' rules unspecified

## Goal / expected outcome

The docs agree and are specific enough to implement: adopt the P7-T025 defaults in 03 M16 and D07.

## Context & references

- Found in: `docs/03-build-spec.md M16 (Reconciliation: 'every N minutes'); roadmap R7.09; docs/14-strategy-evidence-and-validation.md §7 ('unexplained within 24h')`
- Related: P7-T025, P7-T027

## Requirements

- **What:** The recon cadence, tolerances and what counts as 'explained' are not defined.
- **Expected:** Defaults in M16: every 5 min per live sub-account + EOD 00:05 UTC; quantity exact to lot size; balances within max(1 minor unit, 0.01%); a list of explanation rules (fill in flight < 30 s, STP cancel, fee rounding, funding timing ± 5 min, recorded manual transfer).
- **Actual:** 'N minutes' and 'unexplained' are left open.
- **Impact:** The 24 h halt (P7-T027) depends on what 'unexplained' means. (severity S3)
- **Suggested fix:** Adopt the P7-T025 defaults in 03 M16 and D07.

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

- `docs/03-build-spec.md`: apply the agreed fix.
- `docs/ui/dashboards/D07-data-quality.md`: apply the agreed fix.

## Branch & PR

- Branch: `p7/P7-B007-recon-interval-and-tolerances-unspecified`
- PR title: `P7-B007: fix reconciliation interval N, tolerances and 'explained' rules unspecified`
- PR checklist: doc fix or regression test · root cause in the progress log · `./kanban done` run

## Progress log

- 2026-10-21 00:00 · planner · opened
