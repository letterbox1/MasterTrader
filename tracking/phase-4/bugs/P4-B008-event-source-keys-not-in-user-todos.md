---
id: P4-B008
kind: gap
title: FIRMS and ACLED keys (and OpenSanctions licence) not in any USER ToDo
phase: 4
type: DOC
status: done
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
doc_sync_status: done
found_in: docs/roadmap/phase-0-foundations.md T0.10 vs docs/03-build-spec.md M3
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
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

- [x] Decision recorded: FIRMS/ACLED keys + OpenSanctions licence are a USER task (17 §D)
- [x] Docs carry it: roadmap T4.06 (USER) and T4.66 (live check after T0.10, T4.06); 03 M3 'FIRMS/ACLED keys and the OpenSanctions licence are a USER task'
- [x] Implementation owned by P4-T005 (your keys/licence, mapped to T4.06) and P4-T067 (live check, new)

## Verification

### Tests
- Doc review: the corrected section is consistent with the linked sources (links resolve).

### Scenarios
- Given ACLED declines access, then UCDP + GDELT cover conflict (P4-T034).

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Keyed event sources have a USER step (checked in docs/roadmap/phase-4-intel.md T4.06/T4.66 and 03 M3, 2026-10-22)
- [x] Root cause noted: T0.10's key list missed the M3 event sources

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
- 2026-10-22 00:00 · aligner · resolved by 17 §D (P4-B008); docs checked: docs/roadmap/phase-4-intel.md T4.06 + T4.66, 03 M3; implementation owned by P4-T005, P4-T067; root cause: T0.10 key list didn't cover M3 sources
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 §D (P4-B008); docs updated: docs/roadmap/phase-4-intel.md T4.06 + T4.66, 03 M3; implementation owned by P4-T005, P4-T067
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
