---
id: P7-B006
kind: gap
title: Same decay signal is an alert, a downgrade and a kill in different docs
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
branch: p7/P7-B006-decay-signal-action-ambiguous
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/03-build-spec.md, docs/15-bots-hitl-and-worm-audit.md]
doc_sync_status: n/a
found_in: docs/14-strategy-evidence-and-validation.md §6 (decay → alert) vs §7 (live Sharpe after 60 trades < p5 → kill); docs/15-bots-hitl-and-worm-audit.md §1.2 (decay alert → downgrade); docs/03-build-spec.md §8 item 8
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-B006 · Same decay signal is an alert, a downgrade and a kill in different docs

## Goal / expected outcome

The docs agree and are specific enough to implement: write the ladder above into 14 §6 and reference it from 03 §8 item 8 and 15 §1.2.

## Context & references

- Found in: `docs/14-strategy-evidence-and-validation.md §6 (decay → alert) vs §7 (live Sharpe after 60 trades < p5 → kill); docs/15-bots-hitl-and-worm-audit.md §1.2 (decay alert → downgrade); docs/03-build-spec.md §8 item 8`
- Related: P7-T020, P7-T023, P7-T029

## Requirements

- **What:** The rolling 60-trade Sharpe < backtest 5th percentile appears with three different consequences.
- **Expected:** One action ladder: rolling 60-trade **hit rate** < p5 or CUSUM → alert + downgrade autonomous bots + week not clean; rolling 60-trade **Sharpe** < p5 → kill (halt sleeve).
- **Actual:** 14 §6 and 03 §8 say alert; 14 §7 says kill; 15 §1.2 says downgrade.
- **Impact:** Implementers (P7-T020/T023/T029) may disagree on what halts trading. (severity S3)
- **Suggested fix:** Write the ladder above into 14 §6 and reference it from 03 §8 item 8 and 15 §1.2.

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
- `docs/15-bots-hitl-and-worm-audit.md`: apply the agreed fix.

## Branch & PR

- Branch: `p7/P7-B006-decay-signal-action-ambiguous`
- PR title: `P7-B006: fix same decay signal is an alert, a downgrade and a kill in different docs`
- PR checklist: doc fix or regression test · root cause in the progress log · `./kanban done` run

## Progress log

- 2026-10-21 00:00 · planner · opened
