---
id: P7-B006
kind: gap
title: Same decay signal is an alert, a downgrade and a kill in different docs
phase: 7
type: DOC
status: done
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
doc_sync_status: done
found_in: docs/14-strategy-evidence-and-validation.md §6 (decay → alert) vs §7 (live Sharpe after 60 trades < p5 → kill); docs/15-bots-hitl-and-worm-audit.md §1.2 (decay alert → downgrade); docs/03-build-spec.md §8 item 8
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
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

- [x] Decision recorded in docs/17 (17 §B P7-B006/P2-B011): one meaning per signal: rolling 60-trade Sharpe/hit rate < p5, CUSUM break or 5 consecutive losses → downgrade the bot to HITL; daily health check fail → halt the bot; kill criteria → halt the sleeve + step-down
- [x] Owning docs carry it: 16 §2.6; 14 §6 decay table and §7 note; 03 §8 item 8; 15 §1.2
- [x] Affected Phase 7 tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P7-T020, P7-T023, P7-T024, P7-T029, P7-T049
- [x] Decision and root cause noted in the progress log

## Verification

### Tests
- Doc review: the cited sections now state one consistent rule; affected task files reference it.

### Scenarios
- Given an implementer reads only the fixed docs, then they implement the same behaviour the Phase 7 tasks assume.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (16 §2.6; 14 §6 decay table and §7 note; 03 §8 item 8; 15 §1.2)
- [x] Affected tasks consistent with it (P7-T020, P7-T023, P7-T024, P7-T029, P7-T049)
- [x] Root cause noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by docs/17 17 §B P7-B006/P2-B011: one meaning per signal: rolling 60-trade Sharpe/hit rate < p5, CUSUM break or 5 consecutive losses → downgrade the bot to HITL; daily health check fail → halt the bot; kill criteria → halt the sleeve + step-down. Docs now carry it: 16 §2.6; 14 §6 decay table and §7 note; 03 §8 item 8; 15 §1.2. Implementation owned by P7-T020, P7-T023, P7-T024, P7-T029, P7-T049. Root cause: the same 60-trade signal was an alert, a downgrade and a kill in three docs.
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P7-B006/P2-B011); docs updated: 16 §2.6; 14 §6 decay table and §7 note; 03 §8 item 8; 15 §1.2; implementation owned by P7-T020, P7-T023, P7-T024, P7-T029, P7-T049
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:31 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
