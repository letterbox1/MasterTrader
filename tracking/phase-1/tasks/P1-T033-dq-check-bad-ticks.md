---
id: P1-T033
kind: task
title: Add the bad-tick check (robust z-score, spread band, crossed book)
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
branch: p1/P1-T033-dq-check-bad-ticks
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T033 · Add the bad-tick check (robust z-score, spread band, crossed book)

## Goal / expected outcome

Outlier prices are caught with a rolling median/MAD robust z-score and a spread band, and crossed or locked books are flagged, so bad ticks never silently feed bars or strategies.

## Context & references

- Roadmap: requirements [R1.10](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.27](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (DQ checks table) · flow [02 §8 F1](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 5 · subjects [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) · degraded modes [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) · UI [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) Quality tab
- Depends on (this phase): P1-T030

## Requirements

- Robust z = |p − median| / (1.4826 · MAD) over a rolling window (default 200 ticks or 60 s); flag above threshold (default 8, configurable per class)
- Trade outside [bid − k·spread, ask + k·spread] (default k=5) → bad tick
- Crossed (bid > ask) or locked (bid == ask) books → `bad` for book-dependent consumers; locked allowed for FX quotes if the venue does so routinely (configured)
- Bad ticks are flagged (not deleted) in the recorder; bar builder excludes flagged ticks and logs the exclusion

## ToDo

- [ ] Implement the checks and flag propagation to the bar builder
- [ ] Fault injection: inject a 10% spike, a crossed book, a locked book
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Fault injection: single spike → flagged, bar unaffected; genuine fast move (many ticks moving together) → not flagged (property test with random walks)
- Unit: MAD = 0 guard (flat markets) uses a floor

### Scenarios

- Given a crossed book for 3 evaluations, when published, then status `bad` with reason `crossed_book` and P2 risk would block orders

### Stress / failure injection

- Property: on 10k simulated random walks with jumps, false-positive rate < 0.1% at default thresholds (recorded)

## Acceptance criteria

- [ ] Injected bad ticks always flagged; false-positive rate recorded in the PR
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Market open auctions and news jumps: the spread band adapts; record and review false positives in T1.04 (P1-T066)

## Cardinal rules (do NOT)

- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT let any path loosen DQ thresholds, risk or alert routing without C3 (Telegram + TOTP + cool-down); tightening is C1.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.27 once every task traced to it in PHASE.md is done; note P1-T033 next to it.
- `docs/03-build-spec.md` §M16: default thresholds

## Branch & PR

- Branch: `p1/P1-T033-dq-check-bad-ticks`
- PR title: `P1-T033: Add the bad-tick check (robust z-score, spread band, crossed book)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T033` run

## Progress log

- 2026-10-21 00:00 · planner · created
