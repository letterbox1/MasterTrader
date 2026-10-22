---
id: P4-T006
kind: task
title: Encrypt the Telethon session and store the Discord bot token
phase: 4
type: OPS
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T022]
requirements: [R4.02, R4.04]
roadmap_todos: [T4.42]
modules: [M2]
dashboards: [D16]
tools: [docker, sops, age, uv, git]
mcp: []
env: []
services: [postgres, nats]
branch: p4/P4-T006-telethon-discord-secrets
pr: ""
doc_sync: [docs/07-security-notes.md, docs/runbooks/social-accounts.md, docs/roadmap/phase-4-intel.md]
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

# P4-T006 · Encrypt the Telethon session and store the Discord bot token

## Goal / expected outcome

The Telethon `.session` file is created once interactively, encrypted with sops/age and decrypted into tmpfs only for `ingest-text`; the Discord bot token, Telegram `api_id`/`api_hash` and Bot API token are scoped to `ingest-text` only. No social credential exists on disk in plaintext or in git. This task builds and tests the mechanism with a fake session and fake tokens; you run the real login yourself in P4-T001 (keys last).

## Context & references

- Roadmap: [R4.02, R4.04](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.42](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Security: [07 §2](../../../docs/07-security-notes.md#2-secrets) (sops + age → tmpfs, per-service scoping) · [07 §10](../../../docs/07-security-notes.md#10-social--scraping-accounts) (encrypted session file, 2FA password)
- Cross-phase: P0-T022 (T0.43: sops/age → per-service tmpfs `/run/secrets/<service>/<name>`) is a `depends_on` entry. The real Telegram/Discord credentials (P0-T002, P0-T008) are only needed by P4-T001 and P4-T068.
- Decision: the secrets file lives **outside the repo** ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P0-B018, [07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Requirements

- Session bootstrap script `ops/scripts/telethon_login.py` runs once on the host (phone code + 2FA password typed by you), writes the session to tmpfs, then `sops --encrypt` to `/etc/mastertrader/telethon.session.sops` (outside the repo, next to the main secrets file, backed up by restic).
- At stack start `infra/scripts/secrets-up.sh` (P0-T022) decrypts it to `/run/secrets/ingest-text/telethon.session` (tmpfs, mode 0400, uid of the service).
- Secrets scoped per service: only `ingest-text` gets `telegram.*` and `discord.bot_token`; `telegram-bot` keeps its own alerts token.
- Session file never leaves tmpfs unencrypted; on shutdown the tmpfs copy is gone.

## ToDo

- [ ] Write `ops/scripts/telethon_login.py` (interactive, prints no secrets).
- [ ] Add the sops creation rule for `/etc/mastertrader/telethon.session.sops` to `infra/secrets/.sops.yaml` and its decrypt step to `infra/scripts/secrets-up.sh` (scope `ingest-text`).
- [ ] Add `discord.bot_token`, `telegram.api_id`, `telegram.api_hash`, `telegram.ingest_bot_token` key names to `infra/secrets/secrets.example.yaml` (names only) and the `ingest-text` scope.
- [ ] Add gitleaks custom rules for Telethon session strings and Discord token format.
- [ ] Document the bootstrap + rotation in `docs/runbooks/social-accounts.md`.

## Verification

### Tests
- Integration: container starts with the session in tmpfs; `stat` shows mode 0400 and tmpfs mount.
- Unit: secrets loader refuses to start `ingest-text` if the session is world-readable.
- CI: gitleaks catches a planted fake session string and fake Discord token.

### Scenarios
- Given the session is revoked from the phone, when `ingest-text` starts, then Telegram ingest goes `degraded` with an alert and other sources keep running.
- Given another service (e.g. `nlp`) inspects its env/tmpfs, then no Telegram/Discord secret is visible.

### Stress / failure injection
- Restart `ingest-text` 20× in a loop: session decrypts every time; no plaintext copy appears on persistent disk (`find / -name '*.session'` outside tmpfs is empty).

## Acceptance criteria

- [ ] Encrypted-session path proven end to end with a fake session (the real session is created by you in P4-T001 and never committed); plaintext never written to persistent disk
- [ ] Only `ingest-text` can read Telegram/Discord secrets (per-service scope test)
- [ ] Runbook written
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Telethon is archived on GitHub (moved to Codeberg): pin the version; session format changes on upgrade need a re-login (runbook step).

## Cardinal rules (do NOT)

- Do NOT run the login script in CI or on any machine other than the host.
- Do NOT log phone numbers or codes.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT use unpinned images (`:latest`) or vendored code with telemetry/referral IDs; pin by digest.

## Doc sync on completion

- `docs/07-security-notes.md`: §10: reference the session bootstrap runbook
- `docs/runbooks/social-accounts.md`: new runbook (bootstrap, rotation, revocation)
- `docs/roadmap/phase-4-intel.md`: tick T4.42 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T006-telethon-discord-secrets`
- PR title: `P4-T006: Encrypt the Telethon session and store the Discord bot token`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T006` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (secrets outside the repo per 17 §D (P0-B018) and P0-T022 paths; keys last: built with fake session/tokens, real login in P4-T001; depends on P0-T022)
