---
id: P2-T051
kind: task
title: Risk golden and property test suite as a mandatory merge gate
phase: 2
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T017, P2-T018, P2-T069]
requirements: [R2.N2, R2.10, R2.12, R2.13, R2.14]
roadmap_todos: [T2.60]
modules: [M11]
dashboards: []
tools: [uv]
mcp: []
env: []
services: []
branch: p2/P2-T051-verify-risk-golden-property
pr: ""
doc_sync: [docs/04-plan-of-action.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T051 · Risk golden and property test suite as a mandatory merge gate

## Goal / expected outcome

A consolidated `tests/golden/risk/` suite (sizing, limits, sleeves/netting, ladder, gate decisions) plus hypothesis property tests runs in CI as a required status check, so no PR merges if any risk golden or property fails.

## Context & references

- Roadmap: [R2.N2, R2.10](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.60
- Standing rule: [04 risk golden tests mandatory](../../../docs/04-plan-of-action.md#standing-rules)
- Inputs: goldens from P2-T011–T018 and P2-T069 (layer merge); the safety-state goldens (data age, `audit.integrity`, egress) are P2-T076 (T2.71) and join the same required CI job.
- Defaults under test come from [16 §2](../../../docs/16-configuration-and-safety-model.md#2-default-values-all-configurable) (e.g. two-stage drawdowns 10/15 sleeve, 10/25 system; venue cap 25%).

## Requirements

- Golden files are YAML cases `{state, intent, expected: {decision, reasons, size}}`; ≥ 300 cases spanning every rule at below/at/above threshold.
- Golden coverage includes: sleeve drawdown stage 1 (sizes halved) vs stage 2 (halt), system stage 1 (no new entries, exits pass) vs stage 2 (flatten + lock), daily loss on the Sydney day boundary, venue concentration 25%, price collar per asset class, cost blow-out pausing only the bot, L0 clamp.
- Properties: (1) any exception → reject; (2) post-trade exposure never exceeds caps; (3) Kelly used ≤ ¼ f; (4) protective exits never increase exposure; (5) kill ON → no approve decisions; (6) stale/bad DQ → no new entries; (7) the effective limit is always the strictest across L0–L4 (16 §1); (8) drawdown stage 1 < stage 2 for every saved policy.
- CI job `risk-golden` required in branch protection; golden updates need a reviewer note in the PR (changed expected values listed).

## ToDo

- [ ] Consolidate goldens + add missing cases
- [ ] Hypothesis strategies for states/intents
- [ ] CI job + branch protection rule
- [ ] Golden diff report script
- [ ] Record results (numbers, run IDs, screenshots) in the progress log and tick the roadmap ToDo box

## Verification

### Tests
- The suite itself; plus a mutation-testing run (mutmut on `mt_risk/limits` and `gate`) with ≥ 80% mutants killed, recorded.

### Scenarios
- Given a PR that changes the daily-loss evaluator to `>=` instead of `>`, when CI runs, then the golden suite fails and merge is blocked.

### Stress / failure injection
- Hypothesis with 50k examples nightly (5k in PR CI).

## Acceptance criteria

- [ ] ≥ 300 golden cases, 8 properties green
- [ ] Required status check enabled
- [ ] Mutation score recorded ≥ 80%

## Exceptions & edge cases

- Flaky property found: fix the code or the generator, never mark xfail.

## Cardinal rules (do NOT)

- Do NOT update golden expected values without a PR note explaining why.
- Do NOT mark risk tests skip/xfail.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/04-plan-of-action.md` standing rules: name the CI job.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.60 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T051-verify-risk-golden-property`
- PR title: `P2-T051: Risk golden and property test suite as a mandatory merge gate`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T051` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (goldens for two-stage drawdowns, layering strictest-wins and 16 defaults; safety-state goldens joined from P2-T076)
