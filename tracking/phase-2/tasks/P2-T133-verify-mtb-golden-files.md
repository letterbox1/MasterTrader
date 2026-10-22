---
id: P2-T133
kind: task
title: Verify MasterTradingBot golden files match
phase: 2
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T130, P2-T131, P2-T132, P2-T002]
requirements: [R2.48]
roadmap_todos: [T2.67]
modules: [M0]
dashboards: []
tools: [uv]
mcp: []
env: []
services: []
branch: p2/P2-T133-verify-mtb-golden-files
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T133 · Verify MasterTradingBot golden files match

## Goal / expected outcome

Proof that the shared libraries reproduce MasterTradingBot exactly: every provided golden set (indicator values, signals, trades, position sizes) matches, and the golden suite is a mandatory CI job.

## Context & references

- Roadmap: [R2.48](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.67
- [14 §8](../../../docs/14-strategy-evidence-and-validation.md#8-mastertradingbot-integration) · golden inputs from your USER item P2-T002 (T2.04: rule descriptions + historical signal/trade outputs), a true precondition
- Libraries/template: P2-T130, P2-T131, P2-T132

## Requirements

- Golden sets cover at least: one EMA rule, one scalper trigger, one ATR-stop rule, across ≥ 2 asset classes (e.g. gold and an FX pair) and ≥ 6 months each.
- Match criteria: signals and trade entry/exit timestamps identical; indicator values ≤ 1e-8 abs diff; sizes identical after lot rounding.
- Any mismatch is triaged as library bug vs MT5 convention (documented) — never by loosening tolerance.
- Golden job runs on every PR touching `mt_strategy/lib` and nightly.

## ToDo

- [ ] Import T2.04 outputs into `tests/golden/mtb/` (no secrets/account ids)
- [ ] Run harness; triage mismatches into bug items
- [ ] Make the golden job required in CI
- [ ] Write a short match report in the progress log

## Verification

### Tests
- Golden suite (P2-T130 harness) over all provided sets.

### Scenarios
- Given a deliberate off-by-one in EMA seeding, then the golden job fails (mutation check).
- Given an MT5 broker-time DST shift in the data, then timestamps still match after UTC conversion.

### Stress / failure injection
- n/a: deterministic comparison; runtime < 2 min.

## Acceptance criteria

- [ ] All provided golden sets match
- [ ] Golden job required in CI
- [ ] Mutation check proves the suite catches drift

## Exceptions & edge cases

- Golden files contain broker account numbers: strip before committing.
- If T2.04 data is incomplete, list the uncovered rules as gaps (new bug items) rather than passing.

## Cardinal rules (do NOT)

- Do NOT widen tolerances to make goldens pass.
- Do NOT commit broker account identifiers or credentials with golden files.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §8: golden coverage achieved.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.67 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T133-verify-mtb-golden-files`
- PR title: `P2-T133: Verify MasterTradingBot golden files match`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T133` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (depends on the USER golden inputs (P2-T002))
