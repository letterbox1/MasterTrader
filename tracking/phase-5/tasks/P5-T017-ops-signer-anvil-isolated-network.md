---
id: P5-T017
kind: task
title: Signer and Anvil containers on the isolated signer network; keys in OpenBao or sops
phase: 5
type: OPS
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T013]
requirements: [R5.N1, R5.02]
roadmap_todos: [T5.40]
modules: [M22]
dashboards: [D16]
branch: p5/P5-T017-ops-signer-anvil-isolated-network
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/07-security-notes.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T017 · Signer and Anvil containers on the isolated signer network; keys in OpenBao or sops

## Goal / expected outcome

`signer` and `anvil` run in Compose on the `signer` network (egress: chain RPC allow-list only), reachable only from `airdrop-exec` (and later `treasury`), with keys supplied from OpenBao or the sops tmpfs; no LLM/agent/MCP/scraper container can route to them.

## Context & references

- Roadmap: [R5.N1](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.40 · [07 §2](../../../docs/07-security-notes.md#2-secrets) · [07 §5](../../../docs/07-security-notes.md#5-network--host)
- Networks: [02 §3.1](../../../docs/02-v1-architecture.md#31-networks) · containers [02 §3.2](../../../docs/02-v1-architecture.md#32-containers)
- P0 networks (T0.42 / R0.N3) and sops (T0.43 / R0.N1) are prerequisites
- Verified by P5-T054

## Requirements

- Images pinned by digest: `mt-signer` (built), `ghcr.io/foundry-rs/foundry` (anvil) — scanned by trivy/grype in CI.
- `signer` network: members signer, anvil, airdrop-exec; egress via an allow-list proxy to configured RPC hosts only.
- Signer container: read-only root FS, no shell in the image, `cap_drop: ALL`, non-root UID, tmpfs for secrets, no published ports, memory lock where supported.
- OpenBao (if used): own container on a dedicated network reachable only by signer; AppRole auth; audit device on.
- Health checks + `sys.heartbeat.signer`; restart policy `on-failure` with alert.

## ToDo

- [ ] Add `signer`, `anvil` (and optional `openbao`) services to `docker-compose.yml` with digests.
- [ ] Create the egress allow-list (Squid/Envoy or nftables) for RPC hosts from P5-T018.
- [ ] Wire secrets: sops → tmpfs mount for signer only; or OpenBao AppRole with response wrapping.
- [ ] Add CI image scan and a compose lint that fails if any other service joins `signer`.
- [ ] Document in 02 §3.1/§3.2 and 07 §2.

## Verification

### Tests
- Integration: from `agents`, `litellm`, `ingest-text`, `mt-api` containers, TCP connect to signer socket/port fails.
- Integration: from signer, HTTPS to a non-allow-listed host fails; to the RPC host succeeds.
- CI: compose lint rejects a service added to the `signer` network.

### Scenarios
- Given a compromised scraper container, when it scans the internal ranges, then the signer is unreachable.
- Given OpenBao is sealed at boot, when the signer starts, then it stays `frozen` and alerts.

### Stress / failure injection
- Restart the signer 20 times in a loop: always returns to healthy or frozen, never to a partially-keyed state.

## Acceptance criteria

- [ ] Containers up, pinned, scanned
- [ ] Only airdrop-exec can reach the signer
- [ ] Egress restricted to RPC allow-list
- [ ] Keys only via OpenBao/sops tmpfs

## Exceptions & edge cases

- 4G failover changes the egress IP: provider IP restrictions (P5-T003) must include both, or calls fail closed.
- Host reboot: signer requires OpenBao unseal or sops decrypt; until then claims queue as tasks.

## Cardinal rules (do NOT)

- Do NOT publish signer/anvil ports or put them on `core` or `scrape`.
- Do NOT bake keys into images or compose files.
- Do NOT commit secrets or paste them into chats, issues or logs; secrets live only in the sops/age file or OpenBao (07 §2).
- Do NOT give any LLM, agent or MCP path a route to keys, the signer socket or the `signer` network (R5.N1).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §3.1/§3.2: final membership of the `signer` network.
- `docs/07-security-notes.md` §2: note OpenBao adoption if used.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.40 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T017-ops-signer-anvil-isolated-network`
- PR title: `P5-T017: Signer and Anvil containers on the isolated signer network; keys in OpenBao or sops`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T017` run

## Progress log

- 2026-10-21 00:00 · planner · created
