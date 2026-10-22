---
id: P3-T045
kind: task
title: ATO golden-file tests and mandatory tax-golden CI gate
phase: 3
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T011, P3-T023, P3-T024, P3-T025, P3-T026, P3-T027, P0-T015]
requirements: [R3.06, R3.N2, R3.15]
roadmap_todos: [T3.60]
modules: [M18]
dashboards: []
tools: [git, uv, gh]
mcp: []
env: []
services: []
branch: p3/P3-T045-verify-ato-golden-tests-ci-gate
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

# P3-T045 · ATO golden-file tests and mandatory tax-golden CI gate

## Goal / expected outcome

A curated golden suite of ATO-style worked examples (discount boundary, loss ordering, crypto↔crypto, staking income cost base, CFD revenue, Div 775, PAYG basis, dual regime) runs in CI as a required check, so no change merges if any tax golden test fails.

## Context & references

- Roadmap: [R3.06, R3.N2, T3.60](../../../docs/roadmap/phase-3-journal-and-tax.md) · standing rule [04 standing rules](../../../docs/04-plan-of-action.md#standing-rules) (tax golden tests mandatory)
- [09 quality](../../../docs/09-journal-and-tax.md#quality) (golden files from ATO worked examples) · [D15 acceptance 3](../../../docs/ui/dashboards/D15-tax.md) (rule-check panel) · valuation hierarchy [16 §4.1](../../../docs/16-configuration-and-safety-model.md#41-valuing-crypto-for-the-journal) (R3.15 is verified by golden tests) · wash-sale default [16 §4.4](../../../docs/16-configuration-and-safety-model.md#44-tax-flags)
- Cross-phase prerequisite (depends_on): P0-T015 (CI pipeline, required checks)

## Requirements

- Golden cases in `tests/golden/au_2026/*.yaml` (input events + expected outputs), each with a `source` field citing the ATO page/example used (URL + retrieval date) or `synthetic` with derivation.
- Minimum set: (1) bought 2 Feb 2018 → eligible from 3 Feb 2019, not on 2 Feb 2019; (2) leap-year boundary; (3) loss ordering non-discount first; (4) carry-forward; (5) brokerage in cost base; (6) crypto↔crypto; (7) staking/established airdrop income cost base; (8) initial-allocation $0 cost base; (9) CFD revenue + financing; (10) Div 775 FX-cash realisation; (11) PAYG excludes capital gains; (12) trader regime removes the discount for trading-tagged lots; (13) FY boundary at 30 June/1 July local; (14) wash-sale flag at 30 days either side (flag only, loss unchanged) and not at 31; (15) valuation hierarchy: fill price for a trade, AUD-venue VWAP for a staking reward, USD VWAP × RBA when no AUD trades, pool price for a long-tail token; (16) PAYG both ATO methods side by side.
- CI job `tax-golden` is a required status check on `main` (branch protection) and runs on every PR touching `packages/mt_journal/**`, `config/journal/**` or `tests/golden/**`.
- Golden files change only with a reviewer note explaining the rule change and a rule-version bump.

## ToDo

- [ ] Write the golden cases + runner `tests/golden/test_au_golden.py`
- [ ] Add CI job and mark it required (document the branch-protection step for you to click if the token lacks admin)
- [ ] Expose case (1) result to `/tax/summary` rule-check field for D15
- [ ] Docs

## Verification

### Tests

- The suite itself; plus a mutation check: deliberately switching to a 365-day test makes cases 1–2 fail (run once, record in progress log).

### Scenarios

- Given a PR that changes discount logic, when CI runs, then `tax-golden` must pass before merge.
- Given a golden expected value is edited without a rule-version bump, when CI runs, then a guard test fails.

### Stress / failure injection

- n/a: correctness suite

## Acceptance criteria

- [ ] ≥ 16 golden cases pass
- [ ] `tax-golden` is a required check
- [ ] Mutation check recorded
- [ ] Rule-check panel fed

## Exceptions & edge cases

- ATO example pages change → keep the retrieval date and archived numbers in the YAML; never fetch at test time.

## Cardinal rules (do NOT)

- Do NOT mark the CI job optional or skip it for "docs-only" PRs touching journal code.
- Do NOT fetch ATO pages during tests.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."

## Doc sync on completion

- `docs/09-journal-and-tax.md` §Quality: list the golden cases.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.60 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T045-verify-ato-golden-tests-ci-gate`
- PR title: `P3-T045: ATO golden-file tests and mandatory tax-golden CI gate`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T045` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (added golden cases for wash-sale 30 days (16 §4.4), valuation hierarchy (R3.15, 16 §4.1) and PAYG both methods (P3-B005); explicit P0-T015 depends_on; tools filled)
