---
id: P0-T033
kind: task
title: Implement single-user auth: Argon2 password, TOTP and sessions
phase: 0
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T032, P0-T031]
requirements: [R0.08]
roadmap_todos: [T0.24, T0.12]
modules: [mt_api]
dashboards: []
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [postgres, nats]
branch: p0/P0-T033-mt-api-auth-argon2-totp
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/README.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T033 · Implement single-user auth: Argon2 password, TOTP and sessions

## Goal / expected outcome

Single-user login works end to end: Argon2id password + RFC 6238 TOTP, first-boot enrolment guarded by a one-time setup token, an `HttpOnly` `SameSite=Strict` session cookie with 12 h idle timeout, lockout on brute force, and every auth event in `audit.auth_event`. Scoped tokens for Telegram/MCP exist as a model (issued later).

## Context & references

- [Roadmap P0 R0.08](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [02 §7 API contract](../../../docs/02-v1-architecture.md#7-api-contract-mt_api) (Transport and auth)
- [ui §3.6 sessions](../../../docs/ui/README.md#36-permissions--sessions)
- [07 §6 application controls](../../../docs/07-security-notes.md#6-application-controls)
- USER step: P0-T062 (enrol on first boot)
- Depends on: P0-T032, P0-T031

## Requirements

- Password hash: Argon2id (`argon2-cffi`), time_cost 3, memory 64 MiB, parallelism 4; min length 14; stored in `ops.credential` (single row).
- First boot: if no credential exists, mt-api prints a **one-time setup token** to its log at startup (only on the host console via `docker logs`), valid 30 min; `POST /auth/setup` requires it, sets the password and returns a TOTP provisioning URI (QR rendered client-side); enrolment completes only after a valid code is submitted.
- TOTP: SHA-1, 6 digits, 30 s step, ±1 step window, **replay protection** (store last accepted counter); 10 single-use recovery codes (Argon2-hashed) shown once.
- Login `POST /auth/login` {password, totp}; on success creates `ops.session` (random 256-bit id, stored hashed), cookie `mt_session`: `HttpOnly; Secure; SameSite=Strict; Path=/`.
- Idle timeout 12 h (configurable, `ops.setting`), absolute lifetime 7 d; re-login needs TOTP (ui §3.6; defaults in [16 §2.14](../../../docs/16-configuration-and-safety-model.md#214-platform--operations)). CSRF: SameSite=Strict + required header `X-MT-CSRF` matching a non-HttpOnly cookie (double submit) on unsafe methods.
- Brute force (defaults in `ops.setting`, configurable, [16 §2.14](../../../docs/16-configuration-and-safety-model.md#214-platform--operations)): 5 failures / 15 min → exponential lockout (15 min doubling, max 24 h) and a `alert.warn.auth_lockout` NATS message; per-IP and global counters.
- Scoped tokens table `ops.api_token` (purpose `telegram|mcp`, scopes, secret stored as HMAC-SHA-256 with a server pepper, expiry, last-used, client identity; [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8), 17 §A P8-B004) — model + verification code only; issuing UI comes in P2/P8.
- `POST /auth/logout`, `GET /auth/session` (who/expiry/TOTP status/`last_reauth_at`) for D16 Security; `POST /auth/reauth` {password, totp} refreshes `last_reauth_at`, which C2 commands require within 12 h (default, configurable; 02 §7.2, [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P0-B003).

## ToDo

- [ ] Implement credential, session, token models + migrations.
- [ ] Implement setup, login, logout, session endpoints and the auth dependency for routes.
- [ ] Implement lockout counters (Postgres-backed) and the NATS alert.
- [ ] Write all `audit.auth_event` rows (no secrets).
- [ ] Tests below; hand P0-T062 the exact steps.

## Verification

### Tests
- Unit: Argon2 params; TOTP window and replay rejection; recovery code single use.
- Integration: setup token expires after 30 min; setup impossible once a credential exists; login → cookie flags exact; CSRF header required for POST.
- Integration: 6th failed login within 15 min locked; lockout doubles.

### Scenarios
- Given a valid password but a TOTP code already used in this window, when logging in, then 401 and an `auth_event` `totp_replay`.
- Given 12 h of inactivity, when the user clicks anything, then 401 → login screen; a C3 action always re-checks the session (ui §3.6).

### Stress / failure injection
- Brute-force simulation: 1,000 login attempts/min from a script → lockout holds, CPU stays < 1 core (Argon2 cost bounded by lockout), no successful login.

## Acceptance criteria

- [ ] Setup → enrol → login → logout works in an integration test
- [ ] Cookie flags and CSRF enforced
- [ ] Lockout + replay protection tested
- [ ] All auth events audited without secrets
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Lost TOTP device: recovery code login forces re-enrolment; with no recovery codes left, reset needs host console (`mtctl reset-totp`, audited `source=system`).
- Clock skew > 30 s breaks TOTP: chrony keeps it < 50 ms (P0-T019); the error message says 'check device time'.

## Cardinal rules (do NOT)

- Do NOT log or audit passwords, TOTP secrets, codes, recovery codes or session ids.
- Do NOT add a password-only login path or 'remember me' that skips TOTP.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Loosening risk, autonomous mode and mandates are C3 (Telegram + TOTP + cool-down); Kill ON and protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7: document the setup-token first-boot flow; `docs/ui/README.md` §3.6: note absolute session lifetime.
- `docs/roadmap/phase-0-foundations.md`: tick T0.24, T0.12 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T033-mt-api-auth-argon2-totp`
- PR title: `P0-T033: Implement single-user auth: Argon2 password, TOTP and sessions`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T033` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (re-auth endpoint for the C2 12 h rule (17 §D P0-B003), token hashing per 16 §2.12, break-glass CLI renamed mtctl, lockout values as settings; run fields added)
