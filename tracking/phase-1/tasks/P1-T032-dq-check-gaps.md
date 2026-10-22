---
id: P1-T032
kind: task
title: Add the gap check (sequence IDs, trade IDs, bar counts)
phase: 1
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T030]
requirements: [R1.10]
roadmap_todos: [T1.27]
modules: [M16]
dashboards: [D07]
tools: [git, uv, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p1/P1-T032-dq-check-gaps
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
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

# P1-T032 · Add the gap check (sequence IDs, trade IDs, bar counts)

## Goal / expected outcome

Gaps are detected from exchange sequence IDs, trade-ID continuity and expected bar counts, recorded as incidents and summarised in a per-instrument gap report used by the soak.

## Context & references

- Roadmap: requirements [R1.10](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.27](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (DQ checks table) · flow [02 §8 F1](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 5 · subjects [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) · degraded modes [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) · UI [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) Quality tab
- Depends on (this phase): P1-T030

## Requirements

- Stream gaps: `seq != prev_seq + 1` (per venue rules; Binance diff `U == last_u + 1`, trade IDs monotonic +1 where the venue guarantees it)
- Bar gaps: expected 1m bars per session vs present (crypto 1440/day; equities per `exchange_calendars`; FX per broker session) from Timescale
- Gap severity: book sequence gap → `bad` until resync; trade-ID gap → `degraded` with count
- Gap report `mt-monitor gaps --from --to` (per instrument: gaps, total missing seconds, longest) used by P1-T065

## ToDo

- [ ] Implement stream and bar gap checks
- [ ] Implement the report CLI/flow
- [ ] Fault-injection tests via the harness (drop sequence IDs)
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Fault injection: drop 1, 10 and 1000 sequence IDs → correct counts, `bad` for book gaps until resync
- Unit: venues without contiguous trade IDs are exempt (configured), no false positives

### Scenarios

- Given a reconnect, when the first message after it has a higher seq, then one gap incident spans the disconnect and the stale incident links to it

### Stress / failure injection

- Load: 1 week of bars for 50 instruments; report generation < 30 s

## Acceptance criteria

- [ ] Dropped sequence IDs always detected in the fault suite; gap report produced
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Venue resets sequence numbers daily or on reconnect: handled per venue rule, not flagged

## Cardinal rules (do NOT)

- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT let any path loosen DQ thresholds, risk or alert routing without C3 (Telegram + TOTP + cool-down; in P1 via the break-glass CLI `mtctl approve` + TOTP); tightening is C1.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.27 once every task traced to it in PHASE.md is done; note P1-T032 next to it.
- `docs/03-build-spec.md` §M16: per-venue sequence rules

## Branch & PR

- Branch: `p1/P1-T032-dq-check-gaps`
- PR title: `P1-T032: Add the gap check (sequence IDs, trade IDs, bar counts)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T032` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields)
