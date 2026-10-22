---
id: P0-T058
kind: task
title: Scenario: login with TOTP, run a command, see it chained and verified
phase: 0
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T050, P0-T052]
requirements: [R0.08, R0.07, R0.11]
roadmap_todos: [T0.24, T0.23]
modules: [mt_api, M17, M15]
dashboards: [D16]
tools: [git, node>=20, pnpm, playwright, uv, docker]
mcp: []
env: []
services: [postgres, nats, mt-api, caddy, loki]
branch: p0/P0-T058-scenario-login-command-audit-chain
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

# P0-T058 · Scenario: login with TOTP, run a command, see it chained and verified

## Goal / expected outcome

An automated end-to-end scenario (Playwright + API) covers exit criterion 2: log in with password + TOTP, issue a C0 test command (`system.settings.update` theme) and a C1 command (`audit.verify`), then confirm both appear in `audit.command` with a valid hash chain, in D16 Audit with ✓ status, and in the logs via `trace_id`.

## Context & references

- [Roadmap P0 §6 exit criteria](../../../docs/roadmap/phase-0-foundations.md#6-exit-criteria-demo) (2)
- [Roadmap P0 R0.08, R0.07](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [02 §7.2 commands](../../../docs/02-v1-architecture.md#72-commands-rest-write)
- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers)
- [D16 System](../../../docs/ui/dashboards/D16-system.md)
- Depends on: P0-T050, P0-T052 (which bring in P0-T034 and P0-T038)

## Requirements

- Runs against the full compose stack in CI (and on the host for the exit demo) with a seeded test credential.
- Steps: setup/login (TOTP via test secret) → C0 command → C1 preview + execute → `audit.verify` → D16 Audit shows rows with chain ✓ → click `trace_id` → Loki logs contain the same id.
- Unhappy paths: wrong TOTP → 401 + `auth_event`; replayed idempotency key → replay; missing `confirm_token` on C1 → 428.
- Asserts the DB chain directly (`recompute_chain`) as well as through the UI.

## ToDo

- [ ] Write `apps/web/e2e/scenario-login-command.spec.ts` + API assertions.
- [ ] Seed fixtures and teardown.
- [ ] Add to CI (nightly + on `packages/mt_api/**`).
- [ ] Record a run video/screens for the exit demo.

## Verification

### Tests
- The scenario with its unhappy paths.

### Scenarios
- Given a fresh stack, when the scenario runs, then every step passes and the audit chain verifies.
- Given the TOTP code is wrong, then login fails and the failure is in `audit.auth_event`.

### Stress / failure injection
- n/a: functional scenario; load is covered by P0-T059.

## Acceptance criteria

- [ ] Scenario green in CI and on the host
- [ ] Unhappy paths asserted
- [ ] Evidence captured for exit criterion 2
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check, Playwright viewport matrix)

## Exceptions & edge cases

- Clock skew in CI containers: TOTP generated from the same clock as the server.

## Cardinal rules (do NOT)

- Do NOT use a production credential in CI.
- Do NOT bypass the UI login with a pre-made cookie for this scenario.
- Loosening risk, autonomous mode and mandates are C3 (Telegram + TOTP + cool-down); Kill ON and protective exits never wait for approval.
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- None beyond the roadmap tick.
- `docs/roadmap/phase-0-foundations.md`: tick T0.24, T0.23 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T058-scenario-login-command-audit-chain`
- PR title: `P0-T058: Scenario: login with TOTP, run a command, see it chained and verified`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T058` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (confirm_token name (02 §7.2); deps trimmed to true preconditions; run fields added)
