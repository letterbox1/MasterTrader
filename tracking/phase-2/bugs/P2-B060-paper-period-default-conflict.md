---
id: P2-B060
kind: gap
title: Default paper period differs between 03 §8 (3 months) and 14 §6 (2–4 weeks)
phase: 2
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.06]
roadmap_todos: []
modules: [M0, M7]
dashboards: [D03]
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B060-paper-period-default-conflict
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/03-build-spec.md]
doc_sync_status: done
found_in: docs/03-build-spec.md §8 item 5; docs/14-strategy-evidence-and-validation.md §6 gate 7; docs/02-v1-architecture.md §13
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B060 · Default paper period differs between 03 §8 (3 months) and 14 §6 (2–4 weeks)

## Goal / expected outcome

The docs agree and part-B tasks can be built without guessing: one rule shown in D03 Gates: default ≥ 3 months, P1 sleeves ≥ 8 weeks, memecoin ≥ 300 trades.

## Context & references

- [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) · [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [phase 7](../../../docs/roadmap/phase-7-prove-and-go-live.md) R7.02
- Affects P2-T143 (Gates 'paper period elapsed / required'), P2-T180

## Requirements

- **Steps to reproduce:** 03 §8 item 5 and 02 §13 say paper/approve default 3 months; 14 §6 gate 7 says ≥ 2–4 weeks (≥ 8 weeks for P1 sleeves, ≥ 300 trades memecoin). R7.02 combines them ('default ≥ 3 months; P1 sleeves ≥ 8 weeks').
- **Expected:** one rule shown in D03 Gates: default ≥ 3 months, P1 sleeves ≥ 8 weeks, memecoin ≥ 300 trades.
- **Actual:** see steps; the sources disagree or are silent.
- **Suggested fix:** Align 14 §6 gate 7 with R7.02 wording.
- **Impact:** S4: D03 could display the wrong 'required' period.

## ToDo

- [x] Decision recorded: one paper/HITL period rule in the gate profile (16 §2.4); the old '3 months' and '2–4 weeks' wording is gone
- [x] Docs agree: 16 §2.4, 03 §8, 14 §6, roadmap R7.02
- [x] Tasks updated: P2-T007, P2-T114, P2-T180

## Verification

### Tests
- Doc gap: reviewed diff; where code depends on it, the named test in the affected task asserts the decided value.

### Scenarios
- Given the decided value, when the affected task is implemented, then its tests assert that value (no hard-coded alternative).

### Stress / failure injection
- n/a: documentation/spec consistency item.

## Acceptance criteria

- [x] Docs agree in one place, cross-linked from the others (16 §2.4 gate profile (paper/HITL ≥ 8 weeks and ≥ 50 trades; P1 sleeves ≥ 8 weeks; memecoin ≥ 300 trades; low-frequency ≥ 26 weeks); 03 §8 item 5; 14 §6 item 7; roadmap P7 R7.02)
- [x] Affected tasks reference the decision (P2-T007, P2-T114, P2-T180)

## Exceptions & edge cases

- Until resolved, implementations use the suggested default and keep the value configurable.

## Cardinal rules (do NOT)

- Do NOT close without a regression test (code) or a reviewed doc diff (doc gap).
- Do NOT silently pick a value in code without updating the docs.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md`: align with the decision.
- `docs/03-build-spec.md`: align with the decision.

## Branch & PR

- Branch: `p2/P2-B060-paper-period-default-conflict`
- PR title: `P2-B060: Default paper period differs between 03 §8 (3 months) and 14 §6 (2–4 weeks)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-B060` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (resolved by 17 §B (P2-B060, with P7-B001/B002); docs carry it (16 §2.4 gate profile (paper/HITL ≥ 8 weeks and ≥ 50 trades; P1 sleeves ≥ 8 weeks; memecoin ≥ 300 trades; low-frequency ≥ 26 weeks); 03 §8 item 5; 14 §6 item 7; roadmap P7 R7.02); implementation owned by P2-T007, P2-T114, P2-T180)
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B (P2-B060, with P7-B001/B002)); docs updated: 16 §2.4 gate profile (paper/HITL ≥ 8 weeks and ≥ 50 trades; P1 sleeves ≥ 8 weeks; memecoin ≥ 300 trades; low-frequency ≥ 26 weeks); 03 §8 item 5; 14 §6 item 7; roadmap P7 R7.02; implementation owned by P2-T007, P2-T114, P2-T180
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
