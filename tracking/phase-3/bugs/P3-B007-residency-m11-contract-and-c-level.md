---
id: P3-B007
kind: gap
title: Residency-to-risk contract undefined and residency changes can loosen risk at C1
phase: 3
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R3.09]
roadmap_todos: []
modules: [M18]
dashboards: []
branch: p3/P3-B007-residency-m11-contract-and-c-level
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/dashboards/D15-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: docs/09-journal-and-tax.md §Key findings (Egypt)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-B007 · Residency-to-risk contract undefined and residency changes can loosen risk at C1

## Goal / expected outcome

A defined interface by which M11 learns the current residency flags, and a C3 requirement when a residency change removes a block.

## Context & references

- [09 key findings: Egypt](../../../docs/09-journal-and-tax.md#️-key-findings-that-shape-the-design) · [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) · [D15 actions](../../../docs/ui/dashboards/D15-tax.md): `tax.residency.add` is C1
- [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) has no residency/compliance subject or KV
- Affects: P3-T033, P3-T031, P3-T039

## Requirements

- **Steps to reproduce:** Enter an EG period, then remove it, and check how M11 is told and what confirmation is required.
- **Expected:** KV `compliance_state` (or equivalent) read by M11; removing a block is a loosening → C3.
- **Actual:** No contract; `tax.residency.add` is C1 regardless of direction.
- **Impact:** Egypt crypto block may not reach M11; unblocking bypasses C3. (severity S3)
- **Suggested fix:** Adopt P3-T033's design: KV `compliance_state`, fail-closed, C3 for flag removal; update 02 §6, §7.2 and D15.

## ToDo

- [ ] Update 02 §6 (KV) and §7.2 (C-level note)
- [ ] Update D15 Actions
- [ ] Update the affected task files (P3-T033, P3-T031, P3-T039) if the decision differs from their default
- [ ] Note the decision and source in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T033, when they read the linked doc, then the rule is unambiguous.

### Stress / failure injection

- n/a: documentation/spec gap

## Acceptance criteria

- [ ] Decision recorded in the owning doc
- [ ] Affected tasks consistent with it
- [ ] Root cause noted in the progress log

## Exceptions & edge cases

- Until resolved, the affected tasks use the default stated in their Requirements and label it (U).

## Cardinal rules (do NOT)

- Do NOT resolve by editing WORM data; spec changes apply to new computations (superseding rows).
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."

## Doc sync on completion

- `docs/02-v1-architecture.md`: record the decision.
- `docs/ui/dashboards/D15-tax.md`: record the decision.
- `docs/roadmap/phase-3-journal-and-tax.md`: no ToDo box to tick; note the outcome under §7 Risks if it changes a risk or open question.

## Branch & PR

- Branch: `p3/P3-B007-residency-m11-contract-and-c-level`
- PR title: `P3-B007: Residency-to-risk contract undefined and residency changes can loosen risk at C1`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-B007` run

## Progress log

- 2026-10-21 00:00 · planner · opened
