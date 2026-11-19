---
id: P7-T074
kind: task
title: Measure latency-attributable slippage per venue (input to regional engines)
phase: 7
type: RESEARCH
status: backlog
priority: low
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T059]
requirements: [R7.09]
roadmap_todos: []
modules: [M16, M12]
dashboards: [D07, D06]
tools: [git, cargo, supabase]
mcp: []
env: []
services: [supabase-postgres, mt-api]
branch: p7/P7-T074-measure-latency-attributable-slippage-per-venue-
pr: ""
doc_sync: [docs/18-platform-and-deployment.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-19
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P7-T074 · Measure latency-attributable slippage per venue (input to regional engines)

## Goal / expected outcome

**Optional.** A per-venue, per-bot report shows how much of the measured slippage is attributable to latency (engine in Sydney → each venue's matching engine), using M16 TCA data from micro-live (and paper where it is representative). It answers the first condition for a regional engine ([18 §7](../../../docs/18-platform-and-deployment.md#7-latency-and-regions)): is latency-attributable slippage above `deploy.region_min_benefit_bps` over at least `deploy.region_eval_trades` trades? It recommends; it never adds a region.

## Context & references

- Platform: [18 §7](../../../docs/18-platform-and-deployment.md#7-latency-and-regions) (the four conditions for Mode 3) · defaults [16 §2.15](../../../docs/16-configuration-and-safety-model.md#215-platform-deployment-and-regions) (`deploy.region_min_benefit_bps` 2 bps, `deploy.region_eval_trades` 200, `deploy.engine_regions: [syd]`)
- Data: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) TCA (implementation shortfall, time-to-ack per venue)
- Depends on: P7-T059 (micro-live windows produce the live fills). Regional engines themselves are out of scope for Phase 7; no task builds them.
- Related: P7-T073 (runtime host and region), P7-T071 (host choice)

## Requirements

- For each venue and bot with ≥ `deploy.region_eval_trades` live (or paper) fills: decompose implementation shortfall into spread, fees, market impact and a **latency component** (price move between decision time and venue ack, regressed on measured time-to-ack); report bps per trade with a confidence interval.
- Measure round-trip latency from the runtime host to each venue's API endpoint (median, p95) at different times of day; record the venue's matching-engine region where it is published (U otherwise).
- Output: a report in `mt-monitor` (`/monitor/latency-report`, read-only) and a short summary in this task's progress log: per venue, "below / above `deploy.region_min_benefit_bps`" and whether conditions 2–4 of 18 §7 could hold (jurisdiction from the venue registry; static IP and keys per region; risk-budget slices).
- Values come from settings (16 §2.15); nothing hard-coded.

## ToDo

- [ ] Latency-component estimator over M16 TCA rows in `crates/mt-monitor/src/tca/latency.rs`
- [ ] Latency probe from the runtime host per venue (read-only endpoints, within rate limits)
- [ ] Report query `/monitor/latency-report` (read-only) and progress-log summary
- [ ] Tests; docs

## Verification

### Tests
- `cargo test -p mt-monitor tca::latency`: synthetic fills with a known injected latency cost recover it within 10%; zero injected latency → component not significant.

### Scenarios
- Given 250 live fills on a venue with 1.2 bps latency-attributable slippage, then the report says "below threshold (2 bps): no regional engine".
- Given fewer than `deploy.region_eval_trades` fills, then the report says "insufficient sample" and makes no recommendation.

### Stress / failure injection
- n/a: offline analysis over stored TCA rows.

## Acceptance criteria

- [ ] Report covers every live venue with a sample-size note
- [ ] Recommendation per venue against `deploy.region_min_benefit_bps`, with conditions 2–4 of 18 §7 noted

## Exceptions & edge cases

- Venues without published matching-engine locations: latency measured to the API endpoint only, marked (U).
- Minute-to-day strategies: the latency component is expected to be noise; the report says so rather than forcing a number.

## Cardinal rules (do NOT)

- Do NOT add a region, a VM or a key allow-list entry; adding a region is C3 and needs all four 18 §7 conditions.
- Do NOT pick a region to reach a venue or product you couldn't otherwise use (no location masking, 12 §3).
- Do NOT place orders to measure latency; use read-only endpoints and existing fills.
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`.

## Doc sync on completion

- `docs/18-platform-and-deployment.md` §7: replace the (U) latency figures with the measured ones.
- `docs/roadmap/phase-7-prove-and-go-live.md`: note the result (no ToDo exists for it).

## Branch & PR

- Branch: `p7/P7-T074-measure-latency-attributable-slippage-per-venue-`
- PR title: `P7-T074: Measure latency-attributable slippage per venue (input to regional engines)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T074` run

## Progress log

- 2026-11-19 09:37 · cloud:vm:be04b6ae61f8 · created
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (new optional RESEARCH task: input to regional engines, 18 §7; depends on micro-live data P7-T059)
