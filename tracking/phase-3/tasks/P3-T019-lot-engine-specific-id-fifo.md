---
id: P3-T019
kind: task
title: Lot engine with specific-ID matching and FIFO fallback
phase: 3
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T008, P3-T011]
requirements: [R3.05]
roadmap_todos: [T3.23]
modules: [M18]
dashboards: [D15]
tools: [git, uv]
mcp: []
env: []
services: [postgres]
branch: p3/P3-T019-lot-engine-specific-id-fifo
pr: ""
doc_sync: [docs/09-journal-and-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P3-T019 · Lot engine with specific-ID matching and FIFO fallback

## Goal / expected outcome

Every acquisition (trade, income receipt, airdrop, staking reward, FX cash inflow) opens a lot, every disposal is matched to lots by **specific ID** where a valid selection exists and **FIFO** otherwise, with `journal.lot_match` records stating method and reason, all in Decimal, so cost base and holding period are provable per parcel.

## Context & references

- Roadmap: [R3.05, T3.23](../../../docs/roadmap/phase-3-journal-and-tax.md) · [03 M18](../../../docs/03-build-spec.md#m18-trading-journal--tax--mt_journal) · [09 architecture LOT ENGINE](../../../docs/09-journal-and-tax.md#architecture)
- Borrowed ideas: rp2 (Apache) lot-matching plugins + Decimal; isaacrowntree/ledger (MIT) brokerage in cost base — see [09 tools vetted](../../../docs/09-journal-and-tax.md#tools-vetted); vendored code under `third_party/` with pinned commit + licence
- Command `tax.lot.select` (C1) in [D15 actions](../../../docs/ui/dashboards/D15-tax.md)
- Property tests: P3-T046

## Requirements

- `journal.lot`: `lot_id`, asset, account, `acquired_at` (ts + taxpayer-local date), qty, cost base elements (purchase price, incidental costs incl. brokerage, AUD and USD), source event, tax tag at acquisition, flags (`cost_base_estimated`, TAP, pre-2027 snapshot ref, I1 snapshot ref).
- `journal.lot_match`: disposal event → [(lot_id, qty, cost_base_portion)], method `SPECIFIC_ID|FIFO`, reason (`user_selection`, `no_selection`, `selection_invalid`).
- Specific ID: a `tax.lot.select` command before FY close binds a disposal to named lots (C1, audited); valid only if the lots were open at the disposal time with enough qty; otherwise FIFO with reason `selection_invalid`.
- Matching runs per (asset, account-group); internal transfers relocate lots (P3-T018) without matching.
- Lot state is derived (rebuildable): `journal.lot`/`lot_match` rows are WORM; recomputation after a correction writes superseding matches with a `computation_id`.
- Decimal context: 28+ significant digits; quantize only at report output per instrument precision.
- Corporate actions (split/consolidation) produce adjustment rows (new lot rows superseding), preserving acquisition dates.

## ToDo

- [ ] Implement `packages/mt_journal/lots/engine.py`, `methods/fifo.py`, `methods/specific_id.py` (plugin pattern from rp2)
- [ ] Recompute pipeline (incremental on new events; full rebuild command for tests) writing `computation_id`
- [ ] `tax.lot.select` command handler (C1) + validation
- [ ] Vendor/reference rp2 matching code under `third_party/rp2/` with licence and pinned commit if code is copied
- [ ] Unit + golden tests; docs

## Verification

### Tests

- Golden: rp2-style worked example sets (buy 3 parcels, sell across them) → expected matches for FIFO and specific ID.
- Unit: specific ID selecting a lot acquired after the disposal → rejected, FIFO used with reason.
- Unit: brokerage on purchase included in cost base; brokerage on sale reduces proceeds.
- Property hooks for P3-T046 (lots conserved, matched qty = disposed qty).

### Scenarios

- Given 3 BTC lots and a 1.5 BTC sale with no selection, when matched, then FIFO consumes lot 1 fully and 0.5 of lot 2, reason `no_selection`.
- Given you select lot 3 for a sale before FY close, when recomputed, then lot 3 is used and the match records `user_selection` with the command id.
- Given a past event is corrected, when the engine recomputes, then superseding match rows are written and D15 shows the previous computation as superseded.

### Stress / failure injection

- 1M events / 200k lots full rebuild < 10 min on the target host; incremental update per fill < 200 ms p95.

## Acceptance criteria

- [ ] Golden + unit tests pass
- [ ] Every disposal has match rows whose qty sums to the disposed qty
- [ ] Specific-ID selection audited via `audit.command`
- [ ] No float in lot code (lint rule)
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Short sales/derivatives: perps, futures and CFDs are not lot-based CGT assets under the default AU treatment; they're realised P&L events (handled in P3-T020/P3-T024).
- Dust remainders below instrument precision are kept exact (no rounding away).
- FY locked (lodged) via `tax.fy.lock` (C3) → `tax.lot.select` refused with 423 until a C3 unlock (P3-T055; decision [17 §D P3-B006](../../../docs/17-decisions-register.md#d-other-decisions)).

## Cardinal rules (do NOT)

- Do NOT let a user selection change a disposal in a locked FY.
- Do NOT mutate lot rows; write superseding computations.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."

## Doc sync on completion

- `docs/09-journal-and-tax.md`: document match records, `computation_id` and the selection rule.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.23 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T019-lot-engine-specific-id-fifo`
- PR title: `P3-T019: Lot engine with specific-ID matching and FIFO fallback`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T019` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (locked-FY refusal now via `tax.fy.lock` C3 (P3-T055, P3-B006); tools/services filled)
