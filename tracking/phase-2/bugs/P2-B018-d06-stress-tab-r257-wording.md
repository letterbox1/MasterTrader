---
id: P2-B018
kind: gap
title: D06 Stress tab says the shock replay is planned as R2.57; R2.57 is now the placeholder and the replay is R7.16
phase: 2
type: DOC
status: backlog
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.57]
roadmap_todos: []
modules: [M15]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B018-d06-stress-tab-r257-wording
pr: ""
doc_sync: [docs/ui/dashboards/D06-risk.md]
doc_sync_status: n/a
found_in: docs/ui/dashboards/D06-risk.md Stress tab (Phase line)
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B018 · D06 Stress tab says the shock replay is planned as R2.57; R2.57 is now the placeholder and the replay is R7.16

## Goal / expected outcome

D06 points the historical shock replay to P7 R7.16 and the P2 placeholder to R2.57.

## Context & references

- [D06 Stress tab](../../../docs/ui/dashboards/D06-risk.md): "The historical shock replay (May 2022, …) is planned as R2.57".
- Roadmap [R2.57](../../../docs/roadmap/phase-2-strategies-risk-lab.md) (placeholder) and [R7.16](../../../docs/roadmap/phase-7-prove-and-go-live.md) (replay).

## Requirements

- **Steps to reproduce:** Read the D06 Stress tab Phase line.
- **Expected:** 'planned as R7.16 (P7)'.
- **Actual:** 'planned as R2.57'.
- **Suggested fix:** Reword the D06 line. P2-T043 builds the placeholder.
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

- Branch: `p2/P2-B018-d06-stress-tab-r257-wording`
- PR title: `P2-B018: align docs`

## Progress log

- 2026-10-22 00:00 · aligner · opened during task alignment (docs/16–17 wave): doc contradiction found while aligning tasks
