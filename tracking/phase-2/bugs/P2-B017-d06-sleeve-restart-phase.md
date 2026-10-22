---
id: P2-B017
kind: gap
title: D06 lists risk.sleeve.restart as a Phase 7 command, but sleeve halts and their C3 restart exist from Phase 2
phase: 2
type: DOC
status: backlog
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.13, R2.19]
roadmap_todos: []
modules: [M11, M15]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B017-d06-sleeve-restart-phase
pr: ""
doc_sync: [docs/ui/dashboards/D06-risk.md]
doc_sync_status: n/a
found_in: docs/ui/dashboards/D06-risk.md Backend contract (Commands line)
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B017 · D06 lists risk.sleeve.restart as a Phase 7 command, but sleeve halts and their C3 restart exist from Phase 2

## Goal / expected outcome

D06 shows `risk.sleeve.restart` (C3) as available from Phase 2, where sleeve drawdown and health halts first happen.

## Context & references

- [D06 Backend contract](../../../docs/ui/dashboards/D06-risk.md): "Phase 7: `risk.capital.fund`, `risk.capital_step.approve`, `risk.sleeve.restart`, …".
- [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) and [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write): `risk.sleeve.restart` C3, no phase limit; sleeve stage-2 halts are built in P2 (P2-T012).

## Requirements

- **Steps to reproduce:** Read the D06 Commands line.
- **Expected:** `risk.sleeve.restart` listed with the P2 commands (the Live tab may also show it).
- **Actual:** listed under Phase 7 only.
- **Suggested fix:** Move it to the P2 command list in D06. P2-T012/P2-T020 build it in P2.
- **Impact:** S4: wording only.

## ToDo

- [ ] Decide the wording with the user (or apply the suggested fix if it follows 16/17)
- [ ] Update the source doc(s) so they agree
- [ ] Update the affected task file(s) to match

## Verification

### Tests
- The affected tasks' tests encode the agreed behaviour.

### Scenarios
- Given the fixed docs, when a reader follows either section, then both describe the same behaviour.

### Stress / failure injection
- n/a: documentation gap

## Acceptance criteria

- [ ] Docs agree in one place, cross-linked from the others
- [ ] Affected tasks reference the decision

## Exceptions & edge cases

- Until resolved, the affected tasks follow 16/17 (the reference docs) as stated under Suggested fix.

## Cardinal rules (do NOT)

- Do NOT close without the doc fix merged and the dependent task(s) updated to match.
- Do NOT "fix" by silently picking a number in code; the decision is recorded in the docs and in policy.

## Doc sync on completion

- The doc(s) in `doc_sync`: aligned wording.

## Branch & PR

- Branch: `p2/P2-B017-d06-sleeve-restart-phase`
- PR title: `P2-B017: align docs`

## Progress log

- 2026-10-22 00:00 · aligner · opened during task alignment (docs/16–17 wave): doc contradiction found while aligning tasks
