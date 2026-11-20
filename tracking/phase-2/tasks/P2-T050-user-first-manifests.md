---
id: P2-T050
kind: task
title: Draft the first strategy manifests for the P1 candidates
phase: 2
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T004, P2-T005, P2-T008]
requirements: [R2.04]
roadmap_todos: [T2.05]
modules: [M0]
dashboards: [D03]
tools: [git, cargo]
mcp: []
env: []
services: []
branch: p2/P2-T050-draft-first-manifests
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-T050 · Draft the first strategy manifests for the P1 candidates

## Goal / expected outcome

Manifests exist under `strategies/` for the P1 candidates (trend on majors, and funding carry as paper-only research while perps are blocked), drafted by the agent from 14 §1/§3/§7: counterparty sentence, measurable kill criteria, benchmark, universe, timeframe, sleeve and `proposed_mode: paper`. They pass `mt strategy validate` and paper trading can start on them. You review them once in the go-live pack (P7-T070) and can edit them any time in the D03 builder.

## Context & references

- Roadmap: [R2.04](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.05
- Spec: [14 §3 counterparty rule + P1 rows](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) · [14 §7 kill criteria](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) · [14 §1 benchmark rule](../../../docs/14-strategy-evidence-and-validation.md#1-viability-verdict-set-expectations-before-building) · [16 §2.6](../../../docs/16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each)
- Templates: P2-T008/T009; builder P2-T144. Decisions: [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19).
- Unblocks: backtests/validation (P2-T114, P2-T166) and the paper clock (P2-T067).

## Requirements

- `strategies/trend_majors/manifest.yaml`: universe BTC/ETH/SOL (FX majors, gold and indices listed as optional, off), daily and 4h, volatility target, sleeve `trend_majors`, counterparty from 14 §3 ("under- and over-reacting speculators and hedgers who pay for trend"), kill criteria from 14 §7 (live Sharpe after 60 trades below the backtest 5th percentile; drawdown > 1.5× the backtest maximum), benchmark from 14 §1 (buy-and-hold BTC + stablecoin yield).
- `strategies/funding_carry/manifest.yaml`: same structure, `paper_ok` products only (12 §2), marked paper-only research until a venue allows the products.
- Risk values in the manifests are proposals at or below the seeded policy (P2-T048); kill criteria written before any paper run.
- Each manifest carries `drafted_by: agent` and `approved: false` until the go-live pack approval (P7-T070) flips it; live modes refuse unapproved manifests.

## ToDo

- [ ] Generate both manifests from the templates with the 14 values
- [ ] `mt strategy validate strategies/*/manifest.yaml` passes
- [ ] Add `approved` handling to validation and to the live-mode preflight (P7-T011 check)
- [ ] Commit; progress log; `./kanban done P2-T050`

## Verification

### Tests
- Validation passes for both; a manifest without kill criteria fails; a live-mode switch with `approved: false` is refused.

### Scenarios
- Given the drafted trend manifest, when the paper clock starts (P2-T067), then it runs in paper with no approval needed.

### Stress / failure injection
- n/a: authoring.

## Acceptance criteria

- [ ] Trend manifest valid and committed
- [ ] Carry manifest committed as paper-only research, or deferred with the reason
- [ ] Unapproved manifests can't go live

## Exceptions & edge cases

- If no venue allows perps, the carry manifest stays paper-only research (`paper_ok` products) and says so.

## Cardinal rules (do NOT)

- Values come from 14/16 defaults; nothing invented. No secrets in manifests.

## Doc sync on completion

- docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md: update to match what was built.

## Branch & PR

- Branch: `p2/P2-T050-draft-first-manifests`
- PR title: `P2-T050: Draft the first strategy manifests for the P1 candidates`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T050` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (manifest risk values are proposals (16 §1), paper_ok carry, links to lab tasks)

- 2026-11-19: Converted from a USER task to an agent task (17 §G): configurable values are seeded from the 16/14 defaults and approved once in the go-live pack (P7-T070), never asked during the build.
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (manifests are YAML validated by the Rust `mt strategy validate` CLI; no Python needed; tools [git, cargo, uv] → [git, cargo])
