---
id: P7-T048
kind: task
title: Simulated kill-criteria breaches halt the right sleeve or everything
phase: 7
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T020, P7-T021, P7-T022, P7-T027]
requirements: [R7.06]
roadmap_todos: [T7.61]
modules: [M11, M16]
dashboards: [D06]
branch: p7/P7-T048-verify-kill-criteria-simulated-breaches
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T048 · Simulated kill-criteria breaches halt the right sleeve or everything

## Goal / expected outcome

Each kill criterion is breached in simulation (paper venues + injected data) and halts exactly the intended scope — one sleeve or the whole system — with alerts, WORM records and correct restart gating (exit criterion 2).

## Context & references

- Roadmap: [R7.06 · ToDo T7.61](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) · Roadmap R7.06 'Verified by: simulated breach' · [14 §5](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) (fallback ladder rung 5–6)
- Related: P7-T020, P7-T021, P7-T022, P7-T027, P7-T064

## Requirements

- Cases: shortfall > 2× (sleeve); 60-trade Sharpe < p5 (sleeve); memecoin ×4 (sleeve); recon unexplained 24 h (all); portfolio DD > 25% (all + flatten + 30-day lock); second DD event (programme ended).
- For each: halt scope correct, other sleeves unaffected (sleeve cases), cancels < 1 s, critical alert on 3 channels, WORM rows present, restart refused without C3/conditions.
- Runs as an automated suite `tests/sim/test_kill_criteria.py` against paper venues with clock and data injection, plus one manual run you observe on the phone.

## ToDo

- [ ] Build the injection harness (fills with chosen shortfall, trade outcomes, recon breaks, equity path).
- [ ] Implement the 10 cases.
- [ ] Run the observed session; record evidence.
- [ ] File bugs for any deviation.

## Verification

### Tests
- Sim suite: 10 cases, each asserting scope, timing, alerts, records, restart gating.

### Scenarios
- Given two live sleeves, when trend breaches shortfall, then carry keeps trading.
- Given portfolio DD 25.2%, then everything flattens to stables and kill OFF is refused until day 30.

### Stress / failure injection
- Run all 10 cases back-to-back 5 times: deterministic results; random venue disconnects during flatten don't leave positions unprotected.

## Acceptance criteria

- [ ] All 10 cases pass in CI.
- [ ] Observed run recorded with evidence.
- [ ] No open S1/S2 bugs from the run.

## Exceptions & edge cases

- Clock injection must not leak into production config (test-only provider).

## Cardinal rules (do NOT)

- Do NOT run breaches on live money.
- Do NOT relax thresholds to make the suite pass.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §7: link the simulation suite.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.61 when this item is done.

## Branch & PR

- Branch: `p7/P7-T048-verify-kill-criteria-simulated-breaches`
- PR title: `P7-T048: Simulated kill-criteria breaches halt the right sleeve or everything`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T048` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
