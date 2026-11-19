---
id: P0-T017
kind: task
title: Implement mt-core config, clock and ID helpers (Rust)
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
modules: [mt-core]
dashboards: []
tools: [git, cargo]
mcp: []
env: []
services: []
branch: p0/P0-T017-mt-core-config-clock
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T017 · Implement mt-core config, clock and ID helpers (Rust)

## Goal / expected outcome

Services load typed settings from files + environment where secrets come only from tmpfs-mounted files, and all code reads time through an injectable `Clock` (system, frozen or simulated) so tests and backtests are deterministic. Rust services use `mt_core::config` / `mt_core::clock` directly; Python packages get the same clock and defaults loader through the `mt_store` module (P0-T071).

## Context & references

- [Roadmap P0 T0.21](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-core`: config, clock)
- [02 §5.2 key conventions](../../../docs/02-v1-architecture.md#52-key-conventions)
- [07 §2 secrets](../../../docs/07-security-notes.md#2-secrets)
- Related: P0-T022 (tmpfs layout `/run/secrets/<service>/<name>`)
- Depends on: P0-T014

## Requirements

- `mt_core::config::Settings` per service (serde + `figment` or `config`): layered defaults file → service file → env; secret fields typed `secrecy::SecretString`, read from `/run/secrets/<service>/<name>`; with `MT_ENV=prod`, env-provided secrets are refused.
- `Clock` trait with `now_utc()`, `monotonic_ns()`; `SystemClock`, `FrozenClock`, `SimClock`. A clippy `disallowed-methods` rule forbids `SystemTime::now`, `Utc::now`, `OffsetDateTime::now_utc` outside `mt_core::clock`; the ruff banned-api rule does the same for Python (`datetime.now`, `time.time`).
- Display timezone default `Australia/Sydney`; storage always UTC.
- `Debug`/`Display` of settings redacts every secret.
- **Defaults, not literals:** the [16](../../../docs/16-configuration-and-safety-model.md) values P0 uses (C3 cool-down 15 min and C2 re-auth 12 h (§2.3), LLM budgets (§2.10), WORM integrity action `block_new_entries` and chain-check cadence (§2.11), NATS WORM buffer 1 GB / 24 h / 80 % (§3.3), key rotation 90 days (§2.3), platform settings `deploy.mode`, `db.target`, `supabase.data_api`, `supabase.realtime`, `web.host`, `api.exposure`, `models.gpu_profile`, `secrets.age_identity_store` (§2.15)) live in one typed, versioned defaults file `infra/config/defaults.yaml` loaded by `mt_core::config::defaults`; services read the effective value from settings and never hard-code it.

## ToDo

- [ ] Implement the Settings layering with a file-secret source and the prod guard.
- [ ] Implement Clock variants and the clippy/ruff banned-method configs.
- [ ] Add `infra/config/defaults.yaml` + the typed loader for the P0 defaults from 16, each with its 16 section reference.
- [ ] Tests for redaction, prod guard, defaults loading and clock behaviour.

## Verification

### Tests
- `cargo test -p mt-core config clock`: secret from file loads; env secret refused when `MT_ENV=prod`; `format!("{:?}", settings)` never contains the secret.
- `FrozenClock` stable; `SimClock::advance(5s)` works.
- A test fails if a 16 default used in P0 is duplicated as a literal in P0 crates (grep-based guard).

### Scenarios
- Given a secret file is missing, when the service starts, then it exits non-zero naming the secret (not its value).

### Stress / failure injection
- n/a: library code.

## Acceptance criteria

- [ ] Settings + Clock implemented with tests
- [ ] Banned-method rules active (clippy and ruff) and passing
- [ ] P0 defaults load from `infra/config/defaults.yaml`; the literal-duplication guard passes
- [ ] No secret appears in any log or `Debug` output (tested)
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Clock skew: the system clock is chrony-synced (P0-T019); `Clock` doesn't correct skew; M16 monitors it (P1).

## Cardinal rules (do NOT)

- Do NOT read secrets from environment variables in production.
- Do NOT read the system time directly outside `mt_core::clock`.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- None beyond the roadmap tick.
- `docs/roadmap/phase-0-foundations.md`: tick T0.21 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T017-mt-core-config-clock`
- PR title: `P0-T017: Implement mt-core config, clock and ID helpers`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T017` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (one defaults file for the 16 values P0 uses (nothing hard-coded); run fields added)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (Rust `mt_core::config`/`clock` with `secrecy` and clippy disallowed-methods replace pydantic-settings; 16 §2.15 platform settings added to the defaults file)
