---
id: P1-B014
kind: gap
title: Venue-health inputs (withdrawal delays, PoR, AUSTRAC) have no defined free sources
phase: 1
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.13]
roadmap_todos: []
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p1/P1-B014-venue-health-sources-undefined
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/13-wallets-treasury-and-onchain.md]
doc_sync_status: done
found_in: docs/12-policy-and-compliance.md §2; docs/13-wallets-treasury-and-onchain.md §6; docs/roadmap/phase-1-data-and-monitoring.md R1.13
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-B014 · Venue-health inputs (withdrawal delays, PoR, AUSTRAC) have no defined free sources

## Goal / expected outcome

Docs list the signals per venue (status endpoints, deposit/withdraw flags, official status RSS, user notes) and state that AUSTRAC re-checks are a reminder to you, not automated

## Context & references

- Found in: [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) and [13 §6](../../../docs/13-wallets-treasury-and-onchain.md#6-monitors-feed-m16-and-m11) require withdrawal delays, proof-of-reserve changes and AUSTRAC status; no API or source is named; the AUSTRAC register has no API and the task queue (M19) arrives in P5
- Related items: P1-T043

## Requirements

- **Where:** [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) and [13 §6](../../../docs/13-wallets-treasury-and-onchain.md#6-monitors-feed-m16-and-m11) require withdrawal delays, proof-of-reserve changes and AUSTRAC status; no API or source is named; the AUSTRAC register has no API and the task queue (M19) arrives in P5
- **Expected:** Docs list the signals per venue (status endpoints, deposit/withdraw flags, official status RSS, user notes) and state that AUSTRAC re-checks are a reminder to you, not automated
- **Actual:** Undefined; risk of scraping or of a monitor with no inputs
- **Suggested fix:** Adopt the P1-T043 design in 12 §2 / 13 §6; route the AUSTRAC reminder to notifications/Telegram until M19 exists
- **Impact:** R1.13 under-specified (severity S3)

## ToDo

- [x] Decision recorded in docs/17 (17 §D P1-B014): venue health = our own measured withdrawal times + venue status pages/feeds via the regulatory & venue watch + a quarterly AUSTRAC register check (USER task)
- [x] Aligned docs carry it: 12 §2 (Health row, AUSTRAC row, VENUE_CHECK); 13 §6 (Venue health row); roadmap R1.13, T1.06, T1.30; P4 roadmap R4.15
- [x] Affected P1 tasks updated in the 2026-10-22 task alignment: P1-T043, P1-T069 (new USER task, T1.06)

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [x] Docs updated and consistent (12 §2 (Health row, AUSTRAC row, VENUE_CHECK); 13 §6 (Venue health row); roadmap R1.13, T1.06, T1.30; P4 roadmap R4.15)
- [x] Decision and owning tasks noted in the progress log

## Exceptions & edge cases

- Until fixed, related tasks follow the interim rule stated in their own files

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a number in code; the decision lands in the docs first
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/12-policy-and-compliance.md`: apply the fix above
- `docs/13-wallets-treasury-and-onchain.md`: apply the fix above

## Branch & PR

- Branch: `p1/P1-B014-venue-health-sources-undefined`
- PR title: `P1-B014: Venue-health inputs (withdrawal delays, PoR, AUSTRAC) have no defined free sources`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-B014` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D P1-B014; docs carry it (12 §2 (Health row, AUSTRAC row, VENUE_CHECK); 13 §6 (Venue health row); roadmap R1.13, T1.06, T1.30; P4 roadmap R4.15); implementation owned by P1-T043, P1-T069 (new USER task, T1.06)
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P1-B014); docs updated: 12 §2 (Health row, AUSTRAC row, VENUE_CHECK); 13 §6 (Venue health row); roadmap R1.13, T1.06, T1.30; P4 roadmap R4.15; implementation owned by P1-T043, P1-T069 (new USER task, T1.06)
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
