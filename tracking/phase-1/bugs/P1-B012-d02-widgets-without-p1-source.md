---
id: P1-B012
kind: gap
title: D02 macro strip, positioning and nowcasts have no P1 data source
phase: 1
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p1/P1-B012-d02-widgets-without-p1-source
pr: ""
doc_sync: [docs/ui/dashboards/D02-markets.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: done
found_in: docs/ui/dashboards/D02-markets.md /markets widgets vs docs/roadmap/phase-1-data-and-monitoring.md R1.04–R1.06
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Decision recorded in docs/17 (17 §D P1-B003/P1-B004/P1-B012): D02 shows "Arrives in Phase 4" states for P4-fed widgets; P1 widgets named per phase
- [x] Aligned docs carry it: D02 (Macro strip and Positioning rows, "Arrives in P4" section); roadmap R1.15; P4 roadmap R4.11, T4.32
- [x] Affected P1 tasks updated in the 2026-10-22 task alignment: P1-T049, P1-T050

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [x] Docs updated and consistent (D02 (Macro strip and Positioning rows, "Arrives in P4" section); roadmap R1.15; P4 roadmap R4.11, T4.32)
- [x] Decision and owning tasks noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by 17 §D P1-B003/P1-B004/P1-B012; docs carry it (D02 (Macro strip and Positioning rows, "Arrives in P4" section); roadmap R1.15; P4 roadmap R4.11, T4.32); implementation owned by P1-T049, P1-T050
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P1-B003/P1-B004/P1-B012); docs updated: D02 (Macro strip and Positioning rows, "Arrives in P4" section); roadmap R1.15; P4 roadmap R4.11, T4.32; implementation owned by P1-T049, P1-T050
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
