---
id: P2-B051
kind: gap
title: 'Vendored' freqtrade analysers conflict with GPL-3.0 guidance
phase: 2
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B051-freqtrade-analysers-licence-route
pr: ""
doc_sync: [docs/03-build-spec.md, SPEC.md, docs/roadmap/phase-2-strategies-risk-lab.md, third_party/LICENSES.md]
doc_sync_status: done
found_in: docs/03-build-spec.md M7; SPEC.md research-lab row; docs/01-repo-vetting-report.md §2–3.3
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Decision recorded: personal, never-distributed use allows vendoring GPL code; freqtrade analysers stay vendored under `third_party/` with their licence, isolated in `mt_lab`; a clean-room rewrite is needed only for a SaaS (05)
- [x] Docs agree: 03 §1/M7, 01 §2, 14 §6
- [x] Tasks updated: P2-T112 (vendoring + import isolation)

## Verification

### Tests
- Doc gap: reviewed diff; where code depends on it, the named test in the affected task asserts the decided value.

### Scenarios
- Given the decided value, when the affected task is implemented, then its tests assert that value (no hard-coded alternative).

### Stress / failure injection
- n/a: documentation/spec consistency item.

## Acceptance criteria

- [x] Docs agree in one place, cross-linked from the others (03 §1 personal use; 03 M7 (analysers vendored under `third_party/` with their licence, isolated in `mt_lab`); 01 §2 superseded note and table; 14 §6)
- [x] Affected tasks reference the decision (P2-T112)

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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (resolved by 17 §A (P2-B051); docs carry it (03 §1 personal use; 03 M7 (analysers vendored under `third_party/` with their licence, isolated in `mt_lab`); 01 §2 superseded note and table; 14 §6); implementation owned by P2-T112)
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §A (P2-B051)); docs updated: 03 §1 personal use; 03 M7 (analysers vendored under `third_party/` with their licence, isolated in `mt_lab`); 01 §2 superseded note and table; 14 §6; implementation owned by P2-T112
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
