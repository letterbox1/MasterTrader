---
id: P4-T023
kind: task
title: Farcaster ingestion via a self-hosted Hubble node
phase: 4
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010, P4-T008]
requirements: [R4.05]
roadmap_todos: [T4.22]
modules: [M2]
dashboards: [D07, D08]
tools: [uv, git, docker]
mcp: []
env: []
services: [nats]
branch: p4/P4-T023-farcaster-hubble
pr: ""
doc_sync: [docs/06-aggregators-and-market-providers.md, docs/roadmap/phase-4-intel.md]
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

# P4-T023 · Farcaster ingestion via a self-hosted Hubble node

## Goal / expected outcome

A self-hosted Farcaster **Hubble** node (digest-pinned container, or a free hub endpoint if disk is tight) syncs casts, and `mt_data.text.farcaster` subscribes to its event stream, filtering casts on cashtags/keywords/channels into `raw.text.farcaster` (useful for crypto launch chatter feeding P5).

## Context & references

- Roadmap: [R4.05](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.22](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Sources: [06 §2 Farcaster row](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) · [D08 Additions](../../../docs/ui/dashboards/D08-intel.md)
- Cross-phase: P5 R5.10 discovery.

## Requirements

- Hubble container on the `scrape` network, volume sized and monitored (alert at 80% disk); OP mainnet RPC from free provider config.
- Subscriber uses Hubble gRPC/HTTP `subscribe` from the last event id (persisted).
- Filter by keyword/cashtag/channel (`/base`, `/degen`, …) from config.

## ToDo

- [ ] Compose service for Hubble (digest-pinned) + disk alert.
- [ ] Event subscriber with resume.
- [ ] Filters + publisher + tests.

## Verification

### Tests
- Unit: cast fixtures → matches.
- Integration: replay of recorded hub events → items with resume id.

### Scenarios
- Given Hubble is resyncing, then the source shows `degraded` and nothing is lost after it catches up.
- Given disk > 80%, then alert and pause sync rather than fill the disk.

### Stress / failure injection
- Replay 1 day of casts: filter lag < 10 s.

## Acceptance criteria

- [ ] Hubble synced; filtered casts ingesting for 24 h
- [ ] Disk alert tested
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- If Hubble's disk need is too high for the host, switch to a free hub endpoint (config flag) and document it.
- Postgres down (02 §9.3): raw items stay in `RAW_TEXT` and are processed on recovery; the connector itself never needs the DB.

## Cardinal rules (do NOT)

- Do NOT sign or publish casts.
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT use unpinned images (`:latest`) or vendored code with telemetry/referral IDs; pin by digest.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: §2 Farcaster row: self-hosted vs hub endpoint choice
- `docs/roadmap/phase-4-intel.md`: tick T4.22 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T023-farcaster-hubble`
- PR title: `P4-T023: Farcaster ingestion via a self-hosted Hubble node`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T023` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (added P4-T008 dependency (Hubble container on the scrape network))
