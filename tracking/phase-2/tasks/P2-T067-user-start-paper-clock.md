---
id: P2-T067
kind: task
title: Start the paper clock automatically for the validated P1 candidates
phase: 2
type: OPS
status: backlog
priority: critical
size: XS
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T050, P2-T063, P2-T048, P2-T049, P2-T114]
requirements: [R2.20]
roadmap_todos: [T2.08]
modules: [M0, M11]
dashboards: [D03]
tools: []
mcp: []
env: []
services: [mt-web]
branch: p2/P2-T067-user-start-paper-clock
pr: ""
doc_sync: [docs/roadmap/phase-7-prove-and-go-live.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-T067 · Start the paper clock automatically for the validated P1 candidates

## Goal / expected outcome

At the end of the phase the agent switches the validated P1 candidates (trend on majors; carry if permitted) to paper through the real policy/risk/execution path, which starts the paper clock (P1 sleeves ≥ 8 weeks; default gate ≥ 8 weeks **and** ≥ 50 trades, [16 §2.4](../../../docs/16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile)) that gates P7 — exit criterion 4. (The RUN item that tracks the clock, T2.80, is P2-T180.)

## Context & references

- Roadmap: ToDo T2.08 · exit criterion 4 · [14 §6 gate 7 paper ≥ 8 weeks](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7)
- P7: [R7.02 paper period](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Requires the validation report for each candidate (strategy at `validated`, P2-T114) and the seeded policy and sleeves (P2-T048, P2-T049). Paper involves no money, so it starts without asking you (`paper.auto_start_on_validation: true`, 16 §2.5); you see it in the daily digest and can stop it with one tap.
- Paper bots run on the sandbox venue with live P1 data (simulated fills through the real risk and execution path), so no venue keys are needed.

## Requirements

- Each candidate strategy version is `validated` (Part B harness) and its manifest has kill criteria.
- Set each strategy's mode ceiling to `paper` (`strategy.set_mode` with source `auto`, allowed only for `paper` when `paper.auto_start_on_validation` is on; live modes always need you) and create and start one `paper`-mode bot per candidate and sleeve on the sandbox venue (no venue keys needed); record the start date. Your own first-bot and Telegram HITL walkthrough (P2-T066) happens later and doesn't hold the clock.
- Nothing in the paper path is simulated around M11: real policy, risk, execution (sandbox venue).

## ToDo

- [ ] Check D03 Gates for each candidate (validated)
- [ ] Set the mode ceiling to paper and start the paper bots
- [ ] Write the start date and strategy versions in this task's progress log and in the RUN item P2-T180
- [ ] Confirm the first paper fills appear
- [ ] Record completion in the progress log (no secrets) and run `./kanban done P2-T067`

## Verification

### Tests
- Agent verifies paper runs exist (`strategy.runs kind=paper`) with start timestamps.

### Scenarios
- Given trend v1 validated, when its paper bot starts, then it trades on the sandbox venue through M11 and the clock starts.

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
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (paper clock via mode ceiling + paper bots on sandbox (no keys), gate profile ≥ 8 weeks and ≥ 50 trades)

- 2026-11-19: Converted from USER to agent (17 §G): paper has no money at stake, so it starts automatically after validation; live modes still need your approval (P7-T070, P7-T058).
- 2026-11-19: No longer waits on P2-T066 (which waits on testnet keys): the agent creates the paper bots itself, so the ≥ 8-week paper clock starts as soon as the candidates validate.
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (stack wording only (`mt-api`); already converted)
