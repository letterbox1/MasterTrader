---
id: P0-T067
kind: task
title: Verify restart refusal outside the docker-proxy allow-list
phase: 0
type: VERIFY
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T065]
requirements: [R0.14]
roadmap_todos: [T0.68]
modules: [ops, mt_api]
dashboards: [D16]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [docker-proxy, mt-api, postgres, nats]
branch: p0/P0-T067-restart-refusal-test
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T067 · Verify restart refusal outside the docker-proxy allow-list

## Goal / expected outcome

An adversarial test suite (`tests/verify/test_restart_refusal.py`, CI + host run) proves R0.14: `system.service.restart` of a container that isn't allow-listed is refused and audited, the proxy itself refuses every Docker API call beyond list + allow-listed restart, and `mt-api` has no Docker socket mounted.

## Context & references

- Roadmap: [R0.14 · T0.68](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [02 §3.1 networks](../../../docs/02-v1-architecture.md#31-networks) (`ctl`), [02 §3.2 containers](../../../docs/02-v1-architecture.md#32-containers) (`docker-proxy`), [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write)
- [07 §5–§6](../../../docs/07-security-notes.md#5-network--host) (no Docker socket in app containers)
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P0-B012
- Implementation: P0-T065
- Depends on: P0-T065

## Requirements

- Functional (each case asserts the outcome **and** the audit trail):
  - Restart via the command API of each default non-allow-listed container (`postgres`, `nats`, `mt-api`, `docker-proxy`) and of an unknown name → 403 problem+json `not_restartable`, an `audit.command` row `rejected` with the reason, and **no** request reaching the proxy.
  - A restart request for an allow-listed container without a valid C2 token (missing, expired, other args) → 428; with a session re-authenticated > 12 h ago → 428 `reauth_required`.
  - From inside the mt-api container, direct calls to the proxy: `POST /containers/postgres/restart`, `POST /containers/create`, `POST /containers/{id}/exec`, `POST /containers/{id}/stop`, `DELETE /containers/{id}`, `GET /images/json`, `POST /networks/create` → all 403 at the proxy and logged.
  - Static checks: `docker inspect mt-api` shows no `/var/run/docker.sock` (or any `docker.sock`) mount and no `DOCKER_HOST` pointing elsewhere than the proxy; only `docker-proxy` mounts the socket; only mt-api and docker-proxy are on `ctl`; the proxy isn't reachable from `core`, `scrape` or `obs`.
  - Positive control: an allow-listed restart (e.g. `llm-local`) with a valid C2 flow succeeds and is audited (accepted + applied).
  - Allow-list edits: adding a container is classified C3 (stays pending without break-glass approval + TOTP + cool-down); removing one is C1.
- Non-functional: suite runtime ≤ 3 min in CI; same suite run once on the production host (results in the progress log).
- Tools & access: listed in the front matter; no secrets.

## ToDo

- [ ] Write the suite with the cases above (pytest + docker SDK against the compose stack; the SDK is used only from the test runner, never from app containers).
- [ ] Add the network-reachability probes (`core`/`scrape`/`obs` → `docker-proxy:2375` must fail).
- [ ] Wire into CI (marked `verify`) and run once on the host.
- [ ] Log results here; file a bug for any failure.

## Verification

### Tests
- The suite above (≥ 15 cases incl. the positive control).

### Scenarios
- Given a stolen session cookie, when the attacker tries to restart `postgres`, then the command is refused and audited, and nothing restarts.
- Given mt-api code is compromised, when it talks to the proxy directly, then only list and allow-listed restart work.

### Stress / failure injection
- 50 rapid restart requests for a non-allow-listed name → all refused and audited, proxy log shows none; for an allow-listed name → one runs, the rest get 409.

## Acceptance criteria

- [ ] Every refusal case refused and audited; positive control applied
- [ ] Proxy denies every non-allow-listed Docker API call
- [ ] `mt-api` has no Docker socket mount (inspect output attached)
- [ ] Suite in CI and run once on the host
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Docker API version prefixes (`/v1.4x/…`): the proxy regexes must match with and without the version prefix; the suite tests both.

## Cardinal rules (do NOT)

- Do NOT add the Docker socket or the docker SDK to any app container to make a test easier.
- Do NOT widen the allow-list to make a case pass.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/07-security-notes.md` §6: link the refusal suite as the control's evidence.
- `docs/roadmap/phase-0-foundations.md`: tick T0.68 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T067-restart-refusal-test`
- PR title: `P0-T067: Verify restart refusal outside the docker-proxy allow-list`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T067` run

## Progress log

- 2026-10-22 02:01 · cloud:vm:be04b6ae61f8 · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (new task for R0.14 / T0.68, decided in 17 §D P0-B012)
