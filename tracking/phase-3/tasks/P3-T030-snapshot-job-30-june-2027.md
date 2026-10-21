---
id: P3-T030
kind: task
title: 30 June 2027 market-value snapshot job for every open lot
phase: 3
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T019, P3-T011, P3-T009]
requirements: [R3.08]
roadmap_todos: [T3.25]
modules: [M18, M1]
dashboards: [D15]
branch: p3/P3-T030-snapshot-job-30-june-2027
pr: ""
doc_sync: [docs/09-journal-and-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-T030 · 30 June 2027 market-value snapshot job for every open lot

## Goal / expected outcome

An idempotent Prefect flow values **every open lot** (all accounts, all asset classes incl. FX-cash lots) at **2027-06-30 23:59:59 AEST (13:59:59Z)**, records value, price, price source and timestamp per lot in `journal.lot_snapshot`, runs regardless of the reform flag, and is reusable for residency-change (CGT event I1) snapshots.

## Context & references

- Roadmap: [R3.08, T3.25](../../../docs/roadmap/phase-3-journal-and-tax.md) · [roadmap README §4 fixed dates](../../../docs/roadmap/README.md#4-fixed-external-dates)
- [09 key findings](../../../docs/09-journal-and-tax.md#️-key-findings-that-shape-the-design) (end of day AEST, price source recorded) · [02 F9 step 6](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Related: P3-T004 (diary), P3-T044 (runbook), P3-T048 (dry run), P3-B002 (price convention)

## Requirements

- Deployment `journal-snapshot-2027-06-30` scheduled once at 2027-07-01 00:15 AEST (after the valuation instant) with retries every 30 min for 7 days; parameter `valuation_ts = 2027-06-30T13:59:59Z`, `kind = reform_2027`.
- Price rule per asset class (default until P3-B002 resolved): crypto → last 1m bar close ≤ valuation_ts on the preferred venue (P3-T011); FX/cash → RBA F11 30 June 2027; listed equities/ETFs → last official close ≤ valuation_ts on the home exchange (US close of 29 June NY time = 30 June morning AEST, AU close of 30 June); unlisted/illiquid → `needs_valuation` (never zero).
- Uses only recorded data via `pit(as_of=valuation_ts)`; can run late (host down) with identical results.
- Idempotent: unique (`kind`, `valuation_ts`, `lot_id`); re-runs skip existing rows; a corrected price writes a superseding row with reason.
- Completeness check: count(snapshot rows) = count(open lots at valuation_ts); otherwise alert critical + D15 Lots banner.
- Generic `snapshot(kind, valuation_ts)` API reused by P3-T031 (I1).

## ToDo

- [ ] Implement `packages/mt_journal/snapshots/job.py` + price rule module
- [ ] Prefect deployment + schedule in `infra/prefect/deployments/journal.yaml`
- [ ] Completeness check + alert; D15 Lots status query
- [ ] Tests (dry run in P3-T048); docs

## Verification

### Tests

- Integration: fixture DB with open lots across crypto/FX/equity → snapshot rows with source strings; re-run creates no new rows.
- Unit: `pit` used (look-ahead test: a bar after valuation_ts is never used).
- Unit: illiquid token → `needs_valuation`, completeness alert.

### Scenarios

- Given the host was down on 30 June, when the flow runs on 2 July, then values equal those a 1 July run would produce.
- Given the AU_2027_REFORM flag is off, when the date arrives, then the snapshot still runs (it costs nothing).

### Stress / failure injection

- Snapshot 200k open lots < 10 min; kill the worker mid-run 3× → completes with no duplicates.

## Acceptance criteria

- [ ] Flow deployed with the fixed schedule
- [ ] Idempotency and completeness checks proven
- [ ] Every snapshot row has price, source and timestamp
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Exchange outage at the valuation minute → previous available bar within 60 min, flagged `stale_price`; beyond that → next venue in the preference list.
- Lots in transit (withdrawal unmatched) → valued and flagged `in_transit`.

## Cardinal rules (do NOT)

- Do NOT fetch live prices at run time; use recorded data only.
- Do NOT overwrite snapshot rows.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/09-journal-and-tax.md`: state the valuation instant and the per-asset-class price rule.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.25 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T030-snapshot-job-30-june-2027`
- PR title: `P3-T030: 30 June 2027 market-value snapshot job for every open lot`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T030` run

## Progress log

- 2026-10-21 00:00 · planner · created
