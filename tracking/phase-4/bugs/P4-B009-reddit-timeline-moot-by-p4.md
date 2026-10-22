---
id: P4-B009
kind: gap
title: Reddit timeline makes T4.05 likely moot by Phase 4; no connector ToDo if 'yes'
phase: 4
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: []
roadmap_todos: [T4.05]
modules: [M2]
dashboards: [D08]
branch: p4/P4-B009-reddit-timeline-moot-by-p4
pr: ""
doc_sync: [docs/roadmap/phase-4-intel.md]
doc_sync_status: done
found_in: docs/roadmap/phase-4-intel.md T4.05 vs docs/06-aggregators-and-market-providers.md §0
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P4-B009 · Reddit timeline makes T4.05 likely moot by Phase 4; no connector ToDo if 'yes'

## Goal / expected outcome

T4.05 states the sunset context and what happens on 'yes' (an optional connector item), or is dropped.

## Context & references

- Found in: [T4.05](../../../docs/roadmap/phase-4-intel.md#4-todo-sets) · [06 §0](../../../docs/06-aggregators-and-market-providers.md#0-️-time-sensitive-actions) (new access closes 2026-10-31; public Data API closes 2027-01 → 03 (U)); P4 is scheduled 8 Feb – 7 Mar 2027
- Related: P4-T004.

## Requirements

- **Steps to reproduce:** compare P4 dates (roadmap README) with the Reddit timeline.
- **Expected:** T4.05 notes the sunset and that a 'yes' creates an optional connector item.
- **Actual:** T4.05 says 'if yes it joins as optional' with no build ToDo and no sunset note.
- **Impact:** S4 — minor planning ambiguity.
- **Suggested fix:** add the note to T4.05 / §7 risks.

## ToDo

- [x] Decision recorded: Reddit stays optional (17 §D)
- [x] Docs carry it: roadmap T4.05 ('if it wasn't granted by the 2026-10-31 deadline, Reddit stays out and needs no build ToDo') and scope 'Out'; 06 §0 sunset timeline and 06 §2 Deferred row ('a connector is an optional item, and not worth building once the public Data API closes')
- [x] Implementation owned by P4-T004 (your yes/no record); no build task unless access was granted

## Verification

### Tests
- Doc review: the corrected section is consistent with the linked sources (links resolve).

### Scenarios
- Given access was granted but the API closes in March 2027, then don't build it.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] T4.05 states the deadline and what 'yes' means (checked in docs/roadmap/phase-4-intel.md T4.05 and 06 §0/§2, 2026-10-22)
- [x] Root cause noted: T4.05 was written before the Reddit sunset timeline was known

## Exceptions & edge cases

- None.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/roadmap/phase-4-intel.md`: T4.05 note

## Branch & PR

- Branch: `p4/P4-B009-reddit-timeline-moot-by-p4`
- PR title: `P4-B009: fix reddit timeline makes T4.05 likely moot by Phase 4; no connector ToDo if 'yes'`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-B009` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D (P4-B009); docs checked: docs/roadmap/phase-4-intel.md T4.05 + §1 Out, 06 §0 and §2 Deferred row; implementation owned by P4-T004; root cause: T4.05 predated the sunset timeline
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 §D (P4-B009); docs updated: docs/roadmap/phase-4-intel.md T4.05 + §1 Out, 06 §0 and §2 Deferred row; implementation owned by P4-T004
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
