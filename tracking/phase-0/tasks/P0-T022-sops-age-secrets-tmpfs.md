---
id: P0-T022
kind: task
title: Wire sops + age secrets into tmpfs with per-service scoping
phase: 0
type: OPS
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T020, P0-T017]
requirements: [R0.N1]
roadmap_todos: [T0.43]
modules: [ops]
dashboards: []
tools: [sops, age, docker, just]
mcp: []
env: []
services: []
branch: p0/P0-T022-sops-age-secrets-tmpfs
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T022 · Wire sops + age secrets into tmpfs with per-service scoping

## Goal / expected outcome

You fill one plain file, `.env` (copied from the repo's `.env.example`, git-ignored), service by service. `just secrets-seal` encrypts it with sops/age into `~/.config/mastertrader/secrets.sops.env` (**outside the repo**, dotenv format, the same names) and shreds the plaintext. At stack start it's decrypted into per-service tmpfs files (`/run/secrets/<service>/<NAME>`), so each container sees only its own names. Nothing secret is in git or images, agents only ever see names (`just secrets-check`), and key-age metadata feeds the 90-day rotation alert.

## Context & references

- [Roadmap P0 R0.N1](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.43](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [07 §2 secrets](../../../docs/07-security-notes.md#2-secrets)
- [02 §5.1 stores](../../../docs/02-v1-architecture.md#51-stores) (Secrets row: encrypted copy off-site)
- [18 §8](../../../docs/18-platform-and-deployment.md#8-tailscale-and-the-hardware-key-per-mode) and [16 §2.15](../../../docs/16-configuration-and-safety-model.md#215-platform-deployment-and-regions) (`secrets.age_identity_store: keychain` until P7)
- Related: P7-T072 (YubiKey recipients before live money), P0-T013 (offline file), P0-T061 (rotation runbook)
- File location decided in [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P0-B018): outside the repo (e.g. `~/.config/mastertrader/`), backed up by restic.
- Depends on: P0-T020, P0-T017. Build first, keys last: built and tested with a throwaway age identity in `tests/fixtures/age/`; the age identities live in the OS keychain (or a passphrase-protected age file) until the YubiKey move in P7-T072, which is a config change, not a code change.

## Requirements

- **One list of names:** `.env.example` at the repo root is the canonical catalogue of every secret and per-user value from P0 to P8, named `<SERVICE>_<ENVIRONMENT>_<ROLE>_<FIELD>` ([07 §2](../../../docs/07-security-notes.md#2-secrets)); `docs/ENV-SETUP.md` has the setup steps per block. `MT_*` names are generated, `VITE_*` names are public build values.
- `.gitignore`: `.env` and `.env.*` ignored, `!.env.example` kept; gitleaks (P0-T014) also blocks any `.env` content pattern.
- `just secrets-init`: creates the age identities (host + offline) stored per `secrets.age_identity_store` (default `keychain`) and writes `infra/secrets/.sops.yaml` creation rules from `infra/secrets/recipients.txt` (CI uses a test recipient).
- `just secrets-generate`: fills every blank `MT_*` name in `.env` with strong random values (lengths per kind) and lists the ★ ones you must copy to your password manager (restic, pgBackRest cipher, journal key, MCP pepper).
- `just secrets-seal [--merge]`: validates `.env` (unknown names rejected with the closest valid name; values trimmed; no `VITE_*` that looks like a secret), encrypts to `~/.config/mastertrader/secrets.sops.env` (0600; path via `MT_SECRETS_FILE`), adds a `<NAME>__CREATED=YYYY-MM-DD` line per changed value for rotation, verifies the round trip, then shreds `.env`. `--merge` adds or replaces only the names present. `just secrets-edit` opens the sealed file with `sops`.
- `just secrets-check [--for <task-id>]`: prints set/missing per name (never values); `./kanban preflight` uses it to decide whether a live VERIFY task's `env` names are present.
- `infra/secrets/scopes.yaml`: service → names it may read. `infra/scripts/secrets-up.sh` (run by `just up`; optional systemd user unit before compose) decrypts with the host identity, writes each service's names to `/run/secrets/<service>/<NAME>` (tmpfs, 0400, owned by the container uid) and `/run/secrets/_meta/key_age.prom` (names + ages, **no values**).
- Compose mounts only `/run/secrets/<service>` read-only. Rust services read via `mt_core::config` file sources (P0-T017), Python via the same layout, third-party images via `*_FILE` variables.
- `worm_owner`, wallet seeds and private keys are **never** in `.env` or the sealed file (lint check rejects names and value patterns that look like seeds or private keys).
- Grafana alert: any `*__CREATED` older than its `rotate_days` (default 90 days for venue keys; 07 §2, 16 §2.3).

## ToDo

- [ ] `.gitignore` rule set (`.env`, `.env.*`, `!.env.example`) and a test that `git check-ignore .env` passes and `.env.example` is tracked.
- [ ] `just secrets-init`, `secrets-generate`, `secrets-seal [--merge]`, `secrets-edit`, `secrets-check` (Rust CLI in `mt-core` or a small script; no value ever printed).
- [ ] `infra/secrets/scopes.yaml` and `secrets-up.sh` + `secrets-down.sh` (wipes tmpfs) and the systemd unit ordering.
- [ ] Compose: each service mounts only its own folder (Supabase DB/JWT secrets, `GF_SECURITY_ADMIN_PASSWORD__FILE`, …).
- [ ] `infra/scripts/secrets-lint`: every name in `scopes.yaml` and every task `env` name exists in `.env.example`; every `.env.example` name follows the naming convention; no `worm_owner`/seed/private-key names; no plaintext secret patterns in compose.
- [ ] Emit `key_age.prom` and document it for P0-T045.
- [ ] `infra/secrets/README.md`: the five commands above, in the order you use them.

## Verification

### Tests
- Unit: `secrets-lint` fails on a fixture with a `worm_owner` key or an unreferenced secret.
- Integration: the mt-api container sees only `/run/secrets/mt_api`; litellm cannot read the Supabase secrets; the web bundle contains no `service_role` key.
- gitleaks full-history scan: no decrypted file ever committed.

### Scenarios
- Given the workstation reboots, when `just up` (or `mt-secrets.service`) runs, then tmpfs secrets exist before containers start and vanish after `secrets-down` or power off.
- Given the host age identity is unavailable (keychain locked; from P7 the YubiKey removed), when the stack starts, then services fail closed with 'secret missing' and an alert fires.

### Stress / failure injection
- Restart the whole stack 10 times; tmpfs files recreated each time with correct ownership; no secret appears in `docker inspect` env.

## Acceptance criteria

- [ ] No secret in git (gitleaks full-history clean)
- [ ] Each container sees only its own secrets (tested)
- [ ] `key_age.prom` exported without values
- [ ] `docker inspect` of every container shows no secret values in `Env`
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, `supabase test db`, gitleaks, `pit` check)

## Exceptions & edge cases

- Third-party images that only read env vars: wrap with an entrypoint that reads the file inside the container; never put the value in compose.
- OpenBao migration (07 §2 upgrade path) is out of scope until the signer holds more than one hot key (P5).

## Cardinal rules (do NOT)

- Do NOT commit the decrypted file, an `.env` with values, or the age identity.
- Do NOT add `worm_owner` to the runtime file.
- Do NOT pass secrets as build args or bake them into images.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/07-security-notes.md` §2: document the file location (outside git), tmpfs layout and key-age metric.
- `docs/roadmap/phase-0-foundations.md`: tick T0.43 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T022-sops-age-secrets-tmpfs`
- PR title: `P0-T022: Wire sops + age secrets into tmpfs with per-service scoping`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T022` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keyless build with a test age key (no wait on P0-T003); secrets file outside the repo per 17 §D P0-B018; rotation default 90 d (16 §2.3); run fields added)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (Supabase secrets (DB, JWT keys, service_role) added; age identities in the OS keychain until P7-T072 instead of a YubiKey from P0-T003; no systemd/host precondition)
- 2026-11-20 00:00 · main · intake changed to the `.env` flow (17 §G follow-up): `.env.example` is the canonical name catalogue, `.env` is git-ignored and sealed into `secrets.sops.env`; lint checks task env names against it.
