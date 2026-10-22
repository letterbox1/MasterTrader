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
depends_on: [P3-T011, P3-T019, P3-T009, P1-T012, P1-T020, P1-T021, P1-T023]
requirements: [R3.08, R3.15]
roadmap_todos: [T3.25, T3.31]
modules: [M18, M1]
dashboards: [D15]
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, prefect-server]
branch: p3/P3-T030-snapshot-job-30-june-2027
pr: ""
doc_sync: [docs/09-journal-and-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T030 · 30 June 2027 market-value snapshot job for every open lot

## Goal / expected outcome

An idempotent Prefect flow values **every open lot** (all accounts, all asset classes incl. FX-cash lots) at **2027-06-30 23:59:59 AEST (13:59:59Z)**, records value, price, price source, method and timestamps per lot in `journal.lot_snapshot` using the per-asset-class convention of [16 §4.2](../../../docs/16-configuration-and-safety-model.md#42-market-value-snapshot-30-june-2027-and-any-residency-change), runs regardless of the reform flag, and is reusable for residency-change (CGT event I1) snapshots.

## Context & references

- Roadmap: [R3.08, T3.25](../../../docs/roadmap/phase-3-journal-and-tax.md) · [roadmap README §4 fixed dates](../../../docs/roadmap/README.md#4-fixed-external-dates)
- [09 key findings](../../../docs/09-journal-and-tax.md#️-key-findings-that-shape-the-design) (end of day AEST, price source recorded) · [02 F9 step 6](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Convention: [16 §4.2](../../../docs/16-configuration-and-safety-model.md#42-market-value-snapshot-30-june-2027-and-any-residency-change) · decision [17 §A P3-B002](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (defaults, your tax agent to confirm, 09 question 10) · prices via `snapshot_price` in P3-T011
- Cross-phase prerequisites (depends_on): P1-T012 (recorded crypto trades), P1-T020 (RBA F11), P1-T021 (recorded US trades), P1-T023 (official daily closes)
- Related: P3-T004 (diary), P3-T044 (runbook), P3-T048 (dry run)

## Requirements

- Deployment `journal-snapshot-2027-06-30` scheduled once at 2027-07-01 00:15 AEST (after the valuation instant) with retries every 30 min for 7 days; parameter `valuation_ts = 2027-06-30T13:59:59Z`, `kind = reform_2027`.
- Price rule per asset class (16 §4.2 defaults, per-asset-class settings): **crypto** → VWAP of recorded trades 23:55:00–23:59:59 AEST on the primary venue; **ASX** → official close on the day; **US/EU listed** → last trade at or before 23:59:59 AEST from recorded data (the US session is open then), else the previous official close; **FX/cash** → RBA rate for the day (last business day if none published); unlisted/illiquid → the 16 §4.1 hierarchy (pool price) else `needs_valuation` (never zero). Each row records source, method and timestamps.
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

- No recorded trades in the 23:55:00–23:59:59 window on the primary venue (outage) → the next configured venue for the same window, flagged `fallback_venue`; none → `needs_valuation` and a critical alert (never zero, never a live fetch).
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

- `docs/09-journal-and-tax.md`: confirm the snapshot rows record source, method and timestamps as built (convention already in 16 §4.2).
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.25 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T030-snapshot-job-30-june-2027`
- PR title: `P3-T030: 30 June 2027 market-value snapshot job for every open lot`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T030` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (price rule now the 16 §4.2 convention (P3-B002 closed), replaces bar-close default; R3.15/T3.31 mapped; explicit P1 depends_on; tools/services filled)
