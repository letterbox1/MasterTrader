---
id: P7-T046
kind: task
title: Verify venue-registry re-check (< 90 days) gates every funding
phase: 7
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T011, P7-T003]
requirements: [R7.13, R7.05]
roadmap_todos: [T7.63]
modules: [M11]
dashboards: [D06, D16]
branch: p7/P7-T046-verify-registry-recheck-before-funding
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T046 · Verify venue-registry re-check (< 90 days) gates every funding

## Goal / expected outcome

Tests and a recorded check prove that funding confirmation, capital steps and live-mode changes are refused whenever a target venue/product is not `allowed` or its AUSTRAC check is ≥ 90 days old.

## Context & references

- Roadmap: [R7.13, R7.05 · ToDo T7.63](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Roadmap T7.63 → [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) (re-check quarterly; products blocked until reconciled) · Roadmap §7 risk 'venue status changes'
- Related: P7-T011 (preflight), P7-T003 (your checks), P7-T057, P7-T061

## Requirements

- Test matrix: {allowed, read_only, blocked} × {checked 89 days, 90 days, 91 days} × {fund, capital step, bot autonomous, strategy live} → only allowed+<90 passes.
- Recorded pre-funding check for the actual target venues (output of `mt preflight --venue …`) attached to the progress log before P7-T057.

## ToDo

- [ ] Write the integration test matrix in `tests/integration/test_registry_gate.py`.
- [ ] Run `mt preflight` for the real targets; attach redacted output.
- [ ] File a bug for any path that is not gated.

## Verification

### Tests
- Integration: 36-case matrix above.
- Regression: `venue.registry.changed` during a pending C3 capital step cancels it.

### Scenarios
- Given a venue checked 90 days ago, when you confirm funding, then it is refused with 'AUSTRAC re-check overdue'.

### Stress / failure injection
- n/a: deterministic gating tests.

## Acceptance criteria

- [ ] Matrix passes in CI.
- [ ] Pre-funding check for real targets recorded and green.

## Exceptions & edge cases

- Venue status changes between check and funding: re-evaluated at apply time.

## Cardinal rules (do NOT)

- Do NOT stub the registry in the recorded pre-funding check.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.

## Doc sync on completion

- `docs/12-policy-and-compliance.md` §2: note the enforced 90-day window.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.63 when this item is done.

## Branch & PR

- Branch: `p7/P7-T046-verify-registry-recheck-before-funding`
- PR title: `P7-T046: Verify venue-registry re-check (< 90 days) gates every funding`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T046` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
