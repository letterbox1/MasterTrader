---
id: P3-T009
kind: task
title: journal container and Fava sidecar on the internal network
phase: 3
type: OPS
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T008, P0-T020, P0-T021, P0-T023]
requirements: [R3.10, R3.01]
roadmap_todos: [T3.40]
modules: [M18]
dashboards: []
tools: [git, docker]
mcp: []
env: []
services: [postgres, nats, prefect-server, caddy, grafana]
branch: p3/P3-T009-journal-container-fava-sidecar
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T009 · journal container and Fava sidecar on the internal network

## Goal / expected outcome

A `journal` service (image pinned by digest, `mt_journal` entrypoint) runs on the `core` network with its NATS durable consumers, Prefect worker queue `journal` and health checks; a `fava` sidecar serves the latest Beancount export read-only on the internal network only (reachable via Caddy over Tailscale, never public).

## Context & references

- Roadmap: [T3.40, R3.10](../../../docs/roadmap/phase-3-journal-and-tax.md)
- Containers + networks: [02 §3](../../../docs/02-v1-architecture.md#3-deployment-topology) (`journal` in phase 3, `core` network)
- Optional sidecars: `services/beancount-fava` in [03 §3](../../../docs/03-build-spec.md#3-repository-layout)
- Cross-phase prerequisites (depends_on): P0-T020 (compose stack pinned by digest, incl. Prefect), P0-T021 (Docker networks), P0-T023 (observability containers)
- Write-path buffer: [16 §3.3](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check) (owned by P3-T057)
- Related: P3-T035 (export), P3-T049 (Fava opens it)

## Requirements

- `journal` service: non-root user, read-only root FS, tmpfs for secrets, bind mounts `/srv/mastertrader/journal/inbox` (ro), `/srv/mastertrader/journal/exports` (rw) and `data/attachments/` (rw, content-addressed files referenced by hash from `journal.note`); networks `core` only; resource limits (1–2 CPU, 2 GB RAM baseline).
- Heartbeat `sys.heartbeat.journal` every 5 s; `/healthz` reports DB, NATS consumer lag, last FX update.
- NATS durable consumers: `journal-fills` on `fill.>`, `journal-wallet` on `wallet.*.*.transfer`, explicit ack (only after commit), max-deliver unlimited with backoff; the Postgres-down buffer is the bounded `WORM_BUFFER` stream (default 1 GB or 24 h, configurable) defined in P3-T057.
- `fava` sidecar: pinned digest, serves `/srv/mastertrader/journal/exports/current.beancount` read-only, behind Caddy route `/fava/` with the same session auth as the web app; no egress.
- Grafana panel: journal consumer lag, events/min, quarantine count, last recon result.

## ToDo

- [ ] Add `journal` and `fava` services to `infra/docker-compose.yml` (digests pinned)
- [ ] Caddy route `/fava/*` → `fava:5000` with auth; deny from non-Tailscale
- [ ] Prefect work queue `journal` + worker in the container
- [ ] NATS consumer definitions in `infra/nats/consumers/journal.json`
- [ ] Grafana dashboard JSON `infra/grafana/dashboards/journal.json` + alert rules (lag > 5 s for 5 min; quarantine > 0)
- [ ] Health checks + tests; docs

## Verification

### Tests

- Compose config test: images pinned by digest; `journal` only on `core`; `fava` has no egress.
- Integration: `docker compose up journal fava` healthy; `/healthz` green; a test `fill.TEST` message is consumed and acked.

### Scenarios

- Given NATS restarts, when `journal` reconnects, then the durable consumer resumes without loss or duplicates (writer idempotency).
- Given no export exists yet, when `/fava/` is opened, then Fava shows an empty placeholder ledger (not an error).

### Stress / failure injection

- Kill `journal` mid-batch 10×; after restart consumer lag returns to 0 and no duplicate rows exist.

## Acceptance criteria

- [ ] Both services healthy in compose; images pinned
- [ ] Fava reachable only via Caddy over Tailscale
- [ ] Grafana journal panel + alerts provisioned
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Postgres down → consumer stops acking; writes buffer within the configured bound (default 1 GB or 24 h; above 80% new entries stop, exits continue; [16 §3.3](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check), P3-T057).
- Exports dir full → export job fails loudly, ingestion unaffected.

## Cardinal rules (do NOT)

- Do NOT expose Fava or the journal service on a public interface.
- Do NOT use `latest` tags.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §3.2: add the optional `fava` sidecar row.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.40 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T009-journal-container-fava-sidecar`
- PR title: `P3-T009: journal container and Fava sidecar on the internal network`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T009` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (Postgres-down buffer now the 16 §3.3 bound owned by P3-T057 (P3-B015); attachments mount (P3-B013); explicit P0 depends_on; tools/services filled)
