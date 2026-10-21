---
id: P3-B010
kind: gap
title: CARF reconciliation has no defined venue-reported input
phase: 3
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R3.10]
roadmap_todos: []
modules: [M18]
dashboards: []
branch: p3/P3-B010-carf-input-format-undefined
pr: ""
doc_sync: [docs/09-journal-and-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: docs/09-journal-and-tax.md §Cross-border events (CARF / CRS 2.0)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-B010 · CARF reconciliation has no defined venue-reported input

## Goal / expected outcome

09 names the input (venue annual tax statements CSV, later CARF reports) and the comparison metrics.

## Context & references

- [09 CARF](../../../docs/09-journal-and-tax.md#jurisdiction-plugin-interface) · R3.10
- Affects: P3-T037

## Requirements

- **Steps to reproduce:** Build the CARF reconciliation from 09.
- **Expected:** Input source + metrics defined.
- **Actual:** "reconciles your journal against the venue's reported totals" only.
- **Impact:** Scaffold may not fit real data when AU CARF starts (2027/28 (U)). (severity S3)
- **Suggested fix:** Adopt P3-T037's generic importer + metrics; revisit when the first venue report arrives.

## ToDo

- [ ] Add input/metrics to 09
- [ ] Update the affected task files (P3-T037) if the decision differs from their default
- [ ] Note the decision and source in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T037, when they read the linked doc, then the rule is unambiguous.

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

- `docs/09-journal-and-tax.md`: record the decision.
- `docs/roadmap/phase-3-journal-and-tax.md`: no ToDo box to tick; note the outcome under §7 Risks if it changes a risk or open question.

## Branch & PR

- Branch: `p3/P3-B010-carf-input-format-undefined`
- PR title: `P3-B010: CARF reconciliation has no defined venue-reported input`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-B010` run

## Progress log

- 2026-10-21 00:00 · planner · opened
