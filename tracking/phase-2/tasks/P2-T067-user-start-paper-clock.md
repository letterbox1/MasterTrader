---
id: P2-T067
kind: task
title: Start the paper clock for the validated P1 candidates
phase: 2
type: USER
status: backlog
priority: critical
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P2-T050, P2-T066, P2-T063, P2-T048, P2-T049, P2-T045]
requirements: [R2.20]
roadmap_todos: [T2.08]
modules: [M0, M11]
dashboards: [D03]
branch: p2/P2-T067-user-start-paper-clock
pr: ""
doc_sync: [docs/roadmap/phase-7-prove-and-go-live.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T067 · Start the paper clock for the validated P1 candidates

## Goal / expected outcome

At the end of the phase you switch the validated P1 candidates (trend on majors; carry if permitted) to paper through the real policy/risk/execution path, which starts the ≥ 8-week paper clock that gates P7 — exit criterion 4. (The RUN item that tracks the clock, T2.80, is Part B's.)

## Context & references

- Roadmap: ToDo T2.08 · exit criterion 4 · [14 §6 gate 7 paper ≥ 8 weeks](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7)
- P7: [R7.02 paper period](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Requires Part B's validation report for each candidate (strategy at `validated`).

## Requirements

- Each candidate strategy version is `validated` (Part B harness) and its manifest has kill criteria.
- Promote to `paper` (`strategy.promote`, C1) and start paper bots per sleeve; record the start date.
- Nothing in the paper path is simulated around M11: real policy, risk, execution (sandbox/testnet).

## ToDo

- [ ] Check D03 Gates for each candidate (validated)
- [ ] Promote to paper and start the bots
- [ ] Write the start date and strategy versions in this task's progress log and in the Part B RUN item
- [ ] Confirm the first paper fills appear
- [ ] Record completion in the progress log (no secrets) and run `./kanban done P2-T067`

## Verification

### Tests
- Agent verifies paper runs exist (`strategy.runs kind=paper`) with start timestamps.

### Scenarios
- Given trend v1 validated, when promoted to paper, then its bots trade on sandbox/testnet through M11 and the clock starts.

### Stress / failure injection
- n/a.

## Acceptance criteria

- [ ] Paper runs started for all validated P1 candidates
- [ ] Start date recorded

## Exceptions & edge cases

- Carry not permitted by the registry: start it as paper research only or defer (recorded).
- A candidate fails validation: it doesn't start; record why.

## Cardinal rules (do NOT)

- Do NOT bypass validation to start the clock early.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.

## Doc sync on completion

- `docs/roadmap/phase-7-prove-and-go-live.md`: record the paper clock start date (R7.02).
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.08 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T067-user-start-paper-clock` (only if a repo change results, e.g. non-secret config or manifests; secrets never go in git)
- PR title: `P2-T067: Start the paper clock for the validated P1 candidates`
- PR checklist: no secrets in diff (gitleaks clean) · task file ticked · `./kanban done P2-T067` run

## Progress log

- 2026-10-21 00:00 · planner · created
