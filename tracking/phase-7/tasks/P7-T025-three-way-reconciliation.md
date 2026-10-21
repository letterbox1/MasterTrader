---
id: P7-T025
kind: task
title: Three-way reconciliation: venue vs engine vs journal
phase: 7
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.09]
roadmap_todos: [T7.23]
modules: [M16, M12, M18]
dashboards: [D07, D05, D14]
branch: p7/P7-T025-three-way-reconciliation
pr: ""
doc_sync: [docs/03-build-spec.md, docs/ui/dashboards/D07-data-quality.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T025 · Three-way reconciliation: venue vs engine vs journal

## Goal / expected outcome

Every N minutes (default 5) and at end of day, positions, open orders, balances and fills are compared across the venue (read-only key), the engine's in-memory/portfolio state and the journal; each difference is classified explained/unexplained and written to `audit.recon` with its age.

## Context & references

- Roadmap: [R7.09 · ToDo T7.23](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (reconciliation every N minutes and EOD; mismatch = incident) · [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) (venue disconnect → unconfirmed) · [12 §3](../../../docs/12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention) (STP cancels recorded as non-fills) · [D07](../../../docs/ui/dashboards/D07-data-quality.md) Reconciliation tab · [D05](../../../docs/ui/dashboards/D05-execution.md) (reconciliation status per position)
- Cross-phase: P1 T1.29 (venue recon jobs, practice accounts), P3 T3.28 (journal ↔ venue recon). This task joins them into one three-way job for live sub-accounts.
- Related: P7-T026 (unconfirmed state), P7-T027 (24 h ageing → halt), P7-T050 (fault injection), gap P7-B007 (N and tolerances unspecified)

## Requirements

- Sides: venue (REST via read-only key, rate-limit aware from live headers), engine (Nautilus portfolio/cache snapshot via `pos.{account}`), journal (`journal.*` positions/balances).
- Interval: every 5 min per live sub-account (configurable 1–15), plus EOD at 00:05 UTC; on-demand `data.recon.run` (C1).
- Tolerances: quantity exact to venue lot size; balances within max(1 minor unit, 0.01% ); fees within 1 minor unit.
- Auto-explanations (each with rule id): fill in flight (< 30 s old), STP cancel (non-fill), fee rounding, funding settlement timing (± 5 min of funding time), pending deposit/withdrawal (manual, recorded). Everything else is `unexplained` with `first_seen_at`.
- Outputs: `audit.recon` rows (WORM), NATS `recon.{account}`, D07/D05/D14 status; an unexplained break raises `alert.warning.recon` immediately and stays visible until resolved by a correction row.
- Resolution is a new row (`resolution_of`) with reason; never an edit.

## ToDo

- [ ] `packages/mt_monitor/recon/three_way.py` with side adapters (venue via ccxt/native read-only; engine snapshot RPC; journal SQL).
- [ ] Explanation rules module with unit-tested rule ids.
- [ ] Scheduler (monitor service loop) + EOD Prefect flow.
- [ ] `data.recon.resolve` command (C1, reason required) writing resolution rows.
- [ ] D07 Reconciliation tab: three columns (venue/engine/journal), age, rule, resolve action.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: each explanation rule with positive/negative fixtures.
- Integration (testnet/paper venues): clean run → zero breaks; injected phantom position on engine side → unexplained break within one interval.
- WORM: recon rows immutable; resolution creates a new row.

### Scenarios
- Given an STP cancel, then recon marks the missing fill as explained (rule `stp_cancel`) and the journal shows a non-fill.
- Given the journal is missing a fee event, then an unexplained balance break appears with venue vs journal values.
- Given venue REST rate-limited, then the run is `incomplete` (not clean) and retries with backoff.

### Stress / failure injection
- 10 sub-accounts × 5-min interval for 24 h on testnets: no missed runs; venue 418/429 responses respected (no retry storms); run duration p95 < 30 s.

## Acceptance criteria

- [ ] Three-way recon runs on every live sub-account at the configured interval and EOD.
- [ ] Breaks classified with rule ids and ages; unexplained breaks alert immediately.
- [ ] CI green.

## Exceptions & edge cases

- Venue maintenance window: run `incomplete`, not clean; ageing continues for existing breaks.
- Engine restarted: engine side rebuilt from venue before resuming (P7-T026).
- Clock skew: compare using exchange timestamps; chrony offset > 500 ms raises DQ.

## Cardinal rules (do NOT)

- Do NOT 'fix' a break by editing journal or audit rows; append corrections.
- Do NOT use trade keys for recon; read-only keys only.
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M16: three-way recon, interval and rules.
- `docs/ui/dashboards/D07-data-quality.md`: three-column recon view.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.23 when this item is done.

## Branch & PR

- Branch: `p7/P7-T025-three-way-reconciliation`
- PR title: `P7-T025: Three-way reconciliation: venue vs engine vs journal`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T025` run

## Progress log

- 2026-10-21 00:00 · planner · created
