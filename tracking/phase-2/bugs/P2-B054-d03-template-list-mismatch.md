---
id: P2-B054
kind: gap
title: D03 builder template list differs from the R2.02 / 03 M0 template set
phase: 2
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.02]
roadmap_todos: []
modules: [M0, M15]
dashboards: [D03]
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B054-d03-template-list-mismatch
pr: ""
doc_sync: [docs/ui/dashboards/D03-strategies.md]
doc_sync_status: done
found_in: docs/ui/dashboards/D03-strategies.md (builder 'Template' tab)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B054 · D03 builder template list differs from the R2.02 / 03 M0 template set

## Goal / expected outcome

The docs agree and part-B tasks can be built without guessing: D03 states that the template tab is driven by `/strategies/templates` and lists the R2.02 set, with phase availability for market making (P6, optional) and LLM-signal (P6).

## Context & references

- [D03 builder](../../../docs/ui/dashboards/D03-strategies.md) · [03 M0](../../../docs/03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe) · [R2.02](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements)
- Affects P2-T144

## Requirements

- **Steps to reproduce:** D03 lists scalping, intraday, EMA/MA, mean reversion, breakout, swing, grid/DCA, market making, pairs, event, ML-signal, LLM/decision-model signal. R2.02 adds deterministic rule-based, funding carry, cross-sectional momentum, token unlock and memecoin momentum (paper-only), and puts market making and LLM-signal in later phases (P6).
- **Expected:** D03 states that the template tab is driven by `/strategies/templates` and lists the R2.02 set, with phase availability for market making (P6, optional) and LLM-signal (P6).
- **Actual:** see steps; the sources disagree or are silent.
- **Suggested fix:** Edit the D03 template list; P2-T144 renders from the API so no hard-coded list exists in the UI.
- **Impact:** S3: confusion over which templates must exist in P2 and which must be hidden.

## ToDo

- [x] Decision recorded: the template tab renders the API list (R2.02 set); later templates shown disabled with their phase
- [x] Docs agree: D03 builder
- [x] Tasks updated: P2-T144, P2-T008, P2-T009

## Verification

### Tests
- Doc gap: reviewed diff; where code depends on it, the named test in the affected task asserts the decided value.

### Scenarios
- Given the decided value, when the affected task is implemented, then its tests assert that value (no hard-coded alternative).

### Stress / failure injection
- n/a: documentation/spec consistency item.

## Acceptance criteria

- [x] Docs agree in one place, cross-linked from the others (D03 builder Template tab (rendered from `/strategies/templates`, R2.02 set, market making and LLM-signal shown disabled with their phase))
- [x] Affected tasks reference the decision (P2-T144, P2-T008, P2-T009)

## Exceptions & edge cases

- Until resolved, implementations use the suggested default and keep the value configurable.

## Cardinal rules (do NOT)

- Do NOT close without a regression test (code) or a reviewed doc diff (doc gap).
- Do NOT silently pick a value in code without updating the docs.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/dashboards/D03-strategies.md`: align with the decision.

## Branch & PR

- Branch: `p2/P2-B054-d03-template-list-mismatch`
- PR title: `P2-B054: D03 builder template list differs from the R2.02 / 03 M0 template set`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-B054` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (resolved by 17 §D (P2-B054, suggested fix adopted); docs carry it (D03 builder Template tab (rendered from `/strategies/templates`, R2.02 set, market making and LLM-signal shown disabled with their phase)); implementation owned by P2-T144, P2-T008, P2-T009)
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D (P2-B054, suggested fix adopted)); docs updated: D03 builder Template tab (rendered from `/strategies/templates`, R2.02 set, market making and LLM-signal shown disabled with their phase); implementation owned by P2-T144, P2-T008, P2-T009
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
