---
id: P4-T008
kind: task
title: Wire Phase 4 containers, networks and NATS accounts
phase: 4
type: OPS
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T020, P0-T021, P1-T004]
requirements: [R4.N1, R4.06]
roadmap_todos: [T4.40]
modules: [M2, M3, M21]
dashboards: [D16]
tools: [docker, git, nats]
mcp: []
env: []
services: [nats, postgres]
branch: p4/P4-T008-intel-containers-networks
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-4-intel.md]
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

# P4-T008 · Wire Phase 4 containers, networks and NATS accounts

## Goal / expected outcome

`ingest-text`, `crawl4ai`, `nlp`, `ingest-events` and `decision-svc` run under Compose with digest-pinned images, the right networks (`scrape` for fetchers, `core` for processing) and a **narrow NATS account** for scrape-side publishers, so untrusted fetching can only publish raw items to NATS and never reach Postgres or the signer.

## Context & references

- Roadmap: [R4.N1, R4.06](../../../docs/roadmap/phase-4-intel.md#3-requirements) · containers listed in the phase header
- Architecture: [02 §3.1](../../../docs/02-v1-architecture.md#31-networks) · [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) · [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats)
- Related: P4-T007 (rss-bridge), P4-T009 (model serving).
- Cross-phase: P0-T020 (T0.41 Compose), P0-T021 (T0.42 networks) and P1-T004 (JetStream stream/KV pattern) are `depends_on` entries; P1-T053 (Prefect schedules) is reused. The old P4-T007 dependency was dropped: rss-bridge is wired separately.

## Requirements

- `ingest-text` + `crawl4ai` on `scrape` only; they publish to `raw.text.{source}` with a NATS account allowed **publish-only** on `raw.>` (`raw.text.>`, `raw.evt.>`, `raw.reg.>`), `posture.telegram.>` (structured postures and mentions, no text; F3b) and `sys.heartbeat.*`.
- An `intel-writer` worker on `core` (no model clients; DB role limited to INSERT on its tables) persists scrape-side outputs: `raw.evt.>` → `text.geo_event`, `posture.telegram.>` → `text.telegram_mention` / `text.telegram_posture`. `nlp` never subscribes to `posture.telegram.>` or `raw.text.telegram*` ([02 F3b](../../../docs/02-v1-architecture.md#8-end-to-end-flows)).
- `nlp` on `core`: subscribes `raw.text.>`, writes Postgres, publishes `text.doc.new`.
- `ingest-events` on `scrape` publishing `raw.evt.>`; the `intel-writer` on `core` normalises into `text.geo_event` and publishes `evt.{kind}` (same pattern).
- `decision-svc` on `core`, bound to the internal network, API-key protected.
- JetStream stream `RAW_TEXT` (limits: 7 d, 5 GB), `RAW_EVT` (7 d, 1 GB), `RAW_REG` (30 d, 1 GB), `POSTURE_TG` (7 d, 1 GB); `TEXT_DOC` 24 h. Limits are configurable defaults in `ops/nats/streams/*.json`.
- Every service emits `sys.heartbeat.{service}`; resource limits set (nlp 4 GB RAM; crawl4ai 2 GB).

## ToDo

- [ ] Add the services to `docker-compose.yml` (digest-pinned; read-only FS where possible).
- [ ] Create NATS accounts/users in `ops/nats/accounts.conf`: `scrape` (publish `raw.>` only), `core` (normal).
- [ ] Define JetStream streams in `ops/nats/streams/*.json` and the KV bucket `tierb_scores`; reuse `feed_status` (exists from P1).
- [ ] Add the `intel-writer` service on `core` with its narrow DB role.
- [ ] Add Grafana panels for the new services' heartbeats and stream lag.
- [ ] Network test: from `ingest-text`, Postgres/signer unreachable; publishing outside `raw.>` denied.

## Verification

### Tests
- Integration: publish to `text.doc.new` from the scrape account is rejected (permissions violation).
- Integration: end-to-end `raw.text.rss` → `nlp` consumer receives it.
- Network: port probe from scrape-side containers to `postgres:5432` fails.

### Scenarios
- Given `nlp` is down, when `ingest-text` publishes, then raw items queue in `RAW_TEXT` (bounded 7 d / 5 GB) and are processed on recovery.
- Given a malicious page tries SSRF to `http://postgres:5432`, then the request fails at the network layer.

### Stress / failure injection
- Fill `RAW_TEXT` to its limit: oldest messages discarded per policy, alert `alert.warning.stream_full`, no crash.

## Acceptance criteria

- [ ] All five services healthy on `docker compose up`
- [ ] Scrape-side publish permissions restricted to `raw.>` (test proves it)
- [ ] No scrape-side container can reach Postgres or the signer
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- crawl4ai uses a headless browser: keep it on `scrape`, no persistent profile, no cookies stored.

## Cardinal rules (do NOT)

- Do NOT give scrape-side services a Postgres DSN or core NATS credentials.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT use unpinned images (`:latest`) or vendored code with telemetry/referral IDs; pin by digest.

## Doc sync on completion

- `docs/02-v1-architecture.md`: §3.2/§6: add `raw.text.>`/`raw.evt.>` subjects and the scrape NATS account
- `docs/roadmap/phase-4-intel.md`: tick T4.40 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T008-intel-containers-networks`
- PR title: `P4-T008: Wire Phase 4 containers, networks and NATS accounts`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T008` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (F3/F3b split (17 §A P4-B001): scrape account may publish posture.telegram.> and raw.reg.>, core intel-writer persists postures; dropped P4-T007 dep; explicit P0/P1 depends_on)
