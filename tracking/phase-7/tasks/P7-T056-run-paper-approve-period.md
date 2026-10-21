---
id: P7-T056
kind: task
title: Paper/approve period: confirm P1 ≥ 8 weeks and continue others
phase: 7
type: RUN
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T014]
requirements: [R7.02]
roadmap_todos: [T7.80]
modules: [M0, M11]
dashboards: [D03]
branch: p7/P7-T056-run-paper-approve-period
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T056 · Paper/approve period: confirm P1 ≥ 8 weeks and continue others

## Goal / expected outcome

Each candidate strategy's paper/approve clock is confirmed from the gate report: P1 sleeves (started in P2) have ≥ 8 weeks and pass tracking; non-P1 strategies continue toward ≥ 3 months (memecoin ≥ 300 trades). Strategies still running when the phase closes continue and are checked by their own gate reports.

## Context & references

- Roadmap: [R7.02 · ToDo T7.80](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) item 7 · [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) item 5 · Roadmap §2 entry criterion 1
- Cross-phase: P2 T2.80 (paper clock started ~10 Jan 2027).
- Related: P7-T013, P7-T014, P7-T011

## Requirements

- Weekly check (Monday, after the review pack): list each strategy's elapsed/required period, trade count and tracking verdict.
- P1 sleeves: ≥ 56 days through the real policy/risk/execution path with tracking within tolerance; otherwise the clock continues (no shortcuts).
- Non-P1: default ≥ 90 days; memecoin ≥ 300 paper trades.
- This RUN item is done when at least one P1 sleeve's paper gate passes; remaining strategies keep running and are tracked by their gate reports.

## ToDo

- [ ] Confirm P1 paper bots are running on the live-shaped config (approve/HITL mode on paper).
- [ ] Each Monday, record the period table in the progress log.
- [ ] Close when a P1 sleeve's paper gate passes; note which strategies continue.

## Verification

### Tests
- Evidence: gate report paper sections.

### Scenarios
- Given trend-on-majors passes at day 56 but carry is at day 40, then trend proceeds to funding and carry continues on paper.

### Stress / failure injection
- n/a: elapsed-time item.

## Acceptance criteria

- [ ] At least one P1 sleeve has a passing paper section in a passing gate report.
- [ ] Status of every other strategy recorded.

## Exceptions & edge cases

- Paper path interrupted > 24 h: the clock resets per P7-T011 rules; record the reason.

## Cardinal rules (do NOT)

- Do NOT shorten any paper period.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §7: paper phase dates (no figures beyond the report).
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.80 when this item is done.

## Branch & PR

- Branch: `p7/P7-T056-run-paper-approve-period`
- PR title: `P7-T056: Paper/approve period: confirm P1 ≥ 8 weeks and continue others`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T056` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
