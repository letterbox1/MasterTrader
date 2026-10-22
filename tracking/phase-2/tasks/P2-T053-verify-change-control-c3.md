---
id: P2-T053
kind: task
title: Change-control C3 and hard-ceilings tests
phase: 2
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T019, P2-T035, P2-T043, P2-T011, P2-T012, P2-T037]
requirements: [R2.19]
roadmap_todos: [T2.24]
modules: [M11]
dashboards: [D06]
tools: [uv, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p2/P2-T053-verify-change-control-c3
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T053 · Change-control C3 and hard-ceilings tests

## Goal / expected outcome

End-to-end tests prove: tightenings apply immediately at every layer; every loosening (policy at any layer incl. **L0 ceilings**, gate-profile loosen, ladder up, venue allow, kill off, bot → autonomous, approval-policy loosen, `risk.sleeve.restart`, drawdown peak reset) needs Telegram approve + TOTP + cool-down; paper → HITL is C2 (not C3); values above an L0 ceiling are always rejected; MCP-style sources can never loosen; the UI and server classify independently.

## Context & references

- Roadmap: [R2.19](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.24
- Flow: [02 F5](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [D06 acceptance 1–2](../../../docs/ui/dashboards/D06-risk.md) · [07 §6](../../../docs/07-security-notes.md#6-application-controls)
- Cross-phase: P0 confirmation-level tests (P0-T054, T0.62) cover the generic engine; this task covers the risk classifier.
- Decisions: [16 §1](../../../docs/16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance) (tighten immediate, loosen C3 at every layer incl. L0) · [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) (cool-down 15 min; paper → HITL C2; `risk.sleeve.restart` C3) · [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22) (L0 in the strategy settings).

## Requirements

- Matrix: 9 loosening command kinds (L1–L3 policy, L0 ceiling, gate profile, ladder up, venue allow, kill off, bot → autonomous, approval-policy loosen, `risk.sleeve.restart`) × {no approval, approve without TOTP, wrong TOTP, right TOTP before cool-down, after cool-down} → only the last applies.
- `bot.set_mode` paper → hitl asks for C2 (not C3, not C1).
- Tightening matrix applies instantly with audit + notification.
- Ceiling: valid C3 above ceiling → rejected.
- Direct API call crafted to look like a tighten while actually loosening → server classifies as loosen.
- L0 ceilings: tightening via `risk.policy.update {layer: L0}` applies immediately; loosening needs C3; a `risk_tighten`-scoped (MCP-style) token can never loosen anything.
- Break-glass: with `c3.break_glass_enabled=false` the `mtctl approve` path is refused.

## ToDo

- [ ] Test matrix in `tests/e2e/change_control/`
- [ ] Fake Telegram + TOTP fixtures
- [ ] Report table in progress log
- [ ] Record results (numbers, run IDs, screenshots) in the progress log and tick the roadmap ToDo box

## Verification

### Tests
- As above (pytest e2e against compose test stack).

### Scenarios
- Given cool-down 15 min (test-shortened to 5 s via config), when the timer ends, then the change applies and `risk.change` status becomes applied.

### Stress / failure injection
- Concurrent loosen + tighten on the same field: final value respects ordering; both audited.

## Acceptance criteria

- [ ] Every cell of the matrix passes
- [ ] L0 ceilings loosen only via C3 from any interface

## Exceptions & edge cases

- Test-only short cool-down must be impossible in production config (config validator).

## Cardinal rules (do NOT)

- Do NOT ship a production config with shortened cool-down.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/07-security-notes.md` §6: link the test matrix.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.24 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T053-verify-change-control-c3`
- PR title: `P2-T053: Change-control C3 and hard-ceilings tests`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T053` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (C3 matrix for every layer incl. L0, gate profile, sleeve restart; paper→HITL C2; break-glass off)
