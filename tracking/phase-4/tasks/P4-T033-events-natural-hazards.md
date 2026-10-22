---
id: P4-T033
kind: task
title: Global events: USGS, GDACS, NOAA/NHC and NASA FIRMS
phase: 4
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010, P4-T008]
requirements: [R4.08]
roadmap_todos: [T4.25]
modules: [M3]
dashboards: [D08]
tools: [uv, git]
mcp: []
env: []
services: [nats, postgres]
branch: p4/P4-T033-events-natural-hazards
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-4-intel.md]
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

# P4-T033 · Global events: USGS, GDACS, NOAA/NHC and NASA FIRMS

## Goal / expected outcome

`mt_data.events` ingests natural-hazard events from USGS (earthquake GeoJSON feeds), GDACS (RSS/GeoJSON alerts), NOAA/NHC (active storms, advisories) and NASA FIRMS (active fires, MAP_KEY), normalised into `text.geo_event` with location, severity (0–1), start/update time and source ids. FIRMS is built and tested on recorded fixtures without a key; the live FIRMS run with your `MAP_KEY` is P4-T067 (keys last).

## Context & references

- Roadmap: [R4.08](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.25](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Spec: [03 M3](../../../docs/03-build-spec.md#m3-global-events--mt_dataevents) · [02 §4 M3 row](../../../docs/02-v1-architecture.md#4-logical-components) (`text.geo_event`, `evt.*`)
- Related: P4-T035 (exposure + score), P4-T005 (your FIRMS key), P4-T067 (live check).

## Requirements

- `text.geo_event`: id, source, source_event_id, kind (quake/storm/fire/flood/volcano/conflict/sanctions/pm_move), geometry (point/polygon as GeoJSON), country codes, region, severity (normalised 0–1 with per-source mapping documented), event_time, ingest_time, updates as new rows with `supersedes`.
- Severity maps: USGS magnitude + PAGER alert; GDACS alert level (green/orange/red); NHC category; FIRMS FRP + cluster size near assets of interest.
- Poll: USGS 1 min (significant feed), GDACS 5 min, NHC 15 min, FIRMS 3 h (area of interest bboxes: producing regions).
- Raw publishes on `raw.evt.{source}` (scrape side); normaliser on core writes and publishes `evt.{kind}`.

## ToDo

- [ ] Connectors for the four sources.
- [ ] Severity mapping module with documented tables.
- [ ] Normaliser worker.
- [ ] Fixtures + tests.

## Verification

### Tests
- Unit: each source fixture → `geo_event` with expected severity.
- Unit: update to an existing event → new row with `supersedes`.

### Scenarios
- Given an M7.5 quake near Tokyo, then severity ≥ 0.8 and `evt.quake` fires within 2 min.
- Given FIRMS key invalid, then FIRMS goes `bad` and others continue.

### Stress / failure injection
- Replay a hurricane season week of NHC advisories: no duplicate events; update chain intact.

## Acceptance criteria

- [ ] USGS, GDACS and NHC ingesting live (keyless); FIRMS proven on fixtures; severity mapping documented and tested
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- USGS reviewed vs automatic magnitudes: keep both as update rows.

## Cardinal rules (do NOT)

- Do NOT exceed FIRMS key limits; cache area tiles.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md`: M3: severity mapping table
- `docs/roadmap/phase-4-intel.md`: tick T4.25 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T033-events-natural-hazards`
- PR title: `P4-T033: Global events: USGS, GDACS, NOAA/NHC and NASA FIRMS`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T033` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (build first, keys last: FIRMS on fixtures, live in P4-T067; dropped P4-T005 dependency; added P4-T008 (raw.evt account))
