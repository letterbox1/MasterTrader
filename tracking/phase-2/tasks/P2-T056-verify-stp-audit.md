---
id: P2-T056
kind: task
title: STP audit: explicit STP on every order per venue
phase: 2
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T022, P2-T023, P2-T024, P2-T025, P2-T026]
requirements: [R2.31]
roadmap_todos: [T2.63]
modules: [M12]
dashboards: []
branch: p2/P2-T056-verify-stp-audit
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T056 · STP audit: explicit STP on every order per venue

## Goal / expected outcome

A query over `audit.order` and captured venue payloads proves that every order sent to every venue carried an explicit STP parameter (or `engine_guard` where the venue has none), and STP cancels are recorded as non-fills.

## Context & references

- Roadmap: [R2.31](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.63
- Policy: [12 §3](../../../docs/12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention)
- Related: P2-B006.

## Requirements

- SQL check: `SELECT venue, count(*) FILTER (WHERE stp_mode IS NULL) FROM audit.order` = 0 per venue over the test window.
- Payload capture (adapter request log, secrets scrubbed) matches `audit.order.stp_mode`.
- Induced self-match on Binance testnet (two strategies, one account) → both expired, recorded `stp_cancelled`, recon tag present.
- Saved as a reusable check `mt audit stp --since` for P7.

## ToDo

- [ ] Write the check command
- [ ] Run over a 24 h paper window + induced self-match
- [ ] Report in progress log
- [ ] Record results (numbers, run IDs, screenshots) in the progress log and tick the roadmap ToDo box

## Verification

### Tests
- The check itself + induced self-match test.

### Scenarios
- Given 24 h of paper trading across all venues, when `mt audit stp` runs, then 0 orders lack STP.

### Stress / failure injection
- n/a: audit query.

## Acceptance criteria

- [ ] 0 orders without STP per venue
- [ ] Self-match case recorded as non-fills

## Exceptions & edge cases

- Orders rejected pre-submit (never sent) excluded from the count.

## Cardinal rules (do NOT)

- Do NOT count venue-default STP as explicit.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/12-policy-and-compliance.md` §3: reference the audit command.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.63 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T056-verify-stp-audit`
- PR title: `P2-T056: STP audit: explicit STP on every order per venue`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T056` run

## Progress log

- 2026-10-21 00:00 · planner · created
