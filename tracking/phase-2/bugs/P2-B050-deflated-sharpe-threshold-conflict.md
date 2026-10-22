---
id: P2-B050
kind: gap
title: Deflated Sharpe gate threshold conflicts (> 0 vs > 0.95)
phase: 2
type: DOC
status: done
priority: high
size: XS
severity: S2
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.42]
roadmap_todos: []
modules: [M7]
dashboards: [D03, D04]
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B050-deflated-sharpe-threshold-conflict
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/14-strategy-evidence-and-validation.md]
doc_sync_status: done
found_in: docs/03-build-spec.md §8 items 2 and 7; docs/02-v1-architecture.md §13; docs/14-strategy-evidence-and-validation.md §6–7
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B050 · Deflated Sharpe gate threshold conflicts (> 0 vs > 0.95)

## Goal / expected outcome

The docs agree and part-B tasks can be built without guessing: one deflated-Sharpe definition and threshold used by the gate evaluator and shown in D03/D04.

## Context & references

- [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) · [02 §13](../../../docs/02-v1-architecture.md#13-asset-coverage--promotion-gates) · [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7)
- Affects P2-T110, P2-T114, P2-T143

## Requirements

- **Steps to reproduce:** Read 03 §8 item 2 ('deflated Sharpe > 0') and 02 §13 item 2 (same), then 03 §8 item 7 and 14 §6 gate 2 ('> 0.95'), then 14 §7 ('deflated Sharpe > 0 at 95%').
- **Expected:** one deflated-Sharpe definition and threshold used by the gate evaluator and shown in D03/D04.
- **Actual:** see steps; the sources disagree or are silent.
- **Suggested fix:** DSR is a probability: state the gate as 'DSR (probability the true Sharpe > 0) > 0.95'; rewrite 03 §8 item 2, 02 §13 and 14 §7 to that wording.
- **Impact:** S2: the gate evaluator could pass strategies that should fail (> 0 is almost always true for a probability).

## ToDo

- [x] Decision recorded: deflated Sharpe gate is DSR ≥ 0.95 (a probability); "> 0" was an error
- [x] Docs agree: 16 §2.4, 03 §8, 02 §13, 14 §6/§7
- [x] Tasks updated: P2-T110, P2-T114 (threshold from the gate profile)

## Verification

### Tests
- Doc gap: reviewed diff; where code depends on it, the named test in the affected task asserts the decided value.

### Scenarios
- Given the decided value, when the affected task is implemented, then its tests assert that value (no hard-coded alternative).

### Stress / failure injection
- n/a: documentation/spec consistency item.

## Acceptance criteria

- [x] Docs agree in one place, cross-linked from the others (16 §2.4 (DSR ≥ 0.95, a probability); 03 §8 item 2; 02 §13 item 2; 14 §6 gate 2; 14 §7 table)
- [x] Affected tasks reference the decision (P2-T110, P2-T114)

## Exceptions & edge cases

- Until resolved, implementations use the suggested default and keep the value configurable.

## Cardinal rules (do NOT)

- Do NOT close without a regression test (code) or a reviewed doc diff (doc gap).
- Do NOT silently pick a value in code without updating the docs.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md`: align with the decision.
- `docs/02-v1-architecture.md`: align with the decision.
- `docs/14-strategy-evidence-and-validation.md`: align with the decision.

## Branch & PR

- Branch: `p2/P2-B050-deflated-sharpe-threshold-conflict`
- PR title: `P2-B050: Deflated Sharpe gate threshold conflicts (> 0 vs > 0.95)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-B050` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (resolved by 17 §A (P2-B050); docs carry it (16 §2.4 (DSR ≥ 0.95, a probability); 03 §8 item 2; 02 §13 item 2; 14 §6 gate 2; 14 §7 table); implementation owned by P2-T110, P2-T114)
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §A (P2-B050)); docs updated: 16 §2.4 (DSR ≥ 0.95, a probability); 03 §8 item 2; 02 §13 item 2; 14 §6 gate 2; 14 §7 table; implementation owned by P2-T110, P2-T114
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
