---
id: P3-T053
kind: task
title: Start the one-month fully journalled and reconciled paper run
phase: 3
type: RUN
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T013, P3-T014, P3-T034, P3-T009, P3-T042]
requirements: [R3.01, R3.11]
roadmap_todos: [T3.80]
modules: [M18]
dashboards: [D14, D07]
branch: p3/P3-T053-run-start-month-journalled-paper
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-T053 · Start the one-month fully journalled and reconciled paper run

## Goal / expected outcome

One calendar month of the P2 paper clock's trades is journalled automatically and reconciled daily with zero unexplained breaks; this item starts the run, monitors the first 7 days in-phase, and hands the remaining days to the P7 weekly review if the month outlasts the phase.

## Context & references

- Roadmap: [T3.80](../../../docs/roadmap/phase-3-journal-and-tax.md) · exit criterion 1
- Cross-phase: P2 T2.80 (paper clock running), P7 R7.03 (weekly review includes journal reconciliation) where completion is checked if the month outlasts P3
- Runbook: P3-T044

## Requirements

- Start date = the first day all of P3-T013/T014/T034 are live in production compose; end = start + 1 calendar month.
- Daily: recon status `ok` or `explained` for every account; an unexplained break fails the run and the month restarts after the fix.
- Weekly summary (progress log): events by type, fills vs `audit.fill` count, breaks + explanations, ingest p95.
- In-phase close condition: run started and first 7 consecutive days with zero unexplained breaks; the remaining days are checked by the P7 weekly review (T7.05) — the roadmap box T3.80 is ticked only when the full month is clean.

## ToDo

- [ ] Record the start date in the progress log
- [ ] Check D14 recon widget daily; log weekly summaries
- [ ] Follow the runbook for any break; restart the clock if one stays unexplained
- [ ] Hand-off note to P7 if the month extends past the phase exit

## Verification

### Tests

- Evidence = 30/31 `audit.recon` journal-scope days with no unexplained `break`.

### Scenarios

- Given a break explained by a late funding posting, when the next day reconciles, then the run continues (explained ≠ unexplained).

### Stress / failure injection

- n/a: elapsed-time run

## Acceptance criteria

- [ ] Run started (date logged)
- [ ] First 7 days zero unexplained breaks
- [ ] Hand-off or completion recorded

## Exceptions & edge cases

- Testnet reset during the month → account epoch handling; does not count as a break if explained by the epoch event.

## Cardinal rules (do NOT)

- Do NOT mark breaks as explained without a cause reference.
- Do NOT pause the paper clock to avoid breaks.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Keys stay read-only/trade-only, IP-locked, withdrawals disabled; no live money before the P7 gates.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-7-prove-and-go-live.md`: if handed off, note in the P7 weekly review that T3.80 completion is checked there (main agent).
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.80 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T053-run-start-month-journalled-paper`
- PR title: `P3-T053: Start the one-month fully journalled and reconciled paper run`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T053` run

## Progress log

- 2026-10-21 00:00 · planner · created
