---
id: P4-B005
kind: gap
title: R4.05 gates YouTube on a P1 check that P1 doesn't run
phase: 4
type: DOC
status: done
priority: low
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R4.05]
roadmap_todos: []
modules: [M2]
dashboards: []
branch: p4/P4-B005-youtube-check-missing-in-p1
pr: ""
doc_sync: [docs/06-aggregators-and-market-providers.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: done
found_in: docs/roadmap/phase-4-intel.md R4.05 vs docs/roadmap/phase-1-data-and-monitoring.md T1.60 and docs/06 §3 open checks
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P4-B005 · R4.05 gates YouTube on a P1 check that P1 doesn't run

## Goal / expected outcome

The YouTube reachability/terms check has an owner; P4-T024 runs it in Phase 4 and the docs say so.

## Context & references

- Found in: [R4.05](../../../docs/roadmap/phase-4-intel.md#3-requirements) ('StockTwits/YouTube only if checks passed in P1') · [06 §3 open checks](../../../docs/06-aggregators-and-market-providers.md#3-additional-forex--multi-asset-providers) (StockTwits only)
- Related: P4-T024.

## Requirements

- **Steps to reproduce:** read P1 T1.60 — StockTwits listed, YouTube not.
- **Expected:** a YouTube check (channel RSS reachable, Data API v3 quota, yt-dlp subtitle use for chosen channels) exists somewhere.
- **Actual:** missing; R4.05 references a non-existent P1 result.
- **Impact:** S3 — conditional source can't be decided as written.
- **Suggested fix:** add YouTube to 06 §3 open checks and to P1 T1.60, or change R4.05 to 'checks passed (P1 for StockTwits, P4-T024 for YouTube)'.

## ToDo

- [x] Decision recorded: the YouTube check moves to Phase 4 (17 §D)
- [x] Docs carry it: roadmap R4.05 ('YouTube only if its P4 check (T4.65) passes') and ToDo T4.65; 06 §2 Conditional row and the 'Phase 4 check' note
- [x] Implementation owned by P4-T066 (the check, new) and P4-T024 (flagged connector)

## Verification

### Tests
- Doc review: the corrected section is consistent with the linked sources (links resolve).

### Scenarios
- Given P1 is already closed, then P4-T024 runs the YouTube check itself.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] YouTube check has an owner in Phase 4 (checked in docs/roadmap/phase-4-intel.md R4.05/T4.65 and 06 §2, 2026-10-22)
- [x] Root cause noted: R4.05 referred to a P1 check that P1 never planned

## Exceptions & edge cases

- None.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: §3 open checks: add YouTube
- `docs/roadmap/phase-4-intel.md`: R4.05 wording

## Branch & PR

- Branch: `p4/P4-B005-youtube-check-missing-in-p1`
- PR title: `P4-B005: fix r4.05 gates YouTube on a P1 check that P1 doesn't run`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-B005` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D (P4-B005); docs checked: docs/roadmap/phase-4-intel.md R4.05 + T4.65, 06 §2 (Conditional YouTube row, Phase 4 check); implementation owned by P4-T066, P4-T024; root cause: R4.05 pointed at a P1 check that didn't exist
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 §D (P4-B005); docs updated: docs/roadmap/phase-4-intel.md R4.05 + T4.65, 06 §2 conditional YouTube row + Phase 4 check; implementation owned by P4-T066, P4-T024
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
