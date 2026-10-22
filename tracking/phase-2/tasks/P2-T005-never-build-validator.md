---
id: P2-T005
kind: task
title: Never-build validator for X/Never strategy patterns
phase: 2
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T004]
requirements: [R2.05]
roadmap_todos: [T2.20]
modules: [M0]
dashboards: [D03]
tools: [uv]
mcp: []
env: []
services: []
branch: p2/P2-T005-never-build-validator
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

# P2-T005 · Never-build validator for X/Never strategy patterns

## Goal / expected outcome

The manifest validator rejects strategies on the 14 §3 X/Never list (sniping, latency/atomic arb, copy-trading, prediction-market bots, JIT liquidity, listing/news latency trading, sandwiching or any user-harming MEV), with a reason the builder can show.

## Context & references

- Roadmap: [R2.05](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.20
- Spec: [14 §2 no speed edge](../../../docs/14-strategy-evidence-and-validation.md#2-where-a-solo-operator-in-sydney-has-an-edge) · [14 §3 X/Never rows](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) · [03 M0 never-build list](../../../docs/03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe)
- Policy: [12 §1 Polymarket blocked](../../../docs/12-policy-and-compliance.md#1-australian-boundary-the-load-bearing-assumption) · [12 §3 conduct](../../../docs/12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention)
- Related: P2-T004 manifest; the sandboxed generator (P2-T116) calls this validator on generated strategies.

## Requirements

- Rule set in `packages/mt_strategy/never_build.yaml` (versioned): each rule has `id`, `label` (X or Never), `reason`, `evidence` link.
- Manifest checks: template/tags in the deny list; venue `POLYMARKET`/`KALSHI` with any order capability; decision deadline < 1 s combined with taker-only execution; subscriptions to mempool/new-pool/new-listing streams for entry timing; `copy_wallet`/`follow_trader` signal sources (wallets allowed only as **features**).
- Code checks (AST scan of the strategy module): bundles that include or reference other users' pending transactions (backruns, sandwiches); private submission of your own swap (Flashbots Protect / Jito, 13 §7) stays allowed; sub-second order loops keyed on listing events.
- Result: `NeverBuildViolation(rule_id, label, reason, evidence_line)`; `Never` cannot be waived; `X` cannot be waived in P2 either (no waiver path).

## ToDo

- [ ] Write the rule file and loader
- [ ] Implement manifest + AST checks in `packages/mt_strategy/never_build.py`
- [ ] Hook into `mt strategy validate`, `strategy.create` and the generator path
- [ ] Fixtures: one manifest per prohibited pattern + near-miss allowed cases (wallet flows as features; memecoin momentum entering 5–60 min after launch)
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: each prohibited fixture rejected with the right rule id.
- Unit: allowed near-misses pass (memecoin momentum with `entry_delay_min ≥ 5`; wallet-flow feature).
- Integration: `strategy.create` via `mt_api` returns problem+json with the rule reason.

### Scenarios
- Given a 'memecoin sniper' manifest entering in the first slot, when saved in D03, then save is refused and the reason cites 14 §3 X.
- Given a sandwich pattern in generated code, when validated, then it is rejected as Never and logged to `audit.command`.

### Stress / failure injection
- n/a: static validation.

## Acceptance criteria

- [ ] All 14 §3 X/Never patterns covered by a rule and a failing fixture
- [ ] Allowed near-misses pass
- [ ] Rejection reasons surface through `mt_api`
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Market making is P3 (allowed later via Hummingbot, P6), not X: must not be rejected.
- Rule updates are code changes reviewed in PRs, never runtime-editable.

## Cardinal rules (do NOT)

- Do NOT add a waiver or override flag for Never rules.
- Do NOT treat wallets as signal sources for copy-trading; features only.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §3: link the rule file as the enforced list.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.20 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T005-never-build-validator`
- PR title: `P2-T005: Never-build validator for X/Never strategy patterns`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T005` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields; generator link)
