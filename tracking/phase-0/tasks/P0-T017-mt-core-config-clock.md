---
id: P0-T017
kind: task
title: Implement mt_core config, clock and ID helpers
phase: 0
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T014]
requirements: [R0.01, R0.N1]
roadmap_todos: [T0.21]
modules: [mt_core]
dashboards: []
branch: p0/P0-T017-mt-core-config-clock
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T017 · Implement mt_core config, clock and ID helpers

## Goal / expected outcome

Services load typed settings from environment + files where secrets come only from tmpfs-mounted files, and all code reads time through an injectable `Clock` (system, frozen or simulated) so tests and backtests are deterministic.

## Context & references

- [Roadmap P0 T0.21](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [02 §5.2 key conventions](../../../docs/02-v1-architecture.md#52-key-conventions)
- [07 §2 secrets](../../../docs/07-security-notes.md#2-secrets)
- Related: P0-T022 (tmpfs layout `/run/secrets/<service>/<name>`)
- Depends on: P0-T014

## Requirements

- `mt_core.config.Settings` (pydantic-settings) per service; secret fields typed `SecretStr`, read from `/run/secrets/<service>/<name>`; with `MT_ENV=prod`, env-provided secrets are refused.
- `Clock` protocol with `now_utc()`, `monotonic_ns()`; `SystemClock`, `FrozenClock`, `SimClock`. A ruff banned-api rule forbids `datetime.now()`/`time.time()` outside `mt_core.clock`.
- Display timezone default `Australia/Sydney`; storage always UTC.
- Settings dumps redact every `SecretStr`.

## ToDo

- [ ] Implement the Settings base with a file-secret source and the prod guard.
- [ ] Implement Clock variants and the banned-api config.
- [ ] Tests for redaction, prod guard and clock behaviour.

## Verification

### Tests
- Unit: secret from file loads; env secret refused when `MT_ENV=prod`; `repr(settings)` never contains the secret.
- Unit: `FrozenClock` stable; `SimClock.advance(5s)` works.

### Scenarios
- Given a secret file is missing, when the service starts, then it exits non-zero naming the secret (not its value).

### Stress / failure injection
- n/a: library code.

## Acceptance criteria

- [ ] Settings + Clock implemented with tests
- [ ] Banned-api rule active and passing
- [ ] No secret appears in any log or repr (tested)
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Clock skew: the system clock is chrony-synced (P0-T019); `Clock` doesn't correct skew; M16 monitors it (P1).

## Cardinal rules (do NOT)

- Do NOT read secrets from environment variables in production.
- Do NOT call `datetime.now()` directly outside `mt_core.clock`.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- None beyond the roadmap tick.
- `docs/roadmap/phase-0-foundations.md`: tick T0.21 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T017-mt-core-config-clock`
- PR title: `P0-T017: Implement mt_core config, clock and ID helpers`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T017` run

## Progress log

- 2026-10-21 00:00 · planner · created
