---
id: P7-T056
kind: task
title: Paper/HITL period: confirm P1 ≥ 8 weeks and continue others
phase: 7
type: RUN
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T014, P2-T180]
requirements: [R7.02]
roadmap_todos: [T7.80]
modules: [M0, M11]
dashboards: [D03]
tools: [git, uv]
mcp: []
env: []
services: [postgres, mt-api]
branch: p7/P7-T056-run-paper-approve-period
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P7-T056 · Paper/HITL period: confirm P1 ≥ 8 weeks and continue others

## Goal / expected outcome

Each candidate bot's paper/HITL period is confirmed from the gate report against its gate profile (16 §2.4): P1 sleeves (clock started in P2) have ≥ 8 weeks and pass tracking; other bots continue toward ≥ 8 weeks **and** ≥ 50 trades (memecoin ≥ 300 trades; low-frequency ≥ 26 weeks). Strategies still running when the phase closes continue and are checked by their own gate reports.

## Context & references

- Roadmap: [R7.02 · ToDo T7.80](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) item 7 · [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) item 5 · [16 §2.4](../../../docs/16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile) · Roadmap §2 entry criterion 1
- Cross-phase: P2-T180 (`depends_on`: the P1-sleeve paper clock, T2.80).
- Related: P7-T013, P7-T014, P7-T011

## Requirements

- Weekly check (Monday, after the review pack): list each strategy's elapsed/required period, trade count and tracking verdict.
- P1 sleeves: ≥ 56 days through the real policy/risk/execution path with tracking within tolerance; otherwise the clock continues (no shortcuts).
- Other bots: default ≥ 8 weeks and ≥ 50 trades; memecoin ≥ 300 paper trades; low-frequency bots ≥ 26 weeks (16 §2.4; your gate profile may be stricter).
- This RUN item is done when at least one P1 sleeve's paper gate passes; remaining strategies keep running and are tracked by their gate reports.

## ToDo

- [ ] Confirm P1 paper bots are running on the live-shaped config (`hitl` mode on paper).
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
- PR title: `P7-T056: Paper/HITL period: confirm P1 ≥ 8 weeks and continue others`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T056` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (paper/HITL period per 16 §2.4 (≥ 8 weeks and ≥ 50 trades; 26-week low-frequency); dep P2-T180)
