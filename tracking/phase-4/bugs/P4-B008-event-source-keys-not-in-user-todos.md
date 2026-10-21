---
id: P4-B008
kind: gap
title: FIRMS and ACLED keys (and OpenSanctions licence) not in any USER ToDo
phase: 4
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R4.08]
roadmap_todos: []
modules: [M3]
dashboards: []
branch: p4/P4-B008-event-source-keys-not-in-user-todos
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: docs/roadmap/phase-0-foundations.md T0.10 vs docs/03-build-spec.md M3
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-B008 · FIRMS and ACLED keys (and OpenSanctions licence) not in any USER ToDo

## Goal / expected outcome

Every keyed or licence-bound event source has a USER step: NASA FIRMS `MAP_KEY`, ACLED research account, OpenSanctions non-commercial terms.

## Context & references

- Found in: [phase-0 T0.10](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets) key list (FRED, EIA, Myfxbook, CoinGecko, CryptoRank, Helius, Alchemy, GoPlus, Finnhub, CryptoPanic)
- Needs: [03 M3](../../../docs/03-build-spec.md#m3-global-events--mt_dataevents) (FIRMS, ACLED research account, OpenSanctions)
- Covered in P4 by P4-T005.

## Requirements

- **Steps to reproduce:** compare T0.10 with M3 sources.
- **Expected:** keys/licences listed as USER steps (P0 or P4).
- **Actual:** missing.
- **Impact:** S3 — event ingestion would stall on keys.
- **Suggested fix:** add FIRMS/ACLED to T0.10 or reference P4-T005 in the phase-4 roadmap.

## ToDo

- [ ] Agree the fix with the doc owner (main agent / user)
- [ ] Edit the listed docs (outside this phase folder; done by whoever owns those docs)
- [ ] Re-run `./kanban validate` and link the commit here

## Verification

### Tests
- Doc review: the corrected section is consistent with the linked sources (links resolve).

### Scenarios
- Given ACLED declines access, then UCDP + GDELT cover conflict (P4-T034).

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

- `docs/roadmap/phase-0-foundations.md`: T0.10 key list (or phase-4 §4 A note)

## Branch & PR

- Branch: `p4/P4-B008-event-source-keys-not-in-user-todos`
- PR title: `P4-B008: fix fIRMS and ACLED keys (and OpenSanctions licence) not in any USER ToDo`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-B008` run

## Progress log

- 2026-10-21 00:00 · planner · opened
