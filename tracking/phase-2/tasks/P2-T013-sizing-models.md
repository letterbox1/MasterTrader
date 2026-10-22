---
id: P2-T013
kind: task
title: Position sizing models including capped Kelly
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T010]
requirements: [R2.12]
roadmap_todos: [T2.22]
modules: [M11]
dashboards: []
tools: [uv]
mcp: []
env: []
services: []
branch: p2/P2-T013-sizing-models
pr: ""
doc_sync: [docs/03-build-spec.md, docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T013 · Position sizing models including capped Kelly

## Goal / expected outcome

`packages/mt_risk/sizing` implements fixed, fixed-fractional, volatility-target, stop-distance, capped-Kelly and risk-parity sizing, selectable per strategy, with the 14 §4 Kelly rules enforced in code and Decimal math throughout.

## Context & references

- Roadmap: [R2.12](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.22
- Spec: [14 §4 sizing](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) · [03 M11 sizing models](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp)
- Related: the MasterTradingBot sizing library (P2-T131) must agree with these models (golden files).
- Defaults: risk per trade 1% of sleeve equity [0.1–2%], Kelly quarter-Kelly ceiling ([16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)); every model parameter is an L4 setting with its 16 default.
- Golden tests are mandatory for merge (R2.N2, P2-T051).

## Requirements

- Fixed size; fixed-fractional (% of sleeve equity); vol target (target 15–20% annualised from 30–60d realised vol or ATR); stop-distance `units = capital × risk% ÷ |entry − stop|`; Kelly `f = (p·b − q)/b`, q = 1 − p, b = measured avg win ÷ avg loss, **used fraction ≤ ¼ f (ceiling, not target)**; risk parity across a strategy's instruments.
- Reject the `(2p − 1)` shortcut: Kelly requires measured b; b missing → model error, never default b = 1.
- Never stack Kelly on a vol-targeted sleeve: policy validation error if a sleeve has `vol_target` and a strategy in it selects Kelly.
- f ≤ 0 → size 0 (no trade). All outputs then capped by risk/trade and max position limits (P2-T012) and rounded down to lot size.
- Size multipliers applied after the model: ladder rung 2 × 0.5 (P2-T018) and sleeve drawdown stage 1 × 0.5 (P2-T012); multipliers come from policy, not code.

## ToDo

- [ ] Implement models + selector in `packages/mt_risk/sizing/`
- [ ] Policy validation rule (Kelly × vol-target)
- [ ] Golden fixtures `tests/golden/sizing/*.yaml`
- [ ] Property tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Golden: worked examples per model (inputs → exact Decimal units).
- Property: size never exceeds risk/trade or max position caps; Kelly output ≤ 0.25·f; monotone in capital.
- Unit: `2p−1` path impossible (b required); Kelly on vol-target sleeve → validation error.

### Scenarios
- Given p = 0.55, b = 1.2, when Kelly sizing, then f = (0.55·1.2 − 0.45)/1.2 = 0.175 and used ≤ 0.04375 of sleeve.
- Given entry 100, stop 95, capital 10,000, risk 1%, when stop-distance sizing, then 20 units (rounded down to lot).

### Stress / failure injection
- Hypothesis 10k cases per model in CI; runtime < 1 s; per-call p99 < 20 µs.

## Acceptance criteria

- [ ] Six models implemented with golden tests
- [ ] Kelly rules enforced and tested
- [ ] All sizes Decimal and lot-rounded down
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Vol estimate unavailable (insufficient history): model refuses, intent rejected with `sizing_unavailable`.
- Instrument min size above computed size: size 0, not min size.

## Cardinal rules (do NOT)

- Do NOT use floats for sizes or money.
- Do NOT round sizes up to meet a venue minimum.
- Do NOT default Kelly's b.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §4: link golden examples.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.22 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T013-sizing-models`
- PR title: `P2-T013: Position sizing models including capped Kelly`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T013` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (risk-per-trade default and multipliers from policy (16 §2.1); MTB link)
