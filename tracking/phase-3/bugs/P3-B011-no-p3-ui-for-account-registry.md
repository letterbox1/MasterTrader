---
id: P3-B011
kind: gap
title: No P3 UI surface for registering and tagging accounts
phase: 3
type: DOC
status: done
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
doc_sync: [docs/ui/dashboards/D16-system.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: done
found_in: docs/roadmap/phase-3-journal-and-tax.md §4 (T3.04)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
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

- [x] Decision recorded in docs/17 (17 §D P3-B011/P3-B012): P3 adds a minimal Accounts page in D16 settings (`wallet.register`/`wallet.tag` C1, or a seed file through `mt_api`)
- [x] Owning docs carry it: D16 Settings → Accounts (Phase 3) + backend contract; 09 goals §6; 04 Phase 3 checklist; roadmap R3.17/T3.33
- [x] Affected tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P3-T056 (Accounts page), P3-T042 (your registration), P3-T012
- [x] Decision and source noted in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T012, when they read the linked doc, then the rule is unambiguous.

### Stress / failure injection

- n/a: documentation/spec gap

## Acceptance criteria

- [x] Decision recorded in the owning doc (D16 Settings → Accounts (Phase 3) + backend contract; 09 goals §6; 04 Phase 3 checklist; roadmap R3.17/T3.33)
- [x] Affected tasks consistent with it (P3-T056 (Accounts page), P3-T042 (your registration), P3-T012)
- [x] Root cause noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by docs/17 §D P3-B011/P3-B012: P3 adds a minimal Accounts page in D16 settings (`wallet.register`/`wallet.tag` C1, or a seed file through `mt_api`). Docs now carry it: D16 Settings → Accounts (Phase 3) + backend contract; 09 goals §6; 04 Phase 3 checklist; roadmap R3.17/T3.33. Implementation owned by P3-T056 (Accounts page), P3-T042 (your registration), P3-T012. Root cause: the USER registration task had no UI in P3.
- 2026-10-22 02:02 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P3-B011/P3-B012); docs updated: D16 Settings → Accounts (Phase 3) + backend contract; 09 goals §6; 04 Phase 3 checklist; roadmap R3.17/T3.33; implementation owned by P3-T056 (Accounts page), P3-T042 (your registration), P3-T012
- 2026-10-22 02:02 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:03 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
