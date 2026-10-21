---
id: P2-T050
kind: task
title: Write your first strategy manifests for the P1 candidates
phase: 2
type: USER
status: backlog
priority: high
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P2-T004, P2-T005, P2-T008]
requirements: [R2.04]
roadmap_todos: [T2.05]
modules: [M0]
dashboards: [D03]
branch: p2/P2-T050-user-first-manifests
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T050 · Write your first strategy manifests for the P1 candidates

## Goal / expected outcome

Manifests exist under `strategies/` for the P1 candidates — trend on majors and, if venue access permits, funding carry — each with your own counterparty sentence, kill criteria and benchmark, and they pass `mt strategy validate`.

## Context & references

- Roadmap: [R2.04](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.05
- Spec: [14 §3 counterparty rule + P1 rows](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) · [14 §7 kill criteria](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) · [14 §1 benchmark rule](../../../docs/14-strategy-evidence-and-validation.md#1-viability-verdict-set-expectations-before-building)
- Templates from P2-T008/T009; builder in D03 (Part B) or edit YAML.
- Unblocks: Part B backtests/validation and P2-T067 (paper clock).

## Requirements

- `strategies/trend_majors/manifest.yaml`: universe BTC/ETH/SOL (+ FX majors/gold/indices if wanted), daily/4h, vol target, sleeve, counterparty (e.g. 'under-/over-reacting speculators and hedgers who pay for trend'), kill criteria (e.g. live Sharpe after 60 trades < backtest 5th percentile; DD > 1.5× backtest max), benchmark (buy-and-hold BTC + stablecoin yield).
- `strategies/funding_carry/manifest.yaml` only if a venue allows the products (else marked paper-only research).
- Kill criteria measurable and written **before** any paper run.

## ToDo

- [ ] Start from `mt strategy new --template trend_majors`
- [ ] Write counterparty, kill criteria, benchmark in your words
- [ ] Run `mt strategy validate strategies/*/manifest.yaml`
- [ ] Open a PR with the manifests (no secrets in them)
- [ ] Record completion in the progress log (no secrets) and run `./kanban done P2-T050`

## Verification

### Tests
- CI validates the manifests (pre-commit + CI job).

### Scenarios
- Given a manifest without kill criteria, when validated, then it fails and CI blocks the PR.

### Stress / failure injection
- n/a: authoring.

## Acceptance criteria

- [ ] Trend manifest valid and merged
- [ ] Carry manifest merged or explicitly deferred with reason

## Exceptions & edge cases

- Carry not permitted by the registry: keep it as paper-only research manifest.

## Cardinal rules (do NOT)

- Do NOT pick parameters by looking at the validation period (trial counter counts every tweak, Part B).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §3: link your P1 manifests.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.05 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T050-user-first-manifests` (only if a repo change results, e.g. non-secret config or manifests; secrets never go in git)
- PR title: `P2-T050: Write your first strategy manifests for the P1 candidates`
- PR checklist: no secrets in diff (gitleaks clean) · task file ticked · `./kanban done P2-T050` run

## Progress log

- 2026-10-21 00:00 · planner · created
