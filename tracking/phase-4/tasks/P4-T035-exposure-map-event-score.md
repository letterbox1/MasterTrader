---
id: P4-T035
kind: task
title: Exposure map and event score (severity × exposure × novelty)
phase: 4
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T033, P4-T034, P2-T120]
requirements: [R4.08]
roadmap_todos: [T4.25]
modules: [M3, M6]
dashboards: [D08, D02]
tools: [uv, git]
mcp: []
env: []
services: [postgres, nats]
branch: p4/P4-T035-exposure-map-event-score
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

# P4-T035 · Exposure map and event score (severity × exposure × novelty)

## Goal / expected outcome

`text.exposure_map` links locations to assets (country → FX pair/equity index/bond ETF; region → commodity, e.g. Gulf of Mexico → crude/natgas, Brazil → coffee/sugar/soy, Chile/Peru → copper) and every geo event gets an **event score = severity × exposure × novelty** per affected instrument, published on `evt.{kind}` and stored as a feature series.

## Context & references

- Roadmap: [R4.08](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.25](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Spec: [03 M3](../../../docs/03-build-spec.md#m3-global-events--mt_dataevents) (exposure map; event score) · [03 M6](../../../docs/03-build-spec.md#m6-features--mt_features) (event scores as features)
- UI: [D08 Events](../../../docs/ui/dashboards/D08-intel.md) (exposure-map links, event score)
- Cross-phase: P2-T120 (feature registry, R2.46) is a `depends_on` entry.

## Requirements

- Exposure map as versioned YAML `config/intel/exposure_map.yaml` loaded into `text.exposure_map` (location key, instrument id, weight 0–1, rationale); seed ≥ 40 countries/regions covering the P1 universe.
- Exposure = max weight over the event's countries/regions (polygons intersect region shapes from Natural Earth, public domain).
- Novelty = 1 − similarity to events of same kind/location in the past 7 days (time-decayed count).
- Score in [0,1]; `features.value` series `event_score.{instrument}` (max over active events) for M6.
- Payload on `evt.{kind}`: event id, instruments with scores, top score.

## ToDo

- [ ] Exposure map YAML + loader + Natural Earth shapes.
- [ ] Scorer + novelty memory.
- [ ] Feature writer + publisher.
- [ ] Tests.

## Verification

### Tests
- Unit: hurricane in Gulf polygon → CL/NG exposure high.
- Unit: repeated aftershocks → novelty decays.
- Property: score monotonic in severity with exposure/novelty fixed.

### Scenarios
- Given a strike in Chilean copper mines (GDELT), then HG gets an event score and D08 shows the link.
- Given an event in a country with no mapping, then score 0 and listed as 'unmapped' for review.

### Stress / failure injection
- n/a: low volume; computation is O(events × regions).

## Acceptance criteria

- [ ] Exposure map seeded and versioned
- [ ] Event scores visible in `/intel/events` and as features
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Maritime events (no country): use region polygons (straits, gulfs).

## Cardinal rules (do NOT)

- Do NOT hard-code exposures in code; YAML only.
- Do NOT skip, weaken or delete a test to get green.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.

## Doc sync on completion

- `docs/03-build-spec.md`: M3: exposure map format and score formula details
- `docs/roadmap/phase-4-intel.md`: tick T4.25 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T035-exposure-map-event-score`
- PR title: `P4-T035: Exposure map and event score (severity × exposure × novelty)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T035` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (explicit cross-phase depends_on P2-T120 (feature registry))
