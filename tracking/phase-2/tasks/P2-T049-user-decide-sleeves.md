---
id: P2-T049
kind: task
title: Decide sleeves and their risk budgets
phase: 2
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P2-T014, P2-T043]
requirements: [R2.13]
roadmap_todos: [T2.02]
modules: [M11]
dashboards: [D06]
tools: []
mcp: []
env: []
services: [mt-web]
branch: p2/P2-T049-user-decide-sleeves
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

# P2-T049 · Decide sleeves and their risk budgets

## Goal / expected outcome

Your sleeves (names, capital, risk budget, limits, kill rules) are set in the policy, starting from the 14 §3 allocation table, plus the `manual` sleeve limits.

## Context & references

- Roadmap: [R2.13](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.02
- Spec: [14 §3 portfolio allocation](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) · [14 §5 sleeves](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11)
- Decisions: sleeves are the **L3** layer and their names come from your policy ([16 §1](../../../docs/16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance), [17 §D P2-B004](../../../docs/17-decisions-register.md#d-other-decisions)); each sleeve has two drawdown stages (defaults 10% halve / 15% halt, [16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)); a halted sleeve restarts with `risk.sleeve.restart` (C3).
- Related: P2-T048, P2-T043 (D06 Policy → Sleeves).

## Requirements

- Suggested start (risk budget / capital share): trend on majors 40% / 30–40%; funding carry 15% / 20–30% (paper-only while perps blocked); hold-and-earn 10% / 20–30% (P6); memecoin 25% / ≤ 5–10% (paper-only); unlock/event 10% / 5–10%; plus `manual`.
- Paper capital figure per sleeve (notional; no real money in P2).
- Per sleeve: daily loss (default 3%), drawdown stages (default 10% / 15%; stage 1 < stage 2), exit rule on halt, open positions (default 10). Hold-and-earn is excluded from the drawdown basis (16 §2.1).
- Keep a 20–40% stable/AUD reserve in the plan (14 §3).

## ToDo

- [ ] Decide the sleeve list and numbers
- [ ] Enter them in D06 Policy → Sleeves (or YAML import)
- [ ] Assign each P1 candidate strategy to a sleeve
- [ ] Record completion in the progress log (no secrets) and run `./kanban done P2-T049`

## Verification

### Tests
- Agent confirms the sleeves appear in D06 Sleeves widget with your numbers.

### Scenarios
- Given the sleeves are set, when a manifest names an unknown sleeve, then validation fails (P2-T004).

### Stress / failure injection
- n/a: decision.

## Acceptance criteria

- [ ] Sleeves defined in policy
- [ ] Each P1 candidate has a sleeve

## Exceptions & edge cases

- Hold-and-earn is P6: define it now with zero paper capital or leave it out until then.

## Cardinal rules (do NOT)

- Do NOT allocate by capital alone; allocate by risk (14 §3).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §3: record the sleeves chosen.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.02 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T049-user-decide-sleeves` (only if a repo change results, e.g. non-secret config or manifests; secrets never go in git)
- PR title: `P2-T049: Decide sleeves and their risk budgets`
- PR checklist: no secrets in diff (gitleaks clean) · task file ticked · `./kanban done P2-T049` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (sleeves as L3 with two-stage drawdowns and names from policy)
