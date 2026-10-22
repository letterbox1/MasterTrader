---
id: P0-T065
kind: task
title: Deploy the restricted docker-proxy for allow-listed service restarts
phase: 0
type: OPS
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T021, P0-T034]
requirements: [R0.14, R0.02]
roadmap_todos: [T0.47, T0.41]
modules: [ops, mt_api]
dashboards: [D16]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [docker-proxy, mt-api, postgres, nats]
branch: p0/P0-T065-docker-proxy-restart-allow-list
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/07-security-notes.md, docs/ui/dashboards/D16-system.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T065 · Deploy the restricted docker-proxy for allow-listed service restarts

## Goal / expected outcome

A digest-pinned `docker-proxy` container sits on the internal `ctl` network and is the **only** holder of the Docker socket. It allows exactly two Docker API calls: list containers (for status) and `POST /containers/{name}/restart` for containers on a configurable allow-list. `system.service.restart` (C2) in mt-api goes through it, so D16 can restart allow-listed services while mt-api never mounts the Docker socket (R0.14, [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P0-B012).

## Context & references

- Roadmap: [R0.14 · T0.47](../../../docs/roadmap/phase-0-foundations.md#3-requirements) (also part of the T0.41 compose list)
- Architecture: [02 §3.1 networks](../../../docs/02-v1-architecture.md#31-networks) (`ctl`: mt-api + docker-proxy only), [02 §3.2 containers](../../../docs/02-v1-architecture.md#32-containers) (`docker-proxy` row), [02 §7.2 commands](../../../docs/02-v1-architecture.md#72-commands-rest-write) (`system.service.restart` C2, allow-listed containers only)
- Security: [07 §5–§6](../../../docs/07-security-notes.md#5-network--host) ("No Docker socket in app containers")
- Dashboard: [D16 System](../../../docs/ui/dashboards/D16-system.md) (Restart service action: C2, shows dependents; non-allow-listed buttons disabled)
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P0-B012 (closed)
- Related: P0-T021 (creates the `ctl` network), P0-T034 (registers `system.service.restart` with a 501 stub that this task replaces), P0-T046 (`restartable` flag), P0-T051 (D16 button), P0-T067 (refusal test)
- Depends on: P0-T021, P0-T034

## Requirements

- Functional:
  - Image: a socket proxy that supports **path allow-lists** (e.g. `wollomatic/socket-proxy` with `-allowGET`/`-allowPOST` regexes; (U) verify licence, no telemetry, and that it rejects everything not allow-listed), pinned by digest in `infra/images.lock`, recorded in `third_party/LICENSES.md` if vendored.
  - Only `docker-proxy` mounts `/var/run/docker.sock`. It joins `ctl` (`internal: true`) only; no published port, no other network.
  - Allowed calls: `GET /containers/json` (status for D16) and `POST /containers/{name}/restart` where `{name}` is in the allow-list; every other method/path → 403 at the proxy.
  - Allow-list is configuration, not code: `infra/docker-proxy/allowlist.yaml`, loaded as a setting (default: `caddy`, `prefect-worker`, `mlflow`, `litellm`, `tei-embed`, `tei-rerank`, `llm-local`, `grafana`, `loki`, `prometheus`, `vector`, `alertmanager`). `postgres`, `nats`, `mt-api` and `docker-proxy` itself are never on it by default ([16 §2.14](../../../docs/16-configuration-and-safety-model.md#214-platform--operations)). Adding a container is a loosening (C3 via `system.settings.update`); removing one is C1.
  - mt-api handler for `system.service.restart` (C2): validates the name against the allow-list **before** calling the proxy; non-allow-listed → 403 problem+json `not_restartable` and an `audit.command` row `rejected`; allow-listed → preview lists dependents (from compose `depends_on`), then restart via the proxy, wait for health, audit `applied` (or `failed` with the reason).
  - `/system/services` returns `restartable: true|false` per container from the allow-list (consumed by P0-T046/P0-T051).
- Non-functional:
  - Restart call timeout 60 s; one restart per container at a time (409 if one is in flight).
  - Proxy logs every request (method, path, decision) to Loki via Vector; no secrets in logs.
- Tools & access: listed in the front matter (`tools`, `mcp`, `env` names, `services`); `./kanban preflight P0-T065` checks them before start. No secrets needed.

## ToDo

- [ ] Choose and pin the proxy image; record the (U) checks (licence, telemetry, deny-by-default) in the PR.
- [ ] Add the `docker-proxy` service to `infra/docker-compose.yml` on `ctl` only, with the socket mount and the allow-list regexes generated from `allowlist.yaml`.
- [ ] Add `allowlist.yaml` + its settings loader and the tighten C1 / loosen C3 classification for changes.
- [ ] Replace the P0-T034 501 stub with the real `system.service.restart` handler (allow-list check, dependents preview, restart, health wait, audit).
- [ ] Add `restartable` to `/system/services`.
- [ ] Extend the compose lint (P0-T020): fail if any service other than `docker-proxy` mounts the Docker socket or if anything but mt-api/docker-proxy joins `ctl`.
- [ ] Write tests (see Verification); the adversarial refusal suite is P0-T067.
- [ ] Update docs listed under Doc sync.

## Verification

### Tests
- Unit: allow-list loader; name validation; C1/C3 classification of allow-list edits.
- Integration (compose in CI): restart `llm-local` via `POST /api/v1/commands/system.service.restart` → container restarted, healthy again, `audit.command` accepted + applied rows.
- Integration: restart `postgres` → 403 `not_restartable`, `audit.command` `rejected`, no Docker call made (proxy log empty for that request).
- Lint: a fixture compose that mounts the socket into `mt-api` fails the compose lint.

### Scenarios
- Given LiteLLM is wedged, when you press Restart on D16 and confirm (C2), then only `litellm` restarts and the audit trail shows who, when and why.
- Given mt-api is compromised, when it calls the proxy to create or exec into a container, then the proxy returns 403 (only list + allow-listed restart exist).
- Given you add `postgres` to the allow-list, then the change is C3 (break-glass approval + TOTP + cool-down in P0).

### Stress / failure injection
- docker-proxy stopped: restart commands fail fast with 503 problem+json and an audit `failed` row; D16 shows the restart path as unavailable; nothing else is affected.
- Two concurrent restarts of the same container → one runs, the other gets 409.

## Acceptance criteria

- [ ] `docker-proxy` is the only container with the Docker socket; it's on `ctl` only (compose dump attached)
- [ ] Allow-listed restart works end to end with C2 and audit rows
- [ ] Non-allow-listed restart refused by mt-api (403 + audit) and by the proxy (403)
- [ ] Allow-list is a setting (loosen C3, tighten C1), not a code constant
- [ ] Compose lint enforces "no socket outside docker-proxy" and `ctl` membership
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- A container that fails its health check after restart: the command reports `failed` with the last health output; no automatic second restart.
- Restarting `caddy` drops the web session briefly; the UI re-connects (WS snapshot on re-subscribe).
- Engine restarts (P2) must warn about open positions (D16); P2 extends the preview, not this proxy.

## Cardinal rules (do NOT)

- Do NOT mount the Docker socket into mt-api or any app container.
- Do NOT allow any Docker API beyond container list and allow-listed restart (no create, exec, pull, stop, kill, volumes, networks).
- Do NOT hard-code the allow-list; it's a setting, and loosening it is C3.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/02-v1-architecture.md` §3.2: record the proxy image and the allowed API paths.
- `docs/07-security-notes.md` §5–§6: link the allow-list file and the compose lint rule.
- `docs/ui/dashboards/D16-system.md`: confirm the restart action and the disabled-button rule.
- `docs/roadmap/phase-0-foundations.md`: tick T0.47 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T065-docker-proxy-restart-allow-list`
- PR title: `P0-T065: Deploy the restricted docker-proxy for allow-listed service restarts`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T065` run

## Progress log

- 2026-10-22 02:01 · cloud:vm:be04b6ae61f8 · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (new task for R0.14 / T0.47, decided in 17 §D P0-B012)
