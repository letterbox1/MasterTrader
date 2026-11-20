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
depends_on: [P0-T020, P0-T021, P1-T004, P1-T077]
requirements: [R4.N1, R4.06]
roadmap_todos: [T4.40]
modules: [M2, M3, M21]
dashboards: [D16]
tools: [docker, git, nats, cargo, uv]
mcp: []
env: []
services: [nats, supabase-postgres]
branch: p4/P4-T008-intel-containers-networks
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P4-T008 · Wire Phase 4 containers, networks and NATS accounts

## Goal / expected outcome

`ingest-text`, `crawl4ai`, `nlp`, `ingest-events` and `decision-svc` run under Compose with digest-pinned images, the right networks (`scrape` for fetchers, `core` for processing) and a **narrow NATS account** for scrape-side publishers, so untrusted fetching can only publish raw items to NATS and never reach Supabase Postgres or the signer. Language per [18 §2](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates): `ingest-text` is a group of three scrape-side containers, `mt-feeds` (Rust: RSS/Atom, RSS-Bridge, Discord, Bluesky, Mastodon, Farcaster, GDELT clients), `mt-extract` (Python `mt_extract`: trafilatura) and `mt-telegram-reader` (Python `mt_telegram_reader`: Telethon), one container each so secrets are scoped per process; `nlp` is the Rust `mt-nlp`; `decision-svc` is the tier-B service of the Rust `mt-models` crate, calling the vLLM/llama-server backend (P4-T009) over HTTP; `ingest-events` is the Rust `mt-events`; the core-side writer is the Rust `mt-intel-writer`. `crawl4ai` is a third-party container run unmodified ([19](../../../docs/19-third-party-register.md)). Only `mt-extract` and `mt-telegram-reader` are Python ([18 §2.2](../../../docs/18-platform-and-deployment.md#22-python-uv-workspace-packages-only-where-absolutely-required)).

## Context & references

- Roadmap: [R4.N1, R4.06](../../../docs/roadmap/phase-4-intel.md#3-requirements) · containers listed in the phase header
- Architecture: [02 §3.1](../../../docs/02-v1-architecture.md#31-networks) · [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) · [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats)
- Related: P4-T007 (rss-bridge), P4-T009 (model serving).
- Cross-phase: P0-T020 (T0.41 Compose), P0-T021 (T0.42 networks) and P1-T004 (JetStream stream/KV pattern) are `depends_on` entries; scheduled pollers run as `mt-scheduler` jobs (P1-T077, a `depends_on` entry; Prefect is gone, [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20)). The old P4-T007 dependency was dropped: rss-bridge is wired separately.

## Requirements

- `ingest-text` (`mt-feeds`, `mt-extract`, `mt-telegram-reader`) + `crawl4ai` on `scrape` only; they publish to `raw.text.{source}` with a NATS account allowed **publish-only** on `raw.>` (`raw.text.>`, `raw.evt.>`, `raw.reg.>`), `posture.telegram.>` (structured postures and mentions, no text; F3b) and `sys.heartbeat.*`.
- An `intel-writer` worker (Rust crate `mt-intel-writer`) on `core` (no model clients; DB role limited to INSERT on its tables) persists scrape-side outputs: `raw.evt.>` → `text.geo_event`, `posture.telegram.>` → `text.telegram_mention` / `text.telegram_posture`. `nlp` never subscribes to `posture.telegram.>` or `raw.text.telegram*` ([02 F3b](../../../docs/02-v1-architecture.md#8-end-to-end-flows)).
- `nlp` (`mt-nlp`) on `core`: subscribes `raw.text.>`, writes Supabase Postgres, publishes `text.doc.new`.
- `ingest-events` (Rust crate `mt-events`) on `scrape` publishing `raw.evt.>`; the `intel-writer` on `core` normalises into `text.geo_event` and publishes `evt.{kind}` (same pattern).
- `decision-svc` (`mt-models` tier-B service) on `core`, bound to the internal network, API-key protected.
- JetStream stream `RAW_TEXT` (limits: 7 d, 5 GB), `RAW_EVT` (7 d, 1 GB), `RAW_REG` (30 d, 1 GB), `POSTURE_TG` (7 d, 1 GB); `TEXT_DOC` 24 h. Limits are configurable defaults in `ops/nats/streams/*.json`.
- Every service emits `sys.heartbeat.{service}`; resource limits set (nlp 4 GB RAM; crawl4ai 2 GB).

## ToDo

- [ ] Add the services to the workstation compose file under `infra/` ([18 §3](../../../docs/18-platform-and-deployment.md#3-repository-layout); digest-pinned; read-only FS where possible); `mt-feeds`, `mt-nlp`, `mt-models`, `mt-intel-writer` and `mt-events` images built from `crates/`; `mt-extract` and `mt-telegram-reader` images built from `packages/` with `uv`.
- [ ] Create NATS accounts/users in `ops/nats/accounts.conf`: `scrape` (publish `raw.>` only), `core` (normal).
- [ ] Define JetStream streams in `ops/nats/streams/*.json` and the KV bucket `tierb_scores`; reuse `feed_status` (exists from P1).
- [ ] Add the `intel-writer` service (`mt-intel-writer`) on `core` with its narrow DB role (a Supabase Postgres role, INSERT-only on its tables, no `anon`/`authenticated` access).
- [ ] Add Grafana panels for the new services' heartbeats and stream lag.
- [ ] Network test: from each `ingest-text` container, Supabase Postgres/signer unreachable; publishing outside `raw.>` denied.

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
- [ ] No scrape-side container can reach Supabase Postgres or the signer
- [ ] CI green (`cargo test -p mt-intel-writer`, `cargo test -p mt-events`, `cargo clippy`, `docker compose config`, `pit` bypass check)

## Exceptions & edge cases

- crawl4ai uses a headless browser: keep it on `scrape`, no persistent profile, no cookies stored.

## Cardinal rules (do NOT)

- Do NOT give scrape-side services a Supabase Postgres DSN or core NATS credentials.
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
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (`intel-writer` = Rust `mt-intel-writer`, `ingest-events` = Rust `mt-events`; Supabase Postgres; compose under `infra/`; services postgres → supabase-postgres; tools +cargo; CI commands per 18 (cargo/uv/supabase/pnpm))
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (containers mapped to crates: `mt-feeds`/`mt-extract`/`mt-telegram-reader` (ingest-text group), `mt-nlp`, `mt-models` (decision-svc); P1-T053 Prefect reuse → `mt-scheduler` (depends_on +P1-T077); tools +uv for the two Python images)
