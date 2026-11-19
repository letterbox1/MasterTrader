---
id: P0-T070
kind: task
title: Stand up the local Supabase stack (CLI for tests, self-hosted on the workstation)
phase: 0
type: OPS
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T014]
requirements: [R0.02, R0.03]
roadmap_todos: [T0.41]
modules: [supabase, infra]
dashboards: []
tools: [git, docker, supabase, just, psql]
mcp: []
env: []
services: [supabase-postgres, supabase-auth, supabase-storage]
branch: p0/P0-T070-stand-up-the-local-supabase-stack-cli-for-tests-
pr: ""
doc_sync: [docs/18-platform-and-deployment.md, docs/03-build-spec.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-19
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T070 · Stand up the local Supabase stack (CLI for tests, self-hosted on the workstation)

## Goal / expected outcome

One Supabase configuration runs in two places with the same images and migrations: the **Supabase CLI** stack (`supabase start`) for development, CI and agents, and the **self-hosted Supabase** Docker Compose stack on the always-on workstation ([18 §4.1](../../../docs/18-platform-and-deployment.md#41-where-it-runs)). Both have the required extensions, Auth configured for one user with TOTP MFA and sign-ups off, the Data API and Realtime off for MasterTrader schemas, private Storage buckets, and every port bound to localhost. `just db-reset` and `just db-test` work.

## Context & references

- [Roadmap P0 R0.02, R0.03](../../../docs/roadmap/phase-0-foundations.md#3-requirements) · [T0.41](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [18 §4.1 where it runs](../../../docs/18-platform-and-deployment.md#41-where-it-runs) · [18 §4.2 extensions](../../../docs/18-platform-and-deployment.md#42-extensions) · [18 §4.5 access rules](../../../docs/18-platform-and-deployment.md#45-access-rules) · [18 §4.6 auth](../../../docs/18-platform-and-deployment.md#46-auth)
- [16 §2.15](../../../docs/16-configuration-and-safety-model.md#215-platform-deployment-and-regions) (`db.target`, `supabase.data_api`, `supabase.realtime`)
- [03 §2 target environment](../../../docs/03-build-spec.md#2-target-environment) · [07 §5 network & host](../../../docs/07-security-notes.md#5-network--host)
- Unblocks: P0-T024 (migrations), P0-T033 (Auth), P0-T039 (pgBackRest against the Supabase Postgres container), P0-T015 (`db` CI job), P0-T072
- Related: P0-T020 (the rest of the Compose stack), P0-T021 (networks), P0-T022 (secrets)

## Requirements

- `supabase/config.toml` committed (via `supabase init`): project id `mastertrader`, Postgres major 17, Supabase CLI version pinned (in `infra/images.lock` and CI).
- **Extensions** enabled by the first migration: `vector` (pgvector), `pg_trgm`, `pgcrypto`, `pg_cron`, `pgtap`; `pg_partman` if available on the pinned image (U: record the result here and in 18 §4.2; P0-T072 falls back to the `mt-store` job if not). **No TimescaleDB.**
- **Auth** ([18 §4.6](../../../docs/18-platform-and-deployment.md#46-auth)): email + password only; `enable_signup = false`; TOTP MFA enrolment enabled (`[auth.mfa.totp] enroll_enabled = true, verify_enabled = true`); asymmetric JWT signing keys with the JWKS endpoint `mt-api` reads; short access-token lifetime per [16 §2.14](../../../docs/16-configuration-and-safety-model.md#214-platform--operations). The single user is created by a seed/CLI step for tests (`mt-test@localhost`) and by you on the workstation (P0-T062).
- **Access rules** ([18 §4.5](../../../docs/18-platform-and-deployment.md#45-access-rules)): the Data API (PostgREST) does **not** expose MasterTrader schemas (`[api] schemas = []` or limited to Supabase's own); Realtime off (`supabase.realtime: off`); both are settings, defaults from 16 §2.15. RLS deny-all on every table is enforced by the migrations (P0-T024) and checked by pgTAP.
- **Storage:** private buckets `reports`, `tax-exports`, `attachments` (no public buckets).
- **Self-hosted stack** (`infra/supabase/docker-compose.yml`, from the official self-hosting setup): every image pinned by digest; only the services we need (db, auth, storage, rest kept minimal, meta, studio, kong); Studio and Kong bound to `127.0.0.1`; secrets (JWT keys, DB passwords, `service_role` key) from the sops file via P0-T022, never in the repo; Postgres data on a named volume on NVMe.
- The CLI and self-hosted stacks use the same Postgres image digest and the same `supabase/migrations/`; a drift check compares versions.
- `justfile`: `db-start` (`supabase start`), `db-reset` (`supabase db reset`), `db-test` (`supabase test db`), `db-up-local` (self-hosted `supabase migration up --db-url …`).
- `service_role` and `worm_owner` credentials are never given to the web app or any browser code.

## ToDo

- [ ] `supabase init`; commit `supabase/config.toml` with Auth, MFA, API and Realtime settings above.
- [ ] Add the extensions migration (`supabase/migrations/<ts>_extensions.sql`) and a pgTAP test that each required extension exists and TimescaleDB does not.
- [ ] Check `pg_partman` on the pinned Postgres 17 image; log the result.
- [ ] Add `infra/supabase/` self-hosted Compose (digest-pinned, localhost-bound) and its env template (`*.example`, no values).
- [ ] Create the private Storage buckets (seed or migration) and the test user seed for CI.
- [ ] Add the `just` recipes and the CLI-vs-self-hosted drift check.
- [ ] Write tests (see Verification); update docs listed under Doc sync.

## Verification

### Tests
- `supabase start && supabase db reset && supabase test db`: pgTAP asserts extensions present, TimescaleDB absent, buckets private.
- Auth: a sign-up request returns an error; the seeded test user can log in, enrol TOTP and reach `aal2` (script using the Auth API).
- Data API: `GET /rest/v1/<any MasterTrader table>` with the anon key is refused (schema not exposed); Realtime subscription to a MasterTrader table is refused.

### Scenarios
- Given a fresh clone, when an agent runs `just db-reset`, then the local stack has every migration applied and `just db-test` passes.
- Given the self-hosted stack on the workstation, when you run `ss -tlnp`, then no Supabase port listens on a non-loopback address.

### Stress / failure injection
- Restart the self-hosted `db` container mid-session: Auth and Storage recover without manual steps; data persists on the volume.

## Acceptance criteria

- [ ] CLI stack and self-hosted stack both start with pinned images and the same migrations
- [ ] Extensions present (pg_partman result logged); no TimescaleDB
- [ ] Sign-ups off, TOTP MFA enabled, JWKS reachable by `mt-api`
- [ ] Data API and Realtime do not expose MasterTrader schemas (tested)
- [ ] Private buckets only; all ports on localhost
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, `supabase test db`, gitleaks, `pit` check)

## Exceptions & edge cases

- `pg_partman` missing on the image: P0-T072 uses the `mt-store` partition job on pg_cron; note it in 18 §4.2.
- Supabase CLI and self-hosted versions drift: the drift check fails CI; bump both together after review (supply chain rule).
- Passkeys as an MFA factor are not assumed (U in 18 §4.6); TOTP is the factor.

## Cardinal rules (do NOT)

- Do NOT expose MasterTrader schemas through the Data API or Realtime, and do NOT add RLS policies for `anon`/`authenticated`.
- Do NOT put the `service_role` key, JWT secret or DB passwords in the repo or the web bundle.
- Do NOT enable sign-ups.
- Do NOT bind Studio, Kong or Postgres to a non-loopback address.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/18-platform-and-deployment.md` §4.1–4.2: record the pinned versions and the pg_partman result (remove the (U)).
- `docs/03-build-spec.md` §3: `supabase/` contents as built.
- `docs/roadmap/phase-0-foundations.md`: tick T0.41 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T070-stand-up-the-local-supabase-stack-cli-for-tests-`
- PR title: `P0-T070: Stand up the local Supabase stack (CLI for tests, self-hosted on the workstation)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T070` run

## Progress log

- 2026-11-19 00:00 · aligner · created
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (new task: the Supabase CLI + self-hosted stack, extensions per 18 §4.2, Auth with TOTP MFA and sign-ups off, Data API/Realtime off, private Storage buckets)
