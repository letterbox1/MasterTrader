---
id: P2-B018
kind: gap
title: D06 Stress tab says the shock replay is planned as R2.57; R2.57 is now the placeholder and the replay is R7.16
phase: 2
type: DOC
status: done
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
doc_sync_status: done
found_in: docs/ui/dashboards/D06-risk.md Stress tab (Phase line)
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: 2026-10-22
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

- [x] Suggested fix applied
- [x] D06 Stress tab and header now say the replay is R7.16 (P7) and R2.57 is the P2 placeholder
- [x] P2-T043 builds the placeholder; no task change needed

## Verification

### Tests
- The affected tasks' tests encode the agreed behaviour.

### Scenarios
- Given the fixed docs, when a reader follows either section, then both describe the same behaviour.

### Stress / failure injection
- n/a: documentation gap

## Acceptance criteria

- [x] Docs agree: D06 links R7.16
- [x] Affected tasks reference the decision

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
- 2026-10-22 00:00 · wrap-up doc agent · closed in the wrap-up: D06 points the shock replay at R7.16
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · verified: docs/ui/dashboards/D06-risk.md Stress tab + header (replay planned as R7.16 / P7; R2.57 placeholder)
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the wrap-up
