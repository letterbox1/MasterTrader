---
id: P4-T007
kind: task
title: Harden the RSS-Bridge sidecar (whitelist, auth, scrape network)
phase: 4
type: OPS
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R4.01, R4.N1]
roadmap_todos: [T4.40]
modules: [M2]
dashboards: [D07, D08]
branch: p4/P4-T007-rss-bridge-container
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/runbooks/rss-bridge.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T007 · Harden the RSS-Bridge sidecar (whitelist, auth, scrape network)

## Goal / expected outcome

An `rss-bridge` container, pinned by digest, runs only on the `scrape` network with an explicit `enabled_bridges[]` whitelist, HTTP auth on, a 15-min–3-h cache, and no route to Postgres, NATS core or the signer. `ingest-text` reads it with `?format=Json`.

## Context & references

- Roadmap: [R4.01, R4.N1](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.40](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Verdict and config: [06 §1 RSS-Bridge row](../../../docs/06-aggregators-and-market-providers.md#1-verdicts-on-the-tools-you-proposed) · research [social-aggregators](../../../docs/research/social-aggregators.md) (`enabled_bridges[] = *` by default → whitelist)
- Networks: [02 §3.1](../../../docs/02-v1-architecture.md#31-networks) (`scrape`: ingest-text, rss-bridge, crawl4ai; no route to postgres or signer) · [07 §5](../../../docs/07-security-notes.md#5-network--host)
- Cross-phase: P0 T0.42 (networks), T0.43 (secrets).

## Requirements

- `services/rss-bridge/config.ini.php`: `enabled_bridges[]` limited to the whitelist (e.g. `CssSelectorBridge`, `XPathBridge`, `TelegramBridge` (fallback only), `MastodonBridge`, `FilterBridge`, `MrssBridge`) plus any bridge P4-T012 requests; everything else off.
- Auth on (`[authentication] enable = true`), credentials from secrets; `ingest-text` is the only client.
- Cache 15 min minimum per bridge (context only, not latency signals); max 3 h.
- Container: read-only root FS, non-root user, no published ports, `scrape` network only, egress allowed to the internet; memory limit 256 MB.
- No Reddit bridge (Reddit RSS ends 2026-11-13).

## ToDo

- [ ] Add the `rss-bridge` service to `docker-compose.yml` with a digest-pinned image and the hardening flags.
- [ ] Write `services/rss-bridge/config.ini.php` (whitelist, auth, cache) and `services/rss-bridge/whitelist.txt`.
- [ ] Add a health check hitting `/?action=list` with auth.
- [ ] Add a Compose-level network test script `ops/tests/rss_bridge_isolation.sh` (no TCP to postgres:5432, nats:4222 core account, signer).
- [ ] Scan the image with trivy/grype in CI.

## Verification

### Tests
- Integration: unauthenticated request → 401; authenticated whitelisted bridge → 200 JSON; non-whitelisted bridge → error.
- Network: from inside the container, connections to `postgres:5432` and `signer` fail; DNS for them does not resolve.

### Scenarios
- Given someone adds `enabled_bridges[] = *`, when CI runs the config lint, then it fails.
- Given RSS-Bridge is down, then `ingest-text` marks bridged sources `stale` in D07 and other sources continue.

### Stress / failure injection
- Fire 200 parallel bridge requests: cache absorbs repeats, memory stays < 256 MB, no OOM restart.

## Acceptance criteria

- [ ] Image pinned by digest; trivy/grype clean of criticals
- [ ] Isolation test passes (no DB/signer route)
- [ ] Whitelist + auth + cache verified by integration tests
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Some bridges need upstream keys/cookies: never add cookie-based bridges (ToS); skip the site instead.

## Cardinal rules (do NOT)

- Do NOT attach rss-bridge to the `core` network.
- Do NOT enable bridges that log in with user accounts.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT use unpinned images (`:latest`) or vendored code with telemetry/referral IDs; pin by digest.
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.

## Doc sync on completion

- `docs/02-v1-architecture.md`: §3.1/§3.2: confirm rss-bridge network and hardening notes
- `docs/runbooks/rss-bridge.md`: new runbook: add a bridge to the whitelist, rotate auth
- `docs/roadmap/phase-4-intel.md`: tick T4.40 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T007-rss-bridge-container`
- PR title: `P4-T007: Harden the RSS-Bridge sidecar (whitelist, auth, scrape network)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T007` run

## Progress log

- 2026-10-21 00:00 · planner · created
