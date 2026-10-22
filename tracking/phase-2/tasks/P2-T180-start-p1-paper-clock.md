---
id: P2-T180
kind: task
title: Start the P1-sleeve paper clock
phase: 2
type: RUN
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T114, P2-T161, P2-T143, P2-T150, P2-T067]
requirements: [R2.06]
roadmap_todos: [T2.80]
modules: [M0, M7, M11, M12]
dashboards: [D03, D01]
tools: []
mcp: []
env: []
services: [mt-web]
branch: p2/P2-T180-start-p1-paper-clock
pr: ""
doc_sync: [docs/roadmap/phase-7-prove-and-go-live.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T180 · Start the P1-sleeve paper clock

## Goal / expected outcome

The validated P1 candidates (trend on majors; funding carry only if the venue registry allows perps) are running on paper through the real policy/risk/execution path, with the paper-clock start recorded per sleeve so P7 can check the ≥ 8-week requirement. Completion is checked in Phase 7 (T7.80).

## Context & references

- Roadmap: ToDo T2.80 · [exit criterion 4](../../../docs/roadmap/phase-2-strategies-risk-lab.md#6-exit-criteria-demo) · [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) (paper: all P1 sleeves ≥ 8 weeks) · [14 §6 gate 7](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8)
- [Phase 7 entry](../../../docs/roadmap/phase-7-prove-and-go-live.md) ('≥ 8 weeks of paper for each P1 sleeve … started T2.80'; R7.02/T7.80)
- Prerequisites: your manifests (P2-T050, T2.05) and your switch to paper (P2-T067, T2.08, `depends_on`), M11 policy/sleeves (T2.22), paper engine on the sandbox venue (T2.25; no venue keys needed for paper)
- Gate profile ([16 §2.4](../../../docs/16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile)): paper/HITL period default ≥ 8 weeks **and** ≥ 50 trades; class override for P1 sleeves ≥ 8 weeks; memecoin ≥ 300 trades; low-frequency ≥ 26 weeks.

## Requirements

- Each candidate has a `validated` truth validation report (P2-T114) or an explicitly recorded 'paper from backtested' override with reason (D03 rule) — carry stays paper-only regardless.
- Started as paper-mode bots per sleeve (strategy mode ceiling `paper`); start timestamp recorded as `paper_clock_started_at` on the strategy version (visible in D03 Gates 'paper period elapsed / required').
- Required period shown from the gate profile: ≥ 8 weeks for P1 sleeves (default ≥ 8 weeks and ≥ 50 trades; ≥ 300 trades for memecoin, not in P1).
- Daily health check and decay signals (P2-T034, R2.21: decay → downgrade to HITL; health fail → halt the bot) active on these bots; weekly review (P2-T182) scheduled.
- Parity with backtest monitored (tracking error on D03 Performance).

## ToDo

- [ ] Confirm gates/overrides per candidate in D03
- [ ] Start paper per sleeve; verify orders route through M11 (D05)
- [ ] Record `paper_clock_started_at` and screenshot D03
- [ ] Add a P7 check note referencing T7.80

## Verification

### Tests
- Smoke: first paper orders visible in D05 with M11 decisions and `audit.order` rows.

### Scenarios
- Given carry is not allowed by the venue registry for perps, then only the trend sleeve starts and the carry sleeve is recorded as 'deferred: registry'.
- Given a paper sleeve halts by risk in week 2, then the clock records the interruption; P7 decides whether it restarts.

### Stress / failure injection
- n/a: soak continues into later phases; health checks are part A's.

## Acceptance criteria

- [ ] Every eligible P1 sleeve running on paper behind M11
- [ ] Start timestamps recorded and visible in D03
- [ ] P7 handover note written

## Exceptions & edge cases

- Engine restart: clock continues (not reset) unless the strategy version changes; a new version starts a new clock.

## Cardinal rules (do NOT)

- Do NOT start any sleeve with live keys.
- Do NOT reset the paper clock to hide a halt.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT touch live money; keys are trade-only, IP-locked, withdrawals disabled; live waits for the P7 gates.

## Doc sync on completion

- `docs/roadmap/phase-7-prove-and-go-live.md`: record actual paper-clock start dates per sleeve (entry criterion).
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.80 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T180-start-p1-paper-clock`
- PR title: `P2-T180: Start the P1-sleeve paper clock`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T180` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (paper clock via paper bots (no keys), gate profile period per 16 §2.4, depends on your switch (P2-T067))
