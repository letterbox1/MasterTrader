---
id: P7-B009
kind: gap
title: Autonomous mode is 'per strategy' in R7.08 but 'per bot' in 15 §1
phase: 7
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.08]
roadmap_todos: []
modules: []
dashboards: []
branch: p7/P7-B009-auto-mode-per-strategy-vs-per-bot
pr: ""
doc_sync: [docs/roadmap/phase-7-prove-and-go-live.md, docs/15-bots-hitl-and-worm-audit.md, docs/02-v1-architecture.md]
doc_sync_status: done
found_in: docs/roadmap/phase-7-prove-and-go-live.md R7.08; docs/02-v1-architecture.md §7.2 (`strategy.set_mode` and `bot.set_mode`); docs/15-bots-hitl-and-worm-audit.md §1.2
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P7-B009 · Autonomous mode is 'per strategy' in R7.08 but 'per bot' in 15 §1

## Goal / expected outcome

The docs agree and are specific enough to implement: update R7.08 wording and add the precedence rule to 15 §1.2 and 02 §7.2.

## Context & references

- Found in: `docs/roadmap/phase-7-prove-and-go-live.md R7.08; docs/02-v1-architecture.md §7.2 (`strategy.set_mode` and `bot.set_mode`); docs/15-bots-hitl-and-worm-audit.md §1.2`
- Related: P7-T028, P7-T058

## Requirements

- **What:** Mode is defined at two levels with no precedence rule.
- **Expected:** R7.08 reads 'autonomous mode is C3 per bot (15 §1)'; precedence: the stricter of strategy-level and bot-level mode applies.
- **Actual:** R7.08 says 'per strategy'; both `strategy.set_mode` and `bot.set_mode` exist with autonomous = C3.
- **Impact:** Two paths to autonomy; a strategy-level change could appear to promote every bot at once. (severity S3)
- **Suggested fix:** Update R7.08 wording and add the precedence rule to 15 §1.2 and 02 §7.2.

## ToDo

- [x] Decision recorded in docs/17 (17 §B P2-B053/P7-B009): modes are paper/hitl/autonomous, set per bot; a strategy is promoted through gates and its mode caps its bots (the stricter applies)
- [x] Owning docs carry it: roadmap R7.08; 16 §2.3 strategy mode ceiling; 02 §7.2 strategy.set_mode row; 15 §1
- [x] Affected Phase 7 tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P7-T028, P7-T058
- [x] Decision and root cause noted in the progress log

## Verification

### Tests
- Doc review: the cited sections now state one consistent rule; affected task files reference it.

### Scenarios
- Given an implementer reads only the fixed docs, then they implement the same behaviour the Phase 7 tasks assume.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (roadmap R7.08; 16 §2.3 strategy mode ceiling; 02 §7.2 strategy.set_mode row; 15 §1)
- [x] Affected tasks consistent with it (P7-T028, P7-T058)
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- If the user picks a different resolution than suggested, update the dependent Phase 7 tasks in the same PR.

## Cardinal rules (do NOT)

- Do NOT resolve a conflict by picking the looser number.
- Do NOT edit generated files (`KANBAN.md`, boards, README marked blocks) by hand.

## Doc sync on completion

- `docs/roadmap/phase-7-prove-and-go-live.md`: apply the agreed fix.
- `docs/15-bots-hitl-and-worm-audit.md`: apply the agreed fix.
- `docs/02-v1-architecture.md`: apply the agreed fix.

## Branch & PR

- Branch: `p7/P7-B009-auto-mode-per-strategy-vs-per-bot`
- PR title: `P7-B009: fix autonomous mode is 'per strategy' in R7.08 but 'per bot' in 15 §1`
- PR checklist: doc fix or regression test · root cause in the progress log · `./kanban done` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by docs/17 17 §B P2-B053/P7-B009: modes are paper/hitl/autonomous, set per bot; a strategy is promoted through gates and its mode caps its bots (the stricter applies). Docs now carry it: roadmap R7.08; 16 §2.3 strategy mode ceiling; 02 §7.2 strategy.set_mode row; 15 §1. Implementation owned by P7-T028, P7-T058. Root cause: R7.08 said 'per strategy' while 15 §1 set modes per bot, with no precedence.
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P2-B053/P7-B009); docs updated: roadmap R7.08; 16 §2.3 strategy mode ceiling; 02 §7.2 strategy.set_mode row; 15 §1; implementation owned by P7-T028, P7-T058
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
