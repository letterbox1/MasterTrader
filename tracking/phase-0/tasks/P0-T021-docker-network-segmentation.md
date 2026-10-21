---
id: P0-T021
kind: task
title: Define the Docker networks and segmentation
phase: 0
type: OPS
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T020]
requirements: [R0.N3]
roadmap_todos: [T0.42]
modules: [ops]
dashboards: []
branch: p0/P0-T021-docker-network-segmentation
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T021 · Define the Docker networks and segmentation

## Goal / expected outcome

The five networks of 02 §3.1 exist with the right members: `edge`, `core`, `scrape`, `signer`, `obs`. `scrape` has internet egress but **no route to Postgres or the signer**; `signer` is reachable only from airdrop-exec (P5). A probe proves it.

## Context & references

- [Roadmap P0 R0.N3](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.42](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [02 §3.1 networks](../../../docs/02-v1-architecture.md#31-networks)
- [07 §5 network & host](../../../docs/07-security-notes.md#5-network--host)
- Related: P0-T056 port-scan verification
- Depends on: P0-T020

## Requirements

- `edge` (caddy, mt-api); `core` (mt-api, postgres, nats, prefect-*, mlflow, litellm, tei-*, local-advisor); `scrape` (only a probe in P0; egress yes); `signer` (`internal: true`, empty in P0); `obs` (grafana, loki, prometheus, vector, alertmanager, exporters).
- Postgres attached to `core` only; NATS to `core` and `scrape`, with the `SCRAPE` account publish-limited — the only cross-network path.
- Egress allow-list for `core` documented (venues/LLM APIs); P0 either enforces it with a host nftables egress set or documents it for P2 (log decision).
- Exporters join `core` + `obs`; no obs container joins `scrape`.

## ToDo

- [ ] Declare networks and memberships in compose.
- [ ] Add `infra/probes/netprobe` (busybox) on `scrape` trying TCP to `postgres:5432`, `mt-api:8000`, `signer`, `nats:4222`.
- [ ] Expected: all fail except NATS, where the SCRAPE account can only publish `text.raw.>`.
- [ ] Add the probe to CI and to P0-T056.

## Verification

### Tests
- Integration: netprobe on `scrape` → postgres/mt-api/signer unreachable; NATS reachable but `SUB >` and `PUB risk.event` denied.

### Scenarios
- Given a future scraper container is compromised, when it tries to reach Postgres, then there is no route; when it publishes to `kill.set`, then NATS denies it.

### Stress / failure injection
- n/a: static segmentation; the fault case is the probe.

## Acceptance criteria

- [ ] Five networks with memberships as listed (compose config dump attached)
- [ ] Netprobe results match expectations in CI
- [ ] NATS SCRAPE permissions tested
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Never attach a service to both `scrape` and `core` except NATS.

## Cardinal rules (do NOT)

- Do NOT attach Postgres or the signer to `scrape` or `edge`.
- Do NOT give the SCRAPE NATS account subscribe rights.
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/02-v1-architecture.md` §3.1: note the NATS cross-network account rule.
- `docs/roadmap/phase-0-foundations.md`: tick T0.42 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T021-docker-network-segmentation`
- PR title: `P0-T021: Define the Docker networks and segmentation`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T021` run

## Progress log

- 2026-10-21 00:00 · planner · created
