---
id: P5-T054
kind: task
title: Network test: signer and Anvil isolated; no LLM can reach keys
phase: 5
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T017, P5-T013, P0-T021]
requirements: [R5.N1]
roadmap_todos: [T5.40]
modules: [M22, M17]
dashboards: []
tools: [docker, uv]
mcp: []
env: []
services: []
branch: p5/P5-T054-verify-signer-isolation-network
pr: ""
doc_sync: [docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T054 · Network test: signer and Anvil isolated; no LLM can reach keys

## Goal / expected outcome

An automated network test proves the signer and Anvil sit on the isolated `signer` network, reachable only from the policy service (`airdrop-exec` in P5; P5-B003), with egress limited to RPC hosts, and that no LLM/agent/MCP/scraper container or the LiteLLM gateway can reach the signer socket, OpenBao or key files.

## Context & references

- Roadmap: [R5.N1](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) ("Network test") · [07 §5](../../../docs/07-security-notes.md#5-network--host) · [02 §3.1](../../../docs/02-v1-architecture.md#31-networks)
- P0 segmentation test (R0.N3) extended; ops task P5-T017

## Requirements

- From each container on `core`, `scrape`, `obs`, `edge` (and `agents`/`litellm`/`decision-svc` if present): TCP/Unix-socket connect to signer, anvil, openbao → fail.
- From `airdrop-exec`: signer reachable with a valid client cert; without cert → refused.
- From signer: only allow-listed RPC hosts reachable.
- Filesystem: no container other than signer mounts the secrets tmpfs/key volume (compose inspection).
- Runs in CI (compose up in CI runner) and weekly on the host.

## ToDo

- [ ] Write `tests/network/test_signer_isolation.py` driving `docker compose exec` probes.
- [ ] Compose-inspection check for volumes/networks.
- [ ] Schedule the weekly host run (Prefect) with alert on failure.

## Verification

### Tests
- The probe matrix itself; compose-inspection assertions.

### Scenarios
- Given someone adds `litellm` to the `signer` network by mistake, then CI fails with the offending service named.

### Stress / failure injection
- n/a: connectivity assertions

## Acceptance criteria

- [ ] Probe matrix passes in CI and on the host
- [ ] Weekly host run scheduled with alerting

## Exceptions & edge cases

- Containers not present in P5 (agents, mcp) are skipped with a note and auto-included when they appear.

## Cardinal rules (do NOT)

- Do NOT add temporary network exceptions to make the test pass.
- Do NOT give any LLM, agent or MCP path a route to keys, the signer socket or the `signer` network (R5.N1).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- No doc change beyond ticking the R5.N1 verification.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.40 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T054-verify-signer-isolation-network`
- PR title: `P5-T054: Network test: signer and Anvil isolated; no LLM can reach keys`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T054` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (policy service as the signer's only caller per P5-B003; P0 networks dep)
