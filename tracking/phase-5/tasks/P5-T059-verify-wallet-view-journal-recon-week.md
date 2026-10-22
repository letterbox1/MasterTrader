---
id: P5-T059
kind: task
title: Wallet view reconciles with the journal for a test week
phase: 5
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T024, P5-T005, P5-T050, P5-T068]
requirements: [R5.05]
roadmap_todos: [T5.65]
modules: [M22, M18]
dashboards: [D18]
tools: [uv]
mcp: []
env: [HELIUS_API_KEY, ALCHEMY_API_KEY]
services: [postgres, helius, alchemy]
branch: p5/P5-T059-verify-wallet-view-journal-recon-week
pr: ""
doc_sync: [docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T059 · Wallet view reconciles with the journal for a test week

## Goal / expected outcome

For seven consecutive days after you register every wallet, the daily recon shows D18 totals equal to journal-implied balances for every registered wallet with zero unexplained breaks (or each break explained and corrected by append-only rows) — exit criterion 3 (reconciliation part).

## Context & references

- Roadmap: ToDo T5.65 → [R5.05](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) ("Recon report") · exit criterion 3
- Recon P5-T024 · registration P5-T005 · live reads proven in P5-T068 · tolerance and the 24 h "explained" rule per [16 §2.9](../../../docs/16-configuration-and-safety-model.md#29-reconciliation)

## Requirements

- Window: 7 days including at least one sweep, one claim (testnet ok), one internal transfer and one exchange movement.
- Report: per-day table (wallets, assets, breaks, explained, unexplained) attached to the progress log.
- Pass: 0 unexplained breaks at day end for 7 days; D18 net worth equals journal total within tolerance.

## ToDo

- [ ] Start the window after P5-T005 is done; monitor daily recon.
- [ ] Investigate each break; file bugs for classifier gaps.
- [ ] Compile the 7-day report.

## Verification

### Tests
- Daily recon outputs (no new code unless a bug is found).

### Scenarios
- Given an unexplained break on day 4, then the root cause is fixed (bug item) and the 7-day window restarts.

### Stress / failure injection
- n/a: observation window

## Acceptance criteria

- [ ] 7 consecutive clean days recorded
- [ ] Report attached to the progress log

## Exceptions & edge cases

- Provider outage on a day: that day counts only if recon completed with fallback data.

## Cardinal rules (do NOT)

- Do NOT insert balancing entries to force a clean day.
- Do NOT UPDATE or DELETE WORM rows (`curation.mandate`, `curation.exec_log`, the signer ledger, `journal.*`, `audit.*`); corrections are new rows with `supersedes_id` (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- No doc change beyond ticking T5.65.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.65 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T059-verify-wallet-view-journal-recon-week`
- PR title: `P5-T059: Wallet view reconciles with the journal for a test week`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T059` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (live window after the keys-last check P5-T068; recon tolerance per 16 §2.9)
