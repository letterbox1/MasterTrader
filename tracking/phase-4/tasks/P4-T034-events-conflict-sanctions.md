---
id: P4-T034
kind: task
title: Global events: ReliefWeb, UCDP, GDELT events, OpenSanctions and ACLED
phase: 4
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010, P4-T005, P4-T013]
requirements: [R4.08]
roadmap_todos: [T4.25]
modules: [M3]
dashboards: [D08]
branch: p4/P4-T034-events-conflict-sanctions
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T034 · Global events: ReliefWeb, UCDP, GDELT events, OpenSanctions and ACLED

## Goal / expected outcome

Humanitarian, conflict and sanctions events from ReliefWeb (disasters API), UCDP (candidate events API), GDELT events export (from P4-T013), OpenSanctions (daily delta of sanctioned entities/vessels) and ACLED (research account, if granted) are normalised into `text.geo_event` with severity, country and novelty inputs.

## Context & references

- Roadmap: [R4.08](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.25](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Spec: [03 M3](../../../docs/03-build-spec.md#m3-global-events--mt_dataevents)
- Related: P4-T005 (ACLED/OpenSanctions terms), P4-T013 (GDELT).

## Requirements

- ReliefWeb daily + 1-h new disasters; UCDP candidate events monthly/weekly releases; GDELT events filtered to CAMEO root codes 14–20 (protest → conflict) with Goldstein scale for severity; OpenSanctions daily delta (new designations on countries/entities in the exposure map); ACLED weekly pull (research-only flag `commercial_ok=false`).
- GDELT event noise control: require ≥ N mentions (default 10) and ≥ 3 sources before an event is created.
- Sanctions events carry entity names and countries for exposure mapping (country → FX/index).

## ToDo

- [ ] Connectors for ReliefWeb, UCDP, OpenSanctions, ACLED; GDELT events consumer.
- [ ] Severity mapping (Goldstein, fatalities bands, sanction scope).
- [ ] Fixtures + tests.

## Verification

### Tests
- Unit: each fixture → events with expected severity/country.
- Unit: GDELT threshold filter removes single-source noise.

### Scenarios
- Given ACLED access was not granted, then the source is disabled with reason and UCDP/GDELT cover conflict.
- Given a new sanctions package on a country, then one aggregated sanctions event is created, not one per entity.

### Stress / failure injection
- Process a GDELT events backlog of 1 day: noise filter keeps event count manageable (< 500/day) — record actual.

## Acceptance criteria

- [ ] Sources ingesting (or disabled with reason); severity mapping tested
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- UCDP releases lag; mark `event_time` as the event date and `ingest_time` as now (PIT-safe).

## Cardinal rules (do NOT)

- Do NOT use ACLED data outside research/personal use (`commercial_ok=false`).
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md`: M3: list event sources and filters
- `docs/roadmap/phase-4-intel.md`: tick T4.25 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T034-events-conflict-sanctions`
- PR title: `P4-T034: Global events: ReliefWeb, UCDP, GDELT events, OpenSanctions and ACLED`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T034` run

## Progress log

- 2026-10-21 00:00 · planner · created
