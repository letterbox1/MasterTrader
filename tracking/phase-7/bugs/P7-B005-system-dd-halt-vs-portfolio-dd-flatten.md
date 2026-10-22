---
id: P7-B005
kind: gap
title: 10% system drawdown halt vs 25% portfolio DD flatten: interaction undefined
phase: 7
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.06]
roadmap_todos: []
modules: []
dashboards: []
branch: p7/P7-B005-system-dd-halt-vs-portfolio-dd-flatten
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md]
doc_sync_status: done
found_in: docs/14-strategy-evidence-and-validation.md §5 (system DD 10% → halt) and §7 (portfolio DD > 25% → flatten to stables + 30-day review)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P7-B005 · 10% system drawdown halt vs 25% portfolio DD flatten: interaction undefined

## Goal / expected outcome

The docs agree and are specific enough to implement: add to 14 §5/§7: '10% system DD → halt new entries and alert; existing positions keep stops. 25% → flatten. Basis: time-weighted trading equity excluding vault and hold-and-earn.'

## Context & references

- Found in: `docs/14-strategy-evidence-and-validation.md §5 (system DD 10% → halt) and §7 (portfolio DD > 25% → flatten to stables + 30-day review)`
- Related: P7-T022, P7-T048

## Requirements

- **What:** Two portfolio-level drawdown rules exist without a stated relationship or a common equity basis.
- **Expected:** A statement that the 10% halt stops new risk (positions stay with stops) and the 25% rule flattens; plus the equity basis (trading equity excluding vault/hold-and-earn; cash-flow adjusted).
- **Actual:** If the 10% halt holds positions, gaps can still take DD past 25%; neither doc defines the basis or whether hold-and-earn counts.
- **Impact:** P7-T022 could flatten too early/late or count the wrong equity. (severity S3)
- **Suggested fix:** Add to 14 §5/§7: '10% system DD → halt new entries and alert; existing positions keep stops. 25% → flatten. Basis: time-weighted trading equity excluding vault and hold-and-earn.'

## ToDo

- [x] Decision recorded in docs/17 (17 §B P7-B005): two-stage system drawdown: 10% → no new entries (exits and stops continue); 25% → flatten to stables/AUD + 30-day lock; two stage-2 events end the programme; basis = trading equity excl. vault and hold-and-earn, cash-flow adjusted, from its running peak
- [x] Owning docs carry it: 16 §2.1 (system stages and drawdown basis); 14 §5 limits table and drawdown notes; 14 §7
- [x] Affected Phase 7 tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P7-T022, P7-T048 (P2-T012 builds the evaluators)
- [x] Decision and root cause noted in the progress log

## Verification

### Tests
- Doc review: the cited sections now state one consistent rule; affected task files reference it.

### Scenarios
- Given an implementer reads only the fixed docs, then they implement the same behaviour the Phase 7 tasks assume.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (16 §2.1 (system stages and drawdown basis); 14 §5 limits table and drawdown notes; 14 §7)
- [x] Affected tasks consistent with it (P7-T022, P7-T048 (P2-T012 builds the evaluators))
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- If the user picks a different resolution than suggested, update the dependent Phase 7 tasks in the same PR.

## Cardinal rules (do NOT)

- Do NOT resolve a conflict by picking the looser number.
- Do NOT edit generated files (`KANBAN.md`, boards, README marked blocks) by hand.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md`: apply the agreed fix.

## Branch & PR

- Branch: `p7/P7-B005-system-dd-halt-vs-portfolio-dd-flatten`
- PR title: `P7-B005: fix 10% system drawdown halt vs 25% portfolio DD flatten: interaction undefined`
- PR checklist: doc fix or regression test · root cause in the progress log · `./kanban done` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by docs/17 17 §B P7-B005: two-stage system drawdown: 10% → no new entries (exits and stops continue); 25% → flatten to stables/AUD + 30-day lock; two stage-2 events end the programme; basis = trading equity excl. vault and hold-and-earn, cash-flow adjusted, from its running peak. Docs now carry it: 16 §2.1 (system stages and drawdown basis); 14 §5 limits table and drawdown notes; 14 §7. Implementation owned by P7-T022, P7-T048 (P2-T012 builds the evaluators). Root cause: the 10% halt and the 25% flatten were written in different sections with no common basis.
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P7-B005); docs updated: 16 §2.1 (system stages and drawdown basis); 14 §5 limits table and drawdown notes; 14 §7; implementation owned by P7-T022, P7-T048 (P2-T012 builds the evaluators)
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
