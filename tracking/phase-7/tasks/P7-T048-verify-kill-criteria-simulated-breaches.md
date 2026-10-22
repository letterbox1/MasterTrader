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
depends_on: [P7-T020, P7-T022, P7-T027]
requirements: [R7.06]
roadmap_todos: [T7.61]
modules: [M11, M16]
dashboards: [D06]
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, nats, mt-api]
branch: p7/P7-T048-verify-kill-criteria-simulated-breaches
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T048 · Simulated kill-criteria breaches halt the right sleeve or everything

## Goal / expected outcome

Each kill criterion is breached in simulation (paper venues + injected data) and halts exactly the intended scope — one sleeve or the whole system — with alerts, WORM records and correct restart gating (exit criterion 2).

## Context & references

- Roadmap: [R7.06 · ToDo T7.61](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) · Roadmap R7.06 'Verified by: simulated breach' · [14 §5](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) (fallback ladder rung 5–6) · [16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown) (system drawdown stages) · [16 §2.5–2.6](../../../docs/16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each) (warning → back one step; halt → starting allocation)
- Related: P7-T020, P7-T022, P7-T027, P7-T064; the memecoin criteria are breached in P7-T021's own simulation suite because they wait on P5 rug labels ([17 §D P7-B011](../../../docs/17-decisions-register.md#d-other-decisions)).

## Requirements

- Cases: shortfall 1.6× (warning → week not clean, allocation back one step); shortfall > 2× (sleeve halt → starting allocation after review); sleeve 60-trade Sharpe < p5 (sleeve halt); recon unexplained 24 h (all); system drawdown stage 1 at 10% (no new entries anywhere, exits continue); stage 2 at 25% (flatten + 30-day lock); second stage-2 event (programme ended).
- For each: halt scope correct, other sleeves unaffected (sleeve cases), cancels < 1 s, critical alert on 3 channels, WORM rows present, restart refused without C3/conditions.
- Runs as an automated suite `tests/sim/test_kill_criteria.py` against paper venues with clock and data injection, plus one manual run you observe on the phone.

## ToDo

- [ ] Build the injection harness (fills with chosen shortfall, trade outcomes, recon breaks, equity path).
- [ ] Implement the 7 cases.
- [ ] Run the observed session; record evidence.
- [ ] File bugs for any deviation.

## Verification

### Tests
- Sim suite: 7 cases, each asserting scope, timing, alerts, records, capital step-down and restart gating.

### Scenarios
- Given two live sleeves, when trend breaches shortfall, then carry keeps trading.
- Given system drawdown 25.2%, then everything flattens to stables/AUD and kill OFF is refused until day 30.
- Given system drawdown 10.3%, then new entries are rejected everywhere while stops and exits still execute.

### Stress / failure injection
- Run all 7 cases back-to-back 5 times: deterministic results; random venue disconnects during flatten don't leave positions unprotected.

## Acceptance criteria

- [ ] All 7 cases pass in CI.
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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (cases per the 16 §2.1 two-stage system drawdown and 16 §2.5 step-down; memecoin cases moved to P7-T021 (P5 dep))
