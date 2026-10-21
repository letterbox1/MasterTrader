---
id: P5-T053
kind: task
title: Policy tests: autonomy limits and the never-automated list
phase: 5
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T041, P5-T042, P5-T043, P5-T044, P5-T048, P5-T049]
requirements: [R5.15, R5.16]
roadmap_todos: []
modules: [M4, M19, M15]
dashboards: [D12, D13]
branch: p5/P5-T053-verify-autonomy-never-automated-policy
pr: ""
doc_sync: [docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T053 · Policy tests: autonomy limits and the never-automated list

## Goal / expected outcome

An integration suite proves the autonomy boundary: only read-only work, mandated eligible claims from identity wallets (simulation + cost gate), genuine-use tasks after a clean burner run, and defensive revokes/sweeps run without you; every never-automated item becomes a refusal or a user task — at the API, decision, executor and UI layers.

## Context & references

- Roadmap: [R5.15](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) and [R5.16](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) ("Policy tests")
- [08 autonomous](../../../docs/08-airdrops-and-token-launches.md#what-may-run-autonomously) · [08 never automated](../../../docs/08-airdrops-and-token-launches.md#never-automated) · policy module P5-T042

## Requirements

- Matrix: each NA item × {mt_api direct call, decision engine input, executor queue injection, UI presence} → refused/absent.
- Positive cases: read-only discovery runs unattended; mandated claim executes; revoke of a flagged hot-wallet approval runs with kill ON.
- Negative cases: claim without mandate → CLAIM_MANUAL; mandate expired → CLAIM_MANUAL; ICO → ICO_REVIEW; social task → user task; second wallet in a campaign → refused.
- Report: matrix table in the PR and the progress log.

## ToDo

- [ ] Write `tests/policy/test_autonomy_matrix.py` and Playwright checks for absent controls.
- [ ] Add to CI as a required check; record the matrix.

## Verification

### Tests
- Integration matrix (≥ 56 cells) + Playwright absence checks.

### Scenarios
- Given an MCP-style token (future) calls `airdrop.mandate.create`, then it is refused (mandates never exposed, 02 §7.4).

### Stress / failure injection
- n/a: deterministic policy matrix

## Acceptance criteria

- [ ] Every matrix cell passes
- [ ] Required CI check
- [ ] Matrix recorded

## Exceptions & edge cases

- New command added later without an NA classification → meta-test fails until classified.

## Cardinal rules (do NOT)

- Do NOT weaken a policy cell to make the matrix green.
- Do NOT apply loosening (new mandate, higher caps, autonomous claims) without C3 (Telegram approve + TOTP + cool-down); protective actions (revoke, sweep, kill) never wait for approval.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- No doc change beyond ticking R5.15/R5.16 verification in the roadmap.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick the related exit criterion when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T053-verify-autonomy-never-automated-policy`
- PR title: `P5-T053: Policy tests: autonomy limits and the never-automated list`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T053` run

## Progress log

- 2026-10-21 00:00 · planner · created
