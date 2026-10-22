---
id: P3-B015
kind: gap
title: Journal buffer bound during a Postgres outage is unspecified
phase: 3
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R3.01]
roadmap_todos: []
modules: [M18]
dashboards: []
branch: p3/P3-B015-nats-buffer-bound-postgres-down
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: done
found_in: docs/02-v1-architecture.md §9.3 (Postgres down)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P3-B015 · Journal buffer bound during a Postgres outage is unspecified

## Goal / expected outcome

A stated bound (time and bytes) for buffering journal input in NATS, consistent with stream retention, plus the alert threshold.

## Context & references

- [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes): "journal buffered in NATS (bounded)"
- [02 §5.1](../../../docs/02-v1-architecture.md#51-stores): streams 24h–7d
- Affects: P3-T009, P3-T052

## Requirements

- **Steps to reproduce:** Ask how long Postgres may be down before fills are lost to the journal.
- **Expected:** E.g. `fill.>` stream max-age 7 d, max-bytes sized for 7 d at peak; alert at 50%.
- **Actual:** "bounded" without numbers.
- **Impact:** Possible silent loss of journal input in a long outage (ATO record-keeping). (severity S3)
- **Suggested fix:** Set `fill.>` and `wallet.*.*.transfer` streams to max-age 7 d with discard=new + alert at 50% usage; document in 02 §5.1/§9.3.

## ToDo

- [x] Decision recorded in docs/17 (17 §C P3-B015): Postgres-down write path buffers in NATS JetStream bounded at 1 GB or 24 h (defaults); above 80% new entries stop, exits continue; nothing executes without a record
- [x] Owning docs carry it: 16 §3.3; 02 §5.1 stores; 02 §9.3 degraded modes; 15 §2 write path; D16 Settings failure behaviour; roadmap R3.N3/T3.42/T3.67
- [x] Affected tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P3-T057 (stream, buffer, M11 hook), P3-T060 (drill), P3-T009, P3-T052
- [x] Decision and source noted in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T009, when they read the linked doc, then the rule is unambiguous.

### Stress / failure injection

- n/a: documentation/spec gap

## Acceptance criteria

- [x] Decision recorded in the owning doc (16 §3.3; 02 §5.1 stores; 02 §9.3 degraded modes; 15 §2 write path; D16 Settings failure behaviour; roadmap R3.N3/T3.42/T3.67)
- [x] Affected tasks consistent with it (P3-T057 (stream, buffer, M11 hook), P3-T060 (drill), P3-T009, P3-T052)
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- Until resolved, the affected tasks use the default stated in their Requirements and label it (U).

## Cardinal rules (do NOT)

- Do NOT resolve by editing WORM data; spec changes apply to new computations (superseding rows).
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."

## Doc sync on completion

- `docs/02-v1-architecture.md`: record the decision.
- `docs/roadmap/phase-3-journal-and-tax.md`: no ToDo box to tick; note the outcome under §7 Risks if it changes a risk or open question.

## Branch & PR

- Branch: `p3/P3-B015-nats-buffer-bound-postgres-down`
- PR title: `P3-B015: Journal buffer bound during a Postgres outage is unspecified`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-B015` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by docs/17 §C P3-B015: Postgres-down write path buffers in NATS JetStream bounded at 1 GB or 24 h (defaults); above 80% new entries stop, exits continue; nothing executes without a record. Docs now carry it: 16 §3.3; 02 §5.1 stores; 02 §9.3 degraded modes; 15 §2 write path; D16 Settings failure behaviour; roadmap R3.N3/T3.42/T3.67. Implementation owned by P3-T057 (stream, buffer, M11 hook), P3-T060 (drill), P3-T009, P3-T052. Root cause: no bound existed for the Postgres-down buffer.
- 2026-10-22 02:03 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §C P3-B015); docs updated: 16 §3.3; 02 §5.1 stores; 02 §9.3 degraded modes; 15 §2 write path; D16 Settings failure behaviour; roadmap R3.N3/T3.42/T3.67; implementation owned by P3-T057 (stream, buffer, M11 hook), P3-T060 (drill), P3-T009, P3-T052
- 2026-10-22 02:03 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:03 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
