---
id: P1-T070
kind: task
title: Add the IBC-managed ib-gateway container for IBKR paper reconciliation
phase: 1
type: OPS
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T004, P0-T020, P0-T021, P0-T022]
requirements: [R1.12]
roadmap_todos: [T1.44]
modules: [M16]
dashboards: [D07, D16]
tools: [git, uv, docker]
mcp: []
env: []
services: [nats]
branch: p1/P1-T070-ib-gateway-container
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/02-v1-architecture.md, docs/07-security-notes.md]
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

# P1-T070 · Add the IBC-managed ib-gateway container for IBKR paper reconciliation

## Goal / expected outcome

An `ib-gateway` service (IB Gateway run by IBC, digest-pinned) exists in Compose behind an opt-in profile, logs in to the IBKR **paper** account with credentials from the secrets file, re-logs in on IBKR's daily restart, exposes the API **read-only** on the `core` network only, and reports health, so the IBKR recon adapter (P1-T042) has something to talk to. It ships disabled until you use IBKR (`ibkr.enabled: false` by default).

## Context & references

- Roadmap: requirement [R1.12](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.44](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets) (only when IBKR is used)
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B013 (add an `ib-gateway` container, IBC-managed, when IBKR is used)
- Containers and networks: [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) (`ib-gateway`: IBC-managed, digest-pinned, scheduled re-login, read-only API for P1 recon) · [02 §3.1](../../../docs/02-v1-architecture.md#31-networks) (`core`; venue traffic via the egress exit node from P7)
- Keys: [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) (practice/paper accounts use their normal credentials) · secrets [07 §2](../../../docs/07-security-notes.md#2-secrets)
- Live login is checked in P1-T074 (needs your IBKR paper login from P0-T009 / P1-T002)
- Cross-phase prerequisites: P0-T020 (Compose core, image lock), P0-T021 (networks), P0-T022 (sops → tmpfs per service)
- Depends on (this phase): P1-T004

## Requirements

- Image: a maintained IB Gateway + IBC image (e.g. `ghcr.io/gnzsnz/ib-gateway` stable), pinned by `@sha256:` in `infra/images.lock`; reviewed for telemetry (IBC/IB Gateway send none beyond the IBKR session itself)
- Compose profile `ibkr` (off by default); `config/venues.yaml` `ibkr.enabled: false` until you opt in; when disabled, recon shows IBKR as `disabled (not used)`, never `unreachable`
- IBC settings (`infra/ib-gateway/config.ini`, no secrets): `TradingMode=paper`, `ReadOnlyApi=yes`, `AcceptIncomingConnectionAction=reject` except from the `monitor` container, `AutoRestartTime` / daily re-login at the configured time (default 23:45 America/New_York, configurable), `ExistingSessionDetectedAction=primary`
- API port reachable only on `core` from `monitor` (no host port; VNC disabled, or bound to localhost behind Tailscale if you enable it for 2FA troubleshooting)
- Credentials: `IBKR_PAPER_USERNAME` and `IBKR_PAPER_PASSWORD` from the sops file mounted on tmpfs for this container only
- Health: TCP check on the API port plus an `ib_async` `reqCurrentTime` probe from `monitor`; heartbeat `sys.heartbeat.ib-gateway` and `/metrics` via a sidecar exporter; login failure → `alert.warning.ibkr_login`
- Restart via `system.service.restart` (allow-listed in `docker-proxy`)

## ToDo

- [ ] Add the `ib-gateway` service, profile, network and tmpfs secret mount to `infra/docker-compose.yml`; pin the image digest
- [ ] Write the IBC `config.ini` template and the re-login schedule (values in config, not code)
- [ ] Add the health probe and heartbeat in `mt_monitor.recon.ibkr` (probe only; positions are P1-T042)
- [ ] Add `ib-gateway` to the `docker-proxy` restart allow-list and the image scan job
- [ ] Write the tests listed under Verification (keyless: config and wiring only)
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box

## Verification

### Tests

- Unit: rendered `config.ini` has `TradingMode=paper` and `ReadOnlyApi=yes`; a test fails if either flips
- Integration (keyless): `docker compose --profile ibkr config` validates; the container starts and its health check reports `login_pending` without credentials (no crash loop); no host port is published (`docker port` empty)
- Security: secrets mounted only into `ib-gateway`; `monitor` cannot read them; image appears in the trivy/grype scan

### Scenarios

- Given `ibkr.enabled: false`, when the stack starts, then no `ib-gateway` container runs and D07 recon shows IBKR as disabled with the reason
- Given IB Gateway's daily restart, when IBC re-logs in, then the health probe recovers within 5 min and recon resumes without manual action (checked live in P1-T074)
- Given credentials are wrong, when IBC fails to log in, then `alert.warning.ibkr_login` fires once (deduped) and other venues are unaffected

### Stress / failure injection

- Fault: kill the container during a recon cycle; recon reports IBKR `unreachable` for that cycle, Docker restarts it, the next cycle succeeds (live part in P1-T074)

## Acceptance criteria

- [ ] `ib-gateway` defined, digest-pinned, opt-in, read-only API, paper mode, reachable only from `monitor` on `core`
- [ ] Keyless tests pass in CI; the live login is left to P1-T074
- [ ] CI green (ruff, mypy, pytest, image scan, gitleaks)

## Exceptions & edge cases

- IBKR 2FA: paper accounts normally don't need it; if prompted, IBC waits and alerts; you approve on your phone
- IBKR weekly server reset (Sunday): one failed probe is expected; alert only after 2 consecutive failures outside the reset window
- From P7 the container's traffic leaves via the egress exit node like all venue traffic ([16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys))

## Cardinal rules (do NOT)

- Do NOT log in with a live (real-money) IBKR account; paper only in P1; no live money before the P7 gates
- Do NOT enable order placement: `ReadOnlyApi=yes` stays on in P1 (orders arrive in P2 through M11)
- Do NOT publish the API or VNC port outside the `core` network / Tailscale
- Do NOT commit credentials or paste them into chats, issues, logs or test fixtures; they live only in the sops file ([07 §2](../../../docs/07-security-notes.md#2-secrets))
- Do NOT add an image without pinning it by digest, or vendored code that carries telemetry or referral IDs
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.44; note P1-T070 next to it.
- `docs/02-v1-architecture.md` §3.2: confirm the `ib-gateway` row matches (profile, re-login time default).
- `docs/07-security-notes.md` §3: note that IBKR paper uses normal credentials behind a read-only API gateway.

## Branch & PR

- Branch: `p1/P1-T070-ib-gateway-container`
- PR title: `P1-T070: Add the IBC-managed ib-gateway container for IBKR paper reconciliation`
- PR checklist: tests added · image digest pinned and scanned · docs synced · task file ticked · `./kanban done P1-T070` run

## Progress log

- 2026-10-22 00:00 · aligner · created for T1.44 (docs/16–17 alignment, P1-B013 decision)
