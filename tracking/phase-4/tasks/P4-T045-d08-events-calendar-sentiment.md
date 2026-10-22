---
id: P4-T045
kind: task
title: D08 Intel: Events, Calendar (blackout markers) and Sentiment tabs
phase: 4
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T043, P4-T040]
requirements: [R4.13, R4.10]
roadmap_todos: [T4.29]
modules: [M3, M5, M6]
dashboards: [D08]
tools: [pnpm, node>=20, git]
mcp: []
env: []
services: [mt-api]
branch: p4/P4-T045-d08-events-calendar-sentiment
pr: ""
doc_sync: [docs/ui/dashboards/D08-intel.md, docs/roadmap/phase-4-intel.md]
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

# P4-T045 · D08 Intel: Events, Calendar (blackout markers) and Sentiment tabs

## Goal / expected outcome

The Events tab (map ≥ md with MapLibre, list < md; severity, location, exposure-map links, event score), the Calendar tab (consensus/actual/previous/surprise, CB meetings, earnings, IPOs, COT/EIA/WASDE days, holidays, **blackout markers** from the same API as M11, filters) and the Sentiment tab (index over time, mention volume, sentiment vs price, retail positioning, prediction-market probabilities) are live.

## Context & references

- Roadmap: [R4.13, R4.10](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.29](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- UI spec: [D08 tabs](../../../docs/ui/dashboards/D08-intel.md) · [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)
- Related: P4-T038 (blackouts), P4-T035 (events), P4-T040/T041 (features).
- Blackout defaults shown: [16 §2.8](../../../docs/16-configuration-and-safety-model.md#28-calendar-blackouts) (15 min either side of high-importance events, `event_sensitive` bots); the UI only renders what the API returns.

## Requirements

- Map uses MapLibre with a free/self-hosted tile source (no paid key); list view below md.
- Calendar blackout windows come only from `/intel/calendar?with_blackouts=1` (D08 acceptance 2: same source of truth as M11).
- 'Add calendar blackout rule' links to D06 Policy → Blackouts (C1/C3 decided there).
- Times rendered in the user's timezone (default Australia/Sydney) with UTC on hover.

## ToDo

- [ ] Events tab (map + list).
- [ ] Calendar tab + blackout markers + filters.
- [ ] Sentiment tab charts (lightweight-charts) + positioning + PM probabilities.
- [ ] Playwright specs + axe.

## Verification

### Tests
- Playwright: a seeded NFP event shows a blackout marker matching `/risk/state` active blackouts.
- Unit: timezone rendering around DST.

### Scenarios
- Given width < md, then events show as a list and the map is not loaded.
- Given a rule changes in D06, then markers update via WS `cal`/`risk.state`.

### Stress / failure injection
- n/a: low-volume views; covered by P4-T059 viewport matrix.

## Acceptance criteria

- [ ] Events/Calendar/Sentiment tabs per spec
- [ ] Blackout markers match M11 (test)
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, viewport matrix + axe)

## Exceptions & edge cases

- Map tiles unavailable: fall back to list with a notice.

## Cardinal rules (do NOT)

- Do NOT compute blackouts client-side.
- Do NOT use paid map tile keys.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/dashboards/D08-intel.md`: mark Events/Calendar/Sentiment implemented; tile source used
- `docs/roadmap/phase-4-intel.md`: tick T4.29 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T045-d08-events-calendar-sentiment`
- PR title: `P4-T045: D08 Intel: Events, Calendar (blackout markers) and Sentiment tabs`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T045` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (blackout markers follow 16 §2.8 defaults via the API (no client-side rule))
