---
id: P3-B003
kind: gap
title: Wallet registry table named differently across docs and owned by two phases
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
branch: p3/P3-B003-wallet-registry-table-naming-ownership
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/13-wallets-treasury-and-onchain.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: done
found_in: docs/02-v1-architecture.md §4 (M22 row)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P3-B003 · Wallet registry table named differently across docs and owned by two phases

## Goal / expected outcome

One registry table name and one owning phase/module, referenced consistently by 02, 13, P3 and P5.

## Context & references

- [02 §4](../../../docs/02-v1-architecture.md#4-logical-components): M22 owns `treasury.wallet`
- [13 §3](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view) and P5 R5.05: `ops.wallets`
- P3 R3.04 builds the "account/wallet registry" first
- Affects: P3-T012, P3-T018

## Requirements

- **Steps to reproduce:** Search the docs for the wallet registry table.
- **Expected:** Single name (`ops.wallets`) created in P3 (R3.04) and extended in P5 (R5.05); M22 `treasury.*` references it.
- **Actual:** `treasury.wallet` vs `ops.wallets`; ownership ambiguous between P3 and P5.
- **Impact:** Duplicate tables or migrations colliding between phases. (severity S3)
- **Suggested fix:** Use `ops.wallets` (P3-T012 creates it); change 02 §4 M22 row to reference it; P5 extends columns additively.

## ToDo

- [x] Decision recorded in docs/17 (17 §B (P3-B003, P5-B015, P6-B005)): one registry `ops.wallets` (accounts and on-chain addresses), created in P3, extended additively by the P5 wallet-indexer; no `treasury.wallet`
- [x] Owning docs carry it: 02 §4 (one wallet registry note, M18/M22 rows); 02 §5 `ops` schema; 03 §4 `ops`; 09 goals §6; 13 §3
- [x] Affected tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P3-T012 (registry), P3-T056 (Accounts page)
- [x] Decision and source noted in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T012, when they read the linked doc, then the rule is unambiguous.

### Stress / failure injection

- n/a: documentation/spec gap

## Acceptance criteria

- [x] Decision recorded in the owning doc (02 §4 (one wallet registry note, M18/M22 rows); 02 §5 `ops` schema; 03 §4 `ops`; 09 goals §6; 13 §3)
- [x] Affected tasks consistent with it (P3-T012 (registry), P3-T056 (Accounts page))
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
- `docs/13-wallets-treasury-and-onchain.md`: record the decision.
- `docs/roadmap/phase-3-journal-and-tax.md`: no ToDo box to tick; note the outcome under §7 Risks if it changes a risk or open question.

## Branch & PR

- Branch: `p3/P3-B003-wallet-registry-table-naming-ownership`
- PR title: `P3-B003: Wallet registry table named differently across docs and owned by two phases`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-B003` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by docs/17 §B (P3-B003, P5-B015, P6-B005): one registry `ops.wallets` (accounts and on-chain addresses), created in P3, extended additively by the P5 wallet-indexer; no `treasury.wallet`. Docs now carry it: 02 §4 (one wallet registry note, M18/M22 rows); 02 §5 `ops` schema; 03 §4 `ops`; 09 goals §6; 13 §3. Implementation owned by P3-T012 (registry), P3-T056 (Accounts page). Root cause: 13 and 02 named different tables and owners for the registry.
- 2026-10-22 02:02 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B (P3-B003, P5-B015, P6-B005)); docs updated: 02 §4 (one wallet registry note, M18/M22 rows); 02 §5 `ops` schema; 03 §4 `ops`; 09 goals §6; 13 §3; implementation owned by P3-T012 (registry), P3-T056 (Accounts page)
- 2026-10-22 02:02 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:02 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
