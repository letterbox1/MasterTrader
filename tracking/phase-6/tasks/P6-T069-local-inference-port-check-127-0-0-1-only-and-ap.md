---
id: P6-T069
kind: task
title: "Local inference port check: 127.0.0.1 only and API key required"
phase: 6
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T011, P6-T023, P6-T027, P0-T056]
requirements: [R6.N2]
roadmap_todos: [T6.73]
modules: [M21, M9]
dashboards: [D10]
tools: [docker, nmap, ss, curl, uv]
mcp: []
env: []
services: [vllm-classify, onnx-cpu, hindsight, laya, clef-flash, llm-local, tailscale]
branch: p6/P6-T069-local-inference-port-check-127-0-0-1-only-and-ap
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T069 · Local inference port check: 127.0.0.1 only and API key required

## Goal / expected outcome

Evidence for R6.N2: every local inference server added in Phase 6 (tier-B `vllm-classify` and `onnx-cpu`, `hindsight` API/UI, the `bakeoff` profile contenders: Laya, Clef-flash, Kev if cleared, JSON baseline) listens only on `127.0.0.1` or the internal Docker network, publishes no port, and refuses any call without its API key. The check is scripted so it re-runs in CI (compose profile) and after every image bump.

## Context & references

- Roadmap: [R6.N2](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.73
- Spec: [07 §5](../../../docs/07-security-notes.md#5-network--host) (local inference servers bind to `127.0.0.1` and require an API key, even inside the internal network; no published ports except via Tailscale) · [02 §3](../../../docs/02-v1-architecture.md) networks (`core`, `scrape`, `signer`) · [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (`LAYA_API_KEY`)
- Depends on (this phase): P6-T011 (Hindsight), P6-T023 (tier-B serving), P6-T027 (bake-off containers)
- Cross-phase: P0-T056 (image scan + "nothing exposed outside Tailscale" check this extends)

## Requirements

- Listener inventory: `ss -ltnp` inside each container and `docker port`/compose config show no `0.0.0.0` publish for these services.
- External scan: `nmap` from another tailnet device and from the LAN shows the ports closed.
- Auth: for each server, a request without a key → 401/403; with a wrong key → 401/403; with the right key (read from tmpfs, never printed) → 200.
- Network reach: containers on the `scrape` network can't reach any inference server; `agents`/`decision-svc` can.
- Script `tools/verify/inference_ports.py` emits a pass/fail table; non-zero exit on any failure.

## ToDo

- [ ] Write the script (inventory, scan, auth probes, cross-network probe).
- [ ] Add a CI job on the compose `bakeoff` + core profiles.
- [ ] Run on the host; record the table in the progress log.
- [ ] File a bug (S2) for any server that answers without a key or is reachable from outside.

## Verification

### Tests
- The script's own unit tests on recorded `ss`/`nmap` output (pass and fail fixtures).
- CI job green on the compose profiles.

### Scenarios
- Given `vllm-classify` is called without `Authorization`, then it returns 401 and the call is logged.
- Given a container on the `scrape` network tries `hindsight:8888`, then the connection is refused.
- Given an image bump re-enables a published port, then the CI job fails (negative control by editing a test compose file).

### Stress / failure injection
- Restart each server: the key requirement is still enforced on first request after boot (no unauthenticated warm-up window).

## Acceptance criteria

- [ ] Every Phase 6 inference server: no external listener, key required (table in the progress log).
- [ ] CI job committed and green.

## Exceptions & edge cases

- A server with no native auth (e.g. Hindsight if its API has none (U)): fronted by an auth proxy sidecar on the same network; the check targets the proxy and proves the server itself isn't reachable around it.
- Bake-off profile not running: the script starts it, checks, and stops it.

## Cardinal rules (do NOT)

- Do NOT print, log or commit any API key; read keys from tmpfs only.
- Do NOT publish a port to make a probe easier.
- Do NOT commit secrets; do NOT skip, weaken or delete a test to get green; pin images by digest.

## Doc sync on completion

- `docs/07-security-notes.md` §5: list the Phase 6 servers covered and link the check.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.73 (and note this task ID).

## Branch & PR

- Branch: `p6/P6-T069-local-inference-port-check-127-0-0-1-only-and-ap`
- PR title: `P6-T069: Local inference port check: 127.0.0.1 only and API key required`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T069` run

## Progress log

- 2026-10-22 00:00 · aligner · created for T6.73 / R6.N2 (07 §5 port and API-key check over every P6 inference server)
