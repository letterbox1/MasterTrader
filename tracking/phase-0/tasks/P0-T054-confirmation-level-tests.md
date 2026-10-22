---
id: P0-T054
kind: task
title: Verify confirmation levels: C3 needs approval + TOTP + cool-down, Kill ON never blocked
phase: 0
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T035, P0-T036]
requirements: [R0.08, R0.12]
roadmap_todos: [T0.62]
modules: [mt_api]
dashboards: []
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [postgres, nats]
branch: p0/P0-T054-confirmation-level-tests
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md]
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

# P0-T054 · Verify confirmation levels: C3 needs approval + TOTP + cool-down, Kill ON never blocked

## Goal / expected outcome

An adversarial test suite proves that confirmation levels are enforced server-side: no C3 command applies without out-of-band approval **and** a fresh TOTP **and** the full cool-down; C1/C2 require a valid, unexpired, args-bound token; Kill ON succeeds under every degraded condition; Kill OFF is C3.

## Context & references

- [Roadmap P0 R0.08](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.62](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [02 §7.2 commands](../../../docs/02-v1-architecture.md#72-commands-rest-write)
- [07 §6 application controls](../../../docs/07-security-notes.md#6-application-controls)
- [ui §3.3 confirmation](../../../docs/ui/README.md#33-actions--confirmation)
- Implementation: P0-T035
- Depends on: P0-T035, P0-T036

## Requirements

- C3 negative cases (each must leave state unchanged and audit a rejection): no approval; approval without TOTP; TOTP before approval; replayed TOTP; wrong TOTP; approval after 10 min TTL; apply attempt at cool-down − 1 s (SimClock); session expired at apply time; cancel during cool-down; args changed between preview and execute; approval for a different pending id.
- C3 positive: `mtctl approve` → TOTP → wait the configured cool-down (default 900 s, [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)) → applied exactly once; restart mt-api mid cool-down → still applies at the original `apply_at`.
- C1/C2: missing `confirm_token` → 428; expired token (TTL + 1 s) → 428; token reused → 428; token for other args → 428; C2 with a mismatched risk-preview hash → 428; C2 with a session re-authenticated more than 12 h ago (default) → 428 `reauth_required` ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P0-B003).
- Kill ON: succeeds with Postgres paused, with the user locked out of login (uses existing session), under 200 req/s load, with the idempotency store down; p99 < 200 ms; KV `kill` set; audit row appears once DB returns.
- Kill OFF is C3 (all C3 negatives apply).
- Direct API calls (no UI) cannot skip any level.

## ToDo

- [ ] Write `tests/verify/test_confirmation_levels.py` (pytest, SimClock, real Postgres/NATS containers).
- [ ] Add a load harness for the Kill latency case.
- [ ] Wire into CI (marked `verify`), runtime ≤ 5 min.
- [ ] Log results in this task.

## Verification

### Tests
- The suite above (≥ 25 cases).

### Scenarios
- Given an attacker with a stolen session cookie, when they post `risk.kill.off`, then it stays pending forever without your break-glass/Telegram approval and TOTP.
- Given mt-api is restarted 10 times during a cool-down, then the change still applies exactly once at `apply_at`.

### Stress / failure injection
- Kill ON under 200 req/s background + Postgres paused: p99 < 200 ms (logged).

## Acceptance criteria

- [ ] All negative cases rejected and audited
- [ ] Positive C3 path applies exactly once incl. across restarts
- [ ] Kill ON never blocked under the listed faults; p99 < 200 ms
- [ ] Suite runs in CI
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Telegram channel tests arrive in P2 (T2.33/T2.07); this suite uses the break-glass channel and a fake channel.

## Cardinal rules (do NOT)

- Do NOT mock the confirmation engine itself; only the approval channel and clock.
- Do NOT weaken cool-down defaults in tests other than via SimClock.
- Loosening risk, autonomous mode and mandates are C3 (Telegram + TOTP + cool-down); Kill ON and protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- None beyond the roadmap tick.
- `docs/roadmap/phase-0-foundations.md`: tick T0.62 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T054-confirmation-level-tests`
- PR title: `P0-T054: Verify confirmation levels: C3 needs approval + TOTP + cool-down, Kill ON never blocked`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T054` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (C1 confirm_token, C2 preview hash + 12 h re-auth cases (17 §D P0-B003), break-glass mtctl, cool-down from settings; run fields added)
