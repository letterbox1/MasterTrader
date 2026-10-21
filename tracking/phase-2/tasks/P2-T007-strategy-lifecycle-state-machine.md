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
depends_on: [P2-T006]
requirements: [R2.06]
roadmap_todos: [T2.20]
modules: [M0]
dashboards: [D03]
branch: p2/P2-T007-strategy-lifecycle-state-machine
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T007 · Strategy lifecycle state machine with gate checks

## Goal / expected outcome

Each strategy version moves draft → backtested → validated → paper → hitl → autonomous only through gate-checked, audited transitions (`strategy.promote|demote|set_mode`), with `autonomous` requiring C3.

## Context & references

- Roadmap: [R2.06](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.20
- Flow: [02 F7 strategy lifecycle](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · Gates: [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) · [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8)
- UI: [D03 detail actions + Gates tab](../../../docs/ui/dashboards/D03-strategies.md)
- Gate results come from Part B's validation harness (lab); this task defines the `GateProvider` interface they implement.
- Related: P2-B053 (mode naming).

## Requirements

- States: `draft`, `backtested`, `validated`, `paper`, `hitl`, `autonomous`, plus `archived`; transitions table in code.
- Gate checks per transition: backtested needs ≥ 1 completed backtest run; validated needs a passing validation report (from `GateProvider`); paper needs validated (or explicit 'paper from backtested' override, C1, audited); hitl needs paper; autonomous needs all §8 gates + C3.
- Demotion always allowed (C1) and immediate.
- Every transition writes `strategy.lifecycle_event` (WORM: insert-only, hash-chained via P0 WORM layer) + `audit.command`.
- `/strategies/{id}?gates=1` returns each gate pass/fail with the failing reason (D03 acceptance 2).

## ToDo

- [ ] `packages/mt_strategy/lifecycle.py` state machine + `GateProvider` protocol (stub provider returning 'not evaluated' until Part B lands)
- [ ] Migration for `strategy.lifecycle_event` registered with the WORM layer
- [ ] Commands `strategy.promote`, `strategy.demote`, `strategy.set_mode` with server-side levels
- [ ] Gates query endpoint
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: every allowed and forbidden transition (table-driven).
- Integration: promote to autonomous without C3 → rejected; with C3 approve + TOTP + cool-down → applied after cool-down.
- WORM: UPDATE/DELETE on `strategy.lifecycle_event` fails.

### Scenarios
- Given a validated strategy whose deflated Sharpe gate fails, when promoting to autonomous, then the command is refused and the gate reason is returned.
- Given an autonomous strategy, when demoted to hitl, then it applies immediately (C1) and running bots switch to approval cards.

### Stress / failure injection
- n/a: control-plane logic.

## Acceptance criteria

- [ ] All transitions enforced server-side and audited
- [ ] Autonomous requires C3 + gates
- [ ] Gates endpoint lists failing gates
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Gate provider unavailable (lab down): promotions above `backtested` refused; demotions still work.
- A new version starts at `draft` even if the previous version was autonomous.

## Cardinal rules (do NOT)

- Do NOT allow promotion to autonomous through any client without C3.
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
