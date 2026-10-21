---
id: P2-T018
kind: task
title: Six-rung fallback ladder state machine
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T017]
requirements: [R2.15]
roadmap_todos: [T2.22]
modules: [M11]
dashboards: [D06]
branch: p2/P2-T018-fallback-ladder
pr: ""
doc_sync: [docs/ui/dashboards/D06-risk.md, docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T018 · Six-rung fallback ladder state machine

## Goal / expected outcome

The 6-rung fallback ladder runs live per sleeve and system-wide, driven by confidence, decision lateness/staleness, model-service health, hard-limit breaches and the kill switch; it adjusts the gate's decisions and is visible in D06; `risk.ladder.set` steps down at C1 and up at C3.

## Context & references

- Roadmap: [R2.15](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.22
- Spec: [03 M11 fallback ladder](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) · [14 §5 ladder](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) · [D06 ladder widget](../../../docs/ui/dashboards/D06-risk.md)
- Related: P2-B004 (D06 lists 5 rungs), P2-T037 (auto-downgrade at rung ≥ 3), P2-T060 ladder tests.

## Requirements

- Rungs: 1 healthy + high confidence → normal size; 2 low confidence → half size or observe only (policy); 3 late decision / stale feed → hold (no new orders); 4 model service down → rules only: manage exits, no new entries; 5 hard limit breached → halt sleeve, cancel open orders, close per sleeve rule, alert; 6 kill switch → halt everything (+ vault sweep hook, delivered in P5 R5.07).
- Inputs: tier-A confidence (from signal metadata; absent = rung 1 for rule strategies), `dq.status`, decision timestamp vs deadline, heartbeats (`sys.heartbeat.decision-svc` when present, model loader health), limit breaches, KV `kill`.
- Effective rung = max(automatic, manual floor); manual step **down** (more cautious) C1, step **up** C3; automatic recovery only from rungs 2–4 when inputs clear for a hysteresis window (default 60 s); rungs 5–6 need manual action.
- KV `risk_state.ladder.{scope}`, `risk.event{type: ladder_change}`, `/risk/state?ladder=1`.

## ToDo

- [ ] `packages/mt_risk/ladder.py`
- [ ] Gate integration (size multiplier, hold, exits-only)
- [ ] `risk.ladder.set` command classification
- [ ] Endpoint + WS `risk.state` field
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Ladder tests: each input drives the expected rung; hysteresis; manual floor; C3 for step up.
- Integration: rung 4 → entry rejected `ladder_exits_only`, exit allowed.

### Scenarios
- Given the model service heartbeat is missing, when a tier-A strategy emits an entry, then it is rejected and existing positions' exits still run.
- Given you step the ladder down to rung 3 from Telegram, when applied, then it is immediate; stepping back to 1 asks for TOTP + cool-down.

### Stress / failure injection
- Flap the feed status every 500 ms for 2 min: no rung oscillation faster than the hysteresis window; no orders slip through during rung 3.

## Acceptance criteria

- [ ] Six rungs implemented as in 03 M11/14 §5
- [ ] Gate honours each rung
- [ ] Manual set levels enforced server-side
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- No tier-A model in use: rung 2 never triggers from confidence.
- Rung 6 vault sweep is a no-op hook in P2 (logged) until P5 delivers it.

## Cardinal rules (do NOT)

- Do NOT auto-recover from rungs 5–6.
- Do NOT let a manual step-up bypass C3.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/ui/dashboards/D06-risk.md`: ladder widget shows six rungs (fix per P2-B004).
- `docs/14-strategy-evidence-and-validation.md` §5: inputs and hysteresis.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.22 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T018-fallback-ladder`
- PR title: `P2-T018: Six-rung fallback ladder state machine`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T018` run

## Progress log

- 2026-10-21 00:00 · planner · created
