---
id: P1-B012
kind: gap
title: D02 macro strip, positioning and nowcasts have no P1 data source
phase: 1
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.15]
roadmap_todos: []
modules: []
dashboards: []
branch: p1/P1-B012-d02-widgets-without-p1-source
pr: ""
doc_sync: [docs/ui/dashboards/D02-markets.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: docs/ui/dashboards/D02-markets.md /markets widgets vs docs/roadmap/phase-1-data-and-monitoring.md R1.04–R1.06
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-B012 · D02 macro strip, positioning and nowcasts have no P1 data source

## Goal / expected outcome

D02 marks which widgets are P1 (rates, yields, VIX via yfinance, gold, oil, COT) and which arrive in P4 (sentiment, books, prediction markets, nowcasts)

## Context & references

- Found in: [D02 Markets](../../../docs/ui/dashboards/D02-markets.md) (phase 1) shows nowcasts (GDPNow, Cleveland inflation), DXY proxy, VIX, retail sentiment (Myfxbook / IG / OANDA books) and Kalshi/Polymarket probabilities; none are P1 requirements ([06 §3 Reports, nowcasts & forecasts](../../../docs/06-aggregators-and-market-providers.md#reports-nowcasts--forecasts-m6-features-m5-release-events))
- Related items: P1-T049

## Requirements

- **Where:** [D02 Markets](../../../docs/ui/dashboards/D02-markets.md) (phase 1) shows nowcasts (GDPNow, Cleveland inflation), DXY proxy, VIX, retail sentiment (Myfxbook / IG / OANDA books) and Kalshi/Polymarket probabilities; none are P1 requirements ([06 §3 Reports, nowcasts & forecasts](../../../docs/06-aggregators-and-market-providers.md#reports-nowcasts--forecasts-m6-features-m5-release-events))
- **Expected:** D02 marks which widgets are P1 (rates, yields, VIX via yfinance, gold, oil, COT) and which arrive in P4 (sentiment, books, prediction markets, nowcasts)
- **Actual:** Unassigned widget data; risk of fake placeholder data, which DESIGN §10 forbids
- **Suggested fix:** Annotate D02 widgets by phase; add nowcast/positioning ingestion to the P4 roadmap
- **Impact:** D02 incomplete or misleading in P1 (severity S3)

## ToDo

- [ ] Edit D02 and note in the P4 roadmap
- [ ] Update the affected P1 task files if the decision changes their requirements

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [ ] Docs updated and consistent
- [ ] Root cause and decision noted in the progress log

## Exceptions & edge cases

- Until fixed, related tasks follow the interim rule stated in their own files

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a number in code; the decision lands in the docs first
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/ui/dashboards/D02-markets.md`: apply the fix above
- `docs/roadmap/phase-4-intel.md`: apply the fix above

## Branch & PR

- Branch: `p1/P1-B012-d02-widgets-without-p1-source`
- PR title: `P1-B012: D02 macro strip, positioning and nowcasts have no P1 data source`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-B012` run

## Progress log

- 2026-10-21 00:00 · planner · opened
