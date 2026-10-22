---
id: P4-T064
kind: task
title: Venue status, incident and proof-of-reserve watch feeding venue health
phase: 4
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T063, P1-T043]
requirements: [R4.15]
roadmap_todos: [T4.30]
modules: [M16, M5]
dashboards: [D07, D06]
tools: [uv, git]
mcp: []
env: []
services: [postgres, nats, prefect-server]
branch: p4/P4-T064-venue-status-incident-and-proof-of-reserve-watch
pr: ""
doc_sync: [docs/06-aggregators-and-market-providers.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P4-T064 · Venue status, incident and proof-of-reserve watch feeding venue health

## Goal / expected outcome

Each venue's official status page / incident feed, announcements page and proof-of-reserve page are watched with the P4-T063 machinery, and changes update the venue-health inputs of `ops.venue_registry` built in P1 (P1-T043), so D07/D06 show incidents and PoR changes next to our own measured withdrawal times. A material change also raises a `REG_CHANGE` review task; venue status is **never** loosened automatically.

## Context & references

- Roadmap: [R4.15](../../../docs/roadmap/phase-4-intel.md#3-requirements) (venue status pages feed venue health) · ToDo [T4.30](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Venue health inputs: [06 Regulatory & venue watch → Venue health inputs](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) · [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) · [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P1-B014: own withdrawal times + status pages via this watch + quarterly AUSTRAC USER check)
- Cross-phase (`depends_on`): P1-T043 (venue-health collector and `ops.venue_registry` health fields; R1.13 names this watch as its status-page input once P4 lands)
- Related: P4-T063 (fetch/diff machinery).

## Requirements

- `regwatch.yaml` gains a `venues` group: per venue `status_url` (prefer official JSON/RSS status APIs, e.g. Statuspage `/api/v2/summary.json`), `announcements_url`, `por_url`, cadence (configurable default: status 5 min, announcements 1 h, PoR 24 h).
- Status/incident changes map to the P1-T043 health fields (`status`, `incident_open`, `incident_note`, `por_updated_at`) as new versioned rows; a major incident or withdrawal suspension raises `alert.warning.venue_health` and a `REG_CHANGE` task.
- Health changes can only **tighten** automatically (e.g. mark `degraded` → M11 treats it per the registry rules); restoring a venue to healthy after an incident is your C-level action, never automatic.
- Sources are official venue pages only; no third-party status aggregators.

## ToDo

- [ ] Venue entries in `regwatch.yaml` for every venue in `ops.venue_registry`
- [ ] Status-API parsers (Statuspage JSON, RSS) + page fallback via P4-T063
- [ ] Mapper to P1-T043 health fields + alert + `REG_CHANGE` task on material change
- [ ] Fixtures (normal, incident open, incident resolved, PoR update) and tests
- [ ] Update docs listed under Doc sync

## Verification

### Tests
- Unit: Statuspage fixture with an open incident → `incident_open = true`, alert raised.
- Unit: incident resolved → note recorded, venue **not** auto-restored (needs your action).
- Integration: PoR page change → `por_updated_at` + one `REG_CHANGE` task.

### Scenarios
- Given a venue posts 'withdrawals suspended', then D07 shows it within one status cadence and an alert fires.
- Given the status page is unreachable, then the input is `stale` (not 'healthy') and our own withdrawal-time signal still applies.

### Stress / failure injection
- n/a: a few dozen low-frequency fetches; correctness focus.

## Acceptance criteria

- [ ] Every registry venue has a watched status source (or a recorded reason why not)
- [ ] Health fields update from fixtures; only tightening is automatic (test)
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Venues without a status page: rely on announcements + our measured withdrawal times; recorded in the registry.
- AUSTRAC register stays a quarterly USER check (no API); this task doesn't automate it.

## Cardinal rules (do NOT)

- Do NOT loosen a venue's status or limits automatically.
- Do NOT scrape third-party status aggregators.
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: venue health inputs: the status sources as built
- `docs/roadmap/phase-4-intel.md`: tick T4.30 (with P4-T063)

## Branch & PR

- Branch: `p4/P4-T064-venue-status-incident-and-proof-of-reserve-watch`
- PR title: `P4-T064: Venue status, incident and proof-of-reserve watch feeding venue health`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T064` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (R4.15 / T4.30 venue-status inputs per 16 §4.3 and 17 §D P1-B014)
