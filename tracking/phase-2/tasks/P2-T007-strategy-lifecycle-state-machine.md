---
id: P2-T007
kind: task
title: Strategy lifecycle state machine with gate checks
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T006, P0-T029, P0-T035]
requirements: [R2.06]
roadmap_todos: [T2.20]
modules: [M0]
dashboards: [D03]
tools: [uv]
mcp: []
env: []
services: [postgres]
branch: p2/P2-T007-strategy-lifecycle-state-machine
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T007 · Strategy lifecycle state machine with gate checks

## Goal / expected outcome

Each strategy version is **promoted** draft → backtested → validated only through gate-checked, audited transitions (`strategy.promote|demote`), and its **mode ceiling** (`strategy.set_mode`: `paper` → `hitl` → `autonomous`) caps the modes of its bots (the stricter of strategy and bot mode applies). Allowing `hitl` is C2, allowing `autonomous` is C3 with every gate of the strategy's gate profile passing; restricting is C1.

## Context & references

- Roadmap: [R2.06](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.20
- Flow: [02 F7 strategy lifecycle](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · Gates: [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) · [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8)
- UI: [D03 detail actions + Gates tab](../../../docs/ui/dashboards/D03-strategies.md)
- Gate results come from Part B's validation harness (lab); this task defines the `GateProvider` interface they implement.
- Decisions: [17 §B modes](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (`paper`/`hitl`/`autonomous` per bot; a strategy is promoted through gates, a bot is switched between modes) · [16 §2.3 strategy mode ceiling](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) · [16 §2.4 gate profile](../../../docs/16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile)
- Cross-phase (`depends_on`): WORM layer for `strategy.lifecycle_event` (P0-T029, T0.23); confirmation-level engine C1–C3 (P0-T035).

## Requirements

- Lifecycle states: `draft`, `backtested`, `validated`, plus `archived`; mode ceiling `paper` / `hitl` / `autonomous` (set by `strategy.set_mode`, D03 lines 13–14); transitions table in code. `approve`/`auto` are retired aliases.
- Gate checks: backtested needs ≥ 1 completed backtest run; validated needs a passing validation report (from `GateProvider`); ceiling `paper` needs validated (or explicit 'paper from backtested' override, C1, audited); ceiling `hitl` needs the paper-stage gates (**C2**); ceiling `autonomous` needs every gate of the profile (incl. the paper/HITL period and the safety drills) + **C3**.
- **Gate profile per strategy** ([16 §2.4](../../../docs/16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile), defaults, configurable): DSR ≥ 0.95, MC permutation p < 0.05, walk-forward ≥ 60% positive folds and worst fold ≥ −(sleeve halt drawdown), profitable at 2× costs (3× reported), positive per year and per regime (or labelled single-regime), beats benchmark, leakage + look-ahead clean or waived, safety drills passed, paper/HITL period ≥ 8 weeks **and** ≥ 50 trades (P1 sleeves ≥ 8 weeks; memecoin ≥ 300 trades; low-frequency ≥ 26 weeks). Stored as versioned config rows (WORM); tightening free (C1), **loosening any gate is C3** (classified by P2-T019). No threshold hard-coded.
- Restricting the ceiling is always allowed (C1) and immediate; bots above the new ceiling drop to it (P2-T037).
- Every transition writes `strategy.lifecycle_event` (WORM: insert-only, hash-chained via P0 WORM layer) + `audit.command`.
- `/strategies/{id}?gates=1` returns each gate pass/fail with the failing reason (D03 acceptance 2).

## ToDo

- [ ] `packages/mt_strategy/lifecycle.py` state machine + mode ceiling + `GateProvider` protocol (stub provider returning 'not evaluated' until P2-T114 lands)
- [ ] Gate-profile store (`strategy.gate_profile` versioned rows, defaults from 16 §2.4 with class overrides) + update command classified tighten/loosen by P2-T019
- [ ] Migration for `strategy.lifecycle_event` registered with the WORM layer
- [ ] Commands `strategy.promote`, `strategy.demote`, `strategy.set_mode` with server-side levels
- [ ] Gates query endpoint
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: every allowed and forbidden transition (table-driven).
- Integration: `strategy.set_mode autonomous` without C3 → rejected; with C3 approve + TOTP + cool-down (default 15 min) → applied after cool-down. `strategy.set_mode hitl` from paper → C2.
- Unit: loosening a gate (e.g. DSR 0.95 → 0.90) → C3; tightening → C1.
- WORM: UPDATE/DELETE on `strategy.lifecycle_event` fails.

### Scenarios
- Given a validated strategy whose DSR is 0.91 (< 0.95 default), when allowing autonomous, then the command is refused and the gate reason is returned.
- Given a strategy with ceiling `autonomous`, when restricted to `hitl`, then it applies immediately (C1) and its autonomous bots drop to HITL approval cards.

### Stress / failure injection
- n/a: control-plane logic.

## Acceptance criteria

- [ ] All transitions enforced server-side and audited
- [ ] Autonomous requires C3 + gates
- [ ] Gates endpoint lists failing gates
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Gate provider unavailable (lab down): promotions above `backtested` and ceiling raises refused; restrictions still work.
- Memecoin / `paper_only` templates: ceiling stays `paper` in P2 (P2-T009).
- A new version starts at `draft` even if the previous version was autonomous.

## Cardinal rules (do NOT)

- Do NOT allow the `autonomous` ceiling through any client without C3, or hard-code a gate threshold.
- Do NOT skip writing the lifecycle event.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows with `supersedes_id` (15 §2).
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/02-v1-architecture.md` F7 and `docs/03-build-spec.md` M0: state names as built (hitl/autonomous).
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.20 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T007-strategy-lifecycle-state-machine`
- PR title: `P2-T007: Strategy lifecycle state machine with gate checks`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T007` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (promotion vs mode ceiling (strategy.set_mode caps bots, C2/C3/C1), per-strategy gate profile from 16 §2.4 with loosening C3, DSR ≥ 0.95)
