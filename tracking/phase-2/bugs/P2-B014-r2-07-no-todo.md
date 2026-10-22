---
id: P2-B014
kind: gap
title: R2.07 (sweeps, A/B, shadow mode) has no roadmap ToDo
phase: 2
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.07]
roadmap_todos: []
modules: [M0, M7]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B014-r2-07-no-todo
pr: ""
doc_sync: [docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: done
found_in: docs/roadmap/phase-2-strategies-risk-lab.md §3/§4
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B014 · R2.07 (sweeps, A/B, shadow mode) has no roadmap ToDo

## Goal / expected outcome

Every Phase 2 requirement maps to at least one ToDo.

## Context & references

- [R2.07](../../../docs/roadmap/phase-2-strategies-risk-lab.md)
- Covered in practice by P2-T030 (shadow, Part A) and Part B's sweeps/A-B task.

## Requirements

- **Steps to reproduce:** No ToDo in §4 has '→ R2.07'; T2.20 covers R2.01–R2.06 and T2.27 covers R2.40–R2.44.
- **Expected:** T2.20 → R2.01–R2.07 (shadow) and T2.27 → … + R2.07 (sweeps, A/B), or a new ToDo.
- **Actual:** Requirement untraced in the roadmap.
- **Suggested fix:** Edit the roadmap ToDo arrows.
- **Impact:** S4: traceability only.

## ToDo

- [x] Decision recorded: a dedicated ToDo T2.37 covers R2.07
- [x] Docs agree: roadmap §4 B
- [x] Tasks updated: P2-T030 (shadow) and P2-T115 (sweeps + A/B) map to T2.37

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- n/a: documentation.

### Stress / failure injection
- n/a: documentation/specification gap

## Acceptance criteria

- [x] Docs agree in one place, cross-linked from the others (roadmap phase 2 ToDo T2.37 → R2.07 (sweeps, A/B on identical data, shadow mode))
- [x] Affected tasks reference the decision (P2-T030, P2-T115)

## Exceptions & edge cases

- Until resolved, the affected task implements the conservative option stated under Suggested fix.

## Cardinal rules (do NOT)

- Do NOT close without the doc fix merged and the dependent task(s) updated to match.
- Do NOT "fix" by silently picking a number in code; the decision is recorded in the doc and in the risk policy (user input).
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/roadmap/phase-2-strategies-risk-lab.md` §4: ToDo arrows.

## Branch & PR

- Branch: `p2/P2-B014-r2-07-no-todo`
- PR title: `P2-B014: trace R2.07 to ToDos`

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (resolved by 17 §D (P2-B014, suggested fix adopted); docs carry it (roadmap phase 2 ToDo T2.37 → R2.07 (sweeps, A/B on identical data, shadow mode)); implementation owned by P2-T030, P2-T115)
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D (P2-B014, suggested fix adopted)); docs updated: roadmap phase 2 ToDo T2.37 → R2.07 (sweeps, A/B on identical data, shadow mode); implementation owned by P2-T030, P2-T115
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
