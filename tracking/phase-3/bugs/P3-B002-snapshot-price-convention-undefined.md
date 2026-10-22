---
id: P3-B002
kind: gap
title: 30 June 2027 snapshot price convention undefined per asset class
phase: 3
type: DOC
status: done
priority: high
size: XS
severity: S2
owner: agent
claimed_by: ""
depends_on: []
requirements: [R3.08]
roadmap_todos: []
modules: [M18]
dashboards: []
branch: p3/P3-B002-snapshot-price-convention-undefined
pr: ""
doc_sync: [docs/09-journal-and-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: done
found_in: docs/09-journal-and-tax.md §Key findings (2027 reform)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P3-B002 · 30 June 2027 snapshot price convention undefined per asset class

## Goal / expected outcome

The snapshot job values each asset class with an agreed convention (which price, which venue, which time) confirmed by the tax agent.

## Context & references

- [09 key findings](../../../docs/09-journal-and-tax.md#️-key-findings-that-shape-the-design): "end of day AEST, price source recorded"; mechanism (U)
- P3-T002 asks the agent question (d)
- Affects: P3-T030, P3-T002, P3-T048

## Requirements

- **Steps to reproduce:** Value a US ETF, a crypto token and a USD cash balance "at end of day AEST 30 June 2027".
- **Expected:** Documented rule per class (crypto: last 1m close ≤ 23:59:59 AEST on preferred venue; US equities: 29 June NY close; AU equities: 30 June close; FX: RBA F11 30 June; illiquid: manual valuation with evidence).
- **Actual:** Only "end of day AEST"; US markets close at 06:00 AEST the next morning, so "end of day" is ambiguous; no rule for illiquid tokens.
- **Impact:** Hard-date job could record values the agent later rejects; WORM means re-valuation needs superseding rows and evidence. (severity S2)
- **Suggested fix:** Adopt P3-T030's default rule in 09 now, flag (U), and confirm with the agent via P3-T002 before 2027-06-01.

## ToDo

- [x] Decision recorded in docs/17 (17 §A P3-B002): snapshot price convention per asset class (crypto VWAP 23:55:00–23:59:59 AEST on the primary venue; ASX official close; US/EU last trade ≤ 23:59:59 AEST else previous close; FX RBA rate, last business day), recorded with source and method; tax agent confirms via 09 Q10 (P3-T001/P3-T002)
- [x] Owning docs carry it: 16 §4.2; 09 market-value snapshots; roadmap R3.08
- [x] Affected tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P3-T030 (snapshot job), P3-T011 (`snapshot_price`), P3-T048 (dry run)
- [x] Decision and source noted in the progress log

## Verification

### Tests

- Doc/consistency check: the decision appears once, in the owning doc, and the affected tasks reference it.

### Scenarios

- Given a developer picks up P3-T030, when they read the linked doc, then the rule is unambiguous.

### Stress / failure injection

- n/a: documentation/spec gap

## Acceptance criteria

- [x] Decision recorded in the owning doc (16 §4.2; 09 market-value snapshots; roadmap R3.08)
- [x] Affected tasks consistent with it (P3-T030 (snapshot job), P3-T011 (`snapshot_price`), P3-T048 (dry run))
- [x] Root cause noted in the progress log

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

- Branch: `p3/P3-B002-snapshot-price-convention-undefined`
- PR title: `P3-B002: 30 June 2027 snapshot price convention undefined per asset class`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-B002` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by docs/17 §A P3-B002: snapshot price convention per asset class (crypto VWAP 23:55:00–23:59:59 AEST on the primary venue; ASX official close; US/EU last trade ≤ 23:59:59 AEST else previous close; FX RBA rate, last business day), recorded with source and method; tax agent confirms via 09 Q10 (P3-T001/P3-T002). Docs now carry it: 16 §4.2; 09 market-value snapshots; roadmap R3.08. Implementation owned by P3-T030 (snapshot job), P3-T011 (`snapshot_price`), P3-T048 (dry run). Root cause: 09 said 'end of day AEST' without a per-asset-class price rule.
- 2026-10-22 02:02 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §A P3-B002); docs updated: 16 §4.2; 09 market-value snapshots; roadmap R3.08; implementation owned by P3-T030 (snapshot job), P3-T011 (`snapshot_price`), P3-T048 (dry run)
- 2026-10-22 02:02 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:02 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
