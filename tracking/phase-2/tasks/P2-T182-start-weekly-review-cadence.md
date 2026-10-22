---
id: P2-T182
kind: task
title: Start the weekly worst-five-trades and cost review
phase: 2
type: RUN
status: backlog
priority: medium
size: XS
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T150, P2-T180]
requirements: []
roadmap_todos: [T2.81]
modules: [M7, M16]
dashboards: [D05]
tools: []
mcp: []
env: []
services: [telegram]
branch: p2/P2-T182-start-weekly-review-cadence
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T182 · Start the weekly worst-five-trades and cost review

## Goal / expected outcome

The weekly review becomes a habit: the first two weekly packs after the paper clock starts are produced, reviewed and their actions captured; the cadence then continues through P3–P7.

## Context & references

- Roadmap: ToDo T2.81 · [14 §4 discipline](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) · report flow P2-T150

## Requirements

- Two consecutive Monday packs delivered (Telegram link + HTML) and reviewed within 48 h.
- Actions from each review recorded (bug items for cost-model drift > 1.5×, exit-plan violations, strategy follow-ups).
- Review time budgeted per 14 §1 (weekly worst-five-trades review).

## ToDo

- [ ] Confirm schedule fired twice
- [ ] Review packs; record actions as items
- [ ] Note cadence continuation for later phases

## Verification

### Tests
- n/a: operational run; flow tested in P2-T150.

### Scenarios
- Given a week with no closed trades, then the pack says so and the review is still logged.

### Stress / failure injection
- n/a: operational cadence.

## Acceptance criteria

- [ ] Two reviews completed with actions recorded

## Exceptions & edge cases

- Holiday weeks: skip is logged, not silent.

## Cardinal rules (do NOT)

- Do NOT change strategy parameters directly from the review; changes go through the lab and lifecycle.
- Do NOT put Telegram text (or any `model_input_ok = false` / `train_ok = false` row) into a model, prompt, RAG index or training set (12 §4–5).

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §4: link to the first reviews.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.81 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T182-start-weekly-review-cadence`
- PR title: `P2-T182: Start the weekly worst-five-trades and cost review`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T182` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields (no decision change))
