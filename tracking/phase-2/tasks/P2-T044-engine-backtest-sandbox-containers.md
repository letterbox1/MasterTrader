---
id: P2-T044
kind: task
title: engine, backtest-worker and sandbox containers with gVisor and limits
phase: 2
type: OPS
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T020, P0-T021, P0-T022]
requirements: [R2.45, R2.N3]
roadmap_todos: [T2.40]
modules: [M12, M7]
dashboards: []
tools: [docker, runsc]
mcp: []
env: []
services: [docker]
branch: p2/P2-T044-engine-backtest-sandbox-containers
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T044 · engine, backtest-worker and sandbox containers with gVisor and limits

## Goal / expected outcome

`docker-compose.yml` gains `engine`, `backtest-worker`, `sandbox` and `deadman` services, pinned by digest, with CPU/memory limits, correct networks and secret scoping; the host has the gVisor `runsc` runtime and `sandbox` runs with `--network none`, no secrets and a read-only root filesystem. Part B builds the sandbox runner that uses it.

## Context & references

- Roadmap: [R2.45, R2.N3](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.40
- Architecture: [02 §3.2 containers](../../../docs/02-v1-architecture.md#32-containers) · [02 §3.1 networks](../../../docs/02-v1-architecture.md#31-networks)
- Security: [SPEC NN4](../../../SPEC.md#non-negotiable-requirements) · [07 §6 LLM safety](../../../docs/07-security-notes.md#6-application-controls) · [07 §5](../../../docs/07-security-notes.md#5-network--host)
- Cross-phase (`depends_on`): compose base pinned by digest (P0-T020, T0.41), network segmentation (P0-T021, T0.42), sops → tmpfs secret scoping (P0-T022, T0.43).
- Decisions: `deadman` sidecar with its own trade-only keys and venue connections, cancel/flatten only ([16 §3.1](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch), 02 §3.2); venue traffic via the fixed egress exit node from P7 ([16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys)).
- Related: P2-T072 (`deadman` sidecar code), P2-T116 (sandbox runner + generator, T2.28).

## Requirements

- `engine`: network `core`, egress allow-list to testnet/practice venue hosts only; secrets = venue trade keys for its modes; limits e.g. 4 CPU / 8 GB (tune); `restart: unless-stopped`; healthcheck on heartbeat freshness.
- `deadman`: separate container on `core`, its **own** trade-only keys (`venues.<venue>.deadman`, used only to cancel and flatten) and its own venue connections; 0.5 CPU / 256 MB; `restart: always`; healthcheck on its own heartbeat.
- `backtest-worker`: `core` (Postgres read via `pit`, MLflow), **no venue keys**, limits e.g. 6 CPU / 16 GB, scalable replicas.
- `sandbox`: `runtime: runsc`, `network_mode: none`, no secrets, `read_only: true`, tmpfs `/tmp` 512 MB, `pids_limit`, CPU/mem/time limits (e.g. 2 CPU / 4 GB / 10 min wall), non-root user, seccomp default; code + data passed via a mounted job dir; results written back to that dir only.
- All images pinned by digest; trivy/grype scan in CI.

## ToDo

- [ ] Install gVisor on the host (`runsc install`, Docker daemon runtime config) — Ansible/script in `ops/host/`
- [ ] Compose service definitions + resource limits
- [ ] Egress allow-list for `engine` (firewall/nftables or proxy)
- [ ] Secret scoping per service
- [ ] Smoke tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Escape smoke: inside `sandbox`, `curl`/DNS fail, `/run/secrets` absent, writing outside job dir fails, `dmesg` shows gVisor kernel.
- Engine egress: connection to a non-allow-listed host fails.
- Compose config test: every image has `@sha256:`.

### Scenarios
- Given a generated strategy tries to open a socket, when run in `sandbox`, then it fails with network unreachable and the run is marked 'sandbox violation'.
- Given `backtest-worker` env, when inspected, then no venue secret is present.

### Stress / failure injection
- Fork bomb and 20 GB allocation inside `sandbox`: contained by pids/memory limits; host unaffected; job killed and reported.

## Acceptance criteria

- [ ] Four services running with limits and pinned digests
- [ ] Sandbox isolation smoke passes
- [ ] Secrets only where needed
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Host kernel lacks gVisor support: fall back to `--network none` + seccomp + user namespaces, record as degraded, and block LLM-generated code from running until fixed (Part B).

## Cardinal rules (do NOT)

- Do NOT mount any secret or the Docker socket into `sandbox` or `backtest-worker`.
- Do NOT give `engine` broad internet egress.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Pin images by digest; no telemetry or referral/broker IDs in vendored code.
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.

## Doc sync on completion

- `docs/02-v1-architecture.md` §3.2: add `deadman`, record limits and runtime.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.40 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T044-engine-backtest-sandbox-containers`
- PR title: `P2-T044: engine, backtest-worker and sandbox containers with gVisor and limits`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T044` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (deadman container with its own trade-only keys (16 §3.1), egress note, cross-phase deps)
