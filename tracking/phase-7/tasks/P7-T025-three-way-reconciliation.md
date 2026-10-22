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
depends_on: [P1-T041, P1-T042, P3-T034]
requirements: [R7.09]
roadmap_todos: [T7.23]
modules: [M16, M12, M18]
dashboards: [D07, D05, D14]
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, nats, prefect-server]
branch: p7/P7-T025-three-way-reconciliation
pr: ""
doc_sync: [docs/03-build-spec.md, docs/ui/dashboards/D07-data-quality.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T025 · Three-way reconciliation: venue vs engine vs journal

## Goal / expected outcome

Positions and open orders (every 60 s), balances (every 5 min) and a full reconciliation incl. fills (end of day, Sydney) are compared across the venue (read-only key), the engine's portfolio state and the journal (16 §2.9 defaults); each difference is classified explained (matched to a known journal event within 24 h) or unexplained and written to `audit.recon` with its age.

## Context & references

- Roadmap: [R7.09 · ToDo T7.23](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (reconciliation cadence, tolerance and the 24 h 'explained' rule) · [16 §2.9](../../../docs/16-configuration-and-safety-model.md#29-reconciliation) · [17 §C P7-B007](../../../docs/17-decisions-register.md#c-defaults-that-were-n-or-unspecified) · [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) (venue disconnect → unconfirmed) · [12 §3](../../../docs/12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention) (STP cancels recorded as non-fills) · [D07](../../../docs/ui/dashboards/D07-data-quality.md) Reconciliation tab · [D05](../../../docs/ui/dashboards/D05-execution.md) (reconciliation status per position)
- Cross-phase (`depends_on`): P1-T041/P1-T042 (venue recon on testnets and practice accounts), P3-T034 (journal ↔ venue recon). This task joins them into one three-way job for live sub-accounts; it is built and tested keyless (recorded fixtures, venue mock, sandbox paper venue); live read-only keys arrive with P7-T007 and are exercised in P7-T047.
- Related: P7-T026 (unconfirmed state), P7-T027 (24 h ageing → halt), P7-T050 (fault injection), gap P7-B007 (resolved: 16 §2.9)

## Requirements

- Sides: venue (REST via read-only key, rate-limit aware from live headers), engine (Nautilus portfolio/cache snapshot via `pos.{account}`), journal (`journal.*` positions/balances).
- Cadence (16 §2.9 defaults, settings): positions and open orders every 60 s; balances every 5 min; full reconciliation at end of day (Sydney); on-demand `data.recon.run` (C1).
- Tolerances (16 §2.9): position quantities match exactly; balances within 0.01% or dust (dust threshold per asset, a setting).
- Explained = matched to a known journal event within 24 h (16 §2.9). Matching rules (each with a rule id): fill in flight (< 30 s old), STP cancel (non-fill), funding settlement, recorded deposit/withdrawal (manual), fee event. Anything not matched within 24 h is `unexplained` (kill criterion, P7-T027); `first_seen_at` is stored.
- Outputs: `audit.recon` rows (WORM), NATS `recon.{account}`, D07/D05/D14 status; an unexplained break raises `alert.warning.recon` immediately and stays visible until resolved by a correction row.
- Resolution is a new row (`resolution_of`) with reason; never an edit.

## ToDo

- [ ] `packages/mt_monitor/recon/three_way.py` with side adapters (venue via ccxt/native read-only; engine snapshot RPC; journal SQL).
- [ ] Explanation rules module with unit-tested rule ids.
- [ ] Scheduler (monitor service loop: 60 s positions/orders, 5 min balances) + EOD (Sydney) Prefect flow.
- [ ] `data.recon.resolve` command (C1, reason required) writing resolution rows.
- [ ] D07 Reconciliation tab: three columns (venue/engine/journal), age, rule, resolve action.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: each explanation rule with positive/negative fixtures.
- Integration (venue mock + sandbox paper venue, no keys): clean run → zero breaks; injected phantom position on the engine side → break within one 60 s interval, `unexplained` after 24 h without a matching journal event.
- WORM: recon rows immutable; resolution creates a new row.

### Scenarios
- Given an STP cancel, then recon marks the missing fill as explained (rule `stp_cancel`) and the journal shows a non-fill.
- Given the journal is missing a fee event, then an unexplained balance break appears with venue vs journal values.
- Given venue REST rate-limited, then the run is `incomplete` (not clean) and retries with backoff.

### Stress / failure injection
- 10 sub-accounts at the 60 s / 5 min cadence for 24 h against the venue mock with real rate-limit headers: no missed runs; 418/429 respected (no retry storms); positions run p95 < 10 s.

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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (16 §2.9 defaults: 60 s positions/orders, 5 min balances, EOD Sydney, exact qty, 0.01%/dust, 24 h explained rule (P7-B007); keyless build; deps P1-T041/T042, P3-T034)
