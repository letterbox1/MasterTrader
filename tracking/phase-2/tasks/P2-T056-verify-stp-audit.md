---
id: P2-T056
kind: task
title: "STP audit: explicit STP on every order per venue"
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
tools: [uv]
mcp: []
env: []
services: [postgres]
branch: p2/P2-T056-verify-stp-audit
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T056 · STP audit: explicit STP on every order per venue

## Goal / expected outcome

A query over `audit.order` and captured venue payloads proves that every order sent to an STP-capable venue carried an explicit STP parameter, that netting brokers (OANDA, IG, Alpaca, IBKR) are recorded `n/a_netting` and run one strategy per account/sub-account, and that STP cancels are recorded as non-fills.

## Context & references

- Roadmap: [R2.31](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.63
- Policy: [12 §3](../../../docs/12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention)
- Decision: [17 §D P2-B006](../../../docs/17-decisions-register.md#d-other-decisions) (netting brokers `stp: n/a (netting)`; one strategy per account/sub-account).
- Build first, keys last: run on sandbox + mock venues (recorded payloads); the same `mt audit stp` check runs over the live testnet window in P2-T071.

## Requirements

- SQL check: `SELECT venue, count(*) FILTER (WHERE stp_mode IS NULL) FROM audit.order` = 0 per venue over the test window; STP-capable venues never show `n/a_netting`; netting venues always do.
- Netting check: no netting account/sub-account carries bots of two strategies with overlapping instruments (`mt audit stp --netting`).
- Payload capture (adapter request log, secrets scrubbed) matches `audit.order.stp_mode`.
- Induced self-match on a mock Binance venue replaying recorded EXPIRE_BOTH responses (two strategies, one account) → both expired, recorded `stp_cancelled`, recon tag present.
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
- Given 24 h of paper trading across sandbox and mock venues, when `mt audit stp` runs, then 0 orders on STP-capable venues lack STP and every netting-venue order is `n/a_netting`.

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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (STP-capable vs netting venues (17 §D P2-B006), keyless mock self-match; live window in P2-T071)
