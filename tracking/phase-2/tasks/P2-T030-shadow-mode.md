---
id: P2-T030
kind: task
title: Shadow mode: parallel paper run of a live or paper strategy
phase: 2
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T021, P2-T008]
requirements: [R2.07]
roadmap_todos: [T2.25, T2.20]
modules: [M0, M12]
dashboards: [D03]
branch: p2/P2-T030-shadow-mode
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T030 · Shadow mode: parallel paper run of a live or paper strategy

## Goal / expected outcome

Any running strategy version can be shadowed by another version (or itself) in paper mode on the same inputs, with a divergence report (signals, intents, P&L) — the shadow part of R2.07; sweeps and A/B on identical data are lab features delivered by Part B.

## Context & references

- Roadmap: [R2.07](../../../docs/roadmap/phase-2-strategies-risk-lab.md) (shadow part) · ToDos T2.20/T2.25 (no dedicated ToDo, see P2-B014)
- Spec: [03 M0 experimentation](../../../docs/03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe)
- Part B: sweeps + A/B (lab).

## Requirements

- `strategy.run_shadow` (C1): starts a shadow instance pinned to version X, mode forced `paper`, sandbox venue, same subscriptions.
- Shadow intents go through M11 in preview mode (decisions recorded, nothing sent), then simulated fills.
- `strategy.runs(kind=shadow)` + divergence metrics (signal agreement %, P&L delta, cost delta) at `/strategies/{id}/runs?shadow=1`.

## ToDo

- [ ] Shadow launcher in engine
- [ ] Divergence calculator
- [ ] Command + query
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Integration: shadow of v2 next to paper v1 produces runs + divergence metrics; zero venue orders from the shadow.

### Scenarios
- Given a shadow run, when it emits intents, then `audit.order` marks them `shadow=true` and no adapter receives them.

### Stress / failure injection
- Run 5 shadows alongside 5 paper strategies for 1 h: engine p99 signal→submit for real strategies unchanged (±10%).

## Acceptance criteria

- [ ] Shadow runs never reach a venue
- [ ] Divergence report available
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Shadow of a strategy needing L2 on an instrument without L2: refused at start.

## Cardinal rules (do NOT)

- Do NOT let shadow instances use non-paper accounts.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/03-build-spec.md` M0: shadow mode semantics.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.25, T2.20 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T030-shadow-mode`
- PR title: `P2-T030: Shadow mode: parallel paper run of a live or paper strategy`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T030` run

## Progress log

- 2026-10-21 00:00 · planner · created
