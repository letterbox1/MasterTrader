---
id: P3-B011
kind: gap
title: No P3 UI surface for registering and tagging accounts
phase: 3
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R3.04]
roadmap_todos: []
modules: [M18]
dashboards: []
branch: p3/P3-B011-no-p3-ui-for-account-registry
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: docs/roadmap/phase-3-journal-and-tax.md §4 (T3.04)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-B011 · No P3 UI surface for registering and tagging accounts

## Goal / expected outcome

T3.04 can be done from a supported surface in P3.

## Context & references

- T3.04 needs registration in P3; D18 (Wallets & Treasury) only lands in P5 ([P5](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md))
- Commands `wallet.register`/`wallet.tag` exist in [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write)
- Affects: P3-T012, P3-T042

## Requirements

- **Steps to reproduce:** Try to register an account in the P3 UI.
- **Expected:** A minimal surface (seed file loader via mt_api, or a small D15 Settings sub-panel).
- **Actual:** No screen; only commands.
- **Impact:** User can't easily complete T3.04; risk of direct SQL. (severity S3)
- **Suggested fix:** Use the seed-file loader through `mt_api` (P3-T012) in P3; optionally add an Accounts panel to D15 later; document in the roadmap.

## ToDo

- [ ] Add a note to the P3 roadmap T3.04 line (main agent) or D15 spec
- [ ] Update the affected task files (P3-T012, P3-T042) if the decision differs from their default
- [ ] Note the decision and source in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T012, when they read the linked doc, then the rule is unambiguous.

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

- `docs/roadmap/phase-3-journal-and-tax.md`: record the decision.
- `docs/roadmap/phase-3-journal-and-tax.md`: no ToDo box to tick; note the outcome under §7 Risks if it changes a risk or open question.

## Branch & PR

- Branch: `p3/P3-B011-no-p3-ui-for-account-registry`
- PR title: `P3-B011: No P3 UI surface for registering and tagging accounts`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-B011` run

## Progress log

- 2026-10-21 00:00 · planner · opened
