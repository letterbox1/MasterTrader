---
id: P3-B009
kind: gap
title: Column-encryption key rotation conflicts with WORM (re-encrypt needs UPDATE)
phase: 3
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R3.N1]
roadmap_todos: []
modules: [M18]
dashboards: []
branch: p3/P3-B009-column-key-rotation-vs-worm
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: docs/07-security-notes.md §8 and §2 (rotation)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-B009 · Column-encryption key rotation conflicts with WORM (re-encrypt needs UPDATE)

## Goal / expected outcome

A documented rotation model for pgcrypto column keys that never updates WORM rows.

## Context & references

- [07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit) (pgcrypto) · [07 §2](../../../docs/07-security-notes.md#2-secrets) (rotation) · [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) (no UPDATE)
- Affects: P3-T006, P3-T007

## Requirements

- **Steps to reproduce:** Rotate the column key on a WORM table.
- **Expected:** Versioned keys (`key_id` per row); new rows use the new key; old keys retained read-only.
- **Actual:** Unspecified; a naive rotation re-encrypts rows (UPDATE) and breaks WORM/hash chains.
- **Impact:** Either WORM violation or unrotatable keys. (severity S3)
- **Suggested fix:** Add the key-id versioning model to 07 §8.

## ToDo

- [ ] Update 07 §8
- [ ] Update the affected task files (P3-T006, P3-T007) if the decision differs from their default
- [ ] Note the decision and source in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T006, when they read the linked doc, then the rule is unambiguous.

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

- `docs/07-security-notes.md`: record the decision.
- `docs/roadmap/phase-3-journal-and-tax.md`: no ToDo box to tick; note the outcome under §7 Risks if it changes a risk or open question.

## Branch & PR

- Branch: `p3/P3-B009-column-key-rotation-vs-worm`
- PR title: `P3-B009: Column-encryption key rotation conflicts with WORM (re-encrypt needs UPDATE)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-B009` run

## Progress log

- 2026-10-21 00:00 · planner · opened
