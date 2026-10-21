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
depends_on: [P2-T019, P2-T035, P2-T043]
requirements: [R2.19]
roadmap_todos: [T2.24]
modules: [M11]
dashboards: [D06]
branch: p2/P2-T053-verify-change-control-c3
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T053 · Change-control C3 and hard-ceilings tests

## Goal / expected outcome

End-to-end tests prove: tightenings apply immediately; every loosening (policy, ladder up, venue allow, kill off, bot autonomous, approval-policy loosen) needs Telegram approve + TOTP + cool-down; values above ceilings are always rejected; no API can write the ceilings file; the UI and server classify independently.

## Context & references

- Roadmap: [R2.19](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.24
- Flow: [02 F5](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [D06 acceptance 1–2](../../../docs/ui/dashboards/D06-risk.md) · [07 §6](../../../docs/07-security-notes.md#6-application-controls)
- Cross-phase: P0 confirmation-level tests (T0.62).

## Requirements

- Matrix: 6 loosening command kinds × {no approval, approve without TOTP, wrong TOTP, right TOTP before cool-down, after cool-down} → only the last applies.
- Tightening matrix applies instantly with audit + notification.
- Ceiling: valid C3 above ceiling → rejected.
- Direct API call crafted to look like a tighten while actually loosening → server classifies as loosen.
- Ceilings write attempts: no endpoint; container write → EROFS.

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
- [ ] Ceilings unwritable via any interface

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
