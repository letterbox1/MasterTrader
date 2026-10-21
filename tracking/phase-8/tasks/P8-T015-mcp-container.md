---
id: P8-T015
kind: task
title: `mcp` container bound to localhost/Tailscale, token handling in secrets
phase: 8
type: OPS
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T003, P8-B011]
requirements: [R8.02]
roadmap_todos: [T8.40]
modules: [M20, M17]
dashboards: [D16, D17]
branch: p8/P8-T015-mcp-container
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/07-security-notes.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T015 · `mcp` container bound to localhost/Tailscale, token handling in secrets

## Goal / expected outcome

The `mcp` compose service runs `mt_mcp` over Streamable HTTP. It is reachable only from localhost and Tailscale (through Caddy on the Tailscale interface), has no route to Postgres, NATS or the signer, is pinned by digest, is health-checked and has Grafana panels. Client tokens live only in the sops file or the client's OS keychain.

## Context & references

- Roadmap: [R8.02](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.40](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Architecture: [02 §3.1 networks](../../../docs/02-v1-architecture.md#31-networks) · [02 §3.2 containers](../../../docs/02-v1-architecture.md#32-containers) (`mcp` / `mt_mcp`, phase 8)
- Security: [07 §5](../../../docs/07-security-notes.md#5-network--host) (bind to 127.0.0.1 / Tailscale only, digests, scans) · [07 §2](../../../docs/07-security-notes.md#2-secrets) (sops/age, tmpfs)
- Cross-phase: P0 R0.02 (compose pinned by digest), R0.N1 (sops), R0.N2 (Tailscale-only), R0.N3 (segmentation), R0.10 (Grafana/Loki).
- Gap: P8-B011 (network placement of `mcp` not in 02 §3.1).

## Requirements

- Network: `mcp` on `edge` only (reaches `mt-api` over HTTP; Caddy proxies `https://<host>.<tailnet>.ts.net/mcp` to it). No membership in `core`, `scrape`, `signer` or `obs` beyond metrics scraping; no published host ports.
- Container hardening: non-root user, read-only rootfs, `no-new-privileges`, `cap_drop: [ALL]`, memory limit 256 MB, restart `unless-stopped`.
- Image built in CI, pinned by digest in compose, scanned with trivy/grype, SBOM produced.
- Health check `/healthz` (mt_api reachable + registry loaded); Prometheus metrics (calls, errors, latency, sessions); Grafana panel; Loki logs with args redacted.
- `/system/services?kind=mcp` reports status, transport, connected clients and the nearest token expiry (for D17 Connection).
- Feature flag `mcp.enabled` (system setting, default off): when off, the container is stopped and D17 is hidden from nav.
- The service holds no MCP token. Client tokens: host-local stdio clients read theirs from the sops file `secrets/mcp.sops.yaml` (decrypted to tmpfs); laptop clients use the OS keychain. Never in git, `.env` or chat.

## ToDo

- [ ] Add the `mcp` service to `compose.yaml` (build, digest pin, networks, hardening, health check).
- [ ] Add the Caddy route `/mcp` on the Tailscale listener with TLS; forward `Mcp-Session-Id`; keep the `Origin` check in `mt_mcp`.
- [ ] Add the `secrets/mcp.sops.yaml` template (keys only, no values) and a gitleaks rule for the MCP token prefix.
- [ ] Prometheus scrape config, Grafana panel, Loki labels.
- [ ] Write a port-scan check (nmap from a LAN host and from the Tailscale peer) into the ops checklist.
- [ ] Update docs.

## Verification

### Tests
- Ops test: `docker compose up mcp` healthy; `/healthz` green; Grafana panel shows calls.
- Port scan: TCP closed from LAN and public; reachable from a Tailscale peer only via Caddy; localhost reachable.
- Network test: from inside `mcp`, Postgres:5432 and NATS:4222 are unreachable.
- gitleaks: a fake MCP token committed in a test branch is caught.

### Scenarios
- Given `mcp.enabled = false`, then the service is stopped and `/mcp` returns 404 via Caddy.
- Given mt-api is down, then `/healthz` fails and D16 shows `mcp` degraded.

### Stress / failure injection
- Container restart during an active Streamable HTTP session: the client reconnects; pending approvals are unaffected (they live in mt_api).

## Acceptance criteria

- [ ] `mcp` reachable only via localhost/Tailscale; no route to DB/NATS/signer
- [ ] Pinned by digest, scanned, hardened, health-checked, on Grafana
- [ ] No token stored in the image, compose file or git
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Tailscale down: only localhost/stdio access remains; that's acceptable.
- Caddy misroute: `mt_mcp` refuses bad `Origin`, and mt_api still needs a valid token.

## Cardinal rules (do NOT)

- Do NOT publish a host port for `mcp` or attach it to `core`/`signer` networks.
- Do NOT bake tokens into images, compose files or `.env`.
- Do NOT commit secrets or paste them into chats/issues (including into the Claude conversation); secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).
- Do NOT add paid data, APIs or services; free tiers only (03 §1).

## Doc sync on completion

- `docs/02-v1-architecture.md` §3.1/§3.2: `mcp` network membership and Caddy route.
- `docs/07-security-notes.md` §5/§6: MCP exposure.
- `docs/roadmap/phase-8-mcp.md`: tick T8.40.

## Branch & PR

- Branch: `p8/P8-T015-mcp-container`
- PR title: `P8-T015: `mcp` container bound to localhost/Tailscale, token handling in secrets`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T015` run

## Progress log

- 2026-10-21 00:00 · planner · created
