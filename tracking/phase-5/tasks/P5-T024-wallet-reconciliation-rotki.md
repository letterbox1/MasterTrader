---
id: P5-T024
kind: task
title: Wallet reconciliation: daily vs journal, monthly vs rotki
phase: 5
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T023]
requirements: [R5.05]
roadmap_todos: [T5.22]
modules: [M22, M18, M16]
dashboards: [D18, D07]
branch: p5/P5-T024-wallet-reconciliation-rotki
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/09-journal-and-tax.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T024 · Wallet reconciliation: daily vs journal, monthly vs rotki

## Goal / expected outcome

A daily Prefect flow reconciles every registered wallet's indexed balance with the journal-implied balance and writes `ops.recon_wallet_result`; a monthly flow exports addresses to a self-hosted **rotki** and compares its decoded events/balances; any unexplained break is an incident and shows in D18/D07.

## Context & references

- Roadmap: [R5.05](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.22 · verified by P5-T059
- [13 §3 step 3](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view) · [09 quality](../../../docs/09-journal-and-tax.md) · P3 recon (R3.11) and P1 recon (R1.12)
- rotki is AGPL — fine privately ([09 tools table](../../../docs/09-journal-and-tax.md))

## Requirements

- Daily (after 00:30 AEST): per wallet per asset, `indexed − journal` within tolerance (dust ≤ 1e-9 native or ≤ A$0.01) else a break with candidate explanations (missing classification, pending reorg, unpriced token).
- Monthly: rotki sidecar (pinned digest, internal network, no telemetry) fed with registered addresses; diff its balances/events against ours; report.
- Breaks published as `alert.warning.recon_wallet`; unexplained > 24 h escalates to critical (aligns with P7 R7.06 "unexplained recon mismatch > 24 h halts everything").
- Recon report downloadable (CSV) and linked from D18.

## ToDo

- [ ] Implement `packages/mt_treasury/recon/daily.py` and `monthly_rotki.py` Prefect flows.
- [ ] Add rotki service to `services/` compose profile with digest; disable any telemetry/update checks.
- [ ] Write results table and `/data/recon?kind=wallet` endpoint.
- [ ] Tests; doc sync.

## Verification

### Tests
- Integration: seeded journal + snapshots with one missing event → exactly one break with the right candidate cause.
- Integration: rotki export/import round-trip on fixtures.
- Unit: tolerance handling with Decimal.

### Scenarios
- Given a classified airdrop receipt not yet journalled (reorg window), when recon runs, then status `pending_finality`, not a break.
- Given an unexplained break older than 24 h, then a critical alert and a `REVOKE_APPROVAL`/investigate task are raised.

### Stress / failure injection
- Recon over 200 wallets × 50 assets < 2 min.

## Acceptance criteria

- [ ] Daily recon writes results for every wallet
- [ ] Monthly rotki comparison report produced
- [ ] Breaks alert and escalate after 24 h

## Exceptions & edge cases

- rotki down at month-end: retry daily for 7 days, then a task; daily recon unaffected.

## Cardinal rules (do NOT)

- Do NOT "fix" a break by inserting a balancing journal entry without an explained cause and a correction row.
- Do NOT UPDATE or DELETE WORM rows (`curation.mandate`, `curation.exec_log`, the signer ledger, `journal.*`, `audit.*`); corrections are new rows with `supersedes_id` (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §3: recon tolerances.
- `docs/09-journal-and-tax.md`: wallet recon added to quality checks.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.22 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T024-wallet-reconciliation-rotki`
- PR title: `P5-T024: Wallet reconciliation: daily vs journal, monthly vs rotki`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T024` run

## Progress log

- 2026-10-21 00:00 · planner · created
