---
id: P4-B002
kind: gap
title: D08 Feed tab lists Telegram as a DocumentCard source
phase: 4
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R4.13, R4.03]
roadmap_todos: []
modules: [M2]
dashboards: [D08]
branch: p4/P4-B002-d08-feed-lists-telegram-documents
pr: ""
doc_sync: [docs/ui/dashboards/D08-intel.md]
doc_sync_status: n/a
found_in: docs/ui/dashboards/D08-intel.md (Tabs & widgets → Feed)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-B002 · D08 Feed tab lists Telegram as a DocumentCard source

## Goal / expected outcome

D08's Feed tab source list excludes Telegram; Telegram appears only as a postures panel, consistent with the 'Additions' section of the same doc.

## Context & references

- Found in: [D08 Feed row](../../../docs/ui/dashboards/D08-intel.md) ('source (RSS / RSS-Bridge / Telegram / Discord / …)')
- Contradicts: [D08 Additions](../../../docs/ui/dashboards/D08-intel.md) (Telegram shown as postures only) · [R4.13](../../../docs/roadmap/phase-4-intel.md#3-requirements)
- Related: P4-T044.

## Requirements

- **Steps to reproduce:** compare D08 'Tabs & widgets → Feed' with 'Additions from the CryptoTrader review'.
- **Expected:** Feed sources: RSS / RSS-Bridge / Discord / Bluesky / Mastodon / Farcaster / GDELT / EDGAR / CB / Finnhub / CryptoPanic; a separate 'Telegram postures' panel; Sources tab may list Telegram channels (status, counts) without text.
- **Actual:** Telegram listed as a DocumentCard source.
- **Impact:** S3 — UI implementer may render Telegram text.
- **Suggested fix:** update the Feed row and add the postures panel to the widget table.

## ToDo

- [ ] Agree the fix with the doc owner (main agent / user)
- [ ] Edit the listed docs (outside this phase folder; done by whoever owns those docs)
- [ ] Re-run `./kanban validate` and link the commit here

## Verification

### Tests
- Doc review: the corrected section is consistent with the linked sources (links resolve).

### Scenarios
- Given D08 is implemented from the Feed row alone, then Telegram text could be shown — P4-T044 follows the Additions section instead.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Docs updated as described under Requirements
- [ ] Root cause noted in the progress log

## Exceptions & edge cases

- None.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/ui/dashboards/D08-intel.md`: Feed row + postures panel

## Branch & PR

- Branch: `p4/P4-B002-d08-feed-lists-telegram-documents`
- PR title: `P4-B002: fix d08 Feed tab lists Telegram as a DocumentCard source`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-B002` run

## Progress log

- 2026-10-21 00:00 · planner · opened
