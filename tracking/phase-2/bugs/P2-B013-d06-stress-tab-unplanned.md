---
id: P2-B013
kind: gap
title: D06 Stress tab and risk.stress.run have no requirement in any phase
phase: 2
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.50]
roadmap_todos: []
modules: [M11]
dashboards: [D06]
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B013-d06-stress-tab-unplanned
pr: ""
doc_sync: [docs/ui/dashboards/D06-risk.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: done
found_in: docs/ui/dashboards/D06-risk.md Stress tab; docs/roadmap/*
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B013 · D06 Stress tab and risk.stress.run have no requirement in any phase

## Goal / expected outcome

The Stress tab (scenario shocks, `risk.stress.run`, `/risk/stress`) is either given a requirement/phase or marked later/optional.

## Context & references

- [D06 Stress tab](../../../docs/ui/dashboards/D06-risk.md) · [R2.50 lists D06 scope without stress](../../../docs/roadmap/phase-2-strategies-risk-lab.md)
- Affects P2-T043 (renders a placeholder), P2-T015 (VaR/ES only).

## Requirements

- **Steps to reproduce:** Search the roadmap for stress scenarios: only cost stress (lab) exists; D06 is 'Phase 2' and lists a Stress tab and command.
- **Expected:** A roadmap line (P2 or P7) or an 'optional/later' marker in D06.
- **Actual:** Unowned feature.
- **Suggested fix:** Mark Stress as P7 (before live capital) and add a requirement there, or as optional; Phase 2 ships a placeholder tab.
- **Impact:** S4: scope ambiguity.

## ToDo

- [x] Decision recorded: D06 Stress tab ships as a placeholder in P2; the historical shock replay and `risk.stress.run` are built in P7 before live capital
- [x] Docs agree: D06 Stress tab, roadmap R2.57 and R7.16
- [x] Tasks updated: P2-T043 carries R2.57/T2.38

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- n/a: documentation.

### Stress / failure injection
- n/a: documentation/specification gap

## Acceptance criteria

- [x] Docs agree in one place, cross-linked from the others (D06 Stress tab (P2 placeholder, acceptance 6); roadmap R2.57/T2.38; roadmap P7 R7.16/T7.27/T7.66)
- [x] Affected tasks reference the decision (P2-T043 (placeholder; the replay is P7 T7.27))

## Exceptions & edge cases

- Until resolved, the affected task implements the conservative option stated under Suggested fix.

## Cardinal rules (do NOT)

- Do NOT close without the doc fix merged and the dependent task(s) updated to match.
- Do NOT "fix" by silently picking a number in code; the decision is recorded in the doc and in the risk policy (user input).
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/ui/dashboards/D06-risk.md`: phase marker.

## Branch & PR

- Branch: `p2/P2-B013-d06-stress-tab-unplanned`
- PR title: `P2-B013: assign a phase to the D06 Stress tab`

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (resolved by 17 §D (P2-B013, suggested fix adopted); docs carry it (D06 Stress tab (P2 placeholder, acceptance 6); roadmap R2.57/T2.38; roadmap P7 R7.16/T7.27/T7.66); implementation owned by P2-T043 (placeholder; the replay is P7 T7.27))
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D (P2-B013, suggested fix adopted)); docs updated: D06 Stress tab (P2 placeholder, acceptance 6); roadmap R2.57/T2.38; roadmap P7 R7.16/T7.27/T7.66; implementation owned by P2-T043 (placeholder; the replay is P7 T7.27)
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
