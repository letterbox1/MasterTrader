---
id: P2-B055
kind: gap
title: Bull/bear/chop regime definition for the per-regime gate is unspecified
phase: 2
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.42, R2.46]
roadmap_todos: []
modules: [M6, M7]
dashboards: [D03, D04]
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B055-regime-definition-missing
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/03-build-spec.md]
doc_sync_status: done
found_in: docs/14-strategy-evidence-and-validation.md §6 gate 4; docs/03-build-spec.md §8 item 7 and M6
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B055 · Bull/bear/chop regime definition for the per-regime gate is unspecified

## Goal / expected outcome

The docs agree and part-B tasks can be built without guessing: a deterministic, versioned, price-based regime feature available in P2.

## Context & references

- [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [03 M6](../../../docs/03-build-spec.md#m6-features--mt_features)
- Affects P2-T111, P2-T126

## Requirements

- **Steps to reproduce:** 14 §6 requires 'profitable in each regime (bull/bear/chop)' but no doc defines the regimes; M6 regime labels come from sentiment pipelines that start in P4.
- **Expected:** a deterministic, versioned, price-based regime feature available in P2.
- **Actual:** see steps; the sources disagree or are silent.
- **Suggested fix:** Adopt `regime_v1`: bull = close > 200-day MA and 90-day return > +10%; bear = close < 200-day MA and 90-day return < −10%; chop otherwise; per asset, UTC daily; document in 14 §6 and register in M6. Sentiment-based regimes (P4) become `regime_v2` candidates.
- **Impact:** S3: without a definition the gate is untestable and could be tuned per strategy.

## ToDo

- [x] Decision recorded: `regime_v1` price-based regimes per asset, daily (bull/bear/chop), configurable per asset class
- [x] Docs agree: 16 §2.4.1, 14 §6
- [x] Tasks updated: P2-T111

## Verification

### Tests
- Doc gap: reviewed diff; where code depends on it, the named test in the affected task asserts the decided value.

### Scenarios
- Given the decided value, when the affected task is implemented, then its tests assert that value (no hard-coded alternative).

### Stress / failure injection
- n/a: documentation/spec consistency item.

## Acceptance criteria

- [x] Docs agree in one place, cross-linked from the others (16 §2.4.1 regime labels; 14 §6 item 4 (`regime_v1`))
- [x] Affected tasks reference the decision (P2-T111)

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

- Branch: `p2/P2-B055-regime-definition-missing`
- PR title: `P2-B055: Bull/bear/chop regime definition for the per-regime gate is unspecified`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-B055` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (resolved by 17 §C (P2-B055); docs carry it (16 §2.4.1 regime labels; 14 §6 item 4 (`regime_v1`)); implementation owned by P2-T111)
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §C (P2-B055)); docs updated: 16 §2.4.1 regime labels; 14 §6 item 4 (`regime_v1`); implementation owned by P2-T111
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
