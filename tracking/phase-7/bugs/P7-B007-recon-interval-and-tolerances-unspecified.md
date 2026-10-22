---
id: P7-B007
kind: gap
title: Reconciliation interval N, tolerances and 'explained' rules unspecified
phase: 7
type: DOC
status: done
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
doc_sync_status: done
found_in: docs/03-build-spec.md M16 (Reconciliation: 'every N minutes'); roadmap R7.09; docs/14-strategy-evidence-and-validation.md §7 ('unexplained within 24h')
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
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

- [x] Decision recorded in docs/17 (17 §C P7-B007): reconciliation: positions and open orders every 60 s, balances every 5 min, full EOD (Sydney); quantities exact, balances within 0.01% or dust; explained = matched to a known journal event within 24 h, otherwise unexplained (kill criterion)
- [x] Owning docs carry it: 16 §2.9; 03 M16 Reconciliation; D07 Reconciliation tab; roadmap R7.09
- [x] Affected Phase 7 tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P7-T025, P7-T027, P7-T050
- [x] Decision and root cause noted in the progress log

## Verification

### Tests
- Doc review: the cited sections now state one consistent rule; affected task files reference it.

### Scenarios
- Given an implementer reads only the fixed docs, then they implement the same behaviour the Phase 7 tasks assume.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (16 §2.9; 03 M16 Reconciliation; D07 Reconciliation tab; roadmap R7.09)
- [x] Affected tasks consistent with it (P7-T025, P7-T027, P7-T050)
- [x] Root cause noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by docs/17 17 §C P7-B007: reconciliation: positions and open orders every 60 s, balances every 5 min, full EOD (Sydney); quantities exact, balances within 0.01% or dust; explained = matched to a known journal event within 24 h, otherwise unexplained (kill criterion). Docs now carry it: 16 §2.9; 03 M16 Reconciliation; D07 Reconciliation tab; roadmap R7.09. Implementation owned by P7-T025, P7-T027, P7-T050. Root cause: 03 M16 said 'every N minutes' and never defined tolerance or 'explained'.
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §C P7-B007); docs updated: 16 §2.9; 03 M16 Reconciliation; D07 Reconciliation tab; roadmap R7.09; implementation owned by P7-T025, P7-T027, P7-T050
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
