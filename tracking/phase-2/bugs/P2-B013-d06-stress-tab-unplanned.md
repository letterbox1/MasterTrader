---
id: P2-B013
kind: gap
title: D06 Stress tab and risk.stress.run have no requirement in any phase
phase: 2
type: DOC
status: backlog
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
branch: p2/P2-B013-d06-stress-tab-unplanned
pr: ""
doc_sync: [docs/ui/dashboards/D06-risk.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: docs/ui/dashboards/D06-risk.md Stress tab; docs/roadmap/*
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- [ ] Decide the rule with the user (or record the decision taken in the linked task)
- [ ] Update the source doc(s) so they agree
- [ ] Update the affected task file(s) to match

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- n/a: documentation.

### Stress / failure injection
- n/a: documentation/specification gap

## Acceptance criteria

- [ ] Docs agree in one place, cross-linked from the others
- [ ] Affected tasks reference the decision

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
