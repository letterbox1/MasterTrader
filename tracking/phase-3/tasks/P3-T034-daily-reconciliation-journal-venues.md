---
id: P3-T034
kind: task
title: Daily reconciliation job between journal and venues
phase: 3
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T013, P3-T014, P3-T018, P1-T041, P1-T042]
requirements: [R3.11]
roadmap_todos: [T3.28]
modules: [M18, M16]
dashboards: [D14, D07]
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, prefect-server, nats]
branch: p3/P3-T034-daily-reconciliation-journal-venues
pr: ""
doc_sync: [docs/ui/dashboards/D14-journal.md, docs/03-build-spec.md, docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T034 · Daily reconciliation job between journal and venues

## Goal / expected outcome

Every day after venue EOD, a Prefect flow compares journal-derived balances and positions per account and asset against each venue's read-only balances (and against `audit.fill` counts), writes the result to `audit.recon` with `scope = journal`, and raises an incident for any mismatch above tolerance — the evidence for the 1-month zero-break run.

## Context & references

- Roadmap: [R3.11, T3.28](../../../docs/roadmap/phase-3-journal-and-tax.md) · [09 quality](../../../docs/09-journal-and-tax.md#quality) (journal balances reconcile to venue balances daily)
- D14 Reconciliation status widget (`/data/recon?scope=journal`) [D14](../../../docs/ui/dashboards/D14-journal.md) · M16 owns `audit.recon` ([02 §4](../../../docs/02-v1-architecture.md#4-logical-components))
- Cross-phase prerequisites (depends_on): P1-T041 (crypto testnet recon clients), P1-T042 (OANDA/IG/Alpaca/IBKR paper recon clients); P7 T7.23 (three-way hardening) builds on this
- Tolerances and "explained": [16 §2.9](../../../docs/16-configuration-and-safety-model.md#29-reconciliation) (positions exact; balances within 0.01% or dust; explained = matched to a known journal event within 24 h)
- Built and tested against recorded venue responses; the live practice/testnet recon runs in the RUN item P3-T053 with read-only keys

## Requirements

- Schedule `journal-recon-daily` at 01:30 Australia/Sydney (after UTC-midnight funding settlements) + on demand via `data.recon.run` (scope journal).
- Checks per account (tolerances are the 16 §2.9 settings, never constants): (a) asset quantities: journal holdings vs venue balances (position quantities exact; balances within 0.01% or dust); (b) fill count and fee totals: journal vs `audit.fill` for the day; (c) open positions vs venue positions (derivatives); (d) unmatched transfers older than the window.
- Result rows: `audit.recon` (WORM) {scope, account, asset, journal_qty, venue_qty, diff, status ok|break|explained, explanation_ref}.
- Break → `alert.warning.recon_break` (Telegram + ntfy + UI) and an incident record; a break not matched to a known journal event within 24 h (default, 16 §2.9) is **unexplained** → `alert.critical` incident. (In live trading an unexplained mismatch is a kill criterion handled by M16/M11 in P7; journal-scope recon raises the incident.)
- Explaining a break = an audited annotation linking the cause (e.g. venue delay) — never editing journal data; true errors fixed by correction events.

## ToDo

- [ ] Implement `packages/mt_journal/recon/daily.py` reusing P1 read-only venue clients
- [ ] Write `audit.recon` rows + alerts
- [ ] `recon.explain` annotation path (command `journal.note.add` with recon ref)
- [ ] Prefect deployment; tests; docs

## Verification

### Tests

- Integration (recorded venue responses, no keys): fixture venue balances equal → all `ok`; inject a missing funding event → `break` on that asset with diff = funding amount.
- Unit: tolerance rules per asset type.
- Unit: escalation to unexplained/critical after the 24 h explain window (setting).

### Scenarios

- Given a venue API outage at recon time, when the flow runs, then status `skipped_venue_unavailable` is recorded (not ok) and retried hourly up to 6 times.
- Given a break explained by a late deposit, when the next day reconciles, then the break closes automatically and history keeps both rows.

### Stress / failure injection

- Reconcile 20 accounts × 50 assets < 5 min within venue rate limits (quota tracker).

## Acceptance criteria

- [ ] Daily recon rows for every registered account
- [ ] Breaks alert on all channels
- [ ] Zero edits to journal data from recon
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Testnet balance resets → account epoch handling; recon compares from the epoch.
- Dust conversions/venue-side rounding → explained by rule, not tolerance creep.

## Cardinal rules (do NOT)

- Do NOT widen tolerances to make a break disappear.
- Do NOT use keys with trade/withdraw scope.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Keys stay read-only/trade-only, IP-locked, withdrawals disabled; no live money before the P7 gates.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/ui/dashboards/D14-journal.md`: confirm recon widget fields; `docs/03-build-spec.md` M16: note journal-scope recon.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.28 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T034-daily-reconciliation-journal-venues`
- PR title: `P3-T034: Daily reconciliation job between journal and venues`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T034` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (tolerances and 24 h explain window from 16 §2.9 (replaces 0.01 unit / 2-day rule); built on recorded responses; explicit P1 depends_on; tools/services filled)
