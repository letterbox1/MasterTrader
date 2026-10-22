---
id: P8-T015
kind: task
title: "`mcp` container on the internal `edge` network behind Caddy (`/mcp`), Tailscale only; token pepper in secrets"
phase: 8
type: OPS
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T003, P0-T020, P0-T021, P0-T022, P0-T023]
requirements: [R8.02, R8.08]
roadmap_todos: [T8.40]
modules: [M20, M17]
dashboards: [D16, D17]
tools: [docker, sops, git, nmap]
mcp: []
env: []
services: [docker, caddy, tailscale, prometheus, loki]
branch: p8/P8-T015-mcp-container
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/07-security-notes.md, docs/roadmap/phase-8-mcp.md]
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

# P8-T015 · `mcp` container on the internal `edge` network behind Caddy (`/mcp`), Tailscale only; token pepper in secrets

## Goal / expected outcome

The `mcp` compose service runs `mt_mcp` over Streamable HTTP on the internal `edge` network, reached only through Caddy at `/mcp` on the Tailscale interface (TLS). It has no route to Postgres, NATS or the signer (it reaches only `mt_api`), is pinned by digest, hardened, health-checked and on Grafana. The MCP token pepper lives in the sops file and is mounted (tmpfs) into `mt-api` only. Client tokens live only in your OS keychain or the sops file. Built and tested on the compose test stack with a fixture pepper.

## Context & references

- Roadmap: [R8.02](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.40](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Architecture: [02 §3.1 networks](../../../docs/02-v1-architecture.md#31-networks) · [02 §3.2 containers](../../../docs/02-v1-architecture.md#32-containers) (`mcp` / `mt_mcp`, phase 8)
- Security: [07 §5](../../../docs/07-security-notes.md#5-network--host) (bind to 127.0.0.1 / Tailscale only, digests, scans) · [07 §2](../../../docs/07-security-notes.md#2-secrets) (sops/age, tmpfs)
- Cross-phase: P0 R0.02 (compose pinned by digest), R0.N1 (sops), R0.N2 (Tailscale-only), R0.N3 (segmentation), R0.10 (Grafana/Loki).
- Decisions: [17 §D P8-B011](../../../docs/17-decisions-register.md#d-other-decisions) (`mcp` on the internal network behind Caddy, Tailscale only) · [07 §2](../../../docs/07-security-notes.md#2-secrets) (MCP token pepper in the sops file) · [07 §5](../../../docs/07-security-notes.md#5-network--host) (`mcp` on `edge` behind Caddy, reaches only `mt_api`) · [02 §7.4](../../../docs/02-v1-architecture.md#74-telegram--mcp) (Streamable HTTP at `/mcp` on Caddy, Tailscale/TLS only)
- Cross-phase (depends_on): P0-T020 (compose + Caddy, digests), P0-T021 (networks/segmentation), P0-T022 (sops/age into tmpfs), P0-T023 (Prometheus/Loki/Grafana).

## Requirements

- Network: `mcp` on `edge` only (02 §3.1: caddy, mt-api, ntfy, mcp); reaches only `mt-api` over HTTP; Caddy proxies `https://<host>.<tailnet>.ts.net/mcp` to it (and the optional legacy HTTP+SSE path from P8-T032 when enabled). Not on `core`, `scrape` or `signer`; no published host ports.
- Container hardening: non-root user, read-only rootfs, `no-new-privileges`, `cap_drop: [ALL]`, memory limit 256 MB, restart `unless-stopped`.
- Image built in CI, pinned by digest in compose, scanned with trivy/grype, SBOM produced.
- Health check `/healthz` (mt_api reachable + registry loaded); Prometheus metrics (calls, errors, latency, sessions); Grafana panel; Loki logs with args redacted.
- `/system/services?kind=mcp` reports status, transport, connected clients and the nearest token expiry (for D17 Connection).
- Feature flag `mcp.enabled` (system setting, default off): when off, the container is stopped and D17 is hidden from nav.
- Token pepper: sops key `mcp_token_pepper` (you generate it in P8-T018; tests use a fixture), decrypted to tmpfs for `mt-api` only; `mcp` never sees it.
- The `mcp` service holds no MCP token. Client tokens: host-local stdio clients read theirs from the sops file (decrypted to tmpfs); laptop clients use the OS keychain. Never in git, `.env` or chat.

## ToDo

- [ ] Add the `mcp` service to `compose.yaml` (build, digest pin, networks, hardening, health check).
- [ ] Add the Caddy route `/mcp` on the Tailscale listener with TLS; forward `Mcp-Session-Id` and `Last-Event-ID`; disable response buffering for SSE; keep the `Origin` check in `mt_mcp`.
- [ ] Add the sops template entries (key names only: `mcp_token_pepper`, `mcp_client_token_<label>`), the tmpfs mount for `mt-api`, and a gitleaks rule for the MCP token prefix.
- [ ] Prometheus scrape config, Grafana panel, Loki labels.
- [ ] Write a port-scan check (nmap from a LAN host and from the Tailscale peer) into the ops checklist.
- [ ] Update docs.

## Verification

### Tests
- Ops test: `docker compose up mcp` healthy; `/healthz` green; Grafana panel shows calls.
- Port scan: TCP closed from LAN and public; reachable from a Tailscale peer only via Caddy TLS.
- Network test: from inside `mcp`, Postgres:5432 and NATS:4222 are unreachable; the pepper file isn't mounted.
- gitleaks: a fake MCP token committed in a test branch is caught.

### Scenarios
- Given `mcp.enabled = false`, then the service is stopped and `/mcp` returns 404 via Caddy.
- Given mt-api is down, then `/healthz` fails and D16 shows `mcp` degraded.

### Stress / failure injection
- Container restart during an active Streamable HTTP session: the client reconnects; pending approvals are unaffected (they live in mt_api).

## Acceptance criteria

- [ ] `mcp` on `edge` only, reachable only via Caddy on Tailscale/TLS; no route to DB/NATS/signer
- [ ] Pepper in sops, mounted into `mt-api` only
- [ ] Pinned by digest, scanned, hardened, health-checked, on Grafana
- [ ] No token stored in the image, compose file or git
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Tailscale down: only stdio access on the host remains; that's acceptable.
- Caddy misroute: `mt_mcp` refuses bad `Origin`, and mt_api still needs a valid token.

## Cardinal rules (do NOT)

- Do NOT publish a host port for `mcp` or attach it to `core`/`signer` networks.
- Do NOT bake tokens or the pepper into images, compose files or `.env`.
- Do NOT commit secrets or paste them into chats/issues (including into the Claude conversation); secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.
- Do NOT add paid data, APIs or services; free tiers only (03 §1).

## Doc sync on completion

- `docs/02-v1-architecture.md` §3.1/§3.2: `mcp` network membership and Caddy route.
- `docs/07-security-notes.md` §5/§6: MCP exposure.
- `docs/roadmap/phase-8-mcp.md`: tick T8.40.

## Branch & PR

- Branch: `p8/P8-T015-mcp-container`
- PR title: `P8-T015: mcp container on the internal edge network behind Caddy (/mcp), Tailscale only; token pepper in secrets`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T015` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (`edge` network behind Caddy at `/mcp`, Tailscale/TLS only, SSE headers forwarded, token pepper in sops mounted into mt-api only; dropped gap dep P8-B011; added R8.08; cross-phase deps P0-T020/T021/T022/T023; tools/env/services)
