---
id: P1-T036
kind: task
title: Add the book-integrity check (checksums and REST snapshots)
phase: 1
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T030, P1-T010]
requirements: [R1.10]
roadmap_todos: [T1.27]
modules: [M16]
dashboards: [D07]
tools: [git, uv, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p1/P1-T036-dq-check-book-integrity
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

# P1-T036 · Add the book-integrity check (checksums and REST snapshots)

## Goal / expected outcome

Local L2 books are verified against venue checksums where offered and against periodic REST snapshots elsewhere; a mismatch marks the book `bad` and forces a resync.

## Context & references

- Roadmap: requirements [R1.10](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.27](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (DQ checks table) · flow [02 §8 F1](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 5 · subjects [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) · degraded modes [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) · UI [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) Quality tab (Book integrity: venue checksums; periodic REST snapshot reconciliation)
- Depends on (this phase): P1-T030, P1-T010

## Requirements

- Checksum validation for venues that send one (OKX, Kraken; others as available) on every update
- Periodic REST snapshot (default every 5 min per L2 symbol, staggered, via quota tracker) compared to the local book on top N levels (default 20): price/size mismatch beyond tolerance → incident
- Mismatch → `bad` + resync request to the connector; counts per venue in D07

## ToDo

- [ ] Implement checksum validators per venue and the snapshot comparator
- [ ] Fault injection: corrupt one level, drop one diff
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Fault injection: corrupted level → checksum mismatch detected on next update; dropped diff → snapshot mismatch within one interval
- Unit: CRC32 implementation vs venue reference examples

### Scenarios

- Given snapshot comparison races with in-flight diffs, when compared, then the comparator aligns on the snapshot's update ID and avoids false mismatches

### Stress / failure injection

- Quota: snapshot cadence for all L2 symbols stays under 50% of REST weight budget (asserted in test from quota config)

## Acceptance criteria

- [ ] Injected book corruption always detected; resync recovers the book
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Venue drops checksum support: falls back to snapshots with a logged downgrade

## Cardinal rules (do NOT)

- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT let any path loosen DQ thresholds, risk or alert routing without C3 (Telegram + TOTP + cool-down; in P1 via the break-glass CLI `mtctl approve` + TOTP); tightening is C1.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.27 once every task traced to it in PHASE.md is done; note P1-T036 next to it.
- `docs/03-build-spec.md` §M16: per-venue integrity method

## Branch & PR

- Branch: `p1/P1-T036-dq-check-book-integrity`
- PR title: `P1-T036: Add the book-integrity check (checksums and REST snapshots)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T036` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields)
