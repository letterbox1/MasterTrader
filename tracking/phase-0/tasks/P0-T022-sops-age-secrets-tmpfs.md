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
tools: [sops, age, docker, uv]
mcp: []
env: []
services: []
branch: p0/P0-T022-sops-age-secrets-tmpfs
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T022 · Wire sops + age secrets into tmpfs with per-service scoping

## Goal / expected outcome

One sops/age-encrypted secrets file on the host (`~/.config/mastertrader/secrets.sops.yaml`, **outside the repo**) is decrypted at stack start into per-service tmpfs files (`/run/secrets/<service>/<name>`), so each container sees only its own secrets, nothing secret is in git, env files or images, and key-age metadata feeds the 90-day rotation alert.

## Context & references

- [Roadmap P0 R0.N1](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.43](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [07 §2 secrets](../../../docs/07-security-notes.md#2-secrets)
- [02 §5.1 stores](../../../docs/02-v1-architecture.md#51-stores) (Secrets row: encrypted copy off-site)
- Related: P0-T003 (YubiKey recipients, added later to `infra/secrets/recipients.txt`), P0-T013 (offline file), P0-T061 (rotation runbook)
- File location decided in [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P0-B018): outside the repo (e.g. `~/.config/mastertrader/`), backed up by restic.
- Depends on: P0-T020, P0-T017. Build first, keys last: built and tested with a throwaway age identity in `tests/fixtures/age/`; the hardware-key recipients from P0-T003 are a config change, not a code change.

## Requirements

- Repo holds only `infra/secrets/.sops.yaml` (creation rules generated from `infra/secrets/recipients.txt`: host + offline recipients; CI uses a test recipient) and `infra/secrets/secrets.example.yaml` (key names, no values). The real file is `~/.config/mastertrader/secrets.sops.yaml` (owner-only 0600; path configurable via `MT_SECRETS_FILE`) with an encrypted copy off-site via restic (P0-T039).
- Layout: top-level key per service (`postgres`, `mt_api`, `litellm`, `llm_local`, `pgbackrest`, `restic`, `worm_seal`, `telegram`, `grafana`, `alertmanager`, `discord`, `data_keys`, `venues`); each leaf has `value`, `created` (date), optional `rotate_days` (default 90 for venue keys, [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl); configurable).
- `infra/scripts/secrets-up.sh` (systemd unit `mt-secrets.service`, ordered before compose): decrypts with the host identity, writes each service's leaves to `/run/secrets/<service>/<name>` (tmpfs, 0400, owned by the container uid) and writes `/run/secrets/_meta/key_age.prom` (names + ages, **no values**) for node_exporter's textfile collector.
- Compose mounts only `/run/secrets/<service>` into each service (read-only). Services read secrets via `mt_core.config` file sources (P0-T017) or `*_FILE` conventions for third-party images.
- `worm_owner` is **never** in this file (lint check).
- Grafana alert: any key older than its `rotate_days` (default 90 days; 07 §2, 16 §2.3).

## ToDo

- [ ] Write `.sops.yaml` creation rules and `secrets.example.yaml`.
- [ ] Write `secrets-up.sh` + `secrets-down.sh` (wipes tmpfs) and the systemd unit ordering.
- [ ] Update compose so each service mounts only its own folder (`POSTGRES_PASSWORD_FILE`, `GF_SECURITY_ADMIN_PASSWORD__FILE`, …).
- [ ] Add `infra/scripts/secrets-lint.py`: example keys ⊇ compose references; no `worm_owner`; no plaintext secret patterns in compose/env.
- [ ] Emit `key_age.prom` and document it for P0-T045.
- [ ] Document in `infra/secrets/README.md` how the USER tasks (P0-T002, P0-T006, P0-T007, …) add their own values with `sops` (typed by the user, never by an agent).

## Verification

### Tests
- Unit: `secrets-lint.py` fails on a fixture with a `worm_owner` key or an unreferenced secret.
- Integration: the mt-api container sees only `/run/secrets/mt_api`; litellm cannot read postgres secrets.
- gitleaks full-history scan: no decrypted file ever committed.

### Scenarios
- Given the host reboots, when `mt-secrets.service` runs, then tmpfs secrets exist before containers start and vanish after `secrets-down` or power off.
- Given the host age identity is unavailable (YubiKey removed), when the stack starts, then services fail closed with 'secret missing' and an alert fires.

### Stress / failure injection
- Restart the whole stack 10 times; tmpfs files recreated each time with correct ownership; no secret appears in `docker inspect` env.

## Acceptance criteria

- [ ] No secret in git (gitleaks full-history clean)
- [ ] Each container sees only its own secrets (tested)
- [ ] `key_age.prom` exported without values
- [ ] `docker inspect` of every container shows no secret values in `Env`
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

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
