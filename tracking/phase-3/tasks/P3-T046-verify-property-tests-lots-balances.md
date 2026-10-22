---
id: P3-T046
kind: task
title: Property tests for lot conservation, matching and balances
phase: 3
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T018, P3-T019, P3-T020, P3-T034]
requirements: [R3.05, R3.11]
roadmap_todos: [T3.61]
modules: [M18]
dashboards: []
tools: [git, uv]
mcp: []
env: []
services: []
branch: p3/P3-T046-verify-property-tests-lots-balances
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T046 · Property tests for lot conservation, matching and balances

## Goal / expected outcome

Hypothesis property suites prove, over random event streams: lots are conserved, matched quantity equals disposed quantity, internal transfers never create disposals, and journal balances equal (simulated) venue balances.

## Context & references

- Roadmap: [R3.05, R3.11, T3.61](../../../docs/roadmap/phase-3-journal-and-tax.md) · [09 quality property tests](../../../docs/09-journal-and-tax.md#quality)

## Requirements

- Generators: random multi-asset, multi-account event streams (buys, sells, swaps, transfers with fees, income, FX conversions, corrections, splits) with Decimal quantities at instrument precision.
- Properties: (P1) Σ open lot qty per asset = Σ acquisitions − Σ disposals (exact); (P2) per disposal Σ match qty = disposed qty; (P3) own-account transfers → 0 disposals, total qty per asset unchanged; (P4) journal-derived balances = simulated venue ledger balances each day; (P5) recomputation after a correction is deterministic (same result hash); (P6) FX lots: Σ FX lot balances = cash balances per currency.
- ≥ 500 examples per property in CI (`--hypothesis-profile ci`), 10,000 in a nightly job; failing seeds saved to `tests/journal/regressions/`.

## ToDo

- [ ] Write strategies/generators in `tests/journal/strategies.py`
- [ ] Write property tests
- [ ] Nightly CI job
- [ ] Docs

## Verification

### Tests

- The properties above.

### Scenarios

- Given a shrunk failing example, when saved, then it becomes a permanent regression test.

### Stress / failure injection

- Nightly 10k examples per property within 30 min.

## Acceptance criteria

- [ ] All six properties pass in CI and nightly
- [ ] Regression seeds directory in place

## Exceptions & edge cases

- Precision edge cases (1 satoshi, 1e-18 ETH) included in generators.

## Cardinal rules (do NOT)

- Do NOT reduce example counts to get green.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.61 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T046-verify-property-tests-lots-balances`
- PR title: `P3-T046: Property tests for lot conservation, matching and balances`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T046` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (no decision changes; tools filled)
