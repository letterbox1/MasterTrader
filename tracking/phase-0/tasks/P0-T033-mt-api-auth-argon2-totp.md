---
id: P0-T033
kind: task
title: Wire Supabase Auth into mt-api: JWT (JWKS) verification, aal2 for commands, TOTP re-auth
phase: 0
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T032, P0-T031, P0-T070]
requirements: [R0.08]
roadmap_todos: [T0.24, T0.12]
modules: [mt-api, supabase]
dashboards: []
tools: [git, cargo, supabase, docker]
mcp: []
env: []
services: [supabase-postgres, supabase-auth, nats]
branch: p0/P0-T033-mt-api-auth-argon2-totp
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/README.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T033 · Wire Supabase Auth into mt-api: JWT (JWKS) verification, aal2 for commands, TOTP re-auth

## Goal / expected outcome

Single-user login works end to end on **Supabase Auth** instead of a hand-built login ([18 §4.6](../../../docs/18-platform-and-deployment.md#46-auth)): your one account with password + **TOTP MFA** (enrolment required, sign-ups off, P0-T070). `mt-api` verifies the Supabase JWT against the JWKS (asymmetric signing keys), accepts only the configured owner, requires assurance level **`aal2`** for every command, derives the C2 "re-authenticated within 12 h" check from the token, and records every auth event in `audit.auth_event`. Scoped tokens for Telegram/MCP and short-lived command sessions exist as a model (issued later).

## Context & references

- [Roadmap P0 R0.08](../../../docs/roadmap/phase-0-foundations.md#3-requirements) · [T0.24, T0.12](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [18 §4.6 auth](../../../docs/18-platform-and-deployment.md#46-auth) · [16 §2.14](../../../docs/16-configuration-and-safety-model.md#214-platform--operations) (session limits)
- [02 §7 API contract](../../../docs/02-v1-architecture.md#7-api-contract-mt-api) (Transport and auth) · [02 §7.2 commands](../../../docs/02-v1-architecture.md#72-commands-rest-write)
- [ui §3.6 sessions](../../../docs/ui/README.md#36-permissions--sessions) · [07 §6 application controls](../../../docs/07-security-notes.md#6-application-controls)
- USER step: P0-T062 (create your login and enrol TOTP; tests use a seeded test account, so nothing here waits on it)
- Depends on: P0-T032, P0-T031, P0-T070

## Requirements

- **Verification** (`mt_api::auth`): `Authorization: Bearer <access JWT>`; keys from the Supabase JWKS endpoint (cached, refreshed on unknown `kid`, bounded refresh rate); checks `iss`, `aud = authenticated`, `exp`/`nbf` with ≤ 30 s leeway, `role = authenticated`, and `sub` equals the configured owner user id (`auth.owner_user_id` setting); any other user → 403.
- **Assurance level:** every command route requires `aal = aal2`; an `aal1` token reaches only `GET /auth/session` (so the UI can send you to the TOTP step) and the health probes. Reads require `aal2` too.
- **C2 freshness:** C2 commands require the most recent `totp` entry in the token's `amr` claim to be within `auth.c2_reauth_h` (default 12 h, 02 §7.2, [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P0-B003); otherwise 401 problem+json `reauth_required` and the web app runs a Supabase MFA challenge/verify step-up to get a fresh token. `GET /auth/session` returns who, token expiry, `aal`, TOTP status and `last_reauth_at` for D16 Security.
- **Supabase Auth settings** (in `supabase/config.toml`, P0-T070; values from [16 §2.14](../../../docs/16-configuration-and-safety-model.md#214-platform--operations), not literals): sign-ups off; TOTP enrolment required; access-token lifetime and refresh-token reuse interval; Auth rate limits for sign-in and MFA verify set to the 16 lockout defaults (5 failures / 15 min) where Supabase exposes them (U: map each knob; anything Supabase can't express is enforced by `mt-api` watching the Auth audit log and raising `alert.warn.auth_lockout` on NATS).
- **Owner account creation:** `mtctl auth create-owner --email …` (workstation only, uses the `service_role` key from tmpfs, never exposed elsewhere) creates the single user without a password and prints a one-time set-password link valid 30 min to the console; P0-T062 is you completing it and enrolling TOTP. CI/tests use a seeded test user with a TOTP secret in fixtures.
- **Audit:** `audit.auth_event` rows for login/MFA verify/step-up/logout/denied token/lockout, written by `mt-api` from what it observes and from the Auth audit log; never passwords, TOTP codes, secrets or JWTs.
- **Break-glass:** `mtctl` logs in with password + TOTP through the Auth API (gets an `aal2` token) before `mtctl approve` (P0-T035); no separate TOTP store.
- **Scoped tokens and command sessions:** `ops.api_token` (purpose `telegram|mcp`, scopes, secret stored as HMAC-SHA-256 with a server pepper, expiry, last-used, client identity; [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8), 17 §A P8-B004) and `ops.command_session` (Telegram `initData`-verified, TOTP-checked, `aal2`-equivalent, default 15 min, 18 §4.6) — model + verification code only; issuing comes in P2/P8.
- Lost TOTP device: enrol a second TOTP factor on another device at setup (recommended); reset only via `mtctl auth reset-mfa` on the workstation (admin API), audited `source=system`.

## ToDo

- [ ] Implement JWKS fetch/cache, JWT verification, owner check and the `aal2` extractor for axum routes.
- [ ] Implement the C2 freshness check from `amr`, `GET /auth/session`, and the `reauth_required` problem type.
- [ ] Map the 16 §2.14 session and lockout defaults onto `supabase/config.toml` (record which knobs exist) and implement the `mt-api` fallback watcher + NATS alert.
- [ ] Implement `mtctl auth create-owner` / `reset-mfa` and the seeded test user for CI.
- [ ] Migrations for `ops.api_token` and `ops.command_session` models; write all `audit.auth_event` rows.
- [ ] Tests below; hand P0-T062 the exact steps.

## Verification

### Tests
- `cargo test -p mt-api auth`: forged signature, wrong `iss`/`aud`, expired token, unknown `kid`, other `sub` → 401/403; JWKS rotation picked up.
- Integration (Supabase CLI stack, seeded test user): password-only login yields `aal1` → command routes 403, `/auth/session` works; after TOTP verify (`aal2`) commands pass; sign-up attempt fails.
- Integration: a token whose TOTP `amr` entry is 13 h old (time-shifted test clock) gets `reauth_required` on a C2 command; after step-up it passes.

### Scenarios
- Given a valid password but a wrong TOTP code, then Supabase refuses the MFA verify, the token stays `aal1`, and an `auth_event` is written.
- Given repeated failures beyond the 16 §2.14 threshold, then further attempts are refused for the lockout period and `alert.warn.auth_lockout` fires.
- Given 12 h since the last TOTP, when you trigger a C2 action, then the UI asks for a TOTP code and retries.

### Stress / failure injection
- Brute-force simulation: 1,000 login attempts/min from a script → rate limits hold, no successful login, `mt-api` CPU unaffected (verification is local, JWKS cached).
- Supabase Auth container stopped: existing `aal2` tokens keep working until expiry; new logins fail with a clear message; `/system/ready` reports `auth: down`.

## Acceptance criteria

- [ ] Login (password + TOTP) → `aal2` token → command accepted, in an integration test
- [ ] `aal1`, wrong-user, forged and expired tokens refused (tested)
- [ ] C2 freshness from `amr` enforced; session limits and lockout come from 16 §2.14 settings
- [ ] Sign-ups off; owner creation via `mtctl` only
- [ ] All auth events audited without secrets
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, `supabase test db`, gitleaks, `pit` check)

## Exceptions & edge cases

- Passkeys as an MFA factor: not assumed (U, 18 §4.6); revisit when Supabase supports them.
- Clock skew > 30 s breaks TOTP and token checks: chrony keeps it < 50 ms (P0-T019); the error message says 'check device time'.
- Telegram can't carry a Supabase session; its command session is P2 work on the model built here.

## Cardinal rules (do NOT)

- Do NOT log or audit passwords, TOTP secrets, codes, refresh tokens or JWTs.
- Do NOT accept `aal1` tokens for any command, and do NOT add a password-only path or a 'remember me' that skips TOTP.
- Do NOT enable sign-ups or ship the `service_role` key to the browser.
- Do NOT build a second password/TOTP store next to Supabase Auth.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Loosening risk, autonomous mode and mandates are C3 (Telegram + TOTP + cool-down); Kill ON and protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7 and `docs/18-platform-and-deployment.md` §4.6: document the JWT checks, `aal2` rule, `amr`-based C2 freshness and owner creation; `docs/ui/README.md` §3.6: session lifetime as configured in Supabase Auth.
- `docs/roadmap/phase-0-foundations.md`: tick T0.24, T0.12 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T033-mt-api-auth-argon2-totp`
- PR title: `P0-T033: Wire Supabase Auth into mt-api (JWT/JWKS, aal2 for commands, TOTP re-auth)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T033` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (re-auth endpoint for the C2 12 h rule (17 §D P0-B003), token hashing per 16 §2.12, break-glass CLI renamed mtctl, lockout values as settings; run fields added)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (hand-built Argon2 + TOTP + cookie sessions → Supabase Auth (password + TOTP MFA, sign-ups off); `mt-api` verifies JWTs via JWKS, owner-only, `aal2` for commands, C2 freshness from `amr`; owner created by `mtctl`; depends on P0-T070)
