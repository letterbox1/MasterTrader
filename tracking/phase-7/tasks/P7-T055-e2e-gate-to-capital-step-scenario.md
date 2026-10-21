---
id: P7-T055
kind: task
title: End-to-end scenario: gate pass → fund → micro-live → clean weeks → capital step
phase: 7
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T019, P7-T028, P7-T014, P7-T016, P7-T020, P7-T011]
requirements: [R7.05, R7.01, R7.08, R7.03]
roadmap_todos: [T7.21]
modules: [M11, M7, M18, M15]
dashboards: [D03, D06, D14, D01]
branch: p7/P7-T055-e2e-gate-to-capital-step-scenario
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T055 · End-to-end scenario: gate pass → fund → micro-live → clean weeks → capital step

## Goal / expected outcome

A staging run with a simulated clock exercises the whole Phase 7 flow on paper venues — preflight, gate report, funding confirmation, HITL weeks with reviews, clean-week counting, C3 capital step, C3 autonomous promotion, a dirty week resetting the streak — and every step leaves the expected audit trail.

## Context & references

- Roadmap: [R7.05, R7.01, R7.08, R7.03 · ToDo T7.21](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) · [02 §8 flows](../../../docs/02-v1-architecture.md#8-end-to-end-flows) F7 · [15 §1](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) · Roadmap exit criteria 1 and 3
- Related: P7-T011, P7-T014, P7-T016, P7-T019, P7-T020, P7-T028

## Requirements

- Simulated 10 weeks: weeks 1–4 clean (reviews signed) → step proposal → C3 approve → capital +25%; week 6 unsigned review → dirty, streak reset; weeks 7–10 clean → second proposal; bot promoted to autonomous at week 5 via C3; a decay injection at week 9 downgrades it.
- Audit trail check: for each event, the WORM rows exist and chain-verify (`audit.verify`).
- Runs nightly in CI against the staging compose with paper venues and the test clock provider.

## ToDo

- [ ] Scenario script `tests/e2e/test_phase7_flow.py`.
- [ ] Test clock provider wiring (test-only).
- [ ] Audit-trail assertions + `audit.verify` call.
- [ ] Nightly CI job.

## Verification

### Tests
- E2E scenario above; audit chain verification.

### Scenarios
- Given week 6's review is unsigned, then no proposal appears in week 8 and the D06 streak shows 2/4.

### Stress / failure injection
- Run the scenario with random venue disconnects (toxiproxy) — outcome unchanged except recorded unconfirmed periods.

## Acceptance criteria

- [ ] Scenario passes nightly in CI.
- [ ] Audit chain verifies for every event.

## Exceptions & edge cases

- Test clock must be impossible to enable in production (build flag + config validator).

## Cardinal rules (do NOT)

- Do NOT point the scenario at live sub-accounts.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §7: link the scenario as the executable spec.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.21 when this item is done.

## Branch & PR

- Branch: `p7/P7-T055-e2e-gate-to-capital-step-scenario`
- PR title: `P7-T055: End-to-end scenario: gate pass → fund → micro-live → clean weeks → capital step`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T055` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
