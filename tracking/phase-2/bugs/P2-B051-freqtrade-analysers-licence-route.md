---
id: P2-B051
kind: gap
title: 'Vendored' freqtrade analysers conflict with GPL-3.0 guidance
phase: 2
type: DOC
status: backlog
priority: high
size: XS
severity: S2
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.43]
roadmap_todos: []
modules: [M7]
dashboards: [D04]
branch: p2/P2-B051-freqtrade-analysers-licence-route
pr: ""
doc_sync: [docs/03-build-spec.md, SPEC.md, docs/roadmap/phase-2-strategies-risk-lab.md, third_party/LICENSES.md]
doc_sync_status: n/a
found_in: docs/03-build-spec.md M7; SPEC.md research-lab row; docs/01-repo-vetting-report.md §2–3.3
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-B051 · 'Vendored' freqtrade analysers conflict with GPL-3.0 guidance

## Goal / expected outcome

The docs agree and part-B tasks can be built without guessing: a single decided route for the analysers: clean-room re-implementation, GPL module accepted for private use, or freqtrade run unmodified as an external process.

## Context & references

- [03 M7](../../../docs/03-build-spec.md#m7-research-lab--mt_lab) · [01 §3.3](../../../docs/01-repo-vetting-report.md#33-freqtrade--reference-only) · [SPEC](../../../SPEC.md#non-negotiable-requirements)
- Affects P2-T112

## Requirements

- **Steps to reproduce:** 03 M7, SPEC and roadmap R2.43/T2.27 say 'vendored freqtrade look-ahead/recursive analysers'; 01 says freqtrade is GPL-3.0, 'GPL blocks importing the code', 're-implement freqtrade's ideas' and recommends keeping the core permissive.
- **Expected:** a single decided route for the analysers: clean-room re-implementation, GPL module accepted for private use, or freqtrade run unmodified as an external process.
- **Actual:** see steps; the sources disagree or are silent.
- **Suggested fix:** Default to a clean-room re-implementation in `mt_lab/bias/` (from freqtrade's public docs, no code copied) and replace 'vendored' with 're-implemented (freqtrade method)' in 03 M7, SPEC and the roadmap.
- **Impact:** S2: copying GPL code into `mt_lab` would contradict the stated licence posture and block any later SaaS option (05).

## ToDo

- [ ] Decide the resolution (owner: you, with the planner's suggestion as default)
- [ ] Edit the listed docs in one PR so they agree
- [ ] Update the affected part-B task files (Requirements/Acceptance) if the decision differs from the default
- [ ] Add/adjust the regression test named below where code depends on it

## Verification

### Tests
- Doc gap: reviewed diff; where code depends on it, the named test in the affected task asserts the decided value.

### Scenarios
- Given the decided value, when the affected task is implemented, then its tests assert that value (no hard-coded alternative).

### Stress / failure injection
- n/a: documentation/spec consistency item.

## Acceptance criteria

- [ ] Docs listed under Doc sync agree with each other
- [ ] Affected tasks reference the decision
- [ ] Root cause noted in the progress log

## Exceptions & edge cases

- Until resolved, implementations use the suggested default and keep the value configurable.

## Cardinal rules (do NOT)

- Do NOT close without a regression test (code) or a reviewed doc diff (doc gap).
- Do NOT silently pick a value in code without updating the docs.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md`: align with the decision.
- `SPEC.md`: align with the decision.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: align with the decision.
- `third_party/LICENSES.md`: align with the decision.

## Branch & PR

- Branch: `p2/P2-B051-freqtrade-analysers-licence-route`
- PR title: `P2-B051: 'Vendored' freqtrade analysers conflict with GPL-3.0 guidance`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-B051` run

## Progress log

- 2026-10-21 00:00 · planner · opened
