---
id: P2-T049
kind: task
title: Seed the sleeves and risk budgets from the 14 §3 allocation table
phase: 2
type: BUILD
status: backlog
priority: high
size: XS
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T014, P2-T043]
requirements: [R2.13]
roadmap_todos: [T2.02]
modules: [M11]
dashboards: [D06]
tools: [git, cargo, supabase]
mcp: []
env: []
services: [supabase-postgres, mt-api]
branch: p2/P2-T049-seed-sleeves
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T049 · Seed the sleeves and risk budgets from the 14 §3 allocation table

## Goal / expected outcome

The L3 sleeves exist in the policy, seeded from the [14 §3](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) allocation table plus the `manual` sleeve, each with its risk budget, paper notional capital, limits and kill rules from the 16 §2 defaults, and every P1 candidate strategy assigned to a sleeve. Nothing is asked of you during the build; you approve the sleeves once in the go-live pack (P7-T070) and can edit them in D06 any time.

## Context & references

- Roadmap: [R2.13](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.02
- Spec: [14 §3](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) · [14 §5 sleeves](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) · [16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown) · [16 §2.5](../../../docs/16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot) (paper notional)
- Decisions: sleeves are L3 ([16 §1](../../../docs/16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance), [17 §D P2-B004](../../../docs/17-decisions-register.md#d-other-decisions)); [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19).
- Related: P2-T048 (policy seed), P2-T050 (manifests name these sleeves).

## Requirements

- `config/defaults/sleeves.yaml` from 14 §3: trend on majors (risk budget 40%, capital 30–40%, seeded at the midpoint), funding carry (15%, paper-only while perps are blocked), hold-and-earn (10%, P6; excluded from the drawdown basis), memecoin (25% risk budget, ≤ 5–10% capital, paper-only), unlock/event (10%), `manual`; stable/AUD reserve 30% (midpoint of 20–40%).
- Paper notional capital per sleeve = the paper notional default (16 §2.5) × the sleeve's capital share.
- Per sleeve: daily loss 3%, drawdown stages 10% / 15%, exit rule on halt `flatten`, open positions 10.
- Seeded through `mt-api` with source `seed`; idempotent; never overwrites your edits.

## ToDo

- [ ] Write `config/defaults/sleeves.yaml` and a doc-parse test against 14 §3
- [ ] Extend `mt policy seed` with sleeves; assign each P1 candidate to its sleeve
- [ ] Run it; D06 Sleeves widget shows the seeded sleeves
- [ ] Tests; progress log; `./kanban done P2-T049`

## Verification

### Tests
- Seeded sleeves match the defaults file; capital shares plus reserve sum to 100%; stage 1 < stage 2 for every sleeve.
- A manifest naming an unknown sleeve fails validation (P2-T004).

### Scenarios
- Given a fresh stack, when the seed runs, then D06 lists the six sleeves with their budgets and the reserve.

### Stress / failure injection
- n/a: seed data (covered by P2-T048's transaction test).

## Acceptance criteria

- [ ] Sleeves seeded from 14 §3 with source `seed`
- [ ] Each P1 candidate has a sleeve

## Exceptions & edge cases

- If a sleeve in 14 §3 has no eligible venue yet, it is seeded paused with the reason shown in D06.

## Cardinal rules (do NOT)

- Numbers come from the defaults files, never hard-coded; sleeves are policy rows (WORM).

## Doc sync on completion

- docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md: update to match what was built.

## Branch & PR

- Branch: `p2/P2-T049-seed-sleeves`
- PR title: `P2-T049: Seed the sleeves and risk budgets from the 14 §3 allocation table`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T049` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (sleeves as L3 with two-stage drawdowns and names from policy)

- 2026-11-19: Converted from a USER task to an agent task (17 §G): configurable values are seeded from the 16/14 defaults and approved once in the go-live pack (P7-T070), never asked during the build.
